def count_fillers(text):

    fillers = [
        "um",
        "uh",
        "like",
        "you know",
        "actually"
    ]

    words = text.lower().split()

    count = 0

    for filler in fillers:
        count += words.count(filler)

    return count