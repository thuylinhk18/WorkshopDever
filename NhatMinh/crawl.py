import requests
from bs4 import BeautifulSoup

# Gửi yêu cầu đến trang web
response = requests.get("https://danangfantasticity.com/en/things-to-do/entertainment-relax/sport-activities")

# Kiểm tra trạng thái yêu cầu
if response.status_code == 200:
    # Parse nội dung HTML
    soup = BeautifulSoup(response.content, 'html.parser')

    # Tìm tất cả các thẻ <a>
    
    
    # Lấy link con (ẩn trong các tag a) dẫn đến web con
    links = soup.find_all('a')
    link_cons = []
    for link in links:
        href = link.get('href')
        if href and "/things-to-do/" in href and href != "https://danangfantasticity.com/en/things-to-do/entertainment-relax/sport-activities":
            link_cons.append(href)
else:
    print("Lỗi khi truy cập trang web")

def scrape_web_con(url):
    """
    Hàm scrape thông tin từ web con

    Args:
        url (str): URL của web con

    Returns:
        dict: {'tieu_de': tiêu đề bài viết, 'noi_dung': nội dung bài viết}
    """
    # Gửi yêu cầu đến web con
    response = requests.get(url)

    # Kiểm tra trạng thái yêu cầu
    if response.status_code == 200:
        # Parse nội dung HTML
        soup = BeautifulSoup(response.content, 'html.parser')

        # Lấy tiêu đề bài viết
        tieu_de = soup.find('a', class_='post-url post-title').text.strip()

        # Kiểm tra xem có tìm thấy thẻ div mục tiêu không
        div_content = soup.find('div', class_='entry-content clearfix single-post-content')

        # Lấy nội dung bài viết (nếu tìm thấy thẻ div)
        noi_dung = []
        if div_content:
            for p in div_content.find_all('p'):
                noi_dung.append(p.text.strip())
            noi_dung_str = ", ".join(noi_dung)
        else:
            noi_dung_str = None  # Không tìm thấy nội dung


        # Trả về dữ liệu đã scrape
        return {'tieu_de': tieu_de, 'noi_dung': noi_dung_str}
    else:
        print(f"Lỗi khi truy cập trang web con: {url}")
        return {}

# Scrape thông tin từ các web con và lưu vào file Excel
import pandas as pd

data = []
for link_con in link_cons:
    data.append(scrape_web_con(link_con))

# Tạo dataframe và lưu vào file Excel
df = pd.DataFrame(data)
df.to_excel('data.xlsx', index=False)
