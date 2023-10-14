from .constants import DB_HOST, DB_SCHEMA
from .db_secret import DB_USER, DB_PASSWORD
import mysql.connector
import mysql.connector.errors as mysql_errors


class MySQL:
    def __init__(self):
        self.conn = mysql.connector.connect(
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            database=DB_SCHEMA,
        )

    def _formatted_select_query(self, *args, **kwargs) -> str:
        """
        Build a SELECT statement to fetch records
        """

        try:
            where_str = None

            if not kwargs.get("table_name") or len(kwargs.get("table_name")) == 0:
                raise ValueError("ERROR - Missing required argument: table_name")

            qry = f"SELECT * FROM {kwargs.get('table_name')}"

            if kwargs.get("min_id"):
                if not where_str:
                    where_str = f" WHERE id >= {kwargs.get('min_id')} "

                else:
                    where_str += f"AND id >= {kwargs.get('min_id')} "

            if kwargs.get("max_id"):
                if not where_str:
                    where_str = f" WHERE id <= {kwargs.get('max_id')} "

                else:
                    where_str += f"AND id <= {kwargs.get('max_id')} "

            if kwargs.get("where_dict"):
                for k, v in kwargs.get("where_obj").items():
                    if not where_str:
                        where_str = f" WHERE {k} = '{v}' "

                    else:
                        where_str += f"AND {k} = '{v}' "

            qry += where_str

            return qry

        except ValueError as e:
            raise e

        except mysql_errors.ProgrammingError as e:
            raise e

        except Exception as e:
            raise e

    def _formatted_insert_query(self, table_name: str, vals_dict: dict) -> str:
        """
        Build an INSERT statement to add a record to the database
        """

        qry = f"INSERT INTO {table_name}"

        col_names = f"({', '.join([k for k in vals_dict.keys()])})"

        vals_with_quotes = [f"'{v}'" for v in vals_dict.values()]

        insert_vals = f"({', '.join([v for v in vals_with_quotes])})"

        qry = f"{qry} {col_names} VALUES {insert_vals}"

        return qry

    def query_from_table(
        self,
        table_name: str,
        min_id: int = None,
        max_id: int = None,
        where_dict: dict = None,
    ) -> list:
        """
        Query (SELECT) from database

        table_name: Table name as string (required)
        min_id: Lowest record id as int (optional)
        max_id: Highest record id as int (optional)
        where_dict: Dictionary of WHERE/AND conditions where key = column name, value = search val
        """

        try:
            sql_args = locals()
            sql_args.pop("self")

            cur = self.conn.cursor(dictionary=True)
            cur.execute(self._formatted_select_query(**sql_args))

            rows = cur.fetchall()

            return rows

        except Exception as e:
            return e

    def insert_into_table(self, table_name: str, vals_dict: dict):
        """
        Insert a record into the specified table

        table_name: Table name as string
        vals_dict: Dictionary of Column/Values where key = column name, value = val to insert
        """

        cur = self.conn.cursor(dictionary=True)
        cur.execute(self._formatted_insert_query(table_name, vals_dict))

        self.conn.commit()

    def disconnect(self):
        """
        Close any active connection database -- new class instance must be created after calling!
        """
        try:
            self.conn.close()

        except Exception:
            ...
