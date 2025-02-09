# test_agent.py
from cdp_langchain.agent_toolkits import CdpToolkit
from cdp_langchain.utils import CdpAgentkitWrapper
import os
from dotenv import load_dotenv

load_dotenv()

def test_connection():
    try:
        cdp = CdpAgentkitWrapper()
        toolkit = CdpToolkit.from_cdp_agentkit_wrapper(cdp)
        print("Successfully connected to CDP AgentKit!")
        return True
    except Exception as e:
        print(f"Error connecting to CDP AgentKit: {e}")
        return False

if __name__ == "__main__":
    test_connection()