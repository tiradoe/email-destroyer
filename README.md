# email-destroyer
Blow those emails away, one account at a time.

The script checks for a file named 'accounts.csv' and deletes emails from the specified folders.
Each row of the CSV should have the following info (in this order):
host, email, password, folder, port


Example:
imap.gmail.com, email@gmail.com, password1, [Gmail]/Trash, 993
