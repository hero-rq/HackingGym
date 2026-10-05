def first_violation(events):
    granted = set()                      # permissions active right now

    for i, (action, permission) in enumerate(events):
        if action == "grant":
            granted.add(permission)      # adding twice is harmless

        elif action == "revoke":
            granted.discard(permission)  # discard doesn't fail if missing

        elif action == "use":
            if permission not in granted:
                return i                 # first unauthorized use

        else:
            raise ValueError(f"Unknown action: {action!r}")

    return -1                            # every use was authorized


events = [
    ("grant", "filesystem.read"),
    ("use", "filesystem.read"),
    ("revoke", "filesystem.read"),
    ("use", "filesystem.read"),
]
print(first_violation(events))   

print(first_violation([
    ("grant", "filesystem.read"),
    ("use", "filesystem.read"),
    ("use", "network.send"),
]))                              

print(first_violation([
    ("grant", "filesystem.read"),
    ("grant", "network.send"),
    ("use", "filesystem.read"),
    ("revoke", "filesystem.read"),
    ("use", "network.send"),
]))                              

print(first_violation([]))       
