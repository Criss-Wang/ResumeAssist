

<!-- PROJECT LOGO -->
<div>
  <h1 align="center">ResumeAssist: Your private resume guide </h1>
<div>
  
![build](https://github.com/criss-wang/dpai/workflows/build/badge.svg) 
![docs](https://github.com/criss-wang/dpai/workflows/docs/badge.svg) 
![lint](https://github.com/criss-wang/dpai/workflows/lint/badge.svg)
[![codecov](https://codecov.io/gh/Criss-Wang/dpai/graph/badge.svg?token=D73VGZR7NN)](https://codecov.io/gh/Criss-Wang/dpai)
[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/release/python-3110/)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![commit](https://img.shields.io/github/last-commit/criss-wang/dpai)](https://github.com/criss-wang/dpai/commits/master)

**Introducing ResumeAssist, an easy-to-deploy personal resume assistant with UNLIMITED AI suggestions.**


## ⚡ Getting Started
The easiest way to run ResumeAssist is inside a Docker container. It works with Linux, Mac OS, or WSL on Windows.

To start ResumeAssist in a docker container, run the following commands in your terminal:

```bash
Docker command to come soon
```

## 💻 Tech Stack
- **UI**: TypeScript, Next.js, React, Tailwind CSS, MateriaUI

- **Backend**: Fastapi, Neo4j, Docker, 

- **LLM**: LangChain, Jupyter, OpenAI

## 🚀 Documentation
Prototyping... So far you may refer to the following:
### Major Flow
![](backend/docs/major_workflow.png)

### Main execution paths
<P>
  <img src="backend/docs/ai_assist_flow.png" width="600">
</P>
<p>
  <img src="backend/docs/compilation.png" width="200">
</P>


## 📈 Roadmap
### Major updates
- This is a renewed effort of my instruction-based resume assist which started after my Master's Degree. I decided to overhaul the repo, and replace the simple llm-call with a more flexible, multi-agent AI assistant system.
### Completed
- Anthropic based LangChain engine
- Config-based Agent system
- Basic UI for Resume modification
- Neo4j connection
### In progress
- Unit Testing
- Linting
- Integration Tests
### Planned
- Ollama based LangChain engines (True unlimited use)
- Local Model (if GPU is available, may use quantized models)


