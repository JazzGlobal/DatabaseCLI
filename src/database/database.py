import clr
import click
import sys

clr.AddReference(r"D:\code\SQLConnector\SqlConnector\bin\Debug\SqlConnector.dll")
from SqlConnector import SQLConnector


class DatabaseProbe:
    def __init__(self):
        pass

    def __repr__(self):
        return "DatabaseProbe()"

    def __str__(self):
        return "DatabaseProbe: No Elements"


@click.command()
def get_databases():
    """ Prints the available databases within the SQLEXPRESS server instance. """
    connector = SQLConnector("")
    connector.InitializeConnection()
    connector.Open()

    command = connector.CreateCommand("SELECT * FROM SYS.DATABASES;")
    reader = connector.ReadResults(command)

    result_set = []

    while reader.Read():
        result_set.append(reader[0])

    connector.Close()
    click.echo(result_set)
    return result_set


@click.command()
@click.option("--full-backup", default=False, help="Determines whether or not the command executes a backup over each "
                                                   "database within the server instance.")
def backup_databases(full_backup):
    """ Executes a TSQL BACKUP command for the specified databases. """
    connector = SQLConnector("")
    connector.InitializeConnection()

    if full_backup:
        sql = "SELECT * FROM SYS.DATABASES WHERE NAME NOT IN ('master','model','msdb','tempdb')"
    else:
        sys.exit("Script exited because only total backups have been implemented. Re-use command with option "
                 "--full-backup True")

    connector.Open()
    command = connector.CreateCommand(sql)
    reader = connector.ReadResults(command)
    result_set = []
    while reader.Read():
        result_set.append(reader[0])
    connector.Close()

    for database in result_set:
        try:
            connector.Open()
            sql = f"BACKUP DATABASE \"{database}\" TO DISK = \'C:\\CEMDAS\\BACKUP\\{database}.BAK\' WITH INIT"
            print("Executing: ", sql)
            backup_command = connector.CreateCommand(sql)
            connector.ReadResults(backup_command)
            print(f"Successfully Backed Up: {database}")
        except Exception as e:
            print(e)
        finally:
            connector.Close()
