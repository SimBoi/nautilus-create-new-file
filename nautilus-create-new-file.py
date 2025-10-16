import gi
gi.require_version("Nautilus", "4.0")
gi.require_version("Adw", "1")
gi.require_version("Gtk", "4.0")
from gi.repository import GObject, Adw, Gtk, Nautilus, Gio, GLib

# L10n
import gettext, locale, os, polib

base_dir = os.path.dirname(__file__)
locale_dir = os.path.join(base_dir, "nautilus-create-new-file-translations")

lang = locale.getlocale()[0]
po_path = os.path.join(locale_dir, f"{lang}.po")
if not os.path.exists(po_path) and "_" in lang:
    lang = lang.split("_")[0]
    po_path = os.path.join(locale_dir, f"{lang}.po")
mo_path = os.path.join(locale_dir, f"{lang}.mo")

if os.path.exists(po_path):
    # Compile .po to .mo if needed
    if not os.path.exists(mo_path):
        po = polib.pofile(po_path)
        po.save_as_mofile(mo_path)
    # Load translations
    with open(mo_path, "rb") as f_mo:
        trans = gettext.GNUTranslations(f_mo)
    _ = trans.gettext
else:
    # Fallback to no translation
    _ = lambda x: x


class CreateFileDialog(Adw.Dialog):
    def __init__(self, folder: Nautilus.FileInfo):
        super().__init__()

        self.target_dir = folder.get_location().get_path()

        # Set up the dialog properties
        self.set_title(_("New File"))
        self.set_content_width(450)
        root = Adw.ToolbarView()
        header_bar = Adw.HeaderBar()
        header_bar.set_decoration_layout(':close')
        root.add_top_bar(header_bar)
        body = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            hexpand=True,
            spacing=8,
            margin_top=16,
            margin_bottom=16,
            margin_start=16,
            margin_end=16,
        )
        root.set_content(body)
        list_box = Gtk.ListBox(css_classes=["boxed-list-separate"])
        body.append(list_box)

        # Create the entry for the file name
        self.file_name = Adw.EntryRow(title=_("File Name"))
        list_box.append(self.file_name)
        self.file_name.connect("entry-activated", lambda *_: self.creaet_file())

        # Create submit button to call the creaet_file method
        self.submit_button = Gtk.Button(
            label=_("Create"),
            css_classes=["pill", "suggested-action"],
            halign=Gtk.Align.CENTER,
            margin_top=8,
        )
        body.append(self.submit_button)
        self.submit_button.connect("clicked", lambda *_: self.creaet_file(), None)

        self.set_child(root)

    def creaet_file(self):
        file_name = self.file_name.get_text()
        if not file_name:
            return

        # check if the file already exists, if it does, append a number to the file name
        import os
        base_name, ext = os.path.splitext(file_name)
        counter = 1
        while os.path.exists(f"{self.target_dir}/{file_name}"):
            file_name = f"{base_name}_{counter}{ext}"
            counter += 1

        # create the file via GIO
        final_path = os.path.join(self.target_dir, file_name)
        gfile = Gio.File.new_for_path(final_path)
        gfile.replace_contents(b"", None, False, Gio.FileCreateFlags.NONE, None)
        self.close()
        
        # select file via D-Bus
        uri = gfile.get_uri()
        def _select():
            GLib.spawn_async(
                ['gdbus','call','--session',
                 '--dest','org.freedesktop.FileManager1',
                 '--object-path','/org/freedesktop/FileManager1',
                 '--method','org.freedesktop.FileManager1.ShowItems',
                 f"['{uri}']", "''"],
                flags=GLib.SpawnFlags.SEARCH_PATH)
            return False
        GLib.timeout_add(100, _select)


class CreateFileExtension(GObject.GObject, Nautilus.MenuProvider):
    def get_background_items(self, folder: Nautilus.FileInfo):
        menu_item = Nautilus.MenuItem(
            name="CreateFileExtension::CreateFile",
            label=_("New File…"),
        )
        menu_item.connect(
            "activate",
            lambda *_: CreateFileDialog(folder).present(Gtk.Application.get_default().get_active_window()),
            None,
        )
        return [
            menu_item,
        ]
