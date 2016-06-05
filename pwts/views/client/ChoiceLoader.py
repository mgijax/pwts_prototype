"""
Generate choices for form selection
"""
from pwts.model.cv import User

def gen_vocab_choices(cv_class):
    """
    Generate option choices for controlled vocab class (cv_class)
    
    only return active terms
    """
    values = cv_class.query \
        .filter_by(active=True) \
        .all()
    choices = [(x.name, x.name) for x in values]
    choices.sort()
    return choices
    
def gen_user_choices():
    """
    Generate option choices for users
    
    only return active users
    """
    users = User.query \
        .filter_by(active=True) \
        .all()
    choices = [(x.login, x.login) for x in users]
    choices.sort()
    return choices
    