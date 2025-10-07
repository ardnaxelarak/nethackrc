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

    s.post(f"{base_url}/login.php", {
        "username": os.getenv("HDF_USERNAME"),
        "password": os.getenv("HDF_PASSWORD"),
        "submit": "Login",
    })

    get_page = s.get(f"{base_url}/rcedit.php")
    csrf_token = pq(get_page.content)('input[name="csrf_token"]').attr("value")

    s.post(f"{base_url}/rcedit.php", {
        "csrf_token": csrf_token,
        "rctext": rcfile,
        "submit": "Save+RC+File",
    })

    print(f"Uploaded variant {variant}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("template")
    parser.add_argument("-v", "--variant")
    parser.add_argument("--nudist", "-n", action="store_true")
    parser.add_argument("--pauper", "-p", action="store_true")
    parser.add_argument("--nobones", action="store_true")
    parser.add_argument("--nopet", action="store_true")

    args = parser.parse_args()

    rcfile = render(args.template, vars(args))

    if args.variant:
        upload(rcfile, args.variant)
    else:
        print(rcfile)
