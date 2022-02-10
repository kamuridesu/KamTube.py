import sys


def structure(query: str, extract: bool):
    return {"query": query, "extract": extract}


def argparser():
    query = ""
    extract = False
    args = sys.argv[1:]
    if len(args) == 0:
        print("[!] No arguments provided")
        sys.exit(1)
    if "-x" in args:
        extract = True
        args.remove("-x")
    if "-h" in args or "--help" in args: 
        print("Usage: kamtubepy [options] <query>")
        print("Options:")
        print("-x\tExtract audio (audio only)")
        print("-h\tShow this help")
        sys.exit(0)
    if len(args) > 0:
        query = " ".join(args)
        return structure(query, extract)
    print("[!] No arguments provided")