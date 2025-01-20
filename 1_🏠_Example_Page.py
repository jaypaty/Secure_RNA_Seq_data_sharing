import streamlit as st
import streamlit_authenticator as stauth

# Set page configuration FIRST
st.set_page_config(page_title='TITLE_OF_YOUR_WEBPAGE', page_icon='🐭', initial_sidebar_state='auto', layout="wide")

from dependencies import fetch_users, sign_up

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
    authenticator = stauth.Authenticate(credentials, cookie_name='YOUR_PREFERRED_COOKIE_NAME', key='abcdef', cookie_expiry_days=2)

    # Get login status
    email, authentication_status, username = authenticator.login(':grey[Login]', 'main')

    # Define layout for login messages
    info, _ = st.columns(2)

    if authentication_status:
        # If authenticated, show the app content and the logout button
        authenticator.logout('Log Out', 'sidebar')

        def main():
            # Insert company logo    
            logo = "TRR241_logo.jpg"
            st.image(logo, width=250)

            st.title(":gray[YOUR_WEBPAGE_HEADER]")
            
            st.markdown("###### :gray[for issues contact: Jay V. Patankar]", unsafe_allow_html=True)
            st.subheader(":gray[Cytokine-stimulated organoids generated from mouse small intestinal crypts]", divider="grey")
            
            st.markdown("##### :gray[Each colored ring represents significantly regulated genes upon treatment with a specific cytokine]", unsafe_allow_html=True)
            st.markdown("##### :gray[Each bubble represents the log2 fold change of a given gene. Note that the up and down are scaled independently!]", unsafe_allow_html=True)
            st.markdown("##### :gray[The 'highlight genes' search uses a wildcard query. Try 'Casp' and press the return / enter key]", unsafe_allow_html=True)
            st.markdown("###### :gray[Refresh the page if the graphics don't load!]", unsafe_allow_html=True)

            tableau_embed_code = """
            <style>
                iframe {
                    width: 100%;
                    height: 800px;
                }
                body, p, span {
                    font-family: 'Bahnschrift Light', sans-serif;
                    font-size: 16px;
                }
            </style>
            <iframe src='EMBED_YOUR_TABLEAU_PUBLIC_DASHBOARD_HERE:embed=true'></iframe>
            """
            st.components.v1.html(tableau_embed_code, height=900)

        if __name__ == "__main__":
            main()

    elif authentication_status is False:
        # If authentication fails
        with info:
            st.error('Incorrect Password or Username')
            # Call the sign-up form
            sign_up()
        
    elif authentication_status is None:
        # If no credentials are provided
        with info:
            st.warning('Please enter your credentials')
        

except Exception as e:
    st.error(f"An error occurred, please contact Jay Patankar: {e}")
