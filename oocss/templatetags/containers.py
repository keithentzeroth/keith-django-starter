from django.template import Library, Node, TemplateSyntaxError
from django.template.loader import render_to_string

register = Library()
     
class ModTag(Node):
    def __init__(self, skin, nodelist):
        self.skin = skin
        self.nodelist = nodelist
    
    def render(self, context):
        request = context['request']                
        context['mod_skin'] = self.skin
        output = self.nodelist.render(context)        
        h = output.find("</modhead>")
        if h != -1:
            context['mod_head'] = output[output.find("<modhead>")+9:h]
        else:
            context['mod_head'] = None
        b = output.find("</modbody>")
        if b != -1:
            context['mod_body'] = output[output.find("<modbody>")+9:b]
        else:
            context['mod_body'] = None
        str = render_to_string('tags/mod.html', context)
        return str
 
def mod(parser, token):

    skins = token.contents[3:]
        
    nodelist = parser.parse(('endmod',))
    parser.delete_first_token()
    
            
    return ModTag(skins, nodelist)

class ModHead(Node):
    def __init__(self, nodelist):
        self.nodelist = nodelist
    
    def render(self, context):
        output = self.nodelist.render(context)        
        return '<modhead>' + output + '</modhead>'

def modhead(parser,token):
    nodelist = parser.parse(('endmodhead',))
    parser.delete_first_token()
    return ModHead( nodelist) 


class ModBody(Node):
    def __init__(self, nodelist):
        self.nodelist = nodelist
    
    def render(self, context):
        output = self.nodelist.render(context)        
        return '<modbody>' + output + '</modbody>'

def modbody(parser,token):
    nodelist = parser.parse(('endmodbody',))
    parser.delete_first_token()
    return ModBody(nodelist)

register.tag('mod', mod)
register.tag('modhead', modhead)
register.tag('modbody', modbody)
