import os
from pathlib import Path

def get_size_str(size):
    return f"[{size/1024:.1f}K]" if size >= 1024 else f"[{size:4d}]"

def get_file_info(path):
    files_dict = {}
    for root, _, files in os.walk(path):
        for file in files:
            full_path = os.path.join(root, file)
            try:
                if os.path.islink(full_path):
                    continue
                rel_path = os.path.relpath(full_path, path)
                size = os.path.getsize(full_path)
                files_dict[rel_path] = size
            except (OSError, PermissionError):
                continue
    return files_dict

def write_tree(files_dict, output_file):
    with open(output_file, 'w', encoding='utf-8') as f:
        current_path = []
        for filepath in sorted(files_dict.keys()):
            parts = filepath.split(os.sep)
            
            # Compare current path with new path to determine common prefix
            for i, (current_dir, new_dir) in enumerate(zip(current_path, parts[:-1])):
                if current_dir != new_dir:
                    current_path = current_path[:i]
                    break
            
            # Add new directories that aren't in current path
            while len(current_path) < len(parts) - 1:
                dir_to_add = parts[len(current_path)]
                f.write('    ' * len(current_path) + dir_to_add + '\n')
                current_path.append(dir_to_add)
            
            # Write file with size
            size_str = get_size_str(files_dict[filepath])
            indent = '    ' * len(parts[:-1])
            f.write(f"{indent}{size_str:>8}  {parts[-1]}\n")

def main():
    sda2_path = "/mnt/sda2"
    nvme_path = "/"
    
    print("Coletando informações dos arquivos...")
    sda2_files = get_file_info(sda2_path)
    nvme_files = get_file_info(nvme_path)
    
    # Encontra arquivos únicos em cada diretório
    sda2_only = {k: v for k, v in sda2_files.items() if k not in nvme_files}
    nvme_only = {k: v for k, v in nvme_files.items() if k not in sda2_files}
    
    print("\nGerando arquivos de diferenças...")
    write_tree(sda2_only, '/home/borg/Desktop/salva_dif/sda2_only.txt')
    write_tree(nvme_only, '/home/borg/Desktop/salva_dif/nvme_only.txt')
    print(f"Arquivos únicos em sda2: {len(sda2_only)}")
    print(f"Arquivos únicos em nvme: {len(nvme_only)}")

if __name__ == "__main__":
    main()