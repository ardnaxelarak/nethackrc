## NetHack RC Files
nethackrc files using jinja templating

### Dependencies
This project is set up to be run through `uv` and `just`; you could probably manage your own python venv or use a system one, but do that at your own risk. [Just](https://github.com/casey/just) is just a command runner and so is not strictly necessary; you could call the python script directly.

#### Windows
```
winget install --id Casey.Just
winget install --id astral-sh.uv
```

#### MacOS
```
brew install just uv
```

#### Linux
Check your local package manager, or docs for [installing uv](https://docs.astral.sh/uv/getting-started/installation/) and [installing just](https://github.com/casey/just?tab=readme-ov-file#installation)

### .env
Copy `.env.example` to `.env`, and fill in values you wish to use:
- `HDF_USERNAME` and `HDF_PASSWORD` are your hardfought username and password if you wish to make use of automatic upload to US hardfought server
- `JNH_USERNAME` is your username for Junethack, which will be added as a comment at the top of your file

### Usage
Included are templates for 3.7, TNNT, and CrecelleHack; there are `just` tasks to render each of them (`just v37`, `just tnnt`, `just crecelle`) or automatically upload them to hardfought (`just upload_v37`, `just upload_tnnt`, `just upload_crecelle`).
You can also render a single file with `just render <filename>`.

At present, the following arguments are supported to rendering:
- `--nudist` will set the `nudist` option in the rcfile
- `--pauper` will set the `pauper` option (v3.7 and derivatives only)
- `--nobones` will disable the `bones` option
- `--nopet` will remove your starting pet (if going for petless conduct)
- `--hide-comments` will remove the explanatory comments from the rendered file (useful if you want the filesize to be smaller for some reason)
- `--curses` or `--tty` will set the `window_type` option to their corresponding values
