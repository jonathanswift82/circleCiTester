from jira import JIRA
from github import Github

# pip install PyGithub
# pip install jira

userTest = "jonathanswift82@gmail.com"
userProd = "jon.swift-external@sema4.com"
apikeyTest = '2R4hrboo5BTJtN1uAvc9B081'
apikeyProd = 'bkdbgTDafKACGh2svDnqEB20'
server_jira_URL_Test = 'https://jiracircleciintegration.atlassian.net'
serverProd = 'https://sema4genomics.atlassian.net'
githubPersonalToken = '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'
github_jonathanswift82_Token = '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'
github_jonathanswift82_project = 'jonathanswift82/circleCiTester'


# https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token

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
    github_issues   = github_PRs(git_token, git_project)
    
    # moving "PEER REVIEW" to "DEVQA"
    for jira_issue in jira_issues:  
        print(jira_issue)
        for git_issue in github_issues:
            print(git_issue.title)
            if str(jira_issue) in git_issue.title:
                print('found: ')
                jira.transition_issue(jira_issue, transition='DEVQA')
                jira.add_comment(jira_issue, 'CircleCI Sevice: Changing Status to "DEVQA"')

jira_change_status(userTest, apikeyTest, server_jira_URL_Test,github_jonathanswift82_Token,github_jonathanswift82_project)





##########################################################################################################################################
def github_PRs_backup():
    print('github_PRs')
    #g = Github( login_or_token=githubPersonalToken) 
    g = Github( githubPersonalToken) 
    repo = g.get_repo('sema4genomics/s4-workbench-etl')
    issues = repo.get_issues(state="open")
    #prs = repo.get_pulls('all')

    count = 0
    #for pr in prs:
    for pr in issues:
        #if(pr.is_merged):
        #print(pr)
        count = count + 1
    print('Count: ', count)

    return issues

def jira_change_status_backup(user,apikey,serverURL):
    options = {
    'server': serverURL
    }

    jira = JIRA(options, basic_auth=(user,apikey) )
    
    #issue = jira.issue('LPWB-5679')
    #jira.add_comment(issue, 'CircleCI Sevice: Changing Status to "DEVQA"')

    #jira_issues = jira.search_issues('project = "L Plus Workbench" AND status IN ("DEVQA") ORDER BY issuekey')
    jira_issues     = jira.search_issues('project = "circleCiTester" AND status IN ("PEER REVIEW") ORDER BY issuekey')
    github_issues   = github_PRs()
    #print(issues)
    # moving "PEER REVIEW" to "DEVQA"
    for jira_issue in jira_issues:
        print(jira_issue)
        #jira.transition_issue(issue, transition='DEVQA')
        #jira.add_comment(issue, 'CircleCI Sevice: Changing Status to "DEVQA"')
##########################################################################################################################################
