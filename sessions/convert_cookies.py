import json

def convert_cookies():
    with open("sessions/instagram_state.json") as f:
        state = json.load(f)

    cookies = state["cookies"]

    with open("sessions/instagram_cookies.txt", "w") as f:
        f.write("# Netscape HTTP Cookie File\n")

        for c in cookies:
            domain = c["domain"]
            include_subdomains = "TRUE" if domain.startswith(".") else "FALSE"
            path = c["path"]
            secure = "TRUE" if c["secure"] else "FALSE"
            expires = str(int(c.get("expires", 0)))
            name = c["name"]
            value = c["value"]

            f.write(
                f"{domain}\t{include_subdomains}\t{path}\t{secure}\t{expires}\t{name}\t{value}\n"
            )