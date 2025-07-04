# -*- coding: utf-8 -*-
"""ReAct.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1ZBOK0cpVinAu1pCtpBjVbJbXwJunBo2n
"""

from google.colab import userdata
!huggingface-cli login



# Step 1: Make sure you have the required libraries
#!pip install transformers accelerate bitsandbytes torch

import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import os
import gc
from google.colab import userdata

# --- 1. SETUP: Load the Phi-3 Model with 4-bit Quantization ---

"""# Gemma 2B"""

print("--- Loading Model and Tokenizer ---")

tokenizer = AutoTokenizer.from_pretrained("google/gemma-2-2b-it")
model = AutoModelForCausalLM.from_pretrained("google/gemma-2-2b-it")
print("--- Model and Tokenizer Loaded ---")

# --- 2. DEFINE TOOLS ---
knowledge_base = {
    "apple remote": "The Apple Remote is a remote control device. A key patent for its design was co-filed by Martin Eberhard.",
    "martin eberhard": "Martin Eberhard is an American engineer. He co-founded Tesla, Inc. with Marc Tarpenning in 2003.",
    "tesla, inc.": "Tesla, Inc. is an American automotive company. Elon Musk has served as CEO of Tesla since 2008."
}

def wikipedia_search(query: str) -> str:
    print(f"--- TOOL: Searching Wikipedia for '{query}' ---")
    query = query.lower()
    for key in knowledge_base.keys():
        if key in query:
            return knowledge_base[key]
    return f"Could not find information on '{query}'."

# --- 3. THE ReAct PROMPT ---
react_prompt_template_gemma = """<start_of_turn>user
You are a helpful assistant that can solve complex problems by breaking them down into a sequence of thoughts and actions. You have access to the following tools:
- wikipedia_search[query]: Searches a small Wikipedia dataset.
- Finish[answer]: Provides the final answer to the user.

Follow the format:
Thought: Your reasoning and plan for the next step. Generate only one thought and one action per turn.
Action: The tool you will use.

Question: {question}<end_of_turn>
<start_of_turn>model
"""

# --- 4. THE ReAct ENGINE (FIXED: Now takes model and tokenizer as arguments) ---
def run_react_agent(question: str, model, tokenizer):
    text_generator = None
    try:
        eos_token_id = tokenizer.convert_tokens_to_ids('<end_of_turn>')

        text_generator = pipeline(
            "text-generation",
            model=model,
            tokenizer=tokenizer,
            max_new_tokens=100,
            do_sample=False,
            eos_token_id=eos_token_id
        )

        prompt = react_prompt_template_gemma.format(question=question)
        print("--- STARTING AGENT ---")

        for _ in range(5):
            print(f"\n--- STEP {_ + 1} ---")

            raw_output = text_generator(prompt)[0]['generated_text']
            llm_output = raw_output[len(prompt):].strip()
            print(f"LLM Output:\n{llm_output}")

            if "Action:" not in llm_output:
                print("Error: Model did not generate an action.")
                break

            prompt += llm_output + "<end_of_turn>"
            action_str = llm_output.split("Action:")[1].strip()

            if action_str.lower().startswith("finish"):
                answer = action_str[7:-1].strip()
                print(f"\n--- AGENT FINISHED ---")
                print(f"Final Answer: {answer}")
                return # Exit the function

            tool_name, query = action_str.split('[')
            query = query[:-1]

            if tool_name == "wikipedia_search":
                observation = wikipedia_search(query)
            else:
                observation = f"Unknown tool: {tool_name}"

            print(f"Observation:\n{observation}")
            prompt += f"\n<start_of_turn>user\nObservation: {observation}<end_of_turn>\n<start_of_turn>model"

        print("\n--- AGENT STOPPED: MAX STEPS REACHED ---")
    finally:
        # This function only cleans up variables created *inside* it.
        if text_generator is not None:
            del text_generator

# --- 5. RUN THE AGENT AND CLEAN UP ---
try:
    # Pass the global model and tokenizer to the function
    run_react_agent("Who is the current CEO of the company co-founded by the inventor of the Apple Remote?", model, tokenizer)
finally:
    # The main script cleans up the global variables it created.
    print("\n--- Cleaning up global objects ---")
    if 'model' in globals(): del model
    if 'tokenizer' in globals(): del tokenizer
    gc.collect()
    torch.cuda.empty_cache()

