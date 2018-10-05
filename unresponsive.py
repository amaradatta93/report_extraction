import csv
import datetime

from database import db_device_data
from parse_util import date_time_conversion, two_days_back, parsed_dict


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

    for devices in device_info:
        try:
            date_time_obj = date_time_conversion(devices['Date_Stamp'], devices['Time_Stamp'])
            dt_check = two_days_back(date_time_obj)
            if dt_check and ((devices['Device_Status'] == 'Active') and (devices['Billing_Status'] == 'Active')):
                # print(devices['Date_Stamp'], devices['Time_Stamp'], devices['Device_Status'], devices['Billing_Status'])
                parsed_device_list.append(devices)
        except KeyError:
            devices.update({'Date_Stamp': 'not found'})
            devices.update({'Time_Stamp': 'not found'})
    return parsed_device_list


def write_to_csv():
    '''
    Write the obtained dictionary into a CSV file
    :return: None
    '''
    parsed_device_list = parse_unresponsive_data()
    parameter_optimized = parsed_dict(parsed_device_list)

    # csv_columns = ['Account_Name', 'IMEI', 'SIM_No', 'Date_Stamp', 'Time_Stamp', 'Added_On', 'Asset_No', 'Comments']
    csv_columns = ['Account_Name', 'IMEI', 'Date_Stamp', 'Time_Stamp']
    csv_name = 'Unresponsive_device_' + str(datetime.datetime.now().date()) + '.csv'
    print('The unresponsive device report is available in "{0}"'.format(csv_name))

    try:
        with open(csv_name, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
            writer.writeheader()
            for data in parameter_optimized:
                writer.writerow(data)
    except IOError:
        print("I/O error")


write_to_csv()
