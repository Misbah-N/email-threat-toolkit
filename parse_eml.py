import re
import sys
from email import policy
from email.parser import BytesParser

URL_RE=re.compile(r"https?://[^\s<>\"']+")

def parse_eml(path):
    with open(path, "rb") as f:
        msg = BytesParser(policy=policy.default).parse(f)

    body = msg.get_body(preferencelist=("plain", "html"))
    text = body.get_content() if body else ""

    return{
        "from": msg["From"],
        "to": msg["To"],
        "subject": msg["Subject"],
        "received": msg.get_all("Received", []),
        "auth_results": msg.get("Authentication-Results"),
        "urls": URL_RE.findall(text),
    }

if __name__ == "__main__":
    result = parse_eml(sys.argv[1])
    for key, value in result.items():
        print(f"{key}: {value}")
