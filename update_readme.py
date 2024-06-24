import os
from github import Github
import requests
from datetime import datetime

def fetch_contributions(username):
    query = f"""
    query {{
      user(login: "{username}") {{
        contributionsCollection {{
          contributionCalendar {{
            totalContributions
          }}
          commitContributionsByRepository(maxRepositories: 5) {{
            repository {{
              name
              url
            }}
            contributions(first: 5) {{
              nodes {{
                occurredAt
                commitCount
                repository {{
                  name
                  url
                }}
              }}
            }}
          }}
        }}
      }}
    }}
    """
    
    headers = {"Authorization": f"Bearer {os.getenv('GH_TOKEN')}"}
    request = requests.post('https://api.github.com/graphql', json={'query': query}, headers=headers)
    if request.status_code == 200:
        return request.json()
    else:
        raise Exception(f"Query failed to run by returning code of {request.status_code}. {query}")

def update_readme(contributions):
    readme_path = 'README.md'
    with open(readme_path, 'r') as file:
        content = file.readlines()

    new_content = []
    in_contribution_section = False

    for line in content:
        if line.strip() == '<!-- START_CONTRIBUTIONS -->':
            in_contribution_section = True
            new_content.append(line)
            new_content.append(f"\nLast updated: {datetime.utcnow().isoformat()}Z\n")
            new_content.append("\n### My Recent Contributions\n")
            for repo in contributions['data']['user']['contributionsCollection']['commitContributionsByRepository']:
                repo_name = repo['repository']['name']
                repo_url = repo['repository']['url']
                new_content.append(f"- [{repo_name}]({repo_url})\n")
            continue

        if line.strip() == '<!-- END_CONTRIBUTIONS -->':
            in_contribution_section = False

        if not in_contribution_section:
            new_content.append(line)

    with open(readme_path, 'w') as file:
        file.writelines(new_content)

if __name__ == "__main__":
    username = os.getenv('GITHUB_REPOSITORY_OWNER')
    contributions = fetch_contributions(ParthJohri)
    update_readme(contributions)
