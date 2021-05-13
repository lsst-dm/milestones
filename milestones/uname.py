import keyring


def get_login_cli(service="jira_rest", username=None, prompt=False):
    """
    Get the password for the username out of the keyring.  If the password
    isn't found in the keyring, ask for it from the command line.
    :tuple: username, passwd
    """

    if username is None or prompt:
        username = input('Jira Username: ')

    passwd = keyring.get_password(service, username)
    if passwd is None or prompt:
        passwd = input('Enter Password: ')
        set_password(service,username, passwd)

    return (username, passwd)


def set_password(service, username, passwd):
    """
    Writes the password to the keyring.
    """

    keyring.set_password(service, username, passwd)

