def build_url(baseurl, path, args_dict):
    # Returns a list in the structure of urlparse.ParseResult
    url_parts = list(urlparse.urlparse(baseurl))
    url_parts[2] = path
    url_parts[4] = urllib.urlencode(args_dict)
    return urlparse.urlunparse(url_parts)