#!/usr/bin/env python3

from subprocess import run,Popen,PIPE

menu_exec = ['rofi', '-dmenu']  # dmenu compatible menu with prompt (-p) option
trig_exec_entry = b'\tRun scrot\n' # String that executes scrot when selected with menu
trig_exit_entry = b'\tQuit scrot menu\n'

scrot_opts_barr = Popen(['scrot', '--list-options=tsv'],
                        stdout=PIPE).stdout.read()

menu_input_barr = bytearray()
menu_input_barr.extend(trig_exec_entry)
menu_input_barr.extend(trig_exit_entry)
menu_input_barr.extend(scrot_opts_barr)

scrot_opts = []

def exec_scrot():
    print(scrot_opts)

def tsv_row_first_cell(tsv_row: bytes) -> str:
    return tsv_row.split(b'\t')[0].decode()

while True:
    prompt_string = 'scrot ' + ' '.join(str(s) for s in scrot_opts)
    menu_comp_stdout = run([ *menu_exec, b'-p', prompt_string],
                         input=menu_input_barr, capture_output=True).stdout
    if menu_comp_stdout == trig_exec_entry:
        exec_scrot()
        break
    elif menu_comp_stdout == trig_exit_entry:
        exit()
    else:
        option_letter = tsv_row_first_cell(menu_comp_stdout)
        option = '-' + option_letter
        if option in scrot_opts:
            pass
        # TODO: just cleanup such options in menu_input_barr bytearray
        elif option == '- ': 
            pass
        else:
            scrot_opts.append(option)
