from crewai.flow.flow import Flow, start, listen, and_ , router
import random 
from pydantic import BaseModel
from typing import Literal
# crewai a flow class 

class RouterState(BaseModel):
    output: bool = False

class MyRouterFlow(Flow[RouterState]):

    @start() 
    def input_node(self) -> bool:
        random_output = random.choice([True, False]) 
        # add output   
        self.state.output = random_output
        return random_output
    
    @router(input_node)
    def router_node(self) -> Literal["success", "failure"]:
        if self.state.output:
            return "success"
        else:
            return "failure"

    @listen("success")
    def success_branch(self):
        return "congo its a success!"

    @listen("failure")
    def failure_branch(self):
        return "fuck off you are a failure!"

if __name__ == "__main__":
    flow = MyRouterFlow()
    response = flow.kickoff()
    print("Flow State:", response)
    flow.plot("flow_diagram.html")


