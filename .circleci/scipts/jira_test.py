import os
from pathlib import Path
from dotenv import load_dotenv
from jira import JIRA
from github import Github


dotenv_path = Path('var.env')
load_dotenv(dotenv_path)

jira_user = os.getenv('jira_user')
jira_apikey = os.getenv('jira_apikey')
jira_server_URL = os.getenv('jira_server_URL')
github_Token = os.getenv('github_Token')
github_project = os.getenv('github_project')

print(jira_user, jira_apikey, jira_server_URL,  github_Token, github_project)

# pip install PyGithub
# pip install jira
# pip install python-dotenv

def github_PRs(gitToken, gitproject):
    g = Github( gitToken) 
    repo = g.get_repo(gitproject)
    issues = repo.get_issues(state="open")
    return issues

def jira_change_status(jira_user,jira_api_token,jira_server_URL, git_token, git_project):
    options = {
    'server': jira_server_URL
    }

    jira = JIRA(options, basic_auth=(jira_user,jira_api_token) )
    # query uses JQL
    jira_issues    = jira.search_issues('project = "testingTeam" AND status IN ("PEER REVIEW") ORDER BY issuekey')
    github_issues  = github_PRs(git_token, git_project)
    
    # moving "PEER REVIEW" to "DEVQA"
    for jira_issue in jira_issues:
        print(str(jira_issue).upper())
        for git_issue in github_issues:
            print(git_issue.title.upper())
            if str(jira_issue).upper() in git_issue.title.upper():
                print('found')
                jira.transition_issue(jira_issue, transition='DEVQA')
                jira.add_comment(jira_issue, 'CircleCI Sevice: Changing Status to "DEVQA"')

jira_change_status(jira_user, jira_apikey, jira_server_URL,  github_Token, github_project)