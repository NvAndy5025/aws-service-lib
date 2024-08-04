import requests

#gets token by calling oidc api using client credentials
def get_token():
  
  url = "https://dev-h0634160h8l03pmt.us.auth0.com/oauth/token"
  headers = {
      "Content-Type": "application/json"
  }
  cookies = {
      "did": "s%3Av0%3A6ee7f480-18e4-11ef-853b-2ba9eb70a9e4.0HnPZBeGKwPgGweN2IHtf1mkzq6OPybtWPQD6%2BtY5rI",
      "did_compat": "s%3Av0%3A6ee7f480-18e4-11ef-853b-2ba9eb70a9e4.0HnPZBeGKwPgGweN2IHtf1mkzq6OPybtWPQD6%2BtY5rI"
  }
  data = {
      "client_id": "Jj1FckpzUkUKMQ0ndWcPWIX4H6cGOm0S",
      "client_secret": "ewrykonV58XqBTEFK_5KZ62CVbE2w18lzGuZVwyg7-WjfH0Z7bWMI6UnxbRnMfgf",
      "audience": "http://localhost:3000",
      "grant_type": "client_credentials"
  }

  try:
      # Send POST request with headers, cookies, and JSON data
      response = requests.post(url, headers=headers, cookies=cookies, json=data)
      if response.status_code == 200:
          # Return the JSON response data (containing the token)
          return response.json().get('access_token')
      else:
          print(f"Error: {response.status_code}")
          print(response.text)
          return None

  except requests.exceptions.RequestException as e:
      print(f"Error: {e}")
      return None