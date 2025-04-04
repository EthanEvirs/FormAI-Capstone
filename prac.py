def main():
    running = True
    accept = ["yes","y"]
    decline = ["no", "n"]
    while running == True:
        test = input("Do you want to make a call?: ").lower()
        if test in accept:
            call()
        elif test in decline:
            running = False
    
    print("goodbye")


def call():
    contacts = {"Roxanne" : 33, "Ethan" : 8}
    number = int(input("Please input a number!: "))
    if number in contacts.values():
        print(contacts)
    print(f"Calling {number}...")


if __name__ == "__main__":
    main()