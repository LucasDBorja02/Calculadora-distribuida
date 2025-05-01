import Pyro4
import tkinter as tk
from tkinter import ttk, messagebox

class CalculadoraClienteGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Cliente da Calculadora Distribuída")
        
        # Variáveis
        self.uri_var = tk.StringVar()
        self.operacao_var = tk.StringVar(value="+")
        self.num1_var = tk.StringVar()
        self.num2_var = tk.StringVar()
        self.resultado_var = tk.StringVar()
        
        # Frame de conexão
        self.conn_frame = tk.LabelFrame(root, text="Conexão com o Servidor", padx=10, pady=10)
        self.conn_frame.pack(padx=10, pady=5, fill=tk.X)
        
        tk.Label(self.conn_frame, text="URI do Servidor:").grid(row=0, column=0, sticky=tk.W)
        self.uri_entry = tk.Entry(self.conn_frame, textvariable=self.uri_var, width=40)
        self.uri_entry.grid(row=0, column=1, padx=5)
        
        self.connect_btn = tk.Button(self.conn_frame, text="Conectar", command=self.conectar)
        self.connect_btn.grid(row=0, column=2, padx=5)
        
        # Frame de operação
        self.op_frame = tk.LabelFrame(root, text="Operação", padx=10, pady=10)
        self.op_frame.pack(padx=10, pady=5, fill=tk.X)
        
        # Número 1
        tk.Label(self.op_frame, text="Número 1:").grid(row=0, column=0, sticky=tk.W)
        tk.Entry(self.op_frame, textvariable=self.num1_var, width=15).grid(row=0, column=1, padx=5, sticky=tk.W)
        
        # Operação
        tk.Label(self.op_frame, text="Operação:").grid(row=0, column=2, padx=5)
        op_menu = ttk.Combobox(self.op_frame, textvariable=self.operacao_var, 
                              values=["+", "-", "*", "/", "^", "sqrt"], width=5)
        op_menu.grid(row=0, column=3, padx=5)
        
        # Número 2 (visível apenas para operações binárias)
        self.num2_label = tk.Label(self.op_frame, text="Número 2:")
        self.num2_label.grid(row=0, column=4, padx=5, sticky=tk.W)
        self.num2_entry = tk.Entry(self.op_frame, textvariable=self.num2_var, width=15)
        self.num2_entry.grid(row=0, column=5, padx=5, sticky=tk.W)
        
        # Botão calcular
        self.calc_btn = tk.Button(self.op_frame, text="Calcular", command=self.calcular, state=tk.DISABLED)
        self.calc_btn.grid(row=1, column=0, columnspan=6, pady=10)
        
        # Resultado
        self.res_frame = tk.LabelFrame(root, text="Resultado", padx=10, pady=10)
        self.res_frame.pack(padx=10, pady=5, fill=tk.X)
        
        tk.Label(self.res_frame, text="Resultado:").pack(side=tk.LEFT)
        tk.Label(self.res_frame, textvariable=self.resultado_var, font=('Arial', 12, 'bold')).pack(side=tk.LEFT, padx=10)
        
        # Atualiza visibilidade do número 2
        self.operacao_var.trace_add('write', self.atualizar_visibilidade_num2)
        
        self.calculadora = None
    
    def atualizar_visibilidade_num2(self, *args):
        if self.operacao_var.get() == "sqrt":
            self.num2_label.grid_remove()
            self.num2_entry.grid_remove()
        else:
            self.num2_label.grid()
            self.num2_entry.grid()
    
    def conectar(self):
        uri = self.uri_var.get().strip()
        if not uri:
            messagebox.showerror("Erro", "Por favor, informe a URI do servidor")
            return
        
        try:
            self.calculadora = Pyro4.Proxy(uri)
            # Testa a conexão com uma operação simples
            self.calculadora.somar(1, 1)
            
            messagebox.showinfo("Sucesso", "Conectado ao servidor com sucesso!")
            self.calc_btn.config(state=tk.NORMAL)
            self.connect_btn.config(state=tk.DISABLED)
            self.uri_entry.config(state=tk.DISABLED)
            
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao conectar no servidor: {str(e)}")
    
    def calcular(self):
        try:
            num1 = float(self.num1_var.get())
            op = self.operacao_var.get()
            
            if op == "sqrt":
                resultado = self.calculadora.raiz_quadrada(num1)
                expr = f"√{num1} = {resultado}"
            else:
                num2 = float(self.num2_var.get())
                if op == "+":
                    resultado = self.calculadora.somar(num1, num2)
                elif op == "-":
                    resultado = self.calculadora.subtrair(num1, num2)
                elif op == "*":
                    resultado = self.calculadora.multiplicar(num1, num2)
                elif op == "/":
                    resultado = self.calculadora.dividir(num1, num2)
                elif op == "^":
                    resultado = self.calculadora.exponenciacao(num1, num2)
                
                expr = f"{num1} {op} {num2} = {resultado}"
            
            self.resultado_var.set(resultado)
            
            # Mostra a expressão completa no console (opcional)
            print(expr)
            
        except ValueError as ve:
            messagebox.showerror("Erro", f"Valor inválido: {str(ve)}")
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao calcular: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = CalculadoraClienteGUI(root)
    root.mainloop()