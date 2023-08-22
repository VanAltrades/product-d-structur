# The Product Data Class

This repository offers an object-oriented framework for handling internal product information. 

Two approaches in this repository offer modular and scalable additions to product-centric methods/algorithms.

1. product initialization using your configurable, internal sql in a Class object
2. algorithmic methods found in themed python files that can be imported into the Class object 

The Product object exists in this `/src` directory which lives within the following folder structure:

```
.
 |-.env
 |-.gitignore
 |-data
 | |-pdfs
 | |-pdf_images
 | |-pdf_tables
 | |-pdf_text
 |-LICENSE
 |-preprocess
 | |-amazon-product-data.txt
 | |-process_txt.py
 | |-send_to_bq.py
 |-README.md
 |-requirements.txt
 |-secret.json
 |-src
 | |-config.py
 | |-config_secrets.py
 | |-content.py
 | |-internal.py
 | |-plots.py
 | |-Product.py
 | |-serps.py
 | |-trends.py
 | |-__init__.py
 |-tests
 | |-demo.ipynb
```

 ## Product.py

The `Product` data structure allows you to instantiate a product record from your internal product database.

This data structure leverages predefined algorithms to allow you to quickly access beneficial information about the product in the global marketplace.

By using this framework which instantiates product interest, competition, uses, and your own internal algorithms, you can optimize your product assortment efficiently.

 ## trends.py

 `trends.py` contains Product instance and staticmethods to display marketplace trends with ease.

 Currently, methods leverage open source apis.

 Pseudo-code functions exist in the file that could be outfit for paid apis like SERP volume monitoring.

 ![Report on marketplace trends related to your product](.\docs\producttrends.gif)

## plots.py

`plots.py` saves helpful staticmethods that allow you to visualize DataFrames found in your product's instance.

## content.py

`content.py` contains staticmethods that allow you to access large language models for text summarization and more.

You will need to install Pytorch on your machine to leverage the open source models provided by Huggingface that are included in this file.

Pseudo-code functions exist for paid apis like OpenAI as well.

 ## serps.py

`serps.py` contains Product instance and staticmethods to collect your product instance's search engine result page's competition and position.

To leverage Google's custom search api use the following documentation below.

The functions in this file also allow a user to download content from serps and save file, text, images, and tables within the `/docs` directory.

 ![Collect your product's data from search engine results pages](.\docs\serpsandpdfs.gif)

### Setting the Product class' serp.py methods
 Information found on Google's search engine results page can be an invaluable source of information about our product, it's competitors, and content associated with it.

 In order to collect information about your product using Google SERP information, I leverage `advertools`' `serp_goog()` method.

 In order to use this functionality, you will need to add your own search engine api key and id within the `config.py` file as `SE_API_KEY = ""` `SE_ID = ""`

 These credentials can be created through Google Cloud Platform and the Google's Programmable Search Engine offering.

 For more information, this article was very helpful: [Data Science for SEO](https://www.holisticseo.digital/python-seo/data-science/)

 #### Setup a Custom Search API Key

 Navigate to your GCP Project dashboard.

 Navigate to APIs & Services > Library > Custom Search API > Click "Enable"

 From the Custom Search API Service Details page, navigate to Credentials > Configure OAuth Consent to fill out information about your use-case

 From the Credentials page > Select Create Credentials > API key > copy your api key to the SE_API_KEY config variable. Don't share this with anyone/leave it in your public repository.

 #### Setup a Programmable Search Engine ID 

 Navigate to [Google's Programmable Search Engine](https://programmablesearchengine.google.com/controlpanel/all) offering.

 Click Add > Configure the engine with your needs (I select "search the entire web") 

 Copy your Search Engine ID from the URL provided (src="https://cse.google.com/cse.js?cx=`SE_ID`") into your `SE_ID` config variable.


<br><br><br>

# (Data Warehouse Prerequisite) Preprocess Product Data - Setting up a Product Dimension Table in Google BigQuery

Your organization will likely have an internal table that's primary purpose is to store product dimension data.

In this repository, I am extracting an open source product dataset and storing it as a table in Google's BigQuery resource.

If you already have a product dataset you plan on using, feel free to skip this step or review it as a refresher on how to process a text file as a dictionary and send that dictionary's dataframe to a database.

I use the following dataset as my example product dataset:

[Amazon E-Commerce Dataset Text File](https://raw.githubusercontent.com/sameeravithana/Amazon-E-commerce-Data-set/master/Data-sets/amazondata_Electronics_14200%20142.txt)

In the `/preprocess` directory, I save the .txt file.

Then I created ETL functions in `process_txt.py`.

2 functions exist. The first...

`get_dict_from_txt(txt_file='amazon-product-data.txt')`

... takes the text file as an input and returns a dictionary with key value pairs extracted from the txt files format, as well as a set of unique keys(which we need to format schema in a database).

The second function...

`get_structured_dict(d, unique_keys)`

... loops through the dictionary's items and formats them into a structured dictionary using the unique_key set as a schema. If a record does not contain items matching a string in the set, then it will record that value as None.

With this d_schema dictionary, the `send_to_bq.py` file simply formats important keys first in a dataframe and sends that dataframe to the BigQuery table you designate.