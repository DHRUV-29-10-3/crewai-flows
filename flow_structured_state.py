from crewai.flow.flow import Flow, start, listen    
from pydantic import BaseModel, Field

class PersonState(BaseModel):
    name: str = Field(..., description="Name of the person")
    age: int = Field(..., description="Age of the person")
    friends : list[str] = Field(..., description="List of friends of the person")
    contact: dict[str, str|int] = Field(..., description="Contact information of the person")



class MyStructuredState(Flow[PersonState]):

    # define the start node
    @start()
    def get_inputs(self):
        # structured state is in the form of pydantic model
        self.state.name = "Amit"
        self.state.age = 35
        self.state.friends_list.append("Neha")
        list. append ("Rahul")
        self. state. friend
        self.state.friends_list.extend(["Deeksha", "Hemant"])
        self.state.contact_info["email"]="amit123@gmail.com"
        self.state.contact_info["mob"] = 9855599771
        print(f"State: {self.state}")
        return "Hello"

    # define the second node
    @listen(get_inputs)
    def update_state(self):
        return "bye"


if __name__ == "__main__":
    # define the flow
    flow = MyStructuredState()

    # kickoff the flow
    output = flow.kickoff()

    # print the output
    print(f"Flow Output: {output}")

    print("Flow State: ", flow.state)  # print the state of the flow

