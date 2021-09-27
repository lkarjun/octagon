from bs4 import BeautifulSoup
from pydantic import BaseModel
import urllib3

BASE_URL_NOTIFICATION = "https://pareekshabhavan.uoc.ac.in/index.php/examination/notifications"
BASE_URL_EXAM_NOTIFICATION = "https://pareekshabhavan.uoc.ac.in/index.php/examination/timetable"

class notification(BaseModel):
    direct_link: str
    text: str
        
def make_data(links):
    links = [notification(text=i.text, direct_link=i.get('href')) for i in links]
    return links
        
def get_notifications():
    req = urllib3.PoolManager()
    text = req.request('GET', BASE_URL_NOTIFICATION).data.decode()
    soup = BeautifulSoup(text, features="html.parser")
    notifications = {
        'UG': make_data(soup.find("div", id="UG").find_all("a")),
        'PG': make_data(soup.find("div", id="PG").find_all("a")),
        'OTHER': make_data(soup.find("div", id="OTHER").find_all("a"))
    }
    return notifications


def get_exam_notifications():
    req = urllib3.PoolManager()
    text = req.request('GET', BASE_URL_EXAM_NOTIFICATION).data.decode()
    soup = BeautifulSoup(text, features="html.parser")
    notifications = {
        'UG': make_data(soup.find("div", id="UG").find_all("a")),
        'PG': make_data(soup.find("div", id="PG").find_all("a")),
        'OTHER': make_data(soup.find("div", id="OTHER").find_all("a"))
    }
    return notifications


def get_latest_exam_notifications():
    req = urllib3.PoolManager()
    text = req.request('GET', BASE_URL_EXAM_NOTIFICATION).data.decode()
    soup = BeautifulSoup(text, features="html.parser")
    return make_data(soup.find("div", id="ALL").find_all("a"))[:5]

def get_latest_notifications():
    req = urllib3.PoolManager()
    text = req.request('GET', BASE_URL_NOTIFICATION).data.decode()
    soup = BeautifulSoup(text, features="html.parser")
    return make_data(soup.find("div", id="ALL").find_all("a"))[:5]
