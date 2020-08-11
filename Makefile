VIRTUALENV:=demo
VIRTUALENVDIR:=$(HOME)/.virtualenvs/$(VIRTUALENV)
PYTHON_VERSION:=$(shell cat runtime.txt | sed 's/python-//')
MYSHELL=$(shell dscl . -read /Users/$$USER UserShell | awk '{print $$2}')
SHELL_NAME=$(notdir $(MYSHELL))

ifeq ($(SHELL_NAME), zsh)
  PROFILE_FILE=.zprofile
  FUNCTION_SUFFIX=is a shell function
else
  PROFILE_FILE=.bash_profile
  FUNCTION_SUFFIX=is a function
endif

.PHONY: cert setup venv install clean test checkvirtualenvversion

cert: nginx/server.crt nginx/server.key

venv: $(VIRTUALENVDIR)

checkvirtualenvversion:
	@test "$(shell $(VIRTUALENVDIR)/bin/python --version)" = "Python $(PYTHON_VERSION)" || (echo "clearing virtualenv to bump version"; rm -rf $(VIRTUALENVDIR) )

setup: preflight cert $(VIRTUALENVDIR) install .env .env.test .env.integration
	@$(MYSHELL) -lc "workon $(VIRTUALENV)"

preflight:
	@echo "checking for dependencies that require manual install:"
	@echo "Detected '$(SHELL_NAME)' as default shell."
	@echo "Using '~/$(PROFILE_FILE)' as shell profile location."
	@which -s brew > /dev/null || (echo "installing homebrew"; /usr/bin/ruby -e "$$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)")
	@brew list openssl 2>&1 > /dev/null || brew install openssl
	@brew list python 2>&1 > /dev/null || brew install python
	@$(MYSHELL) -lc 'test "$$VIRTUALENVWRAPPER_PYTHON" = "/usr/local/bin/python3"' || (echo 'set VIRTUALENVWRAPPER_PYTHON to python3'; echo 'VIRTUALENVWRAPPER_PYTHON=/usr/local/bin/python3' >> ~/$(PROFILE_FILE) )
	@pyenv install --list | grep '^ *$(PYTHON_VERSION)$$' 1>/dev/null 2>&1 || (echo 'updating pyenv';  brew upgrade pyenv)
	@pyenv install --list | grep '^ *$(PYTHON_VERSION)$$' 1>/dev/null 2>&1 || (echo 'Python version $(PYTHON_VERSION) not available from pyenv';  false)
	@which -s pyenv > /dev/null || (echo "installing pyenv"; brew install pyenv)
	@$(MYSHELL) -lc "type pyenv | grep -q 'pyenv $(FUNCTION_SUFFIX)'" || (echo 'configuring pyenv per instructions starting at step 3: https://github.com/pyenv/pyenv#basic-github-checkout'; echo 'if command -v pyenv 1>/dev/null 2>&1; then\n  eval "$$(pyenv init -)"\nfi' >> ~/$(PROFILE_FILE))
	@$(MYSHELL) -lc "pyenv local $(PYTHON_VERSION)" || (echo "installing python $(PYTHON_VERSION) from pyenv"; pyenv install $(PYTHON_VERSION))
# the above check might work and we get here because the wrong openssl was previously installed.
# This will force a rebuild of the python from pyenv with the newly installed openssl from above.
	@$(MYSHELL) -lc 'pyenv exec python3 -c "import ssl, sys; v = ssl.OPENSSL_VERSION_INFO; sys.exit(int(not v[:3] >= (1,0,2)))"' || (echo "installing python $(PYTHON_VERSION) from pyenv with updated openssl"; pyenv install $(PYTHON_VERSION))
# fail safe, if we get here and the check fails again. Manual intervention is required.
	@$(MYSHELL) -lc 'pyenv exec python3 -c "import ssl, sys; v = ssl.OPENSSL_VERSION_INFO; sys.exit(int(not v[:3] >= (1,0,2)))"' || (echo "OpenSSL 1.0.2 or higher is required but I need manual intervention to make it work"; false)
	@which -s pip || (echo "installing pip"; sudo -H python3 -m ensurepip -U)
# this line needs to cd out of the repo directory so that we're not picking up the local
# pyenv python
	@which -s virtualenv || (echo "installing virtualenv"; (cd ..; sudo -H python3 -m pip install virtualenv))
# this line needs to cd out of the repo directory so that we're not picking up the local
# pyenv python
	@which -s virtualenvwrapper.sh || (echo "installing virtualenv-wrapper"; (cd ..; sudo -H python3 -m pip install virtualenvwrapper); echo 'source /usr/local/bin/virtualenvwrapper.sh' >> ~/$(PROFILE_FILE))
	@which -s foreman || (echo "installing foreman"; sudo gem install foreman)
	@which -s nginx || (echo "installing nginx"; brew install nginx)
	@which -s jq || (echo "installing jq"; brew install jq)
	@$(MYSHELL) -lc "type virtualenvwrapper | grep -q 'virtualenvwrapper $(FUNCTION_SUFFIX)'" || (echo "activating virtualenv-wrapper"; echo 'source /usr/local/bin/virtualenvwrapper.sh' >> ~/$(PROFILE_FILE) )
	@echo "preflight check complete"


install: requirements.txt $(VIRTUALENVDIR)
	$(VIRTUALENVDIR)/bin/pip install -U pip
	export LDFLAGS="-L/usr/local/opt/openssl/lib"; $(VIRTUALENVDIR)/bin/pip install -r requirements.txt

.env:
	cp env.template .env

$(VIRTUALENVDIR): checkvirtualenvversion
	$(MYSHELL) -lc "mkvirtualenv --python=`pyenv which python3` $(VIRTUALENV) -a ."

nginx/server.crt nginx/server.key:
	mkdir -p nginx
	openssl genrsa -des3 -passout pass:gsahdg -out nginx/server.pass.key 2048
	openssl rsa -passin pass:gsahdg -in nginx/server.pass.key -out nginx/server.key
	openssl req -new -key nginx/server.key -out nginx/server.csr
	openssl x509 -req -days 365 -in nginx/server.csr -signkey nginx/server.key -out nginx/server.crt

test:
	./bin/independent-test-run.sh
	heroku local:run ./manage.py test --env=.env,.env.test

clean:
	find . -name '.git' -prune -o -name '*.pyc' -exec rm {} \;

veryclean: clean
	rm -rf .venv $(VIRTUALENVDIR)
	rm -f nginx/server.crt server.key

help:
	@echo "make preflight       check major binary dependencies are installed"
	@echo "make setup       first time setup of development environment"
	@echo "make install     installed development dependencies"
	@echo "make clean       remove development dependencies"
	@echo "make veryclean   make like a fresh checkout"
	@echo "make cert            create self signed SSL Certifcate for nginx SSL termination"
