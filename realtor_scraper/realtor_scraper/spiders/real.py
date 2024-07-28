import scrapy
from urllib.parse import urljoin

class RealtorSpider(scrapy.Spider):
    name = 'real'
    allowed_domains = ['realtor.com']

    def __init__(self, listing_type=None, *args, **kwargs):
        super(RealtorSpider, self).__init__(*args, **kwargs)
        self.listing_type = listing_type

        if not self.listing_type:
            raise ValueError("You must provide a listing type such as 'show-newest-listings', 'show-price-reduced', or 'show-recently-sold'.")
        self.base_url = 'https://www.realtor.com/realestateandhomes-search/Panama-City-Beach_FL/'
        self.start_urls = [
            f'{self.base_url}{self.listing_type}/sby-6'
        ]

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # Check if response is loaded correctly
        if not response:
            self.logger.error('Response not received')
            return

        # Update the selector for the property container
        for property in response.css('section.PropertiesList_propertiesContainer__Vox4I.PropertiesList_listViewGrid__bttyS .BasePropertyCard_propertyCardWrap__30VCU'):
            #address = property.css('.PropertyCardstyles__StyledCardTitle-rui__sc-7yjdgx-1 address::text').get()
            #price = property.css('.CardPrice__Price-rui__sc-1m983j-0 span::text').get()
            price = property.css('div[data-testid="card-price"]::text').get()

            #beds = property.css('.PropertyCardstyles__StyledPropertyStats-rui__sc-7yjdgx-2 span[data-label="pc-meta-beds"]::text').get()
            #baths = property.css('.PropertyCardstyles__StyledPropertyStats-rui__sc-7yjdgx-2 span[data-label="pc-meta-baths"]::text').get()
            baths = property.css('li[data-testid="property-meta-baths"] span[data-testid="meta-value"]::text').get()
            sqft = property.css('li[data-testid="property-meta-sqft"] span[data-testid="meta-value"]::text').get()

            #sqft = property.css('.PropertyCardstyles__StyledPropertyStats-rui__sc-7yjdgx-2 span[data-label="pc-meta-sqft"]::text').get()
            # lot_size = property.css('.PropertyCardstyles__StyledPropertyStats-rui__sc-7yjdgx-2 span[data-label="pc-meta-lotsize"]::text').get()
            # broker = property.css('.BrokerTitle_titleText__RvFV6::text').get()

            # Debugging information
            self.logger.debug(f" Price: {price}, Baths: {baths}, Sqft: {sqft}")
            #Extracted data - Address: {address}, Beds: {beds},, Lot size: {lot_size}, Broker: {broker}
            yield {
                #'address': address.strip() if address else None,
                'price': price.strip() if price else None,
                #'beds': beds.strip() if beds else None,
                'baths': baths.strip() if baths else None,
                'sqft': sqft.strip() if sqft else None,
                #'lot_size': lot_size.strip() if lot_size else None,
                #'broker': broker.strip() if broker else None,
            }

        # # Follow pagination links if available
        # next_page = response.css('a[aria-label="next page"]::attr(href)').get()
        # if next_page:
        #     next_page_url = urljoin(response.url, next_page)
        #     yield scrapy.Request(next_page_url, callback=self.parse)
