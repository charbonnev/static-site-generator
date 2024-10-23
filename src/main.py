import os
import shutil
from block_markdown import markdown_to_html_node
from inline_markdown import extract_title
from textnode import *

def erase_all_files_from_directory(directory):
    # erase all from directory
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f'Failed to delete {file_path}. Reason: {e}')

def copy_all_files(source, destination):
    dir_nodes = list(os.walk(source))
    # dir_nodes is like [('static', ['images'], ['index.css']), ('static/images', [], ['rivendell.png'])]
    dir_node = dir_nodes[0]
    root, dirs, files = dir_node
    for dir in dirs:
        shutil.copytree(os.path.join(root, dir), os.path.join(destination, dir))
    for file in files:
        shutil.copy(os.path.join(root, file), destination)
        
def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    # if not os.path.exists(dest_path):
    #     os.mkdir(dest_path)        
    md_content = ""
    with open(from_path, 'r', encoding='utf-8') as file:
        md_content = file.read()
    template_content = ""
    with open(template_path, 'r', encoding='utf-8') as file:
        template_content = file.read()
    title = extract_title(md_content)
    template_content = template_content.replace("{{ Title }}", title)
    html_node = markdown_to_html_node(md_content)
    html = template_content.replace("{{ Content }}", html_node.to_html())
    with open(dest_path, 'w', encoding='utf-8') as file:
        file.write(html)
        
def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    # crawl every entry in the content directory
    # for each markdown file found, generate a new .html file using the same template.html.
    # the generated pages should be written to the public directory in the same directory structure
    for entry in os.scandir(dir_path_content):
        if entry.is_file() and entry.name.endswith(".md"):
            dest_path = os.path.join(dest_dir_path, os.path.splitext(entry.name)[0] + ".html")
            generate_page(entry.path, template_path, dest_path)
        elif entry.is_dir():
            dest_subdir_path = os.path.join(dest_dir_path, entry.name)
            if not os.path.exists(dest_subdir_path):
                os.mkdir(dest_subdir_path)
            generate_pages_recursive(entry.path, template_path, dest_subdir_path)

def main():
    if os.path.exists("public"):
        erase_all_files_from_directory("public")
    else:
        os.mkdir("public")
    copy_all_files("static", "public")  
    generate_pages_recursive("content", "template.html", "public")
    

if __name__ == "__main__":
    main()