import os
import json
from google import genai
from google.genai import types
from .tools import create_study_plan_tool, analyze_student_weaknesses

#defining the tools to our gemini client
def get_agent_tools_declaration():
    create_plan_func = types.FunctionDeclaration(
        name="create_study_plan_tool",
        description="Creates an automated study plan in the database for the user based on their weak quiz topics.",
        parameters=types.Schema(
            type="OBJECT",
            properties={
                "plan_title": types.Schema(
                    type="STRING",
                    description="Title of the study plan, e.g., 'Django Revision Plan'"
                ),
                "duration_days": types.Schema(
                    type="INTEGER",
                    description="Duration of the plan in days (default: 3)"
                )
            },
            required=["plan_title"]
        )
    )
    return types.Tool(function_declarations=[create_plan_func])

def run_study_mate_agent(user, user_message):
    api_key = os.getenv("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    system_instruction = f"""
    You are StudyMate AI, an intelligent agentic assistant for an e-learning platform.
    Active User: {user.username} (Role: {user.role})
    
    Rules:
    1. If the user asks for a study plan or revision schedule, call the tool `create_study_plan_tool`.
    2. Always respect user security boundaries and perform database actions through the tools only, not from yourself.
    3. Respond clearly and concisely in Arabic or English based on the user prompt.
    4. if there a mixed strings Arabic with English you have to keep the -right to left- writing to give the user 
       more suitable srting.
    """

    tools = [get_agent_tools_declaration()]
    
    response = client.models.generate_content(
        model="gemin-3.6-flash",
        contents=user_message,
        config=types.GenerateContentConfig(
            system_instruction=system_instruction,
            tools=tools,
            temperature=0.2
        )
    )
###########################################
    if response.function_calls:
        for call in response.function_calls:
            if call.name == "create_study_plan_tool":
                args = call.args
                result = create_study_plan_tool(
                    user=user,
                    plan_title=args.get("plan_title", "Custom Study Plan"),
                    duration_days=int(args.get("duration_days", 3))
                )
                
                return f"✅Study plan created successfully in the database!\n\n📋 **Study title:** {result['plan_title']}\n📅 **Lessons**\n" + "\n".join([f"- {item}" for item in result['assigned_modules']])

    return response.text