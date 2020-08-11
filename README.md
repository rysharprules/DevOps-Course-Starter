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

Note, the application is flexible enough to handle different [lists](https://developer.atlassian.com/cloud/trello/rest/api-group-boards/#api-boards-id-lists-get), but depends on the existence of lists with the titles 'To Do' and 'Done'.
