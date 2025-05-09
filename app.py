"""Main application module for Fertilizer Inventory System."""

from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = (
    'postgresql://postgres:ashritha@localhost:5432/fertlizers_db'
   )
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Item(db.Model):
    """Model for fertilizer items."""
    __tablename__ = 'fertilizers'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"<Item {self.name}>"


# Uncomment this in development to auto-create tables
# @app.before_first_request
# def create_tables():
#     """Create database tables before first request."""
#     db.create_all()


@app.route('/')
def index():
    """Display all items."""
    items = Item.query.all()
    return render_template('index.html', items=items)


@app.route('/<int:item_id>')
def get_item(item_id):
    """Display a single item by ID."""
    item = Item.query.get_or_404(item_id)
    return render_template('index.html', items=[item])


@app.route('/add_item', methods=['GET', 'POST'])
def add_item():
    """Add a new item."""
    if request.method == 'POST':
        name = request.form['name']
        quantity = request.form['quantity']
        price = request.form['price']

        new_item = Item(name=name, quantity=quantity, price=price)
        db.session.add(new_item)
        db.session.commit()

        return redirect(url_for('index'))

    return render_template('add_item.html')


@app.route('/update_item/<int:item_id>', methods=['GET', 'POST'])
def update_item(item_id):
    """Update an existing item."""
    item = Item.query.get_or_404(item_id)

    if request.method == 'POST':
        item.name = request.form['name']
        item.quantity = request.form['quantity']
        item.price = request.form['price']
        db.session.commit()

        return redirect(url_for('index'))

    return render_template('update_item.html', item=item)


@app.route('/delete_item/<int:item_id>', methods=['GET'])
def delete_item(item_id):
    """Delete an item."""
    item = Item.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()


