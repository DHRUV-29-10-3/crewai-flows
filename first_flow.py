from crewai.flow.flow import Flow, start, listen

class MyFirstFlow(Flow):

    # define the start_node/trigger_node
    @start()
    def start_flow(self) -> str:
        return "flow started successfully"

    # make the second node listen to the first node
    @listen(start_flow)
    def processing_node(self, message: str) -> str:
        print(f"Received message: {message}")
        return "processing completed"

    @listen(processing_node)
    def final_node(self, message: str) -> str:
        print(f"Received message: {message}")
        return "flow completed"


if __name__ == "__main__":
    flow = MyFirstFlow()
    res = flow.kickoff()  # start the flow
    flow.plot()  # visualize the flow
    print(res)  # prints "flow started successfully"
    

    