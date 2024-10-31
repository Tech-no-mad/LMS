from datetime import date,datetime,timedelta,timezone
import os
from sqlalchemy.sql import or_
from flask import Flask, render_template, request, make_response, jsonify, send_file, send_from_directory
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager,create_access_token,jwt_required,get_jwt_identity
from prompt_toolkit import HTML
from werkzeug.utils import secure_filename
from database import db
from celery import Celery
from flask_mail import Mail,Message
from celery.schedules import crontab
from models import User,Section,EBook,Transaction,Ratings


# Initialize Flask app
app = Flask(__name__)

def make_celery(app):
    celery = Celery(
        app.import_name,
        backend='redis://localhost:6379/0',
        broker='redis://localhost:6379/0'
    )
    celery.conf.update(app.config)
    return celery

celery = make_celery(app)

CORS(app, supports_credentials=True,resources={r"/api/*": {"origins": "http://192.168.1.5:8081"}})

# Set up the base directory and the database URI
base_dir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(base_dir, 'library.db')
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['JWT_SECRET_KEY'] = 'jwt-secret'
app.config['UPLOAD_FOLDER'] = os.path.join(base_dir, 'MyBooks', 'pdf')
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'karteek.t2003@gmail.com'
app.config['MAIL_PASSWORD'] =  'cxlu aecb uzjx hqvp'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

mail = Mail(app)



@celery.task(name="send_daily_reminders")
def send_daily_reminders():
    with app.app_context():
        # Get the current date and time in IST
        current_time = datetime.now(timezone(timedelta(hours=5, minutes=30))).replace(
            hour=20, minute=0, second=0, microsecond=0
        )

        # Get all users who have not visited the app today
        users = User.query.filter(
            or_(User.login_date == None, User.login_date < current_time)
        ).all()

        # Send emails to each user
        for user in users:
            # Create the email message
            msg = Message(
                subject="Daily Reminder: Visit the App",
                sender="karteek.t2003@gmail.com",
                recipients=[user.email],
            )
            msg.body = f"Dear {user.username},\n\nPlease visit the app today to enjoy the benefits."

            # Send the email
            mail.send(msg)



@celery.task
def monthly_activity_report():
    with app.app_context():
        users = User.query.all()
        for user in users:
            if ( user.role == 'user'):
                email = user.email
                uid = user.id
                # Create the HTML report
                html_report = create_monthly_activity_report(uid)

                # Convert the HTML report to PDF
                pdf_report = convert_html_to_pdf(html_report)

                # Send the PDF report as email
                send_email_with_pdf_attachment(email, pdf_report)


def create_monthly_activity_report(uid):
    user_transactions = Transaction.query.filter_by(user_id= uid ).all()
    book_ids = [transaction.book_id for transaction in user_transactions]

   
    sections = Section.query.join(EBook, Section.sid == EBook.sectionid).filter(EBook.ebid.in_(book_ids)).all()

 
    books = EBook.query.filter(EBook.ebid.in_(book_ids)).all()


    ratings = Ratings.query.filter_by(user_id=uid).filter(Ratings.ebid.in_(book_ids)).all()

    html_report = render_template('monthly_report.html', sections=sections, books=books, ratings=ratings)

    return html_report


def convert_html_to_pdf(html_report):
    pdf_report = HTML(string=html_report).write_pdf()
    return pdf_report



def send_email_with_pdf_attachment(email, pdf_report):
    try:
        with app.app_context():
            msg = Message('Monthly Activity Report', sender=app.config['karteek.t2003@gmail.com'], recipients=[])
            msg.body = "Please find the monthly activity report attached."

            # Attach the PDF report
            msg.attach("Monthly_Activity_Report.pdf", "application/pdf", pdf_report)

            # Send the email
            mail.send(msg)
                
            return 'Email sent successfully', 200
    except Exception as e:
            return f'Error sending email: {str(e)}', 500



# Celery beat config
celery.conf.beat_schedule = {
    'send-daily-reminders-every-day-at-8pm': {
        'task': 'send_daily_reminders',
        'schedule': crontab(hour=21, minute=20, day_of_week='*'),  # 8 PM IST daily
    },
    'monthly-activity-report-on-first-day-of-month': {
        'task': 'monthly_activity_report',
        'schedule': crontab(hour=0, minute=0, day_of_month='1'),  # Midnight UTC on the 1st of every month
    },
}

celery.conf.timezone = 'Asia/Kolkata'



# Bind the SQLAlchemy object to the app
db.init_app(app)

# Initialize JWTManager with the app
jwt = JWTManager(app)

# Import models here to ensure they are known to SQLAlchemy
with app.app_context():
    
    db.create_all()

# Define the login route
#User's code
@app.route('/api/login', methods=['POST', 'OPTIONS'])
def userlogin():
    if request.method == 'OPTIONS':  # Preflight request
        # Create a response object with the necessary CORS headers
        response = make_response()
        response.headers['Access-Control-Allow-Origin'] = 'http://192.168.1.5:8081'
        response.headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        response.headers['Access-Control-Allow-Credentials'] = 'true'
        print(response)
        return response
   
   

    username = request.json.get('username', None)
    password = request.json.get('password', None)
    
    user = User.query.filter_by(username=username,password=password,role='user').first()
    if user and (password == user.password):
        access_token = create_access_token(identity=user.id)
        print('access_token :',access_token)
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({"msg": "Bad username or password"}), 401

@app.route('/api/userdashboard', methods=['GET'])
@jwt_required()
def userdashboard():
    books = EBook.query.all()
    user_id = get_jwt_identity()
    transactions = Transaction.query.filter_by(user_id=user_id).all()
    
    requested_book_ids = [transaction.book_id for transaction in transactions]
    
    available_books = [book for book in books if book.ebid not in requested_book_ids]
    
    book_data = [{
        'ebid': book.ebid,
        'title': book.title,
        'author': book.author,
        'description': book.description,
        'sectionid': book.sectionid
    } for book in available_books]

    return jsonify(books=book_data), 200


@app.route('/api/requestbook', methods=['POST'])
@jwt_required()
def request_book():
    data = request.get_json()
    user_id = get_jwt_identity()
    book_id = data.get('book_id')
    
    if not book_id:
        return jsonify({"msg": "Book ID is required"}), 400
    
    existing_transaction = Transaction.query.filter_by(user_id=user_id, book_id=book_id).first()
    if existing_transaction:
        return jsonify({"msg": "You have already requested this book."}), 400
    
    count = Transaction.query.filter_by(user_id=user_id, return_date=None).count()
    if count >= 5:
        return jsonify({"msg": "You have reached the maximum limit of 5 e-book requests."}), 400

    new_transaction = Transaction(
        borrow_date=date.today(),
        return_date=None,
        user_id=user_id,
        book_id=book_id,
        Status = 'request'
    )
    
    db.session.add(new_transaction)
    db.session.commit()
    
    return jsonify({"msg": "Book requested successfully"}), 200



@app.route('/api/mybooks', methods=['GET'])
@jwt_required()
def mybooks():
    user_id = get_jwt_identity()
    transactions = Transaction.query.filter_by(user_id=user_id).all()
    
    completed_books = []
    current_books = []

    for transaction in transactions:
        book = EBook.query.filter_by(ebid=transaction.book_id).first()  # Fetch book details
        book_info = {
            "id": transaction.book_id,
            "title": book.title,
            "author": book.author,
            "section": book.sectionid,
            "borrow_date": transaction.borrow_date,
            "return_date": transaction.return_date,
            "status": transaction.Status,
            "pdf": f'/api/pdf/{book.file}'
        }
        
        # Determine if the book is current or completed
        if transaction.Status == 'grant':
            current_books.append(book_info)
        elif transaction.Status == 'return':
            completed_books.append(book_info)

    return jsonify({
        "current_books": current_books,
        "completed_books": completed_books
    }), 200





@app.route('/api/returnbook', methods=['POST'])
@jwt_required()
def return_book():
    user_id = get_jwt_identity()
    data = request.get_json()
    book_id = data.get('book_id')

    if not book_id:
        return jsonify({"msg": "Book ID is required"}), 400

    transaction = Transaction.query.filter_by(user_id=user_id, book_id=book_id).first()
    
    if not transaction:
        return jsonify({"msg": "No active transaction found for this book."}), 404

    # Mark the transaction as completed
    transaction.return_date = datetime.now()
    transaction.Status = "return"  
    db.session.commit()

    return jsonify({"msg": "Book returned and marked as completed successfully"}), 200





@app.route('/api/addrating', methods=['POST'])
@jwt_required()
def add_rating():
    user_id = get_jwt_identity()
    data = request.get_json()
    book_id = data.get('book_id')
    rating = data.get('rating')

    if not book_id or rating is None:
        return jsonify({"msg": "Book ID and Rating are required"}), 400

    existing_rating = Ratings.query.filter_by(user_id=user_id, ebid=book_id).first()

    if existing_rating:
        existing_rating.rating = rating
    else:
        new_rating = Ratings(user_id=user_id, ebid=book_id, rating=rating)
        db.session.add(new_rating)

    db.session.commit()
    return jsonify({"msg": "Rating added successfully"}), 200

@app.route('/api/downloadpdf', methods=['GET'])
@jwt_required()
def download_pdf():
    book_id = request.args.get('book_id')
    book = EBook.query.filter_by(ebid=book_id).first()  
    if not book:
        return jsonify({"error": "Book not found"}), 404
    pdf_filename = book.file
    
    return send_from_directory(
        app.config['UPLOAD_FOLDER'], 
        f'/api/pdf/{pdf_filename}',                 
        as_attachment=True,          
        mimetype='application/pdf'    
    )



#Librarians code
@app.route('/api/liblogin', methods=['POST', 'OPTIONS','GET'])
def liblogin():
    if request.method == 'OPTIONS':  # Preflight request
        # Create a response object with the necessary CORS headers
        response = make_response()
        response.headers['Access-Control-Allow-Origin'] = 'http://192.168.1.5:8081'
        response.headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS,GET'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        response.headers['Access-Control-Allow-Credentials'] = 'true'
        print(response)
        return response   


    username = request.json.get('username', None)
    password = request.json.get('password', None)
    print(username,password)
    
    user = User.query.filter_by(username=username,password=password,role='librarian').first()
    if user and (password == user.password):
        access_token = create_access_token(identity=user.id)
        print('access_token :',access_token)


        section_data = Section.query.all()
        sections = []
        for section in section_data:
            sections.append({
                'sid': section.sid,
                'title': section.title,
                'date': section.date,
                'description': section.description
            })
            print(sections)


            books = EBook.query.all()
            book_data = []
            for book in books:
                book_data.append({
                    'ebid':book.ebid,
                    'title':book.title,
                    'author':book.author,
                    'description':book.description,
                    'date':book.date,
                    'sectionid':book.sectionid,
                    'file':book.file,
                    'quantity':book.quantity,
                     'price':book.price
                })

        


        return jsonify(access_token=access_token,sections=sections,books=book_data), 200
    else:
        return jsonify({"msg": "Bad username or password"}), 401


@app.route('/api/register', methods=['POST', 'OPTIONS'])
def register():
    if request.method == 'OPTIONS':  # Preflight request
        response = make_response()
        response.headers['Access-Control-Allow-Origin'] = 'http://192.168.1.5:8081'
        response.headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        response.headers['Access-Control-Allow-Credentials'] = 'true'
        return response

    try:
        username = request.json.get('username', None)
        password = request.json.get('password', None)
        email = request.json.get('email', None)

        if username is None or password is None:
            return jsonify({"msg": "Missing username or password"}), 400

        #hashed_password = generate_password_hash(password)
        new_user = User(username=username, password=password, email=email, role='user')

        db.session.add(new_user)
        db.session.commit()

        access_token = create_access_token(identity=new_user.id)

        return jsonify({
            "msg": "User created successfully",
            "access_token": access_token
        }), 201
    except Exception as e:
        # Log the exception for debugging purposes
        print(e)
        # Return a generic error message
        return jsonify({"msg": "An error occurred during registration"}), 500

# Make sure to handle other exceptions and errors as needed

@app.route('/api/users/<int:user_id>', methods=['DELETE', 'OPTIONS'])
@jwt_required()
def delete_user(user_id):
    if request.method == 'OPTIONS':
        # Create a response for the preflight request with the necessary headers
        response = make_response()
        response.headers['Access-Control-Allow-Origin'] = 'http://192.168.1.5:8081'
        response.headers['Access-Control-Allow-Methods'] = 'DELETE, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        response.headers['Access-Control-Allow-Credentials'] = 'true'
        return response, 200  # Make sure to return 200 OK status for preflight request
    elif request.method == 'DELETE':
        user = User.query.get(user_id)
        token = get_jwt_identity()
        print(token)
        if not user:
            return jsonify({"msg": "User not found"}), 404
        if user.id != token:
             return jsonify({"msg": "User unauthorized"}), 401
        else:
            db.session.delete(user)
            db.session.commit()
            return jsonify({"msg": "User deleted successfully"}), 200
        

@app.route('/api/update_user/<int:user_id>', methods=['PUT', 'OPTIONS'])
@jwt_required()
def update_user(user_id):
    if request.method == 'OPTIONS':
        # Create a response for the preflight request with the necessary headers
        response = make_response()
        response.headers['Access-Control-Allow-Origin'] = 'http://192.168.1.5:8081'
        response.headers['Access-Control-Allow-Methods'] = 'PUT, OPTIONS'  # Corrected to include PUT
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        response.headers['Access-Control-Allow-Credentials'] = 'true'
        return response, 200  # Make sure to return 200 OK status for preflight request
    
    elif request.method == 'PUT':
        username = request.json.get('username', None)
        email = request.json.get('email', None)
        user = User.query.get(user_id)
        token = get_jwt_identity()
        if not user:
            return jsonify({"msg": "User not found"}), 404
        
        if user.id != token:
            return jsonify({"msg": "User unauthorized"}), 401
        else:
            if username:
                user.username = username
            if email:
                user.email = email
        
            db.session.commit()
            return jsonify({"msg": "User updated successfully"}), 200  # Ensure to return 200 OK status for successful PUT request

@app.route('/api/add_section', methods=['POST','OPTIONS','GET'])
@jwt_required()
def add_section():
    print(" inside def")
    if request.method == 'OPTIONS':
        # Create a response for the preflight request with the necessary headers
        print('in options')
        response = make_response()
        response.headers['Access-Control-Allow-Origin'] = 'http://192.168.1.5:8081'
        response.headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS'  # Corrected to include PUT
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        response.headers['Access-Control-Allow-Credentials'] = 'true'
        return response, 200  # Make sure to return 200 OK status for preflight request
    
    elif request.method == 'POST':
        try:
            data = request.get_json()
            sections = []
            print("print ->",data)
            title = data.get('title')
            date_created = data.get('dateCreated')
            description = data.get('description')

            
        
            new_section = Section(title=title, date=date_created, description=description)
            db.session.add(new_section)
            db.session.commit()

            sections = Section.query.all()
            section_data = []
            for section in sections:
                section_data.append({
                    'sid': section.sid,
                    'title': section.title,
                    'date': section.date,
                    'description': section.description
                })
                print(section_data)
            return jsonify({"sections":section_data }), 201
        except Exception as e:
            # Log the exception for debugging purposes
            print(e)
            # Return an error message
            return jsonify({"msg": "Error adding section"}), 500  
        
        
@app.route('/api/edit-section', methods=['POST', 'OPTIONS'])
@jwt_required()
def edit_section():
    print("Inside the function")
    if request.method == 'OPTIONS':
        # Create a response for the preflight request with the necessary headers
        print('Handling OPTIONS request')
        response = make_response()
        print('Handling OPTIONS request1')
        response.headers['Access-Control-Allow-Origin'] = 'http://192.168.1.5:8081'
        print('Handling OPTIONS request2')
        response.headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS'  # Corrected to include PUT
        print('Handling OPTIONS request3')
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        print('Handling OPTIONS request4')
        response.headers['Access-Control-Allow-Credentials'] = 'true'
        print('Handling OPTIONS request5')
        return response, 200  # Make sure to return 200 OK status for preflight request
    
    elif request.method == 'POST':
        data = request.json
        section_id = data['sid']
        
        edit_section = Section.query.filter_by(sid = section_id).first()

        edit_section.title= data['title']
        edit_section.date = data['date']
        edit_section.description = data['description']

       

        db.session.commit()

        sections = Section.query.all()
        section_data = []
        for section in sections:
            section_data.append({
                'sid': section.sid,
                'title': section.title,
                'date': section.date,
                'description': section.description
            })
            print(section_data)
        return jsonify({"sections":section_data }), 201


@app.route('/api/delete-section', methods=['DELETE','OPTIONS','GET'])
@jwt_required()
def del_section():
    print(" inside def")
    if request.method == 'OPTIONS':
        # Create a response for the preflight request with the necessary headers
        print('in options')
        response = make_response()
        response.headers['Access-Control-Allow-Origin'] = 'http://192.168.1.5:8081'
        response.headers['Access-Control-Allow-Methods'] = 'DELETE, OPTIONS'  
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        response.headers['Access-Control-Allow-Credentials'] = 'true'
        return response, 200  # Make sure to return 200 OK status for preflight request
    
    elif request.method == 'DELETE':
        try:
            data = request.get_json()
            print('sid',data['sid'])      
           
            sid = data['sid']
            del_section = Section.query.filter_by(sid = sid).first()
            print('sections queried:',del_section)
            db.session.delete(del_section)
            db.session.commit()
            del_books = EBook.query.filter_by(sectionid = sid).all()

            for book in del_books:
                db.session.delete(book)
            db.session.commit()

            sections = Section.query.all()
            section_data = []
            for section in sections:
                section_data.append({
                    'sid': section.sid,
                    'title': section.title,
                    'date': section.date,
                    'description': section.description
                })
            books = EBook.query.all()
            book_data = []
            for book in books:
                book_data.append({
                    'ebid':book.ebid,
                    'title':book.title,
                    'author':book.author,
                    'description':book.description,
                    'date':book.date,
                    'sectionid':book.sectionid,
                    'file':book.file,
                    'quantity':book.quantity
                })

            print(section_data)
            print(book_data)
            return jsonify({"sections":section_data,'books':book_data }), 201
        except Exception as e:
            print(e)
            return jsonify({"msg": "Error deleting section"}), 500  
        

@app.route('/api/add_book', methods=['POST','OPTIONS','GET'])
@jwt_required()
def add_book():
    print(" inside def")
    if request.method == 'OPTIONS':
        # Create a response for the preflight request with the necessary headers
        print('in options')
        response = make_response()
        response.headers['Access-Control-Allow-Origin'] = 'http://192.168.1.5:8081'
        response.headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS'  # Corrected to include PUT
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        response.headers['Access-Control-Allow-Credentials'] = 'true'
        return response, 200  # Make sure to return 200 OK status for preflight request
    
    elif request.method == 'POST':
        try:
            title = request.form.get('title')
            author = request.form.get('author')
            description = request.form.get('description')
            date = request.form.get('date')
            sid = request.form.get('sid')
            quantity = request.form.get('quantity')
            file = request.files.get('file')
            price = request.form.get('price')
          
            if not file:
                return {'error': 'No file part'}, 400

            # Determine the file type (PDF or DOC)
            file_type = file.filename.split('.')[-1].lower()
            print(file_type)
            folder = os.path.join(app.config['UPLOAD_FOLDER'], file_type)

            if not os.path.exists(folder):
                os.makedirs(folder)

            file.save(os.path.join(folder, file.filename))
           
        
            new_book = EBook(title=title, date=date, description=description,author=author,sectionid=sid,file =  file.filename,quantity = quantity,price = price)
            db.session.add(new_book)
            db.session.commit()

            sections = Section.query.all()
            section_data = []
            for section in sections:
                section_data.append({
                    'sid': section.sid,
                    'title': section.title,
                    'date': section.date,
                    'description': section.description
                })

            books = EBook.query.all()
            book_data = []
            for book in books:
                book_data.append({
                    'ebid':book.ebid,
                    'title':book.title,
                    'author':book.author,
                    'description':book.description,
                    'date':book.date,
                    'sectionid':book.sectionid,
                    'file':book.file,
                    'quantity':book.quantity,
                    'price':book.price
                })

            print(section_data)
            print(book_data)
            return jsonify({"sections":section_data,'books':book_data }), 201
        except Exception as e:
            # Log the exception for debugging purposes
            print(e)
            # Return an error message
            return jsonify({"msg": "Error adding BOOK"}), 500
          
@app.route('/api/edit_book', methods=['POST', 'OPTIONS'])
@jwt_required()
def edit_book():
    print("Inside the function")
    if request.method == 'OPTIONS':
        # Create a response for the preflight request with the necessary headers
        print('Handling OPTIONS request')
        response = make_response()
        print('Handling OPTIONS request1')
        response.headers['Access-Control-Allow-Origin'] = 'http://192.168.1.5:8081'
        print('Handling OPTIONS request2')
        response.headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS'  # Corrected to include PUT
        print('Handling OPTIONS request3')
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        print('Handling OPTIONS request4')
        response.headers['Access-Control-Allow-Credentials'] = 'true'
        print('Handling OPTIONS request5')
        return response, 200  # Make sure to return 200 OK status for preflight request
    
    elif request.method == 'POST':
        data = request.json
        ebid = data['ebid']
        
        edit_book= EBook.query.filter_by(ebid = ebid).first()

        edit_book.title= data['title']
        edit_book.date = data['date']
        edit_book.description = data['description']
        edit_book.author= data['author']
        edit_book.quantity = data['quantity']
        edit_book.price = data['price']
       

        db.session.commit()

        sections = Section.query.all()
        section_data = []
        for section in sections:
            section_data.append({
                'sid': section.sid,
                'title': section.title,
                'date': section.date,
                'description': section.description
            })
            
            books = EBook.query.all()
            book_data = []
            for book in books:
                book_data.append({
                    'ebid':book.ebid,
                    'title':book.title,
                    'author':book.author,
                    'description':book.description,
                    'date':book.date,
                    'sectionid':book.sectionid,
                    'file':book.file,
                    'quantity':book.quantity,
                     'price':book.price
                })

            print(section_data)
            print(book_data)

        return jsonify({"sections":section_data,"books":book_data }), 201
        

@app.route('/api/delete_book', methods=['DELETE','OPTIONS','GET'])
@jwt_required()
def del_book():
    print(" inside def")
    if request.method == 'OPTIONS':
        # Create a response for the preflight request with the necessary headers
        print('in options')
        response = make_response()
        response.headers['Access-Control-Allow-Origin'] = 'http://192.168.1.5:8081'
        response.headers['Access-Control-Allow-Methods'] = 'DELETE, OPTIONS'  
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        response.headers['Access-Control-Allow-Credentials'] = 'true'
        return response, 200  # Make sure to return 200 OK status for preflight request
    
    elif request.method == 'DELETE':
        try:
            data = request.get_json()
        
            bid = data['ebid']
        
            del_book = EBook.query.filter_by(ebid = bid).first()
            print('sections queried:',del_book)
            db.session.delete(del_book)
            db.session.commit()

            sections = Section.query.all()
            section_data = []
            for section in sections:
                section_data.append({
                    'sid': section.sid,
                    'title': section.title,
                    'date': section.date,
                    'description': section.description
                })

            books = EBook.query.all()
            book_data = []
            for book in books:
                book_data.append({
                    'ebid':book.ebid,
                    'title':book.title,
                    'author':book.author,
                    'description':book.description,
                    'date':book.date,
                    'sectionid':book.sectionid,
                    'file':book.file,
                    'quantity':book.quantity,
                     'price':book.price
                })

            print(section_data)
            print(book_data)

            return jsonify({"sections":section_data,"books":book_data }), 201
        except Exception as e:
            print(e)
            return jsonify({"msg": "Error deleting section"}), 500
@app.route('/api/pdf/<path:filename>')
def serve_pdf(filename):
    secure_filename(filename)  
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
 
@app.route('/api/getrequests', methods=['OPTIONS','GET'])
@jwt_required()
def get_requests():
    if request.method == 'OPTIONS':
        # Create a response for the preflight request with the necessary headers
        print('in options')
        response = make_response()
        response.headers['Access-Control-Allow-Origin'] = 'http://192.168.1.5:8081'
        response.headers['Access-Control-Allow-Methods'] = 'GET, OPTIONS'  
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        response.headers['Access-Control-Allow-Credentials'] = 'true'
        return response, 200  # Make sure to return 200 OK status for preflight request
    
    elif request.method == 'GET':
        if request.method == 'GET':
            transactions = Transaction.query.all()
            request_data = []
            for transaction in transactions:
                user = User.query.get(transaction.user_id)
                book = EBook.query.get(transaction.book_id)
                sec = Section.query.get(book.sectionid)
                request_data.append({
                    'id': transaction.id,
                    'book_title': book.title,
                    'user_name': user.username,
                    'borrow_date': transaction.borrow_date,
                    'return_date': transaction.return_date,
                    'book_section': sec.title,
                    'days_requested': 5,
                    'pdf':f'/api/pdf/{book.file}',
                    'status':transaction.Status 
                })
            return jsonify(requests=request_data), 200
        else:
            return jsonify({"msg": "Bad request"}), 400


@app.route('/api/rejectrequest/<int:transaction_id>', methods=['OPTIONS','DELETE'])
@jwt_required()
def reject_request(transaction_id):
    if request.method == 'OPTIONS':
        print('in options')
        response = make_response()
        response.headers['Access-Control-Allow-Origin'] = 'http://192.168.1.5:8081'
        response.headers['Access-Control-Allow-Methods'] = 'DELETE, OPTIONS'  
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        response.headers['Access-Control-Allow-Credentials'] = 'true'
        return response, 200
    
    elif request.method == 'DELETE':
        transaction = Transaction.query.get(transaction_id)
        if not transaction:
            return jsonify({"msg": "Transaction not found."}), 404

        transaction.Status = "reject"  
        db.session.commit()

        return jsonify({"msg": "Book request rejected."}), 200


@app.route('/api/grantrequest/<int:transaction_id>', methods=['OPTIONS', 'POST'])
@jwt_required()
def grant_request(transaction_id):
    print("inside def")
    if request.method == 'OPTIONS':
        # Create a response for the preflight request with the necessary headers
        print('in options')
        response = make_response()
        response.headers['Access-Control-Allow-Origin'] = 'http://192.168.1.5:8081'
        response.headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS'  
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        response.headers['Access-Control-Allow-Credentials'] = 'true'
        return response, 200
    
    elif request.method == 'POST':
        transaction = Transaction.query.get(transaction_id)
        if not transaction:
            return jsonify({"msg": "Transaction not found."}), 404

        # Set the borrow_date to the current time in UTC and return_date 5 days later
        transaction.borrow_date = datetime.now(timezone.utc)
        transaction.return_date = transaction.borrow_date + timedelta(days=5)
        transaction.Status = "grant"
        db.session.commit()

        return jsonify({"msg": "Book request granted."}), 200



@app.route('/api/granted', methods=['OPTIONS', 'GET'])
def granted():
    print("Inside def granted()")
    print(f'Request Headers: {request.headers}')
    print(f'Request Method: {request.method}')

    if request.method == 'OPTIONS':
        print('Handling OPTIONS request')
        response = make_response()
        response.headers['Access-Control-Allow-Origin'] = 'http://192.168.1.5:8081'
        response.headers['Access-Control-Allow-Methods'] = 'GET, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        response.headers['Access-Control-Allow-Credentials'] = 'true'
        return response, 200

    elif request.method == 'GET':
        print('Handling GET request')
        
        # Fetch all transactions where return_date is not None, indicating the book has been granted
        transactions = Transaction.query.filter(Transaction.return_date.isnot(None)).all()
        
        if not transactions:
            return jsonify({"msg": "No granted transactions found."}), 404

        granted_requests = [{
                "id": transaction.id,
                "book_title": EBook.query.filter_by(ebid=transaction.book_id).first().title,
                "user_name": User.query.filter_by(id=transaction.user_id).first().username,
                "borrow_date": transaction.borrow_date,
                "return_date": transaction.return_date
            } for transaction in transactions]

        return jsonify({"requests": granted_requests}), 200

    else:
        print(f'Unexpected method: {request.method}')
        return jsonify({"msg": "Method not allowed"}),405


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
 