from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from urllib.parse import urlencode, quote_plus, unquote
import requests
import serial


#미세먼지API받아오는 코드
url = 'https://apis.data.go.kr/B552584/ArpltnInforInqireSvc/getMsrstnAcctoRltmMesureDnsty'
queryParams = '?' + urlencode({quote_plus('serviceKey') : 
	'dvs12WFEjwigr+2+Ezu2Cnetgs16GFTKeT37y8ECv1RDE0DJUZtO6BricXM/oGYybBptSoeSJumiLzWtjQjj4Q=='
	, quote_plus('returnType') : 'xml'
		,quote_plus('numOfRow') : '10'
			,quote_plus('pageNo') : '1'
				,quote_plus('stationName') : '주안'
					, quote_plus('dataTerm') : 'DAILY' 
						, quote_plus('ver') : '1.0'})

res = requests.get(url+queryParams)
soup = BeautifulSoup(res.content, 'html.parser')
data = soup.find_all('item')
#print(data)

for item in data : 
	datatime = item.find("datatime")
	pm25value = item.find("pm25value")
	#print(datatime.get_text())
	#print(pm25value/get_text())
	

#아두이노 연동 코드
port = '/dev/ttyACM0'
brate = 9600
cmd = 'temp'
seri = serial.Serial(port, baudrate = brate, timeout = None)
print(seri.name)

seri.write(cmd.encode())

while 1:
	if seri.in_waiting !=0 :
		content =  seri.readline()
		print(f'기준시간: {datatime.get_text()}')
		print(f'실내 미세먼지: {content.decode()}', end='')
		print(f'실외 미세먼지: {pm25value.get_text()}')
		a = content.decode()

		if float(pm25value.get_text()) < float(a):
			print('환기를 하세요.')
		else:
			print('창문을 닫으세요.')
