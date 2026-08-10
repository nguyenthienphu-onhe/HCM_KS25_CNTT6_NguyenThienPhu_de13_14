def clean_and_validate_products(products):
    valid_products = []
    for p in products:
        cleaned_code = p["product_code"].strip().upper()
        if len(cleaned_code) == 4 and cleaned_code[0] == 'P' and cleaned_code[1:].isdigit():
            p_copy = p.copy()
            p_copy["product_code"] = cleaned_code
            valid_products.append(p_copy)
            
    return valid_products