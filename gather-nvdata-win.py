#!/usr/bin/python3

import subprocess
import xml.etree.ElementTree as ET

def parse_element(element):
    """Recursively parse XML elements into dictionaries."""
    if len(element) == 0:
        return element.text
    else:
        result = {}
        for child in element:
            if child.tag in result:
                # If the key already exists, convert its value to a list
                if not isinstance(result[child.tag], list):
                    result[child.tag] = [result[child.tag]]
                result[child.tag].append(parse_element(child))
            else:
                result[child.tag] = parse_element(child)
        return result

def nvidia_smi_to_dict():
    try:
        output = subprocess.check_output(["nvidia-smi", "-q", "-x"], universal_newlines=True)
        root = ET.fromstring(output)
        return parse_element(root)
    except subprocess.CalledProcessError as e:
        print("Error executing command:", e)
        return None

def only_digits(s):
    #print(f"The value is this: ",s)
    if s == "N/A":
        #print("RETURNING NONE")
        return None
    r_num = ''.join(filter(lambda x: x.isdigit() or x == '.', s))
    return int(float(r_num))
    
def truncate_after_space(s):
    space_index = s.find(' ')
    if space_index != -1:
        return s[:space_index]
    else:
        return s

nvidia_info = nvidia_smi_to_dict()
if nvidia_info:
    process_info_list = nvidia_info['gpu']['processes']['process_info']
    product_name = nvidia_info['gpu']['product_name']
    # define metrics to capture
    metrics = {
        'gpu_temp': nvidia_info['gpu']['temperature']['gpu_temp'],
        'power_draw': nvidia_info['gpu']['gpu_power_readings']['power_draw'],
        'mem_total': nvidia_info['gpu']['fb_memory_usage']['total'],
        'mem_free': nvidia_info['gpu']['fb_memory_usage']['free'],
        'mem_used': nvidia_info['gpu']['fb_memory_usage']['used'],
        'mem_reserved': nvidia_info['gpu']['fb_memory_usage']['reserved'],
        'fan_speed': nvidia_info['gpu']['fan_speed'],
        'graphics_clock': nvidia_info['gpu']['clocks']['graphics_clock'],
        'sm_clock': nvidia_info['gpu']['clocks']['sm_clock'],
        'mem_clock': nvidia_info['gpu']['clocks']['mem_clock'],
        'video_clock': nvidia_info['gpu']['clocks']['video_clock'],
        'max_graphics_clock': nvidia_info['gpu']['max_clocks']['graphics_clock'],
        'max_sm_clock': nvidia_info['gpu']['max_clocks']['sm_clock'],
        'max_mem_clock': nvidia_info['gpu']['max_clocks']['mem_clock'],
        'max_video_clock': nvidia_info['gpu']['max_clocks']['video_clock'],
    }

    output_structure = f'name=Custom Metrics|nvidia-smi|{product_name}|'
    # output non-process metrics
    for metric_name, metric_value in metrics.items():
        metric_value = only_digits(metric_value)
        if metric_value == None:
            continue
        print(output_structure + f"{metric_name.replace('_', ' ').title()}, value={metric_value}")
    # iterate through processes
    #for i, process_info in enumerate(process_info_list, start=1):
    #    process_name = truncate_after_space(process_info['process_name'])
    #    used_memory = process_info['used_memory']
    #    used_memory = only_digits(used_memory)
    #    print(output_structure + f"Processes|{process_name}|Used Memory, value={used_memory}")
    if isinstance(process_info_list, list):
        for i, process_info in enumerate(process_info_list, start=1):
            #process_name = truncate_after_space(process_info['process_name'])
            process_name = process_info['process_name']
            used_memory = process_info['used_memory']
            used_memory = only_digits(used_memory)
            print(output_structure + f"Processes|{process_name}|Used Memory, value={used_memory}")
    else:
        process_info = process_info_list
        process_name = truncate_after_space(process_info['process_name'])
        used_memory = process_info['used_memory']
        used_memory = only_digits(used_memory)
        print(output_structure + f"Processes|{process_name}|Used Memory, value={used_memory}")
