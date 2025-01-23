from flask import Flask, request, Response
import xmltodict
from dicttoxml import dicttoxml

app = Flask(__name__)

# Sample customer data (you can replace it with a database)
customers = {
    "5052456456": {"name": "John Doe", "iin": "5052456456", "status": "Active"},
}

def dict_to_xml_response(data_dict):
    xml_data = dicttoxml(data_dict, custom_root='response', attr_type=False)
    return Response(xml_data, mimetype='application/xml')

@app.route('/getCustomer', methods=['POST'])
def get_customer():
    try:
        xml_data = request.data.decode('utf-8')
        data_dict = xmltodict.parse(xml_data)

        iin = data_dict['NMFIIService']['service_request']['iin']
        if iin in customers:
            response_data = {
                "status": "success",
                "customer": customers[iin]
            }
        else:
            response_data = {"status": "error", "message": "Customer not found"}

        return dict_to_xml_response(response_data)

    except Exception as e:
        return dict_to_xml_response({"status": "error", "message": str(e)})

@app.route('/createCustomer', methods=['POST'])
def create_customer():
    try:
        xml_data = request.data.decode('utf-8')
        data_dict = xmltodict.parse(xml_data)

        customer_info = data_dict['NMFIIService']['service_request']
        iin = customer_info['iin']
        customers[iin] = {
            "name": customer_info.get("name", "Unknown"),
            "iin": iin,
            "status": "Active"
        }
        return dict_to_xml_response({"status": "success", "message": "Customer created", "iin": iin})

    except Exception as e:
        return dict_to_xml_response({"status": "error", "message": str(e)})

if __name__ == '__main__':
    app.run(debug=True)
