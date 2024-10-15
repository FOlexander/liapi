def get_id(url):
    print(url.split("/")[-2])
    return url.split("/")[-2]


if __name__ == '__main__':
    get_id('https://www.linkedin.com/in/oleksandr-les-8137a7ab/')