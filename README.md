# pizzapy-website

Codebase for Official PizzaPy Website

## Installation

### Prerequisites

- [Python 3.11^](https://www.python.org/downloads/)
- [virtualenv](https://virtualenv.pypa.io/en/latest/installation.html)

### Setup

Python dependencies:

```bash
python -m venv venv         # creates a Virtual Environment inside the /venv directory
./venv/Scripts/activate     # activates the venv, to exit, type "deactivate" || for MAC: source venv/bin/activate
pip install -r requirements.txt # installs all the Python dependencies
```

JavaScript dependencies:

```bash
cd PizzaPyWebApp/js_lib
npm install
```

### Environment Variables

1. You'll need two environment variables to be able to run the `manage.py runserver` command. If you're using VSCode, run these commands:

```bash
npx shx cp PizzaPyWebApp/.env.example PizzaPyWebApp/.env # copies .env.example to .env
code PizzaPyWebApp/.env # opens your editor for .env
```

- If you don't use VSCode, just edit the newly created `.env` file manually.

2. Next, you'll need to replace the `check-jira-references-column` values with the values found in Jira.

3. The next section should work without issues, otherwise ask the maintainers for help.

## Usage

> [!WARNING]
> Ensure you've set up the `.env` file with the proper values found in Jira before proceeding!

Once you've installed the dependencies, you can now run the application or build scripts.

```bash
cd PizzaPyWebApp/
python manage.py runserver
```

If you want to watch for TailwindCSS changes, run the following commands in **another terminal instance**:

```bash
cd PizzaPyWebApp/js_lib/
npm run watch
```

This will create a `/PizzaPyWebApp/static/css/output.css` stylesheet based on the `/PizzaPyWebApp/js_lib/input.css` file.

## Side Notes

```txt
Django setup
django-admin startproject project_name
python manage.py startapp app_name

Writes all python dependecies for tracking only (and deployment)
python -m pip freeze > requirements.txt

Installing of packages
pip install package_name

For production to collect static files
python manage.py collectstatic

Removing files from the repo and not locally

directory
git rm --cached -r venv
rm 'venv'

files
git rm --cached venv
rm 'venv'

do the git ignore and remove at the same the time
git rm --cached (git ls-files -i -c -X .gitignore)
rm 'venv'
rm '/PizzaPyWebApp/js_lib/node_modules'
```

### Dockerization

1. To build the container, Run `docker build -t pizzapy-website .`
2. To run the container, use `docker run -d -p 8000:8000 pizzapy-website`
3. Visit `http://localhost:8000` to view the site

develop test 
