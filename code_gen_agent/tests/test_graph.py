from code_gen_agent.src.utils.llm_helper import invoke_llm_json
result = invoke_llm_json("", "how are you?")
print(result)