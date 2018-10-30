def validate_url(url):  # https://de.wikipedia.org/wiki/Lauch
    split_url = url.split(":")
    print(split_url)

    return split_url[0] == "https" or split_url[0] == "http"

print(validate_url("http://de.wikipedia.org/wiki/Lauch"))
