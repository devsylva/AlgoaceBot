
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


