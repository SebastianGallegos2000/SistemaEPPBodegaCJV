from openpyxl import Workbook
from openpyxl.styles import Font

book = Workbook()
bodega_central = book.active
bodega_central['A1'] = 'BODEGA'
bodega_central['B1'] = 'CCODIGO EPP'
bodega_central['C1'] = 'NOMBRE EPP'
bodega_central['D1'] = 'CANTIDAD'
bodega_central['E1'] = 'TOTAL CLP POR EPP'

bodega_t1a = book.create_sheet('Bodega T1A')
bodega_t1a['A1'] = 'BODEGA'
bodega_t1a['B1'] = 'CCODIGO EPP'
bodega_t1a['C1'] = 'NOMBRE EPP'
bodega_t1a['D1'] = 'CANTIDAD'
bodega_t1a['E1'] = 'TOTAL CLP POR EPP'

bodega_cs = book.create_sheet('Bodega CS')
bodega_cs['A1'] = 'BODEGA'
bodega_cs['B1'] = 'CCODIGO EPP'
bodega_cs['C1'] = 'NOMBRE EPP'
bodega_cs['D1'] = 'CANTIDAD'
bodega_cs['E1'] = 'TOTAL CLP POR EPP'

book.save('prueba_excel.xlsx')