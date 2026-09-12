#!/usr/bin/env python3

from subprocess import run,Popen,PIPE

menu_cmd = ['rofi', '-dmenu'] # dmenu compatible menu
trig_exec_bytes = bytes('\tRun scrot\n'.encode()) # String that executes scrot when selected with menu

scrot_opts_proc = Popen(['scrot', '--list-options=tsv'], stdout=PIPE)
rofi_input_barr = bytearray()
rofi_input_barr.extend(trig_exec_bytes)
rofi_input_barr.extend(scrot_opts_proc.stdout.read())


def exec_scrot():
    pass

while True:
    rofi_comp_proc = run(menu_cmd, input=rofi_input_barr, capture_output=True)
    if rofi_comp_proc.stdout == trig_exec_bytes:
        exec_scrot()
        break
