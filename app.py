from flask import Flask, render_template , session, redirect, url_for, g, request
from database import get_db, close_db
from forms import RegistrationForm, LoginForm, addItem, ChangePassword,ReplyForm, SearchUserForm, QuantityForm, SearchForm,CheckOut, IncrementForm, CheckOut, ReviewForm, addColorForm, addressForm, updateForm
from werkzeug.security import generate_password_hash, check_password_hash
import os 
from functools  import wraps

app = Flask(__name__)
app.config["SECRET_KEY"] = "thisISMySecrettKey"
app.teardown_appcontext(close_db)
app.config["UPLOAD_FOLDER"] = "static/images"

@app.before_request
def load_logged_in_user():
    
    if "currency" not in session:
        session["currency"] = 1.0
    if "privacy" not in session:
        session["Privacy"] = "Public"
    if "address" not in session:
        db = get_db()
        user = session.get("user_name")
        if db.execute("""SELECT * FROM users WHERE user_name = ?""",(user,)).fetchone():
            session["address"] = dict(db.execute("""SELECT * FROM users WHERE user_name = ?""",(user,)).fetchone())
    g.user = session.get("user_name")
    g.price = session.get("currency")
    g.mode = session.get("mode")
    g.privacy = session.get("Privacy")
    g.sform = SearchForm()
    g.aform = addressForm()
    g.address = session.get("address")


def login_required(view):
    @wraps(view)
    def wrapped_view(*args, ** kwargs):
        if g.user is None:
            return redirect(url_for("login", next = request.url))
        return view(*args, **kwargs)
    return wrapped_view


def admin_required(view):
    @wraps(view)
    def wrapped_view(*args, ** kwargs):
        if g.user != "admin":
            return redirect(url_for("login", next = request.url))
        return view(*args, **kwargs)
    return wrapped_view


@app.route("/", methods=["GET","POST"])
def index():
    
    db = get_db()
    homeProducts = db.execute("""SELECT * FROM products;""").fetchall()
    return render_template("index.html", homeProducts= homeProducts, user=g.user, sform=g.sform)

@app.route("/category/<categoryType>", methods=["GET","POST"])
def category(categoryType):
    db = get_db()
    if categoryType == "Clothing":
        homeProducts = db.execute("""SELECT * 
                                  FROM products 
                                  WHERE category is ? 
                                  or category is ? 
                                  or category is ? 
                                  or category is ? ;""",("Dry Suits","Wet Suits","Buoyancy Aid", "Shoes"))
    else:
        homeProducts = db.execute("""SELECT * 
                                  FROM products 
                                  WHERE category is ? ;""",(categoryType,))
    return render_template("index.html", homeProducts= homeProducts, user=g.user, sform=g.sform)
@app.route("/brand/<brandType>", methods=["GET","POST"])
def brand(brandType):
    db = get_db()
    homeProducts = db.execute("""SELECT * FROM products WHERE brand is ? ;""",(brandType,))
    return render_template("index.html", homeProducts= homeProducts, user=g.user, sform=g.sform)

@app.route("/product/<int:productId>")
def product(productId):
    rForm = ReviewForm()
    form = QuantityForm()
    db = get_db()
    rating = db.execute("""SELECT rating 
                        FROM reviews 
                        WHERE product_id = ?;""", (productId, )).fetchall()
    colors = db.execute("""SELECT Distinct color 
                        FROM productsSize 
                        WHERE product_id = ?;""", (productId, )).fetchall()
    sizes = db.execute("""SELECT *
                        FROM productsSize 
                       WHERE product_id = ?;""", (productId, )).fetchall()
    counter = 0
    ratingAdv = 0
   
    if rating != []:
        for rate in rating:
            counter +=1
            ratingAdv += float(rate["rating"])
        ratingAdv = ratingAdv / counter
    print(rating)
    product = db.execute("""SELECT * 
                         FROM products 
                         WHERE id = ?;""", (productId, )).fetchone()
    image = product["image"]
    reviews = db.execute("""SELECT * 
                         FROM reviews 
                         WHERE product_id = ?; """,(productId, )).fetchall() 
    reply = db.execute("""SELECT * 
                       FROM reviewsReply; """,).fetchall() 
                       
    return render_template("product.html", product=product, user=g.user, form=form,image=image, sform=g.sform, rForm = rForm,reviews=reviews, reply = reply, ratingAdv=ratingAdv, colors = colors, active="", sizes=sizes)


@app.route("/product/<int:productId>/<color>")
def productColor(productId,color):
    rForm = ReviewForm()
    form = QuantityForm()
    db = get_db()
    product = db.execute("""SELECT * 
                         FROM products 
                         WHERE id = ?;""", (productId, )).fetchone()
    rating = db.execute("""SELECT rating 
                        FROM reviews 
                        WHERE product_id = ?;""", (productId, )).fetchall()
    colors = db.execute("""SELECT Distinct color 
                        FROM productsSize 
                        WHERE product_id = ?;""", (productId, )).fetchall()
    sizes = db.execute("""SELECT * 
                       FROM productsSize 
                       WHERE product_id = ?;""", (productId, )).fetchall()
    images = db.execute("""SELECT image 
                        FROM productsSize 
                        WHERE product_id = ? 
                        and color = ?;""", (productId,color )).fetchall()
    counter = 0
    ratingAdv = 0
    image = product["image"]
    for image in images:
        if image["image"] is not None:
            image = image["image"]
            break
        else:
            print ("image is none")
            image = product["image"]
    if rating != []:
        for rate in rating:
            counter +=1
            ratingAdv += float(rate["rating"])
        ratingAdv = ratingAdv / counter
    print(rating)
    reviews = db.execute("""SELECT * 
                         FROM reviews 
                         WHERE product_id = ?; """,(productId, )).fetchall() 
    reply = db.execute("""SELECT * 
                       FROM reviewsReply; """,).fetchall() 
    return render_template("product.html", product=product, user=g.user, form=form, sform=g.sform, rForm = rForm,reviews=reviews, reply = reply, ratingAdv=ratingAdv, colors = colors,image = image, active=color, sizes=sizes, selectedColor=color)

@app.route("/product/<int:productId>/<color>/<size>")
def productSize(productId,color,size):
    rForm = ReviewForm()
    form = QuantityForm()
    db = get_db()
    stock = db.execute("""SELECT stock 
                       FROM productsSize 
                       WHERE product_id = ?  
                       AND color = ? 
                       and size = ?; """,(productId,color, size )).fetchone()
    stock = stock["stock"]
    print(stock)
    if stock > 10:
        for i in range(10):
            i += 1
            form.quantity.choices.append(i)
            
    else:
        for s in range(stock):
            s += 1
            form.quantity.choices.append(s)
           
    
    sizes = db.execute("""SELECT * 
                       FROM productsSize 
                       WHERE product_id = ?;""", (productId, )).fetchall()
    rating = db.execute("""SELECT rating 
                        FROM reviews 
                        WHERE product_id = ?;""", (productId, )).fetchall()
    colors = db.execute("""SELECT Distinct color
                         FROM productsSize 
                        WHERE product_id = ?;""", (productId, )).fetchall()
    images = db.execute("""SELECT image FROM productsSize WHERE product_id = ? and color = ?;""", (productId,color )).fetchall()
    product = db.execute("""SELECT * FROM products WHERE id = ?;""", (productId, )).fetchone()
    counter = 0
    stock = db.execute("""SELECT stock 
                       FROM productsSize 
                       WHERE product_id = ? 
                       AND color = ? 
                       AND size = ?;""", (productId,color,size )).fetchone()
    stock = stock["stock"]
    ratingAdv = 0
    image = product["image"]
    for image in images:
        if image["image"] is not None:
            image = image["image"]
            break
        else:
            image = product["image"]
    if rating != []:
        for rate in rating:
            counter +=1
            ratingAdv += float(rate["rating"])
        ratingAdv = ratingAdv / counter
    print(rating)
    
    reviews = db.execute("""SELECT * 
                         FROM reviews 
                         WHERE product_id = ?; """,(productId, )).fetchall() 
    reply = db.execute("""SELECT * 
                       FROM reviewsReply; """,).fetchall() 
    return render_template("product.html", product=product, user=g.user, form=form, sform=g.sform, rForm = rForm,reviews=reviews, reply = reply, ratingAdv=ratingAdv, colors = colors,active=color, active1=size, size = size,sizes=sizes, image=image,selectedColor=color, selectedSize=size,stock=stock)



@app.route("/reviews/<int:productId>",  methods=["GET","POST"])
@login_required
def reviews(productId):
    rForm = ReviewForm()
    db= get_db()
    rating = rForm.rating.data
    review = rForm.review.data
    image = rForm.image.data
    if image:
        filename = image.filename
        image.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'], filename)) 
        db.execute("""INSERT INTO reviews (product_id,user_id,rating,image,review ) VALUES (?,?,?,?,?);""", (productId, g.user,rating,filename,review))
    else:
        db.execute("""INSERT INTO reviews (product_id,user_id,rating,review ) VALUES (?,?,?,?);""", (productId, g.user,rating,review))
    db.commit()
    return redirect(url_for("product",productId=productId))
    
@app.route("/deleteReview/<int:reviewId>/<int:productId>", methods=["GET","POST"])
@login_required
def deleteReview(reviewId,productId):
    db = get_db()
    db.execute("""DELETE FROM reviews 
               WHERE id = ? """,(reviewId,))
    db.execute("""DELETE FROM reviewsReply 
               WHERE reviewId = ? """,(reviewId,))
    db.commit()
    return redirect(url_for("product",productId=productId))
@app.route("/deleteReply/<int:reviewId>/<int:productId>", methods=["GET","POST"])
@login_required
def deleteReply(reviewId,productId):
    db = get_db()
    db.execute("""DELETE FROM reviewsReply 
               WHERE id = ? """,(reviewId,))
    db.commit()
    return redirect(url_for("product",productId=productId))

@app.route("/reviewsReply/<int:productId>/<int:reviewId>",  methods=["GET","POST"])
@login_required
def reviewsReply(productId,reviewId):
    db = get_db()
    rForm = ReplyForm()
    reviews = db.execute("""SELECT * 
                         FROM reviews 
                         WHERE product_id = ?; """,(productId, )).fetchone()
    if rForm.validate_on_submit():
        review = rForm.review.data
        db.execute("""INSERT INTO reviewsReply (reviewId,product_id,rUser_id,rReview ) VALUES (?,?,?,?);""", (reviewId,productId, g.user,review))
        db.commit()
        return redirect(url_for("product",productId=productId))
    return render_template("reviewReply.html", user=g.user, sform=g.sform, rForm = rForm, reviews=reviews)

@app.route("/search", methods=["GET","POST"])
def search():
    db = get_db()
    form = SearchForm()
    query = f"%{form.search.data}%"
    
    product = db.execute("""SELECT * 
                         FROM products 
                         WHERE product LIKE ? 
                         or brand LIKE ?;""", (query,query)).fetchall()
    query = form.search.data

    return render_template("index.html", homeProducts=product, user=g.user,sform=g.sform , query = query)

@app.route("/cart", methods=["GET","POST"])
@login_required
def cart():
    form = CheckOut()
    iform = IncrementForm()
    if "cart" not in session:
        session["cart"] = {}      
        session.modified = True
    items = []
    db = get_db()
    for key in session["cart"]:
        item = session["cart"][key]
        row = db.execute("""SELECT stock 
                         FROM productsSize 
                         WHERE product_id = ? 
                         AND color = ? 
                         and size = ?; """,(item["productId"],item["color"], item["size"] )).fetchone()
        if row:
            stock=row["stock"]
            if stock < item["quantity"]:
                session["cart"][key]["quantity"] = stock
        items.append(item)
    return render_template("cart.html", user=g.user, sform=g.sform, form=form , iform=iform, items = items)



@app.route("/add_to_cart/<int:productId>/<color>/<size>",methods=["GET","POST"])
@login_required
def add_to_cart(productId,color,size):
    if "cart" not in session:
            session["cart"] = {}
    form = QuantityForm()
    key = f"{productId}{color}{size}"
    db = get_db()
    name = db.execute("""SELECT * FROM products WHERE id = ?; """,(productId, )).fetchone()
    print(form.errors)
    stock = db.execute("""SELECT stock 
                       FROM productsSize 
                       WHERE product_id = ? 
                       AND color = ? 
                       and size = ?; """,(productId,color, size )).fetchone()
    stock = stock["stock"]
    if stock > 10:
        for i in range(10):
            i += 1
            form.quantity.choices.append(i)
            
    else:
        for s in range(stock):
            s += 1
            form.quantity.choices.append(s)
           
    print(f"Form data: {request.form}")
    if form.validate_on_submit():
        if key not in session["cart"]:
            session["cart"][key] = {
                "productId": productId,
                "productName": name["product"],
                "color": color,
                "size": size,
                "price": name["price"],
                "quantity":int(form.quantity.data) 
            }
            session.modified = True
            
        else:
            session["cart"][key]["quantity"] +=  float(form.quantity.data)
            session.modified = True
 
    return redirect(url_for("cart"))
@app.route("/inc/<int:productId>",methods=["GET","POST"])
@login_required
def inc(productId):
    productId = str(productId)
    if productId in session["cart"]:
        session["cart"][productId] =  float(session["cart"][productId]) +1  
    else:
        session["cart"][productId] = 1 
    session.modified = True

    return redirect(url_for("cart"))
@app.route("/dec/<int:productId>",methods=["GET","POST"])
@login_required
def dec(productId):
    productId = str(productId)
    if productId in session["cart"]:
        session["cart"][productId] =  float(session["cart"][productId]) - 1  
    else:
        session["cart"][productId] = 1 
    session.modified = True

    return redirect(url_for("cart"))








@app.route("/register", methods=["GET","POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user_name = form.user_name.data
        password = form.password.data
        db = get_db()
        clash = db.execute("""SELECT * 
                           FROM users 
                           WHERE user_name = ?;""",(user_name,)).fetchone()

        if clash is not None:
            form.user_name.errors.append("User id already taken")
        else:
            db.execute("""INSERT INTO users (user_name, password) VALUES (?,?);""", (user_name, generate_password_hash(password)))
            db.commit()
            return redirect(url_for("login"))
    return render_template("registration.html", form = form, user=g.user, sform=g.sform)

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user_name = form.user_name.data
        password = form.password.data
        db = get_db()
        user_in_db = db.execute("""SELECT * 
                                FROM users 
                                WHERE user_name = ?;""", (user_name,)).fetchone()
        if user_in_db is None:
            form.user_name.errors.append("NO such user name!")
        elif not check_password_hash(
            user_in_db["password"], password):
            form.password.errors.append("Incorrect password!")
        else:
            session.clear()
            session["user_name"] = user_name
            session.modified = True
            next_page= request.args.get("next")
            if not next_page:
                next_page = url_for("index")
            return redirect(next_page)
    return render_template("login.html", form=form, user=g.user, sform=g.sform)        

@app.route("/address", methods=["GET","POST"])
@login_required
def address(): 
    aform = addressForm()
    form = ChangePassword()
    db = get_db()
    if aform.validate_on_submit():
        firstName = aform.firstName.data
        lastName = aform.lastName.data
        address1 = aform.address1.data
        address2 = aform.address2.data
        address3 = aform.address3.data
        postCode = aform.postCode.data
        db.execute("""UPDATE users 
                   SET firstName = ?, 
                   lastName = ?, 
                   address1 = ?, 
                   address2 = ?, 
                   address3 = ?, 
                   postCode = ? 
                   WHERE user_name = ?;""",(firstName,lastName,address1,address2,address3,postCode,g.user))
        db.commit()
        if session["lastPage"][0] == 'product':
            return redirect(url_for(session["lastPage"][0],productId = session["lastPage"][1],color=session["lastPage"][2],size = session["lastPage"][3]))

        return redirect(url_for('index'))
    return render_template("changepassword.html",form = form, user=g.user,aform=aform, sform=g.sform)

@app.route("/logout")
def logout():
    session.clear()
    session.modified = True
    return redirect(url_for("index"))
@app.route("/mode/<type>", methods=["GET","POST"])
def mode(type):
    session["mode"] = type
    session.modified = True
    next_page= request.referrer
    return redirect(next_page)


@app.route("/currency/<type>", methods=["GET","POST"])
def currency(type):
    if type == "euro":
        currency = 1
    elif type == "dollar":
        currency = 1.2
    elif type == "pound":
        currency = 0.8
    session["currency"] =  currency
    session.modified = True
    next_page= request.referrer
    return redirect(next_page)
   
@app.route("/account", methods=["GET","POST"])
@login_required
def account():
    return render_template("account.html", user=g.user,sform=g.sform)

@app.route("/changepassword", methods=["GET","POST"])
def changepassword():
    form = ChangePassword()
    aform = addressForm()
    db = get_db()
    user = db.execute("""SELECT * 
                       FROM users 
                       WHERE user_name = ?;""",(g.user,)).fetchone()
    aform.firstName.data = user["firstName"]
    aform.lastName.data = user["lastName"]
    aform.address1.data = user["address1"]
    aform.address2.data = user["address2"]
    aform.address3.data= user["address3"]
    aform.postCode.data= user["postCode"]
    if form.validate_on_submit():
        user_name = g.user
        password = form.password.data
        
        clash = db.execute("""SELECT * 
                           FROM users 
                           WHERE user_name = ? 
                           and password = ?;""",(user_name,password)).fetchone()

        if clash is not None:
            form.password.errors.append("Same password")
        else:
            db.execute("""UPDATE users 
                       SET password = ? 
                       WHERE user_name = ?;""", (generate_password_hash(password),user_name))
            db.commit()
            return redirect(url_for("login"))
    return render_template("changepassword.html", form = form, user=g.user, sform=g.sform, aform =aform)

@app.route("/add", methods=["GET","POST"])
@admin_required
def add():
    form = addItem()
    db = get_db()
    if form.validate_on_submit(): 
        product = form.product.data
        description =form.description.data
        price  = form.price.data
        stock = form.stock.data
        size = form.size.data
        category = form.category.data
        color = form.color.data
        brand = form.brand.data
        image = form.image.data
        filename = image.filename
        image.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'], filename)) 
        db = get_db()
        clash = db.execute("""SELECT * 
                           FROM products 
                           WHERE product =? 
                           ;""",(product,)).fetchone()
        if clash is  None:
            db.execute("""INSERT INTO products (product,description,price, brand, image, category) VALUES (?,?,?,?,?,?);""",(product,description,price, brand, filename, category))
            db.commit()
            id = db.execute("""SELECT id FROM products WHERE product =?;""",(product,)).fetchone()
            db.execute("""INSERT INTO productsSize (product_id,size,color,stock,image) VALUES (?,?,?,?,?);""",(id["id"],size,color,stock,filename))
            db.commit()
        return redirect(url_for("product",productId=id["id"]))
    return render_template("addItem.html", form = form, user=g.user, sform=g.sform)

@app.route("/addColor/<int:productId>", methods=["GET","POST"])
@admin_required
def addColor(productId):
    form = addColorForm()
    db = get_db()
    if form.validate_on_submit():
        color = form.color.data
        size = form.size.data
        stock = form.stock.data
        image = form.image.data
        clash = db.execute("""SELECT * 
                           FROM productsSize 
                           WHERE product_id =? 
                           AND size = ?
                            AND color = ?;""",(productId,size,color)).fetchone()
        if clash is not None:
            db.execute("""UPDATE productsSize 
                       SET stock = stock + ? 
                       WHERE product_id = ? 
                       AND size = ? 
                       AND color = ?;""",(stock,productId, size,color))
            db.commit()
        else:
            if image:
                filename = image.filename
                image.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'], filename)) 
                db.execute("""INSERT INTO productsSize (product_id,size,color,stock,image) VALUES (?,?,?,?,?);""",(productId,size,color,stock,filename))
                db.commit()
            else:
                db.execute("""INSERT INTO productsSize (product_id,size,color,stock) VALUES (?,?,?,?);""",(productId,size,color,stock))
                db.commit()
        return redirect(url_for('product', productId=productId))
    return render_template("addColor.html", form = form, user=g.user, sform=g.sform)

@app.route("/deleteColor/<int:productId>/<color>/", methods=["GET","POST"])
@login_required
def deleteColor(productId,color):
    db = get_db()
    db.execute("""DELETE FROM productsSize 
               WHERE product_id = ?
               AND color = ?  """,(productId,color))
    db.commit()
    next_page= request.referrer
    return redirect(next_page)

@app.route("/deleteSize/<int:productId>/<color>/<size>", methods=["GET","POST"])
@login_required
def deleteSize(productId,color, size):
    db = get_db()
    db.execute("""DELETE FROM productsSize 
               WHERE product_id = ?
               AND color = ?
               AND size = ?  """,(productId,color, size))
    db.commit()
    return redirect(url_for("product",productId = productId))

@app.route("/delete/<int:productId>", methods=["GET","POST"])
@login_required
def delete(productId):
    db = get_db()
    db.execute("""DELETE FROM products WHERE id = ? """,(productId,))
    db.execute("""DELETE FROM productsSize WHERE product_id = ? """,(productId,))
    db.execute("""DELETE FROM reviews WHERE product_id = ? """,(productId,))
    db.execute("""DELETE FROM reviewsReply WHERE product_id = ? """,(productId,))
    db.commit()
    next_page= request.referrer
    return redirect(next_page)


@app.route("/update/<int:productId>", methods=["GET","POST"])
@login_required
def update(productId):
    db = get_db()
    products = db.execute("""SELECT *
                           FROM products
                           WHERE ID =? ;""",(productId,)).fetchone()
    form = updateForm()
    form.product.data = products["product"]
    form.description.data = products["description"]
    form.price.data = products["price"]
    form.category.data = products["category"]
    form.brand.data = products["brand"]
    if form.validate_on_submit():
        product = form.product.data
        description =form.description.data
        price  = form.price.data
        category = form.category.data
        brand = form.brand.data
        image = form.image.data
        if image:
            filename = image.filename
            image.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'], filename)) 
            db = get_db()
            db.execute("""UPDATE products SET product = ?,
                                        description= ?,
                                        price = ?,
                                        brand = ?,
                                        image = ?,
                                        category = ?
                                        WHERE id = ?;""",(product,description,price, brand, filename, category,productId))
            db.commit()
        else:
            db = get_db()
            db.execute("""UPDATE products SET product = ?,
                                        description= ?,
                                        price = ?,
                                        brand = ?,
                                        category = ?
                                        WHERE id = ?;""",(product,description,price, brand, category,productId))
            db.commit()

        return redirect(url_for("product",productId = productId))
    return render_template("updateItem.html", form = form, user=g.user, sform=g.sform)


#should break
@app.route("/checkout", methods=["GET","POST"])
@login_required
def checkout():
    form = CheckOut()
    names  = {}
    prices = {}
    db = get_db()
    if form.validate_on_submit():
        print(session["cart"])
        for key, item in session["cart"].items():
            product = item["productName"]
            id = item["productId"]
            size =item["size"]
            color = item["color"]
            quantity = item["quantity"]
            print(f"{quantity} quantity ")
            price = item["price"]
            firstName = form.firstName.data
            lastName = form.lastName.data
            address1 = form.address1.data
            address2 = form.address2.data
            address3 = form.address3.data
            postCode = form.postCode.data
            db.execute("""INSERT INTO orders (user_id,product,size,color,price, quantity, Name, address, orderDate, status) 
                       VALUES (?,?,?,?,?,?,?,?,?,?);""",(g.user,product,size,color,price, quantity,f"{firstName} {lastName}",f"{address1},{address2},{address3}, {postCode}", (""), "Order Placed")) 
            db.execute("""UPDATE productsSize
                                SET stock = stock - ?
                                WHERE product_id = ? 
                                AND color = ? 
                                AND size = ?;""",(quantity,id,color,size))
            db.execute("""DELETE FROM productsSize WHERE stock < 0;""")
            db.commit() 
        session["cart"].clear()
        session.modified = True  
        return redirect(url_for("index"))
    return render_template("checkout.html", cart=session["cart"],names = names, user=g.user, sform=g.sform, form=form , prices = prices)

@app.route("/orders", methods=["GET","POST"])
def orders():
    db = get_db()
    orders = db.execute("""SELECT * FROM orders;""").fetchall()
    usersOrders = db.execute("""SELECT * FROM orders WHERE user_id = ?;""",(g.user,)).fetchall()
    return render_template("orders.html", orders= orders, user=g.user, sform=g.sform, usersOrders=usersOrders)

@app.route("/orderStatus/<id>/<status>", methods=["GET","POST"])
def orderStatus(id,status):
    db = get_db()
    db.execute("""UPDATE orders SET status = ? WHERE id = ?;""",(status,id))
    db.commit()
    orderstatus = db.execute("""SELECT * FROM orders WHERE id = ?;""",(id,)).fetchone()
    if orderstatus["status"] == "Delivered" or orderstatus["status"] == "Cancelled":
        print("delete")
        print(id)
        db.execute("""DELETE FROM orders WHERE id = ?;""",(id,))
        db.commit()
        return redirect(url_for("orders"))
    print("not delete")
    return redirect(url_for("orders"))

@app.route("/addWishList/<int:productId>/<color>/<size>", methods=["GET","POST"])
@login_required
def addWishList(productId,color,size):
    db = get_db()
    clash = db.execute("""SELECT *  
                       FROM wish 
                       WHERE user_id = ? 
                        AND product_id = ?
                       And color = ? 
                       AND size =?;""", (g.user,productId,color,size)).fetchall()
    addressSet = db.execute("""SELECT FirstName FROM users WHERE user_name = ?;""",(g.user,)).fetchone()
    if addressSet["FirstName"] is None:
        session["lastPage"]=['product',productId,color,size]
        print("last page")
        print(session["lastPage"])
        print(session["lastPage"][2])
        return redirect(url_for("address"))
    if not clash:
        db.execute("""INSERT INTO wish (user_id,product_id,color,size,privacy)
                    VALUES (?,?,?,?,?);""",(g.user,productId,color,size,"public"))
        db.commit()
    return redirect(url_for("wishList"))

@app.route("/wishList/<privacy>", methods=["GET","POST"])
@login_required
def wishListPrivacy(privacy):
    db = get_db()
    session["Privacy"] = privacy
    session.modified = True
    inWish = db.execute("""SELECT * FROM Wish WHERE user_id = ?;""",(g.user,)).fetchone()
    if inWish["user_id"] ==g.user:
        db.execute("""UPDATE wish 
               SET privacy = ? 
               WHERE user_id = ?""",(g.privacy,g.user))
        db.commit()
    return redirect(url_for("wishList"))

@app.route("/wishlist", methods=["GET","POST"])
@login_required
def wishList():
    form = SearchUserForm()
    db = get_db()
    wishList = db.execute("""SELECT w.user_id,w.product_id, w.color,w.size,p.product, p.price  
                          FROM wish as w
                           JOIN products as p
                           ON w.product_id = p.id 
                            WHERE w.user_id = ?;""",(g.user,)).fetchall()
    users = []
    if form.validate_on_submit():
        search = f"%{form.search.data}%"
        users = db.execute("""SELECT Distinct user_id
                            FROM wish
                            WHERE user_id LIKE  ? 
                            AND privacy = ?;""", (search,"Public")).fetchall()
        print("validate")
    return render_template("wishList.html", wishList= wishList, user=g.user, sform=g.sform, form = form, users = users)

@app.route("/wishlistUser/<user_id>", methods=["GET","POST"])
@login_required
def wishListUser(user_id):
    form = SearchUserForm()
    db = get_db()
    wishList = db.execute("""SELECT w.user_id, w.product_id, w.color,w.size,p.product, p.price  FROM wish as w
                           JOIN products as p
                           ON w.product_id = p.id 
                            WHERE w.user_id = ?;""",(user_id,)).fetchall()
    users = []
    if form.validate_on_submit():
        search = f"%{form.search.data}%"
        users = db.execute("""SELECT Distinct user_id FROM wish WHERE user_id LIKE ?;""", (search,)).fetchall()
        print("validate")
    return render_template("wishList.html", wishList= wishList, user=user_id, sform=g.sform, form = form, users = users)

@app.route("/buywish/<user_id>/<product_id>/<color>/<size>", methods=["GET","POST"])
@login_required
def buywish(user_id,product_id,color,size):
    form = CheckOut()
    db = get_db()
    address = db.execute("""SELECT * FROM users WHERE user_name = ?;""",(user_id,)).fetchone()
    form.firstName.data = address["firstName"]
    form.lastName.data = address["lastName"]
    form.address1.data = address["address1"]
    form.address2.data = address["address2"]
    form.address3.data = address["address3"]
    form.postCode.data = address["postCode"]
    if form.firstName.data is None:
        return redirect(request.referrer)
    wish = True
    if form.validate_on_submit():
        db.execute("""INSERT INTO orders (user_id,product,size,color,price, quantity, Name, address,orderDate, status) VALUES (?,?,?,?,?,?,?,?,?,?);""",(user_id,product_id,size,color, "Gift",1,f"{form.firstName.data} {form.lastName.data}",f"{form.address1.data},{form.address2.data},{form.address3.data}, {form.postCode.data}",(""), "Order Placed")) 
        db.execute("""UPDATE productsSize
                            SET stock = stock -?
                            WHERE product_id = ? 
                            AND color = ? 
                            AND size = ?;""",(1,product_id,color,size))
        db.execute("""DELETE FROM productsSize WHERE stock < 0;""")
        db.execute("""DELETE FROM wish WHERE user_id = ? AND product_id = ? AND color = ? AND size = ?;""",(user_id,product_id,color,size))
        db.commit()
        return redirect(url_for("wishList"))
    return render_template("checkout.html",user=g.user, sform=g.sform, form = form, wish = wish)

@app.route("/deleteWish/<product_id>/<color>/<size>", methods=["GET","POST"])
def deleteWish(product_id,color,size):
    db = get_db()
    db.execute("""DELETE FROM wish WHERE user_id = ? AND product_id = ? AND color = ? AND size = ?;""",(g.user,product_id,color,size))
    db.commit()
    return redirect(request.referrer)