def calculate_score(answer):

    score=0

    words=len(
        answer.split()
    )

    if words>30:
        score+=5

    if words>60:
        score+=5

    return score