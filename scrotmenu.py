#!/usr/bin/env python3

from subprocess import run,Popen,PIPE

menu_exec = ['rofi', '-dmenu']  # dmenu compatible menu with prompt (-p) option
trig_exec_entry = b'\tRun scrot\n' # String that executes scrot when selected with menu
trig_exit_entry = b'\tQuit scrot menu\n'

list_opts_barr = Popen(['scrot', '--list-options=tsv'],
                        stdout=PIPE).stdout.read()

menu_input_barr = bytearray()
menu_input_barr.extend(trig_exec_entry)
menu_input_barr.extend(trig_exit_entry)
menu_input_barr.extend(list_opts_barr)

selected_opts_barr = []

def exec_scrot():
    print(selected_opts_barr)

def tsv_row_first_cell(tsv_row: bytes) -> bytes:
    return tsv_row.split(b'\t')[0]

while True:
    prompt_string = 'scrot ' + ' '.join(str(s) for s in selected_opts_barr)
    menu_comp_stdout = run([ *menu_exec, b'-p', prompt_string],
                         input=menu_input_barr, capture_output=True).stdout
    if menu_comp_stdout == trig_exec_entry:
        exec_scrot()
        break
    elif menu_comp_stdout == trig_exit_entry:
        exit()
    else:
        option_letter = tsv_row_first_cell(menu_comp_stdout)
        option = b'-' + option_letter
        if option in selected_opts_barr:
            pass
        # TODO: just cleanup such options in menu_input_barr bytearray
        elif option == b'- ': 
            pass
        else:
            selected_opts_barr.append(option)
