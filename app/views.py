"""
Flask Documentation:     https://flask.palletsprojects.com/
Jinja2 Documentation:    https://jinja.palletsprojects.com/
Werkzeug Documentation:  https://werkzeug.palletsprojects.com/
This file contains the routes for your application.
"""
import os
from app import app, db
from flask import render_template, request, flash, redirect, url_for, send_from_directory
from app.models import PropertyProfile
from app.forms import PropertyForm
from werkzeug.utils import secure_filename

###
# Routing for your application.
###

@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')


@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html', name="Mary Jane")


@app.route('/properties')
def properties():
    property = PropertyProfile.query.all()
    return render_template('properties.html', property=property)

@app.route('/properties/<propertyid>')
def this_property(propertyid):
    property = PropertyProfile.query.filter_by(id=propertyid).first()
    return render_template('property.html',property=property)


@app.route('/property/create', methods=['POST','GET'])
def property():
    #flash("I am here!")
    form = PropertyForm()
    ##if request.method == 'POST':
    if form.validate_on_submit():
        photo = form.photo.data
        filename = secure_filename(photo.filename)
        photo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        title = form.title.data
        description = form.description.data
        bedroom = form.bedroom.data
        bathroom = form.bathroom.data
        price = form.price.data
        type = form.type.data
        location = form.location.data
        new_property = PropertyProfile(title, description, bedroom, bathroom, price, type, location, filename) 
        db.session.add(new_property)
        db.session.commit()    
        flash('Property successfully added! Yay!!', 'success')
        return redirect(url_for('properties'))
    
    flash_errors(form)
    return render_template('create_property.html', form=form)
            
@app.route("/uploads/<filename>")

def get_image(filename):
    return send_from_directory(os.path.join(os.getcwd(), app.config['UPLOAD_FOLDER']), filename)

###
# The functions below should be applicable to all Flask apps.
###

# Display Flask WTF errors as Flash messages
def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ), 'danger')

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also tell the browser not to cache the rendered page. If we wanted
    to we could change max-age to 600 seconds which would be 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404
