import sys
import os
import logger
import utility

def build(args):
    if not args:
        logger.log_error("No input folder specified for build.")
        sys.exit(1)

    input_folder = args[0]

    if len(args) > 2 and args[1] in ("-o", "--output"):
        output_folder = args[2]
    else:
        drive_root = os.path.splitdrive(os.path.abspath(input_folder))[0] + os.sep
        output_folder = os.path.join(drive_root, "out")

    if not os.path.isdir(input_folder):
        logger.log_error(f"Input folder does not exist: {input_folder}")
        sys.exit(1)

    try:
        config = utility.load_config(input_folder)
        base_url = config.get("base_url", "")
    except FileNotFoundError:
        logger.log_error(f"Configuration file 'config.json' not found in '{input_folder}'")
        sys.exit(1)
    except Exception as e:
        logger.log_error("Failed to load configuration")
        logger.log_error(str(e))
        sys.exit(1)

    if os.path.exists(output_folder):
        for fpath in utility.walk_files(output_folder):
            try:
                with open(fpath, 'r', encoding='utf-8') as f:
                    content = f.read()
                if base_url in content and '{{ base_url }}' not in content:
                    logger.log_warning(f"URL already configured: {base_url}")
                    logger.log_warning("Skipping build.")
                    return
            except:
                continue

    logger.log_success(f"Processing directory: {input_folder}")

    try:
        logger.log_success(f"Clearing folder: {output_folder}")
        utility.clean(output_folder)
    except Exception as e:
        logger.log_error(f"Failed to clean output folder '{output_folder}'")
        logger.log_error(str(e))
        sys.exit(1)

    skip_files = {"config.json"}
    try:
        for src_path in utility.walk_files(input_folder, skip_files=skip_files):
            rel_path = os.path.relpath(src_path, input_folder)
            dest_path = os.path.join(output_folder, rel_path)
            try:
                logger.log_rendering_file(rel_path)
                utility.copy_with_replacement(src_path, dest_path, base_url)
            except Exception as e:
                logger.log_error_rendering_file(rel_path, str(e))
    except Exception as e:
        logger.log_error("Error walking through input folder")
        logger.log_error(str(e))
        sys.exit(1)

    logger.log_success(f"URL configured: {base_url}")
    logger.log_success("Build process completed successfully.")
