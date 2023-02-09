from openpyxl import Workbook
from openpyxl.styles import Font
def crearExcel():
    book = Workbook()
    bodegas = book.active
    bodegas.title="EPP's"
    bodegas.append(['BODEGA','CODIGO','NOMBRE EPP','CANTIDAD RETIRADA','TOTAL CLP POR EPP'])
  #  for valor in lista_datos:
         

    book.save('prueba_excel.xlsx')

crearExcel()