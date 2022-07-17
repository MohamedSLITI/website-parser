from middleware import *
import time

website = 'https://www.goremedical.com/eu/'
data = []


def main():
    start = time.time()
    pages = urls(website)
    driver = setup(website)
    count = 1
    for page in pages:
        name = f'output/{count}'
        count += 1
        screenshot(driver, page, name)
        image_to_pdf(name)

    end = time.time()
    print("time : === > ", end - start)


if __name__ == "__main__":
    main()
