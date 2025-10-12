import argparse
from dotenv import load_dotenv
from jinja2 import Environment, FileSystemLoader
from pyquery import PyQuery as pq
import os
import requests
import sys

def render(filename, options={}):
    env = Environment(loader=FileSystemLoader("."), trim_blocks=True, lstrip_blocks=True)
    template = env.get_template(filename)
    return template.render(options)

def upload(rcfile, variant):
    load_dotenv()

    s = requests.Session()
    base_url = f"https://www.hardfought.org/nh/{variant}"

    login = s.post(f"{base_url}/login.php", {
        "username": os.getenv("HDF_USERNAME"),
        "password": os.getenv("HDF_PASSWORD"),
        "submit": "Login",
    })

    error = pq(login.content)('.error').text()
    if (len(error) > 0):
        print(f"[{variant}] Error logging in: {error}")
        return False

    get_page = s.get(f"{base_url}/rcedit.php")
    csrf_token = pq(get_page.content)('input[name="csrf_token"]').attr("value")

    if (csrf_token == None or len(csrf_token) == 0):
        print(f"[{variant}] Could not obtain csrf token")
        return False

    post =s.post(f"{base_url}/rcedit.php", {
        "csrf_token": csrf_token,
        "rctext": rcfile,
        "submit": "Save+RC+File",
    })
    error = pq(post.content)('.error').text()
    if (len(error) > 0):
        print(f"[{variant}] Error updating RC file: {error}")
        return False

    return True

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("template")
    parser.add_argument("-v", "--variant", help="If specified, the variant to upload the rendered template to on hardfought.org")
    parser.add_argument("--nudist", "-n", action="store_true")
    parser.add_argument("--pauper", "-p", action="store_true")
    parser.add_argument("--nobones", action="store_true")
    parser.add_argument("--nopet", action="store_true")

    args = parser.parse_args()

    rcfile = render(args.template, vars(args))

    if args.variant:
        if (upload(rcfile, args.variant)):
            print(f"Uploaded template {args.template} to variant {args.variant}")
    else:
        print(rcfile)
