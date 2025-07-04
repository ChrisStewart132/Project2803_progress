import os
import sys

def get_jpg_files(directory):
    """
    Walks through the specified directory and its subdirectories
    to find all JPG/JPEG files. Returns a sorted list of their absolute paths.
    """
    jpg_files = []
    print(f"Scanning directory: {os.path.abspath(directory)}")
    for root, _, files in os.walk(directory):
        for file in files:
            # Check for common JPG/JPEG extensions, case-insensitive
            if file.lower().endswith(('.jpg', '.jpeg', '.png')):
                full_path = os.path.join(root, file)
                jpg_files.append(os.path.abspath(full_path))
    
    # Sort the files alphabetically by their full path for consistent ordering
    jpg_files.sort()
    return jpg_files

def perform_renaming(files_to_rename, dry_run=True):
    """
    Performs the renaming operation based on the provided list of files.
    If dry_run is True, it only prints the actions.
    """
    if dry_run:
        print("\n--- DRY RUN: Proposed Changes (no files will be renamed) ---")
    else:
        print("\n--- RENAMING FILES (this may take a moment) ---")

    if not files_to_rename:
        print("No JPG/JPEG files found to rename.")
        return 0, 0 # Renamed, Failed

    renamed_count = 0
    failed_count = 0
    img_counter = 1

    for old_path in files_to_rename:
        # Get the directory of the original file
        parent_dir = os.path.dirname(old_path)
        
        # Construct the new filename
        if old_path.lower().endswith('.png'):
            new_basename = f"ss{img_counter}.png"
        else:
            new_basename = f"ss{img_counter}.jpg"
        new_path = os.path.join(parent_dir, new_basename)

        if old_path == new_path:
            print(f"Skipping: '{old_path}' is already named '{new_basename}'.")
            img_counter += 1
            continue

        if dry_run:
            print(f"  '{os.path.basename(old_path)}' -> '{new_basename}' (in '{parent_dir}')")
            renamed_count += 1 # Count for dry run summary
        else:
            try:
                # Check if the new name already exists and is a file
                # This prevents overwriting existing files that might not be part of the renaming batch
                if os.path.exists(new_path) and os.path.isfile(new_path):
                     # If the existing file is the one we're trying to rename, it's fine.
                     # Otherwise, it's a conflict.
                    if os.path.abspath(old_path) != os.path.abspath(new_path):
                        print(f"ERROR: Cannot rename '{os.path.basename(old_path)}' to '{new_basename}' because '{new_basename}' already exists and is a file. Skipping.")
                        failed_count += 1
                        img_counter += 1
                        continue

                os.rename(old_path, new_path)
                print(f"Renamed: '{os.path.basename(old_path)}' -> '{new_basename}'")
                renamed_count += 1
            except FileNotFoundError:
                print(f"ERROR: File not found - '{old_path}'. It might have been moved or deleted. Skipping.")
                failed_count += 1
            except PermissionError:
                print(f"ERROR: Permission denied - Cannot rename '{old_path}'. Skipping.")
                failed_count += 1
            except Exception as e:
                print(f"ERROR: Unexpected error renaming '{old_path}': {e}. Skipping.")
                failed_count += 1
        
        img_counter += 1

    if dry_run:
        print(f"\nDry Run complete. {renamed_count} files would be renamed.")
    else:
        print(f"\nRenaming complete. Successfully renamed {renamed_count} files, failed on {failed_count} files.")
    
    return renamed_count, failed_count

def main():
    print("--- JPG Renamer Script ---")
    print("This script will find all JPG/JPEG/PNG files in a directory (and subdirectories)")
    print("and rename them to 'ss1.jpg', 'ss2.jpg', etc., in their original locations.")
    
    target_directory = input(f"\nEnter the directory to process (default: '{os.getcwd()}'): ").strip()
    if not target_directory:
        target_directory = os.getcwd()
    
    if not os.path.isdir(target_directory):
        print(f"Error: Directory '{target_directory}' does not exist or is not a directory.")
        sys.exit(1)

    all_image_files = get_jpg_files(target_directory)

    if not all_image_files:
        print("\nNo JPG/JPEG/PNG files found in the specified directory or its subdirectories.")
        sys.exit(0)
    
    print(f"\nFound {len(all_image_files)} JPG/JPEG/PNG files.")

    # Perform dry run
    perform_renaming(all_image_files, dry_run=True)

    # Ask for confirmation
    confirm = input("\nDo you want to proceed with these changes? (type 'yes' to confirm): ").strip().lower()

    if confirm == 'yes':
        renamed, failed = perform_renaming(all_image_files, dry_run=False)
        print("\nOperation Summary:")
        print(f"Total files found: {len(all_image_files)}")
        print(f"Files successfully renamed: {renamed}")
        print(f"Files failed to rename: {failed}")
        print("\n--- Script Finished ---")
    else:
        print("\nOperation cancelled by user.")
        print("--- Script Finished ---")

if __name__ == "__main__": main()