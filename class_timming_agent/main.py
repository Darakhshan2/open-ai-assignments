from connection import config
from agents import Agent , Runner 
import rich
from pydantic import  BaseModel
from agents import input_guardrail , GuardrailFunctionOutput , InputGuardrailTripwireTriggered
import asyncio

class Student(BaseModel):
    response :str 
    isChangeSlot:bool

Teachers_agent = Agent(
    name="you are a teacher agent",
    instructions="You are a teacher agents .when student ask you to change the slot timming you have to say no to them because it's administration concern",
    output_type = Student

)

@input_guardrail
async def teacher_agent(ctx,agent,input):
    result = await Runner.run(Teachers_agent , input,run_config=config)
    rich.print(result.final_output)

    return GuardrailFunctionOutput(
        output_info=result.final_output.response,
        tripwire_triggered=result.final_output.isChangeSlot
    )


#  main agents
Students = Agent(
    name="Student_agent",
    instructions="You ask something to your teacher",
    input_guardrails=[teacher_agent]
)

async def main():
    try:
        result = await Runner.run(Students , "I don't want to change ", run_config=config)
        rich.print("Good enjoy your slot now and focus on studies")
    except InputGuardrailTripwireTriggered :
       rich.print("your request is answered")
        

if __name__ == "__main__":
  asyncio.run(main())