#!/usr/bin/env python3
"""
Enhanced Seamless Pipeline: CSV Splitter -> RML Generator -> KG Generator -> GraphDB Importer -> Evaluation
This pipeline takes a large CSV file, splits it by device, generates RML files,
creates a complete knowledge graph using SDM-RDFizer, can optionally import
the result into a GraphDB repository, and includes comprehensive evaluation.

ENHANCED: Each pipeline run creates a unique timestamped output folder with full evaluation capabilities.
"""

import os
import sys
import argparse
import logging
import glob
import subprocess
import configparser
import time
import json
import re
import threading
import psutil
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional, Tuple

# Import the functions from your existing scripts
try:
    from CSV_Device_Seperator_With_TimeFormat import split_csv_by_device, setup_logging as setup_splitter_logging
    from RML_Generation import profile_execution
except ImportError as e:
    print(f"Error importing modules: {e}")
    print("Make sure csv_splitter.py and rml_generator.py are in the same directory or Python path")
    sys.exit(1)

# Import requests for GraphDB interaction, optional
try:
    import requests
except ImportError:
    requests = None

# Import rdflib for accurate triple counting
try:
    import rdflib
except ImportError:
    rdflib = None


class ResourceMonitor:
    """Monitors system resources (CPU, RAM) during pipeline execution."""

    def __init__(self, monitor_interval: float = 1.0):
        self.monitor_interval = monitor_interval
        self.monitoring = False
        self.monitor_thread = None
        self.metrics: Dict[str, list] = {
            'cpu_percent': [],
            'memory_rss_mb': [],
            'timestamps': []
        }
        self.logger = logging.getLogger('ResourceMonitor')

    def start_monitoring(self):
        """Start resource monitoring in a separate thread."""
        self.monitoring = True
        self.monitor_thread = threading.Thread(target=self._monitor_resources, daemon=True)
        self.monitor_thread.start()
        self.logger.info("Resource monitoring started.")

    def stop_monitoring(self):
        """Stop resource monitoring."""
        if self.monitoring:
            self.monitoring = False
            if self.monitor_thread:
                self.monitor_thread.join()
            self.logger.info("Resource monitoring stopped.")

    def _monitor_resources(self):
        """The core monitoring loop that runs in a thread."""
        process = psutil.Process(os.getpid())
        while self.monitoring:
            try:
                cpu_percent = psutil.cpu_percent(interval=None)
                memory_rss_mb = process.memory_info().rss / (1024 * 1024)

                self.metrics['cpu_percent'].append(cpu_percent)
                self.metrics['memory_rss_mb'].append(memory_rss_mb)
                self.metrics['timestamps'].append(time.time())

                time.sleep(self.monitor_interval)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                self.logger.warning("Monitoring stopped unexpectedly; process may have ended.")
                break
            except Exception as e:
                self.logger.error(f"Error during resource monitoring: {e}", exc_info=True)
                break

    def get_summary_stats(self) -> Dict[str, Any]:
        """Calculate and return summary statistics of resource usage."""
        if not self.metrics['cpu_percent']:
            return {}

        cpu = self.metrics['cpu_percent']
        mem = self.metrics['memory_rss_mb']

        return {
            'monitoring_duration_sec': self.metrics['timestamps'][-1] - self.metrics['timestamps'][0] if self.metrics[
                'timestamps'] else 0,
            'cpu_percent': {'avg': sum(cpu) / len(cpu), 'max': max(cpu), 'min': min(cpu)},
            'memory_rss_mb': {'avg': sum(mem) / len(mem), 'max': max(mem), 'min': min(mem)}
        }


class KnowledgeGraphAnalyzer:
    """Analyzes knowledge graph files for triple counts and size using rdflib."""

    def __init__(self):
        self.logger = logging.getLogger('KGAnalyzer')
        self.supported_formats = {
            '.ttl': 'turtle',
            '.nt': 'nt',
            '.rdf': 'xml',
            '.xml': 'xml',
            '.jsonld': 'json-ld'
        }

    def count_triples_in_file(self, file_path: str) -> Tuple[int, str]:
        """Accurately count triples in a knowledge graph file using rdflib."""
        if not rdflib:
            self.logger.warning("rdflib not available. Using file size estimation for triple count.")
            file_size_mb = os.path.getsize(file_path) / (1024 * 1024)
            estimated_triples = int(file_size_mb * 1000)  # Rough estimation
            return estimated_triples, 'estimated'

        file_ext = Path(file_path).suffix.lower()
        rdf_format = self.supported_formats.get(file_ext)

        if not rdf_format:
            self.logger.warning(f"Unsupported file extension '{file_ext}' for {file_path}. Skipping triple count.")
            return 0, 'unsupported'

        self.logger.debug(f"Analyzing '{os.path.basename(file_path)}' with format '{rdf_format}'...")
        try:
            g = rdflib.Graph()
            g.parse(file_path, format=rdf_format)
            num_triples = len(g)
            self.logger.debug(f"Found {num_triples} triples in '{os.path.basename(file_path)}'.")
            return num_triples, rdf_format
        except Exception as e:
            self.logger.error(f"Failed to parse {file_path} with rdflib: {e}")
            return 0, 'parse_error'

    def analyze_knowledge_graph_directory(self, kg_dir: str) -> Dict[str, Any]:
        """Analyzes all supported KG files in a directory."""
        self.logger.info(f"Analyzing knowledge graph directory: {kg_dir}")
        if not os.path.isdir(kg_dir):
            self.logger.error(f"KG directory not found: {kg_dir}")
            return {'error': f'Directory not found: {kg_dir}'}

        results: Dict[str, Any] = {
            'total_files': 0,
            'total_triples': 0,
            'total_size_mb': 0.0,
            'files': [],
            'formats': {}
        }

        kg_files = []
        for ext in self.supported_formats.keys():
            kg_files.extend(glob.glob(os.path.join(kg_dir, f'*{ext}')))

        results['total_files'] = len(kg_files)
        total_size_bytes = 0

        for file_path in kg_files:
            file_size_bytes = os.path.getsize(file_path)
            triple_count, file_format = self.count_triples_in_file(file_path)

            file_info = {
                'filename': os.path.basename(file_path),
                'size_mb': file_size_bytes / (1024 * 1024),
                'triple_count': triple_count,
                'format': file_format
            }

            results['files'].append(file_info)
            results['total_triples'] += triple_count
            total_size_bytes += file_size_bytes

            if file_format not in results['formats']:
                results['formats'][file_format] = {'files': 0, 'triples': 0}
            results['formats'][file_format]['files'] += 1
            results['formats'][file_format]['triples'] += triple_count

        results['total_size_mb'] = total_size_bytes / (1024 * 1024)
        self.logger.info(
            f"KG analysis complete. Found {results['total_triples']:,} triples across {results['total_files']} files.")
        return results


class PipelineEvaluator:
    """Evaluates the entire pipeline's output with comprehensive metrics."""

    def __init__(self, pipeline_output_dir: str, log_level: int = logging.INFO):
        self.pipeline_output_dir = os.path.abspath(pipeline_output_dir)
        self.log_level = log_level

        self.log_dir = os.path.join(self.pipeline_output_dir, 'logs')
        self.kg_output_dir = os.path.join(self.pipeline_output_dir, 'knowledge_graph')
        self.eval_output_dir = os.path.join(self.pipeline_output_dir, 'evaluation')

        os.makedirs(self.eval_output_dir, exist_ok=True)
        self.kg_analyzer = KnowledgeGraphAnalyzer()
        self.logger = logging.getLogger('PipelineEvaluator')

    def log_timing_metric(self, stage: str, duration_sec: float):
        """Log timing metrics in a structured format for later parsing."""
        timing_data = {"stage": stage, "duration_sec": duration_sec}
        self.logger.info(f"TIMING_METRIC: {json.dumps(timing_data)}")

    def parse_pipeline_log_for_timings(self) -> Dict[str, float]:
        """Parses the main pipeline log file to extract performance timings."""
        self.logger.info("Parsing pipeline log for performance timings...")
        log_pattern = os.path.join(self.log_dir, 'pipeline_*.log')
        log_files = glob.glob(log_pattern)

        if not log_files:
            self.logger.warning("No pipeline log file found. Per-stage timings will be unavailable.")
            return {}

        latest_log = max(log_files, key=os.path.getmtime)
        self.logger.info(f"Reading timings from: {os.path.basename(latest_log)}")

        timings = {}
        timing_regex = re.compile(r"TIMING_METRIC:\s*(\{.*\})")

        try:
            with open(latest_log, 'r', encoding='utf-8') as f:
                for line in f:
                    match = timing_regex.search(line)
                    if match:
                        try:
                            metric = json.loads(match.group(1))
                            stage = metric.get('stage')
                            duration = metric.get('duration_sec')
                            if stage and isinstance(duration, (int, float)):
                                timings[stage] = duration
                                self.logger.debug(f"Found timing for stage '{stage}': {duration:.2f}s")
                        except json.JSONDecodeError:
                            self.logger.warning(f"Could not parse timing metric JSON: {match.group(1)}")
            return timings
        except Exception as e:
            self.logger.error(f"Failed to read or parse log file {latest_log}: {e}", exc_info=True)
            return {}

    def run_full_evaluation(self, resource_stats: Optional[Dict] = None) -> Optional[Dict[str, Any]]:
        """Runs the complete evaluation and generates a report."""
        self.logger.info("=" * 60)
        self.logger.info(f"STARTING EVALUATION FOR: {self.pipeline_output_dir}")
        self.logger.info("=" * 60)

        try:
            kg_results = self.kg_analyzer.analyze_knowledge_graph_directory(self.kg_output_dir)
            performance_timings = self.parse_pipeline_log_for_timings()

            evaluation_report = {
                'evaluation_timestamp': datetime.now().isoformat(),
                'pipeline_output_dir': self.pipeline_output_dir,
                'performance_metrics': {
                    'total_pipeline_time_sec': performance_timings.get('total_pipeline', 0.0),
                    'stages_sec': {k: v for k, v in performance_timings.items() if k != 'total_pipeline'}
                },
                'knowledge_graph_metrics': kg_results
            }

            if resource_stats:
                evaluation_report['resource_metrics'] = resource_stats

            total_time = evaluation_report['performance_metrics']['total_pipeline_time_sec']
            total_triples = kg_results.get('total_triples', 0)
            if total_time > 0 and total_triples > 0:
                evaluation_report['performance_metrics']['triples_per_second'] = total_triples / total_time

            self.save_evaluation_report(evaluation_report)
            self.print_evaluation_summary(evaluation_report)

            return evaluation_report

        except Exception as e:
            self.logger.critical(f"A critical error occurred during evaluation: {e}", exc_info=True)
            return None

    def save_evaluation_report(self, report: Dict[str, Any]):
        """Saves the final evaluation report to a JSON file."""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_file = os.path.join(self.eval_output_dir, f'evaluation_report_{timestamp}.json')
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=4, default=str)
            self.logger.info(f"Full evaluation report saved to: {output_file}")
        except Exception as e:
            self.logger.error(f"Failed to save evaluation JSON report: {e}", exc_info=True)

    def print_evaluation_summary(self, report: Dict[str, Any]):
        """Prints a user-friendly summary of the evaluation results."""
        print("\n" + "=" * 80)
        print("PIPELINE EVALUATION SUMMARY")
        print("=" * 80)

        perf = report.get('performance_metrics', {})
        print("📊 PERFORMANCE METRICS")
        total_time = perf.get('total_pipeline_time_sec', 0)
        print(f"  - Total Pipeline Execution Time: {total_time:.2f} seconds")
        for stage, duration in perf.get('stages_sec', {}).items():
            print(f"    - {stage.replace('_', ' ').title()} Time: {duration:.2f} seconds")
        if 'triples_per_second' in perf:
            print(f"  - Throughput: {perf['triples_per_second']:,.0f} triples/second")

        if 'resource_metrics' in report:
            resource = report['resource_metrics']
            print("\n🔧 RESOURCE USAGE")
            if 'cpu_percent' in resource:
                cpu = resource['cpu_percent']
                print(f"  - CPU Usage: Avg {cpu['avg']:.1f}%, Max {cpu['max']:.1f}%, Min {cpu['min']:.1f}%")
            if 'memory_rss_mb' in resource:
                mem = resource['memory_rss_mb']
                print(f"  - Memory Usage: Avg {mem['avg']:.1f}MB, Max {mem['max']:.1f}MB, Min {mem['min']:.1f}MB")

        print("\n✨ KNOWLEDGE GRAPH METRICS")
        kg = report.get('knowledge_graph_metrics', {})
        print(f"  - Total Triples Generated: {kg.get('total_triples', 0):,}")
        print(f"  - Total KG Size: {kg.get('total_size_mb', 0):.2f} MB")
        print(f"  - Number of KG Files: {kg.get('total_files', 0)}")
        if 'formats' in kg:
            for fmt, data in kg['formats'].items():
                print(f"    - Format '{fmt}': {data['files']} files with {data['triples']:,} triples")

        print("=" * 80)


class CSVToKnowledgeGraphPipeline:
    """
    Enhanced Pipeline class that orchestrates the complete process:
    CSV splitting -> RML generation -> KG creation -> GraphDB import -> Evaluation
    """

    def __init__(self, input_csv, output_base_dir='pipeline_output', log_level=logging.INFO, use_timestamp=True):
        self.input_csv = os.path.abspath(input_csv)
        self.log_level = log_level
        self.use_timestamp = use_timestamp

        self.timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

        if self.use_timestamp:
            timestamped_dir = f"{output_base_dir}_{self.timestamp}"
            self.output_base_dir = os.path.abspath(timestamped_dir)
        else:
            self.output_base_dir = os.path.abspath(output_base_dir)

        self.split_csv_dir = os.path.join(self.output_base_dir, 'split_csvs')
        self.rml_output_dir = os.path.join(self.output_base_dir, 'rml_files')
        self.kg_output_dir = os.path.join(self.output_base_dir, 'knowledge_graph')
        self.config_dir = os.path.join(self.output_base_dir, 'config')

        for directory in [self.split_csv_dir, self.rml_output_dir, self.kg_output_dir, self.config_dir]:
            os.makedirs(directory, exist_ok=True)

        self.setup_pipeline_logging()

        # Initialize evaluator
        self.evaluator = PipelineEvaluator(self.output_base_dir, log_level)

    def setup_pipeline_logging(self):
        """Setup logging for the pipeline with timestamped log files"""
        log_dir = os.path.join(self.output_base_dir, 'logs')
        os.makedirs(log_dir, exist_ok=True)

        log_file = os.path.join(log_dir, f'pipeline_{self.timestamp}.log')

        logging.basicConfig(
            level=self.log_level,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file, encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger('CSVToKnowledgeGraphPipeline')

        self.logger.info(f"Pipeline output directory: {self.output_base_dir}")
        self.logger.info(f"Pipeline timestamp: {self.timestamp}")

    def log_timing_metric(self, stage: str, duration_sec: float):
        """Log timing metrics for evaluation."""
        timing_data = {"stage": stage, "duration_sec": duration_sec}
        self.logger.info(f"TIMING_METRIC: {json.dumps(timing_data)}")

    def check_requests_installation(self):
        """Check if the 'requests' library is installed."""
        if requests is None:
            self.logger.error("The 'requests' library is required for GraphDB import but is not installed.")
            self.logger.error("Please install it by running: python3 -m pip install requests")
            return False
        self.logger.info("'requests' library is available.")
        return True

    def check_rdfizer_installation(self):
        """Check if SDM-RDFizer is installed and install if necessary"""
        self.logger.info("Checking SDM-RDFizer installation...")

        try:
            result = subprocess.run([sys.executable, '-c', 'import rdfizer'],
                                    capture_output=True, text=True)
            if result.returncode == 0:
                self.logger.info("SDM-RDFizer is already installed")
                return True
        except Exception:
            pass

        self.logger.info("SDM-RDFizer not found. Attempting to install...")
        try:
            subprocess.run([sys.executable, '-m', 'pip', 'install', 'rdfizer'],
                           check=True, capture_output=True, text=True)
            self.logger.info("Successfully installed SDM-RDFizer")
            return True
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Failed to install SDM-RDFizer: {e}")
            self.logger.error("Please install manually with: python3 -m pip install rdfizer")
            return False

    def generate_rdfizer_config(self, remove_duplicate=True, all_in_one_file=False,
                                enrichment=True, ordered=True, output_format='turtle'):
        """Generate the config.ini file for SDM-RDFizer based on available RML files"""
        self.logger.info("=" * 60)
        self.logger.info("STEP 4: GENERATING SDM-RDFIZER CONFIGURATION")
        self.logger.info("=" * 60)

        rml_pattern = os.path.join(self.rml_output_dir, "*.ttl")
        rml_files = glob.glob(rml_pattern)

        if not rml_files:
            raise FileNotFoundError(f"No RML files found in {self.rml_output_dir}")

        self.logger.info(f"Found {len(rml_files)} RML files for knowledge graph generation")

        config_file = os.path.join(self.config_dir, 'rdfizer_config.ini')

        config = configparser.ConfigParser()
        config.optionxform = str

        config['default'] = {
            'main_directory': self.output_base_dir
        }

        config['datasets'] = {
            'number_of_datasets': str(len(rml_files)),
            'output_folder': f"{self.kg_output_dir}",
            'remove_duplicate': 'yes' if remove_duplicate else 'no',
            'all_in_one_file': 'yes' if all_in_one_file else 'no',
            'name': 'joinCondition',
            'enrichment': 'yes' if enrichment else 'no',
            'ordered': 'yes' if ordered else 'no',
            'output_format': output_format
        }

        for i, rml_file in enumerate(rml_files, 1):
            rml_basename = os.path.basename(rml_file)
            dataset_name = rml_basename.replace('.ttl', '').replace('generated_', '').replace('.rml', '')

            config[f'dataset{i}'] = {
                'name': dataset_name,
                'mapping': rml_file
            }

            self.logger.info(f"Added dataset {i}: {dataset_name}")

        with open(config_file, 'w', encoding='utf-8') as f:
            config.write(f)

        self.logger.info(f"Generated RDFizer configuration: {config_file}")
        return config_file, rml_files

    def run_csv_splitter(self, time_col='Time', device_col=None, file_id=''):
        """Step 1: Split the input CSV by device"""
        self.logger.info("=" * 60)
        self.logger.info("STEP 1: SPLITTING CSV BY DEVICE")
        self.logger.info("=" * 60)

        start_time = time.time()
        try:
            devices = split_csv_by_device(
                input_file=self.input_csv,
                output_dir=self.split_csv_dir,
                time_col=time_col,
                device_col=device_col,
                file_id=file_id,
                log_level=self.log_level
            )

            duration = time.time() - start_time
            self.log_timing_metric('csv_splitter', duration)

            self.logger.info(f"Successfully split CSV into {len(devices)} device files")
            self.logger.info(f"Split files saved to: {self.split_csv_dir}")
            return devices

        except Exception as e:
            self.logger.error(f"Error in CSV splitting step: {str(e)}")
            raise

    def run_rml_generator(self, template_path=None, myprefix=None, wid=None, timestamp_column=None):
        """Step 2: Generate RML files for each split CSV"""
        self.logger.info("=" * 60)
        self.logger.info("STEP 2: GENERATING RML FILES")
        self.logger.info("=" * 60)

        start_time = time.time()
        csv_pattern = os.path.join(self.split_csv_dir, "*.csv")
        csv_files = glob.glob(csv_pattern)

        if not csv_files:
            raise FileNotFoundError(f"No CSV files found in {self.split_csv_dir}")

        self.logger.info(f"Found {len(csv_files)} CSV files to process")

        successful_generations = []
        failed_generations = []

        for csv_file in csv_files:
            try:
                csv_file_abs = os.path.abspath(csv_file)
                csv_file_rml = self.normalize_path_for_rml(csv_file_abs)
                self.logger.info(f"Generating RML for: {os.path.basename(csv_file_abs)}")

                result = profile_execution(
                    csv_path=csv_file_rml,
                    template_path=template_path,
                    output_dir=self.rml_output_dir,
                    myprefix=myprefix,
                    wid=wid,
                    timestamp_column=timestamp_column
                )

                successful_generations.append({
                    'csv_file': csv_file_rml,
                    'rml_file': result['output_file'],
                    'timestamp_column': result['timestamp_column']
                })

                self.logger.info(f"[SUCCESS] Successfully generated RML: {result['output_file']}")

            except Exception as e:
                self.logger.error(f"[FAILED] Failed to generate RML for {csv_file}: {str(e)}")
                failed_generations.append({
                    'csv_file': csv_file,
                    'error': str(e)
                })

        duration = time.time() - start_time
        self.log_timing_metric('rml_generator', duration)

        return successful_generations, failed_generations

    def validate_rml_paths(self):
        """Step 3: Validate that RML files contain absolute paths to CSV sources"""
        self.logger.info("=" * 60)
        self.logger.info("STEP 3: VALIDATING RML FILE PATHS")
        self.logger.info("=" * 60)

        start_time = time.time()
        rml_pattern = os.path.join(self.rml_output_dir, "*.ttl")
        rml_files = glob.glob(rml_pattern)
        validation_results = []

        for rml_file in rml_files:
            try:
                with open(rml_file, 'r', encoding='utf-8') as f:
                    content = f.read()

                lines = content.split('\n')
                source_lines = [line.strip() for line in lines if 'rml:source' in line]

                for line in source_lines:
                    if 'rml:source' in line:
                        start_idx = line.find('"') + 1
                        end_idx = line.rfind('"')
                        if start_idx > 0 and end_idx > start_idx:
                            source_path = line[start_idx:end_idx]
                            normalized_source_path = source_path.replace('\\', '/')
                            is_absolute = os.path.isabs(source_path)
                            file_exists = os.path.exists(source_path)
                            has_forward_slashes = '\\' not in source_path

                            validation_results.append({
                                'rml_file': os.path.basename(rml_file),
                                'source_path': source_path,
                                'normalized_path': normalized_source_path,
                                'is_absolute': is_absolute,
                                'file_exists': file_exists,
                                'has_forward_slashes': has_forward_slashes,
                                'status': 'OK' if is_absolute and file_exists and has_forward_slashes else 'ISSUE'
                            })

                            if is_absolute and file_exists and has_forward_slashes:
                                self.logger.info(f"[OK] {os.path.basename(rml_file)}: Valid absolute path")
                            else:
                                issues = []
                                if not is_absolute:
                                    issues.append("not absolute")
                                if not file_exists:
                                    issues.append("file not found")
                                if not has_forward_slashes:
                                    issues.append("contains backslashes")
                                self.logger.warning(f"[ISSUE] {os.path.basename(rml_file)}: {', '.join(issues)}")

            except Exception as e:
                self.logger.error(f"Error validating {rml_file}: {str(e)}")
                validation_results.append({
                    'rml_file': os.path.basename(rml_file),
                    'error': str(e),
                    'status': 'ERROR'
                })

        duration = time.time() - start_time
        self.log_timing_metric('rml_validation', duration)

        return validation_results

    def normalize_path_for_rml(self, path):
        """Normalize a path for RML by converting to absolute path with forward slashes"""
        abs_path = os.path.abspath(path)
        rml_path = abs_path.replace('\\', '/')
        return rml_path

    def fix_relative_paths_in_rml(self):
        """Fix any relative paths found in RML files by converting them to absolute paths"""
        self.logger.info("Fixing relative paths in RML files...")

        rml_pattern = os.path.join(self.rml_output_dir, "*.ttl")
        rml_files = glob.glob(rml_pattern)
        fixes_applied = 0

        for rml_file in rml_files:
            try:
                with open(rml_file, 'r', encoding='utf-8') as f:
                    content = f.read()

                original_content = content
                lines = content.split('\n')

                for i, line in enumerate(lines):
                    if 'rml:source' in line and '"' in line:
                        start_idx = line.find('"') + 1
                        end_idx = line.rfind('"')
                        if start_idx > 0 and end_idx > start_idx:
                            current_path = line[start_idx:end_idx]
                            needs_fixing = not os.path.isabs(current_path) or '\\' in current_path

                            if needs_fixing:
                                possible_paths = [
                                    current_path,
                                    os.path.join(self.split_csv_dir, os.path.basename(current_path)),
                                    os.path.join(os.getcwd(), current_path)
                                ]

                                for test_path in possible_paths:
                                    abs_test_path = os.path.abspath(test_path)
                                    if os.path.exists(abs_test_path):
                                        rml_normalized_path = self.normalize_path_for_rml(abs_test_path)
                                        new_line = line.replace(f'"{current_path}"', f'"{rml_normalized_path}"')
                                        lines[i] = new_line
                                        self.logger.info(f"[FIXED] Path in {os.path.basename(rml_file)}")
                                        fixes_applied += 1
                                        break

                new_content = '\n'.join(lines)
                if new_content != original_content:
                    with open(rml_file, 'w', encoding='utf-8') as f:
                        f.write(new_content)

            except Exception as e:
                self.logger.error(f"Error fixing paths in {rml_file}: {str(e)}")

        self.logger.info(f"Applied {fixes_applied} path fixes")
        return fixes_applied

    def run_knowledge_graph_generation(self, config_file):
        """Step 4: Generate Knowledge Graph using SDM-RDFizer"""
        self.logger.info("=" * 60)
        self.logger.info("STEP 4: GENERATING KNOWLEDGE GRAPH")
        self.logger.info("=" * 60)

        start_time = time.time()
        try:
            self.logger.info(f"Running SDM-RDFizer with config: {config_file}")

            cmd = [sys.executable, '-m', 'rdfizer', '-c', config_file]
            self.logger.info(f"Executing command: {' '.join(cmd)}")

            result = subprocess.run(
                cmd,
                cwd=self.output_base_dir,
                capture_output=True,
                text=True,
                timeout=300
            )

            duration = time.time() - start_time
            self.log_timing_metric('kg_generation', duration)

            if result.returncode == 0:
                self.logger.info("SDM-RDFizer completed successfully")
                self.logger.info("STDOUT:")
                for line in result.stdout.split('\n'):
                    if line.strip():
                        self.logger.info(f"  {line}")

                kg_files = glob.glob(os.path.join(self.kg_output_dir, "*"))
                self.logger.info(f"Generated {len(kg_files)} knowledge graph files:")
                for file in kg_files:
                    self.logger.info(f"  - {os.path.basename(file)} ({os.path.getsize(file)} bytes)")

                return True, kg_files
            else:
                self.logger.error(f"SDM-RDFizer failed with return code: {result.returncode}")
                self.logger.error("STDERR:")
                for line in result.stderr.split('\n'):
                    if line.strip():
                        self.logger.error(f"  {line}")

                return False, []

        except subprocess.TimeoutExpired:
            self.logger.error("SDM-RDFizer timed out after 5 minutes")
            return False, []
        except Exception as e:
            self.logger.error(f"Error running SDM-RDFizer: {str(e)}")
            return False, []

    def import_to_graphdb(self, repository_id, graphdb_url, kg_files, username=None, password=None):
        """Step 5 (Optional): Import generated KG files into a GraphDB repository."""
        self.logger.info("=" * 60)
        self.logger.info("STEP 5: IMPORTING KNOWLEDGE GRAPH TO GRAPHDB")
        self.logger.info("=" * 60)

        start_time = time.time()

        if not self.check_requests_installation():
            return False

        if not kg_files:
            self.logger.warning("No knowledge graph files were generated, skipping GraphDB import.")
            return False

        import_url = f"{graphdb_url.rstrip('/')}/repositories/{repository_id}/statements"
        self.logger.info(f"Targeting GraphDB repository: {repository_id} at {graphdb_url}")

        content_type_map = {
            '.ttl': 'application/x-turtle',
            '.nt': 'application/n-triples',
            '.rdf': 'application/rdf+xml',
            '.xml': 'application/rdf+xml'
        }

        auth = (username, password) if username and password else None

        success_count = 0
        for kg_file in kg_files:
            file_name = os.path.basename(kg_file)
            _, ext = os.path.splitext(kg_file)
            content_type = content_type_map.get(ext, 'application/x-turtle')

            self.logger.info(f"Uploading {file_name} to GraphDB...")

            headers = {'Content-Type': content_type}

            try:
                with open(kg_file, 'rb') as f:
                    response = requests.post(import_url, data=f, headers=headers, auth=auth, timeout=300)

                if response.status_code == 204:
                    self.logger.info(f"[SUCCESS] Successfully imported {file_name} into repository '{repository_id}'.")
                    success_count += 1
                else:
                    self.logger.error(f"[FAILED] Failed to import {file_name}. Status: {response.status_code}")
                    self.logger.error(f"Response from GraphDB: {response.text}")

            except requests.exceptions.RequestException as e:
                self.logger.error(f"[ERROR] A network error occurred while trying to import {file_name}: {e}")
            except Exception as e:
                self.logger.error(f"[ERROR] An unexpected error occurred during import of {file_name}: {e}")

        duration = time.time() - start_time
        self.log_timing_metric('graphdb_import', duration)

        if success_count == len(kg_files):
            self.logger.info("All knowledge graph files were successfully imported.")
            return True
        else:
            self.logger.warning(f"Import finished with errors. {success_count}/{len(kg_files)} files imported.")
            return False

    def run_complete_pipeline(self, enable_evaluation=False, **kwargs):
        """Run the complete pipeline with optional evaluation"""
        self.logger.info("=" * 80)
        self.logger.info("STARTING COMPLETE CSV TO KNOWLEDGE GRAPH PIPELINE")
        self.logger.info("=" * 80)
        self.logger.info(f"Input CSV: {self.input_csv}")
        self.logger.info(f"Output Directory: {self.output_base_dir}")
        self.logger.info(f"Pipeline Timestamp: {self.timestamp}")

        pipeline_start_time = time.time()
        resource_monitor = None

        if enable_evaluation:
            resource_monitor = ResourceMonitor()
            resource_monitor.start_monitoring()

        try:
            if not self.check_rdfizer_installation():
                raise RuntimeError("SDM-RDFizer is not installed and could not be installed automatically")

            devices = self.run_csv_splitter(
                time_col=kwargs.get('time_col', 'Time'),
                device_col=kwargs.get('device_col'),
                file_id=kwargs.get('file_id', '')
            )

            successful, failed = self.run_rml_generator(
                template_path=kwargs.get('template_path'),
                myprefix=kwargs.get('myprefix'),
                wid=kwargs.get('wid'),
                timestamp_column=kwargs.get('timestamp_column')
            )

            validation_results = self.validate_rml_paths()
            issues_found = any(result.get('status') == 'ISSUE' for result in validation_results)
            if issues_found:
                self.logger.info("Found path issues, attempting to fix...")
                self.fix_relative_paths_in_rml()
                validation_results = self.validate_rml_paths()

            config_file, rml_files = self.generate_rdfizer_config(
                remove_duplicate=kwargs.get('remove_duplicate', True),
                all_in_one_file=kwargs.get('all_in_one_file', False),
                enrichment=kwargs.get('enrichment', True),
                ordered=kwargs.get('ordered', True),
                output_format=kwargs.get('output_format', 'turtle')
            )

            kg_success, kg_files = self.run_knowledge_graph_generation(config_file)

            # GraphDB import if requested
            graphdb_success = False
            if kg_success and kwargs.get('import_to_graphdb', False):
                graphdb_success = self.import_to_graphdb(
                    repository_id=kwargs.get('graphdb_repo'),
                    graphdb_url=kwargs.get('graphdb_url', 'http://localhost:7200'),
                    kg_files=kg_files,
                    username=kwargs.get('graphdb_user'),
                    password=kwargs.get('graphdb_password')
                )

            pipeline_time = time.time() - pipeline_start_time
            self.log_timing_metric('total_pipeline', pipeline_time)

            # Stop resource monitoring
            resource_stats = None
            if resource_monitor:
                resource_monitor.stop_monitoring()
                resource_stats = resource_monitor.get_summary_stats()

            # Run evaluation if enabled
            evaluation_report = None
            if enable_evaluation and kg_success:
                evaluation_report = self.evaluator.run_full_evaluation(resource_stats)

            # Pipeline completion summary
            self.logger.info("=" * 80)
            self.logger.info("PIPELINE COMPLETION SUMMARY")
            self.logger.info("=" * 80)
            self.logger.info(f"Pipeline Timestamp: {self.timestamp}")
            self.logger.info(f"Total pipeline execution time: {pipeline_time:.2f} seconds")
            self.logger.info(f"Devices found: {len(devices)}")
            self.logger.info(f"RML files successfully generated: {len(successful)}")
            self.logger.info(f"RML generation failures: {len(failed)}")
            self.logger.info(f"Knowledge graph generation: {'SUCCESS' if kg_success else 'FAILED'}")
            self.logger.info(f"Knowledge graph files generated: {len(kg_files)}")
            if kwargs.get('import_to_graphdb', False):
                self.logger.info(f"GraphDB import: {'SUCCESS' if graphdb_success else 'FAILED'}")
            if enable_evaluation:
                self.logger.info(f"Evaluation: {'COMPLETED' if evaluation_report else 'FAILED'}")

            self.logger.info(f"\nAll outputs saved to: {self.output_base_dir}")
            self.logger.info("=" * 80)

            return {
                'devices': devices,
                'successful_rml': successful,
                'failed_rml': failed,
                'validation_results': validation_results,
                'kg_success': kg_success,
                'kg_files': kg_files,
                'config_file': config_file,
                'total_time': pipeline_time,
                'timestamp': self.timestamp,
                'output_directory': self.output_base_dir,
                'graphdb_success': graphdb_success,
                'evaluation_report': evaluation_report,
                'resource_stats': resource_stats
            }

        except Exception as e:
            self.logger.error(f"Pipeline failed: {str(e)}")
            raise
        finally:
            if resource_monitor:
                resource_monitor.stop_monitoring()


def main():
    parser = argparse.ArgumentParser(
        description="Complete CSV to Knowledge Graph Pipeline with optional GraphDB import, evaluation, and timestamped output folders.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic run with timestamped output folder
  %(prog)s input.csv

  # Run with comprehensive evaluation
  %(prog)s input.csv --evaluate

  # Run the full pipeline and import to GraphDB
  %(prog)s input.csv --import-to-graphdb --graphdb-repo my-repo-id

  # Run with evaluation and GraphDB import
  %(prog)s input.csv --evaluate --import-to-graphdb --graphdb-repo my-repo-id

  # Custom output directory without timestamp
  %(prog)s input.csv --output-dir ./my_output --no-timestamp
        """
    )

    # Required argument
    parser.add_argument('input_csv', help='Path to the input CSV file to be processed')

    # Pipeline output arguments
    parser.add_argument('--output-dir', default='pipeline_output',
                        help='Base output directory for all pipeline outputs (default: pipeline_output)')
    parser.add_argument('--no-timestamp', action='store_false', dest='use_timestamp',
                        help='Disable timestamped output folders')

    # CSV Splitter arguments
    parser.add_argument('--time-col', default='Time', help='Name of the time column (default: Time)')
    parser.add_argument('--device-col', help='Name of the column with device identifiers')
    parser.add_argument('--file-id', default='', help='ID to append to split CSV filenames')

    # RML Generator arguments
    parser.add_argument('--rml-template', default='Jinja_RML-Template_PerDevice.j2',
                        help='Path to the Jinja2 template file (default: Jinja_RML-Template_PerDevice.j2)')
    parser.add_argument('--prefix', default='https://w3id.org/omega-x/ontology/KG/PARKMeteostationDataSets',
                        help='Ontology prefix URL')
    parser.add_argument('--wid', default='W1', help='Window ID (default: W1)')
    parser.add_argument('--timestamp-column', help='Name of the timestamp column for RML (default: auto-detect)')

    # Knowledge Graph arguments
    parser.add_argument('--kg-format', choices=['turtle', 'n-triples', 'rdf-xml'], default='turtle',
                        help='Output format for knowledge graph (default: turtle)')
    parser.add_argument('--remove-duplicates', action='store_true', default=True,
                        help='Remove duplicate triples (default: True)')
    parser.add_argument('--no-remove-duplicates', action='store_false', dest='remove_duplicates')
    parser.add_argument('--all-in-one', action='store_true', help='Generate all datasets in one file')
    parser.add_argument('--no-enrichment', action='store_false', dest='enrichment', default=True,
                        help='Disable enrichment in knowledge graph generation')
    parser.add_argument('--no-ordered', action='store_false', dest='ordered', default=True,
                        help='Disable ordered processing in knowledge graph generation')

    # GraphDB Importer Arguments
    graphdb_group = parser.add_argument_group('GraphDB Importer (Optional)')
    graphdb_group.add_argument('--import-to-graphdb', action='store_true',
                               help='Enable importing the generated KG into a GraphDB repository.')
    graphdb_group.add_argument('--graphdb-url', default='http://localhost:7200',
                               help='URL of the GraphDB instance (default: http://localhost:7200)')
    graphdb_group.add_argument('--graphdb-repo',
                               help='The ID of the GraphDB repository to import data into. Required if --import-to-graphdb is set.')
    graphdb_group.add_argument('--graphdb-user', help='Username for GraphDB authentication.')
    graphdb_group.add_argument('--graphdb-password', help='Password for GraphDB authentication.')

    # Evaluation Arguments
    parser.add_argument('--evaluate', action='store_true',
                        help='Run comprehensive performance and resource evaluation after the pipeline completes.')

    # General arguments
    parser.add_argument('--log-level', choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'], default='INFO',
                        help='Logging level (default: INFO)')
    parser.add_argument('--verbose', action='store_true', help='Enable verbose output')
    parser.add_argument('--version', action='version', version='%(prog)s 3.0 (with Integrated Evaluation)')

    args = parser.parse_args()

    # Convert log level string to logging constant
    log_level = getattr(logging, args.log_level.upper())

    # Validation for GraphDB arguments
    if args.import_to_graphdb and not args.graphdb_repo:
        parser.error("--graphdb-repo is required when using --import-to-graphdb")

    # Validate input file exists
    if not os.path.exists(args.input_csv):
        parser.error(f"Input CSV file not found: {args.input_csv}")

    # Validate RML template exists
    if not os.path.exists(args.rml_template):
        parser.error(f"RML template file not found: {args.rml_template}")

    if args.verbose:
        print(f"Input CSV: {args.input_csv}")
        print(f"Output directory: {args.output_dir}")
        print(f"Use timestamp: {args.use_timestamp}")
        print(f"Evaluation enabled: {args.evaluate}")
        print(f"GraphDB import: {args.import_to_graphdb}")
        if args.import_to_graphdb:
            print(f"GraphDB repository: {args.graphdb_repo}")
            print(f"GraphDB URL: {args.graphdb_url}")

    try:
        # Create and run the pipeline
        pipeline = CSVToKnowledgeGraphPipeline(
            input_csv=args.input_csv,
            output_base_dir=args.output_dir,
            log_level=log_level,
            use_timestamp=args.use_timestamp
        )

        pipeline_result = pipeline.run_complete_pipeline(
            enable_evaluation=args.evaluate,
            time_col=args.time_col,
            device_col=args.device_col,
            file_id=args.file_id,
            template_path=args.rml_template,
            myprefix=args.prefix,
            wid=args.wid,
            timestamp_column=args.timestamp_column,
            remove_duplicate=args.remove_duplicates,
            all_in_one_file=args.all_in_one,
            enrichment=args.enrichment,
            ordered=args.ordered,
            output_format=args.kg_format,
            import_to_graphdb=args.import_to_graphdb,
            graphdb_repo=args.graphdb_repo,
            graphdb_url=args.graphdb_url,
            graphdb_user=args.graphdb_user,
            graphdb_password=args.graphdb_password
        )

        return 0 if pipeline_result and pipeline_result['kg_success'] else 1

    except Exception as e:
        print(f"\nFATAL PIPELINE ERROR: {e}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())
