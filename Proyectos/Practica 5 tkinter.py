from tkinter import *
from pathlib import Path
import glob
import shutil

def destroy_elementos(*args):
    """Aplica la funcion destroy a todos los elementos pasados como argumentos"""
    for arg in args:
        arg.destroy()

#creamos la instancia que representa la ventana principal
main_window = Tk()
#definimos el tamaño de la ventana y dejamos False en ambos parametros del metodo "resizable" para que el
#tamaño de la ventana no pueda ser modificado
main_window.geometry('1024x768')
main_window.resizable(False,False)


def main_tab():

    main_window.configure(background="#04254e")
    ruta_recetas = Path(r'C:\Recetas')
    categorias = {}
    rutas_recetas = []
    total_archivos_txt = 0
    recetas = {}

    # Esta linea del bucle apunta a el directorio Recetas almacenado dentro de la carpeta raiz C:
    # El metodo .iterdir() permite iterar a traves del path
    for directorio in ruta_recetas.iterdir():
        # Verifica si el elemento directorio es un directorio
        if directorio.is_dir():
            # Agrega el nombre del directorio como clave y la ruta del directorio como valor al arreglo lista_categorias
            categorias.update({directorio.stem.lower(): str(Path(directorio))})
            # Busca en el directorio los archivos con el subfijo .txt
            # tambien devuelve en forma de lista la ruta completa del archivo
            archivos_txt = glob.glob(str(directorio / '*.txt'))
            total_archivos_txt += 1
            rutas_recetas.append(archivos_txt)

    # Itera sobre cada elemento de la lista rutas_recetas y retorna un diccionario con el nombre de la receta como key
    # y la ruta completa del archivo como value
    for ruta in rutas_recetas:
        for receta in ruta:
            recetas.update({str(Path(receta).stem.lower()): receta})

    def mostrar_recetas_tab():

        main_window.configure(background="#1a6ca8")
        # al ingresar a este tab los siguientes widgets y su contenido seran eliminados de la ventana
        destroy_elementos(home_page_label,
                          leer_recetas_boton,
                          crear_recetas_boton,
                          mostrar_recetas_boton,
                          eliminar_receta_boton,
                          eliminar_categoria_boton)


        # Configuracion del frame
        tab_2_label = Label(main_window, text="Lista de recetas",font=("courier new" ,30), background="#1a6ca8",fg="#c0c0c0",anchor=CENTER)
        tab_2_label.pack()
        lista_recetas_frame = Frame(main_window,height=20)
        lista_recetas_frame.pack()
        lista_recetas = Text(lista_recetas_frame, font=("courier new", 14),borderwidth=0.5, height=20,padx=10,
                             background="#1a6ca8", fg="#c0c0c0")
        lista_recetas.pack(side=LEFT, fill=BOTH, expand=True)
        desplegar_recetas = end='\n'.join(recetas.keys())
        lista_recetas.insert(index=0.0, chars=desplegar_recetas.title())
        lista_recetas.tag_configure("center", justify='center')
        lista_recetas.tag_add("center", "1.0", "end")
        lista_recetas.configure(state='disabled')
        lista_recetas_scrollbar = Scrollbar(lista_recetas_frame, command=lista_recetas.yview)
        lista_recetas_scrollbar.pack(side=RIGHT, fill=Y)
        lista_recetas.config(yscrollcommand=lista_recetas_scrollbar.set)

        def back_mostrar_lista_recetas_tab():
            destroy_elementos(tab_2_label,
                              lista_recetas_frame,
                              lista_recetas,
                              lista_recetas_scrollbar,
                              boton_regresar,
                              eliminar_categoria_boton,)

            main_tab()

        boton_regresar = Button(main_window, text="Regresar", command=back_mostrar_lista_recetas_tab, width=9, relief=RAISED,
                                             fg="#ffffff",bg="#6ca6cd",activebackground="#e0e0e0",
                                             bd=3,font=("Ink Free", 14), anchor=CENTER)
        boton_regresar.place(x=460, y=540)

    def leer_recetas_tab():
        main_window.configure(background="#7e512b")

        destroy_elementos(home_page_label,
                          mostrar_recetas_boton,
                          leer_recetas_boton,
                          crear_recetas_boton,
                          eliminar_receta_boton,
                          eliminar_categoria_boton)

        def deshabilitar_seleccion_doble_click(event):
            '''
            Evita que se pueda seleccionar el texto desplegado al dar doble click
            '''
            lista_recetas.tag_remove("sel", "1.0", "end")
            return "break"

        def deshabilitar_seleccion_inicial(event):
            lista_recetas.tag_remove("sel", "1.0", "end")
            return "break"

        def back():
            destroy_elementos(tab_3_label,
                              lista_recetas_frame,
                              lista_recetas,
                              input_escoger_receta,
                              boton_leer_receta,
                              boton_back,
                              label,
                              crear_recetas_boton,
                              eliminar_categoria_boton)
            main_tab()


        def mostrar_contenido_receta():
            nombre_receta_1 = input_escoger_receta.get().lower()
            destroy_elementos(tab_3_label,
                              lista_recetas_frame,
                              lista_recetas,
                              lista_recetas_scrollbar,
                              label,
                              boton_leer_receta,
                              input_escoger_receta,
                              boton_back)

            def deshabilitar_seleccion_doble_click(event):
                """ Evita que se pueda seleccionar el texto desplegado al dar doble click"""
                texto_receta.tag_remove("sel", "1.0", "end")
                return "break"

            def editar_contenido():
                destroy_elementos(texto_receta_frame,
                texto_receta,
                texto_receta_scrollbar,
                boton_editar_receta,
                boton_regresar_mostrar_contenido_receta)

                def back_editar_contenido_receta():
                    destroy_elementos(editar_texto_receta_frame,
                                      editar_text_widget,
                                      editar_texto_receta_scrollbar,
                                      boton_guardar,
                                      boton_pagina_anterior)

                    leer_recetas_tab()

                editar_texto_receta_frame = Frame(main_window)
                editar_texto_receta_frame.pack()

                editar_text_widget = Text(editar_texto_receta_frame,height=18 ,fg="#add8e6", bg="#7e512b", borderwidth=0.5, pady=10,
                                    font=("segoe script", 12))
                # Agregar esta linea para cambiar el fondo del widget
                # lista_recetas.configure(background="Red")
                editar_text_widget.pack(side=LEFT, fill=X, expand=True)

                # abrimos el contenido del archivo en modo lectura y guardamos el contenido en una variable para poder
                # insertar el contenido en el text widget
                archivo_texto = open(Path(recetas.get(nombre_receta_1)), 'r+')
                contenido = archivo_texto.read()
                editar_text_widget.insert(END, contenido)

                editar_text_widget.tag_configure("center", justify='center')
                editar_text_widget.tag_add("center", "1.0", "end")

                editar_texto_receta_scrollbar = Scrollbar(editar_texto_receta_frame, command=editar_text_widget.yview)
                editar_texto_receta_scrollbar.pack(side=RIGHT, fill=Y)

                editar_text_widget.config(yscrollcommand=editar_texto_receta_scrollbar.set)

                def guardar_cambios():
                    archivo_texto = open(Path(recetas.get(nombre_receta_1)), 'w+')
                    contenido = editar_text_widget.get("1.0", END)
                    archivo_texto.write(contenido)
                    label_cambios_guardados = Label(main_window, text="Los cambios en la receta\nhan sido guardados",
                                            font=("Consolas", 16), fg="#6eee36", bg="#7e512b")
                    label_cambios_guardados.place(x=365, y=580)
                    main_window.after(2000, label_cambios_guardados.destroy)


                boton_guardar = Button(main_window, text="Guardar\ncambios", command=guardar_cambios,fg="#00008b" ,
                                                    font=("consolas bold",12) ,relief=SOLID, anchor=CENTER)
                boton_guardar.place(x=470, y=490)
                boton_pagina_anterior = Button(main_window, text="Volver al inicio", command=back_editar_contenido_receta,
                                                  fg="#00008b", font=("consolas bold", 12), relief=SOLID, anchor=CENTER)
                boton_pagina_anterior.place(x=428, y=720)

            texto_receta_frame = Frame(main_window)
            texto_receta_frame.pack()


            texto_receta = Text(texto_receta_frame, height=18, fg="#add8e6", bg="#7e512b", borderwidth=0.5, pady=10, font=("segoe script", 12))
            # Agregar esta linea para cambiar el fondo del widget
            # lista_recetas.configure(background="Red")
            texto_receta.pack(side=LEFT, fill=X, expand=True)

            #abrimos el contenido del archivo en modo lectura guardamos en una variable para poder
            #insertar el contenido en el text widget
            desplegar_texto_recetas = open(Path(recetas.get(nombre_receta_1)), 'r')
            contenido_receta = desplegar_texto_recetas.read()

            texto_receta.insert(END, contenido_receta)

            texto_receta.tag_configure("center", justify='center')
            texto_receta.tag_add("center", "1.0", "end")

            texto_receta.configure(state='disabled')
            texto_receta.bind("<Double-1>", deshabilitar_seleccion_doble_click)

            texto_receta_scrollbar = Scrollbar(texto_receta_frame, command=texto_receta.yview)
            texto_receta_scrollbar.pack(side=RIGHT, fill=Y)

            texto_receta.config(yscrollcommand=texto_receta_scrollbar.set)

            def back_mostrar_contenido_receta():
                destroy_elementos(texto_receta_frame,
                texto_receta,
                texto_receta_scrollbar,
                boton_regresar_mostrar_contenido_receta,
                leer_recetas_boton,
                boton_editar_receta)
                leer_recetas_tab()

            boton_editar_receta = Button(main_window, command=editar_contenido, text="Editar\nreceta", fg="#00008b",
                                         font=("consolas bold", 12), relief=SOLID, anchor=CENTER)
            boton_editar_receta.place(x=472, y=485)
            boton_regresar_mostrar_contenido_receta = Button(main_window, text="Pagina anterior", command=back_mostrar_contenido_receta,
                                                             height=1, width=16, fg="#00008b", font=("consolas bold",12), relief=SOLID)
            boton_regresar_mostrar_contenido_receta.place(x=430, y=720)

        tab_3_label = Label(main_window, text="Lista de recetas",font=("segoe script", 30),fg="#add8e6",bg="#7e512b",
                             anchor=CENTER)
        tab_3_label.pack()

        lista_recetas_frame = Frame(main_window, height=14,bg="#7e512b", pady=5)
        lista_recetas_frame.pack()

        lista_recetas = Text(lista_recetas_frame, height=14, fg="#add8e6", bg="#7e512b", borderwidth=0.5, font=("segoe script", 12))
        lista_recetas.pack(side=LEFT, fill=BOTH, expand=True)
        desplegar_recetas = end='\n'.join(recetas.keys())
        lista_recetas.insert(index=0.0, chars=desplegar_recetas.title())

        lista_recetas.tag_configure("center", justify='center')
        lista_recetas.tag_add("center", "1.0", "end")

        lista_recetas.configure(state='disabled')
        lista_recetas.bind("<Double-1>", deshabilitar_seleccion_doble_click)
        # deshabilita la selección del texto al hacer clic izquierdo
        lista_recetas.bind("<Button-1>", deshabilitar_seleccion_inicial)

        lista_recetas_scrollbar = Scrollbar(lista_recetas_frame, command=lista_recetas.yview)
        lista_recetas_scrollbar.pack(side=RIGHT, fill=Y)

        lista_recetas.config(yscrollcommand=lista_recetas_scrollbar.set)
        label = Label(main_window, text="Ingresa el nombre de la\nreceta que quieres leer",
                                   fg="#add8e6",bg="#7e512b",font=("segoe print", 14))
        label.place(x=395, y=435)
        input_escoger_receta = Entry(main_window,width=25, font=("Microsoft Sans Serif", 18), justify=CENTER)
        input_escoger_receta.place(x=340, y=520)

        def abrir_receta():
            """
            Si el valor ingresado en el input_escoger_receta
            se encuentra como "key" en el diccionario recetas
            manda a llamar a la funcion mostrar_contenido_recetas
            """
            nombre_receta = input_escoger_receta.get().lower()
            if nombre_receta in recetas.keys():
                mostrar_contenido_receta()

            else:
                label_no_existe = Label(main_window, text="La receta no existe\ningresa un nombre de la lista",
                                                     font=("Consolas", 16),bg="#7e512b" ,fg="Red")
                label_no_existe.place(x=340, y=580)
                main_window.after(2000, label_no_existe.destroy)

        boton_leer_receta = Button(main_window,command=abrir_receta, text="Abrir receta", height=1,fg="#00008b" ,font=("consolas bold",12) ,relief=SOLID, anchor=CENTER)
        boton_leer_receta.place(x=680, y=520)
        boton_back = Button(main_window, command=back, text="Regresar", height=1, width=12, fg="#00008b", font=("consolas bold",12), relief=SOLID, anchor=CENTER)
        boton_back.place(x=450, y=720)

    def crear_receta():

        main_window.configure(bg="#FFA07A")
        destroy_elementos(home_page_label,
                          mostrar_recetas_boton,
                          leer_recetas_boton,
                          crear_recetas_boton,
                          eliminar_receta_boton,
                          eliminar_categoria_boton)


        def back():
            destroy_elementos(label_principal,
                              crear_receta_entry,
                              label_2,
                              boton_crear,
                              boton_regresar,
                              eliminar_categoria_boton)
            main_tab()

        def creacion_receta():
            nombre_nuevo = crear_receta_entry.get().lower()

            if nombre_nuevo in recetas.keys():
                label = Label(main_window, text="La receta que intentas\ncrear ya existe")
                label.place(x=375, y=330)
                label.configure(pady=25,anchor=CENTER,font=("Courier New Bold", 20),bg="#FFA07A",fg="Red")
                main_window.after(1000,label.destroy)

            elif nombre_nuevo == "":
                label = Label(main_window, justify=CENTER, text="El nombre de la receta no\n puede estar vacio")
                label.place(x=375, y=330)
                label.configure(pady=25,anchor=CENTER,font=("Mongolian Baiti", 20),bg="#FFA07A",fg="Red")
                main_window.after(1000,label.destroy)
            else:

                main_window.configure(bg="#FFA07A")

                def seleccionar_categoria():
                    destroy_elementos(label_principal,
                                      label_2,
                                      crear_receta_entry,
                                      boton_crear,
                                      boton_regresar)


                    def pagina_anterior():
                        destroy_elementos(lista_categorias_frame,
                                          lista_categorias,
                                          lista_recetas_scrollbar,
                                          label_seleecionar_categoria,
                                          seleccionar_categoria_entry,
                                          boton_pagina_anterior,
                                          boton_seleccionar_categoria)

                        crear_receta()

                    lista_categorias_frame = Frame(main_window)
                    lista_categorias_frame.pack()
                    lista_categorias_frame.configure(bg="#FFA07A")

                    lista_categorias = Text(lista_categorias_frame)
                    # Agregar esta linea para cambiar el fondo del widget
                    # lista_recetas.configure(background="Red")
                    lista_categorias.pack(side=LEFT, fill=BOTH, expand=True)
                    lista_categorias.configure(bg="#FFA07A", font=("MV Boli", 18), fg="#800080", borderwidth=0.5
                                               , height=10)
                    desplegar_categorias = end = '\n'.join(categorias.keys())

                    lista_categorias.insert(index=0.0, chars=desplegar_categorias.title())
                    #configuramos el campo de texto para que muestre el contenido centrado
                    #empezando desde la columna 1 hasta el final
                    lista_categorias.tag_configure("center", justify='center')
                    lista_categorias.tag_add("center", "1.0", "end")
                    #inhabilitamos la edicion del archivo
                    lista_categorias.configure(state='disabled')
                    #creamos la scrollbar dentro de lista_categorias_frame y el atributo 'command' va a controlar la vista
                    #en el eje Y del cuadro de texto
                    lista_recetas_scrollbar = Scrollbar(lista_categorias_frame, command=lista_categorias.yview)
                    #posicionamos el scrollbar a la derecha y la expandimos en vertical
                    lista_recetas_scrollbar.pack(side=RIGHT, fill=Y)
                    lista_categorias.config(yscrollcommand=lista_recetas_scrollbar.set)
                    label_seleecionar_categoria = Label(main_window, text="Ingresa la categoria donde\n"
                                                                          "quieres crear la receta",)
                    label_seleecionar_categoria.place(x=338, y=350)
                    label_seleecionar_categoria.configure(bg="#FFA07A", font=("MV Boli", 20), fg="#800080")
                    seleccionar_categoria_entry = Entry(main_window)
                    seleccionar_categoria_entry.configure(justify=CENTER, width=30, font=("MV Boli",14))
                    seleccionar_categoria_entry.place(x=320, y=450)
                    boton_pagina_anterior = Button(main_window, command=pagina_anterior, text="Pagina anterior")
                    boton_pagina_anterior.place(x=438, y=680)
                    boton_pagina_anterior.configure(font=("MV Boli", 16), fg="#00008B", bg="#FFA07A", bd=3,)

                    def validar_categoria():
                        key_categoria_seleccionada = seleccionar_categoria_entry.get().lower()
                        if key_categoria_seleccionada not in categorias.keys():
                            label_no_existe = Label(main_window, text="El campo esta vacio o el nombre\n "
                                                                 " de la categoria que ingresaste\n no existe "
                                                                 "por favor selecciona\n uno de la lista ", pady=3,
                                                                 font=("Microsoft Sans Serif", 18),
                                                                 fg="Red")
                            label_no_existe.place(x=340, y=500)
                            label_no_existe.configure(pady=25,anchor=CENTER,font=("Mongolian Baiti", 20),bg="#FFA07A",fg="Red")
                            main_window.after(2000, label_no_existe.destroy)

                        else:

                            def receta_creada():
                                destroy_elementos(lista_categorias_frame,
                                                  lista_categorias,
                                                  label_seleecionar_categoria,
                                                  seleccionar_categoria_entry,
                                                  boton_seleccionar_categoria,
                                                  boton_pagina_anterior)

                                nombre_nuevo_sufijo_added = nombre_nuevo + ".txt"

                                def pagina_anterior():
                                    destroy_elementos(label_receta_creada,
                                                      label_ruta_receta_creada,
                                                      label_receta_creada)
                                    crear_receta()

                                path_categoria_receta_nueva = Path(categorias.get(key_categoria_seleccionada))
                                receta_nueva = path_categoria_receta_nueva / nombre_nuevo_sufijo_added
                                receta_nueva.touch()

                                label_receta_creada = Label(main_window, text="La receta ha sido creada exitosamente")
                                label_receta_creada.pack()
                                label_receta_creada.configure(bg="#FFA07A", font=("MV Boli", 26), fg="#800080", justify=CENTER)
                                label_ruta_receta_creada = Label(main_window, text=f"Quedo almacenada en \n{receta_nueva}",
                                                                         font=("Helvetica",28))
                                label_ruta_receta_creada.configure(bg="#FFA07A", font=("MV Boli", 20), fg="#800080")
                                label_ruta_receta_creada.place(x=165, y=250)
                                main_window.after(3000, pagina_anterior)

                            receta_creada()

                    boton_seleccionar_categoria = Button(main_window, command=validar_categoria, text="Confirmar",
                                                                     font=("Helvetica", 14))
                    boton_seleccionar_categoria.configure(font=("MV Boli", 12), fg="#00008B", bg="#FFA07A", bd=3,)
                    boton_seleccionar_categoria.place(x=735, y=445)

                seleccionar_categoria()

        label_principal = Label(main_window, text="Crear recetas")
        label_principal.pack()
        label_principal.configure(font=("MV Boli",32),fg="#00008B",pady=30,bg="#FFA07A", anchor=CENTER)

        crear_receta_entry = Entry(main_window)
        crear_receta_entry.place(x=315, y=280)
        crear_receta_entry.configure(width=30, font=("MV Boli",14), bd=3, justify=CENTER)

        label_2 = Label(main_window, text="Ingresa debajo \nel nombre de la\nreceta que quieres crear")
        label_2.pack()
        label_2.configure(pady=10, font=("MV Boli", 18), fg="#00008B", bg="#FFA07A", anchor=CENTER)

        boton_crear = Button(main_window, command=creacion_receta,text="Crear receta")
        boton_crear.place(x=740, y=278)
        boton_crear.configure(font=("MV Boli", 12), fg="#00008B", bg="#FFA07A", bd=3,)

        boton_regresar = Button(main_window, command=back, text="Regresar")
        boton_regresar.configure(font=("MV Boli", 16), fg="#00008B", bg="#FFA07A", bd=3,)
        boton_regresar.place(x=464, y=480)

    def eliminar_receta():

        main_window.configure(bg="#08425c")
        destroy_elementos(home_page_label,
                          mostrar_recetas_boton,
                          leer_recetas_boton,
                          crear_recetas_boton,
                          eliminar_receta_boton,
                          eliminar_categoria_boton)

        def back():
            destroy_elementos(label_2,
                              boton_regresar,
                              lista_recetas_frame,
                              lista_recetas,
                              boton_regresar,
                              boton_eliminar,
                              eliminar_categoria_boton,
                              eliminar_entry)
            main_tab()


        def eliminacion_de_receta():

            variable_para_guardar_el_nombre_de_la_cosa_a_eliminar = eliminar_entry.get()

            def pagina_anterior():
                destroy_elementos(eliminar_entry,
                                  boton_regresar,
                                  boton_eliminar,
                                  label_confirmar,
                                  entry_confirmar,
                                  boton_confirmar,
                                  boton_pagina_anterior)

                eliminar_receta()

            if variable_para_guardar_el_nombre_de_la_cosa_a_eliminar in recetas.keys():
                destroy_elementos(lista_recetas_frame,
                                  lista_recetas,
                                  lista_recetas_scrollbar,
                                  label_2,
                                  eliminar_entry,
                                  boton_regresar,
                                  boton_eliminar)

                def eliminar():
                    respuesta = entry_confirmar.get().lower()

                    if respuesta == "si":
                        destroy_elementos(label_confirmar,
                                          entry_confirmar,
                                          boton_confirmar,
                                          boton_pagina_anterior,
                                          label_confirmar_2)

                        path_receta_a_eliminar = Path(recetas.get(variable_para_guardar_el_nombre_de_la_cosa_a_eliminar))
                        label_receta_eliminada = Label(main_window, text=f"La receta ha sido eliminada\nExitosamente\n"
                                                                         f"Se encontraba almacenada en \n{path_receta_a_eliminar}")

                        label_receta_eliminada.configure(font=("MV Boli", 20), fg="#ff00ff", background="#08425c", pady=10, anchor=CENTER)
                        label_receta_eliminada.pack()
                        #elimina el elemento en el path almacenado en la variable path_receta_a_eliminar
                        path_receta_a_eliminar.unlink()

                        main_window.after(2000, label_receta_eliminada.destroy)
                        main_window.after(2500, main_tab)

                    elif respuesta == "no":
                        main_window.configure(bg="#08425c")

                        def pagina_anterior_2():
                            destroy_elementos(label_confirmar,
                                              entry_confirmar,
                                              boton_confirmar,
                                              boton_pagina_anterior,
                                              label_confirmar_2)

                            label_regresar = Label(main_window, text='La respuesta ingresada fue no\n'
                                                                     'volveras a la pagina anterior en\n'
                                                                     'en unos segundos', font=40, anchor=CENTER)

                            label_regresar.configure(font=("MV Boli", 35), fg="#ff00ff", background="#08425c", anchor=CENTER)
                            label_regresar.pack()

                            main_window.after(2000, label_regresar.destroy)
                            main_window.after(2500, main_tab)

                        pagina_anterior_2()

                    else:
                        label_respuesta_input_incorrecto = Label(main_window, text=('Ingresaste una respuesta incorrecta\n'
                                                                                    'o el espacio esta en blanco\n'
                                                                                    'Escribe "si" o "no" y presiona el boton\n'
                                                                                    '"Confirmar"'))
                        label_respuesta_input_incorrecto.configure(pady=15, font=("MV Boli", 17), fg="red"
                                                                   , background="#08425c", anchor=CENTER)
                        label_respuesta_input_incorrecto.place(x=312, y=330)
                        main_window.after(1500, label_respuesta_input_incorrecto.destroy)

                label_confirmar = Label(main_window, text="Estas seguro de eliminar esta receta?")
                label_confirmar.configure(font=("Arial Italic", 30), fg="red", bg="#08425c", pady=10, anchor=CENTER)
                label_confirmar.pack()
                label_confirmar_2 = Label(main_window,
                                          text='Confirma escribiendo \n"si"\no\n"no"\ny dando click en el boton confirmar')
                label_confirmar_2.configure(font=("MV Boli", 16), bg="#08425c")
                label_confirmar_2.place(x=343, y=105)

                entry_confirmar = Entry(main_window, font=("Helvetica",14),width=14, justify=CENTER)
                entry_confirmar.place(x=440, y=278)

                boton_confirmar = Button(main_window,command=eliminar, text="Confirmar")
                boton_confirmar.configure(font=("Modern Bold", 12),bd=3, fg="blue")
                boton_confirmar.place(x=607, y=275)

                boton_pagina_anterior = Button(main_window, command=pagina_anterior, text="Pagina anterior")
                boton_pagina_anterior.configure(font=("Modern bold", 14),fg="blue",bd=3)
                boton_pagina_anterior.place(x=445, y=550)

            else:
                label_respuesta_input_incorrecto = Label(main_window, text=('  Dejaste el campo en blanco o no  \n'
                                                                            ' escogiste un nombre de la lista\n'
                                                                            '  por favor, escribe uno de la lista'))
                label_respuesta_input_incorrecto.configure(pady=15,font=("MV Boli", 17), fg="red", background="#08425c", anchor=CENTER)
                label_respuesta_input_incorrecto.pack()
                main_window.after(1000, label_respuesta_input_incorrecto.destroy)

        lista_recetas_frame = Frame(main_window)
        lista_recetas_frame.pack()

        lista_recetas = Text(lista_recetas_frame)
        lista_recetas.configure(fg="#ff00ff", background="#08425c",font=("MV Boli", 16), height=15)
        lista_recetas.pack(side=LEFT, fill=BOTH, expand=True)

        desplegar_recetas = end = '\n'.join(recetas.keys())

        lista_recetas.insert(index=0.0, chars=desplegar_recetas.title())
        #configuramos el campo de texto para que muestre el contenido centrado
        #empezando desde la columna 1 hasta el final
        lista_recetas.tag_configure("center", justify='center')
        lista_recetas.tag_add("center", "1.0", "end")
        #inhabilitamos la edicion del archivo
        lista_recetas.configure(state='disabled')
        #creamos la scrollbar dentro de lista_categorias_frame con 'command' va a controlar la vista
        #en Y del cuadro de texto
        lista_recetas_scrollbar = Scrollbar(lista_recetas_frame, command=lista_recetas.yview)
        # expandimos la scrollbar en vertical
        #añadir esta linea para hacer la scrollbar visiblelista_recetas_scrollbar.pack(side = RIGHT, fill = Y)
        lista_recetas_scrollbar.pack_forget()
        lista_recetas.config(yscrollcommand=lista_recetas_scrollbar.set)

        label_2 = Label(main_window, text="Ingresa el nombre de la\nreceta que quieres eliminar")
        label_2.configure(pady=10,font=("MV Boli", 17), fg="#ff00ff", background="#08425c", anchor=CENTER)
        label_2.pack()

        eliminar_entry = Entry(main_window, width=30, font=("Microsoft Sans Serif", 14), bd=3, justify=CENTER)
        eliminar_entry.pack()

        boton_eliminar = Button(main_window, command=eliminacion_de_receta,text="Eliminar",font=("Microsoft Sans Serif", 14))
        boton_eliminar.configure(font=("Modern Bold", 12),bd=3, fg="blue")
        boton_eliminar.place(x=680, y=505)

        boton_regresar = Button(main_window, command=back, text="Regresar")
        boton_regresar.configure(font=("Modern bold", 14),fg="blue",bd=3)
        boton_regresar.place(x=474, y=665)

    def eliminar_categoria():
        main_window.configure(bg="#00a18a")
        destroy_elementos(home_page_label,
                        mostrar_recetas_boton,
                        leer_recetas_boton,
                        crear_recetas_boton,
                        eliminar_receta_boton,
                        eliminar_categoria_boton)

        def back():
            destroy_elementos(eliminar_entry,
                            label_2,
                            boton_regresar,
                            lista_categorias_frame,
                            lista_categorias,
                            boton_regresar,
                            boton_eliminar,
                            eliminar_categoria_boton)

            main_tab()

        def eliminacion_de_categoria():

            variable_para_guardar_el_nombre_de_la_categoria_a_eliminar = eliminar_entry.get()

            def pagina_anterior():
                destroy_elementos(eliminar_entry,
                                boton_regresar,
                                boton_eliminar,
                                label_confirmar,
                                entry_confirmar,
                                boton_confirmar,
                                boton_pagina_anterior)

                eliminar_categoria()

            if variable_para_guardar_el_nombre_de_la_categoria_a_eliminar in categorias.keys():
                destroy_elementos(lista_categorias_frame,
                                lista_categorias,
                                lista_categorias_scrollbar,
                                label_2,
                                eliminar_entry,
                                boton_regresar,
                                boton_eliminar)

                def eliminar():
                    respuesta = entry_confirmar.get().lower()

                    if respuesta == "si":
                        def eliminada ():
                            destroy_elementos(label_confirmar,
                                            entry_confirmar,
                                            boton_confirmar,
                                            boton_pagina_anterior,
                                            label_confirmar_2,
                                            lista_categorias_frame,
                                            lista_categorias,
                                            label_2,
                                            eliminar_entry,
                                            boton_eliminar,
                                            boton_regresar)

                            path_categoria_a_eliminar = Path(categorias.get(variable_para_guardar_el_nombre_de_la_categoria_a_eliminar))
                            label_receta_eliminada = Label(main_window, text=f"La Categoria ha sido eliminada\nExitosamente\n"
                                                                         f"se encontraba almacenada en {path_categoria_a_eliminar}\n"
                                                                             f"volveras a la pagina anterior en unos segundos")
                            label_receta_eliminada.configure(font=("Arial Italic", 30), fg="#12e615",bg="#00a18a",anchor=CENTER)

                            label_receta_eliminada.pack()

                            #elimina el directorio guardado en la variable "path_categoria_a_eliminar"
                            shutil.rmtree(path_categoria_a_eliminar)
                            main_window.after(3500, label_receta_eliminada.destroy)
                            main_window.after(3600, main_tab)

                        eliminada()

                    elif respuesta == "no":

                        def pagina_anterior_2():
                            destroy_elementos(label_confirmar,
                                            entry_confirmar,
                                            boton_confirmar,
                                            boton_pagina_anterior,
                                            label_confirmar_2,
                                            lista_categorias_frame,
                                            lista_categorias,
                                            label_2,
                                            eliminar_entry,
                                            boton_eliminar,
                                            boton_regresar)


                            label_regresar = Label(main_window, text='La respuesta ingresada fue \n"no"\n'
                                                                     'volveras a la pagina anterior en\n'
                                                                     'en unos segundos', font=40, anchor=CENTER)
                            label_regresar.configure(font=("Arial Italic", 30), fg="#12e615",bg="#00a18a",anchor=CENTER)
                            label_regresar.pack()

                            main_window.after(2000,label_regresar.destroy)
                            main_window.after(2500, main_tab)

                        pagina_anterior_2()

                    else:
                        label_respuesta_input_incorrecto = Label(main_window, text=('Ingresaste una respuesta incorrecta\n'
                                                                                    'o el espacio esta en blanco escribe'
                                                                                    '\n"si" o "no"\ny presiona el boton'
                                                                                    '"Confirmar"'))
                        label_respuesta_input_incorrecto.configure(pady=15,font=("MV Boli", 17), fg="#ff0000", bg="#00a18a", anchor=CENTER)
                        label_respuesta_input_incorrecto.place(x=330, y=405)
                        main_window.after(1500, label_respuesta_input_incorrecto.destroy)

                label_confirmar = Label(main_window, text=f'Estas seguro de eliminar esta Categoria?\n'
                                                          f'"{variable_para_guardar_el_nombre_de_la_categoria_a_eliminar.capitalize()}" sera eliminada \n'
                                                          f'"Incluyendo las recetas almacenados en ella!!"',)
                label_confirmar.configure(font=("MV Boli", 30), anchor=CENTER, bg="#00a18a", fg="Red")
                label_confirmar.pack()
                label_confirmar_2 = Label(main_window, text='Confirma escribiendo \n"si"\no\n"no"\ny dando click en el boton confirmar')
                label_confirmar_2.configure(font=("MV Boli", 16), bg="#00a18a")
                label_confirmar_2.place(x=332, y=215)

                entry_confirmar = Entry(main_window)
                entry_confirmar.configure(width=14, font=("MV Boli", 14), bd=3, justify=CENTER)
                entry_confirmar.place(x=410, y=368)

                boton_confirmar = Button(main_window,command=eliminar, text="Confirmar")
                boton_confirmar.configure(font=("Modern Bold", 12),bd=3, fg="blue")
                boton_confirmar.place(x=610, y=369)


                boton_pagina_anterior = Button(main_window, command=pagina_anterior, text="Pagina anterior")
                boton_pagina_anterior.configure(font=("Modern Bold", 12),bd=3, fg="blue")
                boton_pagina_anterior.place(x=450, y=680)

            else:
                label_respuesta_input_incorrecto = Label(main_window, text=('El campo no puede estar en blanco\n'
                                                                            'ingresa uno de la lista de arriba'))
                label_respuesta_input_incorrecto.configure(pady=15,font=("MV Boli", 17), fg="#ff0000", bg="#00a18a", anchor=CENTER)
                label_respuesta_input_incorrecto.pack()
                main_window.after(1000, label_respuesta_input_incorrecto.destroy)

        lista_categorias_frame = Frame(main_window)
        lista_categorias_frame.pack()

        lista_categorias = Text(lista_categorias_frame)
        lista_categorias.configure(fg="#000000", bg="#00a18a", font=("MV Boli", 16), height=15)
        lista_categorias.pack(side=LEFT, fill=BOTH, expand=True)

        desplegar_categorias = end = '\n'.join(categorias.keys())

        lista_categorias.insert(index=0.0, chars=desplegar_categorias.title())
        # configuramos el campo de texto para que muestre el contenido centrado
        # empezando desde la columna 1 hasta el final
        lista_categorias.tag_configure("center", justify='center')
        lista_categorias.tag_add("center", "1.0", "end")
        # inhabilitamos la edicion del archivo
        lista_categorias.configure(state='disabled')
        # creamos la scrollbar dentro de lista_categorias_frame con 'command' va a controlar la vista
        # en Y del cuadro de texto
        lista_categorias_scrollbar = Scrollbar(lista_categorias_frame, command=lista_categorias.yview)
        #añadir esta linea para hacer la scrollbar visiblelista_recetas_scrollbar.pack(side = RIGHT, fill = Y)
        lista_categorias_scrollbar.pack_forget()
        lista_categorias.config(yscrollcommand=lista_categorias_scrollbar.set)

        label_2 = Label(main_window, text="Ingresa el nombre de categoria\nque quieres eliminar",pady=10,
                        font=("MV Boli", 16), fg="#000000")
        label_2.configure(bg="#00a18a",anchor=CENTER)
        label_2.pack()

        eliminar_entry = Entry(main_window, width=30, font=("MV Boli", 14), bd=3, justify=CENTER)
        eliminar_entry.pack()

        boton_eliminar = Button(main_window, command=eliminacion_de_categoria,text="Eliminar",font=("Microsoft Sans Serif", 14)
                             ,bd=3)
        boton_eliminar.configure(font=("Modern Bold", 12),bd=3, fg="blue")
        boton_eliminar.place(x=720, y=504)

        boton_regresar = Button(main_window, command=back, text="Regresar")
        boton_regresar.configure(font=("Modern bold", 14), fg="blue", bd=3)
        boton_regresar.place(x=462, y=710)


    home_page_label = Label(main_window, text="  Cosas bonitas", fg="#ffffff",background="#04254e",font=("Gabriola", 44), anchor=CENTER)

    mostrar_recetas_boton = Button(main_window, text="Mostrar recetas", command=mostrar_recetas_tab, bg="#9004a4",fg="#ffffff", activebackground="#ffe1fe",
                                                bd=3.5,font=("Consolas Bold",14),width=18, pady=5, padx=5)
    mostrar_recetas_boton.place(x=420, y=120)
    leer_recetas_boton = Button(main_window, text="Leer recetas", command=leer_recetas_tab, bg="#9004a4", fg="#ffffff", activebackground="#ffe1fe",
                                              bd=3.5,font=("Consolas Bold",14),width=18, pady=5, padx=5)
    leer_recetas_boton.place(x=420, y=210)
    crear_recetas_boton = Button(main_window, text="Crear receta", command=crear_receta, bg="#9004a4", fg="#ffffff",
                                 activebackground="#ffe1fe", bd=3.5,font=("Consolas Bold",14), width=18, pady=5, padx=5)
    crear_recetas_boton.place(x=420, y=300)

    eliminar_receta_boton = Button(main_window, text="Eliminar receta", command=eliminar_receta, bg="#9004a4",fg="#ffffff",
                                        activebackground="#ffe1fe", bd=3.5,font=("Consolas Bold",14), width=18, pady=5, padx=5)
    eliminar_receta_boton.place(x=420, y=390)

    eliminar_categoria_boton = Button(main_window, text="Eliminar categoria", command=eliminar_categoria,
                                      bg="#9004a4", fg="#ffffff", activebackground="#ffe1fe",
                                   bd=3.5, font=("Consolas Bold", 14), width=18, pady=5, padx=5)
    eliminar_categoria_boton.place(x=420, y=480)

    home_page_label.pack()

main_tab()
mainloop()