import boto3
import os
import json
from fastapi import HTTPException


def ask_claude(prompt: str = "오늘 하루 기분을 알려줘"):
    try:
        # Initialize the Bedrock Runtime client
        bedrock = boto3.client(
            service_name="bedrock-runtime",
            region_name="us-west-2",  # specify your region
            aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
            aws_session_token=os.environ.get("AWS_SESSION_TOKEN"),
        )

        # Create the request body for Claude 3
        request_body = {
            "anthropic_version": "bedrock-2023-05-31",
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 1000,
            "temperature": 0.7,
            "top_p": 0.9,
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
