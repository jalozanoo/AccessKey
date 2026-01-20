import re

def evaluate_password_strength(password: str):
    """
    Devuelve (score, label, color)
    score: 0–4
    """

    score = 0

    if len(password) >= 8:
        score += 1
    if re.search(r"[A-Z]", password):
        score += 1
    if re.search(r"[a-z]", password):
        score += 1
    if re.search(r"\d", password):
        score += 1
    if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        score += 1

    if score <= 2:
        return score, "Débil", "red"
    elif score == 3:
        return score, "Media", "orange"
    elif score == 4:
        return score, "Fuerte", "green"
    else:
        return score, "Muy fuerte", "darkgreen"
