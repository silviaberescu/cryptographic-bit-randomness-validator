from flask import Flask, request
from stattests.autocorrelation import autocorrelation
from stattests.mbit import mbit
from stattests.monobit import monobit
from stattests.runs import runs
from stattests.serial import serial
from stattests import utils
import base64
import sys


app = Flask(__name__)


@app.route('/compute', methods=['GET'])
def compute():
    """
    Compute the p-value of the given bit string using the specified model
    :param model_name: the name of the model to use (autocorrelation, monobit,
                        runs, serial, mbit)
    :param bit_string: the bit string to test
    :param significance: the significance level (alpha, by default 0.05)
    :param optional_param: optional parameter for the model (e.g. M for serial)
    :return: a tuple with the p-value and a boolean value indicating if the
    null hypothesis was rejected
    """

    model_name = request.args.get('model_name').strip().lower()
    bit_string = request.args.get('bit_string')
    significance = request.args.get('significance', "0.05")
    optional_param = request.args.get('optional_param', "")

    print("Request received", file=sys.stderr)
    print("Model name: ", model_name, file=sys.stderr)
    print("Bit string: ", bit_string, file=sys.stderr)
    print("Significance: ", significance, file=sys.stderr)
    print("Optional param: ", optional_param, file=sys.stderr)

    try:
        bit_string = base64.b64decode(bit_string).decode('utf-8')
    except (base64.binascii.Error, UnicodeDecodeError):
        return {"success": False, "error": "Invalid base64 encoding"}, 400

    if not model_name or not bit_string:
        return {"success": False, "error": "Missing required parameters"}, 400

    bit_string = [int(bit) for bit in bit_string]
    significance = float(significance)

    if len(optional_param) > 0:
        optional_param = int(optional_param)
    else:
        optional_param = None

    # Validate the input parameters
    if not utils.validate_bit_sequence(bit_string):
        return {"success": False, "error": "Invalid bit sequence"}, 400

    # Validate the significance level
    if not utils.validate_alpha(significance):
        return {"success": False, "error": "Invalid significance"}, 400

    # Validate the optional parameter
    if model_name == "serial" and not utils.validate_M_param_serial(
                                        int(optional_param), len(bit_string)):
        return {"success": False, "error": "Invalid M parameter"}, 400

    # Validate the optional parameter
    if model_name == "mbit" and not utils.validate_M_param_Mbit(
                                        int(optional_param), len(bit_string)):
        return {"success": False, "error": "Invalid M parameter"}, 400

    # Validate the optional parameter
    if model_name == "autocorrelation" and not utils.validate_d(
                                        int(optional_param), len(bit_string)):
        return {"success": False, "error": "Invalid d parameter"}, 400

    # Compute the p-value for the chosen model
    pvalue = -1
    if model_name == "autocorrelation":
        pvalue = autocorrelation(bit_string, optional_param)
    elif model_name == "monobit":
        pvalue = monobit(bit_string)
    elif model_name == "runs":
        pvalue = runs(bit_string)
    elif model_name == "serial":
        pvalue = serial(bit_string, optional_param)
    elif model_name == "mbit":
        pvalue = mbit(bit_string, optional_param)

    # Check if the null hypothesis is rejected
    if isinstance(pvalue, tuple):
        rejected = (bool)(pvalue[0] < significance) \
            or (bool)(pvalue[1] < significance)
    else:
        rejected = (bool)(pvalue < significance)

    if pvalue != -1:
        pvalue = round(pvalue, 5)
        return {"success": True, "p-value": pvalue, "isRejected": rejected}, \
            200

    return {"success": False, "error": "Model not found"}, 400


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
