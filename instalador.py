import os
import subprocess
import customtkinter as ctk
from tkinter import filedialog, messagebox

# Configuração inicial da interface
ctk.set_appearance_mode("System")  # "System", "Dark", "Light"
ctk.set_default_color_theme("blue")  # "blue", "dark-blue", "green"

# Criar janela principal
janela = ctk.CTk()
janela.title("Instalador Automático")
janela.geometry("600x600")
janela.resizable(False, False)

# Variáveis globais
checkboxes = []
pasta_selecionada = ""


# Função para selecionar a pasta
def selecionar_pasta():
    global pasta_selecionada
    pasta = filedialog.askdirectory()
    if pasta:
        pasta_selecionada = pasta
        listar_executaveis(pasta)


# Função para listar os executáveis na pasta
def listar_executaveis(pasta):
    for widget in frame_checkboxes.winfo_children():
        widget.destroy()

    global checkboxes
    checkboxes = []

    arquivos = [f for f in os.listdir(pasta) if f.lower().endswith('.exe')]

    if not arquivos:
        messagebox.showwarning("Atenção", "Nenhum arquivo .exe encontrado na pasta selecionada.")
        return

    for arquivo in arquivos:
        var = ctk.BooleanVar()
        chk = ctk.CTkCheckBox(frame_checkboxes, text=arquivo, variable=var)
        chk.pack(anchor="w", pady=2)
        checkboxes.append((arquivo, var))


# Função para instalar os selecionados
def instalar_selecionados():
    selecionados = [arquivo for arquivo, var in checkboxes if var.get()]

    if not selecionados:
        messagebox.showinfo("Atenção", "Nenhum executável selecionado.")
        return

    resposta = messagebox.askyesno("Confirmação", "Deseja realmente instalar os executáveis selecionados?")

    if resposta:
        for arquivo in selecionados:
            caminho = os.path.join(pasta_selecionada, arquivo)
            try:
                subprocess.run([caminho, "/S", "/silent", "/quiet"], check=True)
                print(f"Instalado: {arquivo}")
            except Exception as e:
                print(f"Erro ao instalar {arquivo}: {e}")
        messagebox.showinfo("Concluído", "Instalação dos selecionados concluída.")


# ✅ Função para instalar tudo
def instalar_tudo():
    if not pasta_selecionada:
        messagebox.showwarning("Atenção", "Selecione uma pasta primeiro.")
        return

    resposta = messagebox.askyesno("Confirmação", "Deseja realmente instalar TODOS os executáveis da pasta?")

    if resposta:
        arquivos = [f for f in os.listdir(pasta_selecionada) if f.lower().endswith('.exe')]

        if not arquivos:
            messagebox.showwarning("Atenção", "Nenhum arquivo .exe encontrado na pasta.")
            return

        for arquivo in arquivos:
            caminho = os.path.join(pasta_selecionada, arquivo)
            try:
                subprocess.run([caminho, "/S", "/silent", "/quiet"], check=True)
                print(f"Instalado: {arquivo}")
            except Exception as e:
                print(f"Erro ao instalar {arquivo}: {e}")

        messagebox.showinfo("Concluído", "Instalação de todos os executáveis concluída.")


# Label título
label = ctk.CTkLabel(janela, text="Instalador Automático", font=("Segoe UI", 20, "bold"))
label.pack(pady=10)

# Botão selecionar pasta
btn_pasta = ctk.CTkButton(janela, text="Selecionar Pasta", command=selecionar_pasta)
btn_pasta.pack(pady=5)

# Frame scrollável para checkboxes
frame_scroll = ctk.CTkScrollableFrame(janela, width=500, height=400)
frame_scroll.pack(padx=20, pady=10, fill="both", expand=False)

frame_checkboxes = frame_scroll

# Botões de instalação
btn_instalar = ctk.CTkButton(janela, text="Instalar Selecionados", command=instalar_selecionados)
btn_instalar.pack(pady=5)

btn_instalar_tudo = ctk.CTkButton(janela, text="Instalar Tudo", command=instalar_tudo)
btn_instalar_tudo.pack(pady=5)


# Executar janela
janela.mainloop()
