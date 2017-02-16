# Page Object Pattern with Behave
A small proof of concept of using the Page Object pattern with behave

# What you need to run these tests
 - Make sure you have python 3.3+ installed
 - Install virtualenv (`pip install virtualenv`)
 - clone this repository
 - change the email address in `config.py` to your own (**IMPORTANT you need to provide an email that is registered on Ryanair**)
 - set an environment variable `RYANAIR_PASS_your_email_address` (in my case: `RYANAIR_PASS_TOMEKWSZELAKI@GMAIL.COM`) where you indicate the account's password
 
All dependencies are included in the virtual environment folder (po_pattern) so you should be ready to go.

## Run on Windows
```
cd page-object-pattern-python
po_patters\Scripts\activate
behave
```

## Run on Mac (I don't have a mac, so I'm not sure if it works, but it should)
```
cd page-object-pattern-python
source bin/activate
behave
```

# Test reports
Test reports are saved in the `/reports` folder. They are xml files (xUnit compliant format).

#Licence
MIT
