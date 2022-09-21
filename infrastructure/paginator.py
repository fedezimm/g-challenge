class Paginator(object):
    def __init__(self, df, rows_per_page, page_number):
        self.df = df
        self.max_count = len(df)
        self.rows_per_page = rows_per_page
        self.page_number = page_number
        self.total_pages = (self.max_count + self.rows_per_page - 1) // self.rows_per_page
    
    def page(self):
        inf = (self.page_number - 1) * self.rows_per_page
        sup = self.rows_per_page * self.page_number
        df = self.df[inf:sup]
        if self.page_number > self.total_pages:
            return None, None
        metadata = Metadata(self.page_number, self.total_pages, self.rows_per_page, len(df), self.max_count)
        return df, metadata
    
class Metadata(object):
    def __init__(self, page_number, total_pages, rows_per_page, page_count, max_count):
        self.page_number = page_number
        self.total_pages = total_pages
        self.rows_per_page = rows_per_page
        self.page_count = page_count
        self.max_count = max_count
    
    def add_counts(self, good_count, bad_count):
        self.good_count = good_count
        self.bad_count = bad_count