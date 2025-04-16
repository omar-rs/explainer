### Dev
* install Claude desktop app (https://claude.ai/download)
  * to install the `repomix` MCP server in it:
    * copy `claude_desktop_config.json` to `~/Library/Application Support/Claude/claude_desktop_config.json`
    * restart Claude app
    * when it starts, you should see the mcp server running in the Settings > Developer
    * also, you can see the tools in the prompt (the hammer icon) 

* install the mcp inspector package (https://github.com/modelcontextprotocol/inspector)
  * `npx @modelcontextprotocol/inspector node build/index.js`
  * access inspector in browser at http://127.0.0.1:6274

* inspect the `repomix` MCP server in the inspector
  * use `STDIO` for transport
  * use `/opt/homebrew/bin/repomix` for command
  * use `--mcp` for args
  * connect, then list tools

* test `repomix` MCP server tool `pack_remote_repository`
  * use `https://github.com/omar-baba/streamlit-error` for `remote`
  * use `compress`
  * use `**/*.scss,**/*.svg,.Rproj.user/**,ALZ/**,jobs/**,legal_notes/**` `for ignorePatterns`
    * the downloaded file is specified in the response's `outputFilePath`
    * the id of the output file is `outputId` and is used in the next tool `read_repomix_output`

* test `repomix` MCP server tool `read_repomix_output`
    * use the value of the `outputId` from the output of the `pack_remote_repository` tool
