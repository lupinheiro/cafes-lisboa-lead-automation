def score_lead(raw_lead: dict) -> float:
    """Pontuação simples e explicável de um lead, de 0 a 100.

    Critérios:
    - ter website: facilita contacto e enriquecimento posterior (+20)
    - rating do Google: negócio ativo e cuidado (até +30)
    - ter telefone: canal de contacto adicional (+10)

    Uma base de 40 pontos é atribuída a qualquer negócio HORECA
    encontrado na região, por já corresponder ao perfil-alvo.
    """
    score = 40.0

    if raw_lead.get("website"):
        score += 20.0

    rating = raw_lead.get("rating")
    if rating:
        score += min(rating, 5.0) * 6.0

    if raw_lead.get("phone"):
        score += 10.0

    return round(min(score, 100.0), 1)
