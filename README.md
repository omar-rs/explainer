# explainer
* Explain errors in failed content publishing to PCC
* Inspired by the GH Actions <a href="https://github.com/posit-hosted/vivid-api/actions/runs/14268653451/job/39996910370" target="_blank">"Explain error" feature</a> 


### how to ingest repos
* need to pack an entire GH repo into a single, AI-friendly file used as input to the explainer
* repomix
  * https://github.com/yamadashy/repomix
  * install: `brew install repomix`
  * usage: `repomix --remote https://github.com/omar-baba/bokeh/tree/main --output ./src/explainer/codebases/bokeh.xml`
* OneFileLLM
  * https://github.com/jimmc414/onefilellm


### questions
* what type of errors is this best for?
  * syntax errors
  * logical errors
  * dependencies
* how does an error explainer fit in the workflow of a typical user?
* what is the minimum info you need to pass to the llm to explain the errors?
  * only logs
  * logs and source code
  * entry point
* how do we deal with large code bases / logs
  * ran into token limits with the OpenAI API
* what can we do with the output of the error explainer?
  * can we create a PR to fix the error?
  * can the explanation reference the exact line of code that caused the error?
* cost
  * should the error explainer be available for: 
    * paid accounts only?
    * every type of error?
  * how can we put a cost limit after which the explainer is not presented?
* can we explain things other than errors by tweaking the prompt and inputs? 
  * how the code works
  * code quality assessment
  * generate documentation
  * generate tests
* how to run the error explainer in prod
  * repomix supports running as an MCP server


### experiments
* use some of the latest publish failures from production (public repos)
* run them on my own account in prod to retrieve the logs
* use repomix to get the source code
* feed into the error explainer, along with the entry point
* use this [prompt](https://github.com/omar-rs/explainer/blob/7b07e05f645a565d8171df52b67f79fcd1e79e71/src/explainer/prompts/explain_error.txt#L1)
* some early [results](https://github.com/omar-rs/explainer/tree/main/src/explainer/outputs)
