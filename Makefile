APPNAME        := nautilus-create-new-file
PY_FILE        := nautilus-create-new-file.py
PO_DIR         := po
LOCALE_DIR     := locale
USER_EXT_DIR   := $(HOME)/.local/share/nautilus-python/extensions

.PHONY: all pot mo clean install uninstall

all: mo

# Update/generate pot file
pot:
	@mkdir -p $(PO_DIR)
	xgettext -k_ -o $(PO_DIR)/$(APPNAME).pot $(PY_FILE)
	@for f in $(wildcard $(PO_DIR)/*.po); do \
	  echo "Updating $$f…"; \
	  msgmerge --update --backup=none $$f $(PO_DIR)/$(APPNAME).pot; \
	done

# Compile translations
mo:
	@mkdir -p $(LOCALE_DIR)
	@for f in $(wildcard $(PO_DIR)/*.po); do \
	  lang=$$(basename $$f .po); \
	  mkdir -p "$(LOCALE_DIR)/$$lang/LC_MESSAGES"; \
	  msgfmt "$$f" -o "$(LOCALE_DIR)/$$lang/LC_MESSAGES/$(APPNAME).mo"; \
	done

clean:
	rm -rf $(LOCALE_DIR)

# User install
install: mo
	install -m 0644 "$(PY_FILE)" "$(USER_EXT_DIR)/$(PY_FILE)"
	mkdir -p "$(USER_EXT_DIR)/$(APPNAME)/"
	cp -a "$(LOCALE_DIR)" "$(USER_EXT_DIR)/$(APPNAME)/"
	@echo "$(APPNAME) installed in $(USER_EXT_DIR)/$(APPNAME)"

uninstall:
	rm -f "$(USER_EXT_DIR)/$(PY_FILE)"
	rm -rf "$(USER_EXT_DIR)/$(APPNAME)"
	@echo "Removed $(APPNAME) files and locales from $(USER_EXT_DIR)"
