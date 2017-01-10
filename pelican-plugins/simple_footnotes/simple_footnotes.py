from pelican import signals
import html5lib

RAW_FOOTNOTE_CONTAINERS = ["code"]


def getText(node, recursive=False):
    """Get all the text associated with this node.
       With recursive == True, all text from child nodes is retrieved."""
    L = ['']
    for n in node.childNodes:
        if n.nodeType in (node.TEXT_NODE, node.CDATA_SECTION_NODE):
            L.append(n.data)
        else:
            if not recursive:
                return None
        L.append(getText(n))
    return ''.join(L)


def parse_for_footnotes(article_generator):
    s = (html5lib.serializer.htmlserializer
         .HTMLSerializer(omit_optional_tags=False,
                         quote_attr_values=True))
    articles = (elem for elem
                in article_generator.drafts + article_generator.articles)
    for article in articles:
        if "[ref]" in article._content and "[/ref]" in article._content:
            content = (article._content.replace("[ref]", "<x-simple-footnote>")
                       .replace("[/ref]", "</x-simple-footnote>"))
            parser = html5lib.HTMLParser(tree=html5lib.getTreeBuilder("dom"))
            dom = parser.parse(content)
            endnotes = []
            count = 0
            for footnote in dom.getElementsByTagName("x-simple-footnote"):
                pn = footnote
                leavealone = False
                while pn:
                    if pn.nodeName in RAW_FOOTNOTE_CONTAINERS:
                        leavealone = True
                        break
                    pn = pn.parentNode
                if leavealone:
                    continue
                count += 1
                fnid = "sf-%s-%s" % (article.slug, count)
                fnbackid = "%s-back" % (fnid,)
                endnotes.append((footnote, fnid, fnbackid))
                number = dom.createElement("sup")
                number.setAttribute("id", fnbackid)
                numbera = dom.createElement("a")
                numbera.setAttribute("href", "#%s" % fnid)
                numbera.setAttribute("class", "simple-footnote")
                numbera.appendChild(dom.createTextNode(str(count)))
                txt = getText(footnote, recursive=True).replace("\n", " ")
                numbera.setAttribute("title", txt)
                number.appendChild(numbera)
                footnote.parentNode.insertBefore(number, footnote)
            if endnotes:
                ol = dom.createElement("ol")
                ol.setAttribute("class", "simple-footnotes")
                for e, fnid, fnbackid in endnotes:
                    li = dom.createElement("li")
                    li.setAttribute("id", fnid)
                    li.setAttribute("class", "footnote")
                    while e.firstChild:
                        li.appendChild(e.firstChild)
                    backlink = dom.createElement("a")
                    backlink.setAttribute("href", "#%s" % fnbackid)
                    backlink.setAttribute("class", "simple-footnote-back")
                    backlink.appendChild(dom.createTextNode(u'\u21a9'))
                    li.appendChild(dom.createTextNode(" "))
                    li.appendChild(backlink)
                    ol.appendChild(li)
                    e.parentNode.removeChild(e)
                dom.getElementsByTagName("body")[0].appendChild(ol)
                dom_treewalker = html5lib.treewalkers.getTreeWalker("dom")
                output_generator = s.serialize(dom_treewalker(dom.getElementsByTagName("body")[0]))
                article._content = ("".join(list(output_generator))
                                    .replace("<x-simple-footnote>", "[ref]")
                                    .replace("</x-simple-footnote>", "[/ref]")
                                    .replace("<body>", "")
                                    .replace("</body>", ""))


def register():
    signals.article_generator_finalized.connect(parse_for_footnotes)
