import tableauserverclient as TSC
from tsc_webhooks.tsc_constants import (
    PAT_NAME,
    PAT_SECRET,
    TSC_SERVER_URL,
    TSC_SITE_NAME,
)
from event_logger.constants import LAMBDA_URL


def get_server_and_auth() -> tuple:
    """
    Return a tuple containing a TSC.Server and a TSC.PersonalAccessTokenAuth item

    (Avoids repetition of code)
    """

    server = TSC.Server(TSC_SERVER_URL, use_server_version=True)
    tab_auth = TSC.PersonalAccessTokenAuth(PAT_NAME, PAT_SECRET, site_id=TSC_SITE_NAME)

    return server, tab_auth


def get_all_webhooks() -> list:
    """
    Return a list of the dicts of each WebhookItem on the site
    """

    server, tab_auth = get_server_and_auth()

    with server.auth.sign_in(tab_auth):
        hooks = list(TSC.Pager(server.webhooks))

        return [hook.__dict__ for hook in hooks]


def get_webhook_by_id(luid: str) -> dict:
    """
    Query a webhook by LUID, returns a dict of the WebhookItem
    """

    server, tab_auth = get_server_and_auth()

    with server.auth.sign_in(tab_auth):
        hook = server.webhooks.get_by_id(luid)

        return hook.__dict__


def create_webhook(webhook_name: str, source_name: str) -> dict:
    """
    Create a new webhook, return the dict of the WebhookItem's details
    """
    server, tab_auth = get_server_and_auth()

    with server.auth.sign_in(tab_auth):
        new_webhook = TSC.WebhookItem()
        new_webhook.name = webhook_name
        new_webhook.url = LAMBDA_URL
        new_webhook.event = source_name

        new_webhook = server.webhooks.create(new_webhook)

        return new_webhook.__dict__


def delete_webhook(luid: str) -> str:
    """
    Delete a webhook using its LUID
    """

    server, tab_auth = get_server_and_auth()

    with server.auth.sign_in(tab_auth):
        server.webhooks.delete(luid)

        return f"Deleted webhook - id: {luid}"
