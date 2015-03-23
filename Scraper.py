from taskbarNotifier import WindowsBalloonTip
from BeautifulSoup import BeautifulSoup
import mechanize
from StringIO import StringIO
from PIL import Image
from CaptchaParser import CaptchaParser
import cookielib
import time, threading

approval_array = []
def balloon_tip(title, msg):
    w=WindowsBalloonTip(title, msg)


def Scanner():
    br = mechanize.Browser()
    br.set_handle_redirect(True)
    br.set_handle_referer(True)
    cj = cookielib.CookieJar()
    br.set_cookiejar(cj)
    response = br.open('https://academics.vit.ac.in/student/stud_login.asp')
    html = response.read()
    soup = BeautifulSoup(html)
    im = soup.find('img', id='imgCaptcha')
    image_response = br.open_novisit(im['src'])
    img = Image.open(StringIO(image_response.read()))
    parser = CaptchaParser()
    captcha = parser.getCaptcha(img)
    br.select_form('stud_login')
    br.form['regno'] = ''
    br.form['passwd'] = ''
    br.form['vrfcd'] = str(captcha)
    br.submit()
    if(br.geturl() == "https://academics.vit.ac.in/student/home.asp"):
        print "-"*30
        print " "*12+"SUCCESS"
        print "-"*30
        br.open('https://academics.vit.ac.in/student/stud_home.asp')
        response1 = br.open('https://academics.vit.ac.in/student/student_outing_request.asp')
        html1 = response1.read()
        soup1 = BeautifulSoup(html1)
        trs = soup1.findAll('tr')
        index = 0
        for tr in trs:
            if(tr.text=="Sl.NoApply onApply ToLeave TypeFromToNo. of Hrs"):
                break
            index = index + 1
        outing_history = []

        for tr in trs[index+1:]:
            tds = tr.findAll('td')
            outing_history.append({'sl_no': tds[0].text,
                                    'apply_on': tds[1].text,
                                    'apply_to': tds[2].text,
                                    'leave_type': tds[3].text,
                                    'from': tds[4].text,
                                    'to': tds[5].text,
                                    'no_of_hrs': tds[6].text,
                                    'approved_by': tds[7].text,
                                    'approved_on': tds[8].text,
                                    'approval_status': tds[9].text})
        if outing_history[0]['approval_status'] == '':
            if len(approval_array) != 0:
                if approval_array[len(approval_array)-1] == 'n':
                    approval_array.append('a')
                    if __name__ == '__main__':
                        balloon_tip("NOTIFY", "APPROVED")
                        return
            else:
                approval_array.append('a')
        



                
        else: 
            approval_array.append('n')



    else:
        print"FAIL"
    print(time.ctime())
    threading.Timer(10, Scanner).start()

Scanner()

                                