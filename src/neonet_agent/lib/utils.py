def extract_symbol(coin_address):
    """Extract symbol from coin address format: address::module::SYMBOL"""
    parts = coin_address.split("::")
    return parts[-1].lower() if len(parts) >= 3 else ""
