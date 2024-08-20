import cv2
import os
import numpy as np
import tkinter as tk
from tkinter import filedialog, ttk, PhotoImage
from PIL import Image, ImageTk


class FiltroApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Processamento de Imagens com OpenCV-Python")
        
        # Variáveis de imagem
        self.imagem_original = None
        self.imagem_filtrada_mostrada = None
        self.imagem_contornada = None
        self.estado_atual = None
        
        self.origin_file = None
        
        # Lista para armazenar estados anteriores da imagem filtrada
        self.estados_anteriores = []
        
        # Variáveis de controle para seleção de filtros
        self.filtros_selecionados = []
        
        # Variáveis de controle para intensidade de filtros
        self.kernel_var = tk.IntVar(value = 3)
        
        #Valores sigma do filtro bilateral
        self.sigma_color = tk.IntVar(value = 10)
        self.sigma_space = tk.IntVar(value = 10)
        self.sigma_range = tk.DoubleVar(value = 0.5)
        
        self.threshold_var = tk.DoubleVar(value = 0.30)
        
        # Variáveis de controle para iterações de erosão e dilatação
        self.iteracoes_var = tk.IntVar(value=1)
        
        # Variavel de controle de constante da binarização adaptativa
        self.constante_var = tk.IntVar(value=11)
        
        # Variavel de controle de objetos pequenos
        self.limiar_obj_pequeno = tk.IntVar(value = 5)
        
        # Variavel de controle de filtros
        self.lista_filtros = [[]]
        
        # Variável para mostrar informações sobre os filtros
        self.info_filtro_var = tk.StringVar()
        
        # Variável para mostrar a quantidade de objetos na imagem
        self.info_qtd_obj = tk.StringVar()
        
        # Configuração inicial da intensidade
        self.kernel_var.set(0)
        # Variáveis de controle para os parâmetros de Phansalkar
        self.R_var = tk.DoubleVar(value=0.5)
        self.k_var = tk.DoubleVar(value=0.25)
        self.p_var = tk.DoubleVar(value=2.0)
        self.q_var = tk.DoubleVar(value=10.0)
                
        # Criar widgets
        self.frame_controle = ttk.Frame(root)
        self.frame_controle.pack(padx=10, pady=10, fill=tk.X)

        # Frame para seleção de filtro e intensidade
        
        self.frame_filtros = ttk.Frame(self.frame_controle)
        self.frame_filtros.pack(side=tk.LEFT, padx=5, pady=5, fill=tk.X)

        self.label_filtro = ttk.Label(self.frame_filtros, text="Escolha o(s) filtro(s):")
        self.label_filtro.grid(row=0, column=0, padx=5, pady=5)

        self.combo_filtro = ttk.Combobox(self.frame_filtros,  values=['Binarização Adaptativa (Gaussiana)',
                                                                        'Binarização Normal',
                                                                        'Binarização Adaptativa (Média)',
                                                                        'Binarização Sauvola',
                                                                        'Binarização Phansalkar',
                                                                        'Erosão', 'Dilatação', 'Abertura', 'Fechamento',
                                                                        'Negativa', 'Gaussiano', 'MedianBlur',
                                                                        'Filtro Bilateral', 
                                                                        'Filtro de Preservação', 'Filtro de Detalhes'], state="readonly", width=30)  # Define a largura da Combobox


        self.combo_filtro.grid(row=0, column=1, padx=5, pady=5)
        self.combo_filtro.bind("<<ComboboxSelected>>", self.atualizar_filtro)


        self.label_intensidade = ttk.Label(self.frame_filtros, text="Kernel:")
        self.label_intensidade.grid(row=1, column=0, padx=5, pady=5)
        
        self.slider_intensidade = ttk.Scale(self.frame_filtros, from_=2, to=255, variable=self.kernel_var, orient=tk.HORIZONTAL, length=400, command=self.atualizar_filtro)
        self.slider_intensidade.grid(row=1, column=1, padx=5, pady=5)

        self.entry_intensidade = ttk.Entry(self.frame_filtros, textvariable=self.kernel_var, width=5)
        self.entry_intensidade.grid(row=1, column=2, padx=5, pady=5)
        
        self.label_iteracoes = ttk.Label(self.frame_filtros, text="Iterações:")
        self.label_iteracoes.grid(row=2, column=0, padx=5, pady=5)
        
        self.scale_iteracoes = ttk.Scale(self.frame_filtros, from_=1, to=10, variable=self.iteracoes_var, orient=tk.HORIZONTAL, length=400, command = self.atualizar_filtro)
        self.scale_iteracoes.grid(row=2, column=1, padx=5, pady=5)
        
        self.entry_iteracoes = ttk.Entry(self.frame_filtros, textvariable=self.iteracoes_var, width=5)
        self.entry_iteracoes.grid(row=2, column=2, padx=5, pady=5)

        self.label_constante = ttk.Label(self.frame_filtros, text="Constante:")
        self.label_constante.grid(row=3, column=0, padx=5, pady=5)
        
        self.entry_constante = ttk.Entry(self.frame_filtros, textvariable=self.constante_var, width=5)
        self.entry_constante.grid(row=3, column=2, padx=5, pady=5)
        
        self.scale_constante = ttk.Scale(self.frame_filtros, from_ = 2, to = 150, variable = self.constante_var, orient = tk.HORIZONTAL, length=400, command = self.atualizar_filtro)
        self.scale_constante.grid(row=3, column=1, padx=5, pady=5)
        
        self.label_sigma_space = ttk.Label(self.frame_filtros, text="Sigma space:")
        self.label_sigma_space.grid(row=4, column=0, padx=5, pady=5)

        self.scale_sigma_space = ttk.Scale(self.frame_filtros, from_=0, to=100, variable=self.sigma_space, orient = tk.HORIZONTAL, length=400, command = self.atualizar_filtro)
        self.scale_sigma_space.grid(row=4, column=1, padx=5, pady=5)

        self.entry_sigma_space = ttk.Entry(self.frame_filtros, textvariable=self.sigma_space, width=5)
        self.entry_sigma_space.grid(row=4, column=2, padx=5, pady=5)
        
        self.label_sigma_color = ttk.Label(self.frame_filtros, text="Sigma color:")
        self.label_sigma_color.grid(row=5, column=0, padx=5, pady=5)

        self.scale_sigma_color = ttk.Scale(self.frame_filtros, from_=0, to=100, variable=self.sigma_color, orient = tk.HORIZONTAL, length=400, command = self.atualizar_filtro)
        self.scale_sigma_color.grid(row=5, column=1, padx=5, pady=5)

        self.entry_sigma_color = ttk.Entry(self.frame_filtros, textvariable=self.sigma_color, width=5)
        self.entry_sigma_color.grid(row=5, column=2, padx=5, pady=5)
        
        self.label_sigma_range = ttk.Label(self.frame_filtros, text="Sigma range:")
        self.label_sigma_range.grid(row=6, column=0, padx=5, pady=5)

        self.scale_sigma_range = ttk.Scale(self.frame_filtros, from_=0, to=1, variable=self.sigma_range, orient=tk.HORIZONTAL, length=400, command=self.atualizar_filtro)
        self.scale_sigma_range.grid(row=6, column=1, padx=5, pady=5)

        self.entry_sigma_range = ttk.Entry(self.frame_filtros, textvariable=self.sigma_range, width=5)
        self.entry_sigma_range.grid(row=6, column=2, padx=5, pady=5)

        self.label_threshold = ttk.Label(self.frame_filtros, text="Threshold:")
        self.label_threshold.grid(row=7, column=0, padx=5, pady=5)

        self.scale_threshold = ttk.Scale(self.frame_filtros, from_=0, to=2, variable=self.threshold_var, orient=tk.HORIZONTAL, length=400, command=self.atualizar_filtro)
        self.scale_threshold.grid(row=7, column=1, padx=5, pady=5)

        self.entry_threshold = ttk.Entry(self.frame_filtros, textvariable=self.threshold_var, width=5)
        self.entry_threshold.grid(row=7, column=2, padx=5, pady=5)

        self.label_info_filtro = ttk.Label(self.frame_filtros, textvariable=self.info_filtro_var, wraplength=500)
        self.label_info_filtro.grid(row=8, column=0, columnspan=2, padx=5, pady=5)

        # Frame para botões de ação
        self.frame_botoes_acao = ttk.Frame(self.frame_controle)
        self.frame_botoes_acao.pack(side=tk.RIGHT, padx=5, pady=5, fill=tk.X)
        
        # Botões adicionados
        self.botao_carregar = ttk.Button(self.frame_botoes_acao, text="Carregar Imagem", command=self.carregar_imagem)
        self.botao_carregar.grid(row=0, column=0, padx=5, pady=5)

        self.botao_salvar_imagem = ttk.Button(self.frame_botoes_acao, text="Salvar Imagem", command=self.salvar_imagem_e_filtros)
        self.botao_salvar_imagem.grid(row=1, column=0, padx=5, pady=5)
        
        self.botao_desfazer = ttk.Button(self.frame_botoes_acao, text="Desfazer", command=self.desfazer)
        self.botao_desfazer.grid(row=2, column=0, padx=5, pady=5)

        self.botao_resetar = ttk.Button(self.frame_botoes_acao, text="Resetar", command=self.resetar)
        self.botao_resetar.grid(row=3, column=0, padx=5, pady=5)
        
        self.botao_remover_componentes_pequenos = ttk.Button(self.frame_botoes_acao, text="Remover Componentes Pequenos", command=self.remover_componentes_pequenos)
        self.botao_remover_componentes_pequenos.grid(row=4, column=0, padx=5, pady=5)
        
        self.botao_adicionar_filtro = ttk.Button(self.frame_botoes_acao, text="Adicionar Filtro", command=self.adicionar_filtro)
        self.botao_adicionar_filtro.grid(row=5, column=0, padx=5, pady=5)
        
        self.botao_somar_imagem = ttk.Button(self.frame_botoes_acao, text="Somar Imagem", command=self.somar_imagem)
        self.botao_somar_imagem.grid(row=6, column=0, padx=5, pady=5)
        
        self.botao_contornos_verde = ttk.Button(self.frame_botoes_acao, text="AND", command=self.bitwise_and)
        self.botao_contornos_verde.grid(row=7, column=0, padx=5, pady=5) 
               
        self.botao_contornos_verde = ttk.Button(self.frame_botoes_acao, text="NOT", command=self.bitwise_not)
        self.botao_contornos_verde.grid(row=8, column=0, padx=5, pady=5)
               
        self.botao_contornos_verde = ttk.Button(self.frame_botoes_acao, text="OR", command=self.bitwise_or)
        self.botao_contornos_verde.grid(row=7, column=1, padx=5, pady=5)
               
        self.botao_contornos_verde = ttk.Button(self.frame_botoes_acao, text="XOR", command=self.bitwise_xor)
        self.botao_contornos_verde.grid(row=8, column=1, padx=5, pady=5)
        
        self.botao_contornos_verde = ttk.Button(self.frame_botoes_acao, text="Mostrar Contornos Verdes", command=self.mostrar_contornos_verdes)
        self.botao_contornos_verde.grid(row=9, column=0, padx=5, pady=5)
        
        # Slider para o parâmetro R
        self.label_R = ttk.Label(self.frame_filtros, text="Parâmetro R:")
        self.scale_R = ttk.Scale(self.frame_filtros, from_=0.1, to=1.0, variable=self.R_var, orient=tk.HORIZONTAL, length=400, command=self.atualizar_filtro)
        self.entry_R = ttk.Entry(self.frame_filtros, textvariable=self.R_var, width=5)

        # Slider para o parâmetro k
        self.label_k = ttk.Label(self.frame_filtros, text="Parâmetro k:")
        self.scale_k = ttk.Scale(self.frame_filtros, from_=0.0, to=1.0, variable=self.k_var, orient=tk.HORIZONTAL, length=400, command=self.atualizar_filtro)
        self.entry_k = ttk.Entry(self.frame_filtros, textvariable=self.k_var, width=5)

        # Slider para o parâmetro p
        self.label_p = ttk.Label(self.frame_filtros, text="Parâmetro p:")
        self.scale_p = ttk.Scale(self.frame_filtros, from_=0.0, to=10.0, variable=self.p_var, orient=tk.HORIZONTAL, length=400, command=self.atualizar_filtro)
        self.entry_p = ttk.Entry(self.frame_filtros, textvariable=self.p_var, width=5)

        # Slider para o parâmetro q
        self.label_q = ttk.Label(self.frame_filtros, text="Parâmetro q:")
        self.scale_q = ttk.Scale(self.frame_filtros, from_=0.0, to=20.0, variable=self.q_var, orient=tk.HORIZONTAL, length=400, command=self.atualizar_filtro)
        self.entry_q = ttk.Entry(self.frame_filtros, textvariable=self.q_var, width=5)

        # Esconder os sliders de Phansalkar inicialmente
        self.label_R.grid_remove()
        self.scale_R.grid_remove()
        self.entry_R.grid_remove()

        self.label_k.grid_remove()
        self.scale_k.grid_remove()
        self.entry_k.grid_remove()

        self.label_p.grid_remove()
        self.scale_p.grid_remove()
        self.entry_p.grid_remove()

        self.label_q.grid_remove()
        self.scale_q.grid_remove()
        self.entry_q.grid_remove()

        #Obj Pequeno
        self.entry_obj_peq = ttk.Entry(self.frame_botoes_acao, textvariable = self.limiar_obj_pequeno, width = 5)
        self.entry_obj_peq.grid(row=4, column=3, padx=5, pady=5)
        
        self.scale_obj_peq = ttk.Scale(self.frame_botoes_acao, from_=0, to=255, variable=self.limiar_obj_pequeno, orient=tk.HORIZONTAL, length=100)
        self.scale_obj_peq.grid(row=4, column=2, padx=5, pady=5)

        
        self.label_obj_peq = ttk.Label(self.frame_botoes_acao, text="Limiar")
        self.label_obj_peq.grid(row=4, column=1, padx=5, pady=5)

        # Criar o frame de imagem
        self.frame_imagem = ttk.Frame(root)
        self.frame_imagem.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.label_imagem_original = ttk.Label(self.frame_imagem)
        self.label_imagem_original.grid(row=1, column=0, padx=5, pady=5)

        self.label_imagem_contornos = ttk.Label(self.frame_imagem)
        self.label_imagem_contornos.grid(row=1, column=1, padx=5, pady=5)
    
        self.label_cont_obj = ttk.Label(self.frame_imagem, textvariable=self.info_qtd_obj)
        self.label_cont_obj.grid(row=0, column=1, padx=5, pady=5)
        
        self.label_imagem_filtrada = ttk.Label(self.frame_imagem)
        self.label_imagem_filtrada.grid(row=1, column=2, padx=5, pady=5)

        self.atualizar_imagem()

    def atualizar_imagem(self):
        if self.imagem_original is not None:
            # Se a imagem original for em tons de cinza
            if len(self.imagem_original.shape) != 3:
                imagem_original_rgb = cv2.cvtColor(self.imagem_original, cv2.COLOR_GRAY2RGB)
            else:
                imagem_original_rgb = self.imagem_original  # Manter imagem original se for colorida
            
            # Se a imagem filtrada for em tons de cinza
            if len(self.imagem_filtrada_mostrada.shape) != 3:
                imagem_filtrada_rgb = cv2.cvtColor(self.imagem_filtrada_mostrada, cv2.COLOR_GRAY2RGB)
            else:
                imagem_filtrada_rgb = self.imagem_filtrada_mostrada  # Manter imagem filtrada se for colorida

            # Converter imagem filtrada para o tipo de dados uint8
            imagem_filtrada_rgb = imagem_filtrada_rgb.astype(np.uint8)

            # Converter imagens para o formato do Pillow
            imagem_original_pil = Image.fromarray(imagem_original_rgb)
            imagem_filtrada_pil = Image.fromarray(imagem_filtrada_rgb)

            # Converter imagens para o formato do Tkinter
            imagem_original_tk = ImageTk.PhotoImage(imagem_original_pil)
            imagem_filtrada_tk = ImageTk.PhotoImage(imagem_filtrada_pil)

            # Atualizar os rótulos de imagem na GUI
            self.label_imagem_original.configure(image=imagem_original_tk)
            self.label_imagem_original.image = imagem_original_tk

            self.label_imagem_filtrada.configure(image=imagem_filtrada_tk)
            self.label_imagem_filtrada.image = imagem_filtrada_tk
            
            # Se houver uma imagem contornada
            if self.imagem_contornada is not None:
                # Converter imagem contornada para o formato do Pillow e Tkinter
                imagem_contornada_pil = Image.fromarray(self.imagem_contornada)
                imagem_contornada_tk = ImageTk.PhotoImage(imagem_contornada_pil)    

                # Atualizar o rótulo de imagem dos contornos na GUI
                self.label_imagem_contornos.configure(image=imagem_contornada_tk)
                self.label_imagem_contornos.image = imagem_contornada_tk

            
    def remover_componentes_pequenos(self, tamanho_minimo=1):
        if self.imagem_filtrada_mostrada is not None:
            self.adicionar_filtro()
            tamanho_minimo = self.limiar_obj_pequeno.get()
            # Copiar a imagem binarizada para não modificar a original
            imagem_binaria = self.imagem_filtrada_mostrada.copy()
            
            # Encontrar os componentes conectados na imagem binarizada
            num_labels, labels, stats, _ = cv2.connectedComponentsWithStats(imagem_binaria, connectivity=8)
            # Iterar sobre os componentes conectados e remover aqueles com área menor que o tamanho mínimo
            for label in range(1, num_labels):  # Começa de 1 para ignorar o fundo (0)
                area = stats[label, cv2.CC_STAT_AREA]
                if area < tamanho_minimo:
                    imagem_binaria[labels == label] = 0
            
            self.imagem_filtrada_mostrada = imagem_binaria
            # Atualizar a imagem filtrada mostrada com os componentes pequenos removidos
            self.lista_filtros.append(f"Remoção objetos {tamanho_minimo} pixels" )
            self.atualizar_imagem()

    def resetar(self):
        if self.imagem_original is not None:
            self.estado_atual = self.imagem_original.copy()
            self.imagem_filtrada_mostrada = self.imagem_original.copy()
            self.filtros_selecionados.clear()
            self.estados_anteriores.clear()
            self.lista_filtros.clear()
            self.info_filtro_var.set("")  # Limpar informações sobre filtros
            self.atualizar_imagem()
            
    def adicionar_filtro(self):
        if self.imagem_filtrada_mostrada is not None:
            self.estado_atual = self.imagem_filtrada_mostrada.copy()
            self.estados_anteriores.append(self.estado_atual)
            self.lista_filtros.append(self.info_filtro_var.get())
            print(self.info_filtro_var.get())
            self.atualizar_imagem()

    def atualizar_filtro(self, event=None):
        filtro = self.combo_filtro.get()
        kernel = self.kernel_var.get()
        iteracoes = self.iteracoes_var.get()
        constante = self.constante_var.get()
        sigma_space = self.sigma_space.get()

        # Esconder sliders de Phansalkar se outro filtro for selecionado
        self.label_R.grid_remove()
        self.scale_R.grid_remove()
        self.entry_R.grid_remove()

        self.label_k.grid_remove()
        self.scale_k.grid_remove()
        self.entry_k.grid_remove()

        self.label_p.grid_remove()
        self.scale_p.grid_remove()
        self.entry_p.grid_remove()

        self.label_q.grid_remove()
        self.scale_q.grid_remove()
        self.entry_q.grid_remove()
        
        if self.imagem_original is not None:
            self.imagem_filtrada_mostrada = self.estado_atual.copy()

            if filtro == 'Binarização Phansalkar':
                # Garantir que o tamanho do kernel seja ímpar e maior ou igual a 3
                tamanho_kernel = max(3, int(kernel) | 1)

                # Parâmetros de Phansalkar
                R = self.R_var.get()
                k = self.k_var.get()
                p = self.p_var.get()
                q = self.q_var.get()

                # Mostrar os sliders de Phansalkar
                self.label_R.grid(row=8, column=0, padx=5, pady=5)
                self.scale_R.grid(row=8, column=1, padx=5, pady=5)
                self.entry_R.grid(row=8, column=2, padx=5, pady=5)

                self.label_k.grid(row=9, column=0, padx=5, pady=5)
                self.scale_k.grid(row=9, column=1, padx=5, pady=5)
                self.entry_k.grid(row=9, column=2, padx=5, pady=5)

                self.label_p.grid(row=10, column=0, padx=5, pady=5)
                self.scale_p.grid(row=10, column=1, padx=5, pady=5)
                self.entry_p.grid(row=10, column=2, padx=5, pady=5)

                self.label_q.grid(row=11, column=0, padx=5, pady=5)
                self.scale_q.grid(row=11, column=1, padx=5, pady=5)
                self.entry_q.grid(row=11, column=2, padx=5, pady=5)

                # Calcular a média e o desvio padrão na vizinhança local
                mean = cv2.blur(self.imagem_filtrada_mostrada, (tamanho_kernel, tamanho_kernel))
                mean_square = cv2.blur(self.imagem_filtrada_mostrada ** 2, (tamanho_kernel, tamanho_kernel))
                variance = mean_square - mean ** 2
                stddev = np.sqrt(variance)

                # Calcular o limiar de Phansalkar
                threshold = mean * (1 + p * np.exp(-q * mean)) - k * (stddev / R)

                # Binarizar a imagem usando o limiar calculado
                self.imagem_filtrada_mostrada = (self.imagem_filtrada_mostrada > threshold).astype(np.uint8) * 255

                # Atualizar a informação do filtro aplicado
                self.info_filtro_var.set(f'Binarização Phansalkar - Tamanho do Kernel: {tamanho_kernel}, R: {R:.2f}, k: {k:.2f}, p: {p:.2f}, q: {q:.2f}')
            
            elif filtro == 'Binarização Normal':
                _, self.imagem_filtrada_mostrada = cv2.threshold(self.imagem_filtrada_mostrada, kernel, 255, cv2.THRESH_BINARY)
                self.info_filtro_var.set(f'Binarização Normal - Limiar: {kernel:.0f}')

            elif filtro == 'Binarização Adaptativa (Média)':
                tamanho_kernel = max(3, int(kernel) | 1)
                self.imagem_filtrada_mostrada = cv2.adaptiveThreshold(self.imagem_filtrada_mostrada, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, tamanho_kernel, constante)
                self.info_filtro_var.set(f'Binarização Adaptativa Média - Tamanho do Kernel: {tamanho_kernel}, Constante: {constante:.1f}')

            elif filtro == 'Binarização Adaptativa (Gaussiana)':
                tamanho_kernel = max(3, int(kernel) | 1)
                self.imagem_filtrada_mostrada = cv2.adaptiveThreshold(self.imagem_filtrada_mostrada, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, tamanho_kernel, constante)
                self.info_filtro_var.set(f'Binarização Adaptativa Gaussiana - Tamanho do Kernel: {tamanho_kernel}, Constante: {constante:.1f}')

            elif filtro == 'Erosão':
                tamanho_kernel_erosao = max(3, int(kernel) | 1)
                self.imagem_filtrada_mostrada = cv2.erode(self.imagem_filtrada_mostrada, np.ones((tamanho_kernel_erosao, tamanho_kernel_erosao), np.uint8), iterations=iteracoes)
                self.info_filtro_var.set(f'Erosão - Tamanho do Kernel: {tamanho_kernel_erosao}, Iterações: {iteracoes}')

            elif filtro == 'Dilatação':
                tamanho_kernel_dilatacao = max(3, int(kernel) | 1)
                self.imagem_filtrada_mostrada = cv2.dilate(self.imagem_filtrada_mostrada, np.ones((tamanho_kernel_dilatacao, tamanho_kernel_dilatacao), np.uint8), iterations=iteracoes)
                self.info_filtro_var.set(f'Dilatação - Tamanho do Kernel: {tamanho_kernel_dilatacao}, Iterações: {iteracoes}')

            elif filtro == 'Abertura':
                tamanho_kernel_abertura = max(3, int(kernel) | 1)
                self.imagem_filtrada_mostrada = cv2.morphologyEx(self.imagem_filtrada_mostrada, cv2.MORPH_OPEN, np.ones((tamanho_kernel_abertura, tamanho_kernel_abertura), np.uint8))
                self.info_filtro_var.set(f'Abertura - Tamanho do Kernel: {tamanho_kernel_abertura}')

            elif filtro == 'Fechamento':
                tamanho_kernel_fechamento = max(3, int(kernel) | 1)
                self.imagem_filtrada_mostrada = cv2.morphologyEx(self.imagem_filtrada_mostrada, cv2.MORPH_CLOSE, np.ones((tamanho_kernel_fechamento, tamanho_kernel_fechamento), np.uint8))
                self.info_filtro_var.set(f'Fechamento - Tamanho do Kernel: {tamanho_kernel_fechamento}')

            elif filtro == 'Negativa':
                self.imagem_filtrada_mostrada = cv2.bitwise_not(self.imagem_filtrada_mostrada)
                self.info_filtro_var.set('Negativa aplicada')

            elif filtro == 'Gaussiano':
                tamanho_kernel = max(3, int(kernel) | 1)
                self.imagem_filtrada_mostrada = cv2.GaussianBlur(self.imagem_filtrada_mostrada, (tamanho_kernel, tamanho_kernel), 0)
                self.info_filtro_var.set(f'Filtro Gaussiano - Tamanho do Kernel: {tamanho_kernel}')

            elif filtro == 'MedianBlur':
                tamanho_kernel = max(3, int(kernel) | 1)
                self.imagem_filtrada_mostrada = cv2.medianBlur(self.imagem_filtrada_mostrada, tamanho_kernel)
                self.info_filtro_var.set(f'Median Blur - Tamanho do Kernel: {tamanho_kernel}')

            elif filtro == 'Filtro Bilateral':
                diametro = max(3, int(kernel) | 1)
                sigma_color = self.sigma_color.get()
                sigma_space = self.sigma_space.get()
                self.imagem_filtrada_mostrada = cv2.bilateralFilter(self.imagem_filtrada_mostrada, diametro, sigma_color, sigma_space)
                self.info_filtro_var.set(f'Filtro Bilateral - Diâmetro: {diametro}, Sigma space: {sigma_space:.1f}, Sigma Color: {sigma_color:.1f}')

            elif filtro == 'Binarização Sauvola':
                tamanho_kernel = max(3, int(kernel) | 1)
                sauvola_threshold = self.threshold_var.get()
                self.imagem_filtrada_mostrada = cv2.ximgproc.niBlackThreshold(self.imagem_filtrada_mostrada, 255, cv2.THRESH_BINARY, tamanho_kernel, sauvola_threshold, cv2.ximgproc.BINARIZATION_SAUVOLA)
                self.info_filtro_var.set(f'Binarização Sauvola - Tamanho do Kernel: {tamanho_kernel}, Threshold: {sauvola_threshold:.2f}')

            elif filtro == 'Filtro de Preservação':
                sigma_space = self.sigma_space.get()
                sigma_range = self.sigma_range.get()
                self.imagem_filtrada_mostrada = cv2.edgePreservingFilter(self.imagem_filtrada_mostrada, flags=1, sigma_s=sigma_space, sigma_r=sigma_range)
                self.info_filtro_var.set(f'Filtro de Preservação - Sigma space: {sigma_space:.1f}, Sigma Range: {sigma_range:.2f}')

            elif filtro == 'Filtro de Detalhes':
                sigma_space = self.sigma_space.get()
                sigma_range = self.sigma_range.get()
                imagem_colorida = cv2.cvtColor(self.imagem_filtrada_mostrada, cv2.COLOR_GRAY2RGB)
                aux = cv2.detailEnhance(imagem_colorida, sigma_s=sigma_space, sigma_r=sigma_range)
                self.imagem_filtrada_mostrada = cv2.cvtColor(aux, cv2.COLOR_RGB2GRAY)
                self.info_filtro_var.set(f'Filtro de Detalhes - Sigma space: {sigma_space:.1f}, Sigma Range: {sigma_range:.2f}')

            # Atualizar a imagem mostrada
            self.atualizar_imagem()



    
    def somar_imagem(self):
        if self.imagem_original is not None and self.imagem_filtrada_mostrada is not None:
            # Somar a imagem filtrada à original
            imagem_somada = cv2.add(self.imagem_original, self.imagem_filtrada_mostrada)
            # Atualizar a imagem filtrada mostrada para a imagem somada
            self.imagem_filtrada_mostrada = imagem_somada
            self.estado_atual = imagem_somada
            # Atualizar a imagem mostrada na interface
            self.atualizar_imagem()

    def mostrar_contornos_verdes(self):
        if self.imagem_filtrada_mostrada is not None:
            # Encontrar contornos na imagem filtrada
            contours, _ = cv2.findContours(self.imagem_filtrada_mostrada, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            self.info_qtd_obj.set(f"Objetos encontrados {len(contours)}")
            # Desenhar contornos em uma cópia colorida da imagem original
            imagem_com_contornos = cv2.cvtColor(self.imagem_original.copy(), cv2.COLOR_GRAY2RGB)
            cv2.drawContours(imagem_com_contornos, contours, -1, (0, 255, 0), 2)  # Desenhar contornos em verde
            
            # Mostrar imagem com contornos usando cv2.imshow
            self.imagem_contornada = imagem_com_contornos
            self.atualizar_imagem()
            
    def carregar_imagem(self):
        # Obter o diretório atual do programa
        pasta_atual = os.getcwd()
        altura_imagem = largura_imagem = 400
        
        # Abrir a janela de diálogo para selecionar a imagem
        filename = filedialog.askopenfilename(initialdir=pasta_atual, title="Selecione a Imagem", filetypes=(("Arquivos de Imagem", "*.jpg;*.jpeg;*.png;*.bmp;*.tif"), ("Todos os Arquivos", "*.*")))
        self.origin_file = filename
        if filename:
            # Carregar a imagem original em escala de cinza
            self.imagem_original = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)
            
            # Redimensionar a imagem para 400x400 pixels
            self.imagem_original = cv2.resize(self.imagem_original, (altura_imagem, largura_imagem))
            
            # Resetar e adicionar filtro, se necessário
            self.resetar()
            self.adicionar_filtro()


    def salvar_imagem_e_filtros(self):
        if self.imagem_filtrada_mostrada is not None:
            # Perguntar ao usuário onde salvar a imagem
            pasta_atual = os.getcwd()
            nome_pasta_registros = os.path.join(pasta_atual, "Dados_modificados")
            
            # Criar a pasta "Registros" se não existir
            if not os.path.exists(nome_pasta_registros):
                os.makedirs(nome_pasta_registros)
            
            # Obter o nome da pasta de origem do arquivo
            nome_pasta_origem = os.path.basename(os.path.dirname(self.origin_file))
            
            # Encontrar o próximo número para a pasta modificada
            numero_pasta_modificada = 1
            while True:
                nome_pasta_modificada = os.path.join(nome_pasta_registros, f"{nome_pasta_origem}_modificado{numero_pasta_modificada}")
                if not os.path.exists(nome_pasta_modificada):
                    os.makedirs(nome_pasta_modificada)
                    break
                else:
                    numero_pasta_modificada += 1
            
            # Salvar a imagem original
            caminho_imagem_original = os.path.join(nome_pasta_modificada, "original.jpg")
            cv2.imwrite(caminho_imagem_original, self.imagem_original)
            
            # Salvar a imagem filtrada
            caminho_imagem_filtro = os.path.join(nome_pasta_modificada, "filtro.jpg")
            cv2.imwrite(caminho_imagem_filtro, self.imagem_filtrada_mostrada)
            
            # Salvar a imagem de contorno, se existir
            if self.imagem_contornada is not None:
                caminho_imagem_contorno = os.path.join(nome_pasta_modificada, "contorno.jpg")
                cv2.imwrite(caminho_imagem_contorno, self.imagem_contornada)
            
            # Criar o nome do arquivo de texto
            txt_filename = os.path.join(nome_pasta_modificada, "info.txt")
            
            # Abrir o arquivo de texto para escrita
            with open(txt_filename, "w") as f:
                # Escrever as especificações dos filtros utilizados
                f.write("Filtros utilizados:\n")
                for filtro in self.lista_filtros:
                    f.write(f"{filtro}\n")
                f.write("\n" + self.info_qtd_obj.get() + "\n")

    def desfazer(self):
        if len(self.estados_anteriores) > 0:
            self.imagem_filtrada_mostrada = self.estados_anteriores.pop()
            self.lista_filtros.pop()
            self.atualizar_imagem()
    
    def bitwise_and(self):
        # Abrir a janela de diálogo para selecionar a segunda imagem
        filename = filedialog.askopenfilename()
        if filename:
            # Carregar a segunda imagem
            segunda_imagem = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)
            # Redimensionar a segunda imagem para ter as mesmas dimensões que a imagem modificada
            segunda_imagem = cv2.resize(segunda_imagem, (self.imagem_filtrada_mostrada.shape[1], self.imagem_filtrada_mostrada.shape[0]))
            # Aplicar o bitwise AND entre as duas imagens
            self.imagem_filtrada_mostrada = cv2.bitwise_and(self.imagem_filtrada_mostrada, segunda_imagem)
            self.info_filtro_var.set('Bitwise AND')
            self.atualizar_imagem()
            self.adicionar_filtro()
        else:
            print("Nenhuma imagem selecionada.")
    
    def bitwise_not(self):
        # Abrir a janela de diálogo para selecionar a segunda imagem
        filename = filedialog.askopenfilename()
        if filename:
            # Carregar a segunda imagem
            segunda_imagem = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)
            # Redimensionar a segunda imagem para ter as mesmas dimensões que a imagem modificada
            segunda_imagem = cv2.resize(segunda_imagem, (self.imagem_filtrada_mostrada.shape[1], self.imagem_filtrada_mostrada.shape[0]))
            # Aplicar o bitwise AND entre as duas imagens
            self.imagem_filtrada_mostrada = cv2.bitwise_not(self.imagem_filtrada_mostrada, segunda_imagem)
            self.info_filtro_var.set('Bitwise NOT')
            self.atualizar_imagem()
            self.adicionar_filtro()
        else:
            print("Nenhuma imagem selecionada.")
    
    def bitwise_or(self):
        # Abrir a janela de diálogo para selecionar a segunda imagem
        filename = filedialog.askopenfilename()
        if filename:
            # Carregar a segunda imagem
            segunda_imagem = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)
            # Redimensionar a segunda imagem para ter as mesmas dimensões que a imagem modificada
            segunda_imagem = cv2.resize(segunda_imagem, (self.imagem_filtrada_mostrada.shape[1], self.imagem_filtrada_mostrada.shape[0]))
            # Aplicar o bitwise AND entre as duas imagens
            self.imagem_filtrada_mostrada = cv2.bitwise_or(self.imagem_filtrada_mostrada, segunda_imagem)
            self.info_filtro_var.set('Bitwise OR')
            self.atualizar_imagem()
            self.adicionar_filtro()
        else:
            print("Nenhuma imagem selecionada.")
    
    def bitwise_xor(self):
        # Abrir a janela de diálogo para selecionar a segunda imagem
        filename = filedialog.askopenfilename()
        if filename:
            # Carregar a segunda imagem
            segunda_imagem = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)
            # Redimensionar a segunda imagem para ter as mesmas dimensões que a imagem modificada
            segunda_imagem = cv2.resize(segunda_imagem, (self.imagem_filtrada_mostrada.shape[1], self.imagem_filtrada_mostrada.shape[0]))
            # Aplicar o bitwise AND entre as duas imagens
            self.imagem_filtrada_mostrada = cv2.bitwise_xor(self.imagem_filtrada_mostrada, segunda_imagem)
            self.info_filtro_var.set('Bitwise XOR')
            self.atualizar_imagem()
            self.adicionar_filtro()
        else:
            print("Nenhuma imagem selecionada.")


def main():
    root = tk.Tk()
    root.wm_state('zoomed')
    app = FiltroApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
