from flask import Flask, render_template, request, send_file
import qrcode
from PIL import Image
import io
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form.get('url', 'https://www.solucaonetwork.com.br')
        fill_color = request.form.get('fill_color', 'black')
        back_color = request.form.get('back_color', 'white')

        # Cria uma instância do objeto QRCode com as configurações desejadas
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=1,
        )
        qr.add_data(url)
        qr.make(fit=True)
        qr_img = qr.make_image(fill_color=fill_color, back_color=back_color).convert('RGB')

        # Adiciona o logotipo
         # Adiciona o logotipo
        try:
            # Corrige o caminho para o logo usando os.path.join
            logo_path = os.path.join(app.root_path, 'static', 'img', 'logo.png')
            logo = Image.open(logo_path)

            logo_size = qr_img.size[0] // 3
            logo = logo.resize((logo_size, logo_size), Image.LANCZOS)
            logo_position = ((qr_img.size[0] - logo.size[0]) // 2, (qr_img.size[1] - logo.size[1]) // 2)
            qr_img.paste(logo, logo_position, logo)
        except Exception as e:
            print(f"Error loading logo: {e}")

        # Salva a imagem em um buffer de memória
        buf = io.BytesIO()
        qr_img.save(buf, format='PNG')
        buf.seek(0)

        # Envia a imagem como resposta HTTP
        return send_file(buf, mimetype='image/png', as_attachment=False, download_name='qrcode.png')

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
