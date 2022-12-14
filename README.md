# This is GeForce Linexp

Hello, and welcome! I created this repository to start developing an adaptation of (Windows application...) NVIDIA GeForce Experience to automate the process of updating my NVIDIA GTX on Ubuntu distribution.

> I hope it can be useful to you! 

## What this tool can do for now?

- Detect your NVIDIA Graphic Card and store some information about it **locally**.
- **Search**, **download** and **install** new drivers of your NVIDIA Graphic Card.

## Installation

First you have to install Python 3.8 or higher in your machine.

Clone this repository:
```
git clone https://github.com/Dracovanys/geforce-linexp.git
```

Install dependencies:
```
pip install -r requirements.txt
```

## Usage

On terminal, execute "app-term.py" python file:
```
python3 app-term.py
```
And wait for all verification steps complete their work.

![execution-complete](https://user-images.githubusercontent.com/62522345/188321851-0b7aa894-a0a0-4f71-9d0c-c04abd500c1c.png)

During this process, GeForce Linexp should give the following (not exactly) responses:
 - Your NVIDIA Graphic Card is up-to-date.
 - There is a new driver for your NVIDIA Graphic Card. (And start the process to download it and install it)
 - There isn't a Linux driver for your NVIDIA Graphic Card. (Very sad...)
 - This tool can't search drivers for your NVIDIA Graphic Card. (Too very sad...)

### Executing GeForce Linexp on background (startup)

To do this, you can use "linexp_notifier.py", execute it on a terminal just to check if a notification will appear.
```
python3 linexp_notifier.py
```
After executing it, you can check its options on "/data/notifierOptions.json" to deactivate/activate some options as you want:
 - download-now: After detect a new driver available for your NVIDIA Graphic Card, it'll download it before pop-up notification.
 - show-no-new-drivers-notification: You show a notification when "No new drivers" were found. I just created this option to check first script execution.

Now you can set "linexp_notifier.py" to run at startup. On Startup Applications Preferences, add an entry with this command:
```
python3 /path/to/geforce-linexp/linexp_notifier.py &
```
Then reboot your computer (I recommend to activate "show-no-new-drivers-notification" for this) to check if it'll run on system startup.

## Limitations and points to solve

 - This tool uses Selenium WebDriver to navigate in NVIDIA Official Website and search latest drivers but, unfortunalately, some NVIDIA Graphic Cards don't have "family" option to search on Drivers page (like GeForce 9 Series models) so I currently didn't think on a way to verify drivers to this models yet.

## Goals to achieve

### Update driver module

 - [x] Detect user's NVIDIA Graphic Card and search for new drivers to it.
	 - [x] Store user's NVIDIA Graphic Card information to improve verification time on next executions.
 - [x] Download and install new drivers for user's NVIDIA Graphic Card.
 - [ ] Present a visual UI to provides a friendly use of the tool.
 - [x] Run tool as a service to automatically search for new drivers.

### Games adjustment module

 - [ ] Get all Steam games installed on user's machine and store information about each one locally.