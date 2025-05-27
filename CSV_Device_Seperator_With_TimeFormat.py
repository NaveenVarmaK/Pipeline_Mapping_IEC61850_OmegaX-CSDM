import pandas as pd
import re
import os
import logging
import time
import psutil
import threading
from datetime import datetime
import dateutil.parser
from tqdm import tqdm
from tqdm.auto import trange


def extract_device_name(header):
    """
    Extract device name from headers with different formats:
    Format 1: "s4DINV.EnclTmp.mag.f - 1 - TATA_ECP001_S3_SHL001Inverter01"
    Format 2: "METEOSTA004_s4MMET.POAInsol1.mag.f"
    """
    # Try Format 1: "s4DINV.EnclTmp.mag.f - 1 - TATA_ECP001_S3_SHL001Inverter01"
    parts = re.split(r' - \d+ - ', header)
    if len(parts) > 1:
        return parts[-1]  # The device name is the last part

    # Try Format 2: "METEOSTA004_s4MMET.POAInsol1.mag.f"
    match = re.match(r'^(METEOSTA\d+)_', header)
    if match:
        return match.group(1)  # The device name is at the beginning

    # Try to extract any station or device name pattern at the beginning
    match = re.match(r'^([A-Za-z0-9_]+)_', header)
    if match:
        return match.group(1)  # Return the prefix before the underscore

    return "unknown"  # Fallback if no pattern matches


def create_clean_column_name(header):
    """
    Create a clean column name from the signal part of the header
    for different header formats
    """
    # Try Format 1: "s4DINV.EnclTmp.mag.f - 1 - TATA_ECP001_S3_SHL001Inverter01"
    parts = re.split(r' - \d+ - ', header)
    if len(parts) > 1:
        return parts[0]  # The signal name is the first part

    # Try Format 2: "METEOSTA004_s4MMET.POAInsol1.mag.f"
    match = re.match(r'^[A-Za-z0-9_]+_(.*)', header)
    if match:
        return match.group(1)  # The signal name is after the device prefix

    # If no pattern matches, return the original header
    return header


def standardize_datetime(time_series, format='%Y-%m-%dT%H:%M:%S'):
    """
    Convert various datetime formats to the standard ISO 8601 format: 2024-11-02T06:13:20
    Handles:
    - Standard datetime strings
    - Unix timestamps (seconds or milliseconds)
    - Scientific notation (e.g., 1.73E+12 for milliseconds)
    """
    standardized = []

    for time_str in time_series:
        try:
            # Handle scientific notation timestamps (unix time in milliseconds)
            if isinstance(time_str, str) and ('e' in time_str.lower() or 'E' in time_str):
                try:
                    # Convert from scientific notation to a float (milliseconds)
                    timestamp_ms = float(time_str)
                    # Convert to seconds if it's in milliseconds (timestamp > 1e11)
                    if timestamp_ms > 1e11:  # Likely milliseconds
                        timestamp_sec = timestamp_ms / 1000.0
                    else:  # Already in seconds
                        timestamp_sec = timestamp_ms

                    dt = datetime.fromtimestamp(timestamp_sec)
                    standardized.append(dt.strftime(format))
                    continue
                except (ValueError, OverflowError):
                    pass  # If scientific notation parsing fails, try other methods

            # Handle numeric timestamps (could be seconds or milliseconds)
            if isinstance(time_str, (int, float)) or (
                    isinstance(time_str, str) and time_str.replace('.', '', 1).isdigit()):
                timestamp = float(time_str)
                # If timestamp is very large (> year 2286), assume it's in milliseconds
                if timestamp > 10000000000:  # More than 10 billion = likely milliseconds
                    timestamp = timestamp / 1000.0

                dt = datetime.fromtimestamp(timestamp)
                standardized.append(dt.strftime(format))
                continue

            # Try to parse the datetime using dateutil (handles most string formats)
            dt = dateutil.parser.parse(str(time_str))
            standardized.append(dt.strftime(format))

        except (ValueError, TypeError, OverflowError) as e:
            # If parsing fails, keep the original value
            standardized.append(str(time_str))
            print(f"Warning: Could not parse datetime '{time_str}', keeping original value. Error: {str(e)}")

    return standardized


def parse_time_from_ts(ts_value):
    """
    Parse time from ts in the format like "10:00.0" which becomes "12:10:00"

    Args:
        ts_value: A string containing a timestamp in the format "MM:SS.f"

    Returns:
        tuple: (hours, minutes) where hours is typically 12 and minutes comes from the input
    """
    if not isinstance(ts_value, str):
        ts_value = str(ts_value)

    match = re.search(r'(\d+):(\d+)\.(\d+)', ts_value)
    if match:
        minutes = int(match.group(1))  # First number is minutes
        seconds = int(match.group(2))  # Second number is seconds
        return 12, minutes  # Fixed at 12 hours
    return 12, 0  # Default if parsing fails


def combine_timestamps(df):
    """
    Combine date from timestamp_gmt with time from ts
    Creates a new 'Time' column with the ISO 8601 format: 2024-06-26T15:30:00

    Args:
        df: DataFrame containing 'ts' and 'timestamp_gmt' columns

    Returns:
        DataFrame with added 'Time' column
    """
    # Make a copy of the input DataFrame to avoid modifying the original
    result_df = df.copy()

    # Check if both required columns exist
    if 'ts' in df.columns and 'timestamp_gmt' in df.columns:
        def combine_date_and_time(row):
            try:
                # Get base datetime from timestamp_gmt
                ms_timestamp = float(row['timestamp_gmt'])
                base_dt = datetime.fromtimestamp(ms_timestamp / 1000)

                # Parse hours and minutes from ts using custom interpretation
                hours, minutes = parse_time_from_ts(row['ts'])

                # Create new datetime with date from base_dt and time from ts
                combined_dt = base_dt.replace(hour=hours, minute=minutes, second=0)

                # Format as ISO 8601
                return combined_dt.strftime('%Y-%m-%dT%H:%M:%S')
            except (ValueError, KeyError, TypeError) as e:
                logging.warning(f"Error converting timestamp: {e}")
                return None

        # Apply the conversion
        result_df['Time'] = result_df.apply(combine_date_and_time, axis=1)
        logging.info("Created 'Time' column by combining 'ts' and 'timestamp_gmt'")

    return result_df


def detect_format_type(df):
    """
    Detect which format the CSV is using based on column names and values
    Returns:
        - "format3" if there's a 'device' column
        - "format1_2" otherwise (requires header processing)
        - "format4" if there are both 'ts' and 'timestamp_gmt' columns
    """
    # Check for Format 4 (ts + timestamp_gmt combination)
    if 'ts' in df.columns and 'timestamp_gmt' in df.columns:
        return "format4", "device" if "device" in df.columns else None

    # Check for Format 3 (device column)
    device_cols = [col for col in df.columns if col.lower() == 'device']
    if device_cols:
        return "format3", device_cols[0]  # Return "format3" and the actual device column name

    # Default to Format 1/2
    return "format1_2", None


class PerformanceMonitor:
    """
    Monitor system performance metrics (CPU, RAM, disk I/O)
    """

    def __init__(self, interval=1.0):
        self.interval = interval
        self.running = False
        self.stats = {
            'cpu': [],
            'ram': [],
            'disk_read': [],
            'disk_write': []
        }
        self.monitor_thread = None
        self.start_time = None
        self.end_time = None
        self.last_io = None  # Initialize last_io attribute

    def start(self):
        """Start monitoring performance metrics"""
        self.running = True
        self.start_time = time.time()
        self.stats = {'cpu': [], 'ram': [], 'disk_read': [], 'disk_write': []}

        # Initialize disk I/O counters
        self.disk_io_start = psutil.disk_io_counters()
        self.last_io = self.disk_io_start  # Initialize last_io here

        # Start monitoring in a separate thread
        self.monitor_thread = threading.Thread(target=self._monitor)
        self.monitor_thread.daemon = True
        self.monitor_thread.start()

    def stop(self):
        """Stop monitoring performance metrics"""
        self.running = False
        self.end_time = time.time()
        if self.monitor_thread:
            self.monitor_thread.join(timeout=2.0)

    def _monitor(self):
        """Monitor thread function"""
        while self.running:
            # CPU usage (percent)
            cpu_percent = psutil.cpu_percent(interval=None)

            # RAM usage (MB)
            ram_usage = psutil.Process(os.getpid()).memory_info().rss / (1024 * 1024)

            # Disk I/O since last measurement
            current_io = psutil.disk_io_counters()

            # Always calculate disk I/O since last_io is now initialized in start()
            disk_read = (current_io.read_bytes - self.last_io.read_bytes) / (1024 * 1024)  # MB
            disk_write = (current_io.write_bytes - self.last_io.write_bytes) / (1024 * 1024)  # MB

            self.last_io = current_io

            # Store metrics
            self.stats['cpu'].append(cpu_percent)
            self.stats['ram'].append(ram_usage)
            self.stats['disk_read'].append(disk_read)
            self.stats['disk_write'].append(disk_write)

            # Sleep for interval
            time.sleep(self.interval)

    def get_summary(self):
        """Get a summary of the performance metrics"""
        if not self.stats['cpu']:
            return "No performance data collected"

        duration = self.end_time - self.start_time if self.end_time else time.time() - self.start_time

        return {
            'duration': f"{duration:.2f} seconds",
            'cpu_avg': f"{sum(self.stats['cpu']) / len(self.stats['cpu']):.1f}%",
            'cpu_max': f"{max(self.stats['cpu']):.1f}%",
            'ram_avg': f"{sum(self.stats['ram']) / len(self.stats['ram']):.1f} MB",
            'ram_max': f"{max(self.stats['ram']):.1f} MB",
            'disk_read_total': f"{sum(self.stats['disk_read']):.1f} MB",
            'disk_write_total': f"{sum(self.stats['disk_write']):.1f} MB"
        }

    def print_summary(self):
        """Print a summary of the performance metrics"""
        summary = self.get_summary()
        if isinstance(summary, str):
            print(summary)
            return

        print("\n===== Performance Summary =====")
        print(f"Total execution time: {summary['duration']}")
        print(f"CPU usage (avg/max): {summary['cpu_avg']} / {summary['cpu_max']}")
        print(f"RAM usage (avg/max): {summary['ram_avg']} / {summary['ram_max']}")
        print(f"Disk read: {summary['disk_read_total']}")
        print(f"Disk write: {summary['disk_write_total']}")
        print("===============================")


def fix_misaligned_csv(filepath):
    """
    Fix misaligned columns in CSV files

    Args:
        filepath: Path to the CSV file

    Returns:
        DataFrame with properly aligned columns
    """
    try:
        # First attempt: standard read
        df = pd.read_csv(filepath)
        return df
    except pd.errors.ParserError:
        # If standard read fails, try with error_bad_lines=False (skip bad lines)
        try:
            df = pd.read_csv(filepath, on_bad_lines='skip')
            logging.warning(f"Some rows were skipped due to parsing errors in {filepath}")
            return df
        except:
            # If that also fails, try with a different separator or engine
            try:
                # Try with semicolon separator (common in European data)
                df = pd.read_csv(filepath, sep=';')
                return df
            except:
                # Last resort: try with Python engine which is more flexible but slower
                df = pd.read_csv(filepath, engine='python')
                return df


def setup_logging(log_level=logging.INFO):
    """
    Set up logging configuration
    """
    # Create logs directory if it doesn't exist
    log_dir = 'logs'
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # Define log file with timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    log_file = os.path.join(log_dir, f'csv_splitter_{timestamp}.log')

    # Configure logging
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()  # Also output to console
        ]
    )

    return logging.getLogger(__name__)


def split_csv_by_device(input_file, output_dir='Input_CSV_Datasets/Input_CSV_Datasets_by_Devices/CSV_PerDevices',
                        time_col='Time', device_col=None, file_id='', log_level=logging.INFO):
    """
    Split a CSV file by device names extracted from headers or from a device column
    and standardize the time column format to ISO 8601

    Args:
        input_file: Path to the input CSV file
        output_dir: Directory where output files will be saved
        time_col: Column name containing time information
        device_col: Column name containing device identifiers (if applicable)
        file_id: ID string to append to output filenames
        log_level: Logging level
    """
    # Setup logging
    setup_logging(log_level)
    logger = logging.getLogger(__name__)

    # Start performance monitoring
    perf_monitor = PerformanceMonitor(interval=0.5)
    perf_monitor.start()

    logger.info(f"Reading CSV file: {input_file}")
    start_time = time.time()

    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        logger.debug(f"Created output directory: {output_dir}")

    # Read the CSV file with handling for misaligned columns
    try:
        df = fix_misaligned_csv(input_file)
        logger.info(f"Successfully read CSV with {len(df)} rows and {len(df.columns)} columns")
    except Exception as e:
        logger.error(f"Error reading CSV file: {str(e)}")
        perf_monitor.stop()
        perf_monitor.print_summary()
        raise

    # Auto-detect format if device_col is not provided
    format_type, detected_device_col = detect_format_type(df)
    logger.info(f"Detected format type: {format_type}")

    # Use provided device_col if specified, otherwise use detected one
    device_col = device_col or detected_device_col

    # Handle Format 4: Combine ts and timestamp_gmt if needed
    if format_type == "format4":
        logger.info("Processing Format 4: Combining ts and timestamp_gmt")
        with tqdm(total=1, desc="Combining timestamps") as pbar:
            df = combine_timestamps(df)
            pbar.update(1)

    # Check if time column exists and standardize it
    time_columns = [col for col in df.columns if col.lower() in
                    ['time', 'timestamp', 'timestamp_gmt', 'datetime', 'date']]

    if time_col in df.columns:
        time_columns = [time_col]  # Use the specified time column
    elif time_columns:
        time_col = time_columns[0]  # Use the first detected time column
        logger.info(f"Using detected time column: {time_col}")
    else:
        logger.warning(f"No time column found matching common patterns or specified name: {time_col}")

    # Standardize all identified time columns
    for col in time_columns:
        logger.info(f"Standardizing time column format: {col}")
        with tqdm(total=1, desc=f"Standardizing {col}") as pbar:
            df[col] = standardize_datetime(df[col])
            pbar.update(1)

    # Process according to the format type
    if format_type in ["format3", "format4"] and device_col in df.columns:
        # Format 3/4: Device names are in a separate column
        devices = split_by_device_column(df, device_col, output_dir, file_id)
    else:
        # Format 1 & 2: Device names are embedded in headers
        devices = split_by_header_format(df, output_dir, file_id)

    elapsed_time = time.time() - start_time
    logger.info(f"Total processing time: {elapsed_time:.2f} seconds")

    # Stop performance monitoring and print summary
    perf_monitor.stop()
    perf_monitor.print_summary()

    return devices


def split_by_device_column(df, device_col, output_dir, file_id=''):
    """
    Split the dataframe by the values in the device column

    Args:
        df: DataFrame to split
        device_col: Column name containing device identifiers
        output_dir: Directory where output files will be saved
        file_id: ID string to append to output filenames
    """
    logger = logging.getLogger(__name__)
    logger.info(f"Splitting by device column: {device_col}")

    # Get unique device values
    devices = df[device_col].unique()
    logger.info(f"Found {len(devices)} unique devices in '{device_col}' column")

    # Create a dataframe for each device
    for device in devices:
        if pd.isna(device):
            device_name = "unknown"
        else:
            device_name = str(device)

        # Filter rows for this device
        device_df = df[df[device_col] == device].copy()

        # Save the device dataframe
        safe_device_name = re.sub(r'[^\w\-]', '_', device_name)  # Create a safe filename

        # Add file_id to the filename if provided
        if file_id:
            output_file = os.path.join(output_dir, f"{safe_device_name}_{file_id}.csv")
        else:
            output_file = os.path.join(output_dir, f"{safe_device_name}.csv")

        device_df.to_csv(output_file, index=False)
        logger.info(f"Created file for device {device_name}: {output_file} with {len(device_df)} rows")

    logger.info(f"Finished processing. Split into {len(devices)} device files.")
    return list(devices)


def split_by_header_format(df, output_dir, file_id=''):
    """
    Split the dataframe by device names extracted from headers (Format 1 & 2)

    Args:
        df: DataFrame to split
        output_dir: Directory where output files will be saved
        file_id: ID string to append to output filenames
    """
    logger = logging.getLogger(__name__)

    # Extract device names and create a mapping of original column names to (device, clean_name)
    device_columns = {}
    common_cols = []

    # Process all columns
    for col in df.columns:
        device_name = extract_device_name(col)

        if device_name != "unknown":
            # This is a device-specific column
            clean_name = create_clean_column_name(col)
            device_columns[col] = (device_name, clean_name)
        else:
            # This is a common column (time, id, etc.)
            common_cols.append(col)

    logger.info(f"Found {len(common_cols)} common columns: {', '.join(common_cols)}")
    logger.info(f"Found {len(device_columns)} device-specific columns")

    # Group columns by device
    device_dataframes = {}

    # Create initial dataframes with common columns
    for device_name in set(device_info[0] for device_info in device_columns.values()):
        # Start with common columns (time, id, device, etc.)
        device_df = df[common_cols].copy()
        device_dataframes[device_name] = device_df

    # Add device-specific columns to appropriate dataframes
    for original_col, (device, clean_col) in device_columns.items():
        device_dataframes[device][clean_col] = df[original_col]

    # Save each device's data to a separate CSV file
    for device, device_df in device_dataframes.items():
        safe_device_name = re.sub(r'[^\w\-]', '_', device)  # Create a safe filename

        # Add file_id to the filename if provided
        if file_id:
            output_file = os.path.join(output_dir, f"{safe_device_name}_{file_id}.csv")
        else:
            output_file = os.path.join(output_dir, f"{safe_device_name}.csv")

        device_df.to_csv(output_file, index=False)
        logger.info(f"Created file for device {device}: {output_file} with {len(device_df.columns)} columns")

    logger.info(f"Finished processing. Split into {len(device_dataframes)} device files.")
    return list(device_dataframes.keys())


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Split IEC61850 CSV by device names in headers or device column')
    parser.add_argument('input_file', help='Input CSV file path')
    parser.add_argument('--output-dir', default='Input_CSV_Datasets/Input_CSV_Datasets_by_Devices/CSV_PerDevices',
                        help='Output directory for device CSV files')
    parser.add_argument('--time-col', default='Time', help='Name of the time column to standardize')
    parser.add_argument('--device-col', default=None,
                        help='Name of the column containing device identifiers (if applicable)')
    parser.add_argument('--timestamp-col', default=None,
                        help='Alternative name for time column (will be used if --time-col not found)')
    parser.add_argument('--file-id', default='W1',
                        help='ID string to append to each output filename')

    args = parser.parse_args()

    # Try the primary time column name, if not found try the timestamp column
    time_column = args.time_col
    if args.timestamp_col:
        try:
            # Just read the header to check
            sample = pd.read_csv(args.input_file, nrows=1)
            if time_column not in sample.columns and args.timestamp_col in sample.columns:
                time_column = args.timestamp_col
                print(f"Using timestamp column: {time_column}")
        except Exception as e:
            print(f"Warning: Error checking header columns: {str(e)}")

    devices = split_csv_by_device(args.input_file, args.output_dir, time_column, args.device_col, args.file_id)
    print("\nFound devices:")
    for device in sorted(devices):
        print(f"- {device}")