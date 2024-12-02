import os

def get_file_structure(root_path):
    file_structure = {}
    for dirpath, dirnames, filenames in os.walk(root_path):
        for name in dirnames + filenames:
            path = os.path.join(dirpath, name)
            relative_path = os.path.relpath(path, root_path)
            try:
                size = os.path.getsize(path)
                file_structure[relative_path] = size
            except Exception as e:
                pass  # Ignora erros de permissão ou arquivos inacessíveis
    return file_structure

def format_size(size):
    units = ['B', 'K', 'M', 'G', 'T']
    index = 0
    while size >= 1024 and index < len(units)-1:
        size /= 1024
        index += 1
    if units[index] == 'B':
        return f"{size:.0f}{units[index]}"
    else:
        return f"{size:.1f}{units[index]}"

def print_structure(unique_files):
    for path in sorted(unique_files):
        size = unique_files[path]
        indent_level = path.count(os.sep)
        indent = '    ' * indent_level
        print(f"{indent}[{format_size(size):>4}]  {os.path.basename(path)}")

def main():
    sda2_path = '/mnt/sda2'
    nvme_path = os.getcwd()

    sda2_files = get_file_structure(sda2_path)
    nvme_files = get_file_structure(nvme_path)

    unique_files = {path: size for path, size in sda2_files.items() if path not in nvme_files}

    print("Arquivos únicos em /mnt/sda2:")
    print_structure(unique_files)

if __name__ == "__main__":
    main()
