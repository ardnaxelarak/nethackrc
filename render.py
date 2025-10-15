import argparse
from dotenv import load_dotenv
from jinja2 import Environment, FileSystemLoader
from pyquery import PyQuery as pq
import os
import requests
import sys

def render(filename, options={}):
    env = Environment(loader=FileSystemLoader("."), trim_blocks=True, lstrip_blocks=True)
    env.globals['ord'] = ord
    template = env.get_template(filename)
    return template.render(options)

def upload(rcfile, variant):
    s = requests.Session()
    base_url = f"https://www.hardfought.org/nh/{variant}"

    hdf_username = os.getenv("HDF_USERNAME")
    hdf_password = os.getenv("HDF_PASSWORD")
    if hdf_username is None or hdf_password is None or len(hdf_username) == 0 or len(hdf_password) == 0:
        print("To upload config to hardfought you must specify HDF_USERNAME and HDF_PASSWORD in .env")
        return False

    login = s.post(f"{base_url}/login.php", {
        "username": hdf_username,
        "password": hdf_password,
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
    load_dotenv()

    parser = argparse.ArgumentParser()
    parser.add_argument("template", help="template file to render")
    parser.add_argument("--hdf_variant", help="if specified, the variant to upload the rendered template to on hardfought.org")
    parser.add_argument("--nudist", "-n", action="store_true", help="enable nudist conduct in rcfile")
    parser.add_argument("--pauper", "-p", action="store_true", help="enable pauper conduct in rcfile")
    parser.add_argument("--nobones", action="store_true", help="turn off bones in rcfile")
    parser.add_argument("--nopet", action="store_true", help="turn off starting pet in rcfile")
    parser.add_argument("--hide-comments", action="store_false", dest="comments", help="strip out explanatory comments in output to reduce file size")
    parser.add_argument("--curses", action="store_const", const="curses", dest="windowtype", help="set windowtype to curses and set appropriate options")
    parser.add_argument("--tty", action="store_const", const="tty", dest="windowtype", help="set windowtype to tty and set appropriate options")

    args = parser.parse_args()

    render_params = vars(args).copy()
    jnh = os.getenv("JNH_USERNAME")
    if jnh is not None and len(jnh) > 0:
        render_params['jnh_username'] = jnh

    rcfile = render(args.template, render_params)

    if args.hdf_variant:
        if (upload(rcfile, args.hdf_variant)):
            print(f"Uploaded template {args.template} to hardfought variant {args.hdf_variant}")
    else:
        print(rcfile)
