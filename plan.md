Here's the plan:

1. We pass consumer key, secret, callback_url and frontend_callback_url as parameter to the api
2. The api does the twitter auth redirect for us, gets the tokens for us, basically does everything for us and ask for a frontend url to redirect to in order to give us the tokens
