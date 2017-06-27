import json
from data import InvertIdx
from operator import itemgetter
import logging
logger = logging.getLogger(__name__)


class DataMapping(object):
    """Static methods for listing - product mapping
    """

    @staticmethod
    def find_product(products, listing, invert_idx):
        """Find top relevant product idx
        
        Calculate TF*IDF for potential products. Sort scores in decending order.
        Find the first product that model and family must match.
        
        Args:
            param1: products list
            param2: listing
            param3: InvertIdx obj of listing's manufacturer or None if not found
        Returns:
            product idx or None if not found
        """

        if invert_idx is None:
            return None

        prod_id_to_score = {}
        title_tokens = listing.title.split()
        for term in title_tokens:
            term_obj = invert_idx.invert_idx.get(term, None)
            if term_obj is not None:
                for product_id in term_obj["doc_ids"]:
                    prod_id_to_score.setdefault(product_id, 0.0)    
                    prod_id_to_score[product_id] += term_obj["idf"]/float(len(title_tokens))

        if len(prod_id_to_score) == 0:
            # no potential products found
            return None

        prod_id_to_score = sorted(prod_id_to_score.iteritems(), key=itemgetter(1), reverse=True)
        logger.debug("ProductId to scores: " + str(prod_id_to_score))
        
        # find the first matched product
        # for each term in product's model and family, see if they can be found in title_tokens
        # fix partial matching issue like target model 'D60' but get 'D600'
        title_tokens_dict = { title_tokens[i]: True for i in range(len(title_tokens)) } # use dict for better lookup performance
        for (prod_id, score) in prod_id_to_score:
            prod = products[prod_id]
            is_found = True
            # deal with model
            for term in prod.model.split():
                if not term in title_tokens_dict:
                    is_found = False
                    break
            # deal with family
            # family is an optional field, "" if not provided
            if is_found and prod.family != "":
                for term in prod.family.split():
                    if not term in title_tokens_dict:
                        is_found = False
                        break
            if is_found:
                return prod_id

        return None

    @staticmethod
    def product_listing_mapping(products, listings):
        """Link listings to products

        Build reverse index with IDF score for each manufacturer in products.
        Find top relevant product for each listing.

        Args:
            param1: products list
            param2: listings list
        Returns:
            product id list to coressponding listings list
        """
        
        # build reverse index
        manufacturer_to_invert_idx = {}

        for productIdx in range(len(products)):
            prod = products[productIdx]
            logger.debug("productIdx: " + str(productIdx) + ", manufacturer: " + prod.manufacturer)
            invert_idx = manufacturer_to_invert_idx.setdefault(prod.manufacturer, InvertIdx())
            logger.debug("invert_idx: " + str(invert_idx.invert_idx))
            for term in prod.product_name.split():
                logger.debug("term: " + term)
                invert_idx.insert_term(term, productIdx)
            logger.debug("invert_idx after insert: " + str(invert_idx.invert_idx))
        
        # calculate idf
        for invert_idx in manufacturer_to_invert_idx.values():
            invert_idx.calculate_idf()

        # assgin listing to products
        num_assigned = 0
        product_to_listings = [ [] for i in range(len(products)) ]
        for listingIdx in range(len(listings)):
            listing = listings[listingIdx]
            logging.debug("Process listing with manufacturer: " + listing.manufacturer)

            productIdx = DataMapping.find_product(products, listing, manufacturer_to_invert_idx.get(listing.manufacturer, None))
            if productIdx is not None:
                product_to_listings[productIdx].append(listingIdx)
                num_assigned += 1

        # the percentage of listings matched
        print str(num_assigned) + " out of " + str(len(listings)) \
              + " ("+ str( 100.0*float(num_assigned)/float(len(listings)) ) + "%) listings" \
              + " successfully assigned to products."
        
        return product_to_listings