import xml.etree.ElementTree as ET
import csv

# Input files
data_shlok = 'data/export_shlok.xml'
data_akhil = 'data/export_akhil.xml'

# Output files
shlok_csv = 'data/shlok.csv'
akhil_csv = 'data/akhil.csv'

desired_fields = ['data_type', 'creationDate', 'startDate', 'endDate', 'value', 'unit', 'person']

# List of (xml_file, output_csv, person_label)
people_data = [
    (data_shlok, shlok_csv, 'shlok'),
    (data_akhil, akhil_csv, 'akhil')
]

# List of health metric types
metric_types = [
    ('HKQuantityTypeIdentifierActiveEnergyBurned', 'active_energy'),
    ('HKQuantityTypeIdentifierHeadphoneAudioExposure', 'audio_exposure'),
    ('HKQuantityTypeIdentifierBasalEnergyBurned', 'basal_energy'),
    ('HKQuantityTypeIdentifierDistanceWalkingRunning', 'distance'),
    ('HKQuantityTypeIdentifierHeartRate', 'heart_rate'),
    ('HKQuantityTypeIdentifierAppleStandTime', 'standing'),
    ('HKQuantityTypeIdentifierStepCount', 'step_count'),
    ('HKQuantityTypeIdentifierWalkingStepLength', 'step_length'),
]

# Process each person's data
for xml_file, output_csv, person in people_data:
    records = []
    tree = ET.parse(xml_file)
    root = tree.getroot()

    for record_type, data_type in metric_types:
        for record in root.findall('Record'):
            if record.attrib.get("type") == record_type:
                row = {field: record.attrib.get(field, '') for field in desired_fields if field not in ['data_type', 'person']}
                row['data_type'] = data_type
                row['person'] = person
                records.append(row)

    # Write to CSV
    with open(output_csv, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=desired_fields)
        writer.writeheader()
        for row in records:
            writer.writerow(row)

    print(f"Exported {len(records)} records to '{output_csv}' with person='{person}'.")
