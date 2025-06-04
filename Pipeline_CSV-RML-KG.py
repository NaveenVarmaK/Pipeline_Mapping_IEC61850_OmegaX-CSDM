#!/usr/bin/env python3
"""
Enhanced Seamless Pipeline: CSV Splitter -> RML Generator -> Knowledge Graph Generator
This pipeline takes a large CSV file, splits it by device, generates RML files for each device,
and finally creates a complete knowledge graph using SDM-RDFizer.
"""

import os
import sys
import argparse
import logging
import glob
import subprocess
import configparser
import time
from pathlib import Path

# Import the functions from your existing scripts
try:
    from CSV_Device_Seperator_With_TimeFormat import split_csv_by_device, setup_logging as setup_splitter_logging
    from RML_Generation import profile_execution
except ImportError as e:
    print(f"Error importing modules: {e}")
    print("Make sure csv_splitter.py and rml_generator.py are in the same directory or Python path")
    sys.exit(1)


class CSVToKnowledgeGraphPipeline:
    """
    Enhanced Pipeline class that orchestrates the complete process:
    CSV splitting -> RML generation -> Knowledge Graph creation
    """

    def __init__(self, input_csv, output_base_dir='pipeline_output', log_level=logging.INFO):
        self.input_csv = os.path.abspath(input_csv)
        self.output_base_dir = os.path.abspath(output_base_dir)
        self.log_level = log_level

        # Create pipeline directory structure with absolute paths
        self.split_csv_dir = os.path.join(self.output_base_dir, 'split_csvs')
        self.rml_output_dir = os.path.join(self.output_base_dir, 'rml_files')
        self.kg_output_dir = os.path.join(self.output_base_dir, 'knowledge_graph')
        self.config_dir = os.path.join(self.output_base_dir, 'config')

        # Ensure directories exist
        for directory in [self.split_csv_dir, self.rml_output_dir, self.kg_output_dir, self.config_dir]:
            os.makedirs(directory, exist_ok=True)

        # Setup logging
        self.setup_pipeline_logging()

    def setup_pipeline_logging(self):
        """Setup logging for the pipeline"""
        log_dir = os.path.join(self.output_base_dir, 'logs')
        os.makedirs(log_dir, exist_ok=True)

        from datetime import datetime
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        log_file = os.path.join(log_dir, f'pipeline_{timestamp}.log')

        logging.basicConfig(
            level=self.log_level,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file, encoding='utf-8'),
                logging.StreamHandler()
            ]
        )

        self.logger = logging.getLogger('CSVToKnowledgeGraphPipeline')

    def check_rdfizer_installation(self):
        """Check if SDM-RDFizer is installed and install if necessary"""
        self.logger.info("Checking SDM-RDFizer installation...")

        try:
            # Try to import rdfizer to check if it's installed
            result = subprocess.run([sys.executable, '-c', 'import rdfizer'],
                                    capture_output=True, text=True)
            if result.returncode == 0:
                self.logger.info("SDM-RDFizer is already installed")
                return True
        except Exception:
            pass

        # If not installed, try to install it
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
        """
        Generate the config.ini file for SDM-RDFizer based on available RML files
        """
        self.logger.info("=" * 60)
        self.logger.info("STEP 4: GENERATING SDM-RDFIZER CONFIGURATION")
        self.logger.info("=" * 60)

        # Find all RML files
        rml_pattern = os.path.join(self.rml_output_dir, "*.ttl")
        rml_files = glob.glob(rml_pattern)

        if not rml_files:
            raise FileNotFoundError(f"No RML files found in {self.rml_output_dir}")

        self.logger.info(f"Found {len(rml_files)} RML files for knowledge graph generation")

        # Create config file path
        config_file = os.path.join(self.config_dir, 'rdfizer_config.ini')

        # Create configuration
        config = configparser.ConfigParser()
        config.optionxform = str  # Preserve case sensitivity

        # Default section
        config['default'] = {
            'main_directory': self.output_base_dir
        }

        # Datasets section
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

        # Add dataset sections for each RML file
        for i, rml_file in enumerate(rml_files, 1):
            # Generate dataset name from RML filename
            rml_basename = os.path.basename(rml_file)
            dataset_name = rml_basename.replace('.ttl', '').replace('generated_', '').replace('.rml', '')

            config[f'dataset{i}'] = {
                'name': dataset_name,
                'mapping': rml_file
            }

            self.logger.info(f"Added dataset {i}: {dataset_name}")

        # Write configuration file
        with open(config_file, 'w', encoding='utf-8') as f:
            config.write(f)

        self.logger.info(f"Generated RDFizer configuration: {config_file}")

        # Log the configuration content for debugging
        self.logger.debug("Configuration file content:")
        with open(config_file, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                self.logger.debug(f"  {line_num:2d}: {line.rstrip()}")

        return config_file, rml_files

    def run_csv_splitter(self, time_col='Time', device_col=None, file_id=''):
        """Step 1: Split the input CSV by device"""
        self.logger.info("=" * 60)
        self.logger.info("STEP 1: SPLITTING CSV BY DEVICE")
        self.logger.info("=" * 60)

        try:
            devices = split_csv_by_device(
                input_file=self.input_csv,
                output_dir=self.split_csv_dir,
                time_col=time_col,
                device_col=device_col,
                file_id=file_id,
                log_level=self.log_level
            )

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

        return successful_generations, failed_generations

    def validate_rml_paths(self):
        """Step 3: Validate that RML files contain absolute paths to CSV sources"""
        self.logger.info("=" * 60)
        self.logger.info("STEP 3: VALIDATING RML FILE PATHS")
        self.logger.info("=" * 60)

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

        try:
            # Run SDM-RDFizer
            self.logger.info(f"Running SDM-RDFizer with config: {config_file}")

            cmd = [sys.executable, '-m', 'rdfizer', '-c', config_file]
            self.logger.info(f"Executing command: {' '.join(cmd)}")

            # Run the command and capture output
            result = subprocess.run(
                cmd,
                cwd=self.output_base_dir,  # Set working directory
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout
            )

            if result.returncode == 0:
                self.logger.info("SDM-RDFizer completed successfully")
                self.logger.info("STDOUT:")
                for line in result.stdout.split('\n'):
                    if line.strip():
                        self.logger.info(f"  {line}")

                # Check for generated files
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

                self.logger.error("STDOUT:")
                for line in result.stdout.split('\n'):
                    if line.strip():
                        self.logger.error(f"  {line}")

                return False, []

        except subprocess.TimeoutExpired:
            self.logger.error("SDM-RDFizer timed out after 5 minutes")
            return False, []
        except Exception as e:
            self.logger.error(f"Error running SDM-RDFizer: {str(e)}")
            return False, []

    def run_complete_pipeline(self, **kwargs):
        """Run the complete pipeline: CSV splitting -> RML generation -> Knowledge Graph creation"""
        self.logger.info("=" * 80)
        self.logger.info("STARTING COMPLETE CSV TO KNOWLEDGE GRAPH PIPELINE")
        self.logger.info("=" * 80)
        self.logger.info(f"Input CSV: {self.input_csv}")
        self.logger.info(f"Output Directory: {self.output_base_dir}")

        pipeline_start_time = time.time()

        try:
            # Check SDM-RDFizer installation
            if not self.check_rdfizer_installation():
                raise RuntimeError("SDM-RDFizer is not installed and could not be installed automatically")

            # Step 1: Split CSV by device
            devices = self.run_csv_splitter(
                time_col=kwargs.get('time_col', 'Time'),
                device_col=kwargs.get('device_col'),
                file_id=kwargs.get('file_id', '')
            )

            # Step 2: Generate RML files
            successful, failed = self.run_rml_generator(
                template_path=kwargs.get('template_path'),
                myprefix=kwargs.get('myprefix'),
                wid=kwargs.get('wid'),
                timestamp_column=kwargs.get('timestamp_column')
            )

            # Step 3: Validate and fix paths in RML files
            validation_results = self.validate_rml_paths()
            issues_found = any(result.get('status') == 'ISSUE' for result in validation_results)
            if issues_found:
                self.logger.info("Found path issues, attempting to fix...")
                self.fix_relative_paths_in_rml()
                validation_results = self.validate_rml_paths()

            # Step 4: Generate RDFizer configuration and run knowledge graph generation
            config_file, rml_files = self.generate_rdfizer_config(
                remove_duplicate=kwargs.get('remove_duplicate', True),
                all_in_one_file=kwargs.get('all_in_one_file', False),
                enrichment=kwargs.get('enrichment', True),
                ordered=kwargs.get('ordered', True),
                output_format=kwargs.get('output_format', 'turtle')
            )

            # Step 5: Generate Knowledge Graph
            kg_success, kg_files = self.run_knowledge_graph_generation(config_file)

            # Pipeline completion summary
            pipeline_time = time.time() - pipeline_start_time

            self.logger.info("=" * 80)
            self.logger.info("PIPELINE COMPLETION SUMMARY")
            self.logger.info("=" * 80)
            self.logger.info(f"Total pipeline execution time: {pipeline_time:.2f} seconds")
            self.logger.info(f"Devices found: {len(devices)}")
            self.logger.info(f"RML files successfully generated: {len(successful)}")
            self.logger.info(f"RML generation failures: {len(failed)}")
            self.logger.info(f"Knowledge graph generation: {'SUCCESS' if kg_success else 'FAILED'}")
            self.logger.info(f"Knowledge graph files generated: {len(kg_files)}")

            if successful:
                self.logger.info("\nSuccessfully generated RML files:")
                for item in successful:
                    self.logger.info(f"  - {os.path.basename(item['rml_file'])}")

            if kg_files:
                self.logger.info("\nGenerated Knowledge Graph files:")
                for file in kg_files:
                    self.logger.info(f"  - {os.path.basename(file)}")

            if failed:
                self.logger.warning("\nFailed RML generations:")
                for item in failed:
                    self.logger.warning(f"  - {os.path.basename(item['csv_file'])}: {item['error']}")

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
                'total_time': pipeline_time
            }

        except Exception as e:
            self.logger.error(f"Pipeline failed: {str(e)}")
            raise


def main():
    parser = argparse.ArgumentParser(
        description="Complete CSV to Knowledge Graph Pipeline: Split CSV -> Generate RML -> Create Knowledge Graph",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s input.csv
  %(prog)s input.csv --output-dir ./my_pipeline_output
  %(prog)s input.csv --time-col "timestamp" --device-col "device" --file-id W2
  %(prog)s input.csv --rml-template custom_template.j2 --prefix "https://example.org/ontology"
  %(prog)s input.csv --kg-format turtle --remove-duplicates --all-in-one
        """
    )

    # Required argument
    parser.add_argument('input_csv', help='Path to the input CSV file to be processed')

    # Pipeline output arguments
    parser.add_argument('--output-dir', default='pipeline_output',
                        help='Base output directory for all pipeline outputs (default: pipeline_output)')

    # CSV Splitter arguments
    parser.add_argument('--time-col', default='Time',
                        help='Name of the time column to standardize (default: Time)')
    parser.add_argument('--device-col',
                        help='Name of the column containing device identifiers (if applicable)')
    parser.add_argument('--file-id', default='',
                        help='ID string to append to each split CSV filename')

    # RML Generator arguments
    parser.add_argument('--rml-template', default='Jinja_RML-Template_PerDevice.j2',
                        help='Path to the Jinja2 template file (default: Jinja_RML-Template_PerDevice.j2)')
    parser.add_argument('--prefix', default='https://w3id.org/omega-x/ontology/KG/PARKMeteostationDataSets',
                        help='Ontology prefix URL')
    parser.add_argument('--wid', default='W1', help='Window ID (default: W1)')
    parser.add_argument('--timestamp-column',
                        help='Name of the timestamp column for RML generation (default: auto-detect)')

    # Knowledge Graph arguments
    parser.add_argument('--kg-format', choices=['turtle', 'n-triples', 'rdf-xml'], default='turtle',
                        help='Output format for knowledge graph (default: turtle)')
    parser.add_argument('--remove-duplicates', action='store_true', default=True,
                        help='Remove duplicate triples in knowledge graph (default: True)')
    parser.add_argument('--no-remove-duplicates', action='store_false', dest='remove_duplicates',
                        help='Keep duplicate triples in knowledge graph')
    parser.add_argument('--all-in-one', action='store_true',
                        help='Generate all datasets in one file')
    parser.add_argument('--no-enrichment', action='store_false', dest='enrichment', default=True,
                        help='Disable enrichment in knowledge graph generation')
    parser.add_argument('--no-ordered', action='store_false', dest='ordered', default=True,
                        help='Disable ordered processing in knowledge graph generation')

    # General arguments
    parser.add_argument('--log-level', choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'], default='INFO',
                        help='Logging level (default: INFO)')
    parser.add_argument('--verbose', action='store_true', help='Enable verbose output')
    parser.add_argument('--version', action='version',
                        version='CSV to Knowledge Graph Pipeline 2.0 (with SDM-RDFizer)')

    args = parser.parse_args()

    # Convert log level string to logging constant
    log_level = getattr(logging, args.log_level.upper())

    # Validate input file exists
    if not os.path.exists(args.input_csv):
        parser.error(f"Input CSV file not found: {args.input_csv}")

    # Validate RML template exists
    if not os.path.exists(args.rml_template):
        parser.error(f"RML template file not found: {args.rml_template}")

    if args.verbose:
        print("=" * 70)
        print("CSV TO KNOWLEDGE GRAPH PIPELINE CONFIGURATION")
        print("=" * 70)
        print(f"Input CSV: {os.path.abspath(args.input_csv)}")
        print(f"Output Directory: {os.path.abspath(args.output_dir)}")
        print(f"Time Column: {args.time_col}")
        print(f"Device Column: {args.device_col or 'Auto-detect'}")
        print(f"File ID: {args.file_id or 'None'}")
        print(f"RML Template: {args.rml_template}")
        print(f"Ontology Prefix: {args.prefix}")
        print(f"Window ID: {args.wid}")
        print(f"Knowledge Graph Format: {args.kg_format}")
        print(f"Remove Duplicates: {args.remove_duplicates}")
        print(f"All in One File: {args.all_in_one}")
        print(f"Enrichment: {args.enrichment}")
        print(f"Ordered: {args.ordered}")
        print(f"Log Level: {args.log_level}")
        print("=" * 70)

    try:
        # Create and run the pipeline
        pipeline = CSVToKnowledgeGraphPipeline(
            input_csv=args.input_csv,
            output_base_dir=args.output_dir,
            log_level=log_level
        )

        result = pipeline.run_complete_pipeline(
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
            output_format=args.kg_format
        )

        if args.verbose:
            print(f"\nPipeline completed successfully!")
            print(f"Total execution time: {result['total_time']:.2f} seconds")
            print(f"Devices processed: {len(result['devices'])}")
            print(f"RML files generated: {len(result['successful_rml'])}")
            print(f"Knowledge graph generation: {'SUCCESS' if result['kg_success'] else 'FAILED'}")
            print(f"Knowledge graph files: {len(result['kg_files'])}")

        return 0 if result['kg_success'] else 1

    except Exception as e:
        print(f"Pipeline failed: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())