import requests
import json
category = 'fitness'
api_url = 'https://api.api-ninjas.com/v1/quotes?category={}'.format(category)
response = requests.get(api_url, headers={'X-Api-Key': 'eQTly/BTtC/bl6t3APTDSg==zGUXnjnEXYfOkAnI'})
# if response.status_code == requests.codes.ok:
#     print(response.text)
# else:
#     print("Error:", response.status_code, response.text)


s = response.text

# Parse the JSON string
data = json.loads(s)

# Access the values using keys
quote = data[0]['quote']
author = data[0]['author']
category = data[0]['category']

# Print the results
print("Quote:", quote)
print("Author:", author)
print("Category:", category)
