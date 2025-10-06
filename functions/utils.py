import re

def minify_string(text):
    text = re.sub(r'\s+', ' ', text).strip()
    text = text.replace('\n', ' ').replace('\r', '')
    return text
