import os
import shutil
import json
import logger

def copy_with_replacement(src, dst, base_url):
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    try:
        with open(src, 'r', encoding='utf-8') as f:
            content = f.read()
        content = content.replace('{{ base_url }}', base_url)
        with open(dst, 'w', encoding='utf-8') as f:
            f.write(content)
    except Exception:
        shutil.copy2(src, dst)

def clean(path, recreate=True):
    if os.path.exists(path):
        shutil.rmtree(path)
    if recreate:
        os.makedirs(path)

def walk_files(src_dir, skip_files=None):
    skip_files = set(f.lower() for f in (skip_files or []))
    for root, dirs, files in os.walk(src_dir):
        hidden_dirs = [d for d in dirs if d.startswith('.')]
        for d in hidden_dirs:
            rel_path = os.path.relpath(os.path.join(root, d), src_dir)
            logger.log_warning(f"Skipped hidden folder: {rel_path}")
        dirs[:] = [d for d in dirs if not d.startswith('.')]

        for file in files:
            if file.startswith('.'):
                rel_path = os.path.relpath(os.path.join(root, file), src_dir)
                logger.log_warning(f"Skipped hidden file: {rel_path}")
                continue
            if file.lower() in skip_files:
                rel_path = os.path.relpath(os.path.join(root, file), src_dir)
                logger.log_warning(f"Skipped file: {rel_path}")
                continue
            yield os.path.join(root, file)

def load_config(input_folder):
    config_path = os.path.join(input_folder, 'config.json')
    with open(config_path, 'r', encoding='utf-8') as f:
        return json.load(f)
