import os # Common Operating System Interactions
import zipfile # Work with ZIP Files
import glob # File Pathname Module
from datetime import datetime # Convert UNIX Timestamp of Files to DateTime
# Program Metadata
metadata = {
    "Author": "Jay Annadurai",
    "Title": "Canvas Unzipper",
    "Version": 1
}

# Program Defaults
defaults = {
    "File": "submissions",
    "Windows": {
        "Download Folder Path": "C:\\Users\\ajaya\\Downloads",
        "Destination Folder Path": "C:\\Users\\ajaya\\Documents\\Informatics\\Projects\\TA\\FA23\\I211"
    },
    "MacOS": {
        "Download Folder Path": "C:\\Users\\ajaya\\Downloads",
        "Destination Folder Path": "C:\\Users\\ajaya\\Documents\\Informatics\\Projects\\TA\\FA23\\I211"
    }
}

# Helper Function 1: Navigate to a directory
def dirNavigate(directoryPath, purpose=""):
    """
    directoryPath: str - The path to the desired directory
    purpose: str - The purpose of navigation to use in error messages
    """
    try:
        # Debug77
        # print(f"Trying to navigate to: {directoryPath} for {purpose}")
        os.chdir(directoryPath)
    except Exception:
        raise Exception(f"Invalid {purpose} Directory Path") from None

# Helper Function 2: Navigate to or create directories in sequence
def dirUseOrCreate(directoryPath, directoryNames):
    """
    directoryPath: str - The path to the starting directory
    directoryNames: list - A list of directory names to navigate to or create in sequence
    return: str - The final path navigated to
    """
    dirNavigate(directoryPath, purpose="Root Export")
    for dirName in directoryNames:
        if not os.path.exists(dirName):
            print(f"Notice: Creating Directory '{dirName}' within '{os.getcwd()}'!")
            try:
                # Try Creating the Directory
                os.mkdir(dirName)
            except Exception:
                raise Exception(f"Export Folder '{dirName}' unable to be created") from None
        os.chdir(dirName)
    return os.getcwd()

# Helper Function 3: Recursively Unzip Folders in the Directories
def recursiveUnzip(directoryPath):
    """
    directoryPath: str - The path to start the recursive unzip
    """
    dirNavigate(directoryPath, purpose= "Recursive Unzip")
    zipFiles = glob.glob("*.zip")

    for zipFile in zipFiles:
        # Get the Absolute Path to the Zipfile First
        zipFilePath = os.path.abspath(zipFile)
        # Extract the zip file name without the .zip extension
        newFolderPath = os.path.splitext(zipFilePath)[0]
        # print(f"Debug: Folder Path: {newFolderPath}")

        if not os.path.exists(newFolderPath):
            os.mkdir(newFolderPath)

        with zipfile.ZipFile(zipFile, 'r') as zip_ref:
            zip_ref.extractall(newFolderPath)

        # Now recursively unzip inside this directory
        recursiveUnzip(newFolderPath)

        # Delete the original zip file
        # But first go up one directory back to the Entire Export Directory
        os.chdir("..")
        os.remove(zipFile)

# Function 1: Import a ZIP file
def zipImport(directoryPath, fileName):
    """
    directoryPath: str - The path to look for the zip file
    fileName: str - The name to look for within the zip files
    return: str - Absolute path to the zip file found
    """
    dirNavigate(directoryPath, purpose="Import")
    files = glob.glob(f"*{fileName}*.zip")

    if not files:
        raise Exception("No Zip Files found!")
    elif len(files) > 1:
        print(f"\nWarning: {len(files)} Files found...")
        # Sort by most recently modified
        files.sort(key=lambda x: os.path.getmtime(x), reverse=True)
        # Indicate to the User the Multiple Files
        for file in files:
            modificationTimeStamp = os.path.getmtime(file)
            modificationDateTime = datetime.fromtimestamp(modificationTimeStamp)
            print(f'{file} - {modificationDateTime}')
        print(f"\nUsing the Most Recent File: {files[0]} \n")

    return os.path.abspath(files[0])

# Function 2: Extract contents of a ZIP file
def zipExport(directoryPath, zipFile):
    """
    directoryPath: str - The path to extract the zip contents to
    zipFile: str - The zip file to extract
    """
    dirNavigate(directoryPath, purpose="ZIP Export")
    with zipfile.ZipFile(zipFile, 'r') as zip_ref:
        zip_ref.extractall(directoryPath)

# Function 2b: Recursively Extract all Zip Files
def zipExportRecursive(directoryPath, zipFile):
    zipExport(directoryPath,zipFile)

    # Now navigate inside the unzipped folder and continue the recursive unzip
    # exportDirectory = os.path.join(directoryPath, os.path.splitext(os.path.basename(zipFile))[0])

    recursiveUnzip(directoryPath)

# Main Script Functionality
if __name__ == "__main__":

    # Print a Welcome Message
    print(f'Welcome to {metadata["Title"]} V{metadata["Version"]} by {metadata["Author"]}')
    # Determine if OS is Mac/Win
    # Windows: os.name == 'nt'. Mac/Linux/BSD: os.name == 'posix'
    sysOS = "Windows" if os.name == "nt" else "MacOS"
    print(f'Detected Operating System: {sysOS}')

    # User Inputs
    # Organize Files by Module and Number
    moduleNumber = input("Module Number: ")
    assignmentName = input("Assignment Name: ")

    # If neither are provided, raise an error
    if not moduleNumber and not assignmentName:
        raise Exception("Too many empty inputs!")

    # Convert the Module Number to a Folder Name
    moduleStr = "M" + str(moduleNumber)

    # Ask the User if they'd like to use the Default Parameters
    inputUseDefaults = input("Use Default Import and Export Parameters? (True/False): ").lower()

    # Accept alternative True False responses from the useDefaults Input
    match inputUseDefaults:
        # User does not want defaults
        case 'false' | 'no' | '0' | 'n':
            useDefaults = False
        # User wants defaults
        case 'true' | 'yes' | '1' | 'y' :
            useDefaults = True

        # User does not specify
        case _ :
            useDefaults = True
            # Alternatively can raise an exception
            # raise Exception("Usage of Default Parameters unspecified")


    # Depending on whether the Use Defaults Flag is Enabled
    if useDefaults:
        # Use Default Parameters
        fileName = defaults["File"]
        importPath = defaults[sysOS]["Download Folder Path"]
        exportPath = defaults[sysOS]["Destination Folder Path"]
        recursiveZipExport = True
    else:
        # Ask for Parameter Inputs and if there is no input given, use the Defaults
        fileName = input("File Name (Default: submissions): ") or defaults["File"]
        importPath = input(f'Import Path (Default - {defaults[sysOS]["Download Folder Path"]}:') or defaults[sysOS]["Download Folder Path"]
        exportPath = input(f'Export Path (Default - {defaults[sysOS]["Destination Folder Path"]}:') or defaults[sysOS]["Destination Folder Path"]
        inputRecursiveZipExport = input("Recursively Unzip All? (True/False): ").lower()
        recursiveZipExport = False if inputRecursiveZipExport == 'false' else True

    # Define the New Directory Structure to Export/Unzip the Files to
    # Build an Array of only the existing Values
    directoryNames = [name for name in [moduleStr, assignmentName] if name]

    # Import the zipFile
    zipFile = zipImport(importPath, fileName)

    # Create or Identify the Directories to the Final Export Path
    finalExportPath = dirUseOrCreate(exportPath, directoryNames)

    # If the Recursive Export flag is enabled, use the Recursive Zip Export
    if recursiveZipExport:
        zipExportRecursive(finalExportPath, zipFile)

    # Else use the standard Zip Export
    else:
        zipExport(finalExportPath, zipFile)

    # Finally, Clean up the original Zip File
    # os.remove(zipFile)

    # Completion Message
    print('\nZIP Export successfully completed and original ZIP deleted =)')
    print(f'\nThanks for using {metadata["Title"]} by {metadata["Author"]}!')