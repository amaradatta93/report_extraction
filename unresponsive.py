import csv
import datetime, pprint

from database import db_device_data
from parse_util import date_time_conversion, two_days_back, parsed_dict

THRESHOLD_DAYS = input('See all the device which stopped working before how many days? ')


def parse_unresponsive_data():
    '''
    Parse the list of device information and check for:
    - Device_Status
    - Billing_Status
    - If device has reported for past two days or not
    :return: List of those device which has not reported for past two days and has
             active device and billing status
    '''
    device_info = db_device_data()
    parsed_device_list = []

    # pprint.pprint(device_info)

    for devices in device_info:
        try:
            date_time_obj = date_time_conversion(devices['Last_reported_date'], devices['Last_reported_time'])
            dt_check = two_days_back(date_time_obj, THRESHOLD_DAYS)
            if dt_check and ((devices['Device_Status'] == 'Active') and (devices['Billing_Status'] == 'Active')):
                # print(devices['Last_reported_date'], devices['Last_reported_time'], devices['Device_Status'], devices['Billing_Status'])
                parsed_device_list.append(devices)
        except KeyError:
            devices.update({'Last_reported_date': 'not found'})
            devices.update({'Last_reported_time': 'not found'})
    return parsed_device_list


def write_to_csv():
    '''
    Write the obtained dictionary into a CSV file
    :return: None
    '''
    parsed_device_list = parse_unresponsive_data()
    parameter_optimized = parsed_dict(parsed_device_list)

    # csv_columns = ['Account_Name', 'IMEI', 'SIM_No', 'Last_reported_date', 'Last_reported_time', 'Added_On', 'Asset_No', 'Comments']
    csv_columns = ['Account_Name', 'IMEI', 'Last_reported_date', 'Last_reported_time']
    csv_name = 'Unresponsive_device_' + str(datetime.datetime.now().date()) + '.csv'
    print('The unresponsive device report is available in "{0}"'.format(csv_name))

    try:
        with open(csv_name, 'w') as csvfile:
            description_text = 'Device which have not reported since or before last ' + THRESHOLD_DAYS + ' days'
            description = csv.writer(csvfile)
            description.writerow([description_text])
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
            writer.writeheader()
            for data in parameter_optimized:
                writer.writerow(data)
    except IOError:
        print("I/O error")


write_to_csv()
