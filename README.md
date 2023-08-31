# Unzipper
Simple Python Script to assist in unzipping files from a ZIP file to a target destination and is capable of recursively unzipping any inner ZIP files as well. Designed with an emphasis on unzipping student program submissions, submitted as ZIP files themselives, from Canvas.

The program operates by scanning for the name of a given ZIP file in the immport directory path, selecting the most recent ZIP file, and then it extracts the file into a target directoy while cleaning up the ZIP files.
This program is designed to work in IT courses where submissions can be in the form of ZIP files, so it also has ZIP extraction recursion so all ZIP files within the original ZIP file are extracted.
The module number and assignment name are utilzied to organize the extracted files.

Lastly, the program allows for default settings which should be adjusted to the user to accelerate the unzipping workflow. 
