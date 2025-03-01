import requests
import json
import sys
import base64


def get_request_to_nist(model_name, bit_string, significance,
                        optional_param=None):
    '''
    Send a GET request to the nist server with the given parameters.
    Return the response text.
    Example: {"isRejected":true,"p-value":1.2441921148543639e-15}
    '''
    # nist server url
    url = "http://nist:5001/compute"

    bit_string = base64.b64encode(bit_string.encode()).decode()
    params = {
        'model_name': model_name,
        'bit_string': bit_string,
        'significance': significance,
    }

    if optional_param is not None:
        params['optional_param'] = optional_param

    try:
        response = requests.get(url, params=params)

        print(f"Request to {url} with params {params} returned status code ",
              response.status_code, file=sys.stderr)

        try:
            # Try to parse the JSON response
            result = json.loads(response.text)
            return result  # Return the parsed JSON as a Python dictionary
        except json.JSONDecodeError:
            print(f"Error decoding JSON response: {response.text}",
                  file=sys.stderr)
            return None

    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}", file=sys.stderr)
        return None


if __name__ == "__main__":
    bitseq = "101011001011010100101010101010100100101"
    result = get_request_to_nist("monobit", bitseq, 0.05)
    print("Monobit: ", result)
    result = get_request_to_nist("mbit", bitseq, 0.05, 10)
    print("Mbit: ", result)
    result = get_request_to_nist("autocorrelation", bitseq, 0.05, 1)
    print("Autocorrelation: ", result)
    result = get_request_to_nist("serial", bitseq, 0.05, 4)
    print("Serial: ", result)
    result = get_request_to_nist("runs", bitseq, 0.05)
    print("Runs: ", result)
