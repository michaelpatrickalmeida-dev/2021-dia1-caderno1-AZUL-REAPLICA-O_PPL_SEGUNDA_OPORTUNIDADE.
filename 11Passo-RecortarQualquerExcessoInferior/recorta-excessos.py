from PIL import Image
import os
import shutil

def encontrar_faixa_inferior(imagem, pixels_corte_inferior=750):
    """
    Calcula a nova altura da imagem subtraindo os pixels informados da borda inferior.
    Retorna a posição Y de corte ou None caso a imagem seja menor que o corte desejado.
    """
    largura, altura = imagem.size
    
    if altura > pixels_corte_inferior:
        return altura - pixels_corte_inferior
    
    return None

def processar_imagens(pasta_origem, pasta_destino):
    """
    Processa todas as imagens da pasta origem, recortando 750px do fundo
    e copiando todas para a pasta destino.
    """
    # Cria a pasta de destino se não existir
    os.makedirs(pasta_destino, exist_ok=True)
    
    # Lista todos os arquivos da pasta origem
    arquivos = [f for f in os.listdir(pasta_origem) 
                if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff'))]
    
    print(f"Encontrados {len(arquivos)} arquivos para processar")
    
    for arquivo in arquivos:
        caminho_origem = os.path.join(pasta_origem, arquivo)
        caminho_destino = os.path.join(pasta_destino, arquivo)
        
        try:
            # Abre a imagem
            with Image.open(caminho_origem) as imagem:
                print(f"\nProcessando: {arquivo} ({imagem.width}x{imagem.height})")
                
                # Obtém a linha limite cortando 750px da parte inferior
                posicao_corte = encontrar_faixa_inferior(imagem, pixels_corte_inferior=750)
                
                if posicao_corte is not None and posicao_corte > 0:
                    # Se a imagem for maior que 750px, recorta a imagem
                    area_corte = (0, 0, imagem.width, posicao_corte)
                    imagem_recortada = imagem.crop(area_corte)
                    imagem_recortada.save(caminho_destino)
                    print(f"✓ Imagem recortada: {imagem_recortada.width}x{imagem_recortada.height}")
                else:
                    # Se a imagem for menor/igual a 750px, mantém original para evitar erro
                    shutil.copy2(caminho_origem, caminho_destino)
                    print(f"✓ Imagem mantida original (altura menor ou igual a 750px)")
                    
        except Exception as e:
            print(f"✗ Erro ao processar {arquivo}: {e}")
            try:
                shutil.copy2(caminho_origem, caminho_destino)
                print(f"✓ Arquivo copiado mesmo com erro")
            except:
                print(f"✗ Não foi possível copiar o arquivo")

# Função principal
if __name__ == "__main__":
    # Configurações
    pasta_origem = "./questoes"
    pasta_destino = "finalizadas"
    
    print("Iniciando processamento de imagens...")
    print(f"Pasta origem: {pasta_origem}")
    print(f"Pasta destino: {pasta_destino}")
    
    # Verifica se a pasta origem existe
    if not os.path.exists(pasta_origem):
        print(f"Erro: A pasta '{pasta_origem}' não existe!")
        exit(1)
    
    # Executa o processamento
    processar_imagens(pasta_origem, pasta_destino)
    
    print("\n" + "="*50)
    print("Processamento concluído!")
    print(f"Todas as imagens foram salvas em: {pasta_destino}")