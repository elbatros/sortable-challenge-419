# Sortable Challenge

Precision is the fist concern in this solution to make sure no unrelated listings linked with products.

The solution builds inverted index and IDF (inverse document frequency) for product title. To be specific, it maintains individual structure for each manufacturer to reduce searching overhead. I use TF-IDF to get rid of unimportant terms from listing's title.

For each coming listings, it starts from the manufacturer, calculate TF-IDF scores for all potential products. Thereafter, it sorts potential products by score. From the top relevant product, link listing to it only if model and family are matched.

## Usage
```
usage: sortable.py [-h] -p PRODUCTS -l LISTINGS -o OUTPUT

sortable challenge

optional arguments:
  -h, --help            show this help message and exit
  -p PRODUCTS, --products PRODUCTS
                        products file
  -l LISTINGS, --listings LISTINGS
                        listings file
  -o OUTPUT, --output OUTPUT
                        output file
```
Example:
```
$ python sortable.py -p challenge_data_20110429/products.txt -l challenge_data_20110429/listings.txt -o output.txt
6366 out of 20196 (31.5210932858%) listings successfully assigned to products.
```