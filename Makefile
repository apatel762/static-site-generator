# ----------------------------------------------------------------------
# VARIABLES

# abs path of where the notes are
MARKDOWN_FILES_LOCATION=/home/arjun/.nb/notes

# relative path of the temp folder where the .backlinks files will go
# can also as a generic temp folder since it gets cleaned after every
# build (e.g. for index.html file generation)
TEMP_FOLDER=static-site-generator_output/cache

# relative path of the folder where the html files will go
HTML_FOLDER=static-site-generator_output/html

# a location on a server that you want to push the HTML files to
# if you host the website on a server that you manage
REMOTE_FILE_PATH=amigo@192.168.0.26:/var/broadwater/notes/raw/

# ----------------------------------------------------------------------

all: \
	install \
	build

clean:
	rm -rfv "$(TEMP_FOLDER)"
	rm -rfv "$(HTML_FOLDER)"

install:
	@static-site-generator/bin/install.sh
	venv/bin/pre-commit install
	venv/bin/pre-commit run

build:
	@venv/bin/python static-site-generator/bin/py/ssg.py \
		--notes "$(MARKDOWN_FILES_LOCATION)" \
		--temp "$(TEMP_FOLDER)" \
		--html "$(HTML_FOLDER)"
	@mkdir -p static-site-generator/bin/css
	@mkdir -p "$(HTML_FOLDER)/css"
	@rsync -avzh --ignore-missing-args static-site-generator/bin/css/*.css "$(HTML_FOLDER)/css"
	@rsync -avzh --ignore-missing-args static-site-generator/bin/css/*.woff2 "$(HTML_FOLDER)/css"
	@mkdir -p static-site-generator/bin/js
	@mkdir -p "$(HTML_FOLDER)/js"
	@rsync -avzh --ignore-missing-args static-site-generator/bin/js/*.js "$(HTML_FOLDER)/js"
	@rsync -avzh --ignore-missing-args static-site-generator/bin/js/index.json "$(HTML_FOLDER)/js"
	@rsync -avzh --ignore-missing-args "$(MARKDOWN_FILES_LOCATION)/html" "$(HTML_FOLDER)"

push:
	rsync -avzh --delete $(HTML_FOLDER)/* $(REMOTE_FILE_PATH)
