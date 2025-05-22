import os
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv
from azure.ai.textanalytics import (
    TextAnalyticsClient,
    ExtractKeyPhrasesAction,
    AnalyzeSentimentAction,
    RecognizePiiEntitiesAction,
)

def analyze_email(email_data):
    subject = email_data.get("subject", "")
    sender = email_data.get("sender", "")
    body_text = email_data.get("body", "")

    # Fusionner les données pour l’analyse
    full_text = f"Subject: {subject}\nFrom: {sender}\n\n{body_text}"

    document = [{"id": "1", "language": "fr", "text": full_text}]
    results = analyze_documents(document)

    analysis_result = {
        "sentiment": {},
        "entities": [],
        "keyPhrases": [],
    }

    for action_results in results:
        for result in action_results:
            if result.kind == "SentimentAnalysis":
                analysis_result["sentiment"] = {
                    "sentiment": result.sentiment,
                    "confidence_scores": {
                        "positive": result.confidence_scores.positive,
                        "neutral": result.confidence_scores.neutral,
                        "negative": result.confidence_scores.negative,
                    },
                }
            elif result.kind == "PiiEntityRecognition":
                entities = []
                for ent in result.entities:
                    entities.append({
                        "text": ent.text,
                        "category": ent.category,
                        "confidence_score": ent.confidence_score,
                    })
                analysis_result["entities"] = entities
            elif result.kind == "KeyPhraseExtraction":
                analysis_result["keyPhrases"] = result.key_phrases
            elif result.is_error:
                return {
                    "sentiment": {"error": result.error},
                    "entities": {"error": result.error},
                    "keyPhrases": {"error": result.error}
                }

    return analysis_result

def analyze_documents(documents):
    load_dotenv()
    endpoint = os.getenv("AZURE_LANGUAGE_ENDPOINT")
    key = os.getenv("AZURE_LANGUAGE_KEY")
    credential = AzureKeyCredential(key)

    text_analytics_client = TextAnalyticsClient(endpoint=endpoint, credential=credential)

    poller = text_analytics_client.begin_analyze_actions(
        documents,
        display_name="Email Text Analysis",
        actions=[
            RecognizePiiEntitiesAction(),
            ExtractKeyPhrasesAction(),
            AnalyzeSentimentAction(),
        ],
    )
    return poller.result()