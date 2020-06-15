from random import randint, choice
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from post.models import Post



def population(num_users):
    """ The Population function accepts int and returns None.
    """
    print(f"\nPOPULATION {'='*62}\n")
    
    users = list(range(1, num_users+1))
    for u in users:
        user = User.objects.create(
            username=f'user{u}',
            email=f'user{u}@generation.com'
        )
        user.set_password("secret")
        user.save()
        Token.objects.get_or_create(user=user)
        user_token = Token.objects.get(user=user)
        print(user.username, "password: 'secret', token:", user_token.key)
    print(len(users), 'new users was created.')



def posting(max_posts):
    """ The Posting function accepts int and returns None.
    """
    print(f"\nPOSTING {'='*65}\n")
    
    for user in User.objects.all():
        random_posts = range(1, randint(1, max_posts)+1)
        for p in random_posts:
            post = Post.objects.create( 
                owner=user, 
                title=f'Title_{user.username}_post{p}', 
                content=f'Content_{user.username}_post{p}'
            )
        user_posts = [post.id for post in Post.objects.filter(owner=user.id)]
        print(user.username, 'has', len(user_posts), 'posts, id:', sorted(user_posts))



def liking(max_likes):
    """ The Liking function accepts int and returns None.
    """
    print(f"\nLIKING {'='*66}\n")
    
    for user in User.objects.all():
        l = randint(1, max_likes)
        user_liked = []
        while (l > 0):
            post = choice(Post.objects.all())
            if user not in post.liked.all():
                post.liked.add(user)
                user_liked.append(post.id)
            l -= 1
        print(user.username, 'liked', len(user_liked), "posts, id:", sorted(user_liked))
    
    print(f"\n{'='*73}\n")    



def parsing(path):
    """ The Parsing function accepts a file and returns list.
    """
    with open(path, 'rt', encoding='UTF-8') as f:
        lst = [ int(line.split()[2]) for line in f.readlines() ]
        num_users, max_posts, max_likes = lst
        print(messages['DEFAULT_CONFIG'])
        print(
            '\nnumber_of_users =', num_users,
            '\nmax_posts_per_user =', max_posts, 
            '\nmax_likes_per_user =', max_likes, 
        )
    return(lst)



messages = {
    "GREETING": """ 
        You have launched AUTOBOT.\n
        It will help you quickly fill this prototype of a simple Social Network
        with users, posts and likes according to the config-file.
    """,
    'INFO' : """
        AUTOBOT is designed for one-time population of an existing database.
        The best AUTOBOT results are achieved by running it
        on a newly created database -- without any users and posts.

        Restarting AUTOBOT on the same database will be canceled. 
        If you need to use it again, you have to create a new database. 
        Be CAREFUL! If your database contains important data
        - first archive it before deleting.
         
        For run AUTOBOT just do all these steps in command line:
    """,
    'STEPS' : """
        1) make sure your 
            - virtual environment is activated.
            - current folder is the same where your "manage.py" file is.
        2) stop your development Server and/or InteractiveConsole: CTRL+C, CTRL+Z.
        3) for create a new database:
            - archive your database (if it contains important data)
            - delete your old database file: "db.sqlite3".
        4) create a new database: "python manage.py migrate".
        5) run AUTOBOT: "python autobot.py".
    """,
    'TIP' : """
        Before starting AUTOBOT, you can change the file: "default_config.txt"
        in .../media/default/ folder.
    """,
    'PROMT' : """
        To CONTINUE -- press 'Y' key and then press ENTER',
        To EXIT     -- just press ENTER'.
    """,
    'CANCEL' : """
        You have CANCELED the launch of this bot.\n
    """,
    'DEFAULT_CONFIG' : """
        CONFIG FILE EXISTS
        The default configuration will be used.
    """,
    'FILE_NOT_EXISTS' : """
        CONFIG FILE ISN'T EXIST
        This bot didn't find a configuration file,
        so its launch was CANCELED.

        The file: "default_config.txt" must be in .../media/default/ folder.
    """,
    'FORGOT' : """
        WARNING
        Maybe you forgot to delete the database or
        execute the command: "python manage.py migrate" after deletion.\n
        Don't worry. Just do all these steps again:
    """,
    "ERROR" : """
        SOMETHING WENT WRONG
        Please read the instructions carefully again.
    """,
    "DONE" : """
        CONGRATULATIONS

        AUTOBOT has successfully completed its work!\n
        And now, you can execute the following commands: 
        - "python manage.py createsuperuser".
        - "python manage.py runserver"
    """,
}