from pathlib import Path
import glob
import shutil
#Este programa simula un recetario, hace CRUD's dentro del sistema operativo con los archivos de tipo .txt y los directorios

ruta_recetas = Path(r'C:\Recetas')
categorias = {}
lista_recetas = []
rutas_recetas = []
total_archivos_txt = 0
diccionario_receta = {}

#Esta linea del bucle apunta a el directorio Recetas almacenado dentro de la carpeta raiz C:
#El metodo .iterdir() permite iterar a traves del path
for directorio in ruta_recetas.iterdir():
    #Verifica si el elemento directorio es un directorio
    if directorio.is_dir():
        #Agrega el nombre del directorio como clave y la ruta del directorio como valor al arreglo lista_categorias
        categorias.update({directorio.stem : str(Path(directorio))})
        #Busca en el directorio los archivos con el subfijo .txt
        #tambien devuelve en forma de lista la ruta completa del archivo
        archivos_txt = glob.glob(str(directorio / '*.txt'))
        total_archivos_txt += 1
        rutas_recetas.append(archivos_txt)

#print(f'Cantidad de recetas {total_archivos_txt}\n
# Las categorias de tu recetario son: \n',categorias.join(lista_categorias))


#Itera sobre cada elemento de la lista rutas_recetas y retorna un diccionario con el nombre de la receta como key
#y la ruta completa del archivo como value
for ruta in rutas_recetas:
    for receta in ruta:
        diccionario_receta.update({str(Path(receta).stem.lower()): receta})


def leer_receta():
    #Imprime todas las llaves del diccionario 'diccionario_receta' donde cada valor corresponde al path de un archivo .txt que simula ser una receta
    print('Cual de las siguientes recetas quieres leer?\n',end="\n".join(diccionario_receta.keys()))

    opcion = input('\nEscribe el nombre de la receta que quieres leer: ').lower()

    while opcion not in diccionario_receta.keys():
        print('Opcion incorrecta')
        print('Cual de las siguientes recetas quieres leer?\n', end="\n".join(diccionario_receta.keys()))
        opcion = input('\nEscribe el nombre de la receta que quieres leer: ').lower()
    #Toma la llave ingresada por el input e ingresa al Path que tiene como valor, abre el archivo y muestra su contenido
    print(Path(diccionario_receta.get(opcion)).read_text())


def crear_recetas():

    """Crear una nueva receta en una categoría existente o en una nueva categoría."""

    diccionario_indices_paths = {}
    receta_nueva = input('Escribe el nombre de la receta que quieres crear: ')
    ruta_receta = diccionario_receta.get(receta_nueva)

    if ruta_receta:
        if Path(ruta_receta).exists():
            print(f'El archivo ya existe en el directorio {ruta_receta}\nHasta luego :D')
    else:
        crear_receta = input('La ruta del archivo no existe\nQuieres crear una receta nueva con este nombre?\nsi\nno\n').lower()

        if crear_receta == 'si':
            #Genera una tupla con un indice que inicia contando desde 1 y un diccionario donde 'diccionario' representa cada 'llave' de cada key/value
            #en 'categorias.items()'
            for indice, diccionario in enumerate(categorias.items(), 1):
                diccionario_indices_paths.update({indice: diccionario})
                print(f"{indice}) {diccionario[0]}")

            escoger_categoria = int(input('\nEsas son las categorias donde puedes crear la receta, ingresa el numero de la categoria donde quieres crea la receta: \n'))

            while escoger_categoria not in diccionario_indices_paths.keys():
                escoger_categoria = int(input('\nEsas son las categorias donde puedes crear la receta, escoger una: \n'))

            sufijo = '.txt'
            #Esta es la ruta(carpeta)donde se va a crear el archivo
            ruta_receta_nuevo = Path(diccionario_indices_paths.get(escoger_categoria)[1])
            #asignamos al archivo nuevo el nombre del archivo que ya se valido no existe
            # por medio de la variable receta nueva
            nombre_receta_nueva = receta_nueva + sufijo
            #usamos el / para concatenar el path y el nombre del archivo nuevo
            #o funciona de la misma manera con el ejemplo de abajo
            #archivo_nuevo = Path(diccionario_prueba.get(escoger_categoria)[1]) / nombre_receta_nueva
            archivo_nuevo = ruta_receta_nuevo / nombre_receta_nueva
            archivo_nuevo.touch()
            print(f'La receta fue creada con exitos en el directorio {ruta_receta_nuevo}\nAdios :)')
        else:
            print('Si no quieres crear la receta entonces me despido\nAdios :)')


def crear_categoria():
    pregunta_crear_categoria_nueva = input("Quieres crear una categoria en el recetario?\nsi\nno\nEscribe aqui tu respuesta: ").lower().strip()
    while pregunta_crear_categoria_nueva != 'si' and pregunta_crear_categoria_nueva != 'no':
        pregunta_crear_categoria_nueva = input(
            "Quieres crear una categoria en el recetario?\nsi\nno\nEscribe aqui tu respuesta: ").lower()
    if pregunta_crear_categoria_nueva == 'si':
            nombre_categoria_nueva = input("Escribe aqui nombre de la categoria: ")
            if nombre_categoria_nueva in categorias.keys():
                print(f"Ya existe una categoria con ese nombre, se encuentra en la ruta {categorias.get(nombre_categoria_nueva)}")
            else:
                crear_categoria_nueva = Path(ruta_recetas / nombre_categoria_nueva.capitalize())
                crear_categoria_nueva.mkdir(parents=True, exist_ok=False)
                categorias.update({nombre_categoria_nueva:str(crear_categoria_nueva)})
    else:
        print('Si no quieres crear la receta entonces me despido\nAdios :)')


def eliminar_receta():
    recetas = {}
    pregunta_eliminar_receta = input("Quieres eliminar una receta ?\nsi\nno\nEscribe aqui tu respueta: ").lower()
    while pregunta_eliminar_receta != 'si' and pregunta_eliminar_receta != 'no':
        pregunta_eliminar_receta = input("Selecciona una opcion valida\nQuieres eliminar una receta "
                                         "?\nsi\nno\nEscribe aqui tu respuesta: ").lower()
    if pregunta_eliminar_receta == 'si':
        for indice,diccionario in enumerate(diccionario_receta.items(),1):
            recetas.update({indice: diccionario})
            print(indice,'.-',diccionario[0])
        seleccion_eliminar_receta = int(input("Estas son las recetas existentes, "
                                              "selecciona el numero de la receta que quieres eliminar"
                                              "\nEscribe aqui tu respuesta: "))

        confirmar_eliminacion = input(f"Estas seguro de eliminar '{recetas.get(seleccion_eliminar_receta)[0]}?: ").lower()

        while confirmar_eliminacion != 'si' and confirmar_eliminacion != 'no':
            confirmar_eliminacion = input(f"Selecciona una opcion valida"
                                          f"Estas seguro de eliminar "
                                          f"'{recetas.get(seleccion_eliminar_receta)[0]}? '"
                                          f"si\nno: ").lower()

        print(f"La receta '{recetas.get(seleccion_eliminar_receta)[0]}' ha sido eliminada para siempre :(")
        archivo_a_eliminar = Path(diccionario_receta.get(recetas.get(seleccion_eliminar_receta)[0]))
        archivo_a_eliminar.unlink()
        diccionario_receta.pop(recetas.get(seleccion_eliminar_receta)[0])
        print(f"Esta es tu lista de recetas actualizada:")
        for key in diccionario_receta.keys():
            print(key)


def eliminar_categoria():
    diccionario_categorias = {}
    pregunta_eliminar_categoria = input("Quieres eliminar una categoria ?\nsi\nno\nEscribe aqui tus respuesta: ").lower()
    while pregunta_eliminar_categoria != 'si' and 'no':
        pregunta_eliminar_categoria = input(
            "Respuesta no valida\nQuieres eliminar una categoria ?\nsi\nno\nEscribe aqui tus respuesta: ").lower()
    for indice,elemento in enumerate(categorias.items(),1):
        diccionario_categorias.update({indice:elemento})
        print(f"{indice}.-{elemento[0]}")

    escoger_categoria = int(input("Ingresa el numero de la categoria que quieres eliminar: "))
    validar_eliminacion = input(f"""Estas seguro de eliminar la categoria? '{diccionario_categorias.get(escoger_categoria)[0]}'
TODOS LOS ELEMENTOS DENTRO DEL DIRECTORIO SERAN ELIMINADOS
si\nno\nEscribe aqui tu respuesta: """).lower()

    if validar_eliminacion == 'si':
        categoria_eliminar = Path(categorias.get(diccionario_categorias.get(escoger_categoria)[0]))
        categorias.pop(diccionario_categorias.get(escoger_categoria)[0])
        shutil.rmtree(categoria_eliminar)
        print(f"Categoria '{diccionario_categorias.get(escoger_categoria)[0]}' eliminada exitosamente")

        for categoria in categorias:
            print(categoria)

        print("Esas son las categorias restantes")

for k, v in categorias.items():
    print(k,v)