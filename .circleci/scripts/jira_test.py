import os
from pathlib import Path
from dotenv import load_dotenv
from jira import JIRA
from github import Github


env_path        = Path('.circleci\scripts\jira_test.env')
load_dotenv(env_path)
# load  api authenication data
jira_user       = os.getenv('jira_user')
jira_apikey     = os.getenv('jira_apikey')
jira_server_URL = os.getenv('jira_server_URL')
github_Token    = os.getenv('github_Token')
github_project  = os.getenv('github_project')

# pip install PyGithub
# pip install jira
# pip install python-dotenv

##########################################################
def set_environment_fields(monitor_json):
  env = os.sys.argv[3]

  # START - common errors 
  if(len(env.split()) > 1):
    print("ERROR: ENV needs to be one word, ideally kebab-case")
    raise SystemError

  # END - common errors
  monitor_json['tags'] = monitor_json.get('tags', [])

  monitor_json['name'] = monitor_json['name'].format(ENV = env)
  monitor_json['tags'].append(f"env:sema4-lis-{env.lower()}")
  monitor_json['tags'].append("team:echo")
  monitor_json['message'] = monitor_json['message'].format(ENV = env.lower())

  monitor_json['query'] = monitor_json['query'].format(ENV = env.lower())
##########################################################



def github_PRs(gitToken, gitproject):
    g       = Github( gitToken)
    repo    = g.get_repo(gitproject)
    issues  = repo.get_issues(state="closed")
    return issues

def jira_change_status(jira_user,jira_api_token,jira_server_URL, git_token, git_project):
    if jira_api_token is None:
        exit(1)
    
    options = {
    'server': jira_server_URL
    }

    jira = JIRA(options, basic_auth=(jira_user,jira_api_token) )
    # query uses JQL
    #jira_issues     = jira.search_issues('project = "L Plus Workbench" AND status IN ("PEER REVIEW") ORDER BY issuekey')
    jira_issues    = jira.search_issues('project = "testingTeam" AND status IN ("PEER REVIEW") ORDER BY issuekey')
    github_issues  = github_PRs(git_token, git_project)
    
    # loop through issues in Jira comparing them to Issues in Github
    for jira_issue in jira_issues:
        #print(str(jira_issue).upper())
        for git_issue in github_issues:
            if str(jira_issue).upper() in git_issue.title.upper():
                print('found')
                # moving "PEER REVIEW" to "DEVQA"
                jira.transition_issue(jira_issue, transition='DEVQA')
                jira.add_comment(jira_issue, 'CircleCI Sevice: Changing Status to "DEVQA"')
                exit()

jira_change_status(jira_user, jira_apikey, jira_server_URL, github_Token, github_project)