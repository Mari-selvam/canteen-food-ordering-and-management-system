import streamlit as st
import sqlite3
import matplotlib.pyplot as plt
import pandas as pd

connection = sqlite3.connect("canteen.db")
cursor = connection.cursor()
# import numpy as np

globuser= []
mybalance = 400

class HomePage:
    def __init__(self):
        pass
    
    def show(self):
        



# Apply the custom CSS


# Animated account creation form
        st.title("Create Your Account")
        with st.container():
            username = st.text_input("Username")
            email = st.text_input("Email")
            phone = st.text_input("Phone")
            RFID = st.text_input("RFID")
            password = st.text_input("Password", type="password")
            confirm_password = st.text_input("Confirm Password", type="password")
            
            if st.button("Create Account"):
                if password == confirm_password:
                    st.success("Account created successfully!")
                    
                    insert_query = f"INSERT INTO user (username, email,phone,RFID,password,balance) VALUES ('{username}', '{email}','{phone}','{RFID}','{password}',{0})"
                    cursor.execute(insert_query)
                    connection.commit()
                    connection.close()
                    
                    st.balloons()
                    
                    
                else:
                    st.error("Passwords do not match. Please try again.")



class home:
    def __init__(self):
        pass

    def show(self):
        st.title("Sign-In")
        email = st.text_input("Email")
        password = st.text_input('Password', type='password')
        if st.button("Sign In"):
            signin_query = f"SELECT * FROM user WHERE email = '{email}' AND password = '{password}'"
            cursor.execute(signin_query)
            user = cursor.fetchone()

            if user:
                st.success(f"Welcome, {user[0]}!")  # Assuming user name is in the second column of the 'user' table
                st.session_state.is_authenticated = True
                st.session_state.user_name = user[0]  # Assuming user name is in the second column of the 'user' table
                globuser = user
                
                
                st.title("Welcome , "+user[0])
                st.markdown('''
                    :rainbow[Welcome To The Canteen].''')
                

                multi = user[5]
                # st.markdown(f"Your balance : {str(balance)}")
                
                bal = st.number_input("Add money ")
                if st.button("ADD"):
                    mybalance = mybalance + bal
                    
                
                
            else:
                st.error("Invalid email or password. Please try again.")
        connection.close()


class menu:
    def __init__(self):
        pass
    
    def show(self):
        st.title("Food Menu")
        
        # Button to select a category
        category = st.radio("Select a category:", ("Veg", "Non-Veg", "Snacks", "Cool Drinks"))

        # Define food items and their prices for each category
        menu = {
            "Veg": {
                "Paneer Tikka": 30,
                "Veg Biryani": 60,
                "Aloo Paratha": 15,
                "Mushroom Curry": 40
            },
            "Non-Veg": {
                "Chicken Tikka": 50,
                "Chicken Biryani": 90,
                "Fish Curry": 60,
                "Butter Chicken": 70
            },
            "Snacks": {
                "French Fries": 30,
                "Onion Rings": 20,
                "Samosa": 20,
                "Pakora": 30
            },
            "Cool Drinks": {
                "Cola": 15,
                "Lemonade": 20,
                "Iced Tea": 30,
                "Orange Juice": 25
            }
        }

        # Display food items based on the selected category
        st.subheader(f"{category} Food Items:")
        items = list(menu[category].keys())
        select_all = st.checkbox("Select All")
        selected_items = st.multiselect("Select food items:", items if not select_all else items, default=items if select_all else [])

        # Define a dictionary to store counts of selected items
        item_counts = {}

        # Calculate and display the total cost
        total_cost = 0
        for item in selected_items:
            count = st.number_input(f"Quantity for {item}", value=1, min_value=1)
            item_counts[item] = count
            total_cost += count * menu[category][item]

        st.write(f"Total Cost: Rs {total_cost:2}")
        
        
        
        
        st.title(f"your Balance : {mybalance - total_cost} ")
        

class data:
    def __init__(self):
        pass
    
    def show(self):
        st.title("this Month data : ")
        # Parse data into a DataFrame
        df = pd.read_csv('data.csv')

        # Streamlit app
        st.title('Canteen Daily Sales Data')

        # Plot the bar chart
        st.bar_chart(df.set_index('Date')['Total_Sales'])

# Function to run the app
def main():
    st.sidebar.title("Canteen : ")
    pages = {
        "Home":home,
        "Create Account": HomePage,
        "Menu": menu,
        "Data": data,

    }
    
    selection = st.sidebar.radio("Go to", list(pages.keys()))
    page = pages[selection]()
    page.show()
    
if not hasattr(st.session_state, "is_authenticated"):
    st.session_state.is_authenticated = False


if __name__ == "__main__":
    main()
