from PySide6.QtWidgets import QTableView,QAbstractItemView,QHeaderView

class TableView(QTableView):
     def __init__(self, parent=None):
        super().__init__(parent)
         #Make it so the table can't be edited manually.
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)

        #Made the table's scrollpars smooth instead of correcting to the nearest table element
        self.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.setSelectionMode(QTableView.SingleSelection)

        #Adjust the horizontal header to stretch the last column to the edge of the canvas
        horizontal_header = self.horizontalHeader()
        horizontal_header.setStretchLastSection(True)
        horizontal_header.setDefaultSectionSize(300) #Sets default column width to 160
        horizontal_header.setSectionResizeMode(QHeaderView.Fixed)

        #Hide the vertical header, and set the vertical header to resize to the size of the item.
        vertical_header = self.verticalHeader()
        vertical_header.hide()
        vertical_header.setSectionResizeMode(QHeaderView.ResizeToContents)
        vertical_header.setSectionsMovable(False)

        self.setSelectionBehavior(QAbstractItemView.SelectRows)