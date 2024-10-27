import tkinter as tk
import math

root = tk.Tk()
root.title("Calculator")
root.geometry("350x525")  # Tamaño ajustado de la ventana para incluir todas las conversiones

# Variable asociada al campo de entrada
resultados = tk.StringVar()

# Input Field


resultados= tk.Entry(root, font=("Arial", 24), textvariable=resultados)
resultados.grid(row=1, columnspan=6, sticky=tk.W + tk.E)

# Variables globales para el operador y el primer número
operador = None
primer_numero = None
sistema_numerico = "dec"  # Sistema numérico por defecto

# Función para manejar la selección del sistema numérico
def seleccionar_sistema(sistema):
    global sistema_numerico
    sistema_numerico = sistema
   
    # Habilitar o deshabilitar botones según el sistema seleccionado
    for (text, _, _, button_widget) in buttons:
        if text.isdigit() or text in ['A', 'B', 'C', 'D', 'E', 'F']:
            if sistema == "bin":
                if text not in ['0', '1']:
                    button_widget.config(state=tk.DISABLED)
                else:
                    button_widget.config(state=tk.NORMAL)
            elif sistema == "oct":
                if text not in ['0', '1', '2', '3', '4', '5', '6', '7']:
                    button_widget.config(state=tk.DISABLED)
                else:
                    button_widget.config(state=tk.NORMAL)
            elif sistema == "dec":
                if text.isdigit():
                    button_widget.config(state=tk.NORMAL)
                else:
                    button_widget.config(state=tk.DISABLED)
            elif sistema == "hex":
                if text.isdigit() or text in ['A', 'B', 'C', 'D', 'E', 'F']:
                    button_widget.config(state=tk.NORMAL)
                else:
                    button_widget.config(state=tk.DISABLED)
    actualizar_conversiones()

# Etiquetas y botones para mostrar conversiones
def crear_conversion_seccion(texto, fila):
    seleccionar_button = tk.Button(root, text="-->", command=lambda: seleccionar_sistema(texto.lower()))
    seleccionar_button.grid(row=fila, column=0, padx=10)
   
    label = tk.Label(root, text=texto + ":")
    label.grid(row=fila, column=1, sticky='w', padx=10)
   
    value_label = tk.Label(root, text="")
    value_label.grid(row=fila, column=2, sticky='w', padx=10, columnspan=3)
   
    return value_label

# Etiquetas y botones para mostrar conversiones (modificar las filas para que estén debajo)
hex_value = crear_conversion_seccion("Hex", 11)
dec_value = crear_conversion_seccion("Dec", 12)
oct_value = crear_conversion_seccion("Oct", 13)
bin_value = crear_conversion_seccion("Bin", 14)

def agregar_numero(num):
    current_value = resultados.get()
   
    # Validar el número en base al sistema seleccionado
    if sistema_numerico == "hex" and not all(c in "0123456789ABCDEF" for c in num.upper()):
        return  # No permitir números no válidos en hexadecimal
    elif sistema_numerico == "bin" and not all(c in "01" for c in num):
        return  # No permitir números no válidos en binario
    elif sistema_numerico == "oct" and not all(c in "01234567" for c in num):
        return  # No permitir números no válidos en octal
   
    # Manejar el punto decimal
    if num == ".":
        if sistema_numerico != "dec":
            return  # No permitir el punto en sistemas no decimales
        if "." in current_value:
            return  # No permitir más de un punto en el mismo número

    resultados.delete(0, tk.END)
    resultados.insert(tk.END, current_value + str(num))
    actualizar_conversiones()

def realizar_operacion(oper, primer_numero_entrada):
    global operador, primer_numero
    if primer_numero_entrada.strip() == "":  # Verificar si está vacío o solo contiene espacios
        resultados.delete(0, tk.END)
        resultados.insert(tk.END, "Error")
        return
   
    try:
        # Convertir el primer número según el sistema numérico actual
        if sistema_numerico == "hex":
            primer_numero = int(primer_numero_entrada, 16)
        elif sistema_numerico == "bin":
            primer_numero = int(primer_numero_entrada, 2)
        elif sistema_numerico == "oct":
            primer_numero = int(primer_numero_entrada, 8)
        else:
            primer_numero = float(primer_numero_entrada)
       
        operador = oper
        resultados.delete(0, tk.END)
    except ValueError:
        resultados.delete(0, tk.END)
        resultados.insert(tk.END, "Error")

def calcular_resultado():
    global operador, primer_numero
    try:
        # Convertir el segundo número según el sistema numérico actual
        if sistema_numerico == "hex":
            segundo_numero = int(resultados.get(), 16)
        elif sistema_numerico == "bin":
            segundo_numero = int(resultados.get(), 2)
        elif sistema_numerico == "oct":
            segundo_numero = int(resultados.get(), 8)
        else:
            segundo_numero = float(resultados.get())
       
        resultados.delete(0, tk.END)

        resultado = None
        if operador == "+":
            resultado = primer_numero + segundo_numero
        elif operador == "-":
            resultado = primer_numero - segundo_numero
        elif operador == "*":
            resultado = primer_numero * segundo_numero
        elif operador == "/":
            if segundo_numero != 0:
                resultado = primer_numero / segundo_numero
            else:
                resultado = "Error"
        elif operador == "^":
            resultado = primer_numero ** segundo_numero
        elif operador == "%":
            resultado = primer_numero * (segundo_numero / 100)

        if resultado is not None:
            resultados.insert(tk.END, str(resultado))
        else:
            resultados.insert(tk.END, "Operador no válido")

        actualizar_conversiones()
    except ValueError:
        resultados.insert(tk.END, "Error")

def calcular_factorial():
    try:
        numero = int(resultados.get())
        if numero < 0:
            resultados.delete(0, tk.END)
            resultados.insert(tk.END, "Error")
        else:
            resultado = math.factorial(numero)
            resultados.delete(0, tk.END)
            resultados.insert(tk.END, str(resultado))
            actualizar_conversiones()
    except ValueError:
        resultados.delete(0, tk.END)
        resultados.insert(tk.END, "Error")

def calcular_raiz_cuadrada():
    try:
        numero = float(resultados.get())
        if numero < 0:
            resultados.delete(0, tk.END)
            resultados.insert(tk.END, "Error")
        else:
            resultado = math.sqrt(numero)
            resultados.delete(0, tk.END)
            resultados.insert(tk.END, str(resultado))
            actualizar_conversiones()
    except ValueError:
        resultados.delete(0, tk.END)
        resultados.insert(tk.END, "Error")

def calcular_valor_absoluto():
    try:
        numero = float(resultados.get())
        resultado = abs(numero)
        resultados.delete(0, tk.END)
        resultados.insert(tk.END, str(resultado))
        actualizar_conversiones()
    except ValueError:
        resultados.delete(0, tk.END)
        resultados.insert(tk.END, "Error")

def borrar_ultimo():
    current_value = resultados.get()
    if current_value:
        resultados.delete(len(current_value) - 1, tk.END)
        actualizar_conversiones()

def borrar_todo():
    resultados.delete(0, tk.END)
    hex_value.config(text="")
    dec_value.config(text="")
    oct_value.config(text="")
    bin_value.config(text="")

def actualizar_conversiones():
    try:
        # Detectar el valor decimal a partir del sistema numérico actual
        if sistema_numerico == "hex":
            decimal_value = int(resultados.get(), 16)
        elif sistema_numerico == "bin":
            decimal_value = int(resultados.get(), 2)
        elif sistema_numerico == "oct":
            decimal_value = int(resultados.get(), 8)
        else:
            decimal_value = int(float(resultados.get()))
       
        # Convertir a los otros sistemas
        hex_value.config(text=hex(decimal_value)[2:].upper())
        dec_value.config(text=str(decimal_value))
        oct_value.config(text=oct(decimal_value)[2:])
        bin_value.config(text=bin(decimal_value)[2:])
    except ValueError:
        hex_value.config(text="")
        dec_value.config(text="")
        oct_value.config(text="")
        bin_value.config(text="")

# Botones de la calculadora
buttons = [
    ('A', 5, 0), ('Log', 5, 1), ('√', 5, 2), ('CE', 5, 3), (' <- ', 5, 4),
    ('B', 6, 0), ('^', 6, 1), ('%', 6, 2), ('n!', 6, 3), ('/', 6, 4),
    ('C', 7, 0), ('7', 7, 1), ('8', 7, 2), ('9', 7, 3), ('*', 7, 4),
    ('D', 8, 0), ('4', 8, 1), ('5', 8, 2), ('6', 8, 3), ('-', 8, 4),
    ('E', 9, 0), ('1', 9, 1), ('2', 9, 2), ('3', 9, 3), ('+', 9, 4),
    ('F', 10, 0), ('Abs', 10, 1), ('0', 10, 2), ('.', 10, 3), ('=', 10, 4),
]

# Crear los botones y asignar funciones
for (text, row, col) in buttons:
    button_widget = tk.Button(root, text=text, padx=20, pady=20)
    button_widget.grid(row=row, column=col)
   
    if text.isdigit() or text in ['A', 'B', 'C', 'D', 'E', 'F', '.']:  # Números y hexadecimal
        button_widget.config(command=lambda t=text: agregar_numero(t))
    elif text in ['+', '-', '*', '/', '^', '%']:  # Operaciones
        button_widget.config(command=lambda t=text: realizar_operacion(t, resultados.get()))
    elif text == '=':  # Cálculo del resultado
        button_widget.config(command=calcular_resultado)
    elif text == 'n!':  # Factorial
        button_widget.config(command=calcular_factorial)
    elif text == '√':  # Raíz cuadrada
        button_widget.config(command=calcular_raiz_cuadrada)
    elif text == '<--':  # Borrar último
        button_widget.config(command=borrar_ultimo)
    elif text == 'CE':  # Borrar todo
        button_widget.config(command=borrar_todo)
    elif text == 'Abs':  # Valor absoluto
        button_widget.config(command=calcular_valor_absoluto)

    buttons[buttons.index((text, row, col))] = (text, row, col, button_widget)

# Ejecutar la aplicación
root.mainloop()
