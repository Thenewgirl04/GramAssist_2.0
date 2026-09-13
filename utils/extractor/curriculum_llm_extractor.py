from ollama import chat
from models import Major


def extract_curriculum(curriculum_md):
    response = chat(
        model='qwen3:8b',
        messages=[{'role': 'system',
                   'content': (
                       "Extract the university major curriculum from the "
                       "markdown document provided by the user. Only use information contained "
                       "in the document. DO NOT invent missing information. Ensure to adhere strictly "
                       "to the structure defined in the format and fill the fields available"
                   )
                   },{
                    'role': 'user',
                    'content': curriculum_md
                }],
        format=Major.model_json_schema(),
    )

    return Major.model_validate_json(response.message.content)




