from agents.uncertainty_agent import respond

while True:
    user_input = input(">> ")
    response = respond(user_input)
    print(response)
