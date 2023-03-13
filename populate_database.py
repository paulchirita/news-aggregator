import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "newsaggregator.settings")
import django
django.setup()
from mainApp.models import NewsWebsite, Topic, Article, AppUser

# AppUser.objects.all().delete()
# Article.objects.all().delete()
# Topic.objects.all().delete()
# NewsWebsite.objects.all().delete()

user1 = AppUser(email="example_user@mail.com", first_name="example", last_name="user", password="12345",
                username="example")
user1.save()
user2 = AppUser(email="test@mail.com", first_name="test", last_name="test", password="12345",
                username="test")
user2.save()

website1 = NewsWebsite(name="CNN", url="https://cnn.com")
website1.save()
website2 = NewsWebsite(name="NOS", url="https://nos.nl")
website2.save()

topic1 = Topic(name="politics")
topic1.save()
topic2 = Topic(name="sports")
topic2.save()
topic3 = Topic(name="technology")
topic3.save()

article1 = Article(title="Football WC", newsWebsite=website1,
                          articleText="The football world cup is starting today.",
                          topic=topic2)
article1.save()
article2 = Article(title="New Cryptocoin", newsWebsite=website2,
                          articleText="A new crypo coin has been launched",
                          topic=topic3)
article2.save()

user1.savedArticles.add(article1)
user1.preferredTopics.add(topic1, topic2)
user1.preferredNewsWebsites.add(website1)

user2.savedArticles.add(article2)
user2.preferredTopics.add(topic3)
user2.preferredNewsWebsites.add(website2)
