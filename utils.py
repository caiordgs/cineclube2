from datetime import datetime, timedelta
import pytz

# Fuso horário de São Paulo
SP_TZ = pytz.timezone('America/Sao_Paulo')


def converter_para_sp(data_utc):
    """
    Converte uma data UTC para o fuso horário de São Paulo
    """
    if data_utc is None:
        return None

    # Se for string, converte para datetime
    if isinstance(data_utc, str):
        data_utc = datetime.fromisoformat(data_utc.replace('Z', '+00:00'))

    # Se não tiver timezone, assume UTC
    if data_utc.tzinfo is None:
        data_utc = pytz.utc.localize(data_utc)

    # Converte para SP
    return data_utc.astimezone(SP_TZ)


def formatar_data_br(data):
    """
    Formata data no padrão brasileiro: DD/MM/YYYY HH:MM
    """
    if data is None:
        return "Data não disponível"

    data_sp = converter_para_sp(data)
    return data_sp.strftime("%d/%m/%Y %H:%M")


def calcular_dias_restantes(data_sorteio, dias_limite=7):
    """
    Calcula quantos dias faltam para o prazo de assistir o filme.
    Retorna um dicionário com informações sobre o prazo.
    """
    if data_sorteio is None:
        return None

    # Converte para datetime se necessário
    if isinstance(data_sorteio, str):
        data_sorteio = datetime.fromisoformat(data_sorteio.replace('Z', '+00:00'))

    # Garante que tem timezone
    if data_sorteio.tzinfo is None:
        data_sorteio = pytz.utc.localize(data_sorteio)

    # Converte para SP
    data_sorteio_sp = data_sorteio.astimezone(SP_TZ)
    agora_sp = datetime.now(SP_TZ)

    # Calcula o prazo final
    prazo_final = data_sorteio_sp + timedelta(days=dias_limite)

    # Diferença
    diferenca = prazo_final - agora_sp
    dias_restantes = diferenca.days
    horas_restantes = diferenca.seconds // 3600

    return {
        "dias_restantes":  dias_restantes,
        "horas_restantes": horas_restantes,
        "prazo_final":     prazo_final,
        "expirado":        diferenca.total_seconds() < 0,
        "dias_passados":   (agora_sp - data_sorteio_sp).days
    }


def formatar_tempo_restante(info_prazo):
    """
    Formata o tempo restante de forma amigável
    """
    if info_prazo is None:
        return "Prazo não disponível"

    if info_prazo["expirado"]:
        dias_passados = info_prazo["dias_passados"]
        if dias_passados == 7:
            return "⏰ Prazo encerrado hoje"
        return f"⏰ Prazo expirado há {dias_passados - 7} dia(s)"

    dias = info_prazo["dias_restantes"]
    horas = info_prazo["horas_restantes"]

    if dias > 0:
        return f"⏱️ Faltam {dias} dia(s) e {horas}h para assistir"
    elif horas > 0:
        return f"⏱️ Faltam {horas} hora(s) para assistir"
    else:
        return "⏱️ Menos de 1 hora restante!"