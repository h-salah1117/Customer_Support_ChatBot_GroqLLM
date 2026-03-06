import os
from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import Optional
from groq import Groq
from langchain_core.tools import tool
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser

# --- إعدادات البيئة ---
os.environ["GROQ_API_KEY"] = ""
client = Groq(api_key=os.environ["GROQ_API_KEY"])

app = FastAPI(title="AI Support Agent API")

# --- 1. تعريف الهوية (Pydantic Schema) ---
class SupportTicket(BaseModel):
    issue_type: str = Field(description="نوع المشكلة")
    sentiment: str = Field(description="شعور العميل")
    order_id: Optional[str] = Field(description="رقم الأوردر")
    suggested_reply: str = Field(description="الرد المقترح")

class ChatInput(BaseModel):
    message: str

# --- 2. تعريف الأداة (The Tool) ---
@tool
def check_order_status(order_id: str) -> str:
    """Check the status of a customer order using the Order ID."""
    return f"Order {order_id} is currently in the 'Shipping' stage and will arrive within 48 hours."

parser = JsonOutputParser(pydantic_object=SupportTicket)

# --- 3. منطق الوكيل الذكي (Phase 7 Logic) ---
def run_support_agent(user_query: str):
    # إعداد الـ Prompt
    system_prompt = f"""You are a professional AI customer support agent. 
    Analyze the message and provide a structured JSON response.
    If the user asks about order status and provides an ID, use the check_order_status tool.
    {parser.get_format_instructions()}
    Customer message: {user_query}"""

    # نداء الموديل لمعرفة الحاجة لأداة
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": system_prompt}],
        tools=[{
            "type": "function",
            "function": {
                "name": "check_order_status",
                "description": "Get real-time order tracking info",
                "parameters": {
                    "type": "object",
                    "properties": {"order_id": {"type": "string"}},
                    "required": ["order_id"]
                }
            }
        }]
    )
    
    message = response.choices[0].message
    context_info = "No specific tracking info found."
    
    # تنفيذ الأداة لو طلبت
    if message.tool_calls:
        tool_call = message.tool_calls[0]
        import json
        args = json.loads(tool_call.function.arguments)
        context_info = check_order_status.invoke(args['order_id'])

    # الرد النهائي المنظم
    final_res = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": f"Context: {context_info}"},
            {"role": "user", "content": system_prompt}
        ],
        response_format={"type": "json_object"}
    )
    return parser.parse(final_res.choices[0].message.content)

# --- 4. نقطة النهاية للـ API (Phase 8) ---
@app.post("/chat")
async def chat_endpoint(input_data: ChatInput):
    try:
        result = run_support_agent(input_data.message)
        return {"status": "success", "data": result}
    except Exception as e:
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)