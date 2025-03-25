import requests
import json
from django.shortcuts import render
from datetime import datetime  # <-- Add this import
from collections import defaultdict

def home(request):
    # Fetch data from waterlevel.ie GeoJSON endpoint
    geojson_url = "https://waterlevel.ie/geojson/latest/"
    data_result = []

    try:
        response = requests.get(geojson_url, timeout=10)
        response.raise_for_status()
        geojson_data = response.json()

        # Group sensors by station
        stations = defaultdict(lambda: {
            'sensors': [],
            'coordinates': None,
            'values': []
        })

        for feature in geojson_data.get('features', []):
            props = feature.get('properties', {})
            geometry = feature.get('geometry', {})
            
            station_key = (
                props.get('station_ref'),
                props.get('station_name')
            )

            # Store station metadata
            stations[station_key]['coordinates'] = geometry.get('coordinates', [0, 0])
            stations[station_key]['sensors'].append({
                'sensor_ref': props.get('sensor_ref'),
                'value': props.get('value'),
                'datetime': props.get('datetime'),
                'csv_file': props.get('csv_file')
            })

            # Collect values for statistics
            try:
                stations[station_key]['values'].append(float(props.get('value', 0)))
            except (ValueError, TypeError):
                pass

        # Process each station's data
        for (station_ref, station_name), data in stations.items():
            if not data['values']:
                continue  # Skip stations with no valid values

            values = data['values']
            avg = sum(values) / len(values)
            
            data_result.append({
                'series_id': station_ref,
                'site_name': station_name,
                'longitude': data['coordinates'][0],
                'latitude': data['coordinates'][1],
                'average': avg,
                'max': max(values),
                'min': min(values),
                'maxRise': 0,  # Not available in current dataset
                'maxFall': 0,    # Not available in current dataset
                'sensor_count': len(data['sensors']),
                'last_updated': max(s['datetime'] for s in data['sensors'])
            })

    except requests.exceptions.RequestException as e:
        print(f"API request failed: {str(e)}")
    except json.JSONDecodeError:
        print("Invalid JSON response from API")
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
    return render(request, 'index.html', {
        'data': (data_result),
        'last_fetched': datetime.now().isoformat()
    })