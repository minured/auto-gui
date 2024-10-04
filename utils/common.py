import os
import yaml


def load_yaml(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            return yaml.safe_load(file)
    else:
        return None


def merge_configs(config1, config2):
    """递归合并两个配置字典，优先使用 config1 的值"""
    if isinstance(config1, dict) and isinstance(config2, dict):
        for key, value in config2.items():
            if key not in config1:
                config1[key] = value
            else:
                config1[key] = merge_configs(config1[key], config2[key])
    return config1


def snake_to_pascal_case(snake_str):
    components = snake_str.split('_')
    return ''.join(x.capitalize() for x in components)
