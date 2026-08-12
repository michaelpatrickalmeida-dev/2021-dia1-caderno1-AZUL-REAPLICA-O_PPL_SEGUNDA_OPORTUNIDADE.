from PIL import Image
import os

def encontrar_faixa_padrao(imagem, cor_alvo=(76, 76, 78), tolerancia=15, altura_alvo=18, margem_altura=2, offset_corte=6):
    """
    Percorre o último pixel da direita procurando a faixa vertical com a cor e altura especificadas.
    """
    largura, altura = imagem.size
    pixels = imagem.load()
    
    posicoes_corte = []
    altura_min = altura_alvo - margem_altura  # 16 pixels
    altura_max = altura_alvo + margem_altura  # 20 pixels
    
    y = 0
    while y < altura:
        altura_encontrada = 0
        
        # Avalia sequência vertical de pixels com a cor procurada
        while y + altura_encontrada < altura:
            pixel = pixels[largura - 1, y + altura_encontrada]
            r, g, b = pixel[:3]
            
            if (abs(r - cor_alvo[0]) <= tolerancia and 
                abs(g - cor_alvo[1]) <= tolerancia and 
                abs(b - cor_alvo[2]) <= tolerancia):
                altura_encontrada += 1
            else:
                break
        
        # Verifica se a faixa atende à altura de 18 px (margem entre 16 e 20 px)
        if altura_min <= altura_encontrada <= altura_max:
            posicao_corte = max(0, y - offset_corte)
            posicoes_corte.append((posicao_corte, y, altura_encontrada))
            print(f"Padrão encontrado em y={y} (altura {altura_encontrada}px), cortando em y={posicao_corte}")
            y += altura_encontrada
        else:
            y += max(1, altura_encontrada)
            
    return posicoes_corte

def dividir_imagem_por_faixas(caminho_imagem, pasta_saida):
    imagem = Image.open(caminho_imagem)
    largura, altura = imagem.size
    
    print(f"Imagem carregada: {largura}x{altura} pixels")
    
    cor_alvo = (76, 76, 78)  # RGB (76, 76, 78)
    dados_corte = encontrar_faixa_padrao(imagem, cor_alvo=cor_alvo)
    
    if not dados_corte:
        print("Nenhum padrão encontrado na imagem!")
        return
    
    os.makedirs(pasta_saida, exist_ok=True)
    
    posicao_anterior = 0
    for i, (posicao_corte, y_inicio, alt_faixa) in enumerate(dados_corte):
        if posicao_corte <= posicao_anterior:
            continue
            
        area_corte = (0, posicao_anterior, largura, posicao_corte)
        secao = imagem.crop(area_corte)
        
        nome_arquivo = f"parte_{i+1:03d}.png"
        caminho_completo = os.path.join(pasta_saida, nome_arquivo)
        secao.save(caminho_completo)
        print(f"Salvo: {caminho_completo} ({secao.width}x{secao.height}px)")
        
        posicao_anterior = posicao_corte

    # Salva a última seção final
    if posicao_anterior < altura:
        area_corte = (0, posicao_anterior, largura, altura)
        secao = imagem.crop(area_corte)
        nome_arquivo = f"parte_{len(dados_corte)+1:03d}.png"
        caminho_completo = os.path.join(pasta_saida, nome_arquivo)
        secao.save(caminho_completo)
        print(f"Salvo: {caminho_completo} ({secao.width}x{secao.height}px)")

if __name__ == "__main__":
    caminho_imagem = "colunas_concatenadas_verticalmente.png"  # Atualize para sua imagem
    pasta_saida = "questoes_divididas"                        # Atualize para a pasta de saída
    
    dividir_imagem_por_faixas(caminho_imagem, pasta_saida)
    print("Divisão concluída!")