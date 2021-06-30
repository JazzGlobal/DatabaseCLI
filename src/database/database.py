# Python Imports
import clr
import click
import sys
import os
from icecream import ic

sys.path.append(os.getcwd() + r"\ref")

# .NET Imports
clr.AddReference("SqlConnector")
from SqlConnector import SQLConnector


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
        ic(e)
    finally:
        database_probe.dispose()


@click.command()
@click.option("--full-backup", default=False, help="Determines whether or not the command executes a backup over each "
                                                   "database within the server instance.")
def backup_databases(full_backup):
    """ Executes a T-SQL BACKUP command for the specified databases. """
    database_probe = DatabaseProbe()

    if full_backup:
        sql = "SELECT * FROM SYS.DATABASES WHERE NAME NOT IN ('master','model','msdb','tempdb')"
    else:
        sys.exit("Script exited because only total backups have been implemented. Re-use command with option "
                 "--full-backup True")

    result_set = database_probe.execute_query(sql)
    for database in result_set:
        try:
            sql = f"BACKUP DATABASE \"{database}\" TO DISK = \'C:\\CEMDAS\\BACKUP\\{database}.BAK\' WITH INIT"
            print("Executing: ", sql)
            database_probe = DatabaseProbe()  # Create a new probe for each backup execution. We have to do this
            # because the queries get pushed to SQL SERVER for execution.
            database_probe.execute_query(sql)
            print(f"Successfully Backed Up: {database}")
        except Exception as e:
            ic(e)
        finally:
            database_probe.dispose()
