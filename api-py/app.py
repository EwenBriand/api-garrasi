from flask import Flask, request, send_file, render_template
import python as back
from flask_cors import CORS
import sys
import asyncio
from waitress import serve

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})


@app.route('/', methods=['GET'])
def test():
    return back.test(), 200


@app.route('/sc_lacentral', methods=['GET'])
async def sc_lacentral():
    data = request.args.get('url')
    if data is not None:
        print('hello')
        res = await back.get_detail(data)
        if res == None:
            return 'Error func return None', 400
        return res, 200
    else:
        return 'Bad request', 400


@app.route('/download', methods=['POST'])
def download():
    data = request.get_json()
    if data is not None:
        res = back.download_tab([data['tab_1.1'], data['tab_1.2'],
                                data['tab_2.1'], data['tab_2.2']])
        if res == None:
            return 'Error func return None', 400
        return send_file(res, as_attachment=True), 200


@app.route('/url_cote_mob', methods=['GET'])
async def url_cote_mob():
    data = request.args.get('url')
    if data is not None:
        print(data)
        res = await back.get_url_lacentral(data)
        if res == None:
            return 'Bad URL', 400
        else:
            return res, 200
    else:
        return 'Bad request', 400


@app.route('/sc_neo', methods=['GET'])
def sc_neo():
    data = request.args.get('url')
    if data is not None:
        res = back.scrap_neo_ft(data)
        if res == None:
            return 'Error func return None', 400
        return res, 200
    else:
        return 'Bad request', 400


@app.route('/sc_mob', methods=['GET'])
def sc_mob():
    data = request.args.get('url')
    if data is not None:
        res = back.scrap_mobile_offre(data)
        if res == None:
            return 'Error func return None', 400
        return res, 200
    else:
        return 'Bad request', 400


@app.route('/doss_num', methods=['GET'])
def doss_num():
    data = request.args.get('url')
    if data is not None:
        res = back.get_doss_num(data)
        if res == None:
            return 'Error func return None', 400
        return res, 200
    else:
        return 'Bad request', 400


@app.route('/li_doss', methods=['POST'])
def li_doss():
    data = None
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        data = request.get_json()

    if data is not None:
        res = back.creat_doss(data)
        if res == None:
            return 'Error func return None', 400
        return res, 200
    else:
        return 'Bad request', 400


@app.route('/center', methods=['POST'])
def center():
    data = None
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        data = request.get_json()

    if data is not None:
        try:
            res = back.centraliser_info(
                data['type_offre'], data['neo'], data['offre'], data['lizfi'], data['cg'], data['frais'])
            if res == None:
                return 'Error func return None', 400
            return res, 200
        except Exception as e:
            print(e)
            return str(e), 500
    else:
        return 'Bad request', 400


@app.route('/li_list', methods=['POST'])
def li_list():
    data = None
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        data = request.get_json()

    if data is not None:
        res = back.get_lizfi_list(data['marque'], data['model'])
        if res == None:
            return 'Error func return None', 400
        return res, 200
    else:
        return 'Bad request', 400


@app.route('/marque_neo', methods=['POST'])
def marque_neo():
    data = None
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        data = request.get_json()

    if data is not None:
        res = back.marque(back.get_head())
        if res == None:
            return 'Error func return None', 400
        return res, 200
    else:
        return 'Bad request', 400


@app.route('/model_neo', methods=['POST'])
def model_neo():
    data = None
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        data = request.get_json()

    if data is not None:
        res = back.model(back.get_head(), data['marque'])
        if res == None:
            return 'Error func return None', 400
        return res, 200
    else:
        return 'Bad request', 400


@app.route('/version_neo', methods=['POST'])
def version_neo():
    data = None
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        data = request.get_json()

    if data is not None:
        res = back.version(back.get_head(), data['model'])
        if res == None:
            return 'Error func return None', 400
        return res, 200
    else:
        return 'Bad request', 400


@app.route('/make_1', methods=['POST'])
def make_1():
    data = None
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        data = request.get_json()

    if data is not None:
        try:
            res = back.make_first_tab(data['info'])
            if res == None:
                return 'Error func return None', 400
            return res, 200
        except Exception as e:
            print(e)
            return str(e), 500
    else:
        return 'Bad request', 400


@app.route('/make_2', methods=['POST'])
def make_2():
    data = None
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        data = request.get_json()

    if data is not None:
        try:
            res = back.make_sec_tab(data['info'], data['cote'])
            if res == None:
                return 'Error func return None', 400
            return res, 200
        except Exception as e:
            print(e)
            return str(e), 500
    else:
        return 'Bad request', 400


@app.route('/li_url_cote', methods=['POST'])
def li_url_cote():
    data = None
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        data = request.get_json()

    if data is not None:
        res = asyncio.run(back.get_html_page(
            data['marque'], data['model'], int(data['year'])))
        if res == None:
            return 'Error func return None', 400
        return res, 200
    else:
        return 'Bad request', 400


@app.route('/cote_lacentral', methods=['POST'])
def cote_lacentral():
    data = None
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        data = request.get_json()

    if data is not None:
        try:
            res = asyncio.run(back.get_central_cote(data['info']))
            if res == None:
                return 'Error func return None', 400
            return res, 200
        except Exception as e:
            print(e)
            return str(e), 500
    else:
        return 'Bad request', 400


if __name__ == '__main__':
    # serve(app, host='0.0.0.0', port=8080)
    app.run(debug=True)

#  http://127.0.0.1:5000
