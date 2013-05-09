This is the code that people used to get an invitation to Twilio's SxSW party.

To use:
 1. Put a real value for MONGO_URL in the '.env.sample' file
 2. Rename '.env.sample' to '.env'
 3. Run tests with "nosetests"
 4. Run the app with "python app.py"

To deploy to Heroku:
 1. heroku create
 2. heroku config GAME_PASSWORD=<a password>
 3. heroku config DEFAULT=start
 4. heroku config MONGO_URL=<valid mongodb url>
 5. git push heroku master
 6. heroku open