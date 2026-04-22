media_aprovacao = 7
max_notas = 3
nota_maxima = 10


def calcular_situacao(notas):
    if not notas:
        return 0.0, "Sem notas"
    media = sum(notas) / len(notas)
    situacao = "Aprovado" if media >= media_aprovacao else "Reprovado"
    return media, situacao

def validar_nota(nota_str):
    try:
        nota = float(nota_str.replace(',', '.'))
    except ValueError:
        return None, "Nota inválida, Digite apenas números!"
    
    if not (0 <= nota <= nota_maxima):
        return None, f"A nota deve ser entre 0 e {nota_maxima}!"
    
    return nota, None 
