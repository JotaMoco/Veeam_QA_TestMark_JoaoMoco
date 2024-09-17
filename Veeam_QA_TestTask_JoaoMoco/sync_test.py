# Veeam QA test task made by João Moço

# Libraries needed
import os
import shutil
import time
import logging
import hashlib
import argparse
from pathlib import Path

# Function that calculates the MD5 checksum of a file
def md5_calc(file_path):
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

# Function that synchronizes the source and replica folders
def folder_sync(source, replica, logger):
    # File sync process
    for root, dirs, files in os.walk(source):
        rel_path = os.path.relpath(root, source)
        replica_root = os.path.join(replica, rel_path)
        os.makedirs(replica_root, exist_ok=True)
        logger.info(f"Synchronization process started;")
        # Copy new or changed files
        for file in files:
            source_file = os.path.join(root, file)
            replica_file = os.path.join(replica_root, file)
            
            if not os.path.exists(replica_file) or md5_calc(source_file) != md5_calc(replica_file):
                shutil.copy2(source_file, replica_file)
                logger.info(f"Copied/Updated file: {source_file} to {replica_file};")
        
        # Remove files in replica that are not in source
        for file in os.listdir(replica_root):
            if file not in files:
                os.remove(os.path.join(replica_root, file))
                logger.info(f"Removed file: {os.path.join(replica_root, file)};")

# Function to set up logging to file and console
def setup_logger(log_file):
    logger = logging.getLogger('sync_logger')
    logger.setLevel(logging.INFO)
    
    # File handler
    fh = logging.FileHandler(log_file)
    fh.setLevel(logging.INFO)
    
    # Console handler
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    
    # Formatter
    formatter = logging.Formatter('%(asctime)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    
    # Add handlers to the logger
    logger.addHandler(fh)
    logger.addHandler(ch)
    
    return logger

# Main function
def main():
    # Variable definition
    local_time1 = time.strftime("%d-%m-%Y_%H-%M-%S")

    # CLI Interface
    parser = argparse.ArgumentParser(description="Folder Synchronization Tool")
    parser.add_argument('--source', required = True, help="Path to the source folder")
    parser.add_argument('--replica', required = True, help="Path to the replica folder")
    parser.add_argument('--interval', required = False, default=60, type=int, help="Sync interval in seconds")
    parser.add_argument('--cycles', required = False, default= 1, type=int, help="Amount of synchronization cycles")
    args = parser.parse_args()

    source = args.source
    replica = args.replica
    interval2 = args.interval
    cycles = args.cycles

    # Validate paths
    if not os.path.isdir(source):
        print(f"Error: Source folder '{source}' does not exist.")
        return
    if not os.path.exists(replica):
        os.makedirs(replica)
    
    # Log file path and name
    log_path = Path.cwd()
    log_name = f"log_{local_time1}.txt"
    log_file = log_path/log_name

    logger = setup_logger(str(log_file))

    # Warn user of log file path
    print(f"Log file '{log_name}' registered @ '{str(log_file)}'")
    
    # Cycle limiter 
    for i in range(cycles):
        folder_sync(source, replica, logger)
        logger.info(f"Cycle {i + 1} completed. Next sync in {interval2} seconds.")
        time.sleep(interval2)  # Wait for the next cycle
    
    # Warn user that proces is over
    logger.info("Synchronization process completed.")


if __name__ == "__main__":
    main()