from crewai.flow.flow import Flow, start, listen
from typing import Any

# define the flow class
class MyUnstructuredStateFlow(Flow):

    # define the start node
    @start()
    def get_inputs(self) -> dict[str, Any]:
    # to access the state -- > use self.state
    # unstructured state is in the form of dic
        return self.state  
        

    @listen(get_inputs)
    def update_state(self, last_output) -> str:
        print("my state ", last_output) 
        return "state updated"




if __name__ == "__main__":
    # create the flow
    flow = MyUnstructuredStateFlow()

    # execute the flow
    output = flow.kickoff()

    print(f"Flow Output: {output}")
