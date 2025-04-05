import main
with open("examples.txt", "a") as f:
    f.write(main.get_context()[1])