"""
semantic URL processing

:Module: Semantic URL Processing
:Date: 2015-03-21
:Platforms: Mac, Windows, Unix (Tested under Mac OS X)
:Version: TBD
:Authors:
    - Benjamin Schollnick


:Description:
    Parses, and manipulates semantical URLS.

    Designed for the Gallery application.

**Modules Used (Batteries Included)**:

   * Collections
   * os
   * os.path
   * string

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
import copy

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



def pre_slash(path):
    """
    Connivence function to ensure prepended slash to a path
    """
    if path=='':
        path = "/"
        return path

    if path[0] != '/':
        path = '/' + path
    return path

def post_slash(path):
    """
    Connivence function to ensure postpended slash to a path
    """
    if path=='':
        path = "/"
        return path

    if path[-1] != '/':
        path = path +'/'
    return path

class   semantical_url():
    """
        The primary class for semantical manipulation.
    """
    def __init__(self, pageitems=30):
        """
    Args:
        * pageitems (integer): The maximum number of items in a directory.

    Returns:
        NA
        """
        self.slots = collections.OrderedDict([('page', None),
                                              ('item', None),
                                              ('subpage', None),
                                              ('subitem', None)])
        self._current_dir = None
        self.page_items = pageitems
        self.original_uri = None

    def current_page(self):
        """
    Args:
        * None

    Returns:
        Integer - The current Page being viewed
        """
        return self.slots['page']

    def current_item(self):
        """
    Args:
        * None

    Returns:
        Integer - The current item being viewed
        """
        return self.slots['item']

    def current_subpage(self):
        """
    Args:
        * None

    Returns:
        Integer - The current SubPage being viewed
        """
        return self.slots['subpage']

    def current_subitem(self):
        """
    Args:
        * None

    Returns:
        Integer - The current subitem being viewed
        """
        return self.slots['subitem']

    def current_dir(self):
        """
    Args:
        * None

    Returns:
        String - The URL/URI before the semantical components
        """
        return '/'.join(self._current_dir)

    def change_page(self, offset=None, max_page_count=None, nom=True):
        """
    Args:
        * offset - Integer - The positive / negative change to apply
          to the page.
        * max_page_count - The maximum number of pages available.
        * nom - None on Max or Min - If max number of pages reached,
          return none instead of forcing back into range.

    Returns:
        Boolean - True if successful, False if nom is True and the
        value was forced back within the boundry.
        """
        if offset == None:
            return

        if self.slots['page'] == None:
            self.slots['page'] = 1

        if (self.slots['page']+offset > max_page_count) and nom:
            return None
        elif (self.slots['page']+offset < 1) and nom:
            return None
        else:
            self.slots['page'] = norm_number(self.slots['page']+offset,
                                             max_page_count)
        return True

    def change_item(self, offset=None, max_item_count=None, nom=True):
        """
    Args:
        * offset - Integer - The positive / negative change to apply
          to the item.
        * max_item_count - The maximum number of items available.
        * nom - None on Max or Min - If max or min number of itemsreached,
          return none instead of forcing back into range.

    Returns:
        Boolean - True if successful, False if nom is True and the
        value was forced back within the boundry.

    change_item's use case is +1 / -1 incrementing through a gallery.

    The logic works fine for +1 boundary between pages
        """
        if offset == None:
            return

        if self.slots['item'] == None:
            self.slots['item'] = 1

        new_item = self.slots['item']+offset
        if new_item > max_item_count:
            new_item -= max_item_count
        elif new_item < 1 and self.current_page() > 1:
            self.change_page(offset=-1, nom=False)
            if max_item_count != None:
                new_item += max_item_count
            else:
                new_item += self.page_items

        self.slots['item'] = new_item
        return True

    def return_current_uri(self):
        """
        Args:
            * None

        Returns:
            String - Returns the full postpath & semantical components

        *NOTE* may not contain the server & port numbers.  That depends on
        what was provided to the parser.

        """
        uri = post_slash("%s" % self.current_dir())
        for uri_part in self.slots.keys():
            if self.slots[uri_part] != None:
                uri += "%s/" % self.slots[uri_part]
        return uri

    def revert_to_parsed(self):
        """
    Force semantical url to be reset back to the previously parsed
    URI.

    In this manner, you can use this as a URI creator.

    test = semantical_url.semantical_url()
    test_path = ["127.0.0.1:8888", "albums", "2", "3", "44", "99"]
    test.parse_uri (test_path)
    print test.return_current_uri()
        127.0.0.1:8888/albums/2/3/44/99/
    test.change_page(offset=2)
    next_url = test.return_current_uri()
    print next_url
        127.0.0.1:8888/albums/4/3/44/99/
    test.revert_to_parsed()
    test.change_page(offset=-1)
    prev_url = test.return_current_uri()
    print prev_url
        127.0.0.1:8888/albums/1/3/44/99/
        """
        self.parse_uri(self.original_uri)

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

        self.original_uri = copy.deepcopy(postpath)
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

        self._current_dir = postpath

