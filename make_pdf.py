import pdfkit
import  flask_website
flask_website.
config = pdfkit.configuration(wkhtmltopdf="C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe")
pdfkit.from_url("http://127.0.0.1:5000", 'test.pdf', configuration=config)

