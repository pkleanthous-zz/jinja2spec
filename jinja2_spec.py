# -*- coding: utf-8 -*-
import yaml
import jinja2
import time
import colorama

jinja2_config_path = 'configurations/'
jinja2_exp_path = 'test/templates/'


def diff(templates_path, template_file, confg_file, expected_config):

    start_timestamp = time.time()

    tmp_text = "\nRunning jinja2Spec...\n"
    print(colorama.Fore.GREEN + colorama.Style.NORMAL + tmp_text)

    tmp_text = "Template: %s Configuration file: %s Expected Configuration: %s\n" % (
        template_file, confg_file, expected_config)
    print(colorama.Fore.GREEN + colorama.Style.NORMAL + tmp_text)

    colorama.init()

    ENV = jinja2.Environment(loader=jinja2.FileSystemLoader(
        templates_path))

    tmp_cfg_file = jinja2_config_path + confg_file
    with open(tmp_cfg_file) as config:
        config = yaml.load(config)

    template = ENV.get_template(template_file)
    output = template.render(config)

    cfg_list = []
    cfg_list = output.splitlines()
    cfg_list = [line for line in cfg_list if line.strip()]

    tmp_exp_cfg = jinja2_exp_path + expected_config
    expected_cfg = open(tmp_exp_cfg, "r").readlines()

    lineNum = 0
    error_count = 0

    for render_line in cfg_list:
        if lineNum > (len(expected_cfg) - 1):
            tmp_text = "Line: %d exist ONLY in generated file %s" % (
                lineNum, render_line)
            print(colorama.Fore.GREEN + colorama.Style.NORMAL + tmp_text)
            error_count += 1

        else:
            expected_line = expected_cfg[lineNum].strip('\n')
            if render_line != expected_line:
                tmp_text = "In Line: %d" % lineNum
                print(colorama.Fore.GREEN + colorama.Style.NORMAL + tmp_text)
                tmp_text = "Expected: %s" % expected_line
                print(colorama.Fore.GREEN + colorama.Style.NORMAL + tmp_text)
                tmp_text = "Got:      %s" % render_line
                print(colorama.Fore.RED + colorama.Style.NORMAL + tmp_text)
                error_count += 1
        lineNum += 1

    for i in range(lineNum, (len(expected_cfg))):
        tmp_text = "The following line not found in generated config: %s" % (expected_cfg[
                                                                             i].strip('\n'))
        print(colorama.Fore.RED + colorama.Style.NORMAL + tmp_text)

    if error_count == 0:
        tmp_text = "You are awesome! jinja2 spec passed successfully"
        print(colorama.Fore.YELLOW + colorama.Style.NORMAL + tmp_text)
    else:
        tmp_text = "jinja2 spec found %d error(s)" % error_count
        print(colorama.Fore.RED + colorama.Style.BRIGHT + tmp_text)

    elapsed_time = time.time() - start_timestamp
    tmp_text = "Elapsed Time: %.3f Seconds\n" % elapsed_time
    print(colorama.Fore.GREEN + colorama.Style.NORMAL + tmp_text)
