import streamlit as st
import streamlit_authenticator as stauth
from dependencies import fetch_users

try:
    # Fetch users from Firestore
    users = fetch_users()
    emails = []
    usernames = []
    passwords = []

    # Append the users' data, assuming they are already hashed
    for user in users:
        emails.append(user.get('email', ''))  
        usernames.append(user.get('username', ''))
        passwords.append(user.get('password', ''))  # Assuming these are already hashed passwords

    # Prepare credentials for streamlit_authenticator
    credentials = {'usernames': {}}
    for index in range(len(emails)):
        credentials['usernames'][usernames[index]] = {'name': emails[index], 'password': passwords[index]}  # store the hashed password here

    # Initialize the Streamlit Authenticator
    Authenticator = stauth.Authenticate(credentials, cookie_name='YOUR_PREFERRED_COOKIE_NAME', key='abcdef', cookie_expiry_days=2)

    # Get login status
    email, authentication_status, username = Authenticator.login(':grey[Login]', 'main')
    
    # Define layout for login messages
    info, info1 = st.columns(2)

    #if not authentication_status:
     #   sign_up()

    if username:
        if username in usernames:
            if authentication_status:
                
                #let User see app
                Authenticator.logout('Log Out', 'sidebar')
                
                # Insert company logo    
                logo = "TRR241_logo.jpg"
                st.image(logo, width=200)

                # Display the title
                st.title(":gray[YOUR_WEBPAGE_HEADER]") 
                
                # contact in case of issues 
                st.markdown("###### :gray[for issues contact: Jay V. Patankar]", unsafe_allow_html=True)

                #Sub-subheading 1
                st.markdown("### :gray[Interactive scatter plot]", unsafe_allow_html=True)

                # page refresh reminder
                st.markdown("###### :gray[Refresh the page if the graphics don't load!]", unsafe_allow_html=True)

                # Tableau Embed Code with CSS modifications
                tableau_embed_code = """
                    <style>
                        /* Adjust the size of the embedded element */
                        iframe {
                            width: 80%;
                            height: 830px; /* Adjust the height as needed */
                        }
                        
                        /* Change the font family and size */
                        body, p, span {
                            font-family: 'Bahnschrift Light', sans-serif; /* Use Bahnschrift Light font */
                            font-size: 16px; /* Adjust the font size as needed */
                        }
                    </style>
                    <iframe src='EMBED_YOUR_TABLEAU_PUBLIC_DASHBOARD_HERE:embed=true'></iframe>
                    """
                # Display the embedded Tableau visualization
                st.components.v1.html(tableau_embed_code, height=900)  # Adjust the height as needed
                                                     
            elif not authentication_status:
                with info:
                    st.error('Incorrect Password or username')
            else:
                with info:
                    st.warning('Please feed in your credentials')
        else:
            with info:
                st.warning('Username does not exist, Please Sign up')

except Exception as e:
    st.success(f"An error occurred, please contact Jay Patankar: {e}")