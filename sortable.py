import argparse
import json
import sys
from data import Product, Listing
from processing import DataMapping

import logging
logging.basicConfig(level = logging.ERROR)

def main(args):
    products = []
    listings = []
    with open(args.products, "r") as fin:
        for line in fin:
            products.append(Product(line))
            
    with open(args.listings, "r") as fin:
        for line in fin:
            listings.append(Listing(line))

    # link listings to products
    product_to_listings = DataMapping.product_listing_mapping(products, listings)
    
    with open(args.output, "w") as fout:
        for product_idx in range(len(product_to_listings)):
            obj = {"product_name": products[product_idx].json_obj["product_name"], "listings": []}
            for listing_idx in product_to_listings[product_idx]:
                obj["listings"].append(listings[listing_idx].json_obj)
            #fout.write(json.dumps(obj, sort_keys=True, indent=4) + "\n") 
            fout.write(json.dumps(obj) + "\n") 

if __name__ == "__main__": 
    parser = argparse.ArgumentParser(description='sortable challenge')
    parser.add_argument("-p", "--products", help="products file", required=True)
    parser.add_argument("-l", "--listings", help="listings file", required=True)
    parser.add_argument("-o", "--output", help="output file", required=True)
    args = parser.parse_args()

    main(args)