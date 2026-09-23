"""
This program checks whether a robot auditor may run its tools.

audit_gatekeeper processes the event sequence and remembers documents.
decide_run checks one tool request using that memory.
missing_documents identifies required documents that remain unread.

Together, they produce one response for each RUN event.
READ events only update memory.
"""

def missing_documents(
    required: set[str],
    documents_read: set[str],
) -> list[str]:
    """
    Idea: Identify which prerequisites are still unread.

    Inputs: Required names and names already read.
    Return: list[str] of missing names, alphabetically sorted.

    Condition: Include a name only if it is required but unread.
    Role: Supplies the missing-document list for an audit.
    Assumption: Document names are case-sensitive.
    """
    return sorted(required - documents_read)

def decide_run(
    tool: str,
    required: set[str],
    documents_read: set[str],
) -> str:
    """
    Idea: Decide one request using the current reading history.

    Inputs: Tool name, required names, and names already read.
    Return: str: "BLOCKED MANUAL", "OK", or "MISSING <names>".

    Conditions: Check the manual first. INSPECT needs only the
    manual; AUDIT additionally needs all required documents.
    Role: Contains the permission rules.
    Assumption: Tool is either INSPECT or AUDIT.
    """
    if MANUAL not in documents_read:
        return "BLOCKED MANUAL"

    if tool == "INSPECT":
        return "OK"

    # AUDIT needs an additional prerequisite check.
    missing = missing_documents(required, documents_read)

    if missing:
        return "MISSING " + " ".join(missing)

    return "OK"


def audit_gatekeeper(
    required: list[str],
    events: list[str],
) -> list[str]:
    """
    Idea: Process events in order while retaining reading history.

    Inputs: Required document names and chronological events.
    Return: list[str], one response per RUN event.

    Conditions: READ updates memory; RUN appends a decision.
    Role: Connects event processing to the prerequisite checks.
    Assumptions: Events are valid; repeated reads change nothing.
    """
    required_names = set(required)
    documents_read: set[str] = set()
    answers: list[str] = []

    for event in events:
        action, name = event.split()

        if action == "READ":
            documents_read.add(name)

        elif action == "RUN":
            answer = decide_run(name, required_names, documents_read)
            answers.append(answer)            

    return answers


required = ["SPEC", "MAP"]
events = [
    "READ SPEC",
    "RUN AUDIT",
    "READ MANUAL",
    "RUN INSPECT",
    "RUN AUDIT",
    "READ SPEC",
    "READ MAP",
    "RUN AUDIT",
]

print(audit_gatekeeper(required, events))
# Expected: ["BLOCKED MANUAL", "OK", "MISSING MAP", "OK"]
