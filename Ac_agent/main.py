from agents import Agent , Runner  ,input_guardrail, GuardrailFunctionOutput ,InputGuardrailTripwireTriggered , trace
from pydantic import BaseModel
import asyncio
from connection import config
import rich

class CHILD_OUTPUT(BaseModel):
     response:str
     isSpeedInLimit: bool


father = Agent(
    name = "Controlling Agents",
    instructions = "You are a controlling agent. Your task is to control the child's AC speed. If it is less than 24, restrict them in a polite manner.",
    output_type = CHILD_OUTPUT
)

@input_guardrail

async def father_security(ctx , agent ,input):
    result = await Runner.run(father , input , run_config = config)
    print(result.final_output)

    return GuardrailFunctionOutput(
        output_info = result.final_output.response,
        tripwire_triggered = result.final_output.isSpeedInLimit
    )

# main agents
child_agent = Agent(
    name="child",
    instructions = "You are a child agent ",
    input_guardrails= [father_security]
)

async def main():
    try:
          result = await Runner.run(child_agent , "My ac speed is 18" , run_config = config)
          rich.print("You should arrange the speed ")

    except InputGuardrailTripwireTriggered:
      rich.print("sleep peacefully")


if __name__ :"__main__"
asyncio.run(main())