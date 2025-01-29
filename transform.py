import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
import pandas as pd
import streamlit as st

with open('./cred.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)
# hashed_passwords = stauth.Hasher(['abc', 'def']).generate()
# print(hashed_passwords)
# authenticator = stauth.Authenticate(
#     config['credentials'],
#     config['cookie']['name'],
#     config['cookie']['key'],
#     config['cookie']['expiry_days'],
#     config['preauthorized']
# )
# name, authentication_status, username = authenticator.login('Login', 'main')
#authenticator.login()

def authenticated_page():
    # st.set_page_config(page_title="File Uploader")

# Create a file uploader widget
    uploaded_file = st.file_uploader("Choose a file", type=["csv", "txt", "pdf","xlsx"])
    
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
        columns=['Journal Date','Reference Number','Journal Number Prefix','Journal Number Suffix','Notes','Currency','Account','Description','Contact Name','Debit','Credit','Project Name','Employee ID']
        zoho = pd.DataFrame(columns=columns)

        dummy = ["Employee Number","Employee Name","Basic & DA",
        "HRA",
        "Special Allowance",
        "LTA",
        "Laptop Reimbursements",
        "other",
        "Medical Insurance",
        "PF - Employer",
        "ESI Employer",
        "Employee Gratuity contribution",
        "PF Employee",
        "ESI Employee",
        "Professional Tax",
        "Total Income Tax",
        "Medical Insurance Deduction",
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
        print(filter_)
        common_columns = list(set(df_.columns) & set(filter_.columns))


        df = df_[common_columns]

        print(df.columns)
        Debit ={'Salaries and Employee Wages - Direct':['Basic & DA','HRA','Special Allowance','LTA', 'Laptop Reimbursements','Medical Insurance','PF - Employer','ESI Employer','Employee Gratuity contribution'], 'Employee Advance':['Cash Advance'],'Other Expenses':['Others','Courier Charges'],'Food expenses':'Food expenses','Travel & Accommodation Expense':'Travelling', 'Laptop Reimbursement':'Laptop Reimburesement', }
        Credit ={'Salaries and Employee Wages - Direct':"Other Deduction",'Insurance':["Medical Insurance","Medical Insurance Deduction" ],'PF Payable':['PF - Employer','PF Employee'],'ESI Payable':['ESI Employer','ESI Employee'],'Gratuity Payable':'Employee Gratuity contribution','TDS Payable':'Total Income Tax','Professional Tax Payable':'Professional Tax' ,'Employee Advance':['Settlement Against Advance'],'Salary Payable':'Total Net Pay(D+E+F+G)'}


        paygroup=''
        employeeNumber=0
        referenceNumber=0

        for index, row in df.iterrows():
            # payGroup = row['Pay Group']
            PL={'Salaries and Employee Wages - Direct':[0,0],'Insurance':0,'Other Expenses':0,'Food Expenses':0,'Travel & Accommodation Expense':0,'Laptop Reimburesement':0}
            BS={'PF Payable':0,'ESI Payable':0,'Gratuity Payable':0,'TDS Payable':0,'Salary Payable':0,'TDS Payable':0,'Professional Tax Payable':0,'Employee Advance':0}

            # if index == 0:
            employeeNumber=employeeNumber+1
            for i in range (0,len(row.index)):

                value_to_find = row.index[i]
                # Debit Items
                keys =[key for key,value in Debit.items() if value_to_find in value]

                # for key,value in Debit.items():


                if len(keys) >0:

                # new_row={'Journal Date':'2024-03-10','Reference Number':'Ref123','Journal Number Prefix':'JN','Journal Number Suffix':'0023','Notes':"Testing",'Currency':'USD','Account':keys[0],'Description':'None','Contact Name':payGroup,'Debit':row[value_to_find],'Credit':0,'Project Name':payGroup}
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
            #employee = str(row['Employee Number'])+"  "+row['Employee Name'] # Two spaces
            employee = str(row['Employee Number']) + "  " + str(row['Employee Name'])  # Two spaces

            for i in PL:
                referenceNumber=referenceNumber+1
                

                if i == "Salaries and Employee Wages - Direct":
                    new_row={'Journal Date':'2024-03-10','Reference Number':f'Ref{referenceNumber}','Journal Number Prefix':'JN','Journal Number Suffix':employeeNumber,'Notes':"Salary - Feb'24",'Currency':'INR','Account':i,'Description':row["Cost Center"],'Contact Name':"",'Debit':PL[i][0],'Credit':0,'Project Name':row["Cost Center"],'Employee ID':employee}
                    zoho.loc[len(zoho)] = new_row
                    if PL[i][1] != 0:
                        new_row={'Journal Date':'2024-03-10','Reference Number':f'Ref{referenceNumber}','Journal Number Prefix':'JN','Journal Number Suffix':employeeNumber,'Notes':"Salary - Feb'24",'Currency':'INR','Account':i,'Description':row["Cost Center"],'Contact Name':"",'Debit':0,'Credit':PL[i][1],'Project Name':row["Cost Center"],'Employee ID':employee}
                        zoho.loc[len(zoho)] = new_row

                    continue

                if i in Credit:
                    new_row={'Journal Date':'2024-03-10','Reference Number':f'Ref{referenceNumber}','Journal Number Prefix':'JN','Journal Number Suffix':employeeNumber,'Notes':"Salary - Feb'24",'Currency':'INR','Account':i,'Description':row["Cost Center"],'Contact Name':"",'Debit':0,'Credit':PL[i],'Project Name':row["Cost Center"],'Employee ID':employee}
                    zoho.loc[len(zoho)] = new_row
                else:
                    new_row={'Journal Date':'2024-03-10','Reference Number':f'Ref{referenceNumber}','Journal Number Prefix':'JN','Journal Number Suffix':employeeNumber,'Notes':"Salary - Feb'24",'Currency':'INR','Account':i,'Description':row["Cost Center"],'Contact Name':"",'Debit':PL[i],'Credit':0,'Project Name':row["Cost Center"],'Employee ID':employee}
                    zoho.loc[len(zoho)] = new_row


            for i in BS:
                referenceNumber=referenceNumber+1

                if i in Credit:
                    new_row={'Journal Date':'2024-03-10','Reference Number':f'Ref{referenceNumber}','Journal Number Prefix':'JN','Journal Number Suffix':employeeNumber,'Notes':"Salary - Feb'24",'Currency':'INR','Account':i,'Description':row["Cost Center"],'Contact Name':"",'Debit':0,'Credit':BS[i],'Project Name':row["Cost Center"],'Employee ID':employee}
                    zoho.loc[len(zoho)] = new_row
                else:
                    new_row={'Journal Date':'2024-03-10','Reference Number':f'Ref{referenceNumber}','Journal Number Prefix':'JN','Journal Number Suffix':employeeNumber,'Notes':"Salary - Feb'24",'Currency':'INR','Account':i,'Description':row["Cost Center"],'Contact Name':"",'Debit':BS[i],'Credit':0,'Project Name':row["Cost Center"],'Employee ID':employee}
                    zoho.loc[len(zoho)] = new_row
            extracted_rows_for_employee =[]
            extracted_rows_for_employee = zoho[(zoho['Employee ID'] == employee) & (zoho['Debit'] >= 0)]
            print(extracted_rows_for_employee)
            sumOfDebit=extracted_rows_for_employee['Debit'].sum()
            sumOfCredit=extracted_rows_for_employee['Credit'].sum()
            print(sumOfDebit)
            print(sumOfCredit)
            difference = sumOfDebit-sumOfCredit
            print(difference)
            row = zoho[(zoho['Account'] == 'Salaries and Employee Wages - Direct') & (zoho['Debit'] > 0) & (zoho['Employee ID'] == employee)]
            print(row)
            row['Debit']=row['Debit']-difference
            print(row['Debit'])
            zoho.loc[row.index] = row


        zoho = zoho.loc[(zoho['Debit'] != 0) | (zoho['Credit'] != 0)]
        print(zoho)
        st.write(zoho)


    

   
    

            



# Use st.session_state to store the current page and authentication status
if "page" not in st.session_state:
    st.session_state.page = "home"
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# Bypass authentication check by forcing the page to "authenticated"
st.session_state.page = "authenticated"  # Forcing the page to authenticated

# Print session state for debugging
print(st.session_state)

# Here, we're bypassing the actual authentication logic
if st.session_state.page == "authenticated":
    # Assuming authenticated_page() is a function to display the authenticated page
    authenticated_page()
