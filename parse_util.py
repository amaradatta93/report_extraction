import datetime, pprint


def date_time_conversion(date_str, time_str):
    '''
    Convert the date and time string into a single data_time object
    :param date_str: Date string
    :param time_str: Time string
    :return: Date_Time object
    '''
    dt = date_str + 'T' + time_str
    date_time = datetime.datetime.strptime(dt, '%d.%m.%YT%H:%M:%S')
    return date_time


def two_days_back(dt_obj, threshold_days):
    '''
    Check if the difference between the present time and the date parameter is less than two days
    :param dt_obj: Date_Time object
    :return: Boolean True/False based on the time-delta
    '''
    now = datetime.datetime.strptime(datetime.datetime.now().strftime('%d.%m.%YT%H:%M:%S'), '%d.%m.%YT%H:%M:%S')
    diff = now - dt_obj
    return diff.days > datetime.timedelta(days=int(threshold_days)).days


def parsed_dict(unparsed_dict):
    '''
    The key-value pair in the dictionary is filtered out and reduced
    :param unparsed_dict: Dictionary containing all the key-value pairs
    :return: Dictionary containing only required key-value pairs
    '''
    parameter_optimized = []
    for each_dict in unparsed_dict:
        parameter_optimized.append({
            'Account_Name': each_dict['Account_Name'],
            'IMEI': each_dict['IMEI'],
            'Device': each_dict['Device'],
            # 'SIM_No': str(each_dict['SIM_No']),
            'Last_reported_date': each_dict['Last_reported_date'],
            'Last_reported_time': each_dict['Last_reported_time'],
            'Added_On': each_dict['Added_On'],
            'Asset_No': each_dict['Asset_No'],
            # 'Comments': each_dict['Comments']
        })
    return parameter_optimized
