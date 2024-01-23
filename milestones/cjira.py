from datetime import timedelta
from os import environ

from jira import JIRA

from milestones.uname import get_login_cli

__all__ = ["cjira"]


def list_jira_issues(jira, pred2=None, query=None):
    """
    :JIRA jira: setup up JIRA object
    :String query: Query string "
    :String pred2: If you use the defualt query string but want to
                    add more predicate or sort order start with AND or OR
    """
    fields = ["key", "labels", "type", "assignee", "summary", "duedate"]
    if query is None:
        query = """project = DM AND resolution = Unresolved AND
                   (type = epic or type= story) """

    if pred2 is not None:
        query = f"{query} {pred2}"
    r = jira.search_issues(jql_str=query, fields=fields, maxResults=500)
    return r


def get_jira(username=None, prompt=False):
    """Setup up the JIRA object endpoint - prompt
        for username and passwd as needed.
        Password will be looked up from key chain.
    :String username: Optionally pass the username (prompted othereise)
    """
    user, pw = environ["JIRA_USER"], environ["JIRA_PW"]
    if not user or not pw:
        user, pw = get_login_cli(username=username, prompt=prompt)
    print("Jira user:" + user)
    ep = "https://jira.lsstcorp.org"
    return (user, pw, JIRA(server=ep, basic_auth=(user, pw)))


def set_jira_due_date(id, due_date, jira=None, issue=None):
    """
    Update the duedate of the issue in jira - add a comment also
    if jira is passed.

    :param ms: Milesonte ID
    :param due_date: date
    :param jira: optional JIRA object do not pass for no comments
    :issue issue: optiona issue - will look up on ms
    :return:
    """

    formatted_date = due_date.strftime("%Y-%m-%d")
    if issue is None:
        p2 = " and key = " + id
        issues = list_jira_issues(jira, pred2=p2)
        if issues:
            issue = issues[0]
        else:
            print(f" Issue {id} not returned - it may be marked done.")
            return
    issue_id: str = issue.key
    tdate = issue.fields.duedate
    if tdate != formatted_date:
        message = f"Setting due date on {issue_id} to {formatted_date} from P6"
        print(message)
        issue.update(duedate=formatted_date)
        jira.add_comment(issue_id, message)
    else:
        message = f"{issue_id}  date {tdate} ok!"
        print(message)


def cjira(args, milestones):
    my_jira = get_jira()[2]
    for ms in milestones:
        if ms.jira and ms.due:
            set_jira_due_date(ms.jira, ms.due, my_jira)
        elif ms.code.startswith("LDM-503"):
            if not ms.jira:
                print("WARNING: %s is not in Jira" % (ms.code,))
            if not ms.due:
                print("WARNING: %s has no due date" % (ms.code,))
        if ms.jira_testplan and ms.due:
            set_jira_due_date(ms.jira_testplan, ms.due - timedelta(days=45), my_jira)
