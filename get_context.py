import main
with open("examplesv4.txt", "a") as f:
    print(main.get_context()[1])
    f.write(main.get_context()[1])