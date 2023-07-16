import random
import requests

# some free proxies
HTTP_PROXIES = [
    'http://129.151.91.248:80',
    'http://18.169.189.181:80',
    # ...
    'http://212.76.110.242:80'

]
HTTPS_PROXIES = [
    'http://31.186.239.245:8080',
    'http://5.78.50.231:8888',
    # ...
    'http://52.4.247.252:8129'
]

# a function to perform an HTTP request
# over a rotating proxy system
def rotating_proxy_request(http_method, url, max_attempts=3):
    response = None

    attempts = 1
    while attempts <= max_attempts:
        try:
            # get a random proxy
            http_proxy = random.choice(HTTP_PROXIES)
            https_proxy = random.choice(HTTPS_PROXIES)
            proxies = {
                'http': http_proxy,
                'https': https_proxy
            }

            print(f'Using proxy: {proxies}')

            # perform the request over the proxy
            # waiting up to 5 seconds to connect to the server
            # through the proxy before failing
            response = requests.request(http_method, url, proxies=proxies, timeout=5)

            break
        except Exception as e:
            # log the error
            print(e)

            print(f'{attempts} failed!')
            print(f'Trying with a new proxy...')

            # new attempt
            attempts += 1

    return response

response = rotating_proxy_request('get', 'https://www.g2.com/products/zenrows/reviews')
print(response.status_code)
