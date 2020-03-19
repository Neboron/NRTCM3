# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals
import regex, six, math, sys

from pyfiglet import figlet_format
from pprint import pprint
from PyInquirer import style_from_dict, Token, prompt
from PyInquirer import Validator, ValidationError
from pyconfigstore import ConfigStore

import glob
import os

from rtcm3_parser import rtcm3_parser



try:
    import colorama
    colorama.init()
except ImportError:
    colorama = None

try:
    from termcolor import colored
except ImportError:
    colored = None


# Variables declaration
file_list_1 = []
file_number = 0
msg_file_data = ""



style = style_from_dict({
    Token.QuestionMark: '#E91E63 bold',
    Token.Selected: '#673AB7 bold',
    Token.Instruction: '',  # default
    Token.Answer: '#2196f3 bold',
    Token.Question: '',
})



def log(string, color, font="slant", figlet=False):
    if colored:
        if not figlet:
            six.print_(colored(string, color))
        else:
            six.print_(colored(figlet_format(
                string, font=font), color))
    else:
        six.print_(string)



class NumberValidator(Validator):
    def validate(self, document):
        try:
            float(document.text)
        except ValueError:
            raise ValidationError(
                message='Please enter a number',
                cursor_position=len(document.text))  # Move cursor to end



def MenuList():
    menu_list = [
        {
        'type': 'list',
        'name': 'menu',
        'message': 'What operation do you need?',
        'choices': ['RTCM3 parser', 'Parse RTCM3 message file', 'Position trnsformation'],
        'filter': lambda val: val.lower()
        }
    ]
    answers = prompt(menu_list, style=style)
    return answers




def InputDataList():
    input_data_list = [
        {
        'type': 'list',
        'name': 'menu',
        'message': 'Choose file',
        'choices': ['Files list',
                    'Set path',
                    '<-Back'
                   ],
        'filter': lambda val: val.lower()
        }
    ]
    answers = prompt(input_data_list, style=style)
    return answers




def FilesListInput():
    variables = [
        {
            'type': 'input',
            'name': 'File number',
            'message': 'file:',
            'validate': NumberValidator
        }
    ]
    answers = prompt(variables, style=style)
    return answers



class nrtcm3:

    def __init__(self) :
        self.rtcmp = rtcm3_parser()
        pass

    def MainMenu(self):
        menuInfo = MenuList()
        if (menuInfo.get("menu") == "rtcm3 parser"):
            self.FileParserMenu()
        elif (menuInfo.get("menu") == "parse rtcm3 message file"):
            self.FileParserMenu()
        pass

    def FileParserMenu(self):
        dataMenuInfo = InputDataList()
        if (dataMenuInfo.get("menu") == "files list"):
            self.FilesList()
        elif (dataMenuInfo.get("menu") == "<-back"):
            self.MainMenu()
        pass

    def FilesList(self):
        path_to_msg_files = os.path.abspath(os.getcwd())+"/msg_files/*.txt"
        global file_list_1; file_list_1 = glob.glob(path_to_msg_files)
        n = 1
        for files in file_list_1:
            log(str(n) + " " + files, "green")
            n+=1

        variableInfo = FilesListInput()
        global file_number;  file_number = int(variableInfo.get("File number"))

        msg_file = open(file_list_1[file_number-1], "r")
        global msg_file_data; msg_file_data = msg_file.read()
        print(msg_file_data)
        self.ParseFile()

        self.FileParserMenu()
        pass

    def ParseFile(self):
        global msg_file_data
        msg_file_data = msg_file_data.replace("\r", "")
        msg_file_data = msg_file_data.replace("\n", "")
        msg_file_data = bytearray.fromhex(msg_file_data)
        self.rtcmp.process_rtcm_data(msg_file_data)
        




def main():
    nr = nrtcm3()
    log("NRTCM 3", color="yellow", figlet=True)
    log("RTCM3 tools", "green")
    

    nr.MainMenu()

    sys.exit()



if __name__ == '__main__':
    main()




