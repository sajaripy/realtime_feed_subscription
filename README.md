# realtime_feed_subscription
 realtime feed subscription

Implemented features:
1. User Authentication: Users can register and log in and logout from the application.

2. Subscription: Upon logging in, users can subscribe to a channel group to receive live feed updates. Subscribed user's info gets stored in UserSubscription model thus in feed_subscription_usersubscription table.

3. WebSocket Integration: Used Daphne, which is the ASGI server used by Django Channels to handle WebSocket connections and send live feed messages to subscribed users.

4. Scalability: Implemented throttling to handle large number of concurrent users
subscribing to the feed. for ex: Page will redirect if refreshed for 10 times in a minute and will wait for a minute to go back when refreshed.

To run the project:
=> Move to the realtime_feed_subscription project directory containing manage.py
=> activate pipenv using command: pipenv shell
=> Install dependencies: 1. pip3 install django
                      2. pip3 install djangorestframework
                      3. pip3 install channels
                      4. pip3 install websocket-client
                      5. python -m pip install -U channels["daphne"]

If you want to use Channels only and not Daphne:
pip3 install channels==3.0.4
pip3 install django==4.0.0
These two versions are compatible with each other

=> run migrations: python manage.py makemigrations
                python manage.py migrate

=> run the server: python manage.py runserver

=> Use credentials if you don't want to register: username: sajari2 
                                               password: Sasa@1499

=> Click on subscribe to receive the live feed data.
