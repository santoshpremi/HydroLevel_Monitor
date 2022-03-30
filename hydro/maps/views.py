# Create your views here
def home(request):
    from_date = request.GET.get('datefrom')
    to_date = request.GET.get('dateto')
    from datetime import date
    if not from_date and not to_date:
        today = date.today()
        from_date = today
        to_date = today

    import requests
    series_data = requests.get(
        'https://hydrology.gov.np/gss/api/socket/river_test/response').json()
    # print(type(series_data))
    data_result = []
    for x in series_data:
        try:
            if x['series_id']:
                series_value = x['series_id']
                longitude = x['longitude']
                latitude = x['latitude']
                # average dict
                data = {}
                data['series_id'] = series_value
                data['longitude'] = longitude
                data['latitude'] = latitude               
                all_data = requests.get(
                    'https://hydrology.gov.np/gss/api/observation?series_id={series_value}&date_from={from_date}T01:00:00&date_to={to_date}T01:00:00'.format(series_value=series_value, from_date=from_date, to_date=to_date)).json()
            
                water_level_value = [float(i['value']) for i in all_data['data']]

                #average
                average_value = sum(water_level_value)/len(water_level_value)
                data['average'] = average_value
                data_result.append(data)
                # max
                maximum_value = max(water_level_value)
                data['max'] = maximum_value
                data_result.append(data)
                #min
                minimum_value = min(water_level_value)
                data['min'] = minimum_value
                data_result.append(data)
                #maxRise
                def max_increase(value_list):
                    values = len(value_list)-1
                    max_rise=0
                    for i in range(values):                       
                        diff_rise = value_list[i+1]-value_list[i]
                        if(diff_rise > max_rise>=0):
                            max_rise=diff_rise
                    return max_rise
                max_value= water_level_value
                data['maxRise'] = max_increase(max_value)               
                data_result.append(data)
                #maxfall
                def max_decrease(value_list):
                    values = len(value_list)-1
                    max_fall=0
                    for i in range(values):                       
                        diff_fall = value_list[i]-value_list[i+1]
                        if(diff_fall > max_fall>=0):
                            max_fall=diff_fall
                    return max_fall
                max_value= water_level_value
                data['maxFall'] = max_decrease(max_value)
                data_result.append(data)
               
        except:
            pass
    from json import dumps
    data = dumps(data_result)
    from django.shortcuts import render
    return render(request, 'maps/home.html', context={
        "data": data,

    })
