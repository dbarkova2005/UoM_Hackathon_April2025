import main
with open("examples.txt", "a") as f:
    print(main.get_context()[1])
    f.write(main.get_context()[1])