from datetime import timedelta
from os import environ

import requests

__all__ = ["jira"]


def jira(args, milestones):
    def set_jira_due_date(issue_id, due_date):
        API_ENDPOINT = "https://jira.lsstcorp.org/rest/api/latest/"
        user, pw = environ["JIRA_USER"], environ["JIRA_PW"]
        formatted_date = due_date.strftime("%Y-%m-%d")
        data = {"fields": {"duedate": formatted_date}}
        print("Setting due date on", issue_id, "to", formatted_date)
        requests.put(API_ENDPOINT + "issue/" + issue_id, auth=(user, pw), json=data)

    for ms in milestones:
        if ms.jira and ms.due:
            set_jira_due_date(ms.jira, ms.due)
        elif ms.code.startswith("LDM-503"):
            if not ms.jira:
                print("WARNING: %s is not in Jira" % (ms.code,))
            if not ms.due:
                print("WARNING: %s has no due date" % (ms.code,))
        if ms.jira_testplan and ms.due:
            set_jira_due_date(ms.jira_testplan, ms.due - timedelta(days=45))
