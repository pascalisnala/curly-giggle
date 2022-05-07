import asyncio

list_item = []


def tag_from_type(text, type, color=None):
    if type == "heading_1":
        return f"""
    <h2>{text}</h2>
    """

    elif type == "heading_2":
        return f"""
    <h3>{text}</h3>
    """

    elif type == "heading_3":
        return f"""
    <h4>{text}</h4>
    """

    elif type == "paragraph":
        return f"""
    <p>{text}</p>
    """

    elif type == "code":
        return f"""
    <pre class="prettyprint">{text}</pre>
    """

    elif type == "bulleted_list_item":
        list_item.append(
            f"""
      <li> {text} </li>
      """
        )
        return ""

    elif type == "quote":
        return f"""
        <blockquote style="margin-left: .3em;">
            <p>{text}</p>
        </blockquote>
        """

    elif type == "callout":
        return f"""
        <div class="callout">
            <span class="callout-text">{text}</span>
        </div>
        """

    elif type == "toggle":
        return f"""
        <button class="toggle"><span class="toggle-title">{text}<span></button>
        """

    else:
        return ""


def hyperlink(text, url):
    return f"""
  <a href={url}>{text}</a>
  """


def toggle(title, content):
    pass


def tag_from_annotations(text, annots):
    out = text
    if annots["bold"]:
        out = f"""<b>{out}</b>"""

    if annots["italic"]:
        out = f"""<i>{out}</i>"""

    if annots["strikethrough"]:
        out = f"""<strike>{out}</strike>"""

    if annots["underline"]:
        out = f"""<u>{out}</u>"""

    if annots["code"]:
        out = f"""<code>{out}</code>"""

    return out


def show_image(url, alt, hyperlink=None):
    return f"""
    <img class="center" src={url} alt={alt}>
    <p style="color: grey; text-align:center; margin-top:0em; font-size:smaller; ">{alt}</p>
    """


def show_equation(expression):
    return f"<p>\[{expression}\]</p"


async def insert_toggle_content(toggle_content):
    return f"""
    <div class="toggle-content">
    {toggle_content}
    </div>
    """


def wrap_list():
    return f"""
    <ul style="margin-top:0em;">
        {" ".join(list_item)}
    </ul>
    """


async def article_content(block):
    global list_item
    out = ""

    type = block["type"]
    if list_item and type != "bulleted_list_item":
        out += wrap_list()
        list_item = []
    html_text = ""
    loc = "caption" if type == "image" else "text"

    if type == "image":
        image_type = block[type]["type"]
        url = block[type][image_type]["url"]
        try:
            alt = block[type][loc][0]["plain_text"]
        except:
            alt = ""
        out += show_image(url, alt)
    elif type == "toggle":
        for item in block[type][loc]:
            text = item["plain_text"]
            if item["href"]:
                text = hyperlink(text, item["href"])
            text = tag_from_annotations(text, item["annotations"])
            html_text += text
        id = block["id"]
        # print(get_article_content(id, HEADERS))

        out += tag_from_type(html_text, type)
    elif type == "equation":
        expression = block[type]["expression"]
        out += show_equation(expression)
    else:
        for item in block[type][loc]:
            text = (
                f"\({item['plain_text']}\)"
                if item["type"] == "equation"
                else item["plain_text"]
            )
            if item["href"]:
                text = hyperlink(text, item["href"])
            text = tag_from_annotations(text, item["annotations"])
            html_text += text

        out += tag_from_type(html_text, type)

    return out


def article_title(metadata):
    out = ""
    if metadata["cover_url"] != None:
        cover = f"""
        <img class="article-cover" src={metadata['cover_url']}>
        """
    else:
        cover = ""
    title = f"""
  <h1 style=text-align:left;>{metadata['title']}</h1>
  """
    subtitle = f"""
  <b>{metadata['author']}</b> &emsp; <span style="font-size:smaller; color:darkslategray;"><i class="far fa-calendar"></i> {metadata['created_time']}</span> <br>
  """
    tags = f"""
  <i style='font-size: smaller;'><i class="fas fa-tag"></i> {', '.join(metadata['tags'])}</i>
  """
    return cover, out + title + subtitle + tags
