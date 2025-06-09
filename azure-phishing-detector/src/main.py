# main.py

from fetch_emails import get_access_token, get_latest_emails
from analyze_with_azure import analyze_email
from detect_phishing import detect_phishing  # Add this import if detect_phishing is defined in detect_phishing.py
from sendTo import send_to_sentinel  # Adjusted import to match the function name in sendTo.py
import os
from dotenv import load_dotenv
from bs4 import BeautifulSoup

load_dotenv()

def main():
    token = get_access_token()
    user_email = os.getenv("GRAPH_USER_EMAIL")
    emails = get_latest_emails(user_email, token)

    for idx, email in enumerate(emails):
        subject = email.get("subject", "N/A")
        sender = email.get("from", {}).get("emailAddress", {}).get("address", "Unknown")

        raw_body = email.get("body", {}).get("content", "")
        soup = BeautifulSoup(raw_body, "html.parser")
        body = soup.get_text(separator="\n", strip=True)


        email_data = {
            "subject": subject,
            "sender": sender,
            "body": body
        }

        print(f"--- Email {idx+1} ---")
        print("Subject:", subject)
        print("From:", sender)
        # print("Body:", body[:300] + "..." if len(body) > 300 else body)

        analysis = analyze_email(email_data)

        print("Sentiment:", analysis["sentiment"])
        print("Entities:", analysis["entities"])
        print("Key Phrases:", analysis["keyPhrases"])

        if detect_phishing(analysis):
            send_to_sentinel(email_data)
            print("⚠️  Phishing suspecté !")
        else:
            print("✅ Pas de phishing détecté.")
        print()
        print()

if __name__ == "__main__":
    main()
