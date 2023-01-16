import os
import sys

# Extension should have been built in parent directory.
sys.path.append(os.path.dirname('..'))

from ringing import Row


methods = [
    ('Slinky', Row('14523ET90786')),
    ('Top', Row('2134567890ET')),
    ('Up', Row('2134TE098765')),
    ('Strange', Row.reverse_rounds(12)),
    ('Down', Row('8765432190TE')),
    ('Charm', Row('6543217890TE')),
    ('Meson', Row('1287094365ET')),
    ('Gluon', Row('13527496E8T0')),
    ('Baryon', Row('E9T705836142')),
]


LEAD_LIMIT = 4


def condensed_output(lead_heads, method_names):
    print(', '.join(method_names))


def full_output(lead_heads, method_names):
    print('1234567890ET  ' + method_names[0])
    print('------------')

    for i in range(len(method_names) - 1):
        print(str(lead_heads[i]) + '  ' + method_names[i + 1])

    print(lead_heads[-1])
    print('------------')
    print()


output_composition = condensed_output


def iterate(row, lead_heads, method_names):
    if len(lead_heads) >= LEAD_LIMIT:
        return

    for method_name, lead_head in methods:
        new_row = row * lead_head

        if new_row in lead_heads:
            continue  # Trivially false

        new_lead_heads = lead_heads + [new_row]
        new_method_names = method_names + [method_name]

        if new_row.is_rounds():
            output_composition(new_lead_heads, new_method_names)
            continue  # Have come round

        iterate(new_row, new_lead_heads, new_method_names)


iterate(Row(12), [], [])
