## Instructions

1. Create a new [Github token (classic)](https://github.com/settings/tokens/new) with the `repo` permissions
    
    - Technically, it's possible to use the script without a token but [rate limits](https://docs.github.com/en/rest/overview/resources-in-the-rest-api?apiVersion=2022-11-28#rate-limiting) apply.
    - For security reasons, an expiration date for the token is a good idea (30 days, by default).

2. Save the token as an environment variable on your laptop called **GH_TOKEN**:

    1. On ZSH 
      - `$ echo 'export GH_TOKEN=<YOUR GH TOKEN>' >> ~/.zshenv`
      - `$ source ~/.zshenv` 
    
    2. On BASH 
      - `$ echo 'export GH_TOKEN=<YOUR GH TOKEN>' >>``~/.bash_profile`
      - `$ source ~/.bash_profile`

3. Install requirements

Not all the modules are required to run the script
  
  - install everything, especially unit tests stuff : `$ pip install -r requirements.txt` 
  - only want to run the script: `$ pip install requests`

4. Run the script
The query is the same you would use in the Github website. The only difference is that you have to add also the `repo:owner/repo` at the end. You can then first try the query directly in Github and than copy-paste it in the CLI.

You can run the script by add the search query as argument: for example: 
  - `$ python3 main.py "is:pr is:closed merged:2023-01-25..2023-02-01 repo:silvanocostanzo/merge-time"`

5. Results
If you config is OK, **especially your GH_TOKEN**, a file ***prs.json*** will be created in the same folder.
