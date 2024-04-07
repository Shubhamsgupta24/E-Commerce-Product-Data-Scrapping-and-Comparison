import streamlit as st
import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent

def SearchURL(product,base_url):
    if base_url == "https://www.amazon.in" :
        return f"{base_url}/s?k={product.replace(' ', '+')}"
    elif base_url == "https://www.croma.com" :
        return f"{base_url}/searchB?q={product}%3Arelevance&text={product}"
    elif base_url == "https://www.flipkart.com":
        return f"{base_url}/search?q={product.replace(' ', '%20')}"
    else:
        st.error("The browser url could not be fetched")
        return None

def ScrapeHTML(url):
    # Using selenium
    DRIVER_PATH = r"/home/sgubuntu/Projects/Website_Differer/chromedriver-linux64/chromedriver"

    # Initialize Chrome WebDriver options
    chrome_options = Options()
    chrome_options.binary_location = "/usr/bin/google-chrome-stable"

    # Set Chrome WebDriver executable path
    chrome_options.add_argument("webdriver.chrome.driver=" + DRIVER_PATH)

    # Set Chrome WebDriver to run in headless mode if you do not want the popup
    # chrome_options.add_argument("--headless")

    # Exclude the "enable-automation" switch to prevent WebDriver detection
    chrome_options.add_experimental_option("excludeSwitches", ['enable-automation'])

    # Initialize the Chrome WebDriver with the specified options
    driver = webdriver.Chrome(options=chrome_options)

    # Open the URL
    driver.get(url)
    
    # Get the page source
    page_source = driver.page_source

    # Create a BeautifulSoup object to parse the page source
    soup = BeautifulSoup(page_source, 'html.parser')

    # Close the WebDriver to release resources
    driver.quit()   

    if soup is None:
        st.error(f"Failed to load the page at {url}")
        return None
    
    #Testing
    # paragraphs = soup.find_all('p')
    # for p in paragraphs:
    #     st.write(p.get_text())
    
    return soup

def useragent_html(url):
    ua = UserAgent()
    user_agent = user_agent = f"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.6312.105 Safari/537.36"
    headers = {'User-Agent': user_agent}

    req = requests.get(url,headers=headers)
    content = BeautifulSoup(req.text,'html.parser')
    print(content)

    return content

def DataFrameInitialization(parameters):
    data = {'Title': []}

    for param in parameters:
        data[param] = []
    # st.write(data)
    return data

def scrape_amazon(product,parameters):
    amazon_url = "https://www.amazon.in"
    search_url = SearchURL(product,amazon_url)

    amazon_html = ScrapeHTML(search_url)

    #Initialising DataFrame
    data = DataFrameInitialization(parameters)

    #Scrapping necessary and relevant information

    #1)Product Title
    titles = amazon_html.select("span.a-size-medium.a-color-base.a-text-normal")  #Title has some issue with the companys name
    for title in titles:
        data["Title"].append(title.string)

    #2)Price
    if 'Price' in data:
        prices = amazon_html.select("span.a-price")
        for price in prices:
            if not ("a-text-price" in price.get("class")):
                data['Price'].append(price.find("span").get_text())
            if len(data["Price"]) == len(data["Title"]):
                break

    #3)M.R.P.
    if 'M.R.P' in data:
        Mrps = amazon_html.select("span.a-price.a-text-price")
        for mrp in Mrps:
            data['M.R.P'].append(mrp.find("span").get_text())
            if len(data["M.R.P"]) == len(data["Title"]):
                break
            
    #4)Ratings
    if 'Ratings' in data:
        ratings = amazon_html.select('.a-row.a-size-small')
        for rating in ratings:
            data['Ratings'].append(rating.find("span").get_text())
            if len(data["Ratings"]) == len(data["Title"]):
                break

    #5)Link
    if 'Link' in data:
        links = amazon_html.select('h2.a-size-mini.a-spacing-none.a-color-base.s-line-clamp-2 > a')
        for link in links:
            data['Link'].append(link['href'])
            if len(data["Link"]) == len(data["Title"]):
                break
            
    df = pd.DataFrame.from_dict(data)
    return df

def scrape_flipkart(product,parameters):
    flipkart_url = "https://www.flipkart.com"
    search_url = SearchURL(product,flipkart_url)

    flipkart_html = ScrapeHTML(search_url)

    #Initialising DataFrame
    data = DataFrameInitialization(parameters)

    #Scrapping necessary and relevant information

    # 1) Product Title
    titles = flipkart_html.select("div._4rR01T")
    for title in titles:
        data["Title"].append(title.get_text())  

    # 2) Price
    if 'Price' in data:
        prices = flipkart_html.select("div._30jeq3")
        for price in prices:
            data['Price'].append(price.get_text())
            if len(data["Price"]) == len(data["Title"]):
                break
    # 3) M.R.P.
    if 'M.R.P' in data:
        mrps = flipkart_html.select("div._3I9_wc") 
        for mrp in mrps:
            data['M.R.P'].append(mrp.get_text())  
            if len(data["M.R.P"]) == len(data["Title"]):
                break

    # 4) Ratings
    if 'Ratings' in data:
        ratings = flipkart_html.select('div._3LWZlK') 
        for rating in ratings:
            data['Ratings'].append(rating.get_text())  
            if len(data["Ratings"]) == len(data["Title"]):
                break

    # 5) Link
    if 'Link' in data:
        links = flipkart_html.select('a._1fQZEK')
        for link in links:
            data['Link'].append(link['href'])
            if len(data["Link"]) == len(data["Title"]):
                break

    df = pd.DataFrame.from_dict(data)
    return df


def scrape_croma(product,parameters):
    croma_url = "https://www.croma.com"
    # search_url = SearchURL(product,croma_url)
    search_url = "https://www.croma.com/searchB?q=iphone%3Arelevance&text=iphone"

    croma_html = ScrapeHTML(search_url)
    # croma_html = useragent_html(search_url)

    #Initialising DataFrame
    data = DataFrameInitialization(parameters)

    #Scrapping necessary and relevant information

    #1)Product Title
    titles = croma_html.find_all("h3", class_="product-title plp-prod-title 999")
    for title in titles:
        data["Title"].append(title.find("a").get_text())


    #2)Price
    if 'Price' in data:
        prices = croma_html.select("span.amount.plp-srp-new-amount")
        for price in prices:
            data["Price"].append(price.string)
            if len(data["Price"]) == len(data["Title"]):
                break

    #3)M.R.P.
    if 'M.R.P' in data:
        Mrps = croma_html.select("span.amount")
        for mrp in Mrps:
            if not ("plp-srp-new-amount" in mrp.get("class")):
                data['M.R.P'].append(mrp.string)
            if len(data["M.R.P"]) == len(data["Title"]):
                break
            
    #4)Ratings
    if 'Ratings' in data:
        ratings = croma_html.select('span.rating-text')
        for rating in ratings:
            data['Ratings'].append(rating.string)
            if len(data["Ratings"]) == len(data["Title"]):
                break

    #5)Link
    if 'Links' in data:
        links = croma_html.select('h3.product-title.plp-prod-title.999 > a')
        for link in links:
            data['Link'].append(link['href'])
            if len(data["Link"]) == len(data["Title"]):
                break

    df = pd.DataFrame.from_dict(data)
    return df

def display_logo(logo_path):
    col1, col2, col3 = st.columns([2, 1, 2])
    with col2:
        st.image(logo_path, width=200)

def main():
    st.set_page_config(layout="wide")
    
    # Displaying logo and center aligning the logo
    display_logo("coep-logo.jpg")

    #Header and subheader
    st.title("E-commerce Product Analysis")
    st.markdown(
        """
        <div style='margin-bottom: 40px;'>
            <p style='font-size: 18px; color: #666;'>A Platform to analyze Features, Prices, and Reviews Across E-commerce Websites</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    #Input Product Name
    product = st.text_input("Enter the product name:", "")

    #Input Parameters
    parameters = st.multiselect('Choose Parameters',['Price','M.R.P','Ratings','Link'])
    st.write("Selected Parameters:")
    for param in parameters:
        st.write("- " + param)
    
    #Scraping
    if st.button("Scrape"):
        if product and parameters:
            # df_amazon = scrape_amazon(product,parameters)
            df_flipkart = scrape_flipkart(product,parameters)
            st.dataframe(df_flipkart)
            df_flipkart.to_csv("data_flipkart.csv", index=False)
        else:
            st.warning("Please enter a product name and also choose the parameters for scraping")

if __name__ == "__main__":
    main()
