"""
semantic URL processing

import semantical_url
reload(semantical_url)
test = semantical_url.semantical_url()
test_path = ["127.0.0.1:8888", "albums", "2", "3", "44", "99"]
test_path2 = ["127.0.0.1:8888", "albums", "anime", "0", "3", "44", "99"]
test.parse_uri (test_path)
print test.current_dir()
print test.return_current_uri()
print "-"*10
test.parse_uri (test_path2)
print test.current_dir()
print test.return_current_uri()
print "-"*10

"""
import collections
import string
import os
import os.path

def is_int(value_to_test):
    """
    Test to see if string is an integer.

    If integer, returns True.
    If not integer, returns False.
    """
    try:
        int(value_to_test)
        return True
    except ValueError:
        return False

def norm_number(page, max_number=None):
    """
    Normalize a integer (page).

    * Ensure that it is greater than Zero, and is not None.
        - If less than 1, or None, set it to 1

    * if max_number is None, then do not check for max_number
        * if greater than max_number, reset it to be max_number
    """
    if page == None or page < 1:
        page = 1

    if max_number != None:
        if page > max_number:
            page = max_number
    return page


class   semantical_url ():
    def __init__(self, pageitems=30):
        self.slots = collections.OrderedDict([('page', None),
                                              ('item', None),
                                              ('subpage', None),
                                              ('subitem', None)])
        self._current_dir = None
        self.page_items = pageitems

    def current_page(self):
        return self.slots['page']

    def current_item(self):
        return self.slots['item']

    def current_subpage(self):
        return self.slots['subpage']

    def current_subitem(self):
        return self.slots['subitem']

    def current_dir(self):
        return '/'.join(self._current_dir)

    def change_page(self, offset=None, max_page_count=None):
        if offset == None:
            return

        self.slots['page'] = norm_number(self.slots['page']+offset,
                                         max_page_count)

    def change_item(self, offset=None, max_item_count=None):
        """
change_item's use case is +1 / -1 incrementing through a gallery.

The logic works fine for +1 boundary between pages
        """
        if offset == None:
            return

        new_item = self.slots['item']+offset
        if new_item > max_item_count:
            self.change_page(offset=+1)
            new_item -= max_item_count
        elif new_item < 1 and self.current_page() > 1:
            self.change_page(offset=-1)
            if max_item_count != None:
                new_item += max_item_count
            else:
                new_item += self.page_items

        self.slots['item'] = new_item
#        self.slots['page'] = norm_number(self.slots['page']+offset,
#                                         max_item_count)



    def return_current_uri(self):
        uri = "%s/" % self.current_dir()
        for uri_part in self.slots.keys():
            if self.slots[uri_part] != None:
                uri += "%s/" % self.slots[uri_part]
        return uri

    def parse_uri(self, postpath=None):
        """
    postpath - a url broken in to a list (postpath from twisted)
    e.g. ["127.0.0.1:8888", "albums", "2", "3", "44", "99"]

    Decode the postpath list, and deconstruct the

    * Page
    * Item
    * subpage   (Archives)
    * subitem   (Archives)

    import gallery
    test =["127.0.0.1:8888", "albums", "2", "3", "44", "99"]
    gallery.new_decode_semantical_url(test)
    ctx={}
    test =["127.0.0.1:8888", "albums", "2", "3", "44", "99"]
    postpath, ctx["surl"] = gallery.new_decode_semantical_url(test)
        """
        def find_next_empty():
            """
            return next open slot key
            """
            for x in self.slots.keys():
                if self.slots[x] == None:
                    return x

        path_to_parse = postpath
        self.slots = collections.OrderedDict([('page', None),
                                              ('item', None),
                                              ('subpage', None),
                                              ('subitem', None)])
        self._current_dir = None
        if path_to_parse in [[], '', None]:
            self._current_dir = postpath

        for x_postpath in range(0, len(postpath)):
            if is_int(postpath[x_postpath].strip()):
                self.slots[find_next_empty()] = int(postpath[x_postpath])

        for removal in self.slots.keys():
            if self.slots[removal] != None:
                postpath.remove(str(self.slots[removal]))

        for key in self.slots.keys():
            self.slots[key] = norm_number(self.slots[key])

        self._current_dir = postpath

