import requests
import re


if __name__ == "__main__":

    # Replace the author name with your GitHub username
    url = "https://api.github.com/search/issues?q=is:pr+author:ParthJohri+is:merged"

    r = requests.get(url)
    if r.status_code == 200:
        pr_data = r.json()
        pr_list = []
        emoji = ["🥳","🎉","🎊","🥂","🙌🏼"]
        count = 0;
        total_merged_prs = pr_data['total_count']
        total_merged_prs_content = f"""  <span><img src="https://img.shields.io/badge/Total_Merged_PRs-{total_merged_prs}-1877F2?style=for-the-badge"></span>"""
        
        for item in pr_data['items']:
            
         emoticon = emoji[round(count%5)]
         pull_request_url = item['html_url']
         new_repo_url = re.sub(r'/pull/\d+', '', pull_request_url)
         serial_number = count + 1
         
         pr_list.append(f"{serial_number}. {emoticon} Merged PR [{item['number']}]({pull_request_url}) - [{item['repository_url'][29:]}]({new_repo_url})")
         count=count+1
         
         # Provide the number of PRs you want to show in the README
         if(count==5): break
         
        pr_content = "\n".join(pr_list)
        
        # Read and Write the New ReadMe Content
        with open("README.md", "r") as f:
            readme_content = f.read()
            
        new_readme_content = re.sub(
        r'(\<!--Start Count Merged PRs-->\n)(.*?)(\<!--Finish Count Merged PRs-->\n)|(\<!--Start Merged PRs-->\n)(.*?)(\<!--Finish Merged PRs-->\n)',
        lambda m: (
            f'{m.group(1)}{total_merged_prs_content}\n{m.group(3)}' if m.group(1) else
            f'{m.group(4)}{pr_content}\n{m.group(6)}'
        ),
        readme_content,
        flags=re.DOTALL
         )


        with open("README.md", "w") as f:
            f.write(new_readme_content)

