import random

def generate_captcha():
    captcha=' '
    for i in range(2):
        a=str(random.randint(0,9))
        b=chr(random.randint(65,90))
        captcha=captcha+' '+ a +'  '+b+'  '
        #captcha=captcha.replace(" ",'')
    return captcha