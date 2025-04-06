import json
import requests
import os
from dotenv import load_dotenv
load_dotenv()

from algo import compute, calculate_risk

URL = "mts-prism.com"
PORT = 8082

# Please do NOT share this information anywhere, unless you want your team to be cooked.
TEAM_API_CODE = os.getenv("TEAM_API_CODE")
# @cyrus or @myguysai on Discord if you need an API key

def send_get_request(path):
    """
    Sends a HTTP GET request to the server.
    Returns:
        (success?, error or message)
    """
    headers = {"X-API-Code": TEAM_API_CODE}
    response = requests.get(f"http://{URL}:{PORT}/{path}", headers=headers)

    # Check whether there was an error sent from the server.
    # 200 is the HTTP Success status code, so we do not expect any
    # other response code.
    if response.status_code != 200:
        return (
            False,
            f"Error - something went wrong when requesting [CODE: {response.status_code}]: {response.text}",
        )
    return True, response.text


def send_post_request(path, data=None):
    """
    Sends a HTTP POST request to the server.
    Pass in the POST data to data, to send some message.
    Returns:
         (success?, error or message)
    """
    headers = {"X-API-Code": TEAM_API_CODE, "Content-Type": "application/json"}

    # Convert the data from python dictionary to JSON string,
    # which is the expected format to be passed
    data = json.dumps(data)
    response = requests.post(f"http://{URL}:{PORT}/{path}", data=data, headers=headers)

    # Check whether there was an error sent from the server.
    # 200 is the HTTP Success status code, so we do not expect any
    # other response code.
    if response.status_code != 200:
        return (
            False,
            f"Error - something went wrong when requesting [CODE: {response.status_code}]: {response.text}",
        )
    return True, response.text


def get_context():
    """
    Query the challenge server to request for a client to design a portfolio for.
    Returns:
        (success?, error or message)
    """
    return send_get_request("/request")


def get_my_current_information():
    """
    Query your team information.
    Returns:
        (success?, error or message)
    """
    return send_get_request("/info")


def send_portfolio(weighted_stocks):
    """
    Send portfolio stocks to the server for evaluation.
    Returns:
        (success?, error or message)
    """
    if weighted_stocks:
        data = [
            {"ticker": weighted_stock[0], "quantity": weighted_stock[1]}
            for weighted_stock in weighted_stocks
        ]
        return send_post_request("/submit", data=data)
    else:
        return (True, "Not sent")


success, information = get_my_current_information()
if not success:
    print(f"Error: {information}")
print(f"Team information: ", information)

success, context = get_context()
if not success:
    print(f"Error: {context}")
print(f"Context provided: ", context)
print(compute(eval(context)["message"]))

# Maybe do something with the context to generate this?
with open("log3.txt", "a") as f:
    f.write(eval(context)["message"] + "\n")
    # f.write("PARSED: " + str(extract_preferences(eval(context)["message"])) + "\n")
    try:
        portfolio = compute(eval(context)["message"])
    except Exception:
        pass
    ctx = json.loads(eval(context)["message"])
    try:
        f.write("BUDG/SAL:" + str(ctx["budget"]/ctx["salary"]) + "\n")
        f.write("RISK:" + str(calculate_risk(ctx["age"], ctx["employed"], ctx["budget"]/ctx["salary"])) + "\n")

    except ZeroDivisionError:
        f.write("RISK:" + str(calculate_risk(ctx["age"], ctx["employed"], 0)) + "\n")
        pass
    
    f.write("PORTF:" + str(portfolio) + "\n")
    success, response = send_portfolio(portfolio)
    if not success:
        f.write(f"Error: {response}\n")
        f.write(f"Evaluation response: {response}\n")
        pass
    f.write(f"Evaluation response: {response}\n")