from .models import Book,Review


def ratingCalc(rating):
    
    ratings_sum = sum(rating)
    total_rating = len(rating)
    average_rating = ratings_sum / total_rating if total_rating > 0 else None
    percentage_rating = average_rating * 20 if average_rating is not None else None
    #return percentage_rating
    