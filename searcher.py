import requests
from bs4 import BeautifulSoup

def get_webpage(url):
    requested_page = requests.get(url)
    return requested_page

def get_content(requested_page, html_class, html_tag):
    data_list = []
    page_content = BeautifulSoup(requested_page.content, 'html.parser') #gets the content of the whole requested page
    all_offers = page_content.find_all(class_=html_class) #finds all objects contained inside the given HTML class
    for offer in all_offers:           
        single_offer = offer.find_next(html_tag) #gets objects with the given html_tag
        offer_data = single_offer.string #gets the string containted inside the html tag
        if offer_data == None:            
            offer_data = single_offer.get('href') #gets the link to the object     
        data_list.append(offer_data)                      
    return data_list
    
def combining_data(urls):
    combined_data = []
    separeted_links = urls.split(',') #if multiple urls are given, separe links are created by splitting
    for url in separeted_links:
        requested_page = get_webpage(url)
        items_name = get_content(requested_page, 'marginright5 link linkWithHash detailsLink', 'strong')
        items_price = get_content(requested_page, 'wwnormal tright td-price', 'strong')
        items_place = get_content(requested_page, 'color-9 lheight16 marginbott5', 'span')
        items_date = get_content(requested_page, 'color-9 lheight16 marginbott5', 'p')
        items_link = get_content(requested_page, 'x-large lheight20 margintop5', 'a')
        for i in range(len(items_name)): 
            combined_data.extend(('<p>' '<strong>Name: </strong>'+items_name[i]+'<br>', '<strong>Price: </strong>'+items_price[i]+'<br>', '<strong>Place: </strong>'+items_place[i]+'<br>', 
                                  '<strong>Added: </strong>'+items_date[i]+'<br>', '<strong>Link: </strong>'+items_link[i]+'<br></p>'))
               
    return combined_data