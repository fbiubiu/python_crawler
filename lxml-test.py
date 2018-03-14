import lxml.html
html_content = '<ul class=country><li>Area<li>Population</ul>'
tree = lxml.html.fromstring(html_content)
fixed_html = lxml.html.tostring(tree, pretty_print=True)
print(fixed_html)
