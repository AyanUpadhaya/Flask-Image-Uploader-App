from flask import Flask, request, url_for,render_template, redirect
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

#configurations
app.config["IMAGE_UPLOADS"] ='static/imgs'
app.config['ALLOWED_IMAGE_EXTENSIONS']=['JPG','JPEG','PNG','GIF']

#check if image file
def allowed_images(filename):
	if  ' ' in filename:
		return False

	ext = filename.rsplit('.',1)[1]

	if ext.upper()  in app.config['ALLOWED_IMAGE_EXTENSIONS']:
		return True
	else:
		return False
#upload images
@app.route('/',methods=['GET','POST'])
def index():
	if request.method == "POST":
		if request.files:
			image = request.files['image']
			
			if image.filename =="":
				print("No file selected")
				return redirect(request.url)
	
			if allowed_images(image.filename):
				filename = secure_filename(image.filename)
				image.save(os.path.join(app.config["IMAGE_UPLOADS"], filename))
				print("image saved!")
				print(filename)
				return redirect(request.url)
			else:
				print('Unknown file format')
				return redirect(request.url)

		return redirect(request.url)
			
	else:
		return render_template('index.html',title="Application | Home")
# gallery of images
@app.route('/gallery.html')
def gallery():
	imgs = os.listdir(app.config["IMAGE_UPLOADS"])
	return render_template('gallery.html',title="Application | Gallery",imgs=imgs)
@app.route('/delete/<string:img>')
def delete(img):
	path = 'static/imgs'
	os.remove(os.path.join(path,img))
	print(img+" deleted successfully")
	return redirect('/gallery.html')
if __name__=="__main__":
	app.run(debug=True)