import requests
import csv
from bs4 import BeautifulSoup


def centos_scraper(link):
    """
    Get a list of files inside a link
    :param link: CentOS link
    :return: A list of lists containing a file's name, download link, and size
    """
    csv_output = []
    response = requests.get(link).text
    html_parser = BeautifulSoup(response, 'html.parser')
    table_rows = html_parser.find_all('tr')
    table_rows = table_rows[3:-1]  # Cutout unneeded rows(ex. table header)

    for table_row in table_rows:
        file_name = table_row.a["href"]
        file_link = f'{link}{file_name}'

        if file_name.endswith('/'):  # Check if directory
            csv_output += centos_scraper(file_link)
        else:
            csv_output.append(get_csv_row(table_row, file_link))

    return csv_output


def get_csv_row(table_row, file_link):
    """
    Get a file's name, download link, and size
    :param table_row: A 'tr' tag object
    :param file_link: A file's download link
    :return: A dictionary whose pairs are 'filename':<filename>, 'download_link':<download link, and 'filesize':<size>
    """
    keys = ['filename', 'download_link', 'filesize']
    elements = table_row.find_all('td')
    csv_row = elements[1].a['href'], file_link, elements[3].text
    return dict(zip(keys, csv_row))


def create_csv_file(csv_output):
    """
    Create a csv file from a list of dictionaries
    :param csv_output: List of dictionaries
    :return: None
    """
    filename = 'csv_file.csv'
    with open(filename, "w+", newline='') as csv_file:
        writer = csv.DictWriter(csv_file, ["filename", "download_link", "filesize"], delimiter=',')
        writer.writeheader()
        writer.writerows(csv_output)


if __name__ == '__main__':
    create_csv_file(centos_scraper('http://mirror.rise.ph/centos/7/updates/x86_64/'))
