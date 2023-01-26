from fpdf import FPDF
#FUENTES
#Courier - Helvetica - Arial - Times - Symbol - ZapfDingbats
def tfont_size(hoja,size):
    hoja.set_font_size(size)

lista_datos = (('BODEGA CENTRAL','03262082182','ARNES PARA CASCO','UNICA','2'),
                ('BODEGA CENTRAL','03196005201','CHALECO GEOLOGO SUPERVISOR BICOLOR','XL','1'),
                ('BODEGA CS','03196052004','CHALECO GEOLOGO NARANJO','M','1'),
                ('BODEGA T1A','03162600044','BOTAS PUNTERIA DE ACERO PLANT ANTIPERF','44','1'),

)
pdf = FPDF('P', 'cm', (21.59,27.94)) #funcion para instanciar la hoja y crear parametros P= Vertical, mm= Unidad de medicion en est
#en este caso en centimetros, (MEDIDAS DE LA HOJA LARGO , ANCHO)#
pdf.add_page() #Funcion sirve para mantener el orden en base a los nuevos objetos que se agreguen al texto.

#Header
pdf.set_font('Courier','B',15)
pdf.text(x=8,y=1,txt='Vale de salida No. %s')
tfont_size(pdf,7)
pdf.text(x=9,y=1.5,txt='Emitido el día %s')
pdf.image('logoInterfaz.png',x=0.5,y=0.5,w=6,h=2)
pdf.ln(3.5)

#DATOS BODEGUERO
pdf.set_top_margin(10)
tfont_size(pdf,15)
pdf.cell(w=0,h=1,txt='Datos Bodeguero',border=1,align='C',fill=0,ln=1)
tfont_size(pdf,9)
pdf.cell(w=5,h=1,txt='Rut',border=1,align='C',fill=0)
pdf.cell(w=0,h=1,txt='Nombre',border=1,align='C',fill=0)
pdf.ln(2)

#DATOS TRABAJADOR
pdf.set_top_margin(10)
tfont_size(pdf,15)
pdf.cell(w=0,h=1,txt='Datos Trabajador',border=1,align='C',fill=0,ln=1)
tfont_size(pdf,9)
pdf.cell(w=5,h=1,txt='Rut',border=1,align='C',fill=0)
pdf.cell(w=0,h=1,txt='Nombre',border=1,align='C',fill=0)

pdf.ln(3.5)

#DATOS EPP
pdf.set_top_margin(10)
tfont_size(pdf,15)
pdf.cell(w=0,h=1,txt='EPPS',border=1,align='C',fill=0,ln=1)
pdf.cell(w=3,h=1,txt='BODEGA',border=1,align='C',fill=0)
pdf.cell(w=3,h=1,txt='CÓDIGO',border=1,align='C',fill=0)
pdf.cell(w=8,h=1,txt='DESCRIPCIÓN',border=1,align='C',fill=0)
pdf.cell(w=2,h=1,txt='TALLA',border=1,align='C',fill=0)
pdf.cell(w=0,h=1,txt='CANTIDAD',border=1,align='C',fill=0,ln=1)
tfont_size(pdf,8)
for valor in lista_datos:
    pdf.cell(w= 3,h= 1,txt=valor[0],border=1,align='C',fill=0)
    pdf.cell(w= 3,h= 1,txt=valor[1],border=1,align='C',fill=0)
    pdf.cell(w= 8,h= 1,txt=valor[2],border=1,align='C',fill=0)
    pdf.cell(w= 2,h= 1,txt=valor[3],border=1,align='C',fill=0)
    pdf.multi_cell(w= 0,h= 1,txt=valor[4],border=1,align='C',fill=0,ln=1)

pdf.ln(3)
tfont_size(pdf,15)
pdf.cell(w=5,h=1,txt='Firma Bodega',border=1,align='C',fill=0)
pdf.cell(w=5.5,h=1,txt='Firma Trabajador',border=1,align='C',fill=0,ln=1)
tfont_size(pdf,7)
pdf.cell(w=5,h=2,txt='_______________________________',border=1,align='C',fill=0)
pdf.cell(w=5.5,h=2,txt='__________________________________',border=1,align='C',fill=0)

#def funcionIdDocumento():
#    identificadorPdf=identificadorPdf+1
identificadorPdf=1

"""def iD_Pdf(numero):
    numero=1
    while numero!=0:
        i=numero+1
        numero=i
    return numero



iD_Pdf(identificadorPdf)"""

pdf.output('C:\ReportesValesDeSalida\Vale_Salida_No.%s.pdf'%identificadorPdf,'D') #Aqui va la ruta de donde queremos que se almacene el archivo creado.