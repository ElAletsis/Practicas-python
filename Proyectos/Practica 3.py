from random import choice
import string

#Adivina la palabra secreta

words = ['cosas', 'bonitas', 'palabras', 'hermosas']
#Selecciona de manera aleatoria una palabra dentro de la lista "words" 
secret_word = choice(words)
#Genera el alfabeto en minusculas en forma de lista
alphabet = [l for l in string.ascii_lowercase]
#Genera una lista de "-" como strings con una longitud basada en la el largo de "secret_word"
hidden_word_list = ['-'] * len(secret_word)
#Almacenara las letras que se ingresen por el input y que no esten en "secret_word"
incorrect_letters = []
lives = -2

def choose_a_letter(lives):
    '''
    Simula el juego del ahorcado tomando un valor numerico que representa la cantidad de vidas o intentos restantes
    en caso de que lives
    '''


    print(secret_word)

    #Usamos el metodo "strip()" para eliminar espacios en blanco en caso de que el usuario deje uno despues de ingresar la letra
    letter = input("Choose a letter: ").lower().strip()
    while letter not in alphabet:
        print("You need to choose a letter, not numbers or special characters: ")
        letter = input("Choose a letter: ").lower()
        
    if letter in secret_word:
        #Si la letra ingresada en el input esta en "word_secret" reemplaza el "-" del indice de "i" 
        #generado en el bucle for con la letra ingresada en el input
        for i, letra in enumerate(secret_word): 
            #Si la letra ingresada en el input esta en "word_secret" reemplaza el "-" del indice de "i" generado en el bucle for
            if letra == letter:
                hidden_word_list[i] = letra
        print(f"Nice you guess one letter of the secret word here you have the\nletters you guessed\n{hidden_word_list}")
    #Si la letra no esta en "secret_word" resta una vida 
    elif letter not in secret_word:
        incorrect_letters.append(letter)
        lives -= 1
        print(f"""Bad choice :( the letter you choose is not in the secret word
Here you have the letters that are not in the secret word
{incorrect_letters}
lives left {lives}""")
    return lives



#Este bucle controla la llamada de la funcion, mientras la variable "lives" sea mayor a 0 o haya letras sin adivinar se continuara llamando a la funcion
while True:
    #La variable 'lives' toma el valor retornado por la funcion
    lives = choose_a_letter(lives)
    counter = hidden_word_list.count('-')
    if lives == 0:
        print("You have no lives left\nGame over")
        break
    elif "-" not in hidden_word_list:
        print(f"Congrats you've guessed the secret word\nThe secret word is '{secret_word}'")
        break