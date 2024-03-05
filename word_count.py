import os
import pathlib

DOCS_PATHS = ["state", "ui"]

def recursive_concatenate(path):
    if os.path.isfile(path):
        with open(path, 'r') as f:
            return f'File: {path}\n{f.read()}\n\n'
    return ''.join([recursive_concatenate(os.path.join(path, subpath)) for subpath in os.listdir(path)])

def add_component(path, components):
    for file in os.listdir(path):
        if "example" not in file and "api_ref" not in file:
            with open(os.path.join(path, file), 'r') as f:
                component_name = f.readline().strip()
                components[component_name] = {}
                components[component_name]["description"] = f.read()
            with open(os.path.join(path, file.replace(".txt", "_api_ref.txt")), 'r') as f:
                components[component_name]["api_ref"] = f.read()
            with open(os.path.join(path, "example.txt"), 'r') as f:
                components[component_name]["example"] = f.read()

def get_component_docs(path, components):
    if os.path.isfile(os.path.join(path, os.listdir(path)[0])):
        add_component(path, components)
    else:
        for subpath in os.listdir(path):
            get_component_docs(os.path.join(path, subpath), components)

docs = ""

for folder in ["state", "ui"]:
    if not os.path.isfile(folder) and '__pycache__' not in folder:
        docs += recursive_concatenate(folder)

components = {}

get_component_docs("components", components)