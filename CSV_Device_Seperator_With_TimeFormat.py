import pandas as pd
import re
import os
from datetime import datetime
import dateutil.parser


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
    """
    standardized = []

    for time_str in time_series:
        try:
            # Try to parse the datetime using dateutil (handles most formats)
            dt = dateutil.parser.parse(str(time_str))
            # Format to the desired output format
            standardized.append(dt.strftime(format))
        except (ValueError, TypeError):
            # If parsing fails, keep the original value
            standardized.append(str(time_str))
            print(f"Warning: Could not parse datetime '{time_str}', keeping original value")

    return standardized


def detect_format_type(df):
    """
    Detect which format the CSV is using based on column names and values
    Returns:
        - "format3" if there's a 'device' column
        - "format1_2" otherwise (requires header processing)
    """
    device_cols = [col for col in df.columns if col.lower() == 'device']
    if device_cols:
        return "format3", device_cols[0]  # Return "format3" and the actual device column name
    else:
        return "format1_2", None


def split_csv_by_device(input_file, output_dir='Input_CSV_Datasets/Input_CSV_Datasets_by_Devices/CSV_PerDevices',
                        time_col='Time', device_col=None):
    """
    Split a CSV file by device names extracted from headers or from a device column
    and standardize the time column format to ISO 8601
    """
    print(f"Reading CSV file: {input_file}")

    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Read the CSV file
    df = pd.read_csv(input_file)

    # Auto-detect format if device_col is not provided
    if device_col is None:
        format_type, device_col = detect_format_type(df)
        print(f"Detected format type: {format_type}")
    else:
        # If device_col is provided, use Format 3
        format_type = "format3" if device_col in df.columns else "format1_2"
        print(f"Using format type: {format_type}")

    # Check if time column exists and standardize it
    if time_col in df.columns:
        print(f"Standardizing time column format: {time_col}")
        df[time_col] = standardize_datetime(df[time_col])
    else:
        print(f"Warning: Time column '{time_col}' not found in the CSV")

    # Process according to the format type
    if format_type == "format3":
        # Format 3: Device names are in a separate column
        return split_by_device_column(df, device_col, output_dir)
    else:
        # Format 1 & 2: Device names are embedded in headers
        return split_by_header_format(df, output_dir)


def split_by_device_column(df, device_col, output_dir):
    """
    Split the dataframe by the values in the device column
    """
    print(f"Splitting by device column: {device_col}")

    # Get unique device values
    devices = df[device_col].unique()
    print(f"Found {len(devices)} unique devices in '{device_col}' column")

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
        output_file = os.path.join(output_dir, f"{safe_device_name}.csv")
        device_df.to_csv(output_file, index=False)
        print(f"Created file for device {device_name}: {output_file} with {len(device_df)} rows")

    print(f"Finished processing. Split into {len(devices)} device files.")
    return list(devices)


def split_by_header_format(df, output_dir):
    """
    Split the dataframe by device names extracted from headers (Format 1 & 2)
    """
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

    print(f"Found {len(common_cols)} common columns: {', '.join(common_cols)}")
    print(f"Found {len(device_columns)} device-specific columns")

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
        output_file = os.path.join(output_dir, f"{safe_device_name}.csv")
        device_df.to_csv(output_file, index=False)
        print(f"Created file for device {device}: {output_file} with {len(device_df.columns)} columns")

    print(f"Finished processing. Split into {len(device_dataframes)} device files.")
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

    args = parser.parse_args()

    # Try the primary time column name, if not found try the timestamp column
    time_column = args.time_col
    if args.timestamp_col and time_column not in pd.read_csv(args.input_file, nrows=1).columns:
        if args.timestamp_col in pd.read_csv(args.input_file, nrows=1).columns:
            time_column = args.timestamp_col
            print(f"Using timestamp column: {time_column}")

    devices = split_csv_by_device(args.input_file, args.output_dir, time_column, args.device_col)
    print("\nFound devices:")
    for device in sorted(devices):
        print(f"- {device}")