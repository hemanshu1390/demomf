from flask import Flask, request, Response
import xmltodict
import dicttoxml

app = Flask(__name__)

# Sample customer database (for demonstration purposes)
customers = {}

# Route to fetch customer details
@app.route('/get-customer', methods=['POST'])
def get_customer():
    try:
        data = xmltodict.parse(request.data)
        iin = data['NMFIIService']['service_request']['iin']

        if iin in customers:
            response_data = {
                'NMFIIService': {
                    'service_response': {
                        'status': 'success',
                        'message': 'Customer found',
                        'customer_data': customers[iin]
                    }
                }
            }
        else:
            response_data = {
                'NMFIIService': {
                    'service_response': {
                        'status': 'error',
                        'message': 'Customer not found'
                    }
                }
            }

        response_xml = dicttoxml.dicttoxml(response_data, custom_root='NMFIIService', attr_type=False)
        return Response(response_xml, mimetype='application/xml')

    except Exception as e:
        error_response = {'NMFIIService': {'service_response': {'status': 'error', 'message': str(e)}}}
        response_xml = dicttoxml.dicttoxml(error_response, custom_root='NMFIIService', attr_type=False)
        return Response(response_xml, mimetype='application/xml')

# Route to create customer
@app.route('/create-customer', methods=['POST'])
def create_customer():
    try:
        data = xmltodict.parse(request.data)
        appln_id = data['NMFIIService']['service_request']['appln_id']
        password = data['NMFIIService']['service_request']['password']
        broker_code = data['NMFIIService']['service_request']['broker_code']
        iin = data['NMFIIService']['service_request']['iin']

        customers[iin] = {
            'appln_id': appln_id,
            'password': password,
            'broker_code': broker_code,
            'iin': iin
        }

        response_data = {
            'NMFIIService': {
                'service_response': {
                    'status': 'success',
                    'message': 'Customer created successfully',
                    'iin': iin
                }
            }
        }

        response_xml = dicttoxml.dicttoxml(response_data, custom_root='NMFIIService', attr_type=False)
        return Response(response_xml, mimetype='application/xml')

    except Exception as e:
        error_response = {'NMFIIService': {'service_response': {'status': 'error', 'message': str(e)}}}
        response_xml = dicttoxml.dicttoxml(error_response, custom_root='NMFIIService', attr_type=False)
        return Response(response_xml, mimetype='application/xml')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
