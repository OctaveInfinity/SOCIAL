import django
from django.db.utils import OperationalError, IntegrityError
from django.conf import settings
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "social_project.settings")
django.setup()

from helper import (
                    User, 
                    Post, 
                    parsing, 
                    population, 
                    posting, 
                    liking, 
                    messages,
                    )


# Greeting and information
print(
      messages['GREETING'],
      messages['INFO'],
      messages['STEPS'],
      messages['TIP']
      )

# Continue or cancel
promt = input(messages['PROMT'])
if promt != 'Y':
    print(messages['CANCEL'])
else:
    
    # Check if database exists and fresh
    try:
        test_user = User.objects.create(username=f'user0')
        User.objects.get(username=f'user0').delete()

    except (OperationalError, IntegrityError):
        print(messages['FORGOT'],
              messages['STEPS'],
              messages['TIP']
              )

    else:

        # Check if configuration file exists
        try:
            path = settings.MEDIA_ROOT + '/default/default_config.txt'
            with open(path, 'rt', encoding='UTF-8') as f:
                pass

        except:
            print(messages['FILE_NOT_EXISTS'])

        else:
            # Try to do our job
            try:
                lst = parsing(path)
                num_users, max_posts, max_likes = lst
                
                population(num_users)
                posting(max_posts)
                liking(max_likes)
                
            except Exception as e:
                print(f"We've catched: {str(e)}")
                print(messages['ERROR'],
                        messages['FORGOT'],
                        messages['STEPS'],
                        messages['TIP']
                        )
            else:
                print(messages['DONE'])
