import json
import sys

ssl_var_constants = ['Subject', 'Altnames', 'Ciphers', 'Issuer']


def read_txt_file(txt_file_path):
    with open(txt_file_path, 'r') as txt_file:
        content = txt_file.read()
        return content


def write_json_file(json_file_path, content):
    with open(json_file_path, 'w') as json_file:
        json.dump(content, json_file, indent=4)


def contains_in_ssl_constants(line):
    for ssl_constant in ssl_var_constants:
        if ssl_constant in line:
            return True
    return False


def get_ssl_constant(line):
    for ssl_constant in ssl_var_constants:
        if ssl_constant in line:
            return ssl_constant


def convert_text_to_json(text):
    lines = text.split('\n')
    results = {}
    info_counter = 0
    ssl_params_list = {}
    for line in lines:
        if line.startswith('+') and ':' in line and not line.count(':') == 2 and not contains_in_ssl_constants(line):
            key, value = line.split(':', 1)
            results[process_str(key)] = process_str(value)
        elif line.startswith('+') and ':' not in line:
            results[f'info_{info_counter}'] = process_str(line)
            info_counter += 1
        elif line.startswith('-') and ':' in line:
            key, value = line.split(': ', 1)
            results[process_str(key)] = process_str(value)
        elif line.startswith('-') and ':' not in line and '---' not in line:
            results[f'info_{info_counter}'] = process_str(line)
            info_counter += 1
        elif line.count(':') == 2 and contains_in_ssl_constants(line):
            ssl_info, ssl_param, ssl_value = process_str(line).split(':', 2)
            ssl_params_list[process_str(ssl_param)] = process_str(ssl_value)
        elif contains_in_ssl_constants(line):
            ssl_param, ssl_value = process_str(line).split(':', 1)
            ssl_params_list[process_str(ssl_param)] = process_str(ssl_value)

    if ssl_params_list:
        results['SSl Info'] = ssl_params_list
    return results


def process_str(key):
    if '-' in key:
        if key.startswith('-'):
            return key.replace('-', '', 1).replace('\t', '').strip()
    if '+' in key:
        if key.startswith('+'):
            return key.replace('+', '', 1).replace('\t', '').strip()
    else:
        return key.replace('\t', '').strip()


def main(input_file, output_file):
    text = read_txt_file(input_file)
    content = convert_text_to_json(text)
    write_json_file(output_file, content)


if __name__ == '__main__':
    input_file = sys.argv[1] if len(sys.argv) > 1 else None
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    main(input_file, output_file)

# TODO () push code to GitHub
