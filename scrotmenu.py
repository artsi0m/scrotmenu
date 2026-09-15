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


selected_opts_barr = []

def exec_scrot():
    print(selected_opts_barr)

def first_cell(tsv_row: bytes) -> bytes:
    return tsv_row.split(b'\t')[0]

def second_cell(tsv_row: bytes) -> bytes:
    return tsv_row.split(b'\t')[1]

def forth_cell(tsv_row: bytes) -> bytes:
    return tsv_row.split(b'\t')[3]

def seive_opts_barr(opts: bytes) -> bytes:
    ret = bytearray()
    for row in opts.split(b'\n'):
        if not bytes.isalpha(first_cell(row)):
            pass
        else:
            new_row = first_cell(row) + b'\t' + second_cell(row) + b'\t' + forth_cell(row) + b'\n'
            ret.extend(new_row)
    return ret

menu_input_barr.extend(seive_opts_barr(list_opts_barr))

while True:
    prompt_string = b'scrot ' + b' '.join(s for s in selected_opts_barr)
    menu_comp_stdout = run([ *menu_exec, b'-p', prompt_string],
                         input=menu_input_barr, capture_output=True).stdout
    if menu_comp_stdout == trig_exec_entry:
        exec_scrot()
        break
    elif menu_comp_stdout == trig_exit_entry:
        exit()
    else:
        option_letter = first_cell(menu_comp_stdout)
        option = b'-' + option_letter
        if option in selected_opts_barr:
            pass
        # TODO: just cleanup such options in menu_input_barr bytearray
        elif option == b'- ': 
            pass
        else:
            selected_opts_barr.append(option)
