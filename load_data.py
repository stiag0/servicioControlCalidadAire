import sys
import xlrd
import csv
from main.model.model import db_save

template = {'fecha_hora': '',
'vereda': '', 
'PM2_5_CC_ICA': -9999.0, 
'altitud': -9999.0, 
'estado': '', 
'online': '', 
'longitude': -9999.0, 
'barrio': '', 
'ciudad': '', 
'temperatura': -9999.0, 
'humedad_relativa': -9999.0, 
'latitude': -9999.0, 
'nombre': '', 
'PM2_5_last': -9999.0, 
'PM2_5_mean': -9999.0, 
'codigo': -9999.0}

def load_xlsx(datafile):
    workbook = xlrd.open_workbook(datafile)
    worksheet = workbook.sheet_by_index(0)
    print(">Msg: Reading '"+datafile+"'")
    print("- Filas: "+str(worksheet.nrows))
    print("- Columnas: "+str(worksheet.ncols))

    for fila in range(worksheet.nrows):
        #Almacenará unicamente una medicion a la vez
        medicion = []
        for columna in range(worksheet.ncols):
            medicion.append(worksheet.cell(fila,columna).value)

        print(medicion)
        #print("aquí se guardaría el dato")

def load_csv(datafile):
    censors = []
    with open(datafile,'r') as csvfile:
        reader = csv.reader(csvfile)
        #cont = 0
        row1 = True
        for row in reader:
            if row1 == True:
                censors = row
                row1 = False
                continue
            #cont += 1
            index = 0
            date = ''
            for field in row:
                if index == 0:
                    date = field
                    index += 1
                else:
                    # censors[index] = numero identificacion de sensor
                    # date = fecha de la medicion
                    # field = medicion
                    #print(censors[index],date,field)
                    if field != '':
                        medicion = template
                        medicion['nombre'] = str(censors[index])
                        medicion['codigo'] = int(censors[index])
                        medicion['fecha_hora'] = str(date[:10]) + "T" + str(date[11:])
                        medicion['PM2_5_last'] = float(field)

                        save_response = db_save('mediciones', medicion)
                        if save_response == False:
                            print("- Hubo un problema almacenando el dato: ")
                            print(sensor,"\n")

                    #print(medicion['fecha_hora'])
                    index += 1
            #if cont == 2:
            #    break

def main():
    for datafile in sys.argv[1:]:
        ext=""
        i=datafile.rfind(".")
        if i == -1:
            print(">Error: Los ficheros no tienen extención '"+datafile+"'\n")
        else:
            if datafile[i:] == ".csv":
                    load_csv(datafile)
            else:
                if datafile[i:] == ".xlsx" or datafile[i:] == ".xls" or datafile[i:] == ".xlsm":
                    #load_xlsx(datafile)
                    pass
                else:
                    print(">Warning: Extención de fichero no soportado '"+datafile+"'\n")    

main()