class ResultPage:
    def __init__(self, driver):
        self.driver = driver

    def go_to_next_page(self):
        pagination_items = self.driver.find_elements_by_class_name("pagination-item")
        index = 0
        for index, item in enumerate(pagination_items):
            if "active-page" in item.get_attribute("class"):
                break 
        try:
            self.driver.implicitly_wait(100)
            next_item = pagination_items[index+1]
            next_item.click()
            self.driver.implicitly_wait(3)
            return True
        except:
            self.driver.implicitly_wait(3)
            return False

    def _get_result_image(self, index):
        """
        get image link for "single-listing-search-result-wrapper" element
        """
        try:
            result = self.get_results()[index]
            element = result.find_element_by_class_name("single-listing-image")
            return element.get_attribute("src")
        except:
            return None

    def _get_result_type(self, index):
        """
        get type of home for "single-listing-search-result-wrapper" element
        """
        try:
            result = self.get_results()[index]
            element = result.find_element_by_class_name("type-of-home-label")
            return element.text.strip()
        except:
            return None

    def _get_result_beds(self, index):
        """
        get number of beds for "single-listing-search-result-wrapper" element
        """
        try:
            result = self.get_results()[index]
            element = result.find_element_by_class_name("bedrooms-label")
            return element.text
        except:
            return None

    def _get_result_baths(self, index):
        """
        get number of baths for "single-listing-search-result-wrapper" element
        """
        try:
            result = self.get_results()[index]
            element = result.find_element_by_class_name("bathrooms-label")
            return element.text
        except:
            return None

    def _get_result_timestamp(self, index):
        """
        get timestamp for "single-listing-search-result-wrapper" element
        """
        try:
            result = self.get_results()[index]
            element = result.find_element_by_class_name("daysonsite-label")
            return element.text
        except:
            return None

    def _get_result_address(self, index):
        """
        get address for "single-listing-search-result-wrapper" element
        """
        try:
            result = self.get_results()[index]
            element = result.find_element_by_class_name("single-listing-address-row")
            return element.get_attribute("title")
        except:
            return None

    def _get_result_municipality(self, index):
        """
        get municipality for "single-listing-search-result-wrapper" element
        """
        try:
            result = self.get_results()[index]
            element = result.find_element_by_class_name("single-listing-municipality-row")
            return element.get_attribute("title")
        except:
            return None

    def _get_result_price(self, index):
        """
        get price for "single-listing-search-result-wrapper" element
        """
        try:
            result = self.get_results()[index]
            element = result.find_element_by_class_name("active-price")
            return element.text
        except:
            return None

    def get_results(self):
        return self.driver.find_elements_by_class_name("single-listing-search-result-wrapper")

    def get_result_info(self, index):
        image = self._get_result_image(index)
        type = self._get_result_type(index)
        beds = self._get_result_beds(index)
        baths = self._get_result_baths(index)
        timestamp = self._get_result_timestamp(index)
        address = self._get_result_address(index)
        municipality = self._get_result_municipality(index)
        price = self._get_result_price(index)
        return {
            "image": image,
            "type": type,
            "beds": beds,
            "baths": baths,
            "timestamp": timestamp,
            "address": address,
            "municipality": municipality,
            "price": price
        }
