# Gemma-2B-ReAct-Playground.
(THINK → ACTION → OBSERVE → ANSWER) to life using the Gemma 2B model—all within a single kernel. Perfect for showcasing how large language models can interleave reasoning with tool calls in real time.



## ✨ Why This Notebook?
Inline Reasoning: Witness each THINK step as markdown, then see ACTION code execute immediately.
Gemma 2B Kernel: Run a 2‑billion‑parameter model locally via the Gemma kernel—no external API needed.
Tool-Driven: Easily integrate lookup functions, HTTP calls, or custom Python tools.
Self-Documenting: Combines narrative, code, and output for transparent LLM workflows.

## 🚀 Getting Started
Clone & Enter
git clone https://github.com/yourusername/gemma-react-playground.git
cd gemma-react-playground
Setup Python Environment

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt gemma gemma-2b
jupyter gemma install

Open the Notebook
jupyter notebook Gemma2B_ReAct_Playground.ipynb

Select Gemma (2B) kernel from the Kernel menu.
Run Through the Flow
Execute each cell in order to see THINK ➔ ACTION ➔ OBSERVE ➔ ANSWER in action.

## 🧠 Notebook Tour
Stage                 | Description
THINK                 | Outline the agent’s reasoning in markdown.
ACTION                | Invoke tools or functions via Python code.
OBSERVE               | Inspect raw outputs: JSON, tables, charts.
ANSWER                | Compose the final natural-language response.

> Question: Who invented the Apple Remote?

THINK: Need to search Wikipedia for inventor.
ACTION: wikipedia_search('Apple Remote inventor')
OBSERVE: Found key patent co-filed by Martin Eberhard.
ANSWER: The Apple Remote’s design patent was co-filed by Martin Eberhard.

## ⚙️ Implementation Details
In the notebook, each ReAct stage is implemented using Gemma’s cell tagging and inline code:
Prompt Template: A Python variable at the top defines the meta‑prompt with placeholders for [THOUGHT], [ACTION], and [OBSERVE].

## 1- prompt_template = '''
You are a research assistant.
{thought_marker}: {thought}
{action_marker}: {action}
{observation_marker}: {observation}
{answer_marker}:'''

## 2- THINK Cells:
Prefixed with a markdown comment # THINK:. Gemma renders this as a thought bubble before execution.
Contains plain-text reasoning to decide on the next tool.

## 3- ACTION Cells:
Tagged with # ACTION: and call the corresponding Python function decorated with @tool.
Example:
@tool
def wikipedia_search(query: str) -> str:
    # perform HTTP lookup...

# ACTION:
result = wikipedia_search('Deep RL Hands-On author')

## 4- OBSERVE Cells:
Marked with # OBSERVE: to display raw outputs.
Uses display(result) or pandas to render tables.

## 5- ANSWER Cells:

Use # ANSWER: and a final LLM call to fill in the template with all previous steps:

# ANSWER:
llm(prompt_template.format(
    thought=thought,
    action=last_action,
    observation=result,
    answer_marker='ANSWER'
))

Gemma automatically sequences these cells, capturing the LLM’s thought and final answer inline, giving you a transparent, step-by-step ReAct workflow.

## 🔧 Customize & Extend
Add New Tools: Define a Python function with @tool decorator.
Switch KB: Swap the lookup logic in the tool cell (e.g., replace with ChromaDB query).
Tune Prompts: Edit the prompt template cell to adjust reasoning style or context.


# Demo:
![Demo](https://github.com/Umang-projects/Gemma-2B-ReAct-Playground./tree/main/Screenshot 2025-06-26 004842.png)
