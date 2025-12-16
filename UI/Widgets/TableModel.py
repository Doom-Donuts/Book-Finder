from PySide6.QtCore import Qt, QAbstractTableModel

class DictionaryTableModel(QAbstractTableModel):
    def __init__(self, data, col_labels, parent=None):
        super().__init__(parent)
        self._data = data  # List of dictionaries
        self._headers = col_labels

    def rowCount(self, parent=None):
        return len(self._data)

    def columnCount(self, parent=None):
        return len(self._headers)

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            row_data = self._data[index.row()]
            column_key = self._headers[index.column()]
            return row_data.get(column_key, None)

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            return self._headers[section]
        return None

    def flags(self, index):
        return Qt.ItemIsEditable | Qt.ItemIsSelectable | Qt.ItemIsEnabled

    def setData(self, index, value, role=Qt.EditRole):
        if role == Qt.EditRole:
            row_data = self._data[index.row()]
            column_key = self._headers[index.column()]
            row_data[column_key] = value  # Update the value in the dictionary
            self.dataChanged.emit(index, index)  # Notify the view to update the cell
            return True
        return False

    def _get_all_keys(self):
        keys = set()
        for item in self._data:
            keys.update(item.keys())
        return keys

    def update_data(self, row, column, new_value):
        """This method updates the model's data and notifies the view."""
        row_data = self._data[row]
        column_key = self._headers[column]
        row_data[column_key] = new_value  # Update the value
        index = self.createIndex(row, column)  # Create the index for the changed cell
        self.dataChanged.emit(index, index)  # Notify the view to update that cell

    def update_row(self, row, new_values):
        """Update a whole row."""
        for column, new_value in enumerate(new_values.values()):
            print(new_value)
            self._data[row][self._headers[column]] = new_value

        top_left = self.createIndex(row, 0)
        bottom_right = self.createIndex(row, self.columnCount() - 1)
        self.dataChanged.emit(top_left, bottom_right)  # Notify the view to update the whole row
