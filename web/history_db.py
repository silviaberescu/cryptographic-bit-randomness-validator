import mysql.connector

# Database configuration
db_config = {
    'host': 'mysql',
    'user': 'root',
    'password': 'rootpassword',
    'database': 'mydatabase'
}


# Helper function to get a database connection
def get_db_connection():
    conn = mysql.connector.connect(**db_config)
    return conn


# not tested
def save_result_to_db(id_user, stattest, bitseq, p_value,
                      significance, status):
    '''
    Save the result of the statistical test to the database.
    :param id_user: The ID of the user who ran the test.
    :param bitseq: The bit sequence used for the test.
    :param stattest: The type of statistical test performed
    the valid entries are: monobit, mbit, runs, autocorrelation, serial
    :param p_value: The p-value of the test.
    :param significance: The significance level used for the test.
    :param status: The status of the test (e.g., "PASSED", "FAILED").
    :return: True if the result was saved successfully, False otherwise.
    '''
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        bitseq_binary = int(bitseq, 2).to_bytes((len(bitseq) + 7) // 8,
                                                byteorder='big')
        # Convert bit sequence to binary
        # bitseq_binary = bitseq.encode('utf-8')

        if isinstance(p_value, list):
            p_value = ','.join(map(str, p_value))

        cursor.execute(
            "INSERT INTO history (id_user, stattest, bitseq, pvalue,\
                significance, stat) VALUES (%s, %s, %s, %s, %s, %s)",
            (id_user, stattest, bitseq_binary, p_value, significance, status)
        )
        conn.commit()

        cursor.execute("SELECT LAST_INSERT_ID()")
        last_id = cursor.fetchone()[0]

        return last_id
    except mysql.connector.Error as err:
        print(f'Error saving result to database: {err}')
        return None
    finally:
        cursor.close()
        conn.close()


# not tested
def retrieve_results_from_db(id_user, stattest=None, date_from=None):
    '''
    Retrieve the results of the statistical tests for a given user.
    :param id_user: The ID of the user.
    :param stattest: The type of statistical test to filter by (e.g. "monobit")
    :param date_from: The start date to filter by (e.g., "2021-12-25").
    :return: A list of dictionaries containing the results of the tests
    '''
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    query = "SELECT * FROM history WHERE id_user = %s"
    params = [id_user]

    if stattest and stattest != 'all':
        query += " AND stattest = %s"
        params.append(stattest)

    if date_from:
        query += " AND date_time BETWEEN %s AND %s"
        params.append(date_from + " 00:00:00")
        params.append(date_from + " 23:59:59")

    cursor.execute(query, tuple(params))
    results = cursor.fetchall()

    for result in results:
        bitseq_binary = result['bitseq']
        bitseq = bin(int.from_bytes(bitseq_binary, byteorder='big'))[2:]
        result['bitseq'] = bitseq

    cursor.close()
    conn.close()

    return results


def get_submission_from_id(id_submission):
    '''
    Retrieve the submission from the database given its ID.
    :param id_submission: The ID of the submission.
    :return: A dictionary containing the submission details
    or None if not found.
    '''
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("SELECT * FROM history WHERE id_submission = %s",
                       (id_submission,))
        submission = cursor.fetchone()

        if not submission:
            return None

        # Convert bit sequence to binary
        bitseq_binary = submission['bitseq']
        bitseq = bin(int.from_bytes(bitseq_binary, byteorder='big'))[2:]
        submission['bit_sequence'] = bitseq  # Renamed the key to bit_sequence
        del submission['bitseq']  # Delete the old key

        return submission

    except Exception as e:
        print(f"Error retrieving submission from database: {e}")
        return None

    finally:
        cursor.close()
        conn.close()


def delete_result_from_db(id_submission, user_id):
    '''
    Delete a result from the database by its ID.
    :param id_submission: The ID of the submission to delete.
    :param user_id: The ID of the user trying to delete the result.
    :return: True if the result was successfully deleted, False otherwise.
    '''
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("DELETE FROM history WHERE id_submission = %s AND\
                       id_user = %s", (id_submission, user_id))
        conn.commit()

        if cursor.rowcount > 0:
            return True
        else:
            return False
    except mysql.connector.Error as err:
        print(f"Error deleting result: {err}")
        return False
    finally:
        cursor.close()
        conn.close()
