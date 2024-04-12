def is_admin(user):
    """
    Vérifie si l'utilisateur est un administrateur.
    """
    return user.is_authenticated and user.is_superuser

def is_standard_user(user):
    """
    Vérifie si l'utilisateur est un utilisateur standard.
    """
    return user.is_authenticated and not user.is_superuser
