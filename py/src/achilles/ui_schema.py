def ui_schema(args=None, context=None):
    return {
        "FoodItem": {
            "upc": {"type": "text", "label": "UPC Code"},
            "sku": {"type": "text", "label": "SKU"},
            "lot": {"type": "text", "label": "Lot Number"},
            "serial": {"type": "text", "label": "Serial Number"},
            "name": {"type": "text", "label": "Name", "required": True},
            "title": {"type": "text", "label": "Title"},
            "description": {"type": "textarea", "label": "Description"},
            "brandid": {"type": "integer", "label": "Brand ID"},
            "manufid": {"type": "integer", "label": "Manufacturer ID"},
            "qsr": {"type": "bool", "label": "Quick Service Restaurant?"},
            "msgpresent": {"type": "bool", "label": "MSG Present?"},
            "msgonlabel": {"type": "bool", "label": "MSG on Label?"},
            "dsgpresent": {"type": "bool", "label": "DSG Present?"},
            "dsgonlabel": {"type": "bool", "label": "DSG on Label?"},
            "frozen": {"type": "bool", "label": "Frozen?"},
            "wic": {"type": "bool", "label": "WIC Eligible?"},
            "price": {"type": "float", "label": "Price"},
            "quantity": {"type": "text", "label": "Quantity"},
            "producturl": {"type": "text", "label": "Product URL"},
        },
        "Search": {
            "filter_msg": {"type": "bool", "label": "MSG Only"},
            "filter_qsr": {"type": "bool", "label": "QSR Only"},
            "filter_vendor": {"type": "text", "label": "Vendor"},
        },
    }
