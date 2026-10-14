# Modelbox
Modelbox is a security test suite for AI models built on top of Docker sandboxes.

## What you'll need to run this
* Virtualization enabled on your machine
* Python installed
* [Docker Sandboxes](https://github.com/docker/sbx-releases) installed

## Setting Up Docker Sandboxes
1. Make sure you're logged in using `sbx login`
2. Set the URL of your OpenAI compatible API inside the .env file (see .env.example)
3. Execute setup_sbx.sh
4. cd into sandbox and run `sbx create --name test-sandbox shell .`
5. Try running `sbx exec test-sandbox sh -c 'echo out; echo err >&2; exit 3' 2>/dev/null`
   * On your first sbx exec, make sure you choose **Locked Down** for network access
   * **ONLY** run the sandbox inside of the *sandbox* directory
   * You should see `out` as the output

## Setting up the python environment
1. Setup a venv and activate it
      ```bash
      python3 -m venv .venv
      source .venv/bin/activate        # bash/zsh
      source .venv/bin/activate.fish   # fish
      ```
2. Install dependencies `pip install -r requirements.txt`

## Running tests
`pytest -q tests`

## Want to add a test?
Feel free to make a PR with your test inside of /tests
