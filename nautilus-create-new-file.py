import gi
gi.require_version("Nautilus", "4.0")
gi.require_version("Adw", "1")
gi.require_version("Gtk", "4.0")
from gi.repository import GObject, Adw, Gtk, Nautilus


class CreateFileDialog(Adw.Dialog):
    def __init__(self, folder: Nautilus.FileInfo):
        super().__init__()

        self.target_dir = folder.get_location().get_path()

        # Set up the dialog properties
        self.set_title("New File")
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
        self.file_name = Adw.EntryRow(title="File Name")
        list_box.append(self.file_name)
        self.file_name.connect("entry-activated", lambda *_: self.creaet_file())

        # Create submit button to call the creaet_file method
        self.submit_button = Gtk.Button(
            label="Create",
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

        # create the file using subprocess to call touch command
        import subprocess
        subprocess.run(["touch", f"{self.target_dir}/{file_name}"])

        self.close()


class CreateFileExtension(GObject.GObject, Nautilus.MenuProvider):
    def get_background_items(self, folder: Nautilus.FileInfo):
        menu_item = Nautilus.MenuItem(
            name="CreateFileExtension::CreateFile",
            label="New File…",
        )
        menu_item.connect(
            "activate",
            lambda *_: CreateFileDialog(folder).present(None),
            None,
        )
        return [
            menu_item,
        ]
