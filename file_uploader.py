import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
import pandas as pd
import streamlit as st
import hashlib  # For password hashing
from datetime import datetime


users = {
    "admin": hashlib.sha256("password".encode()).hexdigest()
}

def is_authenticated(username, password):
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    if username in users and users[username] == hashed_password:
        return True
    return False

def main():
    # st.set_page_config(page_title="File Uploader")
    logged_in = st.session_state.get("logged_in", False)
    username = st.session_state.get("username", None)

    if not logged_in:
        # Render the login form
        st.title("Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        login_button = st.button("Login")

        if login_button:
            # Check if the username and password are correct
            if is_authenticated(username, password):
                st.session_state["logged_in"] = True
                st.session_state["username"] = username
                st.experimental_rerun()
            else:
                st.error("Invalid username or password")
    else:


        # Create a file uploader widget
        st.title(f"Welcome, {username}!")
        # st.set_page_config(page_title='Calendar Example')

        # Add a header

        # Add a date input widget
        selected_date = st.date_input(
            "Select a date",
            datetime.now().date())

        # Display the selected date
        st.write('Selected date:', selected_date)
        selected_month = selected_date.strftime('%B')
        selected_year = selected_date.year
        cost_month= str(str(selected_month[:3])+" "+str(selected_year))

        uploaded_file = st.file_uploader("streamlit run file_uploader.py --server.enableXsrfProtection=falseChoose a file", type=["csv", "txt", "pdf","xlsx"])


        
        # Check if a file was uploaded
        if uploaded_file is not None:
            # Get the file details
            file_details = {
                "filename": uploaded_file.name,
                "filetype": uploaded_file.type,
                "filesize": uploaded_file.size
            }
            df_ = pd.read_excel(uploaded_file)
            df_ = df_.dropna(subset=['Employee Name'])
            columns=['Journal Date','Journal Number Prefix','Journal Number Suffix','Notes','Currency','Account','Description','Contact Name','Debit','Credit','Employee ID', "Quantity","Cost Month"]
            zoho = pd.DataFrame(columns=columns)

            dummy = ["Employee Number","Employee Name","Basic & DA",
            "HRA",
            "Special Allowance",
            "LTA",
            "Laptop Reimbursements",
            "other",
            "Working days",
            "PF - Employer",
            "ESI Employer",
            "Employee Gratuity contribution",
            "PF Employee",
            "ESI Employee",
            "Professional Tax",
            "Total Income Tax",
            
            "Other Deduction",
            "Cash Advance(E)",
            "Settlement Aganist Advance(F)",
            "Others",
            "Food expenses",
            "Travelling",
            "Courier Charges",
            "Laptop Reimburesement",
            "Total Net Pay(D+E+F+G)",
            "Cost Center"]
            filter_ = pd.DataFrame(columns=dummy)

            common_columns = list(set(df_.columns) & set(filter_.columns))

            df = df_[common_columns]

            Debit ={'Salaries and Employee Wages - Direct':['Basic & DA','HRA','Special Allowance','LTA', 'Laptop Reimbursements','PF - Employer','ESI Employer','Employee Gratuity contribution'], 'Employee Advance':['Cash Advance'],'Other Expenses':['Others','Courier Charges'],'Food expenses':'Food expenses','Travel & Accommodation Expense':'Travelling', 'Laptop Reimbursement':'Laptop Reimburesement', }
            Credit ={'Salaries and Employee Wages - Direct':"Other Deduction",'PF Payable':['PF - Employer','PF Employee'],'ESIC Payable':['ESI Employer','ESI Employee'],'Gratuity Payable':'Employee Gratuity contribution','TDS Payable':'Total Income Tax','Professional Tax Payable':'Professional Tax' ,'Employee Advance':['Settlement Against Advance'],'Salary Payable':'Total Net Pay(D+E+F+G)'}


            paygroup=''
            employeeNumber=0
            
            referenceNumber=0

            for index, row in df.iterrows():
                # payGroup = row['Pay Group']
                PL={'Salaries and Employee Wages - Direct':[0,0],'Other Expenses':0,'Food Expenses':0,'Travel & Accommodation Expense':0,'Laptop Reimburesement':0}
                BS={'PF Payable':0,'ESIC Payable':0,'Gratuity Payable':0,'TDS Payable':0,'Salary Payable':0,'TDS Payable':0,'Professional Tax Payable':0,'Employee Advance':0}

                # if index == 0:
                employeeNumber=employeeNumber+1
                
                quantity = row['Working days']
                for i in range (0,len(row.index)):

                    

                    value_to_find = row.index[i]
                    # Debit Items
                    keys =[key for key,value in Debit.items() if value_to_find in value]

                    # for key,value in Debit.items():


                    if len(keys) >0:

                    # new_row={'Journal Date':selected_date,'Reference Number':'Ref123','Journal Number Prefix':'JN','Journal Number Suffix':'0023','Notes':"Testing",'Currency':'USD','Account':keys[0],'Description':'None','Contact Name':payGroup,'Debit':row[value_to_find],'Credit':0,'Project Name':payGroup}
                    # zoho.loc[len(zoho)] = new_row

                        for j in PL:
                            if keys[0]==j:


                                if keys[0]=="Salaries and Employee Wages - Direct":
                                    PL[j][0]+=row[value_to_find]
                                    continue

                                PL[j]+=row[value_to_find]



                        for k in BS:
                            if keys[0]==k:
                                BS[k]+=row[value_to_find]



                    keys=[]
                    keys =[key for key,value in Credit.items() if value_to_find in value]

                    if len(keys) >0:


                        for j in PL:
                            if keys[0]==j:

                                if keys[0]=="Salaries and Employee Wages - Direct":
                                    PL[j][1]+=row[value_to_find]
                                    continue

                                PL[j]+=row[value_to_find]
                    # if keys[0]  in PL:
                    #   PL[keys[0] ]+=row[value_to_find]



                        for k in BS:
                            if keys[0]==k:
                                BS[k]+=row[value_to_find]


                    # if keys[0]  in BS:
                    #   BS[keys[0] ]+=row[value_to_find]

                    keys=[]
                employee = str(row['Employee Number'])+"  "+row['Employee Name'] # Two spaces
                for i in PL:
                    referenceNumber=referenceNumber+1

                    if i == "Salaries and Employee Wages - Direct":
                        new_row={'Journal Date':selected_date,'Journal Number Prefix':'JN','Journal Number Suffix':employeeNumber,'Notes':f'Salary - {selected_month[:3]} 24','Currency':'INR','Account':i,'Description':row["Cost Center"],'Contact Name':"",'Debit':PL[i][0],'Credit':0,'Employee ID':employee,'Quantity':quantity, "Cost Month":cost_month}
                        zoho.loc[len(zoho)] = new_row
                        if PL[i][1] != 0:
                            new_row={'Journal Date':selected_date,'Journal Number Prefix':'JN','Journal Number Suffix':employeeNumber,'Notes':f'Salary - {selected_month[:3]} 24','Currency':'INR','Account':i,'Description':row["Cost Center"],'Contact Name':"",'Debit':0,'Credit':PL[i][1],'Employee ID':employee,'Quantity':quantity,"Cost Month":cost_month}
                            zoho.loc[len(zoho)] = new_row

                        continue

                    if i in Credit:
                        new_row={'Journal Date':selected_date,'Journal Number Prefix':'JN','Journal Number Suffix':employeeNumber,'Notes':f'Salary - {selected_month[:3]} 24','Currency':'INR','Account':i,'Description':row["Cost Center"],'Contact Name':"",'Debit':0,'Credit':PL[i],'Employee ID':employee,'Quantity':quantity,"Cost Month":cost_month}
                        zoho.loc[len(zoho)] = new_row
                    else:
                        new_row={'Journal Date':selected_date,'Journal Number Prefix':'JN','Journal Number Suffix':employeeNumber,'Notes':f'Salary - {selected_month[:3]} 24','Currency':'INR','Account':i,'Description':row["Cost Center"],'Contact Name':"",'Debit':PL[i],'Credit':0,'Employee ID':employee,'Quantity':quantity,"Cost Month":cost_month}
                        zoho.loc[len(zoho)] = new_row

# 'Project Name':row["Cost Center"]
# 'Project Name':row["Cost Center"]
# 'Project Name':row["Cost Center"]
# 'Project Name':row["Cost Center"]
# 'Reference Number':f'Ref{referenceNumber}'
# 'Reference Number':f'Ref{referenceNumber}'
# 'Reference Number':f'Ref{referenceNumber}'
# 'Reference Number':f'Ref{referenceNumber}'
# 'Reference Number':f'Ref{referenceNumber}'
# 'Reference Number':f'Ref{referenceNumber}'

                for i in BS:
                    referenceNumber=referenceNumber+1

                    if i in Credit:
                        new_row={'Journal Date':selected_date,'Journal Number Prefix':'JN','Journal Number Suffix':employeeNumber,'Notes':f'Salary - {selected_month[:3]} 24','Currency':'INR','Account':i,'Description':row["Cost Center"],'Contact Name':"",'Debit':0,'Credit':BS[i],'Employee ID':employee,'Quantity':quantity,"Cost Month":cost_month}
                        zoho.loc[len(zoho)] = new_row
                    else:
                        new_row={'Journal Date':selected_date,'Journal Number Prefix':'JN','Journal Number Suffix':employeeNumber,'Notes':f'Salary - {selected_month[:3]} 24','Currency':'INR','Account':i,'Description':row["Cost Center"],'Contact Name':"",'Debit':BS[i],'Credit':0,'Employee ID':employee,'Quantity':quantity,"Cost Month":cost_month}
                        zoho.loc[len(zoho)] = new_row
                extracted_rows_for_employee =[]
                extracted_rows_for_employee = zoho[(zoho['Employee ID'] == employee) & (zoho['Debit'] >= 0)]
                sumOfDebit=extracted_rows_for_employee['Debit'].sum()
                sumOfCredit=extracted_rows_for_employee['Credit'].sum()            
                difference = sumOfDebit-sumOfCredit
                row = zoho[(zoho['Account'] == 'Salaries and Employee Wages - Direct') & (zoho['Debit'] > 0) & (zoho['Employee ID'] == employee)]
                row['Debit']=row['Debit']-difference
                zoho.loc[row.index] = row


            zoho = zoho.loc[(zoho['Debit'] != 0) | (zoho['Credit'] != 0)]
            st.write(zoho)

        logout_button = st.button("Logout")
        if logout_button:
            # Clear the session state
            st.session_state.clear()
            st.rerun()

if __name__ == "__main__":
    main()  

   
    

            

# # Use st.session_state to store the current page and authentication status
# if "page" not in st.session_state:
#     st.session_state.page = "home"
# if "authenticated" not in st.session_state:
#     st.session_state.authenticated = False

# # if authentication_status:
# #     authenticator.logout('Logout', 'main')

   
# # elif authentication_status == False:
# #     st.error('Username/password is incorrect')
# # elif authentication_status == None:
# #     st.warning('Please enter your username and password')

# print(st.session_state)

# if st.session_state["authentication_status"]:
#     authenticator.logout('Logout', 'main')
#     st.session_state.page = "authenticated"
#     print(authenticator)

# elif st.session_state["authentication_status"] == False:
#     st.error('Username/password is incorrect')
# elif st.session_state["authentication_status"] == None:
#     st.warning('Please enter your username and password')

# # if "page" not in st.session_state:
# #     st.session_state.page = "home"
# # if "authenticated" not in st.session_state:
# #     st.session_state.authenticated = False

# # Authenticate the user



# # Display the selected page
# # if st.session_state.page == "home":
# #     home_page()
# if st.session_state.page == "authenticated":
#     authenticated_page()