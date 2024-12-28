# Changing project variable names and Database Tables names

## Table names
After reviewing some of the code, I arrived to the conclusion that I need to 
change the name of the variables and consecuently the name of the classes and 
sql tables. Right now, in the sql tables, it doesn't make sense because the 
names are not correct, for example:
    - `domain` should be named `onion_url` because in reallity we are talking, 
    about the onion url that contains the following components:
        - `Scheme` -> "http://"
        - `Host Name` that can be 6-character alphanumeric strings derived from 
        RSA keys or 56-character alphanumeric strings derived from Ed25519 keys, 
        offering better security 
        ex.:"torlinksge6enmcyyuxjpjkoouw4oorgdgeo7ftnq3zodj7g2zxi3kyd"
        - `Top Level Domain` -> ".onion"
    - So a full `onion_url` should be -> 
    "http://torlinksge6enmcyyuxjpjkoouw4oorgdgeo7ftnq3zodj7g2zxi3kyd.onion"
    - And if we are naming this to `onion_url` then the variable/table `link` 
    then it should be named `path` because it contains the path relative to 
    that specific `onion_url`.
    - I could optimize my database by separating every component of a .onion 
    url, I could separate it like this:
        - `protocol` (probably will always be http but there's a chance of 
        being https)
        - `onion_hostname`
        - `path`
    - There's also the `large_link` table, I think it should be named, at least 
    `large_url` becasue this table will store all the urls that are larger than 
    what I can download.
    - I should check why I have a `file` table. I don't remember why I have it 
    there. And also this `file` table is associated with the `domain` table, 
    shouldn't it be associated with the path table? Since the file is in a 
    specific path?
    - And at last, should I keep the hash of the onion url? I think I should 
    because of the future mongo database that will be used for storing the 
    content of the onion_urls. And like that we can cross reference the DBs.
