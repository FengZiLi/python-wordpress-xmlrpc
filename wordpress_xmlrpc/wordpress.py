from .fieldmaps import FieldMap, IntegerFieldMap, DateTimeFieldMap, TermsListFieldMap
from wordpress_xmlrpc.exceptions import FieldConversionError


class WordPressBase(object):
    """
    Base class for representing a WordPress object. Handles conversion
    of an XML-RPC response to an object, and construction of a `struct`
    to use in XML-RPC requests.

    Child classes should define a `definition` property that contains
    the list of fields and a `FieldMap` instance to handle conversion
    for XML-RPC calls.
    """
    definition = {}

    def __init__(self, xmlrpc=None):
        # create private variable containing all FieldMaps for the `definition`
        self._def = {}

        for key, value in self.definition.items():
            # if the definition was not a FieldMap, create a simple FieldMap
            if isinstance(value, FieldMap):
                self._def[key] = value
            else:
                self._def[key] = FieldMap(value)

            # convert and store the value on this instance if non-empty
            try:
                converted_value = self._def[key].convert_to_python(xmlrpc)
            except Exception, e:
                raise FieldConversionError(key, e)
            if converted_value:
                setattr(self, key, converted_value)

    @property
    def struct(self):
        """
        XML-RPC-friendly representation of the current object state
        """
        data = {}
        for var, fmap in self._def.items():
            if hasattr(self, var):
                data.update(fmap.get_outputs(getattr(self, var)))
        return data

    def __repr__(self):
        return '<%s: %s>' % (self.__class__.__name__, unicode(self).encode('utf-8'))


class WordPressTaxonomy(WordPressBase):
    definition = {
        'name': 'name',
        'labels': 'labels',
        'hierarchical': 'hierarchical',
        'public': 'public',
        'query_var': 'query_var',
        'rewrite': 'rewrite',
        'show_ui': 'show_ui',
        'show_tagcloud': 'show_tagcloud',
        'show_in_nav_menus': 'show_in_nav_menus',
        'cap': 'cap',
        'is_builtin': '_builtin'
    }

    def __str__(self):
        return self.name


class WordPressTerm(WordPressBase):
    definition = {
        'id': 'term_id',
        'group': 'term_group',
        'taxonomy': 'taxonomy',
        'taxonomy_id': 'term_taxonomy_id',
        'name': 'name',
        'slug': 'slug',
        'description': 'description',
        'parent': 'parent',
        'count': IntegerFieldMap('count')
    }

    def __str__(self):
        return self.name


class WordPressPost(WordPressBase):
    definition = {
        'id': 'post_id',
        'user': 'post_author',
        'date': DateTimeFieldMap('post_date_gmt'),
        'date_modified': DateTimeFieldMap('post_modified_gmt'),
        'slug': 'post_name',
        'post_status': 'post_status',
        'title': 'post_title',
        'content': 'post_content',
        'excerpt': 'post_excerpt',
        'link': 'link',
        'comment_status': 'comment_status',
        'ping_status': 'comment_status',
        'terms': TermsListFieldMap(WordPressTerm, 'terms'),
        'custom_fields': 'custom_fields',
        'enclosure': 'enclosure',
        'password': 'post_password',
        'post_format': 'post_format',
        'thumbnail': 'post_thumbnail',
        'sticky': 'sticky',
        'post_type': FieldMap('post_type', default='post'),
    }

    def __str__(self):
        return self.title or self.slug


class WordPressPage(WordPressPost):
    definition = dict(WordPressPost.definition, **{
        'template': 'wp_page_template',
        'parent_id': 'wp_page_parent_id',
        'parent_title': 'wp_page_parent_title',
        'order': IntegerFieldMap('wp_page_order'),
        'post_type': FieldMap('post_type', default='page'),
    })


class WordPressComment(WordPressBase):
    definition = {
        'id': 'comment_id',
        'user': 'user_id',
        'post': 'post_id',
        'post_title': 'post_title',
        'parent': 'comment_parent',
        'date_created': DateTimeFieldMap('dateCreated'),
        'status': 'status',
        'content': 'content',
        'link': 'link',
        'author': 'author',
        'author_url': 'author_url',
        'author_email': 'author_email',
        'author_ip': 'author_ip',
    }

    def __str__(self):
        return self.content


class WordPressBlog(WordPressBase):
    definition = {
        'id': 'blogid',
        'name': 'blogName',
        'url': 'url',
        'xmlrpc': 'xmlrpc',
        'is_admin': FieldMap('isAdmin', default=False),
    }

    def __str__(self):
        return self.name


class WordPressAuthor(WordPressBase):
    definition = {
        'user_id': 'user_id',
        'user_login': 'user_login',
        'display_name': 'display_name',
    }

    def __str__(self):
        return self.display_name


class WordPressUser(WordPressBase):
    definition = {
        'user_id': 'userid',
        'nickname': 'nickname',
        'url': 'url',
        'first_name': 'firstname',
        'last_name': 'lastname',
    }

    def __str__(self):
        return self.nickname


class WordPressMedia(WordPressBase):
    definition = {
        'parent': 'parent',
        'title': 'title',
        'description': 'description',
        'caption': 'caption',
        'date_created': DateTimeFieldMap('date_created_gmt'),
        'link': 'link',
        'thumbnail': 'thumbnail',
        'metadata': 'metadata',
    }

    def __str__(self):
        return self.title


class WordPressOption(WordPressBase):
    definition = {
        'name': 'name',
        'description': 'desc',
        'value': 'value',
        'read_only': FieldMap('readonly', default=False),
    }

    def __str__(self):
        return '%s="%s"' % (self.name, self.value)


class WordPressPostType(WordPressBase):
    definition = {
        'name': 'name',
        'label': 'label',
        'labels': 'labels',
        'cap': 'cap',
        'capability_type': 'capability_type',
        'description': 'description',
        'exclude_from_search': 'exclude_from_search',
        'has_archive': 'has_archive',
        'hierarchical': 'hierarchical',
        'menu_icon': 'menu_icon',
        'menu_position': 'menu_position',
        'public': 'public',
        'publicly_queryable': 'publicly_queryable',
        'query_var': 'query_var',
        'rewrite': 'rewrite',
        'show_in_menu': 'show_in_menu',
        'show_in_nav_menus': 'show_in_nav_menus',
        'show_ui': 'show_ui',
        'taxonomies': 'taxonomies',
        'is_builtin': '_builtin'
    }

    def __str__(self):
        return self.label
