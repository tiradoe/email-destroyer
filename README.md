# Email Destroyer

The script checks for a file named 'accounts.csv' (or a file that is provided using the -f flag) and deletes emails from the specified folders.
Each row of the CSV should have the following info (in this order):

host, email, password, folder, port


Example:

imap.gmail.com, email@gmail.com, password1, [Gmail]/Trash, 993


## Flags
--help, -h Show help info

--list, -l [filename] List available folders and exit. Takes in file location.

--file, -f [filename] Path to CSV file with accounts list.  If not provided, will default to 'accounts'csv.
