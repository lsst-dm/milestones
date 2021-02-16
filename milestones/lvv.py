import requests
from marshmallow import Schema, fields, pre_load, EXCLUDE

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
    jira_url = fields.String()

    @pre_load(pass_many=True)
    def extract_fields(self, data, **kwargs):
        """Extract the needed fields"""

        out_data = dict()
        out_data["key"] = str(data["key"]).strip()
        data_fields = data["fields"]
        out_data["summary"] = data_fields["summary"]
        out_data["jira_url"] = ISSUE_UI_URL.format(issue=data["key"])

        out_data["req_priority"] = "None"
        if data_fields["priority"]:
            out_data["req_priority"] = data_fields["priority"]["name"]

        return out_data


if __name__ == "__main__":
    key = "LVV-8"
    print("Reading jira VE:  " + key)
    rs = requests.Session()

    # Get VE details for a requirement
    jve_res = rs.get(ISSUE_URL.format(issue=key)).json()
    ve_details = VerificationE(unknown=EXCLUDE).load(jve_res)

    print("key:: " + ve_details["key"])
    print("summary:: " + ve_details["summary"].strip())
    print("req priority:: " + ve_details["req_priority"])
    print("req URL:: " + ve_details["jira_url"])
    print("End")
