# -*- coding: utf-8 -*-
import requests

from odoo import http
from odoo.http import request
import json
import requests
import base64
from datetime import datetime, date




class SmsSchool(http.Controller):
    @http.route('/create_teacher', type='json', auth='user', methods=['POST'])
    def create_teacher(self, **kwargs):
        self.get_teacher_data()
        if request.httprequest:
            ids = []
            for key, value in kwargs.items():
                print(key, value)
                teacher_values = {}
                if value['name']:
                    teacher_values['name'] = value['name']
                if value['middle']:
                    teacher_values['middle'] = value['middle']
                if value['last']:
                    teacher_values['last'] = value['last']
                if value['photo']:
                    response = requests.get(value['photo'])
                    image_data = response.content
                    # Convert the image data to a base64 encoded string
                    encoded_image_data = base64.b64encode(image_data).decode('utf-8')
                    # Assign the base64 encoded string to the photo field of the teacher record
                    teacher_values['photo'] = encoded_image_data
                if value['age']:
                    teacher_values['age'] = value['age']
                if value['gender']:
                    teacher_values['gender'] = value['gender']
                if value['teacher_ssn']:
                    teacher_values['teacher_ssn'] = value['teacher_ssn']
                if value['contact_phone']:
                    teacher_values['contact_phone'] = value['contact_phone']
                if value['email']:
                    teacher_values['email'] = value['email']
                if value['rank']:
                    teacher_values['rank'] = value['rank']
                if value['contact_mobile']:
                    teacher_values['contact_mobile'] = value['contact_mobile']

                teacher = request.env['school.teacher'].sudo().create(teacher_values)
                ids.append(teacher.id)
                print(ids)
            data = {'status': 'success', 'ids': ids, 'message': 'Success'}
        return data

    def get_teacher_data(self, **kw):
        response_API = requests.get('https://jsonplaceholder.typicode.com/users')
        print(response_API.status_code)

        # 2. Get the data from API
        data = response_API.text
        # print(data)
        # 3. Parse the data into JSON format
        parse_json = json.loads(data)
        print(parse_json)
        active_case = parse_json[0]['name']
        print("Active cases in South Andaman:", active_case)

        print('rec', kw)
        if parse_json[0]['name']:
            vals = {
                'patient_name': parse_json[0]['name'],
                'pharmacy_note': parse_json[0]['username']
            }
            # new_patient = request.env['hospital.patient'].create(vals)
            print('vals', vals)
            args = {'status': 200, 'success': True, 'message': 'Success', 'ID': 1}
        return args

# url = 'http://localhost:8069/create_teacher'
# headers = {'Content-Type': 'application/json'}
# data = {
#     'name': 'John Doe',
#     'middle': '123456789',
#     'last': 'john.doe@example.com'
# }
# response = requests.post(url, headers=headers, data=json.dumps({'data': json.dumps(data)}))
# if response.status_code == 200:
#     response_data = response.json()
