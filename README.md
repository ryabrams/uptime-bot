# 🤖 Website Uptime Checker

Automated website uptime monitoring using GitHub Actions. This tool checks your website every 15 minutes and sends email alerts when downtime is detected.

## ⚡️ Features

- 🕐 Checks website availability every 15 minutes
- 📧 Email alerts when your site goes down
- 📊 Maintains a log of all checks (successful and failed)
- 🔄 Automatically runs on GitHub Actions
- 🔐 Secure credential handling

## 🧩 Project Structure

```
website-uptime-checker/
├── .devcontainer/
│   └── devcontainer.json
├── .github/
│   └── workflows/
│       └── uptime-check.yml
├── .gitignore
├── website_checker.py
├── requirements.txt
├── uptime_log.json
├── README.md
└── LICENSE
```

## 🛠️ Setup Instructions

### 1. Create a Gmail App Password

For security reasons, Gmail requires an App Password instead of your regular password:

1. Go to your [Google Account](https://myaccount.google.com/)
2. Select Security
3. Under "Signing in to Google," select 2-Step Verification
4. At the bottom of the page, select App passwords
5. Enter a name for the app password (e.g., "GitHub Uptime Checker")
6. Click "Create" and copy the generated password

### 2. Set Up GitHub Repository Secrets

1. Go to your GitHub repository
2. Navigate to Settings > Secrets and variables > Actions
3. Add the following secrets:
   - `EMAIL_USERNAME`: Your full Gmail address (e.g., youremail@gmail.com)
   - `EMAIL_APP_PASSWORD`: The app password generated in step 1

### 3. Customize the Configuration

Edit `website_checker.py` to set your specific website URL:

```python
WEBSITE_URL = "https://example.com"  # Replace with your actual website
```

### 4. Enable GitHub Actions

Make sure GitHub Actions are enabled for your repository:

1. Go to Actions tab
2. If prompted, click "I understand my workflows, go ahead and enable them"

### 5. Trigger the Workflow

The workflow will automatically run every 15 minutes (once enabled), but you can trigger it manually:

1. Go to Actions tab
2. Select "Website Uptime Check" workflow
3. Click "Run workflow"

## 🖥️ Managing GitHub Actions

### Initial Setup (Actions Disabled)

The GitHub Actions workflow is initially configured to run **only when manually triggered**. The automatic schedule is commented out in the workflow file:

```yaml
on:
  # schedule:
  #   - cron: '*/15 * * * *'  # Run every 15 minutes
  workflow_dispatch:  # Allow manual trigger only
```

This allows you to:
1. Set up the repository and test everything manually first
2. Add your secrets and verify configurations
3. Make any necessary adjustments before enabling automatic runs

### Enabling Scheduled Runs

When you're ready to enable automatic checks every 15 minutes:

1. Edit the `.github/workflows/uptime-check.yml` file
2. Uncomment the schedule section:
   ```yaml
   on:
     schedule:
       - cron: '*/15 * * * *'  # Run every 15 minutes
     workflow_dispatch:  # Allow manual trigger
   ```
3. Commit and push this change

### Temporarily Disabling Actions

If you need to temporarily disable the automatic checks:

1. Go to your repository on GitHub
2. Navigate to Actions → Website Uptime Check
3. Click "..." (three dots) menu
4. Select "Disable workflow"

You can re-enable it from the same location when needed.

## 🧪 Testing and Development

### Running in Test Mode

For development and testing purposes, you can run the script in test mode, which prevents it from sending actual emails or writing to the log file:

```bash
# Run in test mode (no emails, no log writes)
python website_checker.py --test

# Test the alert system by forcing the website to be considered "down"
python website_checker.py --test --force-down
```

In test mode, the script will:
- Still perform the actual website check (unless using --force-down)
- Print what would be logged or emailed, without actually doing it
- Not modify the uptime_log.json file

### Using the Dev Container

When working within the dev container:

1. All dependencies are automatically installed
2. You can run tests without affecting your production environment
3. Code formatting and linting tools are pre-configured

To run the script inside the dev container:
1. Open the terminal in VS Code
2. Run the script with the test flag: `python website_checker.py --test`

## 🔎 Understanding the Logs

The `uptime_log.json` file contains a record of all checks:

```json
{
  "checks": [
    {
      "timestamp": "2025-03-09T12:00:00.123456",
      "is_up": true,
      "status_code": 200,
      "response_time": 0.543,
      "error_message": null
    },
    ...
  ]
}
```

## 🆘 Troubleshooting

If you encounter issues:

1. Check the GitHub Actions logs for error messages
2. Verify your secrets are set correctly
3. Ensure your Gmail account allows less secure apps or is properly set up with an app password
4. Check if GitHub Actions has proper permissions to commit to your repository

## 🪪 License

This project is open source and available under the MIT License.