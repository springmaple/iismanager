from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput


class StartStopButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.is_started = False
        self.set_to_start()

    def set_to_start(self):
        self.text = 'Start'
        self.is_started = False
        self.background_color = (1, 1, 1, 1)

    def set_to_stop(self):
        self.text = 'Stop'
        self.is_started = True
        self.background_color = (1, 0, 0, 1)


class MyApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._selection_box = BoxLayout(orientation='vertical')
        self._console_widget = TextInput(multiline=True, font_size='10sp')
        self._site_labels = {}
        self._console_texts = {}
        self._pull_btns = {}
        self._build_btns = {}
        self._start_btns = {}
        self._selected_console_site_id = None

    def build(self):
        container = BoxLayout(orientation='horizontal')
        container.add_widget(self._selection_box)
        container.add_widget(self._console_widget)
        return container

    def add_site(self,
                 id_,
                 name,
                 on_pull_btn_pressed,
                 on_build_btn_pressed,
                 on_start_btn_pressed,
                 on_site_label_pressed):
        row = BoxLayout(orientation='horizontal')

        label_title = '[ref=%s]%s[/ref]' % (id_, name)
        self._site_labels[id_] = label = Label(text=label_title,
                                               on_ref_press=on_site_label_pressed,
                                               halign='left',
                                               markup=True)
        row.add_widget(label)

        self._pull_btns[id_] = pull_btn = Button(text='Pull', on_press=on_pull_btn_pressed, size_hint=(.4, 1))
        row.add_widget(pull_btn)

        self._build_btns[id_] = build_btn = Button(text='Build', on_press=on_build_btn_pressed, size_hint=(.4, 1))
        row.add_widget(build_btn)

        self._start_btns[id_] = start_btn = StartStopButton(on_press=on_start_btn_pressed, size_hint=(.4, 1))
        row.add_widget(start_btn)

        self._selection_box.add_widget(row)

    def disable_pull_btn(self, site_id):
        self._pull_btns[site_id].disabled = True

    def disable_build_btn(self, site_id):
        self._build_btns[site_id].disabled = True

    def get_start_btn(self, site_id):
        return self._start_btns.get(site_id, None)

    def set_console_output(self, site_id, text):
        self._console_texts[site_id] = self._console_texts.get(site_id, '') + text
        self._update_console()

    def clear_console_output(self, site_id):
        self._console_texts.pop(site_id, None)
        self._update_console()

    def set_console_site(self, id_):
        if self._selected_console_site_id is not None:
            self._site_labels[self._selected_console_site_id].color = (1, 1, 1, 1)
        self._selected_console_site_id = id_
        self._site_labels[self._selected_console_site_id].color = (0, 0, 1, 1)
        self._update_console()

    def _update_console(self):
        self._console_widget.text = self._console_texts.get(self._selected_console_site_id, '')
