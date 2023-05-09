
def Login():
    username = input("Username: ")
    password = input("Password: ")
    if (username == "nnt") and (password == "dtd"):
        return True 

def TerminalEmulator():
    pass

if __name__ == "__main__":
    i = 0
    while i < 3:
        if Login():
            TerminalEmulator()
            break
        else:
            print("Wrong Username or Password.")
            i += 1
    