"""Парсер html-таблиц."""
from typing import List

import bs4


class HTMLTableParser:
    """Парсер html-таблиц.

    По номеру таблицы на странице формирует представление ее ячеек в виде списка списков. Ячейки с
    rowspan и colspan представляются в виде набора набора ячеек с одинаковыми значениями.
    """

    def __init__(self, html: str, table_index: int):
        soup = bs4.BeautifulSoup(html, "lxml")
        self._table = soup.find_all("table")[table_index]
        self._parsed_table = []

    @property
    def parsed_table(self) -> List[List]:
        """html-таблица в виде списка списков ячеек."""
        if self._parsed_table:
            return self._parsed_table
        table = self._table
        row_pos = 0
        col_pos = 0
        for row in table.find_all("tr"):
            for cell in row.find_all(["th", "td"]):
                col_pos = self._find_empty_cell(row_pos, col_pos)
                row_span = int(cell.get("rowspan", 1))
                col_span = int(cell.get("colspan", 1))
                self._insert_cells(cell.text, row_pos, col_pos, row_span, col_span)
            row_pos += 1
            col_pos = 0
        return self._parsed_table

    def _find_empty_cell(self, row_pos: int, col_pos: int) -> int:
        """Ищет первую незаполненную ячейку в ряду и возвращает ее координату."""
        parse_table = self._parsed_table
        if row_pos >= len(parse_table):
            return col_pos
        row = parse_table[row_pos]
        while col_pos < len(row) and row[col_pos] is not None:
            col_pos += 1
        return col_pos

    def _insert_cells(self, value: str, row: int, col: int, row_span: int, col_span: int):
        """Заполняет таблицу значениями с учетом rowspan и colspan ячейки."""
        for row_pos in range(row, row + row_span):
            for col_pos in range(col, col + col_span):
                self._insert_cell(value, row_pos, col_pos)

    def _insert_cell(self, value: str, row_pos: int, col_pos: int):
        """Заполняет значение, при необходимости расширяя таблицу."""
        parse_table = self._parsed_table
        while row_pos >= len(parse_table):
            parse_table.append([None])
        row = parse_table[row_pos]
        while col_pos >= len(row):
            row.append(None)
        row[col_pos] = value
