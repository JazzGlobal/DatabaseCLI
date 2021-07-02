# DatabaseCLI
CLI application for DatabaseToolKit. Designed for developers to script behavior without using GUI.

# Installation
The project already comes with a version controlled virtual environment for script execution and testing. Simply clone the repository and open using PyCharm.
It's way easier to just install PyCharm and clone the repository using PyCharm's built in GUI. You can get PyCharm, JetBrains' Python IDE, for free here: https://www.jetbrains.com/pycharm/ . Be sure to follow their distribution rules.

Once installed and cloned, you must start the virtual environment. Start the virtual environment by running:
```commandline
.\venv\Scripts\activate.bat
```

If the above is not available to you, follow the steps within the link to add a new virtual environment:
jetbrains.com/help/pycharm/creating-virtual-environment.html#python_create_virtual_env

Then download / install the dependencies:
```commandline
pip install -r requirements.txt
```

# Command Usage
Now try running the following command for execute a full backup of all databases on your SQLEXPRESS instance:
```commandline
backup --full-backup True
```

You can even output the above command's output to an external file:
```commandline
backup --full-backup True >> BackupLog.log
```
# Future Features
More features are coming. I plan to add time frame specific backups, overwriting options, and various restore features. I have a few other ideas on the brain but this is a super early / WIP state.s