from asgiref.sync import sync_to_async


@sync_to_async
def getDepositAddress(currency):
    try:
        address = CryptoAddress.objects.get(currency=currency, is_active=True)
        
        if address:
            return {
                'address': address.address,
                'memo': address.memo,
                'network': address.network
            }
        else:
            return None
    except CryptoAddress.DoesNotExist:
        return None


@sync_to_async
def getTransactionhistory(user, limit=10):
    return Transaction.objects.filter(user=user).order_by('-created_at')[:limit]


@sync_to_async
def getFaqCategories():
    """Get all active FAQ categories"""
    return FAQ.objects.filter(
        is_active=True
    ).values('category').distinct()

@sync_to_async
def getCategoryFaqs(category):
    """Get all FAQs for a category"""
    return FAQ.objects.filter(
        category=category,
        is_active=True
    ).order_by('order')