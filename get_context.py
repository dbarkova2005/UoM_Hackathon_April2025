import main
with open("examplesv4.txt", "a") as f:
    ctx = main.get_context()
    ctx = eval(ctx)["message"]
    print(ctx)
    f.write(ctx)