def detect_phishing(analysis_result):
    """
    Détermine s'il y a suspicion de phishing à partir des résultats d'analyse Azure.
    Retourne True si phishing suspecté, sinon False.
    """
    phishing_keywords = [
        "mot de passe", "cliquez ici", "urgent", "confidentiel", "vérifiez votre compte",
        "paiement", "identifiant", "sécurité", "mise à jour", "compte bloqué"
    ]

    # Vérifier le sentiment d'abord : si positif, on considère l'email comme sûr
    sentiment = analysis_result.get("sentiment", {}).get("sentiment", "")
    if sentiment == "positive":
        return False

    # Vérifier les entités PII
    if analysis_result.get("entities"):
        for entity in analysis_result["entities"]:
            if entity.get("category") in ["Email", "PhoneNumber", "CreditCardNumber", "BankAccountNumber"]:
                return True

    # Vérifier les phrases clés pour des mots suspects
    for phrase in analysis_result.get("keyPhrases", []):
        for keyword in phishing_keywords:
            if keyword.lower() in phrase.lower():
                return True

    # Si sentiment est négatif, neutre ou mixed, et qu'il y a d'autres signaux, suspicion
    if sentiment in ["negative", "neutral", "mixed"]:
        return True

    return False