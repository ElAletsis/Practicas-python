class Persona:
        def __init__(self, nombre, apellido):
            self.nombre = nombre
            self.apellido = apellido

class Cliente(Persona):
    def __init__(self, nombre, apellido, numero_de_cuenta:int):
        super().__init__(nombre, apellido)
        self.balance = 0.0
        self.numero_de_cuenta = numero_de_cuenta

    def __str__(self):
        return (f"Nombre: {self.nombre}\nApellido: {self.apellido}\nNumero de cuenta: {self.numero_de_cuenta}\n"
                f"Balance: ${self.balance}")

    def retirar(self):
        try:
            cantidad_a_retirar = int(input("Ingresa la cantidad que quieres retirar: "))
            if self.balance < cantidad_a_retirar:
                print("Fondos insuficientes")
            else:
                self.balance -= cantidad_a_retirar
                print(f"Retiro exitoso\nTu balance actual es: ${self.balance}")
        except ValueError:
            print("No puedes ingresar letras en esta operacion")

    def depositar(self):
        try:
            cantidad_a_depositar = int(input("Ingresa la cantidad que quieres depositar: "))
            if cantidad_a_depositar <= 0:
                print("La cantidad a depositar no puede ser 0")
            else:
                self.balance += cantidad_a_depositar
                print(f"Deposito realizado exitosamente\nBalance actual: ${self.balance}")
        except ValueError:
            print("No puedes ingresar letras en esta operacion")

lista_de_clientes={}

def crear_cliente():
    """Crea un instancia de cliente capturando los datos del mismo por inputs,
       despues asigna un numero de cuenta basado en la longitud de la lista de clientes sumandole 1
       para mantener el numero de clientes serializado"""

    numero_de_clientes = len(lista_de_clientes)
    nombre = input("Ingresa el nombre del cliente: ")
    apellido = input("Ingrese el apellido del cliente: ")
    numero_de_cuenta = numero_de_clientes + 1
    #Se crea la instancia de cliente
    cliente = Cliente(nombre, apellido, numero_de_cuenta)
    #Agrega los datos del cliente como diccionario a la lista de clientes donde la llave es el numero de cuenta
    lista_de_clientes.update({cliente.numero_de_cuenta: cliente})
    print(f"El cliente ha sido creado exitosamente")


def buscar_cliente():
    try:
        numero_de_cuenta_cliente = int(input("Ingresa el numero de cuenta del cliente: "))
        cliente = lista_de_clientes.get(numero_de_cuenta_cliente)
        if cliente:
            return cliente
        else:
            print("El cliente no existe")
    except Exception:
        print("Los datos ingresados no son correctos intente nuevamente")

def menu_bancario():

    while True:
        opciones = input("Bienvenido al menu bancario\nQue es lo que quieres hacer?\n"
                         "1) Crear cliente\n2) Realizar retiro\n"
                         "3) Realizar deposito\n4) Salir\nIngresa aqui tu eleccion: ")

        if opciones == "1":
            crear_cliente()
        elif opciones == "2":
            try:
                cliente = buscar_cliente()
                cliente.retirar()
            except:
                pass
        elif opciones == "3":
            try:
                cliente = buscar_cliente()
                cliente.depositar()
            except:
                pass
        elif opciones == "4":
            print("Saliendo...\nGracias por usar el Banco Puercobich 10,000")
            break
        else:
            print("Opcion incorrecta")

menu_bancario()
