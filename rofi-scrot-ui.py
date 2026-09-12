#!/usr/bin/env python3

from subprocess import run,Popen,PIPE

menu_exec = ['rofi', '-dmenu']  # dmenu compatible menu with prompt
trig_exec_bytes = bytes('\tRun scrot\n'.encode()) # String that executes scrot when selected with menu

scrot_opts_proc = Popen(['scrot', '--list-options=tsv'], stdout=PIPE)
rofi_input_barr = bytearray()
rofi_input_barr.extend(trig_exec_bytes)
rofi_input_barr.extend(scrot_opts_proc.stdout.read())

scrot_opts = []

def exec_scrot():
    print(scrot_opts)

def tsv_row_first_cell(tsv_row: bytes) -> str:
    return tsv_row.split(b'\t')[0].decode()

while True:
    prompt_string = 'scrot ' + ' '.join(str(s) for s in scrot_opts)
    rofi_comp_proc = run([ *menu_exec, '-p', prompt_string],
                         input=rofi_input_barr, capture_output=True)
    if rofi_comp_proc.stdout == trig_exec_bytes:
        exec_scrot()
        break
    else:
        option_letter = tsv_row_first_cell(rofi_comp_proc.stdout)
        option = '-' + option_letter
        if option in scrot_opts:
            pass
        # TODO: just cleanup such options in rofi_input_barr bytearray
        elif option == '- ': 
            pass
        else:
            scrot_opts.append(option)
