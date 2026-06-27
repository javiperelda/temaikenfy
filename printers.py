from rich.console import Console
from rich.table import Table

class DataPrinter:
    def format_data(self, data, columns, title="Resultados"):
        
        console = Console()

        table = Table(title=title)

        # Esto recorre las columnas que se envian desde el llamado y extrae los encabezados. Ademas del color.
        for column in columns:
            # JP - 2026-06-22 - Permitir configurar ancho de columnas
            # table.add_column(column["header"], style=column.get("style", "white"))
            table.add_column(
                column["header"],
                style=column.get("style", "white"),
                width=column.get("width"),
                min_width=column.get("min_width"),
                no_wrap=column.get("no_wrap", False),
                overflow=column.get("overflow", "ellipsis"),
            )


        for item in data:
            row = []
            for column in columns:
                value_getter = column.get("value")
                if value_getter:
                    value = value_getter(item)
                else:
                    value = item.get(column.get("key"), "N/D")
                row.append(str(value))

            table.add_row(*row)

        console.print(table)
        
