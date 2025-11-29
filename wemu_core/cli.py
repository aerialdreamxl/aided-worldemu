import wemu_core

version="Pre-Alpha"
instance={}

def _headLine():
    print("="*20)
    if instance=={}:
        print("Now Loaded: None")
    else:
        print("Now Loaded: "+instance["name"])

def instanceOps():
    while(1):
        _headLine()
        print("[0]Back")
        print("[1]Load")
        print("[2]New")
        print("[3]Save")
        print("[4]Edit")
        inp=int(input(">"))
        if inp==0:
            break

def main():
    print("Welcome to WEMU CLI Version "+version)
    while(1):
        _headLine()
        print("[0]Exit WEMU CLI")
        print("[1]WEMU instance operations")
        print("[9]Test Options")
        inp=int(input(">"))
        if inp==0:
            break
        elif inp==1:
            instanceOps()

if __name__ == "__main__":
    main()