#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
          ___
      .:::---:::.
    .'--:     :--'.                      ___     ____   ______        __ __  
   /.'   \   /   `.\      ____ _ ____   /   |   /  _/  /_  __/____ _ / // /__
  | /'._ /:::\ _.'\ |    / __ `// __ \ / /| |   / /     / /  / __ `// // //_/
  |/    |:::::|    \|   / /_/ // /_/ // ___ | _/ /     / /  / /_/ // // ,<   
  |:\ .''-:::-''. /:|   \__, / \____//_/  |_|/___/    /_/   \__,_//_//_/|_|  
   \:|    `|`    |:/   /____/                                                
    '.'._.:::._.'.'
      '-:::::::-'

goAI_talk - Football Match Results Q&A Bot
File: utils/header_script.py
Author: hosu-kim
Created: 2025-03-14 13:45:10 UTC

Description:
    Utility script to add standardized headers to Python files in the project.
    It preserves existing code while adding/updating the standardized header.
"""
import os
import re
import sys
from datetime import datetime

# Header template
HEADER_TEMPLATE = """#!/usr/bin/env python
# -*- coding: utf-8 -*-
\"\"\"
          ___
      .:::---:::.
    .'--:     :--'.                      ___     ____   ______        __ __  
   /.'   \   /   `.\      ____ _ ____   /   |   /  _/  /_  __/____ _ / // /__
  | /'._ /:::\ _.'\ |    / __ `// __ \ / /| |   / /     / /  / __ `// // //_/
  |/    |:::::|    \|   / /_/ // /_/ // ___ | _/ /     / /  / /_/ // // ,<   
  |:\ .''-:::-''. /:|   \__, / \____//_/  |_|/___/    /_/   \__,_//_//_/|_|  
   \:|    `|`    |:/   /____/                                                
    '.'._.:::._.'.'
      '-:::::::-'

goAI_talk - Football Match Results Q&A Bot
File: {file_path}
Author: hosu-kim
Created: 2025-03-14 {time} UTC

Description:
    {description}
\"\"\"
"""

def format_time():
    """Generate current time in HH:MM:SS format"""
    return datetime.now().strftime("%H:%M:%S")

def get_description_prompt(file_path):
    """Generate a description prompt based on the file path"""
    if file_path.endswith('__init__.py'):
        return "Package initialization file."
        
    filename = os.path.basename(file_path)
    module_name = os.path.splitext(filename)[0]
    
    if "api" in file_path:
        return f"This module provides API functionality for {module_name}."
    elif "database" in file_path:
        return f"This module handles database operations for {module_name}."
    elif "interface" in file_path:
        return f"This module provides user interface components for {module_name}."
    elif "utils" in file_path:
        return f"This module provides utility functions for {module_name}."
    elif "llm" in file_path:
        return f"This module handles language model operations for {module_name}."
    else:
        return "Please add a description for this module."

def process_file(file_path):
    """Add or update the header in the given file"""
    if not file_path.endswith('.py'):
        print(f"Skipping non-Python file: {file_path}")
        return False
        
    try:
        # Read the file
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Check if it already has our ASCII art header
        if '___\n      .:::---:::.' in content:
            print(f"Header already exists in {file_path}")
            return False
            
        # Extract any existing file docstring for description
        description = ""
        doc_match = re.search(r'"""(.*?)"""', content, re.DOTALL)
        if doc_match:
            desc_lines = doc_match.group(1).strip().split('\n')
            if len(desc_lines) > 1:
                description = desc_lines[0]
            
        # If no description found, generate a prompt
        if not description:
            description = get_description_prompt(file_path)
            
        # Create relative file path for the header
        rel_path = os.path.relpath(file_path, os.path.dirname(os.path.dirname(file_path)))
        
        # Generate new header
        new_header = HEADER_TEMPLATE.format(
            file_path=rel_path,
            time=format_time(),
            description=description
        )
        
        # Remove existing shebang, encoding, and docstring if present
        content = re.sub(r'^#!.*\n', '', content)
        content = re.sub(r'^# -\*-.*-\*-\n', '', content)
        content = re.sub(r'^""".*?"""\n', '', content, flags=re.DOTALL)
        
        # Add new header
        new_content = new_header + '\n' + content.lstrip()
        
        # Write back to file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
            
        print(f"Added header to {file_path}")
        return True
        
    except Exception as e:
        print(f"Error processing {file_path}: {str(e)}")
        return False

def process_directory(directory):
    """Process all Python files in the directory and its subdirectories"""
    success_count = 0
    fail_count = 0
    
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                success = process_file(file_path)
                if success:
                    success_count += 1
                else:
                    fail_count += 1
                    
    print(f"Completed: {success_count} files updated, {fail_count} files skipped or failed.")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python header_script.py <directory_path>")
        sys.exit(1)
        
    target_dir = sys.argv[1]
    if not os.path.isdir(target_dir):
        print(f"Error: {target_dir} is not a valid directory")
        sys.exit(1)
        
    print(f"Adding headers to Python files in {target_dir}...")
    process_directory(target_dir)
