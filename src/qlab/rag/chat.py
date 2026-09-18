from langchain_core.messages import SystemMessage, HumanMessage, AIMessage, ToolMessage

from .config import SYSTEM_PROMPT, TOOL_RESPONSE_PROMPT
from .database import get_relevant_context, get_user_chat_history, save_user_chat_messages
from qlab.core.model import User, test_user
from .agent import agent
from .tools import tools_map


def chat(user: User, prompt: str) -> AIMessage:

    user_name = f'{user.first_name} {user.last_name}'
    user_prompt = prompt

    relevant_context = get_relevant_context(query=user_prompt)

    system_message = SystemMessage(SYSTEM_PROMPT.format(context=relevant_context, user_id=user.id, user_name=user_name))
    user_message = HumanMessage(user_prompt)
    chat_history = get_user_chat_history(user_id=user.id)

    output = agent.invoke([system_message, *chat_history, user_message])
    response = ''
    messages = [{'role': 'human', 'content': user_prompt}]

    if not output.tool_calls:    
        response += output.content
        messages.append({'role': 'ai', 'content': output.content})

    else:
        tool_messages = []
        for tool_call in output.tool_calls:
            tool_name = tool_call['name']
            tool_args = tool_call['args']

            selected_tool = tools_map[tool_name]

            print(f'calling tool: {tool_name}.invoke({tool_args})')
            tool_response = selected_tool.invoke(tool_args)

            if not tool_response:
                tool_response = 'No data found.'
            response += f'{tool_response}'

            tool_messages.append(
                ToolMessage(content=str(tool_response), tool_call_id=tool_call['id'])
            )
            messages.append({'role': 'tool', 'content': str(tool_response), 'id': tool_call['id']})

        final_output = agent.invoke([
            SystemMessage(TOOL_RESPONSE_PROMPT),
            user_message,
            output,
            *tool_messages
        ])

        response = final_output.content
        messages.append({'role': 'ai', 'content': final_output.content}) 

    save_user_chat_messages(user_id=user.id, messages=messages)

    return AIMessage(content=response)
    
