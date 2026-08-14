from PIL import Image
import os
import shutil

def encontrar_faixa_inferior(imagem, cor_alvo, tolerancia=15):
    """
    Encontra uma faixa de 40px de largura por 4px de altura centrada no meio da imagem.
    Percorre de baixo para cima.
    Retorna a posição Y onde deve ser feito o corte (acima da faixa) ou None se não encontrar.
    """
    largura, altura = imagem.size
    pixels = imagem.load()
    
    # Define a faixa horizontal de 40 pixels ao redor do centro da imagem
    x_inicio = (largura // 2) - 20
    x_fim = (largura // 2) + 20

    # Verifica se a imagem tem largura suficiente para a busca
    if x_inicio < 0 or x_fim > largura:
        return None

    # Percorre a imagem de baixo para cima (precisa de pelo menos 4 pixels de altura)
    for y in range(altura - 1, 3, -1):
        faixa_encontrada = True
        
        # Verifica os 4 pixels de altura (de y-3 até y)
        for dy in range(4):
            pixel_y = y - dy
            
            # Verifica os 40 pixels de largura para cada linha da faixa
            for x in range(x_inicio, x_fim):
                pixel = pixels[x, pixel_y]
                r, g, b = pixel[:3]  # Funciona para RGB e RGBA
                
                # Verifica se a cor está dentro da tolerância do RGB alvo
                if (abs(r - cor_alvo[0]) > tolerancia or 
                    abs(g - cor_alvo[1]) > tolerancia or 
                    abs(b - cor_alvo[2]) > tolerancia):
                    faixa_encontrada = False
                    break
            
            if not faixa_encontrada:
                break
        
        if faixa_encontrada:
            posicao_corte = y - 3  # Corta acima da faixa (remove a faixa e tudo abaixo dela)
            print(f"Faixa encontrada! Cortando na posição y={posicao_corte}")
            return posicao_corte
    
    return None

def processar_imagens(pasta_origem, pasta_destino, cor_alvo):
    """
    Processa todas as imagens da pasta origem, recortando as que têm a faixa inferior
    e copiando todas para a pasta destino.
    """
    os.makedirs(pasta_destino, exist_ok=True)
    
    arquivos = [f for f in os.listdir(pasta_origem) 
                if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff'))]
    
    print(f"Encontrados {len(arquivos)} arquivos para processar")
    
    for arquivo in arquivos:
        caminho_origem = os.path.join(pasta_origem, arquivo)
        caminho_destino = os.path.join(pasta_destino, arquivo)
        
        try:
            with Image.open(caminho_origem) as imagem:
                print(f"\nProcessando: {arquivo} ({imagem.width}x{imagem.height})")
                
                # Procura pela faixa inferior
                posicao_corte = encontrar_faixa_inferior(imagem, cor_alvo)
                
                if posicao_corte is not None and posicao_corte > 0:
                    # Recorta mantendo apenas do topo (0) até o início da faixa (posicao_corte)
                    area_corte = (0, 0, imagem.width, posicao_corte)
                    imagem_recortada = imagem.crop(area_corte)
                    imagem_recortada.save(caminho_destino)
                    print(f"✓ Imagem recortada: {imagem_recortada.width}x{imagem_recortada.height}")
                else:
                    shutil.copy2(caminho_origem, caminho_destino)
                    print(f"✓ Imagem mantida original (sem faixa detectada)")
                    
        except Exception as e:
            print(f"✗ Erro ao processar {arquivo}: {e}")
            try:
                shutil.copy2(caminho_origem, caminho_destino)
                print(f"✓ Arquivo copiado mesmo com erro")
            except:
                print(f"✗ Não foi possível copiar o arquivo")

# Função principal
if __name__ == "__main__":
    pasta_origem = "./questoes"
    pasta_destino = "finalizadas"
    cor_alvo = (35, 31, 32)  # RGB alvo (35, 31, 32)
    
    print("Iniciando processamento de imagens...")
    print(f"Pasta origem: {pasta_origem}")
    print(f"Pasta destino: {pasta_destino}")
    print(f"Cor alvo: RGB{cor_alvo}")
    
    if not os.path.exists(pasta_origem):
        print(f"Erro: A pasta '{pasta_origem}' não existe!")
        exit(1)
    
    processar_imagens(pasta_origem, pasta_destino, cor_alvo)
    
    print("\n" + "="*50)
    print("Processamento concluído!")
    print(f"Todas as imagens foram salvas em: {pasta_destino}")