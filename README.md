# Create New File Dialog

An extension for Nautilus, adds a menu item to the right-click menu for creating a new file with a dialog instead of the default templates, you can create files with custom names and extensions using the dialog.

Check my [nautilus extension collection](https://github.com/SimBoi/nautilus-extension-collection).

## Installation
1. Install required packages. See my [nautilus extension collection](https://github.com/SimBoi/nautilus-extension-collection/blob/main/README.md) for details.
2. Clone the repo locally: `git clone https://github.com/SimBoi/nautilus-create-new-file && cd nautilus-create-new-file`
3. Install the extension with `make install` (this will perform a user install)

## Uninstallation
To uninstall the extension, either run `make uninstall` in the cloned repo or run
```
rm -f ~/.local/share/nautilus-python/extensions/nautilus-create-new-file.py
rm -rf ~/.local/share/nautilus-python/extensions/nautilus-create-new-file
```


<details>
  <summary>Additional make info</summary>

The Makefile supports the following commands
- `make pot`: regenerates pot file to include new strings from source file and updates po files
- `make mo`: compiles translations
- `make clean`: deletes the compiled translations
- `make install`: compiles translations and install the extension with translations for the user
- `make uninstall`: remove the extension and translations for the user

</details>
