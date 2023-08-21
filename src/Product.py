from .config import CLIENT, PRODUCT_TABLE_ID

class Product:

    from .serps import get_serp_brand_mpn, get_serp_pdfs, download_pdfs, extract_pdf_text
    from .content import get_txt_files_as_str_list, generate_summary_huggingface_t5
    from .trends import get_interest_keywords_product, get_interest_trends_product, get_interest_keywords_brand, get_interest_trends_brand
    from .plots import plot_line

    def __init__(self, mpn):
        self._mpn = mpn
        self._attributes = self.get_product_attributes()
        self._brand = self._attributes['Brand'][0]
        self._title = self._attributes['Title'][0]
        self._manufacturer = self._attributes['Manufacturer'][0]
        self._product_group = self._attributes['ProductGroup'][0]
        self._product_type = self._attributes['ProductTypeName'][0]

    def get_product_attributes(self):
        query = f"""
            SELECT *
            FROM `{PRODUCT_TABLE_ID}`
            WHERE MPN = '{self._mpn}'
        """
        query_job = CLIENT.query(query)
        results = query_job.result()
        df = results.to_dataframe()
        return df