import requests

def get_data(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print('Error:', response.text)
        return None

def post_data(url, data):
    response = requests.post(url, json=data)
    if response.status_code == 201:
        return response.json()
    else:
        print('Error:', response.text)
        return None

def put_data(url, data):
    response = requests.put(url, json=data)
    if response.status_code == 200:
        return response.json()
    else:
        print('Error:', response.text)
        return None

def delete_data(url):
    response = requests.delete(url)
    if response.status_code == 200:
        return response.json()
    else:
        print('Error:', response.text)
        return None

def main():
    base_url = 'http://localhost:5000'
    
    # Example usage
    
    # Get data from the '/energy' endpoint
    energy_url = base_url + '/energy'
    energy_data = get_data(energy_url)
    if energy_data:
        print('Energy Data:', energy_data)
    
    # Create a new energy record
    create_record_url = energy_url
    record_data = {
        'consumption': 100,
        'time': '2023-07-01T12:00:00',
        'cost': 1000
    }
    created_record = post_data(create_record_url, record_data)
    if created_record:
        print('Created Record:', created_record)
    
    # Update an existing energy record
    record_id = '64a0862b569a1ed89b136457'  # Replace with the actual record ID
    update_record_url = energy_url + '/' + record_id
    updated_data = {
        'consumption': 200,
        'time': '2023-07-01T12:00:00',
        'cost': 2000
    }
    updated_record = put_data(update_record_url, updated_data)
    if updated_record:
        print('Updated Record:', updated_record)
    
    # Delete an energy record
    delete_record_url = energy_url + '/' + record_id
    deleted_record = delete_data(delete_record_url)
    if deleted_record:
        print('Deleted Record:', deleted_record)

if __name__ == '__main__':
    main()
