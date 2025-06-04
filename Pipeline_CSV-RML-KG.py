#!/usr/bin/env python3
"""
Seamless Pipeline: CSV Splitter -> RML Generator
This pipeline takes a large CSV file, splits it by device, then generates RML files for each device.
Fixed version that ensures absolute paths are used in RML generation.
"""

import os
import sys
import argparse
import logging
import glob
from pathlib import Path

# Import the functions from your existing scripts
try:
    from CSV_Device_Seperator_With_TimeFormat import split_csv_by_device, setup_logging as setup_splitter_logging
    from RML_Generation import profile_execution
except ImportError as e:
    print(f"Error importing modules: {e}")
    print("Make sure csv_splitter.py and rml_generator.py are in the same directory or Python path")
    sys.exit(1)


class CSVToRMLPipeline:
    """
    Pipeline class that orchestrates the CSV splitting and RML generation process
    """

    def __init__(self, input_csv, output_base_dir='pipeline_output', log_level=logging.INFO):
        self.input_csv = os.path.abspath(input_csv)  # Convert to absolute path
        self.output_base_dir = os.path.abspath(output_base_dir)  # Convert to absolute path
        self.log_level = log_level

        # Create pipeline directory structure with absolute paths
        self.split_csv_dir = os.path.join(self.output_base_dir, 'split_csvs')
        self.rml_output_dir = os.path.join(self.output_base_dir, 'rml_files')

        # Ensure directories exist
        os.makedirs(self.split_csv_dir, exist_ok=True)
        os.makedirs(self.rml_output_dir, exist_ok=True)

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
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )

        self.logger = logging.getLogger('CSVToRMLPipeline')

    def run_csv_splitter(self, time_col='Time', device_col=None, file_id=''):
        """
        Step 1: Split the input CSV by device
        """
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
        """
        Step 2: Generate RML files for each split CSV
        """
        self.logger.info("=" * 60)
        self.logger.info("STEP 2: GENERATING RML FILES")
        self.logger.info("=" * 60)

        # Find all CSV files in the split directory
        csv_pattern = os.path.join(self.split_csv_dir, "*.csv")
        csv_files = glob.glob(csv_pattern)

        if not csv_files:
            raise FileNotFoundError(f"No CSV files found in {self.split_csv_dir}")

        self.logger.info(f"Found {len(csv_files)} CSV files to process")

        successful_generations = []
        failed_generations = []

        for csv_file in csv_files:
            try:
                # Ensure we're using absolute paths with forward slashes for RML
                csv_file_abs = os.path.abspath(csv_file)
                csv_file_rml = self.normalize_path_for_rml(csv_file_abs)
                self.logger.info(f"Generating RML for: {os.path.basename(csv_file_abs)}")
                self.logger.debug(f"Absolute CSV path: {csv_file_abs}")
                self.logger.debug(f"RML normalized path: {csv_file_rml}")

                result = profile_execution(
                    csv_path=csv_file_rml,  # Pass RML-normalized path (absolute + forward slashes)
                    template_path=template_path,
                    output_dir=self.rml_output_dir,
                    myprefix=myprefix,
                    wid=wid,
                    timestamp_column=timestamp_column
                )

                successful_generations.append({
                    'csv_file': csv_file_rml,  # Store the RML-normalized path
                    'rml_file': result['output_file'],
                    'timestamp_column': result['timestamp_column']
                })

                self.logger.info(f"✓ Successfully generated RML: {result['output_file']}")

            except Exception as e:
                self.logger.error(f"✗ Failed to generate RML for {csv_file}: {str(e)}")
                failed_generations.append({
                    'csv_file': csv_file,
                    'error': str(e)
                })

        return successful_generations, failed_generations

    def validate_rml_paths(self):
        """
        Step 3: Validate that RML files contain absolute paths to CSV sources
        """
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

                # Look for rml:source lines
                lines = content.split('\n')
                source_lines = [line.strip() for line in lines if 'rml:source' in line]

                for line in source_lines:
                    if 'rml:source' in line:
                        # Extract the path from the line
                        start_idx = line.find('"') + 1
                        end_idx = line.rfind('"')
                        if start_idx > 0 and end_idx > start_idx:
                            source_path = line[start_idx:end_idx]

                            # Normalize path for comparison (convert backslashes to forward slashes)
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
                                self.logger.info(
                                    f"✓ {os.path.basename(rml_file)}: Valid absolute path with forward slashes")
                            else:
                                issues = []
                                if not is_absolute:
                                    issues.append("not absolute")
                                if not file_exists:
                                    issues.append("file not found")
                                if not has_forward_slashes:
                                    issues.append("contains backslashes")

                                self.logger.warning(
                                    f"⚠ {os.path.basename(rml_file)}: Path issues - {', '.join(issues)}")
                                self.logger.warning(f"  Path: {source_path}")

            except Exception as e:
                self.logger.error(f"Error validating {rml_file}: {str(e)}")
                validation_results.append({
                    'rml_file': os.path.basename(rml_file),
                    'error': str(e),
                    'status': 'ERROR'
                })

        return validation_results

    def normalize_path_for_rml(self, path):
        """
        Normalize a path for RML by converting to absolute path with forward slashes
        """
        # Convert to absolute path
        abs_path = os.path.abspath(path)
        # Convert backslashes to forward slashes for RML compatibility
        rml_path = abs_path.replace('\\', '/')
        return rml_path

    def fix_relative_paths_in_rml(self):
        """
        Fix any relative paths found in RML files by converting them to absolute paths with forward slashes
        """
        self.logger.info("=" * 60)
        self.logger.info("FIXING RELATIVE PATHS IN RML FILES")
        self.logger.info("=" * 60)

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
                        # Extract the current path
                        start_idx = line.find('"') + 1
                        end_idx = line.rfind('"')
                        if start_idx > 0 and end_idx > start_idx:
                            current_path = line[start_idx:end_idx]

                            # Check if path needs fixing (relative path or backslashes)
                            needs_fixing = not os.path.isabs(current_path) or '\\' in current_path

                            if needs_fixing:
                                # Try different approaches to find the correct absolute path
                                possible_paths = [
                                    current_path,
                                    os.path.join(self.split_csv_dir, os.path.basename(current_path)),
                                    os.path.join(os.getcwd(), current_path)
                                ]

                                for test_path in possible_paths:
                                    abs_test_path = os.path.abspath(test_path)
                                    if os.path.exists(abs_test_path):
                                        # Normalize the path for RML (absolute + forward slashes)
                                        rml_normalized_path = self.normalize_path_for_rml(abs_test_path)

                                        # Replace the path in the line
                                        new_line = line.replace(f'"{current_path}"', f'"{rml_normalized_path}"')
                                        lines[i] = new_line
                                        self.logger.info(f"Fixed path in {os.path.basename(rml_file)}")
                                        self.logger.info(f"  From: {current_path}")
                                        self.logger.info(f"  To:   {rml_normalized_path}")
                                        fixes_applied += 1
                                        break
                                else:
                                    self.logger.warning(f"Could not find absolute path for: {current_path}")

                            # Also fix existing absolute paths that have backslashes
                            elif '\\' in current_path and os.path.exists(current_path):
                                rml_normalized_path = self.normalize_path_for_rml(current_path)
                                new_line = line.replace(f'"{current_path}"', f'"{rml_normalized_path}"')
                                lines[i] = new_line
                                self.logger.info(f"Normalized path slashes in {os.path.basename(rml_file)}")
                                self.logger.info(f"  From: {current_path}")
                                self.logger.info(f"  To:   {rml_normalized_path}")
                                fixes_applied += 1

                # Write back if changes were made
                new_content = '\n'.join(lines)
                if new_content != original_content:
                    with open(rml_file, 'w', encoding='utf-8') as f:
                        f.write(new_content)

            except Exception as e:
                self.logger.error(f"Error fixing paths in {rml_file}: {str(e)}")

        self.logger.info(f"Applied {fixes_applied} path fixes")
        return fixes_applied

    def run_complete_pipeline(self, **kwargs):
        """
        Run the complete pipeline: CSV splitting -> RML generation -> Path validation and fixing
        """
        self.logger.info("=" * 80)
        self.logger.info("STARTING COMPLETE CSV TO RML PIPELINE")
        self.logger.info("=" * 80)
        self.logger.info(f"Input CSV: {self.input_csv}")
        self.logger.info(f"Output Directory: {self.output_base_dir}")

        pipeline_start_time = time.time()

        try:
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

            # Fix any relative paths found
            issues_found = any(result.get('status') == 'ISSUE' for result in validation_results)
            if issues_found:
                self.logger.info("Found path issues, attempting to fix...")
                fixes_applied = self.fix_relative_paths_in_rml()

                # Re-validate after fixes
                if fixes_applied > 0:
                    self.logger.info("Re-validating after fixes...")
                    validation_results = self.validate_rml_paths()

            # Pipeline completion summary
            pipeline_time = time.time() - pipeline_start_time

            self.logger.info("=" * 80)
            self.logger.info("PIPELINE COMPLETION SUMMARY")
            self.logger.info("=" * 80)
            self.logger.info(f"Total pipeline execution time: {pipeline_time:.2f} seconds")
            self.logger.info(f"Devices found: {len(devices)}")
            self.logger.info(f"RML files successfully generated: {len(successful)}")
            self.logger.info(f"RML generation failures: {len(failed)}")

            if successful:
                self.logger.info("\nSuccessfully generated RML files:")
                for item in successful:
                    self.logger.info(
                        f"  - {os.path.basename(item['rml_file'])} (from {os.path.basename(item['csv_file'])})")

            if failed:
                self.logger.warning("\nFailed RML generations:")
                for item in failed:
                    self.logger.warning(f"  - {os.path.basename(item['csv_file'])}: {item['error']}")

            # Path validation summary
            valid_paths = sum(1 for result in validation_results if result.get('status') == 'OK')
            total_paths = len(validation_results)
            self.logger.info(f"\nPath validation: {valid_paths}/{total_paths} paths are valid")

            self.logger.info(f"\nAll outputs saved to: {self.output_base_dir}")
            self.logger.info("=" * 80)

            return {
                'devices': devices,
                'successful_rml': successful,
                'failed_rml': failed,
                'validation_results': validation_results,
                'total_time': pipeline_time
            }

        except Exception as e:
            self.logger.error(f"Pipeline failed: {str(e)}")
            raise


def main():
    parser = argparse.ArgumentParser(
        description="Complete CSV to RML Pipeline: Split CSV by device then generate RML files with absolute paths",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s input.csv
  %(prog)s input.csv --output-dir ./my_pipeline_output
  %(prog)s input.csv --time-col "timestamp" --device-col "device" --file-id W2
  %(prog)s input.csv --rml-template custom_template.j2 --prefix "https://example.org/ontology" --wid W3
  %(prog)s input.csv --timestamp-column "datetime" --output-dir /tmp/pipeline
        """
    )

    # Required argument
    parser.add_argument(
        'input_csv',
        help='Path to the input CSV file to be processed'
    )

    # Pipeline output arguments
    parser.add_argument(
        '--output-dir',
        default='pipeline_output',
        help='Base output directory for all pipeline outputs (default: pipeline_output)'
    )

    # CSV Splitter arguments
    parser.add_argument(
        '--time-col',
        default='Time',
        help='Name of the time column to standardize (default: Time)'
    )

    parser.add_argument(
        '--device-col',
        help='Name of the column containing device identifiers (if applicable)'
    )

    parser.add_argument(
        '--file-id',
        default='',
        help='ID string to append to each split CSV filename'
    )

    # RML Generator arguments
    parser.add_argument(
        '--rml-template',
        default='Jinja_RML-Template_PerDevice.j2',
        help='Path to the Jinja2 template file (default: Jinja_RML-Template_PerDevice.j2)'
    )

    parser.add_argument(
        '--prefix',
        default='https://w3id.org/omega-x/ontology/KG/PARKMeteostationDataSets',
        help='Ontology prefix URL (default: https://w3id.org/omega-x/ontology/KG/PARKMeteostationDataSets)'
    )

    parser.add_argument(
        '--wid',
        default='W1',
        help='Window ID (default: W1)'
    )

    parser.add_argument(
        '--timestamp-column',
        help='Name of the timestamp column for RML generation (default: auto-detect)'
    )

    # General arguments
    parser.add_argument(
        '--log-level',
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
        default='INFO',
        help='Logging level (default: INFO)'
    )

    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose output'
    )

    parser.add_argument(
        '--version',
        action='version',
        version='CSV to RML Pipeline 1.1 (with path fixing)'
    )

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
        print("=" * 60)
        print("CSV TO RML PIPELINE CONFIGURATION")
        print("=" * 60)
        print(f"Input CSV: {os.path.abspath(args.input_csv)}")
        print(f"Output Directory: {os.path.abspath(args.output_dir)}")
        print(f"Time Column: {args.time_col}")
        print(f"Device Column: {args.device_col or 'Auto-detect'}")
        print(f"File ID: {args.file_id or 'None'}")
        print(f"RML Template: {args.rml_template}")
        print(f"Ontology Prefix: {args.prefix}")
        print(f"Window ID: {args.wid}")
        print(f"Timestamp Column: {args.timestamp_column or 'Auto-detect'}")
        print(f"Log Level: {args.log_level}")
        print("=" * 60)

    try:
        # Create and run the pipeline
        pipeline = CSVToRMLPipeline(
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
            timestamp_column=args.timestamp_column
        )

        if args.verbose:
            print(f"\nPipeline completed successfully!")
            print(f"Total execution time: {result['total_time']:.2f} seconds")
            print(f"Devices processed: {len(result['devices'])}")
            print(f"RML files generated: {len(result['successful_rml'])}")

            valid_paths = sum(1 for r in result['validation_results'] if r.get('status') == 'OK')
            total_paths = len(result['validation_results'])
            print(f"Path validation: {valid_paths}/{total_paths} paths are valid")

        return 0

    except Exception as e:
        print(f"Pipeline failed: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == "__main__":
    import time

    exit(main())