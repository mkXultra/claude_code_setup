installing claude code perplexity mcp:

1. Install smithery `npx -y @smithery/cli install perplexity-mcp --client claude`
2. register claude code via `claude mcp add-json perplexity-mcp '{"type":"stdio","command":"perplexity-mcp","env":{"PERPLEXITY_API_KEY":"pplx-YOUR-API-KEY-HERE"},"args":["--model","sonar-pro","--reasoning-model","sonar-reasoning-pro"]}' -s user`
3. test it via `claude mcp list`


troubleshooting:
1. install uv package manager `curl  -LsSf https://astral.sh/uv/install.sh | sh`
2. run `uvx perplexity-mcp --help`

If you see an error about PERPLEXITY_API_KEY not being available then add it to your .bashrc or .zshrc by inserting this line: PERPLEXITY_API_KEY: [your_api_key]

If you run `uvx perplexity-mcp --help` again and you get no error and The terminal doesn't return control, then run ps aux | grep perplexity-mcp. If you see the following three

beetz12 23227 0.0 0.0 1217488 32596 pts/3 Sl+ 16:27 0:00 /home/beetz12/.local/bin/uv tool uvx perplexity-mcp --help
beetz12 23246 0.2 0.1 139912 58004 pts/3 Sl+ 16:27 0:00 /home/beetz12/.cache/uv/archive-v0/J6WbpC_nddXWilnjnkyyJ/bin/python /home/beetz12/.cache/uv/archive-v0/J6WbpC_nddXWilnjnkyyJ/bin/perplexity-mcp --help
beetz12 23262 0.0 0.0 4096 1792 pts/2 S+ 16:29 0:00 grep --color=auto perplexity-mcp

the second one is the mcp server running. In this case, run `claude mcp remove perplexity-mcp` and then run `claude mcp add-json perplexity-mcp '{"type":"stdio","command":"uvx","args":["perplexity-mcp","--model","sonar-pro","--reasoning-model","sonar-reasoning-pro"],"env":{"PERPLEXITY_API_KEY":"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"}}' -s user`
