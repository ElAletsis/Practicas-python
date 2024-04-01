from random import randint
numero_secreto = randint(1,100)
print(numero_secreto)
nombre = input("Ingresa tu nombre: ")
print (f'''Hola {nombre} he pensado un numero entre 1 y 100
y tienes solo 8 intentos para adivinar cual crees que es el numero''')
intentos = 8
while True:
    try:
        guess = int(input("Ingresa tu respuesta : "))
        if guess == numero_secreto:
            print (f"Felicidades Adivinaste el numero secreto {numero_secreto}!!\nJuego Terminado")
            break       
        elif guess <= 0 or guess > 100:
            print ("El numero que escogiste esta fuera del rango, escoge un numero entre 1 y 100")
            print(f"Intentos restantes {intentos}")
        elif guess != numero_secreto:
            print("Respuesta incorrecta, el numero que elegiste es menor al numero secreto")
            intentos -= 1
            print(f"Intentos restantes {intentos}")
            if intentos == 0:
                print("Te quedaste sin intentos\nEl juego ha finalizado")
                break
    except :
        print("Error!! no puedes ingresar letras, solo numeros")
