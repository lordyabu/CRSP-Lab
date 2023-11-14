import os

def list_files(startpath):
    for root, dirs, files in os.walk(startpath):
        # Skip specific directories
        dirs[:] = [d for d in dirs if d not in ['.pytest_cache', 'another_folder_to_ignore', '.git', '__pycache__']]

        level = root.replace(startpath, '').count(os.sep)
        indent = ' ' * 4 * (level)
        print(f"{indent}- {os.path.basename(root)}/")
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            print(f"{subindent}- {f}")

# Replace 'your_project_directory' with the path to your project directory
list_files(r'C:\Users\theal\PycharmProjects\ensembleLegends')
