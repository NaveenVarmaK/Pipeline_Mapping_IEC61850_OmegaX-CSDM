import csv
import re
import os
import time
import tracemalloc
import psutil
from jinja2 import Environment, FileSystemLoader

# Import the dictionaries from a separate file
# to be Accessed the CSV_Header_Dictionary.py file from Resources Package
from Resources.CSV_Header_Dictionary import MEASUREMENTS, UNIT_TO_QUDT, get_qudt_unit


def profile_execution():
    """Measure execution time and memory usage for RML generation process"""

    # Start memory tracking
    tracemalloc.start()
    process = psutil.Process(os.getpid())

    # Record the starting memory usage
    start_memory = process.memory_info().rss / 1024 / 1024  # Convert to MB

    # Record the starting time
    start_time = time.time()

    # Step 1: Load CSV and parse headers
    csv_path = 'Input_CSV_Datasets/NARB_ECP001_S3_SHL001Inverter01.csv'

    # Timing for CSV loading step
    csv_load_start = time.time()
    with open(csv_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        headers = next(reader)  # First row contains column names
    csv_load_time = time.time() - csv_load_start

    # Step 2: Parse headers to extract semantic information
    def parse_header(header):
        """
        Parse an IEC 61850 header to extract semantic information
        Returns a dictionary with parsed components and unit information
        """
        # Skip columns we don't want to process
        skip_columns = {"timestamp", "id", "device"}
        if header in skip_columns or header.strip() == "":
            return None

        # Split by dots to separate components
        parts = header.lower().split('.')

        # Initialize result with defaults
        result = {
            "property_id": header.replace('.', '').replace(' ', ''),
            "csv_column": header,
            "unit": None,
            "description": None
        }

        # Try to extract measurement type for unit determination
        for part in parts:
            # Remove any numeric suffix (like inv1 -> inv)
            base_part = re.sub(r'\d+$', '', part)

            # Check if this part corresponds to a known measurement
            if base_part in MEASUREMENTS:
                result["measurement_type"] = base_part
                result["description"] = MEASUREMENTS[base_part]["description"]

                # Get unit if available
                unit = get_qudt_unit(base_part)
                if unit:
                    result["unit"] = unit
                break

        # If no unit was found, set a default
        if not result["unit"]:
            result["unit"] = "UNITLESS"  # Default when no unit is specified

        return result

    # Process all headers
    header_parse_start = time.time()
    properties = []
    for column in headers:
        parsed = parse_header(column)
        if parsed:
            properties.append(parsed)
    header_parse_time = time.time() - header_parse_start

    # Extract the device ID from the CSV filename
    def extract_device_id_from_csv_path(path):
        """Extract device ID from CSV filename"""
        filename = os.path.basename(path)
        # Remove extension
        device_id = os.path.splitext(filename)[0]
        return device_id

    # Step 3: Define context
    context_create_start = time.time()
    device_id = extract_device_id_from_csv_path(csv_path)
    context = {
        "inverter_id": device_id,  # Dynamically set from CSV filename
        "date": "20241101",
        "csv_path": csv_path,
        "base_uri": "https://w3id.org/omega-x/ontology/KG/MeteostationDataSets",
        "properties": properties
    }
    context_create_time = time.time() - context_create_start

    # Step 4: Load and render template
    template_render_start = time.time()
    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template('Jinja_RML-Template_PerDevice.j2')
    output = template.render(context)
    template_render_time = time.time() - template_render_start

    # Step 5: Save to file
    file_write_start = time.time()
    output_filename = f'../OmegaX-Pipeline/Output/RML/generated_{device_id}.rml.ttl'
    with open(output_filename, 'w') as f:
        f.write(output)
    file_write_time = time.time() - file_write_start

    # Calculate total time and memory usage
    total_time = time.time() - start_time
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    end_memory = process.memory_info().rss / 1024 / 1024  # Convert to MB
    memory_used = end_memory - start_memory

    # Print performance metrics
    print(f"\n{'=' * 50}")
    print("PERFORMANCE METRICS")
    print(f"{'=' * 50}")
    print(f"RML file generated at '{output_filename}'")
    print(f"\nTime Metrics:")
    print(f"  - CSV loading time:       {csv_load_time:.4f} seconds")
    print(f"  - Header parsing time:    {header_parse_time:.4f} seconds")
    print(f"  - Context creation time:  {context_create_time:.4f} seconds")
    print(f"  - Template rendering:     {template_render_time:.4f} seconds")
    print(f"  - File writing time:      {file_write_time:.4f} seconds")
    print(f"  - Total execution time:   {total_time:.4f} seconds")
    print(f"\nMemory Metrics:")
    print(f"  - Current memory usage:   {current / 1024 / 1024:.2f} MB")
    print(f"  - Peak memory usage:      {peak / 1024 / 1024:.2f} MB")
    print(f"  - Process memory start:   {start_memory:.2f} MB")
    print(f"  - Process memory end:     {end_memory:.2f} MB")
    print(f"  - Total memory increase:  {memory_used:.2f} MB")
    print(f"{'=' * 50}")

    # Return metrics for potential further use
    return {
        'total_time': total_time,
        'peak_memory_mb': peak / 1024 / 1024,
        'memory_increase_mb': memory_used
    }


if __name__ == "__main__":
    metrics = profile_execution()