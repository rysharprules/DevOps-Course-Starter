# DevOps Apprenticeship: Project Exercise

## Getting started

The project uses a virtual environment to isolate package dependencies. To create the virtual environment and install required packages, run the following from a bash shell terminal:

### On macOS and Linux

```bash
$ source setup.sh
```

### On Windows

Git Bash:

```bash
$ source setup.sh --windows
```

PowerShell

```bash
$ ./setup --windows
```

### Environment variables

To run effectively, update the `.env` file with your application details:

1. `API_KEY` - Used to call the [Trello](https://developer.atlassian.com/cloud/trello/rest/api-group-actions/) API
1. `API_TOKEN` - Used to call the [Trello](https://developer.atlassian.com/cloud/trello/rest/api-group-actions/) API
1. `BOARD_ID` - An ID reference to the [board](https://developer.atlassian.com/cloud/trello/rest/api-group-boards/#api-boards-id-get) on Trello

### Run

Once the setup script has completed and all packages have been installed, start the Flask app by running:
```bash
$ flask run
```

You should see output similar to the following:

```bash
 * Serving Flask app "app" (lazy loading)
 * Environment: development
 * Debug mode: on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with fsevents reloader
 * Debugger is active!
 * Debugger PIN: 226-556-590
```

Now visit [`http://localhost:5000/`](http://localhost:5000/) in your web browser to view the app.

### Testing

#### Unit testing

To run unit tests use the command:

```bash
$ pytest .\tests\
```

#### Integration testing

You will need Firefox version 60+ to run these tests. [Download here](https://www.mozilla.org/en-GB/firefox/new/).

To run integration tests use the command:

```bash
$ pytest .\tests_e2e\
```

#### Statuses

This application relies on the existence of Lists on the Trello board named "`To Do`", "`Doing`", and "`Done`" (the default set). The code is extendable to use further lists by calling `statuses` directly from the `ViewModel` rather than the `board_statuses` subset (the default set) returned by `getBoardStatuses`. "`Done`" is still required to facilitate the `/complete/<id>` route. An alternative solution for this would be to simply set the "complete" item with the _last_ status in the list of statuses returned from Trello, e.g. `item['status'] = getStatuses()[-1].title`. Another solution would be to remove the route as the functionality to mark a task as "complete" is fulfilled by the drag and drop feature.

### Virtual environments

This application can also be run within a virtual machine (VM) by using [Vagrant](https://www.vagrantup.com/downloads.html).

Vagrant requires a hypervisor installed. This application is configured to use Windows [Hyper-V](https://docs.microsoft.com/en-us/virtualization/hyper-v-on-windows/about/). 

#### Setting up Hyper-V

1. Install Hyper-V
2. Add an external switch in Hyper-V Manager as per "Tip 1" in these [instructions](https://techcommunity.microsoft.com/t5/virtualization/vagrant-and-hyper-v-tips-and-tricks/ba-p/382373).
3. Virtualization needs to be turned on in the firmware. This must be done via the BIOS. This varies by machine but generally the steps are:
   1. Restart the system
   2. Press F2 (or alternate shown on screen) to enter BIOS
   3. Navigate to Advanced
   4. Select Virtualization Technology and then press the Enter key and select Enabled
   5. Escape and save

#### Run the application on the VM

To run the VM, run the following command as an admin:

`vagrant up`

You'll be asked to choose a switch to attach to the Hyper-V instance. Select the external switch created during the Hyper-V setup.

The machine will now report it's IP address. Take note of this as it will be used to access the application later.

The command may request your username and password. Enter your Windows credentials (the `@domain` is optional).

The Vagrantfile within this repo will:

- Pull down a Ubuntu Linux image to run the app
- Prep your VM for Python installation
- Install Python 3.6.6
- Install poetry and load any dependencies
- Launch the TODO app
  
Add the IP of the VM to your browser with the port of `5000` to see the TODO application.

##### Example output

````
Windows PowerShell
Copyright (C) Microsoft Corporation. All rights reserved.

Try the new cross-platform PowerShell https://aka.ms/pscore6

Hello and welcome to...
  _____                   _    	   _____ 		               _____ _          _ _ 
 |  __ \                 ( )      |  __ \                     / ____| |        | | |
 | |__) |   _  __ _ _ __ |/ ___   | |__) |____      _____ _ __ (___ | |__   ___| | |
 |  _  / | | |/ _` | '_ \  / __|  |  ___/ _ \ \ /\ / / _ \ '__\___ \| '_ \ / _ \ | |
 | | \ \ |_| | (_| | | | | \__ \  | |  | (_) \ V  V /  __/ |  ____) | | | |  __/ | |
 |_|  \_\__, |\__,_|_| |_| |___/  |_|   \___/ \_/\_/ \___|_| |_____/|_| |_|\___|_|_|
         __/ |                                                                     
        |___/                                                                      
Running in admin mode.
Loading personal and system profiles took 1300ms.
→ C:\WINDOWS\system32› proj devops
→ C:\projects\DevOps-Course-Starter [exercise-4 ≡ +4 ~3 -2 !]› vagrant up
Bringing machine 'default' up with 'hyperv' provider...
==> default: Verifying Hyper-V is enabled...
==> default: Verifying Hyper-V is accessible...
==> default: Importing a Hyper-V instance
    default: Creating and registering the VM...
    default: Successfully imported VM
    default: Please choose a switch to attach to your Hyper-V instance.
    default: If none of these are appropriate, please open the Hyper-V manager
    default: to create a new virtual switch.
    default:
    default: 1) External Switch
    default: 2) Default Switch
    default:
    default: What switch would you like to use? 1
    default: Configuring the VM...
    default: Setting VM Enhanced session transport type to disabled/default (VMBus)
==> default: Starting the machine...
==> default: Waiting for the machine to report its IP address...
    default: Timeout: 120 seconds
    default: IP: 192.168.0.74
==> default: Waiting for machine to boot. This may take a few minutes...
    default: SSH address: 192.168.0.74:22
    default: SSH username: vagrant
    default: SSH auth method: password
    default:
    default: Inserting generated public key within guest...
    default: Removing insecure key from the guest if it's present...
    default: Key inserted! Disconnecting and reconnecting using new SSH key...
==> default: Machine booted and ready!
==> default: Preparing SMB shared folders...
    default: You will be asked for the username and password to use for the SMB
    default: folders shortly. Please use the proper username/password of your
    default: account.
    default:
    default: Username (user[@domain]): Ryan
    default: Password (will be hidden):

Vagrant requires administrator access to create SMB shares and
may request access to complete setup of configured shares.
==> default: Mounting SMB shared folders...
    default: C:/projects/DevOps-Course-Starter => /vagrant
==> default: Running provisioner: shell...
    default: Running: inline script
	... install prereqs
	... install pyenv
	... install python
	... install poetry
==> default: Running action triggers after up ...
==> default: Running trigger: Launching App...
==> default: Running the TODO application setup script
    default: Running: inline script
    default: Creating virtualenv todo-app-vs8V2ZPt-py3.6 in /home/vagrant/.cache/pypoetry/virtualenvs
    ... install dependencies via poetry
    default:  * Serving Flask app "app" (lazy loading)
    default:  * Environment: development
    default:  * Debug mode: on
    default:  * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
    default:  * Restarting with stat
    default:  * Debugger is active!
    default:  * Debugger PIN: 110-403-136
````