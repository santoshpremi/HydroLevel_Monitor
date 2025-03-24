from django.shortcuts import render
from datetime import date
import requests
from json import dumps

def home(request):
    # Get date parameters from request
    from_date = request.GET.get('datefrom')
    to_date = request.GET.get('dateto')
    
    # Set default dates to today if not provided
    if not from_date or not to_date:
        today = date.today().isoformat()
        from_date = today
        to_date = today

    # USGS API base URLs
    usgs_sites_url = "https://waterservices.usgs.gov/nwis/site/"
    usgs_iv_url = "https://waterservices.usgs.gov/nwis/iv/"
    
    # Example site codes (replace with actual site codes for your area)
    site_codes = ["01581680", "01582500", "01583000"]  # USGS site codes

    data_result = []

    for site_code in site_codes:
        try:
            # Get site information
            site_params = {
                "sites": site_code,
                "format": "json"
            }
            site_response = requests.get(usgs_sites_url, params=site_params)
            site_data = site_response.json()

            # Extract site coordinates
            try:
                longitude = site_data['value']['sites'][0]['longitude']
                latitude = site_data['value']['sites'][0]['latitude']
            except (KeyError, IndexError):
                continue  # Skip if coordinates not available

            # Base data structure
            data = {
                'series_id': site_code,
                'longitude': longitude,
                'latitude': latitude
            }

            # Get water level data
            iv_params = {
                "sites": site_code,
                "parameterCd": "00060",  # Streamflow parameter code
                "format": "json",
                "startDT": from_date,
                "endDT": to_date
            }
            iv_response = requests.get(usgs_iv_url, params=iv_params)
            iv_data = iv_response.json()

            # Extract water level values
            try:
                water_level_values = [
                    float(val['value']) 
                    for val in iv_data['value']['timeSeries'][0]['values'][0]['value']
                ]
            except (KeyError, IndexError, ValueError):
                water_level_values = []

            # Calculate statistics
            if water_level_values:
                data['average'] = sum(water_level_values) / len(water_level_values)
                data['max'] = max(water_level_values)
                data['min'] = min(water_level_values)

                # Calculate max rise and fall
                def calculate_max_change(values, rise=True):
                    max_change = 0
                    for i in range(len(values) - 1):
                        if rise:
                            change = values[i+1] - values[i]
                        else:
                            change = values[i] - values[i+1]
                        if change > max_change:
                            max_change = change
                    return max_change

                data['maxRise'] = calculate_max_change(water_level_values)
                data['maxFall'] = calculate_max_change(water_level_values, rise=False)
            else:
                data['average'] = 0
                data['max'] = 0
                data['min'] = 0
                data['maxRise'] = 0
                data['maxFall'] = 0

            data_result.append(data)
            
        except Exception as e:
            print(f"Error processing site {site_code}: {str(e)}")
            continue

    return render(request, 'index.html', context={
        "data": dumps(data_result),
    })