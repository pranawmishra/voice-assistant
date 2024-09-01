# Setup Instructions

Before running the main.py script, ensure that all necessary secret keys are added to the configuration files located in the **src/config/** directory. Follow the steps below:

**1. Add Secret Keys:** <br>
    1.1.Create a virtual environment and install all the modules in **requirements.txt**<br>
    1.1.Navigate to the **src/config/ directory**.<br>
    1.2.Add all required secret keys to the appropriate configuration files.<br>
   
**2: Set Up the Application and Tunneling**<br>
2.1. Execute the Application
Once the secret keys have been added:<br>

Execute the **app.py** script to run the Deepgram integration with Twilio.<br>
Alternatively, run **app_twilio.py** for Twilio's built-in speech-to-speech integration.<br>
**2.2. Install ngrok**<br>
Visit the ngrok website to download and install ngrok. This tool will help in setting up a tunnel to expose your localhost URL to a public URL.<br>

**2.3. Run ngrok**<br>
Once ngrok is set up, execute the following command in your terminal to start the tunnel:

**ngrok http 5000**<br>
Here, 5000 is the port number to bind your localhost to a public URL where all of your Twilio calls will be routed.<br>

**3. Interact with the Agent**<br>
After setting up the ngrok tunnel, you will be able to interact with the Agent through the provided public URL.<br>
