print("Inicialización de secret/securebox.")

running = True
while running:
    c = input(">").lower()
    
    if c == "quit" or c == "exit" or c == "q":
        running = False
    elif c == "help" or c == "h":
        print("Te ayudo")

print("Programa finalizado con éxito, espero verte pronto.")