import os
import http.server
import socketserver
import utility
import logger

def serve(args):
    input_folder = os.path.abspath(args[0]) if args else os.getcwd()

    if not os.path.isdir(input_folder):
        logger.log_error(f"Input folder does not exist: {input_folder}")
        return

    drive_root = os.path.splitdrive(input_folder)[0] + os.sep
    tmp_dir = os.path.join(drive_root, ".serve")

    try:
        if os.path.exists(tmp_dir):
            utility.clean(tmp_dir)
        else:
            os.makedirs(tmp_dir)
        if os.name == 'nt':
            os.system(f'attrib +h "{tmp_dir}"')
    except Exception as e:
        logger.log_error("Failed to prepare .serve folder")
        logger.log_error(str(e))
        return

    logger.log_success("Clearing folder: .serve")
    logger.log_success(f"Processing directory: {input_folder}")

    base_url = "http://localhost:8000/"
    skip_files = {"config.json"}

    for src_path in utility.walk_files(input_folder, skip_files=skip_files):
        rel_path = os.path.relpath(src_path, input_folder)
        dst_path = os.path.join(tmp_dir, rel_path)
        try:
            logger.log_rendering_file(rel_path)
            utility.copy_with_replacement(src_path, dst_path, base_url)
        except Exception as e:
            logger.log_error_rendering_file(rel_path, str(e))

    os.chdir(tmp_dir)
    handler = http.server.SimpleHTTPRequestHandler

    with socketserver.TCPServer(("", 8000), handler) as httpd:
        try:
            logger.log_success(f"Starting server on {base_url}")
            httpd.serve_forever()
        except KeyboardInterrupt:
            logger.log_success("Keyboard interrupt received, shutting down server.")
            httpd.shutdown()
            httpd.server_close()
            try:
                os.chdir(input_folder)
                utility.clean(tmp_dir, recreate=False)
                logger.log_success("Removed folder: .serve")
            except Exception as e:
                logger.log_error(f"Failed to clean .serve folder: {e}")
