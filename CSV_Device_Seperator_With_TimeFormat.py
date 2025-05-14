import pandas as pd
import re
import os
from datetime import datetime
import dateutil.parser


def extract_device_name(header):
    """
    Extract device name from a header like "s4DINV.EnclTmp.mag.f - 1 - TATA_ECP001_S3_SHL001Inverter01"
    """
    # Split by the separator pattern " - 1 - " or any similar pattern like " - X - "
    parts = re.split(r' - \d+ - ', header)
    if len(parts) > 1:
        return parts[-1]  # The device name is the last part
    return "unknown"  # Fallback if pattern doesn't match


def create_clean_column_name(header):
    """
    Create a clean column name from the signal part of the header
    """
    parts = re.split(r' - \d+ - ', header)
    return parts[0]  # The signal name is the first part


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


def split_csv_by_device(input_file, output_dir='Input_CSV_Datasets/Input_CSV_Datasets_by_Devices/CSV_PerDevices', time_col='Time'):
    """
    Split a CSV file by device names extracted from headers
    and standardize the time column format to ISO 8601
    """
    print(f"Reading CSV file: {input_file}")

    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Read the CSV file
    df = pd.read_csv(input_file)

    # Check if time column exists
    if time_col in df.columns:
        print(f"Standardizing time column format: {time_col}")
        df[time_col] = standardize_datetime(df[time_col])
    else:
        print(f"Warning: Time column '{time_col}' not found in the CSV")

    # Extract device names and create a mapping of original column names to (device, clean_name)
    device_columns = {}
    common_cols = []

    for col in df.columns:
        # Check if the column header contains the device pattern
        if re.search(r' - \d+ - ', col):
            device_name = extract_device_name(col)
            clean_name = create_clean_column_name(col)
            device_columns[col] = (device_name, clean_name)
        else:
            # Keep track of columns that don't follow the device pattern (like time, id, device)
            common_cols.append(col)

    print(f"Found {len(common_cols)} common columns: {', '.join(common_cols)}")
    print(f"Found {len(device_columns)} device-specific columns")

    # Group columns by device
    device_dataframes = {}

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

    parser = argparse.ArgumentParser(description='Split IEC61850 CSV by device names in headers')
    parser.add_argument('input_file', help='Input CSV file path')
    parser.add_argument('--output-dir', default='Input_CSV_Datasets/Input_CSV_Datasets_by_Devices/CSV_PerDevices', help='Output directory for device CSV files')
    parser.add_argument('--time-col', default='time', help='Name of the time column to standardize')

    args = parser.parse_args()

    devices = split_csv_by_device(args.input_file, args.output_dir, args.time_col)
    print("\nFound devices:")
    for device in sorted(devices):
        print(f"- {device}")