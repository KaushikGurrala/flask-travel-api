def calculate_rating(score):
    if score > 100:
        return "Excellent"
    else:
        return "Bad"

def test_rating():
    assert calculate_rating(101)=="Excellent"
    assert calculate_rating(99)=="Bad"