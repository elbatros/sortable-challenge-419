import json
import math
import logging
logger = logging.getLogger(__name__)

class Utils(object):
    """Util functions

    Keep original copy and processed str in attributes 
    """

    # lowcase and replease non letter/number by " " 
    @staticmethod
    def preprocess(raw_str):
        raw_str = raw_str.strip().lower()
        return "".join([ c if c.isalnum() else " " for c in raw_str ])

class Product(object):
    """Product info
    """
    def __init__(self, json_str):
        self.product_name = ""
        self.manufacturer = ""
        self.model = ""
        self.family = ""
        self.json_obj = {}

        try:
            self.json_obj = json.loads(json_str.strip())
        except RuntimeError as e:
            logger.error("Parse error, " + str(e.message))

        try:
            self.product_name = Utils.preprocess(self.json_obj["product_name"])
            self.manufacturer = Utils.preprocess(self.json_obj["manufacturer"])
            self.model = Utils.preprocess(self.json_obj["model"])
            self.family = Utils.preprocess(self.json_obj.get("family", "")) #optional
        except RuntimeError as e:
            logger.error("Unexpected data missing, " + str(e.message))

class Listing(object):
    """Listing info

    Keep original copy and processed str in attributes
    """

    def __init__(self, json_str):
        self.title = ""
        self.manufacturer = ""
        self.json_obj = {}

        try:
            self.json_obj = json.loads(json_str.strip())
        except RuntimeError as e:
            logger.error("Parse error" + str(e.message))
        try:
            self.title = Utils.preprocess(self.json_obj["title"])
            self.manufacturer = Utils.preprocess(self.json_obj["manufacturer"])
        except RuntimeError as e:
            logger.error("Unexpected data missing, " + str(e.message))

class InvertIdx(object):
    """InvertIdx and IDF score

    Provide method to insert terms and maintain invert doc idx, IDF score

    invert_idx: {
        term-1: {
            "idf": double,
            "doc_ids": {
                int(doc_id): int(count),
                ...
            },
            ...
        },
        ...
    }
    """
    
    def __init__(self):
        self.invert_idx = {}
        self.doc_ids = {}

    def insert_term(self, term, doc_id):
        self.doc_ids.setdefault(doc_id, True)
        term_obj = self.invert_idx.setdefault(term, {"idf": 0.0, "doc_ids": {}})
        term_obj["doc_ids"].setdefault(doc_id, 0)
        term_obj["doc_ids"][doc_id] += 1

    def calculate_idf(self):
        for term_val in self.invert_idx.values():
            term_val["idf"] = math.log( float(len(self.doc_ids)) / float(len(term_val["doc_ids"])) )