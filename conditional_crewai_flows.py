
from crewai.flow.flow import Flow, start, listen, and_
from crewai import Agent
from dotenv import load_dotenv
from pydantic import BaseModel
from crewai_tools import FileWriterTool

load_dotenv()

writer_tool = FileWriterTool()


class AgentState(BaseModel):
    topic: str = ""
    notes: str = ""
    qa: str = ""


class MyConditionalFlow(Flow[AgentState]):

    # Starting node
    @start()
    def get_topic(self):
        return self.state.topic

    # Branch 1: Generate notes
    @listen(get_topic)
    def create_notes(self, topic: str):

        notes_agent = Agent(
            role=f"Expert in {topic} who can provide detailed notes.",
            goal=f"Provide detailed and structured notes on {topic}.",
            backstory=f"You are an expert in {topic}. "
                      "You provide comprehensive, factual and "
                      "well-organized notes.",
            verbose=True
        )

        notes_prompt = (
            f"Please provide detailed notes on {topic}, "
            "including key concepts, important details and examples."
        )

        notes_response = notes_agent.kickoff(
            messages=notes_prompt
        ).raw

        self.state.notes = notes_response

        return notes_response

    # Branch 2: Generate Q&A independently
    @listen(get_topic)
    def create_qa(self, topic: str):

        qa_agent = Agent(
            role=f"Expert in creating questions and answers about {topic}.",
            goal=f"Create a comprehensive Q&A about {topic}.",
            backstory=f"You are an expert in {topic} "
                      "and can create accurate educational questions.",
            verbose=True
        )

        qa_prompt = (
            f"Create a set of questions and answers about {topic}. "
            "Cover important concepts and provide clear answers."
        )

        qa_response = qa_agent.kickoff(
            messages=qa_prompt
        ).raw

        self.state.qa = qa_response

        return qa_response

    # Wait for both branches
    @listen(and_(create_notes, create_qa))
    def merge_notes_qa(self):

        notes = self.state.notes
        qa = self.state.qa

        compiler_agent = Agent(
            role="Expert document compiler",
            goal="Merge notes and Q&A into one comprehensive document.",
            backstory=(
                "You are an expert in compiling information into "
                "well-organized and readable Markdown documents."
            ),
            verbose=True
        )

        merge_prompt = f"""
        Merge the following notes and Q&A into one comprehensive
        Markdown document.

        Topic: {self.state.topic}

        NOTES:
        {notes}

        QUESTIONS AND ANSWERS:
        {qa}

        Organize the document with appropriate headings.
        """

        merged_response = compiler_agent.kickoff(
            messages=merge_prompt
        ).raw
    
        
        return merged_response


if __name__ == "__main__":

    flow = MyConditionalFlow()

    final_document = flow.kickoff(
        inputs={
            "topic": "Artificial Intelligence"
        }
    )

    print("Final document:")
    print(final_document)

    print("Flow State:")
    print(flow.state)

    flow.plot("flow_diagram.html")

    # Save the generated Markdown document
    writer_tool.run(
        filename="ai.md",
        content=final_document
    )
