# Python Imports
import os
import glob
import sys
import click
import clr
from icecream import ic
from pathlib import Path

sys.path.append(os.getcwd() + r"\ref")

# .NET Imports
clr.AddReference("SqlConnector")
from SqlConnector import SQLConnector

ic.configureOutput(prefix="DEBUG: ", includeContext=True)


class DatabaseProbe:
    def __init__(self):
        self.sql_connector = SQLConnector("")
        self.sql_connector.InitializeConnection()

    def __repr__(self):
        return "DatabaseProbe()"

    def __str__(self):
        return f"DatabaseProbe: \nConnection String = {self.sql_connector.ConnectionString}"

    def execute_query(self, sql_query_string):
        self.sql_connector.Open()
        command = self.sql_connector.CreateCommand(sql_query_string)
        reader = self.sql_connector.ReadResults(command)

        result_set = []

        while reader.Read():
            result_set.append(reader[0])

        self.sql_connector.Close()
        return result_set

    def dispose(self):
        self.sql_connector.Dispose()


@click.command()
def get_databases():
    """ Prints the available databases within the SQLEXPRESS server instance. """
    try:
        database_probe = DatabaseProbe()
        result_set = database_probe.execute_query("SELECT * FROM SYS.DATABASES;")
        click.echo(result_set)
        return result_set
    except Exception as e:
        click.secho(e, bold=True, fg="red")
        ic(e)
    finally:
        database_probe.dispose()


@click.command()
@click.option("--full-backup", default=False, metavar='<bool>', help="Determines whether or not the command executes "
                                                                     "a backup over each "
                                                                     "database within the server instance.")
def backup_databases(full_backup):
    """ Executes a T-SQL BACKUP command for the specified databases. """
    database_probe = DatabaseProbe()

    if full_backup:
        sql = "SELECT * FROM SYS.DATABASES WHERE NAME NOT IN ('master','model','msdb','tempdb')"
    else:
        exit_message = "Script exited because only total backups have been implemented. Re-use command with option " \
                       "--full-backup True "
        click.echo(exit_message)
        sys.exit()

    result_set = database_probe.execute_query(sql)
    ic(result_set)
    for database in result_set:
        try:
            sql = f"BACKUP DATABASE \"{database}\" TO DISK = \'C:\\CEMDAS\\BACKUP\\{database}.BAK\' WITH INIT"
            ic(sql)
            click.echo(f"Executing: {sql}")
            database_probe = DatabaseProbe()  # Create a new probe for each backup execution. We have to do this
            # because the queries get pushed to SQL SERVER for execution.
            database_probe.execute_query(sql)
            click.secho(f"SUCCESS: {database} BACKUP COMPLETE", bold=True, fg="green")
        except Exception as e:
            click.secho(f"ERROR during {database} BACKUP attempt. {e}", bold=True, fg="red")
            ic(e)
        finally:
            database_probe.dispose()


@click.command()
@click.option("--recursive", "-r", default=False,
              help="If set to True, will recursively search PATH for .BAK files.",
              metavar='<bool>')
@click.argument("path", metavar="<PATH>")
def restore_databases(path, recursive):
    """ Restores the .BAK files from a given directory to the current SQLEXPRESS Instances

    PATH is the path searched.
    """

    path = Path(path)

    # Debug
    ic(str(path))
    ic(recursive)
    # End Debug

    click.echo("Checking for .BAK files ... ")

    result_set = []
    if recursive:
        result_set = glob.glob(str(path) + "/**/*.BAK", recursive=True)
    else:
        result_set = glob.glob(str(path) + "/*.BAK", recursive=False)
    # Debug
    ic(result_set)
    # End Debug

    if len(result_set) > 1:
        # Attempt to restore .BAK files.
        for backup_file in result_set:
            split_file_name = backup_file.split('\\')
            name_index = len(split_file_name) - 1
            backup_name = split_file_name[name_index].split('.')[0]
            sql = f"RESTORE DATABASE [{backup_name}] FROM DISK='{backup_file}' WITH REPLACE"

            # Debug
            ic(backup_name)
            ic(sql)
            # Debug End

            try:
                database_probe = DatabaseProbe()
                click.echo(f"Restoring Database {backup_name} from file {backup_file}")
                database_probe.execute_query(sql)
                click.secho(f"SUCCESS: {sql}", bold=True, fg="green")
            except Exception as e:
                ic(e)
                click.secho(f"FAILED: {sql}", bold=True, fg="red")
                click.secho(e, fg="red")
            finally:
                database_probe.dispose()
    else:
        print(f"No .BAK files were found in path: {path}")
