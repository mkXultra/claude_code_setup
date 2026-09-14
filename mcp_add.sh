
claude mcp add-json chat '{"name":" chat","command":"npx","args":["agent-communication-mcp"]}'
claude mcp add-json ccm '{"name":"ccm","command":"npx","args":["@mkxultra/claude-code-mcp@latest"]}'
claude mcp add graphiti --transport sse http://localhost:8000/sse
claude mcp add n4query --transport sse http://localhost:8090/sse



