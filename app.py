import os

from dotenv import load_dotenv

load_dotenv(override=False)

from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from openai import AzureOpenAI
from azure.identity import ManagedIdentityCredential


credential = DefaultAzureCredential(exclude_managed_identity_credential=True)
 

my_endpoint = os.getenv("FOUNDRY_PROJECT_ENDPOINT")

project_client = AIProjectClient(
    endpoint=my_endpoint,
    credential=credential,
)

# Resolve the connected Azure OpenAI resource
connection_name = os.getenv("AZURE_OPENAI_CONNECTION_NAME")
connection = project_client.connections.get(connection_name)
aoai_endpoint = connection.target  # e.g. https://azopenaieastus2.openai.azure.com/

deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT")

my_agent = "HealthcareAssistant"
my_version = "1"

HEALTHCARE_INSTRUCTIONS = (
    "You are a knowledgeable and empathetic healthcare assistant.\n\n"
    "## Capabilities\n"
    "- Provide general health and wellness information.\n"
    "- Explain common symptoms, conditions, and their typical management.\n"
    "- Offer guidance on when to seek professional medical attention.\n"
    "- Share preventive-care tips (nutrition, exercise, sleep, stress management).\n"
    "- Summarize publicly available medication information (uses, common side effects).\n\n"
    "## Guardrails\n"
    "- Always remind users that you are an AI assistant and NOT a licensed medical professional.\n"
    "- Never diagnose conditions or prescribe treatments.\n"
    "- Encourage users to consult a qualified healthcare provider for personal medical decisions.\n"
    "- Do not provide information on controlled substances or illegal drugs.\n"
    "- If a user describes a medical emergency, instruct them to call emergency services immediately.\n\n"
    "## Tone\n"
    "- Warm, professional, and reassuring.\n"
    "- Use clear, jargon-free language unless the user explicitly asks for technical detail."
)

# Create agent if it doesn't exist, otherwise fetch its instructions
try:
    agent_version = project_client.agents.get_version(my_agent, my_version)
    agent_instructions = agent_version.definition["instructions"]
    print(f"Using existing agent '{my_agent}' version {my_version}")
except Exception:
    from azure.ai.projects.models import PromptAgentDefinition

    definition = PromptAgentDefinition(
        model=deployment,
        instructions=HEALTHCARE_INSTRUCTIONS,
        temperature=0.7,
    )
    project_client.agents.create_version(
        agent_name=my_agent,
        definition=definition,
        description="Healthcare assistant agent",
    )
    agent_instructions = HEALTHCARE_INSTRUCTIONS
    print(f"Created agent '{my_agent}' version {my_version}")

# Create an AzureOpenAI client pointed at the connected AOAI resource
from azure.identity import get_bearer_token_provider

token_provider = get_bearer_token_provider(credential, "https://cognitiveservices.azure.com/.default")

aoai_client = AzureOpenAI(
    azure_endpoint=aoai_endpoint,
    azure_ad_token_provider=token_provider,
    api_version="2025-03-01-preview",
)

response = aoai_client.responses.create(
    model=deployment,
    instructions=agent_instructions,
    input=[{"role": "user", "content": "I am sick."}],
)

print(f"Response output: {response.output_text}")