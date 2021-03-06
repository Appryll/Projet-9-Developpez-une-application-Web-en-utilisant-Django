from django.contrib.auth.models import User
from review.models import Review, Ticket
from authentication.models import Relationship

def get_user_follows(user):
    """Returns list of users followed by current user"""
    follows = Relationship.objects.filter(from_user=user)
    followed_users = []
    for follow in follows:
        followed_users.append(follow.to_user)
    return followed_users

def get_user_viewable_reviews(user: User):
    """
    All viewable reviews for user feed:
    Reviews by followed users + current user
    Reviews to current user tickets if review author is not followed

    @param user: currently logged-in User instance
    @return: filtered reviews queryset with no duplicate results
    """
    followed_users = get_user_follows(user)
    followed_users.append(user)

    reviews = []
    all_reviews = Review.objects.filter(user__in=followed_users).distinct()
    for review in all_reviews:
        reviews.append(review.id)

    user_tickets = Ticket.objects.filter(user=user)
    for ticket in user_tickets:
        review_responses = Review.objects.filter(ticket=ticket)
        for review in review_responses:
            reviews.append(review.id)
    reviews = Review.objects.filter(id__in=reviews).distinct()
    return reviews

def get_user_viewable_tickets(user: User):
    """
    All viewable tickets for user feed:
    Tickets by followed users + current user
    Filter out tickets with review response if review author is followed

    @param user: currently logged-in User instance
    @return: filtered tickets queryset
    """
    followed_users = get_user_follows(user)
    followed_users.append(user)

    tickets = Ticket.objects.filter(user__in=followed_users)
    for ticket in tickets:
        try:
            replied = Review.objects.get(ticket=ticket)
            if replied and replied.user in followed_users:
                tickets = tickets.exclude(id=ticket.id)

        except Review.DoesNotExist:
            pass
    return tickets

def get_replied_tickets(tickets):
    """
    Get tickets with review response
    Get corresponding review to link to for detail view

    @param tickets: user tickets queryset
    @return: list of tickets with response, list of review responses to corresponding tickets
    """
    replied_tickets = []
    replied_reviews = []

    for ticket in tickets:
        try:
            replied = Review.objects.get(ticket=ticket)
            if replied:
                replied_tickets.append(replied.ticket)
                replied_reviews.append(replied)

        except Review.DoesNotExist:
            pass
    return replied_tickets, replied_reviews
