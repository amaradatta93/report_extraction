import os, pprint

import mysql.connector


USER = os.getenv('USER')
PASSWORD = os.getenv('PASSWORD')
HOST = os.getenv('HOST')
DATABASE = os.getenv('DATABASE')


def db_device_data():
    '''
    Query the database to obtain device information and account information
    Get all the accounts
    Under accounts get all the devices
    :return: List of dictionary containing all the information about accounts and its devices
    '''
    device_data = []

    cnx = mysql.connector.connect(user=USER, password=PASSWORD, host=HOST, database=DATABASE)
    cursor1 = cnx.cursor(dictionary=True, buffered=True)
    cursor2 = cnx.cursor(dictionary=True, buffered=True)
    cursor3 = cnx.cursor(dictionary=True, buffered=True)
    cursor4 = cnx.cursor(dictionary=True, buffered=True)

    device_info = ("SELECT * FROM DEVICE_REGISTER "
                   "WHERE ACCOUNT_ID IN (SELECT ACCOUNT_ID FROM ACCOUNT ) ")
    account_name = ("SELECT ACCOUNT_NAME FROM ACCOUNT "
                    "WHERE ACCOUNT_ID = %s ")
    imei_date = ("SELECT Date_Stamp, Time_Stamp FROM DEVICE_DATA_VIEW "
                 "WHERE IMEI = %s ")
    device_name = ("SELECT Device_Type FROM DEVICE_TYPE "
                 "WHERE Device_Type_ID = %s ")

    cursor1.execute(device_info)
    for device in cursor1:

        cursor2.execute(imei_date, (device['IMEI'],))

        cursor3.execute(account_name, (device['Account_ID'],))

        cursor4.execute(device_name, (device['Device_Type_ID'],))

        for name in cursor3:
            device.update({'Account_Name': name['ACCOUNT_NAME']})

        for device_type in cursor4:
            device.update({'Device': device_type['Device_Type']})

        for (dt) in cursor2:
            device.update({'Last_reported_date': dt['Date_Stamp']})
            device.update({'Last_reported_time': dt['Time_Stamp']})

        device_data.append(device)

    cursor3.close()
    cursor2.close()
    cursor1.close()
    cnx.close()
    # pprint.pprint(device_data)
    return device_data
