from crewai.flow.flow import Flow, start, listen 
from crewai import Agent 
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from typing import Literal 


load_dotenv()  # Load environment variables from .env file

class Agentstate(BaseModel):
    topic: str = Field(description="The topic of the agent", default="")
    description: str = Field(description="1 paragragh description about the topic", default="")
    topic_category: Literal["Technical", "Non-Technical"] | None = Field(description="Category of the topic", default=None)

    
class Agentoutput(BaseModel):
    topic_description: str = Field(description="One paragraph description about the topic")
    category: Literal["Technical", "Non-Technical"] = Field(description="Category of the topic")


# define the flow 
class AgenticStateFlow(Flow[Agentstate]): # Flow[Agentstate] indicates that the flow will use the Agentstate model as its state

    # define the start node
    @start()
    def get_topic(self) -> str:
        topic = self.state.topic
        return topic

    # define the second node
    @listen(get_topic)
    def get_description(self, topic: str) -> dict[str, str]:
        agent = Agent(
            role="Your goal is to provide a one paragraph description about the topic and categorize it as Technical or Non-Technical. You should not provide any other information.",
            goal="Provide a one paragraph description about the topic and categorize it as Technical or Non-Technical.",
            backstory="You are an expert in providing descriptions and categorizing topics."
        )

        # build the prompt for the agent
        prompt = f"Please provide a one paragraph description about the topic '{topic}' and categorize it as Technical or Non-Technical. You should not provide any other information."

        # get the output from the agent
        output = agent.kickoff(messages=prompt, response_format=Agentoutput) 

        # update the state with the output from the agent
        self.state.description = output.pydantic.topic_description
        self.state.topic_category = output.pydantic.category

        # return the state as a dictionary
        return self.state.model_dump()  # return the state as a dictionary

if __name__ == "__main__":
    # define the flow
    flow = AgenticStateFlow()

    # kickoff the flow
    output = flow.kickoff(inputs={
        "topic": "AI agents in coding and software development"
    })

    # print the output
    print(f"Flow Output: {output}")

    print("Flow State: ", flow.state)  # print the state of the flow
