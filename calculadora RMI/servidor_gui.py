import Pyro4
import math
import tkinter as tk
from tkinter import scrolledtext

@Pyro4.expose
class CalculadoraAvancada:
    def somar(self, a, b): return a + b
    def subtrair(self, a, b): return a - b
    def multiplicar(self, a, b): return a * b
    def dividir(self, a, b): 
        if b == 0: raise ValueError("Divisão por zero!")
        return a / b
    def raiz_quadrada(self, a): 
        if a < 0: raise ValueError("Raiz de número negativo!")
        return math.sqrt(a)
    def exponenciacao(self, base, expoente): return base ** expoente

class ServidorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Servidor da Calculadora Distribuída")
        
        # Frame principal
        self.frame = tk.Frame(root, padx=20, pady=20)
        self.frame.pack()
        
        # Área de texto para logs
        self.log_area = scrolledtext.ScrolledText(self.frame, width=50, height=15)
        self.log_area.pack(pady=10)
        self.log_area.insert(tk.END, "Iniciando servidor...\n")
        
        # Botões
        self.btn_frame = tk.Frame(self.frame)
        self.btn_frame.pack()
        
        self.start_btn = tk.Button(self.btn_frame, text="Iniciar Servidor", command=self.iniciar_servidor)
        self.start_btn.pack(side=tk.LEFT, padx=5)
        
        self.stop_btn = tk.Button(self.btn_frame, text="Parar Servidor", state=tk.DISABLED, command=self.parar_servidor)
        self.stop_btn.pack(side=tk.LEFT, padx=5)
        
        self.daemon = None
        self.uri = None
    
    def log(self, message):
        self.log_area.insert(tk.END, message + "\n")
        self.log_area.see(tk.END)
    
    def iniciar_servidor(self):
        try:
            self.log("Iniciando servidor RMI...")
            self.daemon = Pyro4.Daemon()
            self.uri = self.daemon.register(CalculadoraAvancada)
            
            self.log(f"Servidor iniciado com sucesso!")
            self.log(f"URI do objeto: {self.uri}")
            self.log("Aguardando conexões de clientes...")
            
            self.start_btn.config(state=tk.DISABLED)
            self.stop_btn.config(state=tk.NORMAL)
            
            # Inicia o servidor em uma thread separada para não bloquear a GUI
            import threading
            threading.Thread(target=self.daemon.requestLoop, daemon=True).start()
            
        except Exception as e:
            self.log(f"Erro ao iniciar servidor: {str(e)}")
    
    def parar_servidor(self):
        if self.daemon:
            self.log("Parando servidor...")
            self.daemon.shutdown()
            self.log("Servidor parado com sucesso.")
            self.start_btn.config(state=tk.NORMAL)
            self.stop_btn.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    app = ServidorGUI(root)
    root.mainloop()