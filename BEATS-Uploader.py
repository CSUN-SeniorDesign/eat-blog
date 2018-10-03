import subprocess

print("""
______            _         _   _       _                 _
| ___ \          | |       | | | |     | |               | |
| |_/ / ___  __ _| |_ ___  | | | |_ __ | | ___   __ _  __| | ___ _ __
| ___ \/ _ \/ _` | __/ __| | | | | '_ \| |/ _ \ / _` |/ _` |/ _ \ '__|
| |_/ /  __/ (_| | |_\__ \ | |_| | |_) | | (_) | (_| | (_| |  __/ |
\____/ \___|\__,_|\__|___/  \___/| .__/|_|\___/ \__,_|\__,_|\___|_|
                                 | |
                                 |_|
""")

'''
Program Startup.
Informs user that Git is required.
'''
def programStartup():
    print("This program requires git.")
    print("This program only works on Linux distrbutions, with bash installed.")
    value = raw_input("Is git installed on your system? Y/N: ")
    return str(value)

'''
Main Method
Primary output for the program.
Will only run if a user says they have git installed, to save them time.
'''
def mainMethod():
    if programStartup() == "Y":
        print("OK. Cloning from Eat-Blog.\n")
        print(doCloning())
        print("Cloning Successful. Getting current master-branch SHA.")
        print("Latest master-branch commit SHA : " + getHeadSHA())
        print("\nEnter 'Y' to use this commit SHA.")
        inputSha = raw_input("Otherwise, enter the SHA of the commit you want to appear on the production site. (Note - This won't be tested for authenticity.) ")
        updateProductionSiteTXT(inputSha)
        print("\nSuccessfully updated SHA.")
        print("\nCreating new git branch, adding, and committing.")
        doGIT()
        print("\n\nScript complete. Visit your GitHub account to verify and create a pull request.")
        print("You may now safely delete the eat-blog directory.")
'''
Do Cloning
Clones the eat-blog directory from github.
If there is an error, it will inform the user.
'''
def doCloning():
    try:
        return subprocess.check_output(["git", "clone", "https://github.com/CSUN-SeniorDesign/eat-blog.git"])
    except:
        print("Cloning Failed. Try installing git or removing eat-blog directory if it already exists.")
        exit()

'''
Get Current Dir
Gets the script's working directory, replaces the trailing \n with a blank.
'''
def getCurrentDir():
    local_directory = subprocess.check_output(["pwd"])
    return local_directory.replace("\n","")

'''
Get Head SHA
Gets the current commit's SHA using rev-parse.
'''
def getHeadSHA():
    try:
        cleaned_directory = getCurrentDir()
        subprocess_directory_input = "--git-dir="+cleaned_directory+"/eat-blog/.git"
        raw_sha = subprocess.check_output(["git", subprocess_directory_input, "rev-parse", "HEAD"])
        return raw_sha.replace("\n","")
    except:
        print("Something went wrong. Ensure eat-blog repo was properly created.")
        exit()

'''
Update Production Site txt
This will update the productionsite.txt file with the user-submitted SHA.
'''
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

'''
Do Git
This method will create a new branch, checkout the branch, add the new txt file, commit, then push to github.
'''
def doGIT():
        cleaned_directory = getCurrentDir()
        txt_location = cleaned_directory+"/eat-blog/ProductionSite.txt"
        git_location = "--git-dir="+cleaned_directory+"/eat-blog/.git"

        try:
            #Branching, checking out, adding the new file, committing, then pushing.
            subprocess.call(["git", git_location, "branch", "Script-Update-ProductionSite" ])
            subprocess.call(["git", git_location, "checkout", "Script-Update-ProductionSite" ])
            subprocess.call(["git", git_location, "add", txt_location ])
            subprocess.call(["git", git_location, "commit", "-m", "\"BEATS Uploader - Update ProductionSite.txt\"" ])
            print("\n\n\nEnter your GitHub username and password. \nNote this script doesn't see what you type.")
            print("Alternatively, CTRL+C to exit, then run git push on your own in the eat-blog directory.\n")
            subprocess.call(["git", git_location, "push", "origin", "Script-Update-ProductionSite"])
        except:
            print("\n\nError pushing to GitHub. Ensure the previous \"Script-Update-ProductionSite\" branch was deleted if this script was used before.")

mainMethod()
