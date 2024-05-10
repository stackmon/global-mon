# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License

import time
import requests
import logging


def heartbeat_check(elements):
    """
    This function takes a dictionary 

    service_name:
        urls:
            - url1
            ...
    
    It returns the dictionary, result, containing return_code and return_time

    service_name:
        - url: url1
          return_code: x
          return_time: x ms
          
    """
    result = {}
    for service, url_list in elements.items():
        logging.info(f"Checking {service}...")
        result[service] = {}
        for url in url_list['urls']:
            try:
                start_time = time.time()
                response = requests.get(url)
                end_time = time.time()
                response_time = (end_time - start_time) * 1000  # Convert to milliseconds
                return_data = {
                    'return_code': response.status_code,
                    'return_time': f"{response_time:.2f} ms"
                }
                result[service][url] = return_data
            except requests.RequestException as e:
                return_data = {
                    'return_code': 'Error',
                    'return_time': str(e)
                }
                result[service][url] = return_data
    return result