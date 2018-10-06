import subprocess, sys

global s3_bucket
global s3_uploads
global txt_location
global working_dir

s3_bucket = "s3://csuneat-project-2/"
s3_uploads = s3_bucket+"Uploads/"
txt_location = s3_bucket+"ProductionSite.txt"
working_dir = subprocess.check_output(["pwd"]).replace("\n","")

def fetchTxt(type):

    try:
        s3_current_production = subprocess.check_output(["cat","ProductionSite.txt"])
    except:
        subprocess.call(["touch","ProductionSite.txt"])
        s3_current_production = ""

    if type =="production":
        subprocess.call(["aws","s3","cp",txt_location,working_dir+"/ProductionSiteNew.txt"])
        s3_new_production = subprocess.check_output(["cat","ProductionSiteNew.txt"])
        subprocess.call(["mv","ProductionSiteNew.txt","ProductionSite.txt"])

        if s3_new_production == s3_current_production:
            return
        else:
            getSite(s3_new_production)

    else:
        newestSite = getLatestSiteTar()

        if newestSite == s3_current_production.replace("\n",""):
            return
        else:
            txt_file = open("ProductionSite.txt", 'w')
            txt_file.write(newestSite+"\n")
            txt_file.close()
            getSite("Staging")

def getSite(site_type):

    print("Downloading Site.")

    if site_type == "Staging":
        new_site = getLatestSiteTar()
        subprocess.check_output(["aws","s3","cp",s3_uploads+new_site, "site.tar.gz"])
        replaceTar("Staging")
    else:
        formatted_sitename = site_type.replace("\n","")
        subprocess.check_output(["aws","s3","cp",s3_uploads+formatted_sitename, "site.tar.gz"])
        replaceTar("Production")


def getLatestSiteTar():
    uploads = subprocess.check_output(["aws","s3","ls",s3_uploads,"--recursive"])
    upload_list = uploads.split("\n")
    latest = max(upload_list).split("/")
    return(latest[-1])

def replaceTar(site_type):
    print("Replacing site with new version.")

    directory = subprocess.check_output(["pwd"]).replace("\n","")
    subprocess.call(["tar","-xvzf","site.tar.gz"])

    if site_type == "Staging":
        subprocess.call("rm -rf /var/www/staging", shell=True)
        subprocess.call("mkdir /var/www/staging", shell=True)
        subprocess.call("mv "+directory+"/public/* /var/www/staging", shell=True)
    else:
        subprocess.call("rm -rf /var/www/html", shell=True)
        subprocess.call("mkdir /var/www/html", shell=True)
        subprocess.call("mv "+directory+"/public/* /var/www/html", shell=True)
        
    subprocess.call("service apache2 restart", shell=True)

def main(type):
    print("Fetching from S3.")
    fetchTxt(type)

main(str(sys.argv[1]))
