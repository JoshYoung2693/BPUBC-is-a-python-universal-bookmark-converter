# Import the sqlite reader, and an os reader
import sqlite3, os
from sqlite3 import Error
filepath = input('what is the path to your ".db" file?')

# Create a connection to the .db bookmark file
def create_connection(db_file):
    """ create a database connection to a SQLite database """
    # Conn will contain all of the contents of the bookmark file
    conn = None
    # This is a try, to verify the input
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
    return conn

# Add all of the links and link titles to lists
def make_new_lists(conn):
    # Initialize the url list
    url_list  = []
    # Initialize the Name list
    names_list = []
    # I don't really understand this, but it is important
    cur = conn.cursor()
    # Open the bookmark directory of the .db file
    cur.execute("SELECT * FROM bookmarks")
    # Grab every link from it all at once
    rows = cur.fetchall()
    # Iterate through all of the rows in the table
    for row in rows:
        # Add to the list of URL's
        url_list.append(row[2])
        # Add to the list of names
        names_list.append(row[1])
    # Return the two lists
    return(url_list, names_list)

# Find a name that doesn't have any conflicts
def find_a_new_name_for_the_html():
    new_name = 'bookmarks.html'
    file_number = 0
    repeat = True
    # It will iterate through different potential names, until it finds an unused one.
    while repeat:
        if os.path.exists(new_name):
            new_name = 'bookmarks'+str(file_number)+'.html'
            repeat = True
            file_number += 1
        else:
          repeat = False
    return new_name

# Make the Netscape HTML file
def make_the_html(url_list, names_list, new_name):
    # Make the file with the new name
    f = open(new_name, 'x')
    # Write in the netscape header
    f.write('''<!DOCTYPE NETSCAPE-Bookmark-file-1>
<META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=UTF-8">
<TITLE>Bookmarks</TITLE>
<H1>Bookmarks</H1>
<DL><p>''')
    # Iterate through all of the url's and names
    for i, j in zip(url_list, names_list):
        f.write('<DT><A HREF="'+i+'" ICON="">'+j+'</A>\n')
    f.write('</DL><p>')

# The main program, the weird if is the from SQLite website
if __name__ == '__main__':
    conn = create_connection(filepath)
    url_list, names_list = make_new_lists(conn)
    new_name = find_a_new_name_for_the_html()
    make_the_html(url_list, names_list, new_name)
    print('Your bookmark file has been saved. :)')
