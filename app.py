# import os
# import boto3
# import json
# from flask import Flask, request, jsonify
# from flask_cors import CORS # type: ignore

# # AWS Config
# AWS_REGION = "us-east-1"  # Change to your AWS region
# MODEL_ID = "anthropic.claude-v2"  # Change if needed

# # Initialize AWS Bedrock Client
# bedrock = boto3.client("bedrock-runtime", region_name=AWS_REGION)

# # Initialize Flask App
# # app = Flask(__name__)
# CORS(app)  # Enable CORS for API requests

# # API for Real-Time Text Generation
# @app.route("/generate-text", methods=["POST"])
# def generate_text():
#     data = request.json
#     prompt = data.get("prompt", "")

#     if not prompt:
#         return jsonify({"error": "Prompt is required"}), 400

#     try:
#         payload = {
#             "prompt": prompt,
#             "max_tokens": 300,  # Adjust as needed
#             "temperature": 0.7,
#         }

#         response = bedrock.invoke_model(
#             modelId=MODEL_ID,
#             body=json.dumps(payload),
#             accept="application/json",
#             contentType="application/json",
#         )

#         result = json.loads(response["body"].read().decode("utf-8"))
#         return jsonify({"response": result.get("completion", "")})

#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

# # Run Flask App
# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=5000, debug=True)
# from fastapi import FastAPI, File, Form, UploadFile
# import boto3
# import json
# import base64

# app = FastAPI()

# # Initialize Amazon Bedrock runtime client
# bedrock = boto3.client(service_name='bedrock-runtime', region_name='us-east-1')

# # Function to encode image to base64
# def encode_image(image_file):
#     return base64.b64encode(image_file.read()).decode("utf-8")

# # Route for image analysis
# @app.post("/analyze-image")
# async def analyze_image(file: UploadFile = File(...), question: str = Form(...)):
#     base64_image = encode_image(await file.read())

#     payload = {
#         "anthropic_version": "bedrock-2023-05-31",
#         "max_tokens_to_sample": 1000,
#         "messages": [
#             {
#                 "role": "user",
#                 "content": [
#                     {
#                         "type": "image",
#                         "source": {
#                             "type": "base64",
#                             "media_type": file.content_type,
#                             "data": base64_image
#                         }
#                     },
#                     {
#                         "type": "text",
#                         "text": question
#                     }
#                 ]
#             }
#         ]
#     }

#     response = bedrock.invoke_model(
#         modelId="anthropic.claude-3-sonnet-20240229-v1:0",
#         contentType="application/json",
#         accept="application/json",
#         body=json.dumps(payload)
#     )

#     response_body = json.loads(response['body'].read().decode('utf-8'))
#     return {"response": response_body.get("content", "No response generated.")}

# # Route for AI chat
# @app.post("/chat")
# async def chat(prompt: str = Form(...)):
#     payload = {
#         "prompt": f"User: {prompt}\nAI:",
#         "max_tokens_to_sample": 300
#     }

#     response = bedrock.invoke_model(
#         modelId="anthropic.claude-3-sonnet-20240229-v1:0",
#         contentType="application/json",
#         accept="application/json",
#         body=json.dumps(payload)
#     )

#     response_body = json.loads(response['body'].read().decode('utf-8'))
#     return {"response": response_body.get("completion", "No response generated.")}

# from fastapi.middleware.cors import CORSMiddleware

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # Change "*" to your frontend URL for security
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import boto3
import json

# Initialize FastAPI
app = FastAPI()

# Initialize Amazon Bedrock client
bedrock = boto3.client(service_name="bedrock-runtime", region_name="us-east-1")

# Define request model
class ChatRequest(BaseModel):
    user_input: str

# Function to generate response from Claude 3 Sonnet
def generate_response(prompt):
    payload = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 500,
        "messages": [{"role": "user", "content": [{"type": "text", "text": prompt}]}]
    }

    response = bedrock.invoke_model(
        modelId="anthropic.claude-3-sonnet-20240229-v1:0",
        contentType="application/json",
        accept="application/json",
        body=json.dumps(payload)
    )

    response_body = json.loads(response['body'].read().decode('utf-8'))
    return response_body.get("content", "No response generated.")

# API endpoint to chat with the AI bot
@app.post("/chat")
def chat(request: ChatRequest):
    try:
        ai_response = generate_response(request.user_input)
        return {"response": ai_response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Root endpoint
@app.get("/")
def root():
    return {"message": "AI Chatbot for Data Science, Coding Help & Interview Prep"}
