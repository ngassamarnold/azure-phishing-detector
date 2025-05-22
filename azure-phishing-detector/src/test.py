import os
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv
from azure.ai.textanalytics import (
    TextAnalyticsClient,
    ExtractKeyPhrasesAction,
    AnalyzeSentimentAction,
    RecognizePiiEntitiesAction,
)


load_dotenv()

endpoint = os.getenv("AZURE_LANGUAGE_ENDPOINT")
key = os.getenv("AZURE_LANGUAGE_KEY")

# Create a client
credential = AzureKeyCredential(key)
text_analytics_client = TextAnalyticsClient(endpoint=endpoint, credential=credential)
documents = [
    {"id": "1", "language": "en", "text": "I hated the movie. It was so slow!"},
    {"id": "2", "language": "en", "text": "The movie made it into my top ten favorites. What a great movie!"},
    {"id": "3", "language": "en", "text": "Parker Doe has repaid all of their loans as of 2020-04-25. Their SSN is 859-98-0987. To contact them, use their phone number 555-555-5555. They are originally from Brazil and have Brazilian CPF number 998.214.865-68"},
    {"id": "4", "language": "fr", "text": "Subject: Mise à jour urgente de votre mot de passe Microsoft 365, cliquez ici pour le mettre à jour. Bonjour, Nous avons détecté une activité suspecte sur votre compte Microsoft 365. Pour protéger votre compte, nous vous recommandons de mettre à jour votre mot de passe immédiatement. Cliquez sur le lien ci-dessous pour procéder à la mise à jour. https://password-update-m365 Merci, L'équipe de sécurité Microsoft."},
]
response = text_analytics_client.analyze_sentiment(documents)
successful_responses = [doc for doc in response if not doc.is_error]
# for doc in successful_responses:
#     print(f"Document ID: {doc.id}")
#     print(f"Sentiment: {doc.sentiment}")
#     print(f"Confidence Scores: {doc.confidence_scores}")
#     print(f"Sentences: {doc.sentences}")
#     print()
poller = text_analytics_client.begin_analyze_actions(
    documents,
    display_name="Sample Text Analysis",
    actions=[
        RecognizePiiEntitiesAction(),
        ExtractKeyPhrasesAction(),
        AnalyzeSentimentAction(),
    ],
)

document_results = poller.result()
for doc, action_results in zip(documents, document_results):
    print(f"\nDocument text: {doc}")
    for result in action_results:
        if result.kind == "EntityRecognition":
            print("...Results of Recognize Entities Action:")
            for entity in result.entities:
                print(f"......Entity: {entity.text}")
                print(f".........Category: {entity.category}")
                print(f".........Confidence Score: {entity.confidence_score}")
                print(f".........Offset: {entity.offset}")

        elif result.kind == "PiiEntityRecognition":
            print("...Results of Recognize PII Entities action:")
            for pii_entity in result.entities:
                print(f"......Entity: {pii_entity.text}")
                print(f".........Category: {pii_entity.category}")
                print(f".........Confidence Score: {pii_entity.confidence_score}")

        elif result.kind == "KeyPhraseExtraction":
            print("...Results of Extract Key Phrases action:")
            print(f"......Key Phrases: {result.key_phrases}")

        elif result.kind == "EntityLinking":
            print("...Results of Recognize Linked Entities action:")
            for linked_entity in result.entities:
                print(f"......Entity name: {linked_entity.name}")
                print(f".........Data source: {linked_entity.data_source}")
                print(f".........Data source language: {linked_entity.language}")
                print(
                    f".........Data source entity ID: {linked_entity.data_source_entity_id}"
                )
                print(f".........Data source URL: {linked_entity.url}")
                print(".........Document matches:")
                for match in linked_entity.matches:
                    print(f"............Match text: {match.text}")
                    print(f"............Confidence Score: {match.confidence_score}")
                    print(f"............Offset: {match.offset}")
                    print(f"............Length: {match.length}")

        elif result.kind == "SentimentAnalysis":
            print("...Results of Analyze Sentiment action:")
            print(f"......Overall sentiment: {result.sentiment}")
            print(
                f"......Scores: positive={result.confidence_scores.positive}; \
                neutral={result.confidence_scores.neutral}; \
                negative={result.confidence_scores.negative} \n"
            )

        elif result.is_error is True:
            print(
                f"...Is an error with code '{result.error.code}' and message '{result.error.message}'"
            )

    print("------------------------------------------")