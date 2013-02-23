Call To Action: Text “Party” to [xxx-xxx-xxxx]

[voice also?]

* Must get all questions correctly to receive link and password.
* Password should be updated every 3-5 days depending on the increase of rsvps we see
* Easily updated in Eventbrite

From the perspective of an attendee:
* Sees a phone number on:
  * Twilio landing page
  * Twilio blog
  * Twitter/Facebook
  * Partner promotions (Github, Mashery, etc)
* User plays game (see below)
* User visits our Eventbrite, enters password, cancels unicorn ride

From the perspective of the Twilio person running this:
* It's time for a password change!
  * Twilio Person visits Eventbrite, updates password
  * Twilio Person coordinates with Joel to update app password


Party-seeker Texts “Party” to [xxx-xxx-xxx] or Dials [xxx-xxx-xxx]

-----
intro
-----
1st response:
[SMS] You are planning your trip to SxSW 2013 and see there is a rocking party on the agenda for the Twilio community. To get on the RSVP list, you realize you must answer three questions correctly to prove your cloud communications street cred. Do you accept this challenge? Respond Y/N

[SMS 140]
To get on the list for Twilio's SxSW party, you must answer three questions to prove your Twilio street cred. Do you accept this challenge?

[Voice] You are planning your trip to SxSW 2013 and see there is a rocking party on the agenda for the Twilio community. To get on the RSVP list, you realize you must answer three questions correctly to prove your cloud communications street cred. Do you accept this challenge? 

<Say> Press 1 to accept</Say>
<Say> Press 2 to decline</Say>

If Respond N:
Sorry to see you go! Make sure to follow @twilio on Twitter for updates around SxSW 2013. 
_____________________

If Respond Y:
[SMS] Challenge accepted. Answer this correctly to proceed. Which TwiML verb ends a call? 

[Accepted Responses]
Hangup
Hang up
<Hangup>


-----
part1
-----
[Voice] Challenge accepted. Answer this correctly to proceed. Which Twilio TwiML verb ends a call? 

<Say>Press 1 for Reject</Say>
<Say>Press 2 for Hangup</Say>
<Say>Press 3 for Leave</Say>

________________________


If Respond Incorrectly:
Unfortunately, that is incorrect but never fear! You can start from the beginning to try again. Dial [xxxxxxxxx] or text Party to [xxxxxxxxxx]

If Respond Correctly:
-----
part2
-----
[SMS] Well party-seeker, you proved you know your TwiML but in order to gain access you must answer two more questions. In what year was Alexander Graham Bell awarded the patent for the telephone?

[SMS 140]
You have two questions remaining: In what year was Alexander Graham Bell awarded the patent for the telephone? 

[Accepted Responses]
1876

[Voice] Well party-seeker, you proved you know your TwiML but in order to gain access you must answer two more questions. In what year was Alexander Graham Bell awarded the patent for the telephone? 

<Say>Press 1 for 1876</Say>
<Say>Press 2 for 1875</Say>
<Say>Press 3 for The patent is actually held by Elisha Gray</Say>

__________________________

If Respond Incorrectly:
Oh no, so close, but that in incorrect. Fear not! You can start from the beginning to try again. Dial [xxxxxxxxx] or text Party to [xxxxxxxxxx]

-----
part3
-----
If Respond Correctly:
[SMS] So party-seeker, you hold knowledge of telephony history alongside the Twilio API. You are just one question away from receiving the password.  

[SMS 140]
You're one question away! When initially testing your very first Twilio app, what phrase is used to verify it is working correctly? 

[Voice] So party-seeker, you hold knowledge of telephony history alongside the Twilio API. You are just one question away from receiving the password.  

If Respond Incorrectly:
Oh no, so close, but that in incorrect. Fear not! You can start from the beginning to try again. Dial [xxxxxxxxx] or text Party to [xxxxxxxxxx]

If Respond Correctly:
-----
end
-----
[Voice+SMS] Congratulations, you have proven your alliance to cloud communications and we’d be honored to have you attend our SxSW private event. We will follow up with a link and password to register. Make sure to follow @twilio on Twitter for daily updates. 

[SMS 140]
Congratulations, we’d be honored to have you at our party. Register at: http://twiliosxsw2013.eventbrite.com with password: BBQisdelicious

--->Send SMS with link and password


Notes:

Write code in a way that makes it easy to switch out the text with voice files that Murphy will provide.

Build in a “shortcut mode” that we can enable if it’s looking like people aren’t going through the process.

