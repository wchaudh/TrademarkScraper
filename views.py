from flask import render_template, flash, redirect, request, Response
from application import application
import requests
from bs4 import BeautifulSoup
import os
import pandas as pd
import numpy as np
from tqdm import *
import sys
import time
import logging
import pathlib
import re

@application.route('/')
@application.route('/index', methods = ['POST', 'GET'])
def index():
    columns = ['rn', 'sn', 'brand_name', 'mark_literal', 'status', 'registration_date',
           'register','mark_drawing_type', 'owner_name', 'source_country',
           'attorney', 'attorney_email', 'attorney_phone', 'correspondent', 'correspondent_email',
           'email_auth']

    if request.method == 'POST':
        try:
            items = request.form['text']
            result = re.sub('[^0-9,\s]','', items)
            #items_list = result.split(",")
            items_list = result.split()
        except:
            items_list = list()
        trade_frame = list()
        for item in tqdm(items_list):

            if len(item) == 8:
                url = "http://tsdr.uspto.gov/statusview/sn" + item
            elif len(item) <= 7:
                url = "http://tsdr.uspto.gov/statusview/rn" + item
            else:
                pass

            html=requests.get(url).content
            soup = BeautifulSoup(html, "lxml")

            try:
                sn = soup.find(text='US Serial Number:').next.next.text.strip()
            except:
                sn = ''

            try:
                rn = soup.find(text='US Registration Number:').next.next.text.strip()
            except:
                rn = ''

            try:
                mark = soup.find(text='Mark:').next.next.text.strip()
            except:
                mark = ''

            try:
                mark_literal = soup.find(text='Mark Literal Elements:').next.next.text.strip()
            except:
                mark_literal = ''

            try:
                status = soup.find(alt='TM5 Common Status image').next.next.next.next.next.next.text.strip()
            except:
                status = ''

            try:
                registration_date = soup.find(text='Registration Date:').next.next.text.strip()
            except:
                registration_date = ''

            try:
                register = soup.find(text='Register:').next.next.text.strip()
            except:
                register = ''

            try:
                mark_drawing_type = soup.find(text='Mark Drawing Type:').next.next.text.strip()[:1]
            except:
                mark_drawing_type = ''

            try:
                owner = soup.find(text='Owner Name:').next.next.text.strip()
            except:
                owner = ''

            try:
                source_country = soup.find(text='State or Country Where Organized:').next.next.text.strip()
            except:
                source_country = ''

            try:
                attorney = soup.find(text='Attorney Name:').next.next.text.strip()
            except:
                attorney = ''

            try:
                attorney_email = soup.find(text='Attorney Primary Email Address:').next.next.text.strip()
            except:
                attorney_email = ''

            try:
                attorney_phone = soup.find(text='Phone:').next.next.text.strip()
            except:
                attorney_phone = ''

            try:
                correspondent = soup.find(text='Correspondent Name/Address:').next.next.text.strip()
            except:
                correspondent = ''

            try:
                correspondent_email = soup.find(text='Correspondent e-mail:').next.next.text.strip()
            except:
                correspondent_email = ''

            try:
                email_auth = soup.find(text='Correspondent e-mail Authorized:').next.next.text.strip()
            except:
                email_auth = ''

            metadata = [rn, sn, mark, mark_literal, status, registration_date, register, mark_drawing_type,
                       owner, source_country, attorney, attorney_email, attorney_phone, correspondent, correspondent_email,
                       email_auth]
            trade_frame.append(metadata)

        df = pd.DataFrame(trade_frame, columns = columns).to_html(classes='male')

    else:
        processed_text = ""
        df = ""
        items_list = ""
        url = ""
    return render_template("index.html",
                           table = df,
                           debug = items_list
                           )
    return Response(
        df,
        mimetype="text/csv",
        headers={"Content-disposition":
                 "attachment; filename=trademark_out.csv"})
