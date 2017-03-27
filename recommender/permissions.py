def has_l0d_permission(user):
    return user.groups.filter(name='L0D').exists()

def has_roborisk_permission(user):
    return user.groups.filter(name='RoboRisk').exists()

def has_recommender_permission(user):
    return user.groups.filter(name='Recommender').exists()

def has_shopgo_permission(user):
    return user.groups.filter(name='ShopGo').exists()

def has_bidloan_permission(user):
    return user.groups.filter(name='BidLoan').exists()