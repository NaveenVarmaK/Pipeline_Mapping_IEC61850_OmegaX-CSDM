import pandas as pd
import re
import os


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


def split_csv_by_device(input_file, output_dir='device_data'):
    """
    Split a CSV file by device names extracted from headers
    """
    print(f"Reading CSV file: {input_file}")

    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Read the CSV file
    df = pd.read_csv(input_file)

    # Extract device names and create a mapping of original column names to (device, clean_name)
    device_columns = {}
    for col in df.columns:
        device_name = extract_device_name(col)
        clean_name = create_clean_column_name(col)
        device_columns[col] = (device_name, clean_name)

    # Group columns by device
    device_dataframes = {}

    for original_col, (device, clean_col) in device_columns.items():
        if device not in device_dataframes:
            # Create a new dataframe with the index column (assuming first column is timestamp/index)
            device_dataframes[device] = pd.DataFrame(df.iloc[:, 0])

        # Add the column to the device's dataframe with the clean name
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
    parser.add_argument('--output-dir', default='device_data', help='Output directory for device CSV files')

    args = parser.parse_args()

    devices = split_csv_by_device(args.input_file, args.output_dir)
    print("\nFound devices:")
    for device in sorted(devices):
        print(f"- {device}")