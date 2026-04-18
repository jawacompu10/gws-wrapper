# Google WorkSpace CLI Wrapper

I found the Google Workspace CLI at Github: https://github.com/googleworkspace/cli

This is good, but it is too big for my requirements. There are too many command options and sub-options, with a lot of parameters. I want to build a wrapper and write adapters for common use cases like get my most recent 'n' mails, get my calendar events for the next 'n' days, etc.

Let's use the gws CLI itself to help us build this. We can use a combination of `gws -h` and `gws schema` to understand the available commands and functions. Then build our wrapper. This is just for me to run locally, so no need to worry about authentication to Google. For the interface to external systems, I want to leave the option to make it as flexible as possible. So, we will write functions that can be called from an interface layer - which will either be CLI or API or MCP.


For coding guidelines, I do not want to build blindly - so, explain each code change you are doing so that this will also be a learning opportunity for me. Keep each change small and easily explainable. We will also make atomic commits so as not to lose our data.


### Tech Stack
We will use Python, uv, dynaconf, loguru.
For CLI, let's use "click".

Keep the code clean - smaller functions, clearer names, more readable.
