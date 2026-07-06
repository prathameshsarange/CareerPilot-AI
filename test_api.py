from agents.master_agent import MasterAgent

resume = """
John Doe
Python
Flask
SQL
Git
"""

report = MasterAgent().run(resume)

print(type(report))
print(report)