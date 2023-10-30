import tableauserverclient as TSC
from tsc_webhooks.tsc_constants import (
    TSC_SERVER_URL,
    TSC_SITE_NAME,
    BASE_DS_SEARCH_URL,
    PAT_NAME,
    PAT_SECRET,
)


def get_server_and_auth() -> tuple:
    """
    Return a tuple containing a TSC.Server and a TSC.PersonalAccessTokenAuth item

    (Avoids repetition of code)
    """

    server = TSC.Server(TSC_SERVER_URL, use_server_version=True)
    tab_auth = TSC.PersonalAccessTokenAuth(PAT_NAME, PAT_SECRET, site_id=TSC_SITE_NAME)

    return server, tab_auth


def get_site_name_from_id(
    server: TSC.Server, auth: TSC.PersonalAccessTokenAuth, site_luid: str
) -> str:
    """
    Query a site by LUID and return its name (since webhook event only includes site LUID)
    """

    with server.auth.sign_in(auth):
        site = server.sites.get_by_id(site_luid)

        return site._name


def get_tsc_owner_by_id(
    server: TSC.Server, auth: TSC.PersonalAccessTokenAuth, owner_id: str
) -> TSC.UserItem:
    """
    Query the content owner by LUID, return a UserItem
    """

    with server.auth.sign_in(auth):
        user = server.users.get_by_id(owner_id)

        return user


def construct_datasource_url(resp: dict) -> str:
    """
    DatasourceItems returned by TSC do not have 'webpage_url' populated. Return a formatted search string for hyperlinks
    """

    new_url = resp["webpage_url"]

    if resp["webpage_url"] is None:
        base_url = BASE_DS_SEARCH_URL
        obj_name = resp["resource_name"]

        new_url = base_url + obj_name

    return new_url


def get_item_details(
    server: TSC.Server, auth: TSC.PersonalAccessTokenAuth, resp: dict
) -> dict:
    """
    Query additional information about the impacted webhook item*

    * called by get_additional_event_details
    """

    with server.auth.sign_in(auth):
        tsc_obj = None

        match resp.get("resource").upper():
            case "WORKBOOK":
                tsc_obj = server.workbooks.get_by_id(resp.get("resource_luid"))

            case "DATASOURCE":
                tsc_obj = server.datasources.get_by_id(resp.get("resource_luid"))

            case "EXTRACTS":
                if "workbook" in resp.get("event_type").lower():
                    tsc_obj = server.workbooks.get_by_id(resp.get("resource_luid"))

                if "datasource" in resp.get("event_type").lower():
                    tsc_obj = server.datasources.get_by_id(resp.get("resource_luid"))

            case "USER":
                tsc_obj = server.users.get_by_id(resp.get("resource_luid"))

        if not tsc_obj:
            raise ValueError("Value for 'resource' is not valid")

        if resp.get("resource") in ["WORKBOOK", "DATASOURCE", "EXTRACTS"]:
            resp["webpage_url"] = tsc_obj._webpage_url
            resp["project_luid"] = tsc_obj._project_id
            resp["project_name"] = tsc_obj._project_name
            resp["owner_luid"] = tsc_obj.owner_id

        if resp.get("resource") == "USER":
            resp["resource_name"] = tsc_obj.fullname
            resp["owner_email"] = tsc_obj.email

        return resp


def get_additional_event_details(resp: dict) -> dict:
    """
    Augment the webhook event body with additional information from Tableau
    """

    server, tab_auth = get_server_and_auth()
    augmented_resp = resp

    if "Deleted" not in resp["event_type"]:
        augmented_resp = get_item_details(server, tab_auth, resp)

        if resp["resource"] == "EXTRACTS":
            augmented_resp["owner_luid"] = resp["owner_luid"]

        if resp["resource"] not in ["USER"]:
            tsc_owner = get_tsc_owner_by_id(
                server, tab_auth, augmented_resp["owner_luid"]
            )

            augmented_resp["owner_name"] = tsc_owner.fullname
            augmented_resp["owner_email"] = tsc_owner.email
            augmented_resp["owner_site_role"] = tsc_owner._site_role

    augmented_resp["text"] = augmented_resp["text"].replace("'", "")
    augmented_resp["created_at"] = augmented_resp["created_at"].split("Z")[0]
    augmented_resp["site_name"] = get_site_name_from_id(
        server, tab_auth, resp.get("site_luid")
    )

    augmented_resp["webpage_url"] = construct_datasource_url(augmented_resp)

    return augmented_resp
