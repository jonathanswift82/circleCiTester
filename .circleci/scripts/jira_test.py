from pickle import FALSE, TRUE
import sys
from jira import JIRA
from github import Github

def github_PRs(gitToken, gitproject):
    g       = Github( gitToken)
    repo    = g.get_repo(gitproject)
    issues  = repo.get_issues(state="closed")
    return issues

def jira_change_status(jira_user,jira_api_token, jira_project_name, jira_server_URL, git_token, git_project):
    if jira_api_token is None or jira_project_name  is None or jira_user is None or jira_server_URL is None or git_token is None or git_project is None:
        exit(13)
    
    options = {
    'server': jira_server_URL
    }

    jira = JIRA(options, basic_auth=(jira_user,jira_api_token) )
    #query uses JQL
    jira_issues    = jira.search_issues('project = \"'+jira_project_name+'\" AND status IN (\'PEER REVIEW\') ORDER BY issuekey') 
    github_issues  = github_PRs(git_token, git_project)
    
    # loop through issues in Jira comparing them to Issues in Github
    found = FALSE
    for jira_issue in jira_issues:
        print('jira: ',str(jira_issue).upper())
        for git_issue in github_issues:
            if str(jira_issue).upper() in git_issue.title.upper():
                print('found match: ' + str(jira_issue).upper())
                found = TRUE
                # moving "PEER REVIEW" to "DEVQA"
                jira.transition_issue(jira_issue, transition='DEVQA')
                jira.add_comment(jira_issue, 'CircleCI Sevice: Changing Status to "DEVQA". PR :'+git_issue.title.upper())


if __name__ == "__main__":
    args = sys.argv
    if(len(args) != 7):
        exit(12)
    for arg in args:
        print(arg)
    jira_change_status(args[1], args[2], args[3], args[4], args[5], args[6])