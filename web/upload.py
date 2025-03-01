from history_db import save_result_to_db
from request_results import get_request_to_nist
import sys


def handle_upload(user_id, bitseq: str, testtype: str,
                  alpha: str, optional_param: str):
    optional_param = optional_param if optional_param else None

    # Call NIST API and save result
    response = get_request_to_nist(testtype, bitseq, alpha, optional_param)
    print(response, file=sys.stderr)

    if response is None:
        return None, None

    if not response["success"]:
        return None, response["error"]

    p = response['p-value']
    status = 'PASS' if not response['isRejected'] else 'FAIL'

    # Save result to DB
    submission_id = save_result_to_db(user_id, testtype, bitseq, p,
                                      alpha, status)

    print("Submission Id: ", submission_id, file=sys.stderr)
    # Redirect to results
    return submission_id, None
