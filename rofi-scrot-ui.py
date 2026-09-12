#!/usr/bin/env python3

from subprocess import run,Popen,PIPE

menu_exec = ['rofi', '-dmenu'] # dmenu compatible menu
trig_exec_bytes = bytes('\tRun scrot\n'.encode()) # String that executes scrot when selected with menu

scrot_opts_proc = Popen(['scrot', '--list-options=tsv'], stdout=PIPE)
rofi_input_barr = bytearray()
rofi_input_barr.extend(trig_exec_bytes)
rofi_input_barr.extend(scrot_opts_proc.stdout.read())

chosen_opts_arr = []

def exec_scrot():
    print(chosen_opts_arr)

def tsv_row_first_cell(tsv_row: bytes) -> str:
    return tsv_row.split(b'\t')[0].decode()

while True:
    rofi_comp_proc = run(menu_exec, input=rofi_input_barr, capture_output=True)
    if rofi_comp_proc.stdout == trig_exec_bytes:
        exec_scrot()
        break
    else:
        option = tsv_row_first_cell(rofi_comp_proc.stdout)
        if option in chosen_opts_arr:
            pass
        else:
            chosen_opts_arr.append(option)

