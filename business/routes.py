from flask import url_for, render_template, redirect, flash, session, request
from flask_login import current_user
import json

from business import app
from business.forms import LocationForm, LocationListForm, RestaurantChoiceForm, LoginForm
from business import utils
from business.zomatoAPIWrapper import ZomatoAPIWrapper


@app.route("/", methods=["GET", "POST"])
def index():
    form = LocationForm()
    session["count_tracker"] = 0
    
    if request.method=="POST" and form.validate_on_submit():
        return redirect(url_for("choose_location",
                                query=form.location.data))

    return render_template("index.html", 
                            form=form)


@app.route("/choose_location", methods=["GET", "POST"])                            
def choose_location():
    query = request.args.get("query")
    locations = utils.filter_location(query)
    
    form = LocationListForm()
    form.locations.choices = [(json.dumps(loc), loc["title"]) for loc in locations]

    if request.method=="POST" and form.validate_on_submit():
        session["first_time"] = True
        
        session["location"] = form.locations.data
        return redirect(url_for("get_restaurant"),
                                #query=form.locations.data),
                                #first_time=True), 
                        code=307)

    return render_template("choose_location.html",
                    title="Choose Location",
                    form=form)


@app.route("/get_restaurant", methods=["GET", "POST"])    
def get_restaurant():
    
    zomato = ZomatoAPIWrapper()
    
    location = utils.apply_conversion_logic(session["location"])
    
    loc_id, loc_type = location["entity_id"], location["entity_type"]
    
    location_details = zomato.get_location_details(entity_id=loc_id, entity_type=loc_type)
    restaurant_count = location_details["num_restaurant"]
    
    restaurant = utils.generate_restaurant(loc_id=loc_id,
                                            loc_type=loc_type,
                                            restaurant_count=restaurant_count)
    
    form = RestaurantChoiceForm()
    
    # if session["first_time"]:
        # flash("This is first time")
    
    session["first_time"] = False
    
    session["count_tracker"] += 1
    
    # if session["count_tracker"] == 3:
        # flash("This is your thid time! Consider registering with us.")
    
    if request.method=="POST" and form.validate_on_submit() and form.yes.data:
        flash("This is where you want to record in DB")
        return redirect(url_for("index"))
    
    return render_template("result.html",
                            restaurant=restaurant,
                            form=form)



# Not used for now as there is no DB

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)