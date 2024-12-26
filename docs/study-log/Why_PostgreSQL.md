# Why did I chose PostgreSQL?

Before this project was conceived using mysql. But I would like to use somethig
that I've never used before, so I decided to change to PostgreSQL, little did I
know the trouble beyind that decision.

So I just simply started by installing (via docker) Postgres, and tchanan it
doesn't work... So my `init.sql` file was made for MySQL and I had to learn 
that Postgres and MySQL are different, they are like different cars with the 
same objective that is driving. Both of them, fundamentally, do the same thing
but they have some differences on how they manage the database and the sintax  
that you use to make those changes in the database... So I tried to learn a 
little bit of Postgres so that I could start my Postgres container with the 
database that I wanted. Aaaaaaaand it worked!

Now let's just run the program and see what happens! Oh no, it broke... I can't 
connect to the database, it says that it doesn't exist. I forgot to adapt my 
code so that I could connect to a Postgres database instead of a MySQL database
so let's make some changes... I'm using sqlalchemy and for what I understood 
I should keep that has is, but the engine that it's running its for mysql so 
let's study a little bit and check what's the correct setup to connect to a 
postgres database via sqlalchemy. For that, when creating the engine, I had to 
use `postgresql` and `psycopg2` #7a763ee. Aaaaaaand it worked I can connect to 
the database.

But now I have to review how I use the sqlalchemy, I don't understand what I've 
done anymore. I'm already reading the documentation and will do a rework on the 
way I use the sqlalchemy library.
