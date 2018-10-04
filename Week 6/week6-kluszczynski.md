## Tyler's Blog. Week 6.
#### What's new this week?

##### Finishing Project 2.
For this project, I took on much more work than I expected. I was responsible for CircleCI, AWS IAM, ASG, Route 53 and an upload script, and a download script from S3. For this blog, I will go over some of the code I wrote for my upload script.

##### BEATS Uploader
The BEATS Uploader is a python script that can be ran on any linux distribution that has bash and git installed.

The first step is cloning from the eat-blog GitHub directory.
```
def doCloning():
    try:
        return subprocess.check_output(["git", "clone", "https://github.com/CSUN-SeniorDesign/eat-blog.git"])
    except:
        print("Cloning Failed. Try installing git or removing eat-blog directory if it already exists.")
    exit()
```

After, we get the eat-blog directory's most recent commit SHA:
```
def getHeadSHA():
    try:
        cleaned_directory = getCurrentDir()
        subprocess_directory_input = "--git-dir="+cleaned_directory+"/eat-blog/.git"
        raw_sha = subprocess.check_output(["git", subprocess_directory_input, "rev-parse", "HEAD"])
        return raw_sha.replace("\n","")
    except:
        print("Something went wrong. Ensure eat-blog repo was properly created.")
exit()
```

Next, the ProductionSite.txt is updated, which stores the SHA of the production version.

```
def updateProductionSiteTXT(sha):
    if sha == "Y":
        sha = getHeadSHA()

    formatted_sha = sha+".tar.gz"
    txt_file_dir = getCurrentDir() + "/eat-blog/ProductionSite.txt"

    try:
        #Opening txt file to edit, editing, then closing.
        txt_file = open(txt_file_dir, 'w')
        txt_file.write(formatted_sha+"\n")
        txt_file.close()
    except:
        print("Error writing to file. Assure you have permissions to write to /eat-blog/ProductionSite.txt")
        exit()
```

Some of these methods require the current directory, which is retrieved through the getCurrentDir() method:

```
def getCurrentDir():
    local_directory = subprocess.check_output(["pwd"])
    return local_directory.replace("\n","")
```

Finally, the script creates a new branch, adds the new ProductionSite.txt to it, then pushes the new branch to the eat-blog GitHub. :

```
def doGIT():
        cleaned_directory = getCurrentDir()
    
        try:
            #Branching, checking out, adding the new file, committing, then pushing.
            subprocess.call(["git","-C", "eat-blog", "branch", "Script-Update-ProductionSite" ])
            subprocess.call(["git","-C", "eat-blog", "checkout", "Script-Update-ProductionSite" ])
            subprocess.call(["git","-C", "eat-blog", "add", "ProductionSite.txt" ])
            subprocess.call(["git","-C", "eat-blog", "commit", "-m", "\"BEATS Uploader - Update ProductionSite.txt\"" ])
            print("\n\n\nEnter your GitHub username and password. \nNote this script doesn't see what you type.")
            print("Alternatively, CTRL+C to exit, then run git push on your own in the eat-blog directory.\n")
            subprocess.call(["git","-C", "eat-blog", "push", "origin", "Script-Update-ProductionSite"])
        except:
            print("\n\nError pushing to GitHub. Ensure the previous \"Script-Update-ProductionSite\" branch was deleted if this script was used before.")

```
Note that in the .py file, there are comments before the methods stating what their functions are.

##### After the .txt is updated
After the ProductionSite.txt file is updated, CircleCI will push it onto S3 with the following line:

```
aws s3 cp /home/circleci/project/ProductionSite.txt s3://csuneat-project-2/
```

Note that it is placed in a directory separate from the .tar.gz files that are uploaded.

Once the .txt file is uploaded onto s3, within 5 minutes a cronjob runs on our servers. This cronjob runs another python file that will fetch the ProductionSite.txt from s3, and compare it to the ProductionSite.txt it has stored (for the production site).

For the staging site, the script will fetch the latest .tar.gz that has been uploaded with CircleCI, then compare that to the current .tar.gz version, which is stored in its local Productionsite.txt. This means that there are two different ProductoinSite.txt files running on the same server, along with two cronjobs pointing to two copies of the same script.

It would have been possible to use only one copy of the script, but to save time two copies of the same script are ran in different directories.

If a site knows that it needs to update, it will fetch the .tar.gz it was told to fetch, then will unzip it using tar, remove the contents of the /var/www/staging or /var/www/html, place the contents of the unzipped public folder in the respective directory, restart apache, then reboot the server.


