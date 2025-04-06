with open("examples.txt", "r") as f:
    lines = f.readlines()
    for line in lines:
        if line.count("$") == 1 and "budget" not in line and "total investment" not in line:
            print(line)