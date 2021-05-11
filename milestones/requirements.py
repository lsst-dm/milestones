import requests
from marshmallow import Schema, fields, pre_load, EXCLUDE

__all__ = ["extract_ve_details"]

JIRA_INSTANCE = "https://jira.lsstcorp.org"
ISSUE_UI_URL = f"{JIRA_INSTANCE}/browse/{{issue}}"
JIRA_API = f"{JIRA_INSTANCE}/rest/api/latest"
ISSUE_URL = f"{JIRA_API}/issue/{{issue}}"


class VerificationE(Schema):
    """ LSST Verification Element definition class

    Methods
    -------
    extract_fields(data)
        Extracts the few data fields needed from the full schema.

    """

    key = fields.String()
    summary = fields.String()
    req_id = fields.String()
    req_priority = fields.String()
    # req_milestone = fields.String(allow_none=True)
    jira_url = fields.String()

    @pre_load(pass_many=False)
    def extract_fields(self, data, **kwargs):
        """Extract the needed fields"""

        out_data = dict()
        out_data["key"] = str(data["key"])
        data_fields = data["fields"]
        out_data["summary"] = data_fields["summary"]
        out_data["jira_url"] = ISSUE_UI_URL.format(issue=data["key"])

        # out_data['req_milestone'] = None
        # if data_fields["labels"] is not None and len(data_fields["labels"]) > 0:
        #     out_data["req_milestone"] = data_fields["labels"][0]

        out_data["req_priority"] = None
        if data_fields["priority"]:
            out_data["req_priority"] = data_fields["priority"]["name"]

        return out_data


def extract_ve_details(lvv_key):
    """
    Extract the details from Jira for an LVV

    :return: Object with VE details
    """
    rs = requests.Session()
    jve_res = rs.get(ISSUE_URL.format(issue=lvv_key)).json()
    ve_details = VerificationE(unknown=EXCLUDE).load(jve_res)
    rs.close()
    return ve_details
