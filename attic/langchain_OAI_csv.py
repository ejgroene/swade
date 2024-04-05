from langchain.agents.agent_types import AgentType
from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI
from langchain_experimental.agents.agent_toolkits import create_csv_agent
import os

# agent = create_csv_agent(
#     OpenAI(temperature=0),
#     "titanic.csv",
#     verbose=True,
#     agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
# )

base_filepath = "/Users/malikluti/Documents/MyProjects/SWADE/ImageCat/Data/V2"
city_a = os.path.join(base_filepath, 'city_A.csv')
city_b = os.path.join(base_filepath, 'city_B.csv')


agent = create_csv_agent(
    ChatOpenAI(temperature=0.7, model="gpt-4", ),
    city_a,
    verbose=True,
    agent_type=AgentType.OPENAI_FUNCTIONS,
)

agent.run("how many rows are there in the file?")

