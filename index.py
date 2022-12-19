# main file
from flask import Flask, render_template, redirect, request
from flask.views import View, MethodView
from flask_mysqldb import MySQL
from wtforms import Form, StringField, DateField, SubmitField, IntegerField

from entities.bill import Bill
from entities.flatmate import Flatmate
from entities.pdf_report import PdfReport
from utilities.db_utilities import insert

app = Flask(__name__)

# mysql config
app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'baly'
app.config['MYSQL_PASSWORD'] = 'lorem'
app.config['MYSQL_DB'] = 'flatmate_bill'

mysql = MySQL(app)

# home page
class HomePage(MethodView):

    def get(self):
        return render_template('home.html', name='home')

# bill page
class BillPage(View):
    methods = ['GET', 'POST']

    def  dispatch_request(self):
        bill_form = BillForm(request.form)
        
        if request.method == 'POST':

            # faltmate first
            flatmate_first = Flatmate(
                name = bill_form.name_first.data,
                days_in_house= bill_form.days_first.data
            )
            insert('flatmates', 
            ['name', 'days_in_house'], 
            (flatmate_first.name, int(flatmate_first.days_in_house)),
            mysql)

            # faltmate second
            flatmate_second = Flatmate(
                name = bill_form.name_second.data,
                days_in_house= bill_form.days_second.data
            )
            insert('flatmates', 
            ['name', 'days_in_house'], 
            (flatmate_second.name, 
            int(flatmate_second.days_in_house)),
            mysql)

            # bill
            bill = Bill(
                amount = bill_form.amount.data,
                period = bill_form.period.data
            )
            insert('bills', 
            ['amount', 'period', 'id_first_flatmate', 'id_second_flatmate'], 
            (int(bill.amount), bill.period, 1, 2),
            mysql)

            # generate pdf report
            bill_pdf_report = PdfReport('bill_' + str(bill.period))
            bill_pdf_report.generate(bill, [flatmate_first, flatmate_second])
            print('The pdf report has been generated in the /reports folder')

            return redirect('/bill')

        return render_template('bill.html', bill_form=bill_form)

# bill form
class BillForm(Form):
    
    #bill
    amount = IntegerField('Bill Amount')
    period = DateField('Bill Period')

    #first_users
    name_first = StringField('A - Flatmate Name')
    days_first = IntegerField('A - Days in House')

    #second_users
    name_second = StringField('B - Flatmate Name')
    days_second = IntegerField('B - Days in House')

    #submit
    submit = SubmitField('Generate')

# pages rendering
app.add_url_rule('/', view_func=HomePage.as_view('home_page'))
app.add_url_rule('/bill', view_func=BillPage.as_view('bill_page'))

# app running
if __name__ == '__main__':
    app.run(debug=True, port=8001)