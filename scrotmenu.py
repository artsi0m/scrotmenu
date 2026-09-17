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


selected_opts_lst = []

def exec_scrot():
    print([b'scrot', *selected_opts_lst])

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

def handle_opt_stack_k(opts: list):
    menu_input_barr = b'h\nv'
    prompt_string = b'-k (--stack[=OPT])'
    sel = run([ *menu_exec, b'-p', prompt_string],
               input=menu_input_barr,
               capture_output=True).stdout.strip(b'\n')
    opts.append(b'-' + b'k')
    opts.append(sel)


def handle_opt_line_l() -> bytes:
    trig_exec_entry = b'\tSave selection style'
    trig_exit_entry = b'\tQuit selection style submenu'
    trig_mode_entry = b'mode'
    trig_style_entry = b'style'
    trig_width_entry = b'width'
    trig_opacity_entry = b'opacity'
    menu_input_barr = b'\n'.join(s for s in [ trig_exec_entry,
                                              trig_exit_entry,
                                              trig_mode_entry,
                                              trig_style_entry,
                                              trig_width_entry,
                                              trig_opacity_entry ])
    return menu_input_barr

while True:
    prompt_string = b'scrot ' + b' '.join(s for s in selected_opts_lst)
    menu_comp_stdout = run([ *menu_exec, b'-p', prompt_string],
                         input=menu_input_barr, capture_output=True).stdout
    if menu_comp_stdout == trig_exec_entry:
        exec_scrot()
        break
    elif menu_comp_stdout == trig_exit_entry:
        exit()
    elif first_cell(menu_comp_stdout) == b'k':
        handle_opt_stack_k(selected_opts_lst)
    else:
        option_letter = first_cell(menu_comp_stdout)
        option = b'-' + option_letter
        if option in selected_opts_lst:
            pass
        else:
            selected_opts_lst.append(option)
