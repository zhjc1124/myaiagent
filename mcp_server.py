from pydantic import BaseModel
import io
from fastmcp import FastMCP, Image
import pyautogui
import io
import base64

mcp_server = FastMCP('mybot')

# 截图工具实现
@mcp_server.tool(name="get_screenshot")
async def get_screenshot() -> str:
    """获取屏幕截图"""
    buffer = io.BytesIO()

    # if the file exceeds ~1MB, it will be rejected by Claude
    screenshot = pyautogui.screenshot()
    screenshot.convert("RGB").save(buffer, format="JPEG", quality=60, optimize=True)
    return Image(data=buffer.getvalue(), format="jpeg")

# 定义点击工具参数模型
class ClickRequest(BaseModel):
    x: int
    y: int
    button: str = "left"

# 点击控制工具实现
@mcp_server.tool(name="perform_click")
async def perform_click(params: ClickRequest) -> dict:
    """模拟鼠标点击操作"""
    pyautogui.click(x=params.x, y=params.y, button=params.button)
    return {"status": "success"}

@mcp_server.prompt()
def gamebot_prompt(topic: str) -> str:
    """Generates a prompt for gamebot"""
    output_prompt = (  
        f"You are a highly intelligent {topic} gameplay agent trained to win the game."  
        "Your goal is to analyze the screenshot carefully and choose the best actions."
        "Analyze the given screenshot carefully and identify where is the game."
        "Then analyze the game board and find out the best actions."
        "You need to simulate the mouse to click the screen.\n\n"
        "### OUTPUT FORMAT (STRICT) and Only output a list of actions in the format below ###\n"
        "- Respond in the following strict JSON format:\n"
        "[\n" 
        '  {"x": X, "y": Y, "button": B},\n'
        '  ...\n'  
        ']\n'
        '- Requirements:\n'
        '- X and Y are integers representing screen coordinate.\n'
        '- B means the operation of mouse button and must be one of: "left", "right", "doubleleft".\n'
        '- Ensure no extra text, explanations, or markdown formatting — output ONLY the JSON array.\n'
        '- The list can contain any number of actions, and zero number means the game is finished.\n'
    )
    return output_prompt
    

if __name__ == "__main__":
    mcp_server.run(transport='stdio')