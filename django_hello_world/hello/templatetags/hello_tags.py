from django import template
from django.core.urlresolvers import reverse

register = template.Library()


@register.tag(name="edit_link")
def do_edit_link(parser, token):
    try:
        # split_contents() knows not to split quoted strings.
        tag_name, object_string = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError("%r tag requires a single argument" % token.contents.split()[0])
    return EditLinkNode(object_string)


class EditLinkNode(template.Node):
    def __init__(self, tp_object):
        self.tp_object = template.Variable(tp_object)

    def url_to_edit_object(self, real_object):
        url = reverse(
            'admin:%s_%s_change' %
            (real_object._meta.app_label,  real_object._meta.module_name),
            args=[real_object.id]
        )
        return u'<a href="%s">(admin)</a>' % url

    def render(self, context):
        print self.tp_object
        real_object = self.tp_object.resolve(context)
        print self.url_to_edit_object(real_object)
        return self.url_to_edit_object(real_object)