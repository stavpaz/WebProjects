from flask import Blueprint, render_template, redirect, url_for, session, request

# sign_in blueprint definition
business_profile = Blueprint('business_profile', __name__, static_folder='static', static_url_path='/business_profile',
                             template_folder='templates')
from utilities.db.db_manager import dbManager
from utilities.db.db_manager import dbManager
from classes.manicurists import manicurist
from classes.dynamicMani import DynamicMani
from classes.ratings import Rate


# Routes

@business_profile.route('/business_profile')
def def_business_profile():
    if session['isMani'] == False:
        return render_template('noProfileMessage.html')
    email = session['email']
    newManicurist = manicurist(email, FirstName='', LastName='', PhoneNumber='', password='', businessName='',
                               x_location='', y_location='',city='')
    users_list = newManicurist.getServices()
    manicurists = newManicurist.getMyDetails()
    images = newManicurist.getMyImages()
    city= newManicurist.getCity()

    return render_template('business_profile.html', services=users_list, name=manicurists[0][1],
                           aboutMe=manicurists[0][8], phoneNum=manicurists[0][3], images=images, rate=manicurists[0][9],
                           ismani=session['isMani'],city=city)


@business_profile.route('/business_profile/<int:ID>')
def def_business_profile_ByID(ID):
    newDynamic = DynamicMani(ID)
    email = newDynamic.getEmail()  # email of manicurist
    if email == 'null':
        return render_template('IDnotFound.html')
    session['currentMani'] = email[0]
    newManicurist = manicurist(email, FirstName='', LastName='', PhoneNumber='', password='', businessName='',
                               x_location='', y_location='',city='')
    users_list = newManicurist.getServices()
    manicurists = newManicurist.getMyDetails()
    images = newManicurist.getMyImages()
    city= newManicurist.getCity()
    if session['isMani'] == True:
        return render_template('noProfileMessage.html')
    return render_template('business_profile.html', services=users_list, name=manicurists[0][1],
                           aboutMe=manicurists[0][8], phoneNum=manicurists[0][3], images=images, rate=manicurists[0][9],
                           ismani=session['isMani'],city=city)


@business_profile.route('/business_edit')
def def_business_edit():
    email = session['email']
    newManicurist = manicurist(email, FirstName='', LastName='', PhoneNumber='', password='', businessName='',
                               x_location='', y_location='',city='')
    users_list = newManicurist.getServices()
    manicurists = newManicurist.getMyDetails()
    images = newManicurist.getMyImages()
    city= newManicurist.getCity()
    return render_template('business_edit.html', services=users_list, name=manicurists[0][1],
                           aboutMe=manicurists[0][8], phoneNum=manicurists[0][3], images=images, rate=manicurists[0][9],
                           ismani=session['isMani'],city=city)


@business_profile.route('/business_edit_about', methods=['get', 'post'])
def def_business_edit_AboutMe():
    email = session['email']
    newAbout = request.form['feedText']
    newManicurist = manicurist(email, FirstName='', LastName='', PhoneNumber='', password='', businessName='',
                               x_location='', y_location='',city='')
    users_list = newManicurist.getServices()
    manicurists = newManicurist.getMyDetails()
    images = newManicurist.getMyImages()
    if newAbout != '':
        newManicurist.setAbout(newAbout)
        message = "description successfully updated"
    else:
        message = "description is empty - please fill before submitting"
    return render_template('business_edit.html', services=users_list, name=manicurists[0][1],
                           aboutMe=manicurists[0][8], phoneNum=manicurists[0][3], images=images, message=message,
                           rate=manicurists[0][9], ismani=session['isMani'])


@business_profile.route('/business_add_service', methods=['get', 'post'])
def newservice():
    duplicate = False
    email = session['email']
    servicen = request.form['newService']
    price = request.form['newprice']
    newManicurist = manicurist(email, FirstName='', LastName='', PhoneNumber='', password='', businessName='',
                               x_location='', y_location='',city='')
    currentServices = newManicurist.getServices()
    for service in currentServices:
        if service.serviceName == servicen:
            duplicate = True
    if duplicate == False:  # update new service
        newservice = request.form['newService']
        newManicurist.AddService(price, email, newservice)
        message = "service successfully added"
    else:
        message = "service name already exist"
    currentServices = newManicurist.getServices()
    manicurists = newManicurist.getMyDetails()
    images = newManicurist.getMyImages()
    return render_template('business_edit.html', services=currentServices, name=manicurists[0][1],
                           aboutMe=manicurists[0][8], phoneNum=manicurists[0][3], images=images, message=message,
                           rate=manicurists[0][9], ismani=session['isMani'])


@business_profile.route('/pic1', methods=['get', 'post'])
def changepic1():
    URL = request.args['pic1']
    email = session['email']
    newManicurist = manicurist(email, FirstName='', LastName='', PhoneNumber='', password='', businessName='',
                               x_location='', y_location='',city='')
    users_list = newManicurist.getServices()
    manicurists = newManicurist.getMyDetails()
    images = newManicurist.getMyImages()
    message = "no pic was chosen please try again"
    if URL != '':
        image = images[0][0]
        for i in images:
            if i[0] == URL:
                message = "The picture is already exist"
                return render_template('business_edit.html', services=users_list, name=manicurists[0][1],
                                       aboutMe=manicurists[0][8], phoneNum=manicurists[0][3], images=images,
                                       message=message,
                                       rate=manicurists[0][9], ismani=session['isMani'])

        newManicurist.updateImage(image, URL)
        images = newManicurist.getMyImages()
        return render_template('business_edit.html', services=users_list, name=manicurists[0][1],
                               aboutMe=manicurists[0][8], phoneNum=manicurists[0][3], images=images,
                               rate=manicurists[0][9], ismani=session['isMani'])
    return render_template('business_edit.html', services=users_list, name=manicurists[0][1],
                           aboutMe=manicurists[0][8], phoneNum=manicurists[0][3], images=images, message=message,
                           rate=manicurists[0][9], ismani=session['isMani'])


@business_profile.route('/pic2', methods=['get', 'post'])
def changepic2():
    URL = request.args['pic2']
    email = session['email']
    newManicurist = manicurist(email, FirstName='', LastName='', PhoneNumber='', password='', businessName='',
                               x_location='', y_location='',city='')
    users_list = newManicurist.getServices()
    manicurists = newManicurist.getMyDetails()
    images = newManicurist.getMyImages()
    message = "no pic was chosen please try again"
    if URL != '':
        image = images[1][0]
        for i in images:
            if i[0] == URL:
                message = "The picture is already exist"
                return render_template('business_edit.html', services=users_list, name=manicurists[0][1],
                                       aboutMe=manicurists[0][8], phoneNum=manicurists[0][3], images=images,
                                       message=message,
                                       rate=manicurists[0][9], ismani=session['isMani'])

        newManicurist.updateImage(image, URL)
        images = newManicurist.getMyImages()
        return render_template('business_edit.html', services=users_list, name=manicurists[0][1],
                               aboutMe=manicurists[0][8], phoneNum=manicurists[0][3], images=images,
                               rate=manicurists[0][9], ismani=session['isMani'])
    return render_template('business_edit.html', services=users_list, name=manicurists[0][1],
                           aboutMe=manicurists[0][8], phoneNum=manicurists[0][3], images=images, message=message,
                           rate=manicurists[0][9], ismani=session['isMani'])


@business_profile.route('/pic3', methods=['get', 'post'])
def changepic3():
    URL = request.args['pic3']
    email = session['email']
    newManicurist = manicurist(email, FirstName='', LastName='', PhoneNumber='', password='', businessName='',
                               x_location='', y_location='',city='')
    users_list = newManicurist.getServices()
    manicurists = newManicurist.getMyDetails()
    images = newManicurist.getMyImages()
    message = "no pic was chosen please try again"
    if URL != '':
        image = images[2][0]
        for i in images:
            if i[0] == URL:
                message = "The picture is already exist"
                return render_template('business_edit.html', services=users_list, name=manicurists[0][1],
                                       aboutMe=manicurists[0][8], phoneNum=manicurists[0][3], images=images,
                                       message=message,
                                       rate=manicurists[0][9], ismani=session['isMani'])

        newManicurist.updateImage(image, URL)
        images = newManicurist.getMyImages()
        return render_template('business_edit.html', services=users_list, name=manicurists[0][1],
                               aboutMe=manicurists[0][8], phoneNum=manicurists[0][3], images=images,
                               rate=manicurists[0][9], ismani=session['isMani'])
    return render_template('business_edit.html', services=users_list, name=manicurists[0][1],
                           aboutMe=manicurists[0][8], phoneNum=manicurists[0][3], images=images, message=message,
                           rate=manicurists[0][9], ismani=session['isMani'])


@business_profile.route('/pic4', methods=['get', 'post'])
def changepic4():
    URL = request.args['pic4']
    email = session['email']
    newManicurist = manicurist(email, FirstName='', LastName='', PhoneNumber='', password='', businessName='',
                               x_location='', y_location='',city='')
    users_list = newManicurist.getServices()
    manicurists = newManicurist.getMyDetails()
    images = newManicurist.getMyImages()
    message = "no pic was chosen please try again"
    if URL != '':
        image = images[3][0]
        for i in images:
            if i[0] == URL:
                message = "The picture is already exist"
                return render_template('business_edit.html', services=users_list, name=manicurists[0][1],
                                       aboutMe=manicurists[0][8], phoneNum=manicurists[0][3], images=images,
                                       message=message,
                                       rate=manicurists[0][9], ismani=session['isMani'])

        newManicurist.updateImage(image, URL)
        images = newManicurist.getMyImages()
        return render_template('business_edit.html', services=users_list, name=manicurists[0][1],
                               aboutMe=manicurists[0][8], phoneNum=manicurists[0][3], images=images,
                               rate=manicurists[0][9], ismani=session['isMani'])
    return render_template('business_edit.html', services=users_list, name=manicurists[0][1],
                           aboutMe=manicurists[0][8], phoneNum=manicurists[0][3], images=images, message=message,
                           rate=manicurists[0][9], ismani=session['isMani'])


@business_profile.route('/business_edit_service/<line>', methods=['get', 'post'])
def def_business_edit_service(line):
    duplicate = False
    email = session['email']
    service = "service" + line
    current = "currentService" + line
    price = "price" + line
    newCurrent = request.form[current]
    newService = request.form[service]
    newPrice = request.form[price]
    newManicurist = manicurist(email, FirstName='', LastName='', PhoneNumber='', password='', businessName='',
                               x_location='', y_location='',city='')
    currentServices = newManicurist.getServices()
    for service in currentServices:
        if service.serviceName == newService:
            duplicate = True
    if newService != '':
        if newPrice == '':
            if duplicate == False:  # update new service
                newManicurist.updateServiceName(newService, email, newCurrent)
                message = "service name successfully updated"
            else:
                message = "service name already exist"
    if newService == '':
        if newPrice != '':
            newManicurist.updateServicePrice(newPrice, email, newCurrent)
            message = "service price successfully updated"
    if newService != '':
        if newPrice != '':
            if duplicate == False:
                newManicurist.updateNamePrice(newService, newPrice, email, newCurrent)
                message = "service successfully updated"
            else:
                message = "service name already exist"
    currentServices = newManicurist.getServices()
    manicurists = newManicurist.getMyDetails()
    images = newManicurist.getMyImages()
    return render_template('business_edit.html', services=currentServices, name=manicurists[0][1],
                           aboutMe=manicurists[0][8], phoneNum=manicurists[0][3], images=images, message=message,
                           rate=manicurists[0][9], ismani=session['isMani'])

@business_profile.route('/business_delete_service/<line>', methods=['get', 'post'])
def def_business_Delete_service(line):
    duplicate = False
    email = session['email']
    service = "service" + line
    current = "currentService" + line
    price = "price" + line
    DeleteSer = request.form['serviceName']
    newManicurist = manicurist(email, FirstName='', LastName='', PhoneNumber='', password='', businessName='',
                               x_location='', y_location='',city='')
    newManicurist.DeleteService(DeleteSer, email)
    message = "service successfully Deleted"
    currentServices = newManicurist.getServices()
    manicurists = newManicurist.getMyDetails()
    images = newManicurist.getMyImages()
    return render_template('business_edit.html', services=currentServices, name=manicurists[0][1],
                           aboutMe=manicurists[0][8], phoneNum=manicurists[0][3], images=images, message=message,
                           rate=manicurists[0][9], ismani=session['isMani'])

@business_profile.route('/rating')
def def_rating():
    newrate = request.args['Rate']
    email = session['email']
    s = Rate(session['currentMani'], email, newrate)
    s.add_rate()
    emailm=session['currentMani']
    newManicurist = manicurist(emailm, FirstName='', LastName='', PhoneNumber='', password='', businessName='',
                               x_location='', y_location='',city='')
    currentServices = newManicurist.getServices()
    manicurists = newManicurist.getMyDetails()
    images = newManicurist.getMyImages()
    city= newManicurist.getCity()
    return render_template('business_profile.html', services=currentServices, name=manicurists[0][1],
                           aboutMe=manicurists[0][8], phoneNum=manicurists[0][3], images=images,
                           rate=manicurists[0][9], ismani=session['isMani'],city=city)
