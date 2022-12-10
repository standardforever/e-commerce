from flask import render_template, url_for, flash, request, redirect, session, current_app
from .models import Brand, Category, Addproduct
from shop import app, db, photos
from .forms import Addproducts
import secrets, os

@app.route('/')
def home():
    """Home page"""
    page = request.args.get('page', 1, type=int)
    products = Addproduct.query.filter(Addproduct.stock > 0).paginate(page=page, per_page=8)
    brands = Brand.query.join(Addproduct, (Brand.id == Addproduct.brand_id)).all()
    categories = Category.query.join(Addproduct, (Category.id == Addproduct.category_id)).all()
    return render_template('products/index.html', products=products, brands=brands, categories=categories)


@app.route('/categories/<int:id>')
def get_category(id):
    """Get Category by id in database """
    get_cat_prod = Addproduct.query.filter_by(category_id=id)
    categories = Category.query.join(Addproduct, (Category.id == Addproduct.category_id)).all()
    brands = Brand.query.join(Addproduct, (Brand.id == Addproduct.brand_id)).all()
    return render_template('products/index.html', get_cat_prod=get_cat_prod, categories=categories, brands=brands)



@app.route('/addcat', methods=["POST", "GET"])
def addcat():
    """Add New category to the database"""

    if request.method == 'POST':
        getcategory = request.form.get('category')
        cat = Category(name=getcategory)
        db.session.add(cat)
        flash(f'The Brand {getcategory} was added to your database', 'success')
        db.session.commit()
        return redirect(url_for('addbrand'))

    return (render_template('products/addbrand.html'))


# @app.route('/updatecat/<int:id>', methods=['GET', 'POST'])
# def updatecat(id):
#     """Update category in the database"""

#     if 'email' not in db.session:
#         flash(f'please login first', 'danger')
#         updatecat = Category.query.get_or_404(id)
#         category = request.form.get('category')
#         if request.method == "POST":
#             updatecat.name = category
#             flash(f'Your category has been updated', 'success')
#             db.session.commit()
#             return(redirect(url_for('category')))
#         return render_template('products/updatebrand.html', title='Update Category Page', updatecat=updatecat)


@app.route('/updatecategory/<int:id>', methods=["POST", "GET"])
def updatecategory(id):
    """Update category in the database"""

    if 'email' not in session:
        flash(f'Please login first', 'danger')
        return redirect(url_for('login'))
    updatecat = Category.query.get_or_404(id)
    category = request.form.get('category')

    if request.method == 'POST':
        updatecat.name = category
        flash(f'Your category has been updated', 'success')
        db.session.commit()
        return redirect(url_for('category'))
    return render_template('products/updatebrand.html', title='Update category page', updatecategory=updatecat)



@app.route('/deletecategory/<int:id>', methods=['POST'])
def deletecategory(id):
    """Delete category from the database"""

    if 'email' not in session:
        flash(f'Please login')
        return redirect(url_for('login'))
    category = Category.query.get_or_404(id)

    if request.method == 'POST':
        db.session.delete(category)
        db.session.commit()
        flash(f'The category {category.name} was deleted from your database', 'success')
        return redirect(url_for('admin'))
    flash(f'The category {category.name} can\'t be deleted', 'warning')
    return redirect(url_for("admin"))



@app.route('/brand/<int:id>')
def get_brand(id):
    """Get brand by id in database """
    brand = Addproduct.query.filter_by(brand_id=id)
    brands = Brand.query.join(Addproduct, (Brand.id == Addproduct.brand_id)).all()
    categories = Category.query.join(Addproduct, (Category.id == Addproduct.category_id)).all()
    return render_template('products/index.html', brand=brand, brands=brands, categories=categories)


@app.route('/addbrand', methods=["POST", "GET"])
def addbrand():
    """Add New brand to the database"""

    if request.method == "POST":
        getbrand = request.form.get('brand')
        brand = Brand(name=getbrand)
        db.session.add(brand)
        flash(f"The Brand {getbrand} was added to your database", 'success')
        db.session.commit()
        return redirect(url_for('addbrand'))

    return (render_template('products/addbrand.html', brands='brand'))


@app.route('/updatebrand/<int:id>', methods=["POST", "GET"])
def updatebrand(id):
    """Update brand in the database"""

    if 'email' not in session:
        flash(f'Please login first', 'danger')
        return redirect(url_for('login'))
    updatebrand = Brand.query.get_or_404(id)
    
    brand = request.form.get('brand')
    if request.method == 'POST':
        updatebrand.name = brand
        flash(f'Your brand has been updated', 'success')
        db.session.commit()
        return redirect(url_for('brands'))
    return render_template('products/updatebrand.html', title="Update brand page", updatebrand=updatebrand)


@app.route('/deletebrand/<int:id>', methods=["POST"])
def deletebrand(id):
    """Delete brand in the database"""

    if 'email' not in session:
        flash(f'Please login', 'danger')
        return redirect(url_for('login'))

    brand = Brand.query.get_or_404(id)
    if request.method == "POST":
        db.session.delete(brand)
        db.session.commit()
        flash(f'The brand {brand.name} was deleted from your database', 'success')
        return redirect(url_for('admin'))
    flash(f'The brand {brand.name} can\'t be deleted', 'warning')
    return redirect(url_for("admin"))
    

@app.route('/addproduct', methods=['POST', 'GET'])
def addproduct():
    """Add product to the database"""

    brands = Brand.query.all()
    categories = Category.query.all()
    form = Addproducts(request.form)
    if request.method == 'POST':
        name = form.name.data
        price = int(form.price.data)
        discount = form.discount.data
        stock = form.stock.data
        colors = form.colors.data
        desc = form.discription.data
        brand = request.form.get('brand')
        category = request.form.get('category')
        image_1 = photos.save(request.files.get('image_1'), name=secrets.token_hex(10) + ".")
        image_2 = photos.save(request.files.get('image_2'), name=secrets.token_hex(10) + ".")
        image_3 = photos.save(request.files.get('image_3'), name=secrets.token_hex(10) + ".")
        addpro = Addproduct(name=name, price=price, discount=discount,stock=stock, colors=colors, desc=desc, brand_id=brand, 
                        category_id=category, image_1=image_1, image_2=image_2, image_3=image_3)

        db.session.add(addpro)
        flash(f'The product {name} has been added to your database', 'success')
        db.session.commit()
        return redirect(url_for('admin'))
    return render_template('products/addproduct.html', title="Add Product page", form=form, brands=brands,
                            categories=categories)


@app.route('/updateproduct/<int:id>', methods=["POST", "GET"])
def updateproduct(id):
    """Update product in the database"""
    
    if 'email' not in session:
        flash(f'Please login first', 'danger')
        redirect(url_for('login'))
    brands = Brand.query.all()
    categories = Category.query.all()
    form = Addproducts(request.form)
    product = Addproduct.query.get_or_404(id)
    brand = request.form.get('brand')
    category = request.form.get('category')

    if request.method == 'POST':
        product.name = form.name.data
        product.price = form.price.data
        product.discount = form.discount.data
        product.brand_id = brand
        product.category_id = category
        product.colors = form.colors.data
        product.desc = form.discription.data
        if request.files.get("image_1"):
            try:
                os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_1))
                product.image_1 = photos.save(request.files.get('image_1'), name=secrets.token_hex(10) + ".")
            except:
                product.image_1 = photos.save(request.files.get('image_1'), name=secrets.token_hex(10) + ".")

        if request.files.get("image_2"):
            try:
                os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_2))
                product.image_2 = photos.save(request.files.get('image_2'), name=secrets.token_hex(10) + ".")
            except:
                product.image_2 = photos.save(request.files.get('image_2'), name=secrets.token_hex(10) + ".")
        
        if request.files.get("image_3"):
            try:
                os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_3))
                product.image_3 = photos.save(request.files.get('image_3'), name=secrets.token_hex(10) + ".")
            except:
                product.image_3 = photos.save(request.files.get('image_3'), name=secrets.token_hex(10) + ".")

        db.session.commit()
        flash(f'Your product has been updated', 'success')
        return redirect(url_for('admin'))


    form.name.data = product.name
    form.price.data = product.price
    form.discount.data = product.discount
    form.stock.data = product.stock
    form.colors.data = product.colors
    form.discription.data = product.desc
    
    return render_template('products/updateproduct.html', form=form, categories=categories, brands=brands,
                        product=product)


@app.route('/deleteproduct/<int:id>', methods=['POST'])
def deleteproduct(id):
    """Delete Product from database"""
    if 'email' not in session:
        flash(f'Please login')
        return redirect(url_for('login'))
    
    product = Addproduct.query.get_or_404(id)

    if request.method == 'POST':
        try:
            os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_2))
        except:
            pass
        try:
            os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_2))
        except:
            pass
        try:
            os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_3))
        except:
            pass
        
        db.session.delete(product)
        db.session.commit()
        flash(f'The product {product.name} was deleted from your database', 'success')
        return redirect(url_for('admin'))
    flash(f'The product {product.name} can\'t be deleted', 'warning')
    return redirect(url_for("admin"))
