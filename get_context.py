import main
with open("examplesv5.txt", "a") as f:
    ctx = main.get_context()
    ctx = eval(ctx)["message"]
    print(ctx)
    f.write(ctx)