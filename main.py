from utils.file_sorter import sort_files
from utils.report_generator import generate_report
import os

def main():
    folder_path = input("Enter the path of the folder to organize: ")
    
    if not os.path.exists(folder_path):
        print("Folder does not exist.")
        return
    
    sorted_files = sort_files(folder_path)
    generate_report(sorted_files, folder_path)
    print("Folder organized successfully!")

if __name__ == "__main__":
    main()

