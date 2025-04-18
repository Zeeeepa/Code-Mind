# Code-Mind
Code-Mind -Codegen engine driven by itself.
Input - Requirements references. (any files, codefiles, links to codebases, articles etc). 
Button Start - Shows processing progress. 
codegen implements full features of codebase analysis via codegen sdk and uses multithreading agent api further prompting in a full CI/CD self reflection -> Task is done? -> If no-Continue by providing mew scheme to execute. So that it wouldn't get stuck if something fails, so that he could reflect on issues and try otherway.


Autonomous full CI/CD. User should be able to adjust requirements at any moment.
TO USE LINEAR API FOR FULL PROGRAMIC PROJECT MANAGEMENT.


Example uses. 

from codegen import Agent
# Create an agent
agent = Agent(org_id="ccc", token="cccccc")
# Run on task
task = agent.run("Generate docs for my backend repo")
# Refresh to get updated status
task.refresh()
print(task.status)
# Once task is complete, you can access the result
if task.status == "completed":
    print(task.result)





from codegen import Agent

# Initialize the Agent with your organization ID and API token
agent = Agent(org_id="...", token="...")

# Run an agent with a prompt
task = agent.run(prompt="Leave a review on PR #123")

# Check the initial status
print(task.status)

# Refresh the task to get updated status (tasks can take time)
task.refresh()

if task.status == "completed":
    print(task.result)  # Result often contains code, summaries, or links





from codegen.agents.agent import Agent

# Initialize the Agent with your organization ID and API token
agent = Agent(
    org_id="YOUR_ORG_ID",  # Find this at codegen.com/developer
    token="YOUR_API_TOKEN",  # Get this from codegen.com/developer
    # base_url="https://codegen-sh-rest-api.modal.run",  # Optional - defaults to production
)

# Run an agent with a prompt
task = agent.run(prompt="Implement a new feature to sort users by last login.")

# Check the initial status
print(task.status)

# Refresh the task to get updated status (tasks can take time)
task.refresh()

# Check the updated status
print(task.status)

# Once task is complete, you can access the result
if task.status == "completed":
    print(task.result)  # Result often contains code, summaries, or links




