import csv
import re
import os
from jinja2 import Environment, FileSystemLoader

# Import the dictionaries from a separate file
# to be Accessed the CSV_Header_Dictionary.py file from Resources Package
from Resources.CSV_Header_Dictionary import MEASUREMENTS, UNIT_TO_QUDT, get_qudt_unit

# Step 1: Load CSV and parse headers
csv_path = 'Input_CSV_Datasets/NARB_ECP001_S3_SHL001Inverter01.csv'  # Path to your actual CSV file

with open(csv_path, newline='') as csvfile:
    reader = csv.reader(csvfile)
    headers = next(reader)  # First row contains column names


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
properties = []
for column in headers:
    parsed = parse_header(column)
    if parsed:
        properties.append(parsed)


# Extract the device ID from the CSV filename
def extract_device_id_from_csv_path(path):
    """Extract device ID from CSV filename"""
    filename = os.path.basename(path)
    # Remove extension
    device_id = os.path.splitext(filename)[0]
    return device_id


# Step 3: Define context
device_id = extract_device_id_from_csv_path(csv_path)
context = {
    "inverter_id": device_id,  # Dynamically set from CSV filename
    "date": "20241101",
    "csv_path": csv_path,
    "base_uri": "https://w3id.org/omega-x/ontology/KG/NarbonneDataSets",
    "properties": properties
}

# Step 4: Load and render template
env = Environment(loader=FileSystemLoader('.'))
template = env.get_template('Jinja_RML-Template_PerDevice.j2')
output = template.render(context)

# Step 5: Save to file
output_filename = f'../OmegaX-Pipeline/Output/generated_{device_id}.rml.ttl'
with open(output_filename, 'w') as f:
    f.write(output)

print(f"RML file generated at '{output_filename}'")