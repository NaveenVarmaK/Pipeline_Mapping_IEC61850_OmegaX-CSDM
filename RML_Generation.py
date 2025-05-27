import csv
import re
import os
import time
import tracemalloc
import psutil
import argparse
from jinja2 import Environment, FileSystemLoader

from Resources.CSV_Header_Dictionary import MEASUREMENTS, get_qudt_unit


def profile_execution(csv_path, template_path=None, output_dir=None, myprefix=None, wid=None):
    """Measure execution time and memory usage for RML generation process"""

    tracemalloc.start()
    process = psutil.Process(os.getpid())
    start_memory = process.memory_info().rss / 1024 / 1024

    start_time = time.time()

    # Validate input file exists
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"CSV file not found: {csv_path}")

    # Load CSV headers
    csv_load_start = time.time()
    with open(csv_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        headers = next(reader)
    csv_load_time = time.time() - csv_load_start

    # Enhanced parse_header function with better property mapping
    def parse_header(header):
        skip_columns = {"timestamp", "id", "device", "ts", "timestamp_gmt", "site", "Time"}
        if header in skip_columns or not header.strip():
            return None

        parts = header.lower().split('.')
        result = {
            "property_id": header.replace('.', '').replace(' ', ''),
            "csv_column": header,
            "unit": "UNITLESS",
            "property": f"Property for {header}",  # Default property
            "measurement_type": None
        }

        # Try to find matching measurement type and extract property
        for part in parts:
            # Remove numbers from the end to get base measurement type
            base_part = re.sub(r'\d+$', '', part)

            if base_part in MEASUREMENTS:
                result["measurement_type"] = base_part
                result["property"] = MEASUREMENTS[base_part]["property"]

                # Get unit information
                unit = get_qudt_unit(base_part)
                if unit:
                    result["unit"] = unit
                elif MEASUREMENTS[base_part].get("unit"):
                    result["unit"] = MEASUREMENTS[base_part]["unit"]

                break

        # If no direct match found, try partial matching
        if not result["measurement_type"]:
            header_clean = header.lower().replace('.', '').replace('_', '')
            for measurement_key, measurement_data in MEASUREMENTS.items():
                if measurement_key in header_clean or header_clean.startswith(measurement_key):
                    result["measurement_type"] = measurement_key
                    result["property"] = measurement_data["property"]

                    unit = get_qudt_unit(measurement_key)
                    if unit:
                        result["unit"] = unit
                    elif measurement_data.get("unit"):
                        result["unit"] = measurement_data["unit"]
                    break

        return result

    # Parse all headers
    header_parse_start = time.time()
    properties = [parsed for column in headers if (parsed := parse_header(column))]
    header_parse_time = time.time() - header_parse_start

    # Extract device_id
    def extract_device_id_from_csv_path(path):
        filename = os.path.basename(path)
        return os.path.splitext(filename)[0]

    device_id = extract_device_id_from_csv_path(csv_path)

    # Get unique units for the template
    unique_units = list(set(prop["unit"] for prop in properties if prop["unit"] != "UNITLESS"))

    # Create rendering context
    context_create_start = time.time()
    context = {
        "device_id": device_id,
        "csv_path": csv_path,
        "myprefix": myprefix,
        "properties": properties,
        "unique_units": unique_units,
        "wid": wid
    }
    context_create_time = time.time() - context_create_start

    # Debug: Print properties for verification
    print(f"\nParsed Properties:")
    print(f"{'=' * 80}")
    for prop in properties[:5]:  # Show first 5 for debugging
        print(f"Property ID: {prop['property_id']}")
        print(f"CSV Column: {prop['csv_column']}")
        print(f"property: {prop['property']}")
        print(f"Unit: {prop['unit']}")
        print(f"Measurement Type: {prop['measurement_type']}")
        print("-" * 40)

    # Render template
    template_render_start = time.time()
    template_dir = os.path.dirname(template_path) if template_path else '.'
    template_name = os.path.basename(template_path) if template_path else 'Jinja_RML-Template_PerDevice.j2'

    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template(template_name)
    output = template.render(context)
    template_render_time = time.time() - template_render_start

    # Save to file
    file_write_start = time.time()
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
        output_filename = os.path.join(output_dir, f'generated_{device_id}.rml.ttl')
    else:
        output_filename = f'../OmegaX-Pipeline/Output/RML/generated_{device_id}.rml.ttl'
        os.makedirs(os.path.dirname(output_filename), exist_ok=True)

    with open(output_filename, 'w') as f:
        f.write(output)
    file_write_time = time.time() - file_write_start

    # Track and print metrics
    total_time = time.time() - start_time
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    end_memory = process.memory_info().rss / 1024 / 1024
    memory_used = end_memory - start_memory

    print(f"\n{'=' * 50}")
    print("PERFORMANCE METRICS")
    print(f"{'=' * 50}")
    print(f"RML file generated at '{output_filename}'")
    print(f"Total properties processed: {len(properties)}")
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

    return {
        'total_time': total_time,
        'peak_memory_mb': peak / 1024 / 1024,
        'memory_increase_mb': memory_used,
        'output_file': output_filename
    }


def main():
    parser = argparse.ArgumentParser(
        description="Generate RML files from CSV datasets with performance profiling",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s input.csv
  %(prog)s input.csv -t custom_template.j2 -o ./output -p "https://example.org/ontology" -w W2
  %(prog)s /path/to/data.csv --output-dir /tmp/rml --wid W3
        """
    )

    # Required argument
    parser.add_argument(
        'csv_path',
        help='Path to the input CSV file'
    )

    # Optional arguments
    parser.add_argument(
        '-t', '--template',
        default='Jinja_RML-Template_PerDevice.j2',
        help='Path to the Jinja2 template file (default: Jinja_RML-Template_PerDevice.j2)'
    )

    parser.add_argument(
        '-o', '--output-dir',
        help='Output directory for generated RML files (default: ../OmegaX-Pipeline/Output/RML/)'
    )

    parser.add_argument(
        '-p', '--prefix',
        default='https://w3id.org/omega-x/ontology/KG/PARKMeteostationDataSets',
        help='Ontology prefix URL (default: https://w3id.org/omega-x/ontology/KG/PARKMeteostationDataSets)'
    )

    parser.add_argument(
        '-w', '--wid',
        default='W1',
        help='Window ID (default: W1)'
    )

    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Enable verbose output'
    )

    parser.add_argument(
        '--version',
        action='version',
        version='RML Generator 1.0'
    )

    args = parser.parse_args()

    # Validate template file exists
    if not os.path.exists(args.template):
        parser.error(f"Template file not found: {args.template}")

    if args.verbose:
        print(f"Input CSV: {args.csv_path}")
        print(f"Template: {args.template}")
        print(f"Output directory: {args.output_dir or '../OmegaX-Pipeline/Output/RML/'}")
        print(f"Prefix: {args.prefix}")
        print(f"Window ID: {args.wid}")
        print("-" * 50)

    try:
        result = profile_execution(
            csv_path=args.csv_path,
            template_path=args.template,
            output_dir=args.output_dir,
            myprefix=args.prefix,
            wid=args.wid
        )

        if args.verbose:
            print(f"\nExecution completed successfully!")
            print(f"Output file: {result['output_file']}")

    except FileNotFoundError as e:
        print(f"Error: {e}")
        return 1
    except Exception as e:
        print(f"An error occurred: {e}")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())