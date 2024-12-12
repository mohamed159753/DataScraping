import requests
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def fetch_data(api_url, pages):
    all_data = []

    for page in range(1, pages + 1):
        url = api_url.format(page=page)
        logger.info('Fetching data from URL: %s', url)
        response = requests.get(url)
        status_code = response.status_code

        if status_code == 200:
            response_json = response.json()
            places = response_json.get('places', [])
            if places:
                for place in places:
                    address = place.get('address', {})
                    street = address.get('street', 'N/A')
                    zipcode = address.get('zipcode', 'N/A')
                    city = address.get('city', 'N/A')
                    full_address = f"{street}, {zipcode}, {city}"

                    phone_number = place.get('phone', 'N/A')

                    data_entry = {
                        'name': place.get('name', 'N/A'),
                        'address': full_address,
                        'phone': phone_number,
                        'url': f"https://www.bokadirekt.se/places/{place.get('slug', '')}"
                    }
                    all_data.append(data_entry)
            else:
                logger.info(f"No data found on page {page}")
        else:
            logger.error('Failed to fetch data for page %d: %s', page, status_code)

    return all_data

def format_data(data):
    formatted_data = []
    for idx, entry in enumerate(data, 1):
        formatted_data.append("==================================================")
        formatted_data.append(f"{idx} {entry['url']}")
        formatted_data.append(f"name : {entry['name']}")
        formatted_data.append(f"address : {entry['address']}")
        formatted_data.append(f"phone : {entry['phone']}")
        formatted_data.append("--------------------------------------------------")

    return "\n".join(formatted_data)

def main():
    api_url = 'https://www.bokadirekt.se/api/search?q=sk%C3%B6nhet&location=G%C3%B6teborg&startDate=2024-07-14&endDate=2024-08-14&version=2&page={page}'
    pages = 20 # Assuming there are 20 pages of data (adjust if needed)

    try:
        data = fetch_data(api_url, pages)
        if data:
            formatted_data = format_data(data)
            # Print to console
            print(formatted_data)
            # Write to a text file
            with open('clinics_goteborg.txt', 'w', encoding='utf-8') as f:
                f.write(formatted_data)
            logger.info('Text file "clinics_goteborg.txt" has been created with the clinic entries.')
        else:
            logger.warning('No data fetched to write to text file.')
    except Exception as e:
        logger.error('Error during data fetch or processing: %s', str(e))

if __name__ == "__main__":
    main()
