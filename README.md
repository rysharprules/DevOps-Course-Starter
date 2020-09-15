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