#!/usr/bin/env python3
"""
Enhanced Pipeline Evaluation Script
This script evaluates the output of the CSV to Knowledge Graph Pipeline.

ENHANCEMENTS:
- Uses the 'rdflib' library for accurate triple counting in all RDF formats.
- Parses the pipeline's log file to get precise per-stage execution times.
- Provides more detailed logging and a clearer summary report.

FIXED: Corrected attribute initialization order in PipelineEvaluator class.
"""
import argparse
import os
import sys
import time
import psutil
import threading
import logging
import json
import glob
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional, Tuple

# --- DEPENDENCY CHECK: rdflib is now essential for accurate KG analysis ---
try:
    import rdflib
except ImportError:
    print("Error: The 'rdflib' library is required for accurate evaluation.")
    print("Please install it by running: python3 -m pip install rdflib")
    sys.exit(1)


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
                # Get current CPU and Memory (RSS) usage
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
        """
        Accurately count triples in a knowledge graph file using rdflib.
        """
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

        # Find all potential KG files based on supported extensions
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

            # Track format stats
            if file_format not in results['formats']:
                results['formats'][file_format] = {'files': 0, 'triples': 0}
            results['formats'][file_format]['files'] += 1
            results['formats'][file_format]['triples'] += triple_count

        results['total_size_mb'] = total_size_bytes / (1024 * 1024)
        self.logger.info(
            f"KG analysis complete. Found {results['total_triples']:,} triples across {results['total_files']} files.")
        return results


class PipelineEvaluator:
    """Main class to evaluate the entire pipeline's output."""

    def __init__(self, pipeline_output_dir: str, log_level: int = logging.INFO):
        self.pipeline_output_dir = os.path.abspath(pipeline_output_dir)
        self.log_level = log_level

        # FIXED: Define all directory paths BEFORE calling setup_logging
        self.log_dir = os.path.join(self.pipeline_output_dir, 'logs')
        self.kg_output_dir = os.path.join(self.pipeline_output_dir, 'knowledge_graph')
        self.eval_output_dir = os.path.join(self.pipeline_output_dir, 'evaluation')

        # Create evaluation directory if it doesn't exist
        os.makedirs(self.eval_output_dir, exist_ok=True)

        # Now setup logging (after eval_output_dir is defined)
        self.setup_logging()

        # Initialize the knowledge graph analyzer
        self.kg_analyzer = KnowledgeGraphAnalyzer()

    def setup_logging(self):
        """Set up logging for the evaluation process."""
        log_file = os.path.join(self.eval_output_dir, f'evaluation_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log')
        logging.basicConfig(
            level=self.log_level,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[logging.FileHandler(log_file), logging.StreamHandler(sys.stdout)]
        )
        self.logger = logging.getLogger('PipelineEvaluator')

    def parse_pipeline_log_for_timings(self) -> Dict[str, float]:
        """Parses the main pipeline log file to extract performance timings."""
        self.logger.info("Parsing pipeline log for performance timings...")
        log_pattern = os.path.join(self.log_dir, 'pipeline_*.log')
        log_files = glob.glob(log_pattern)

        if not log_files:
            self.logger.warning("No pipeline log file found. Per-stage timings will be unavailable.")
            return {}

        # Use the most recent log file
        latest_log = max(log_files, key=os.path.getmtime)
        self.logger.info(f"Reading timings from: {os.path.basename(latest_log)}")

        timings = {}
        # Regex to find lines like: TIMING_METRIC: {"stage": "csv_splitter", "duration_sec": 0.5}
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

    def run_full_evaluation(self) -> Optional[Dict[str, Any]]:
        """Runs the complete evaluation and generates a report."""
        self.logger.info("=" * 60)
        self.logger.info(f"STARTING EVALUATION FOR: {self.pipeline_output_dir}")
        self.logger.info("=" * 60)

        try:
            # Step 1: Analyze the generated Knowledge Graph
            kg_results = self.kg_analyzer.analyze_knowledge_graph_directory(self.kg_output_dir)

            # Step 2: Parse the pipeline log for precise timings
            performance_timings = self.parse_pipeline_log_for_timings()

            # Step 3: Assemble the final report
            evaluation_report = {
                'evaluation_timestamp': datetime.now().isoformat(),
                'pipeline_output_dir': self.pipeline_output_dir,
                'performance_metrics': {
                    'total_pipeline_time_sec': performance_timings.get('total_pipeline', 0.0),
                    'stages_sec': {k: v for k, v in performance_timings.items() if k != 'total_pipeline'}
                },
                'knowledge_graph_metrics': kg_results
            }

            # Add calculated metrics
            total_time = evaluation_report['performance_metrics']['total_pipeline_time_sec']
            total_triples = kg_results.get('total_triples', 0)
            if total_time > 0 and total_triples > 0:
                evaluation_report['performance_metrics']['triples_per_second'] = total_triples / total_time

            # Step 4: Save and print the report
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
        """Prints a user-friendly summary of the evaluation results to the console."""
        print("\n" + "=" * 80)
        print("PIPELINE EVALUATION SUMMARY")
        print("=" * 80)

        # Performance Metrics
        perf = report.get('performance_metrics', {})
        print(" PERFORMANCE METRICS")
        total_time = perf.get('total_pipeline_time_sec', 0)
        print(f"  - Total Pipeline Execution Time: {total_time:.2f} seconds")
        for stage, duration in perf.get('stages_sec', {}).items():
            print(f"    - {stage.replace('_', ' ').title()} Time: {duration:.2f} seconds")
        if 'triples_per_second' in perf:
            print(f"  - Throughput: {perf['triples_per_second']:,.0f} triples/second")

        print("-" * 40)

        # Knowledge Graph Metrics
        kg = report.get('knowledge_graph_metrics', {})
        print(" KNOWLEDGE GRAPH METRICS")
        print(f"  - Total Triples Generated: {kg.get('total_triples', 0):,}")
        print(f"  - Total KG Size: {kg.get('total_size_mb', 0):.2f} MB")
        print(f"  - Number of KG Files: {kg.get('total_files', 0)}")
        if 'formats' in kg:
            for fmt, data in kg['formats'].items():
                print(f"    - Format '{fmt}': {data['files']} files with {data['triples']:,} triples")

        print("=" * 80)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Evaluate the output of the CSV to Knowledge Graph Pipeline.")
    parser.add_argument('pipeline_output_dir', help='Path to the pipeline\'s timestamped output directory.')
    parser.add_argument('--log-level', choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'], default='INFO',
                        help='Set the logging level.')
    args = parser.parse_args()

    if not os.path.isdir(args.pipeline_output_dir):
        print(f"Error: Directory not found at '{args.pipeline_output_dir}'")
        sys.exit(1)

    log_level = getattr(logging, args.log_level.upper())
    evaluator = PipelineEvaluator(args.pipeline_output_dir, log_level)
    evaluator.run_full_evaluation()