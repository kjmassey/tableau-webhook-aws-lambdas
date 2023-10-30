### DataDev Day November 2023
# Tableau Webhooks + AWS Lambda
##### Kyle Massey | *Twitter/X*: @UpInYourVizness | *github*: @kjmassey
---
### Installation
##### NOTE: Exact cli/terminal syntax may vary by OS
1. Clone this repo
2. Create Python virtual environment:
   - *python -m venv name_of_env*
   - *name_of_env* = your virtual environment name
   - 'venv' is just fine :)
3. Activate your virtualenv
   - e.g. *source venv/Scripts/activate* (bash)

---
### Example tableauserverclient (TSC) calls for Webhooks:
###### /tsc_webhooks

A collection of code examples which use the *tableauserverclient (TSC)* for Python to manage Webhooks on Tableau Server.

##### Configuration
1. Open **tsc_webhooks > tsc_constants.py**
2. Update the following values with your own:
   ```
    TSC_SERVER_URL = "YOUR_TABLEAU_SERVER_URL"
    TSC_SITE_NAME = "YOUR_SITE_NAME"

    # Tableau Personal Access Token Authentication
    PAT_NAME = "YOUR_PAT_NAME"
    PAT_SECRET = "YOUR_PAT_SECRET"
   ```
---
### Example Lambda Functions
###### /email_alerter
A simple example of an AWS Lambda function that accepts an 'ExtractRefreshFailed' webhook event, queries additional information from Tableau Server and sends a custom email to the selected recipients

##### Configuration
1. Open **email_alerter > constants.py**
2. Update the follwing values with your own:
    ```
    EMAIL_FROM = "YOUR_FROM_ADDRESS"
    CC_LIST = ["YOUR_CC_1", "YOUR_CC_2"]
   ```
3. This example uses a Gmail application secret: [Configure yours here](https://support.google.com/mail/answer/185833?hl=en)
4. Once your Gmail application secret is created, add it to line #2 in **email_alerter > gmail_secret.py**
5. The body of the generated email can be updated via **email_alerter > email_body.py**

---
###### /event_logger

An AWS Lambda function that accepts multiple event types, queries additional information and writes records to an AWS RDS MySQL database. This data is then used by [frontend](https://github.com/kjmassey/vue-tableau-webhooks-ui) and [backend](https://github.com/kjmassey/django-tableau-webhooks) applications to create an 'Admin Portal' experience.

##### Configuration
1. Open **event_logger > constants.py**
2. Update the following values to your own:
   ```
    DB_HOST = "YOUR_DB_HOST"
    DB_PORT = "YOUR_DB_PORT"
    DB_SCHEMA = "YOUR_DB_SCHEMA"
    DB_USER = "YOUR_DB_USER"
    DB_PASSWORD = "YOUR_DB_PASSWORD"

    LAMBDA_URL = "YOUR_LAMBDA_URL"
   ```
3. This example uses MySQL
    - Changes can be made to **event_logger > db.py** as needed

---

### Additional Documentation

- [AWS Lambda](https://aws.amazon.com/lambda/)
- [AWS RDS for MySQL](https://aws.amazon.com/rds/mysql/)
- [Tableau Webhooks](https://help.tableau.com/current/developer/webhooks/en-us/)
- [Tableau REST API - Notification Methods](https://help.tableau.com/current/api/rest_api/en-us/REST/rest_api_ref_notifications.htm) (which includes Webhooks)
- [Tableau TSC Documentation](https://tableau.github.io/server-client-python/docs/api-ref)