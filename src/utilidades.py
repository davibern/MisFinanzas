def color_positivo_negativo(valor: int | float) -> str:
    """Devuelve estilo CSS de color verde si es positivo o rojo si es negativo,
    para usar en Panda Styler

    Args:
        valor (int | float): cantidad a evaluar

    Returns:
        str: color hexadecimal
    """
    if isinstance(valor, (int, float)):
        if valor > 0:
            return "color: #00c076"  # Verde
        elif valor < 0:
            return "color: #ff4b4b"  # Rojo
    return ""
