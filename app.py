import streamlit as st
import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent
import matplotlib.pyplot as plt
import seaborn as sns

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
    # Write the scraped HTML to a file
    with open("scraped_data.txt", "w", encoding="utf-8") as file:
        file.write(str(soup))
    
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
        links = amazon_html.select('a.a-link-normal.s-underline-text.s-underline-link-text.s-link-style.a-text-normal')
        for link in links:
            href  = link['href']
            full_link = search_url + href
            data['Link'].append(full_link)
            if len(data["Link"]) == len(data["Title"]):
                break
    
    # Check if all lists have the same length after appending values
    data_lengths = [len(data[key]) for key in data]
    max_length = max(data_lengths)

    # Ensure all lists have the same length
    for key in data:
        while len(data[key]) < max_length:
            data[key].append('N/A')  # Append a default value

            
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
            href = link['href']
            full_link = search_url + href
            data['Link'].append(full_link)
            if len(data["Link"]) == len(data["Title"]):
                break
    
    # Check if all lists have the same length after appending values
    data_lengths = [len(data[key]) for key in data]
    max_length = max(data_lengths)

    # Ensure all lists have the same length
    for key in data:
        while len(data[key]) < max_length:
            data[key].append('N/A')  # Append a default value

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

    # Check if all lists have the same length after appending values
    data_lengths = [len(data[key]) for key in data]
    max_length = max(data_lengths)

    # Ensure all lists have the same length
    for key in data:
        while len(data[key]) < max_length:
            data[key].append('N/A')  # Append a default value


    df = pd.DataFrame.from_dict(data)
    return df

def display_logo(logo_path):
    col1, col2, col3 = st.columns([2, 1, 2])
    with col2:
        st.image(logo_path, width=200)

def data_scraping_section():
    st.header("Data Scraping")
    st.subheader("Product Information Retrieval")

    # Input Product Name
    product = st.text_input("Enter the product name:", st.session_state.get("product", ""))

    # Input Parameters
    parameters = st.multiselect('Choose Parameters', ['Price', 'M.R.P', 'Ratings', 'Link'], st.session_state.get("parameters", []))

    st.write("Selected Parameters:")
    for param in parameters:
        st.write("- " + param)

    # Scraping
    if st.button("Scrape"):
        if product and parameters:
            st.session_state.product = product
            st.session_state.parameters = parameters

            df_amazon = scrape_amazon(product, parameters)
            st.dataframe(df_amazon)
            df_amazon.reset_index(drop=True, inplace=True)  #Satrting index from number 1
            df_amazon.to_csv("data_amazon.csv", index=False)

            df_flipkart = scrape_flipkart(product, parameters)
            st.dataframe(df_flipkart)
            df_flipkart.reset_index(drop=True, inplace=True)  #Starting index from number 1
            df_flipkart.to_csv("data_flipkart.csv", index=False)

            # Enable access to other sections and save CSV paths to session state
            st.session_state.data_scraped = True
            st.session_state.amazon_csv_path = "data_amazon.csv"
            st.session_state.flipkart_csv_path = "data_flipkart.csv"

            # Save the DataFrames to session state
            st.session_state.df_amazon = df_amazon
            st.session_state.df_flipkart = df_flipkart

        else:
            st.warning("Please enter a product name and also choose the parameters for scraping")

def data_visualization_section():
    if 'data_scraped' not in st.session_state:
        st.warning("Please perform data scraping first.")
    else:
    # if True:

        #Load CSV files
        df_amazon = pd.read_csv(st.session_state.amazon_csv_path)
        df_flipkart = pd.read_csv(st.session_state.flipkart_csv_path)
    
        # Load CSV files for already scraped Amazon and Flipkart
        # df_amazon = pd.read_csv("data_amazon.csv")
        # df_flipkart = pd.read_csv("data_flipkart.csv")

        # Starting the csv from index 1
        df_amazon.index = range(1, len(df_amazon) + 1)
        df_flipkart.index = range(1, len(df_flipkart) + 1)

        # Display the data from CSV files
        st.subheader("Amazon Data:")
        st.write(df_amazon)

        st.subheader("Flipkart Data:")
        st.write(df_flipkart)

        # Convert Price and MRP columns to numeric (remove ₹ sign) and comma
        df_amazon['Price'] = df_amazon['Price'].replace({'₹': ''}, regex=True).str.replace(',', '').astype(float)
        df_amazon['M.R.P'] = df_amazon['M.R.P'].replace({'₹': ''}, regex=True).str.replace(',', '').astype(float)
        df_flipkart['Price'] = df_flipkart['Price'].replace({'₹': ''}, regex=True).str.replace(',', '').astype(float)
        df_flipkart['M.R.P'] = df_flipkart['M.R.P'].replace({'₹': ''}, regex=True).str.replace(',', '').astype(float)

        # First Graph: Price Vs MRP
        st.subheader("Price vs M.R.P")
        fig_price_mrp = plt.figure(figsize=(10, 5))
        sns.scatterplot(data=df_amazon, x='Price', y='M.R.P', label='Amazon')
        sns.scatterplot(data=df_flipkart, x='Price', y='M.R.P', label='Flipkart')
        plt.title('Price vs M.R.P')
        plt.xlabel('Price (in ₹)')
        plt.ylabel('M.R.P (in ₹)')
        plt.legend()
        st.pyplot(fig_price_mrp)

        # Second Graph: Highest Price and Lowest Price
        # 1) Amazon
        st.subheader("Price Range Distribution for Amazon")
        fig_amazon_price_range = plt.figure(figsize=(9, 6))
        highest_lowest_prices = pd.concat([df_amazon[['Price', 'Title']]], axis=0)
        highest_lowest_prices = highest_lowest_prices.groupby('Title')['Price'].agg(['min', 'max'])
        highest_lowest_prices = highest_lowest_prices.reset_index()
        max_price = highest_lowest_prices['max'].max()
        bins = range(0, int(max_price) + 10000, 5000)  # Adjust bin sizes dynamically
        highest_lowest_prices['Price Range'] = pd.cut(highest_lowest_prices['min'], bins=bins, right=False)
        price_range_counts_amazon = highest_lowest_prices['Price Range'].value_counts()
        sns.countplot(data=highest_lowest_prices, y='Price Range', order=price_range_counts_amazon[price_range_counts_amazon > 0].index)
        plt.title('Price Range Distribution for Amazon')
        plt.xlabel('Count')
        plt.ylabel('Price Range (in ₹)')
        st.pyplot(fig_amazon_price_range)

        # 2) Flipkart
        st.subheader("Price Range Distribution for Flipkart")
        fig_flipkart_price_range = plt.figure(figsize=(9, 6))
        highest_lowest_prices = pd.concat([df_flipkart[['Price', 'Title']]], axis=0)
        highest_lowest_prices = highest_lowest_prices.groupby('Title')['Price'].agg(['min', 'max'])
        highest_lowest_prices = highest_lowest_prices.reset_index()
        max_price = highest_lowest_prices['max'].max()
        bins = range(0, int(max_price) + 10000, 5000)  # Adjust bin sizes dynamically
        highest_lowest_prices['Price Range'] = pd.cut(highest_lowest_prices['min'], bins=bins, right=False)
        price_range_counts_flipkart = highest_lowest_prices['Price Range'].value_counts()
        sns.countplot(data=highest_lowest_prices, y='Price Range', order=price_range_counts_flipkart[price_range_counts_flipkart > 0].index)
        plt.title('Price Range Distribution for Flipkart')
        plt.xlabel('Count')
        plt.ylabel('Price Range (in ₹)')
        st.pyplot(fig_flipkart_price_range)

def data_modeling_section():
    if 'data_scraped' not in st.session_state:
        st.warning("Please perform data scraping first.")
    else:
        st.header("Data Modeling")

        # Load CSV files
        df_amazon = pd.read_csv(st.session_state.amazon_csv_path)
        df_flipkart = pd.read_csv(st.session_state.flipkart_csv_path)

        # Your data modeling code goes here

def main():
    st.set_page_config(layout="wide")
    
    # Displaying logo and center aligning the logo
    display_logo("coep-logo.jpg")

    # Header and subheader
    st.title("E-commerce Product Analysis")
    st.markdown(
        """
        <div style='margin-bottom: 40px;'>
            <p style='font-size: 18px; color: #666;'>A Platform to analyze Features, Prices, and Reviews Across E-commerce Websites</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Sidebar menu
    menu_options = ["Data Scraping", "Data Visualization", "Data Modeling"]

    # Display menu options vertically
    for option in menu_options:
        st.sidebar.write(option)
    
    menu_selection = st.sidebar.selectbox("", menu_options)

    # Main content based on menu selection
    if menu_selection == "Data Scraping":
        data_scraping_section()
    elif menu_selection == "Data Visualization":
        st.header("Data Visualization")
        data_visualization_section()
    elif menu_selection == "Data Modeling":
        st.header("Data Modeling")
        data_modeling_section()

if __name__ == "__main__":
    main()