import requests
import datetime
import smtplib
import os
import json
import argparse
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path

# Configuration
WEBSITE_URL = "https://example.com"  # Replace with your actual website
CHECK_TIMEOUT = 30  # seconds
LOG_FILE = "uptime_log.json"
EMAIL_FROM = os.environ.get("EMAIL_USERNAME")
EMAIL_TO = os.environ.get("EMAIL_USERNAME")  # Sending to self

def check_website():
    """Check if the website is up and return status information."""
    timestamp = datetime.datetime.now().isoformat()
    try:
        response = requests.get(WEBSITE_URL, timeout=CHECK_TIMEOUT)
        is_up = 200 <= response.status_code < 300
        status_code = response.status_code
        response_time = response.elapsed.total_seconds()
        error_message = None
    except Exception as e:
        is_up = False
        status_code = None
        response_time = None
        error_message = str(e)
    
    return {
        "timestamp": timestamp,
        "is_up": is_up,
        "status_code": status_code,
        "response_time": response_time,
        "error_message": error_message
    }

def log_check(check_result, test_mode=False):
    """Log the check result to a JSON file."""
    if test_mode:
        print("[TEST MODE] Would log the following:")
        print(json.dumps(check_result, indent=2))
        return None
    
    log_path = Path(LOG_FILE)
    
    # Load existing log if it exists
    if log_path.exists():
        with open(log_path, 'r') as f:
            try:
                log_data = json.load(f)
            except json.JSONDecodeError:
                log_data = {"checks": []}
    else:
        log_data = {"checks": []}
    
    # Add new check result
    log_data["checks"].append(check_result)
    
    # Write updated log
    with open(log_path, 'w') as f:
        json.dump(log_data, f, indent=2)
    
    return log_path

def send_alert_email(check_result, test_mode=False):
    """Send an email alert when the website is down."""
    if test_mode:
        print("[TEST MODE] Would send email alert with the following content:")
        print(f"Subject: ⚠️ ALERT: Website {WEBSITE_URL} is DOWN!")
        print(f"To: {EMAIL_TO}")
        print("\nEmail body would contain check details")
        return
    
    subject = f"⚠️ ALERT: Website {WEBSITE_URL} is DOWN!"
    
    # Create email message
    msg = MIMEMultipart()
    msg['From'] = EMAIL_FROM
    msg['To'] = EMAIL_TO
    msg['Subject'] = subject
    
    # Email body
    body = f"""
    ⚠️ Your website appears to be down! ⚠️
    
    URL: {WEBSITE_URL}
    Time of check: {check_result['timestamp']}
    
    """
    
    if check_result['status_code'] is not None:
        body += f"Status code: {check_result['status_code']}\n"
    
    if check_result['error_message'] is not None:
        body += f"Error message: {check_result['error_message']}\n"
    
    body += "\nThis is an automated message from your GitHub Actions uptime checker."
    
    msg.attach(MIMEText(body, 'plain'))
    
    # Send email
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(os.environ.get("EMAIL_USERNAME"), os.environ.get("EMAIL_PASSWORD"))
        server.send_message(msg)
        server.quit()
        print("Alert email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {str(e)}")

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Check website uptime")
    parser.add_argument("--test", action="store_true", help="Run in test mode (no emails, no logs)")
    parser.add_argument("--force-down", action="store_true", help="Force website to be considered down (for testing alerts)")
    args = parser.parse_args()
    
    # Check website status
    result = check_website()
    
    # If testing with forced down state
    if args.force_down:
        result["is_up"] = False
        result["status_code"] = 500
        result["error_message"] = "Forced down state for testing"
        print("[TEST MODE] Forcing website down state")
    
    print(f"Website check result: {'UP' if result['is_up'] else 'DOWN'}")
    print(f"Status code: {result['status_code']}")
    print(f"Response time: {result['response_time']} seconds")
    
    # Log the result (unless in test mode)
    log_file = log_check(result, test_mode=args.test)
    if not args.test:
        print(f"Check logged to {log_file}")
    
    # Send alert if website is down
    if not result['is_up']:
        print("Website is DOWN! Sending alert email...")
        send_alert_email(result, test_mode=args.test)

if __name__ == "__main__":
    main()
