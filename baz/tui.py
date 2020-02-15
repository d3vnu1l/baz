import itertools
import sys

from asciimatics.event import KeyboardEvent, MouseEvent
from asciimatics.widgets import Frame, TextBox, Layout, Label, Divider, Text, CheckBox, Button, Background, DropdownList
from asciimatics.scene import Scene
from asciimatics.screen import Screen
from asciimatics.exceptions import ResizeScreenError, StopApplication

from baz.inventory import BazConfigInventory


class MainFrame(Frame):
    inventory = None

    def _create_checkboxes_from_dict(self, dictionary, layout, name):
        """Creates checkboxes with documentation"""
        layout.add_widget(Label(name), 1)
        layout.add_widget(Label(" "), 2)
        for flag, doc in dictionary.items():
            layout.add_widget(CheckBox(flag, name=flag, on_change=self._on_data_field_change), 1)
            layout.add_widget(Label("(" + doc + ")"), 2)

    def _create_config_menu(self, layout):
        layout.add_widget(Label("Configs:"), 1)
        layout.add_widget(Label(" "), 2)
        layout.add_widget(Label(" "), 3)

        toggle = itertools.cycle([1, 2, 3]).__next__
        for config in self.inventory.config_keys:
            layout.add_widget(CheckBox(config, name=config, on_change=self._on_data_field_change), toggle())

    def _create_compilation_modes_menu(self, layout):
        layout.add_widget(Label("Compilation Mode:"), 1)
        layout.add_widget(DropdownList(
            [("Fastbuild (Build as quickly as possible)", 'fastbuild'),
             ("Debug (Build with symbols and no optimization)", 'dbg'),
             ("Optimized (Build with full code optimization)", 'opt')],
            name="compilation_mode", on_change=self._on_data_field_change), 2)

    def _add_bazel_path_menu(self, layout):
        layout.add_widget(Label("Bazel Path:"), 1)
        layout.add_widget(Text(name="tool", on_change=self._on_data_field_change), 2)
        layout.add_widget(Label("Additional Bazel Flags:"), 1)
        layout.add_widget(Text(name="bazelopts", on_change=self._on_data_field_change), 2)

    def __init__(self, screen, inventory):
        self.inventory = inventory
        super(MainFrame, self).__init__(screen,
                                        int(screen.height * 10 // 11),
                                        int(screen.width * 14 // 15),
                                        data=inventory.persistent_data,
                                        has_shadow=True,
                                        name="Baz Configuration Menu")
        self.set_theme("bright")
        self._save_button = Button("Save", self._save_config)

        # Layout (Configs)
        layout_configs = Layout([1, 7, 7, 7, 1])
        self.add_layout(layout_configs)
        self._create_config_menu(layout_configs)

        # Layer (Bazel Path, copts, linkopts, other bazel options)
        layout_bazel_path = Layout([1, 8, 14, 1])
        self.add_layout(layout_bazel_path)
        self._add_bazel_path_menu(layout_bazel_path)

        # Layer (Compilation Modes)
        layoutcompilation_modes = Layout([1, 8, 14, 1])
        self.add_layout(layoutcompilation_modes)
        self._create_compilation_modes_menu(layoutcompilation_modes)

        # Layer (Troubleshooting)
        layout_troubleshooting = Layout([1, 8, 14, 1])
        self.add_layout(layout_troubleshooting)
        self._create_checkboxes_from_dict(self.inventory.troubleshooting_keydict, layout_troubleshooting, "Troubleshooting")

        # Layout 3 is just a dividor to match layout 1
        layout3 = Layout([1, 22, 1])
        self.add_layout(layout3)
        layout3.add_widget(Divider(), 1)

        # Layout 4 (Nav buttons)
        layout4 = Layout([1, 1, 1])
        self.add_layout(layout4)
        layout4.add_widget(Button("Reset", self._reset_config), 0)
        layout4.add_widget(self._save_button, 1)
        layout4.add_widget(Button("Save and Exit", self._save_config_and_exit), 2)
        self._save_button.disabled = True

        self.fix()

    def process_event(self, event):
        # Pass any events on to the Frame and contained widgets.
        return super(MainFrame, self).process_event(event)

    def _on_data_field_change(self):
        self.save()
        self._save_button.disabled = False

    def _reset_config(self):
        """Reset form data but do not write to disk"""
        self.data = self.inventory.get_default_data()
        self.save()

    def _save_config(self):
        """Save form data to disk"""
        self.save()
        self.inventory.save_to_file(self.data)
        self._save_button.disabled = True

    def _save_config_and_exit(self):
        self._save_config()
        raise StopApplication("User requested exit")

# Event handler for global keys


def global_shortcuts(event):
    if isinstance(event, KeyboardEvent):
        c = event.key_code
        if c in (17, 24):
            raise StopApplication("User terminated app")


def play_scenes(screen, scene, inventory):
    if sys.platform.startswith('win'):
        background_color = 0
    else:
        background_color = 234  # To match vscode gray

    screen.play([Scene([
        Background(screen, bg=background_color),
        MainFrame(screen, inventory)
    ], -1)], stop_on_resize=True, start_scene=scene, allow_int=True, unhandled_input=global_shortcuts)


def run_tui(inventory):
    last_scene = None
    while True:
        try:
            Screen.wrapper(play_scenes, catch_interrupt=False, arguments=[last_scene, inventory])
            break
        except ResizeScreenError as e:
            last_scene = e.scene

    return 0
