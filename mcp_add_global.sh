
claude mcp add-json chat '{"name":" chat","command":"npx","args":["agent-communication-mcp@latest"]}' -s user
claude mcp add-json ccm '{"name":"ccm","command":"npx","args":["@mkxultra/claude-code-mcp@latest"]}' -s user
claude mcp add-json playwright '{"command":"npx","args":["@playwright/mcp@latest"]}' -s user
claude mcp add-json perplexity-mcp '{"type":"stdio","command":"uvx","args":["perplexity-mcp","--model","sonar-pro","--reasoning-model","sonar-reasoning-pro"],"env":{"PERPLEXITY_API_KEY":"pplx-your-real-key-here"}}' -s user



