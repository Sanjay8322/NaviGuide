from tempfile import NamedTemporaryFile
import shutil
import csv


def process_csv(data):
    filename = 'output.csv'
    tempfile = NamedTemporaryFile(mode='w', delete=False)

    fields = ['Userid', 'Purposeid', 'Visit-frequency']

    with open(filename, 'r') as csvfile, tempfile:
        reader = csv.DictReader(csvfile, fieldnames=fields)
        writer = csv.DictWriter(tempfile, fieldnames=fields)
        row_exists_flag = False
        for row in reader:
            if str(row['Userid']) == str(data['Userid']) and row['Purposeid'] == data['Purposeid']:
                print('updating row...')
                row['Userid'], row['Purposeid'], row['Visit-frequency'] = data['Userid'], row['Purposeid'], str(int(row['Visit-frequency'])+int(data['Visit-frequency']))
                row_exists_flag = True

            row = {'Userid': row['Userid'], 'Purposeid': row['Purposeid'], 'Visit-frequency': row['Visit-frequency']}
            writer.writerow(row)

        if not row_exists_flag:
            row = data
            writer.writerow(row)

    shutil.move(tempfile.name, filename)
    print("Dataset Updated")


# data = {
#         "Userid": '2',
#         "Purposeid": "kore",
#         "Visit-frequency": '1'
# }

# process_csv(data)
