# Contributing to Academic Research Assistant

Thank you for your interest in contributing! This guide will help you get started.

## Getting Started

### Prerequisites

- Python 3.10+
- Node.js 18+ (for OpenCode)
- OpenCode CLI or MiMo Code CLI

### Installation

```bash
# Clone the repository
git clone https://github.com/erfan-ashtari/academic-opencode.git
cd academic-opencode

# Install Python dependencies
pip install httpx fastmcp scholarly

# Copy environment template
cp .env.example .env

# Edit .env with your API keys
nano .env
```

## Development Setup

### Project Structure

```
academic-opencode/
├── .opencode/              # OpenCode configuration
│   ├── agents/             # Agent definitions
│   ├── skills/             # Skill definitions
│   ├── commands/           # Command definitions
│   └── rules/              # Context rules
├── mcp_servers/            # MCP server implementations
│   ├── fallback_utils.py   # Shared fallback utilities
│   └── *-mcp/              # Individual servers
├── templates/              # Document templates
└── docs/                   # Documentation
```

## Adding a New MCP Server

### 1. Create Server Directory

```bash
mkdir mcp_servers/my-new-mcp
```

### 2. Create server.py

Use the template from `mcp_servers/AGENTS.md`:

```python
from fastmcp import FastMCP
from fallback_utils import enrich_result, enrich_results_list, web_search_fallback

mcp = FastMCP("my-server")

@mcp.tool()
async def search_tool(query: str, max_results: int = 10) -> list[dict]:
    """Search description."""
    try:
        # API implementation
        results = await api_search(query, max_results)
        return enrich_results_list(results, "my-server")
    except Exception:
        return await web_search_fallback(query, "my-server", max_results)
```

### 3. Add to .mcp.json

```json
{
  "my-server": {
    "type": "stdio",
    "command": "python",
    "args": ["mcp_servers/my-new-mcp/server.py"]
  }
}
```

### 4. Update Documentation

- Add entry to `mcp_servers/AGENTS.md`
- Update `README.md` server table
- Add API key to `.env.example` if required

## Adding a New Skill

### 1. Create Skill Directory

```bash
mkdir .opencode/skills/my-skill
```

### 2. Create SKILL.md

```markdown
---
name: my-skill
description: Brief description for triggering (include trigger phrases)
---

# My Skill

Brief overview of what the skill does.

## How It Works

1. Step 1
2. Step 2

## Input

Describe expected input format.

## Output

Describe output format.

## Examples

Show usage examples.

## Dependencies

List MCP servers and other skills required.
```

### 3. Update Documentation

- Add entry to `.opencode/skills/AGENTS.md`
- Add trigger phrases to root `AGENTS.md`

## Adding a New Agent

### 1. Create Agent Directory

```bash
mkdir .opencode/agents/my-agent
```

### 2. Create AGENT.md

```markdown
---
model: opencode/mimo-v2.5-free
temperature: 0.7
---

# My Agent

## Purpose
Brief description of what this agent does.

## Capabilities
- Capability 1
- Capability 2

## Skills Used
- skill-1
- skill-2

## When to Use
Describe scenarios where this agent should be spawned.
```

### 3. Add Routing Rules

Update root `AGENTS.md` with routing patterns:

```markdown
| Query Pattern | Agent Spawned | Skills Loaded |
|---------------|---------------|---------------|
| "my pattern" | `my-agent` | `my-skill` |
```

## Code Style

### Python

- Follow PEP 8
- Use type hints
- Add docstrings to all public functions
- Keep functions focused and small
- Use async/await for API calls

### Markdown

- Use clear headings
- Include code examples
- Keep descriptions concise

## Testing

### Test MCP Servers

```bash
# Test individual server
python mcp_servers/arxiv-mcp/server.py

# Test fallback behavior
python -c "
import asyncio
from mcp_servers.fallback_utils import web_search_fallback
asyncio.run(web_search_fallback('test query', 'arxiv'))
"
```

### Test Skills

1. Load the skill in OpenCode/MiMo Code
2. Verify trigger phrases work
3. Test with various inputs
4. Check output format

## Pull Request Process

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### PR Requirements

- [ ] Code follows project style
- [ ] Tests pass
- [ ] Documentation updated
- [ ] No breaking changes (or clearly documented)
- [ ] Commit messages are clear

## Questions?

- Open an issue for bugs
- Start a discussion for features
- Check existing documentation first

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
