# Homie Bot

A Personal Assistant Bot (Built using a Raspberry Pi) that can find missing items in a room just by Voice Commands. It can also update you with News, Weather, Send Mails etc.

## Getting Started

### Prerequisites
* Raspberry Pi 3
* Webcam
* Ultrasonic Sensor
* OpenCV Python
* Python 3.x

## Working
A predefined dataset of Images has to be provided to the Bot. Upon a voice command, the bot collects all the images of the object that the user wishes to find and then using Feature Matching (implemented in OpenCV Python), the bot looks around the room for the item with the highest percentage matching with the dataset provided.

At an average, the bot takes around 3-4 minutes to find the desired object.

## Additional Features
* Send Mail (by voice commands)
* Current Temperature (Scraped based on the place the User says)
* Latest News Updates (Scraped from Google News Results)
* Tell Jokes when you ask for them ;)
