import base64
import io
import json
import logging

import boto3
from fastapi import HTTPException
from PIL import Image

from app.configs.environs import config

logger = logging.getLogger(__name__)


def ask_claude(query: str = "오늘 하루 기분을 알려줘", translate: bool = False):
    try:
        # Initialize the Bedrock Runtime client
        bedrock = boto3.client(
            service_name="bedrock-runtime",
            region_name="us-west-2",  # specify your region
            aws_access_key_id=config.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=config.AWS_SECRET_ACCESS_KEY,
            aws_session_token=config.AWS_SESSION_TOKEN,
        )

        # write a prompt template to generate SNS message
        if translate:
            prompt = f"""
            Assistant: You are a good prompt writer for Stable Image Ultra 1.0 model.
                       The query is an SNS post. Write a prompt in English to generate an image for
                       the query. The result should only include the promt and not any extra information
                       like the explanation.
            Human: {query}
            """
        else:
            prompt = f"""
            Assistant: Based on the query, write me a SNS message.
            Human: {query}
            """

        # Create the request body for Claude 3
        request_body = {
            "anthropic_version": "bedrock-2023-05-31",
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 1000,
            "temperature": 0.9,
            "top_p": 1.0,
        }

        # Invoke the model
        response = bedrock.invoke_model(
            modelId="anthropic.claude-3-sonnet-20240229-v1:0",  # Claude 3 Sonnet model
            body=json.dumps(request_body),
        )

        # Parse the response
        response_body = json.loads(response["body"].read())
        generated_text = response_body["content"][0]["text"]

        return {"generated_content": generated_text}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def generate_image_for_post(prompt, output_filename="generated_image.png"):
    # Create a Bedrock Runtime client
    bedrock_runtime = boto3.client(
        service_name="bedrock-runtime",
        region_name="us-west-2",  # Change to your preferred region
        aws_access_key_id=config.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=config.AWS_SECRET_ACCESS_KEY,
        aws_session_token=config.AWS_SESSION_TOKEN,
    )
    logger.debug(f"prompt: {prompt}")
    image_prompt = ask_claude(prompt, translate=True)

    prompt_template = f"""
    {image_prompt["generated_content"]}
    """

    request_body = {"prompt": prompt_template, "mode": "text-to-image"}

    try:
        # Call the Titan Image Generator model
        logger.debug(prompt_template)
        response = bedrock_runtime.invoke_model(
            modelId="stability.stable-image-ultra-v1:0", body=json.dumps(request_body)
        )

        # Parse the response
        response_body = json.loads(response.get("body").read())

        # Get the base64 encoded image
        base64_image = response_body.get("images")[0]

        # Decode the image
        image_data = base64.b64decode(base64_image)

        # Create an image from the decoded data
        image = Image.open(io.BytesIO(image_data))

        # Save the image
        image.save(output_filename)
        print(f"Image successfully generated and saved as {output_filename}")

        # Display the image (optional)
        # image.show()

        return output_filename

    except Exception as e:
        print(f"Error generating image: {str(e)}")
        return False
