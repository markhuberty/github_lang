import re

re_ml = re.compile('machine learning')
re_nlp = re.compile('natural language|nlp')
re_statistics = re.compile('statistics')
re_enterprise = re.compile('enterprise| sap |peoplesoft|salesforce|accounting')
re_amazon = re.compile(' aws |amazon web services')
re_mobile = re.compile('mobile|smart phone')
re_cloud = re.compile('cloud')
re_finance = re.compile('finance')
re_encryption = re.compile('encryption|security')
re_social = re.compile('twitter|facebook|myspace|google plus|tumblr)


re_dict = {'ml':re_ml,
           'nlp': re_nlp,
           'stats': re_statistics,
           'enterprise': re_enterprise,
           'finance': re_finance,
           'cloud': re_cloud,
           'aws': re_amazon,
           'mobile': re_mobile,
           'encryption': re_encryption,
           }
