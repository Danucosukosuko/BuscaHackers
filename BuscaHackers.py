import ctypes
import psutil
import tkinter as tk
from tkinter import ttk, messagebox

def modify_memory(process_handle, memory_address, new_value):
    ctypes.windll.kernel32.WriteProcessMemory(process_handle, memory_address, ctypes.byref(ctypes.c_int(new_value)), ctypes.sizeof(ctypes.c_int), None)

def modify_value(address, value_entry):
    try:
        target_process_name = "winmine.exe"  # Reemplaza con el nombre del proceso
        memory_address = int(address, 16)  # Convierte la dirección a entero hexadecimal
        new_value = int(value_entry.get())  # Obtiene el nuevo valor
        
        matching_processes = [p for p in psutil.process_iter(['pid', 'name']) if target_process_name in p.info['name']]
        
        if matching_processes:
            process = matching_processes[0]
            process_id = process.info['pid']
            
            process_handle = ctypes.windll.kernel32.OpenProcess(ctypes.c_uint(0x1F0FFF), ctypes.c_int(False), ctypes.c_int(process_id))
            
            modify_memory(process_handle, memory_address, new_value)  # Modifica la dirección de memoria
            
            ctypes.windll.kernel32.CloseHandle(process_handle)
            messagebox.showinfo("Éxito", f"Valor modificado en la dirección {hex(memory_address)} a {new_value}")
        else:
            messagebox.showerror("Error", "No se encontró el proceso.")
        
    except ValueError:
        messagebox.showerror("Error", "Introduce un valor válido.")

def show_help():
    help_window = tk.Toplevel()
    help_window.title("Ayuda")
    
    help_label = ttk.Label(help_window, text="Instrucciones de Ayuda: Tú pones las reglas en el buscaminas", font=("Helvetica", 16))
    help_label.pack(pady=10)
    
    instruction_label1 = ttk.Label(help_window, text="1. Ingresa el nuevo valor para cada memoria. Los valores son: 1º Tiempo de juego. 2º Contador de minas. 3º Minas reales. 4º Tamaño de ancho. 5º Tamaño de alto.", font=("Helvetica", 12))
    instruction_label1.pack(anchor="w", padx=20)
    
    instruction_label2 = ttk.Label(help_window, text="2. Refresca la ventana moviéndola por debajo de la barra de tareas o observa el tablero.", font=("Helvetica", 12))
    instruction_label2.pack(anchor="w", padx=20)

def main():
    global value_entries
    
    window = tk.Tk()
    window.title("Control de Memoria")
    window.geometry("600x350")  # Cambia el tamaño de la ventana
    
    style = ttk.Style()
    style.configure("TButton", font=("Helvetica", 12), padding=10)  # Cambia el estilo del botón
    
    addresses = ["0100579C", "01005194", "010056A4", "010056A8", "010056AC"]  # Direcciones de memoria predefinidas
    
    for address in addresses:
        frame = ttk.Frame(window)
        frame.pack(pady=10)
        
        label = ttk.Label(frame, text=f"Dirección {address}:", font=("Helvetica", 14))
        label.pack(side="left")
        
        value_entry = ttk.Entry(frame, font=("Helvetica", 12))
        value_entry.pack(side="left", padx=10)
        
        value_entries[address] = value_entry  # Guarda la entrada de valor en un diccionario
        
        modify_button = ttk.Button(frame, text=f"Modificar {address}", command=lambda addr=address: modify_value(addr, value_entries[addr]))
        modify_button.pack(side="left")
    
    help_button = ttk.Button(window, text="Ayuda", command=show_help)
    help_button.pack(pady=20)
    
    window.mainloop()

if __name__ == "__main__":
    value_entries = {}  # Diccionario para almacenar las entradas de valor
    main()
