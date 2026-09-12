#!/usr/bin/env python3

scrot_opts_proc = subprocess.Popen(['scrot', '--list-options=tsv'], stdout=subprocess.PIPE)
rofi_input_barr = bytearray(scrot_opts_proc.stdout.read())
rofi_input_barr.extend('Run scrot\n'.encode())
