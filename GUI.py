import sys
import os
import tkinter.filedialog
from pathlib import Path
import PySimpleGUI as sg
from tkinter import *

import pygame
from math import ceil
import re

WIDTH = 1024
HEIGHT = 700
FONT_SIZES = [8, 10, 11, 12, 13, 14, 16, 18, 20, 22, 24]

ROOT = Path(os.getcwd())
NOTES_FOLDER = Path(os.getcwd()).joinpath('Notes')
ICON = 'icon.ico'

pygame.init()


# ///////////////////////////////////////////////////////////////////////////////////////////////////

class Menu:
    def __init__(self, w, h):
        self.WIDTH = w
        self.HEIGHT = h


# ///////////////////////////////////////////////////////////////////////////////////////////////////


class TextEditor:
    def __init__(self, width, height):
        self.w = width
        self.h = height
        self.theme = 'LightBlue1'
        sg.set_options(self.theme)

        self.default_font = 'Arial'
        self.font_size = 12
        self.font = 'Arial'
        self.all_fonts = [i.capitalize() for i in pygame.font.get_fonts()]
        self.toolbar_height = ceil(self.h / 10)

        # self.title_bar = sg.Titlebar(title='Notey', key='TITLE BAR', icon=sg.Image(ICON, size=(100, 50)))

        menu_def = [['File', ['New', 'Open', 'Save', 'Exit', ]], ['Edit', ['Undo', 'Redo', 'Copy', 'Paste'], ],
                    ['View', ['Zoom', 'Wrap Text'], ],
                    ['Help', 'About...'], ['Tools', ['Word Count', 'Word Counts'], ],
                    ['Settings', ['Change Theme'], ]]

        self.menu_layout = [[sg.Menu(menu_definition=menu_def, visible=True, key='MENU')]]

        self.menu_bar = sg.Frame(key='MENU BAR', size=(10, 10), layout=self.menu_layout, title='')

        self.toolbar_layout = [[self.menu_bar],
                               [sg.Combo(values=self.all_fonts, default_value=self.all_fonts[0], key='FONT BOX',
                                         size=(20, 10)),
                                sg.Combo(size=(10, 10), key='FONT SIZE', values=FONT_SIZES,
                                         default_value=self.font_size),
                                sg.Button(button_text='I', font=('Arial', 10, 'italic'), key='ITALIC',
                                          enable_events=True,
                                          tooltip='Italic'),
                                sg.Button(button_text='B', font=('Arial', 10, 'bold'), key='BOLD', enable_events=True,
                                          tooltip='Bold'),
                                sg.Button(button_text='_', key='UNDERLINE', enable_events=True, tooltip='Underline'),
                                sg.ColorChooserButton(button_text='A', visible=True, key='TEXT COLOR',
                                                      tooltip='Change Text Color')]
                               ]

        self.toolbar = sg.Frame(key='TOOLBAR', size=(self.w, self.toolbar_height), title='', layout=self.toolbar_layout)

        self.layout = [
            [self.toolbar],
            [sg.Multiline('', size=(self.w, self.h), font=(self.default_font, self.font_size), key='NOTE',
                          expand_y=True, no_scrollbar=False)]
        ]

        self.WINDOW = sg.Window('Notey', layout=self.layout, size=(width, height), return_keyboard_events=True,
                                grab_anywhere=True, icon=ICON, use_custom_titlebar=False, auto_size_text=True)

    def change_app_theme(self):
        # global selected_theme
        theme_selection_window_layout = [
            [sg.Combo(values=sg.theme_list(), default_value=self.theme, enable_events=True, key='THEME SELECT BOX'),
             sg.Button('Cancel', key='CANCEL THEME SELECT', enable_events=True),
             sg.Button('Apply', key='APPLY SELECTED THEME', enable_events=True)]
        ]
        theme_selection_window = sg.Window(title='Theme Selection', size=(300, 200),
                                           layout=theme_selection_window_layout,
                                           modal=True)

        while True:
            ev, vals = theme_selection_window.read()
            # print(ev)
            if ev == sg.WIN_CLOSED:
                break

            if ev == 'CANCEL THEME SELECT':
                theme_selection_window.close()
            if ev == 'THEME SELECT BOX':
                selected_theme = vals['THEME SELECT BOX']
                # current_theme = sg.LOOK_AND_FEEL_TABLE[selected_theme]
                self.theme = selected_theme
            if ev == 'APPLY SELECTED THEME':
                if vals['THEME SELECT BOX']:
                    selected_theme = vals['THEME SELECT BOX']
                    current_theme = sg.LOOK_AND_FEEL_TABLE[selected_theme]
                    self.theme = selected_theme
                    # iterate thru widgets
                    for v, element in self.WINDOW.AllKeysDict.items():
                        try:
                            color = current_theme.get(element.Type.upper())
                            if color:

                                if element.Type == 'button':
                                    element.Widget.config(foreground=color[0], background=color[1])
                                else:

                                    element.Widget.config(background=color)
                                element.update()
                            else:
                                element.BackgroundColor = current_theme['BACKGROUND']
                        except Exception as e:
                            print(e)

                    # TODO: figure out how to get rest of bg's to change color, font colors etc.
                    self.WINDOW.TKroot.configure(background=current_theme['BACKGROUND'])
                    self.WINDOW.TtkTheme = selected_theme
                    self.toolbar.Widget.configure(background=current_theme['BACKGROUND'])
                    self.menu_bar.Widget.configure(background=current_theme['BACKGROUND']) \
 \
                        # for item in tool bar and menu bar to change texts i think

    def save(self, text: sg.Multiline):
        file = tkinter.filedialog.asksaveasfile(defaultextension='.txt',
                                                filetypes=[("Text file", ".txt"), ("All Files", ".*")],
                                                initialdir=NOTES_FOLDER)
        file.writelines(text)

    def open(self):
        saved_file = tkinter.filedialog.askopenfilename(defaultextension='.txt',
                                                        filetypes=[("Text file", ".txt"), ("All Files", ".*")],
                                                        initialdir=NOTES_FOLDER)
        with open(saved_file, 'r') as f:
            content = f.readlines()
        for i in self.layout:
            for element in i:
                if type(element) == sg.Multiline:
                    element.update(value=f'{"".join(content)}')
                    self.WINDOW.refresh()

    def about(self):
        layout = [
            [sg.Text(
                text=f'Notey is a note-taking app created by Matt Blair in 2023, written entirely in Python using packages like pygame and PySimpleGUI! If you have questions about how to use this app, dont bother asking! Tyty :)',
                size=(50, 10))]
        ]
        about_window = sg.Window(title='About Notey', layout=layout)

        while True:
            event, vals = about_window.read()

            if event == sg.WIN_CLOSED:
                break

    def new_file(self):
        pass

    def select_text(self, selection):
        # TODO: figure this out
        self.WINDOW.find_element(key='NOTE', silent_on_error=True)

    def count_words(self, text):
        pattern = r'\w+'
        words = re.findall(pattern, text)

        lil_layout = [
            [sg.Text(text=f'The file has {len(words)} words.', key='WORD COUNT')],
            # [sg.Cancel(button_text='Close', auto_size_button=True, key='CLOSE WORD COUNT')]
        ]
        lil_window = sg.Window(title='Word Count', layout=lil_layout, size=(200, 100), modal=True)

        while True:
            event, values = lil_window.read()

            if event == sg.WIN_CLOSED:
                break

            if event == 'CLOSE WORD COUNT':
                break


    # TODO: these all crash app if no selection, and edits the whole document instead of just the selected text
    def bolden(self, selection):
        multiline_elt = self.WINDOW['NOTE']
        multiline_elt.Widget.config(font=(self.font, self.font_size, 'bold'))
        self.WINDOW.refresh()

    def italicize(self, selection):

        multiline_elt = self.WINDOW['NOTE']
        multiline_elt.Widget.config(font=(self.font, self.font_size, 'italic'))
        self.WINDOW.refresh()

    def underline(self, selection):
        multiline_text_full = self.WINDOW['NOTE']
        print(multiline_text_full.Widget.config().get('font'))
        multiline_text_full.update(selection, append=False, font=(self.font, self.font_size, 'underline'))

        self.WINDOW.refresh()

    def change_text_color(self):
        pass

    def change_text_font(self):
        pass


# ///////////////////////////////////////////////////////////////////////////////////////////////////


# ///////////////////////////////////////////////////////////////////////////////////////////////////


editor = TextEditor(WIDTH, HEIGHT)

while True:

    event, values = editor.WINDOW.read()

    if event == sg.WINDOW_CLOSED:
        break

    # if event in ['Copy', 'Select']:
    #     try:
    #         editor.WINDOW['NOTE'].Widget.selection_get()
    #         print(selection)
    #         editor.select_text(selection)
    #     except:
    #         pass
    #
    # if event == 'Paste':
    #     try:
    #         print(selection)
    #         editor.WINDOW['NOTE'].Widget.insert(selection)
    #         print(pygame.mouse.get_cursor())
    #         editor.WINDOW.refresh()
    #     except:
    #         pass


    # TODO: fix, this crashes when nothing is selected
    if event in ['BOLD', 'ITALIC', 'UNDERLINE']:
        match event:
            case 'BOLD':
                editor.bolden(selection=editor.WINDOW['NOTE'].Widget.selection_get())
            case 'ITALIC':
                editor.italicize(selection=editor.WINDOW['NOTE'].Widget.selection_get())
            case 'UNDERLINE':
                editor.underline(selection=editor.WINDOW['NOTE'].Widget.selection_get())

    if event == 'Word Count':
        editor.count_words(values['NOTE'])

    if event == 'Change Theme':
        editor.change_app_theme()

    if event in ['New', 'Open', 'Save', 'Exit']:
        match event:
            case 'New':
                pass
            case 'Open':
                editor.open()
            case 'Save':
                note = values['NOTE']
                editor.save(note)
            case 'Exit':
                pygame.quit()
                sys.exit()

    if event == 'About...':
        editor.about()

    print(event, values)

editor.WINDOW.close()
