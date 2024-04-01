#Contado de palabras y letras en un texto


#Texto en el que vamos a buscar la letra y la palabra
text = "Lorem ipsum dolor sit amet, consectetur adipiscing elit"
text.upper()
letter = input("Ingresa la letra que quieres saber cuentas veces aparece en el texto: ").upper()
#Usamos la funcion count para contar las veces que aparece la letra ingresada en el input dentro de la variable "text"
letter_counter = text.count(letter)
#Devuelve una lista de sub-strings a partir del la variable "text" 
words_list = text.split()
#Contamos la cantidad de palabras de la variable "text" usando "len()"
words_counter = len(words_list)
#Obtenemos el caracter en el indice 0 de la variable "text"
first_letter = text[0]
#Obtenemos el caracter en el indice -1 de la variable "text"
last_letter = text[-1]
#Invertimos el texto original 
reversed_text = text[::-1]
#Devuelve True o False si la palabra "python" aparece en la variable "text"
python_in_text = "python" in text
print(f"""Cantidad de veces que aparece {letter} en el texto {letter_counter},
Total de palabras en el texto {words_counter},
Primer letra {first_letter}, Ultima letra {last_letter},
Texto en orden inverso {reversed_text},
Aparece la palabra 'python' en el texto ? {python_in_text}
""")