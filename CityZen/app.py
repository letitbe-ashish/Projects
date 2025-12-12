from flask import Flask, render_template, request, redirect, url_for, send_from_directory, session, flash,jsonify
import sqlite3
import os
from werkzeug.utils import secure_filename
from datetime import datetime
import uuid

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


app = Flask(__name__)
app.secret_key = "iwillforgetit"

UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# Uploaded images
@app.route('/Images/<path:filename>')
def serve_images(filename):
    return send_from_directory('static/images', filename)

# Homepage
@app.route('/',methods=['GET', 'POST'])
def Ulogin():
    if request.method == 'POST':
       
        if 'login_username' in request.form and 'login_password' in request.form:
            username = request.form['login_username']
            password = request.form['login_password']

            conn = sqlite3.connect('database.db')
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM login_info WHERE username = ? AND password = ?", (username, password))
            user = cursor.fetchone()
            conn.close()

            if user:
                session['user'] = username
                session['user_email'] = user['email'] 
                session.setdefault('user_id', str(uuid.uuid4())) 
                flash("Login successful!", "success")
                return redirect(url_for('dashboard'))

            else:
                flash("Invalid username or password.", "error")
                return redirect(url_for('Ulogin'))

    
        elif 'register_username' in request.form and 'register_password' in request.form and 'register_email' in request.form:
            username = request.form['register_username']
            password = request.form['register_password']
            email = request.form['register_email']

            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()

            
            cursor.execute("SELECT * FROM login_info WHERE username = ? OR email = ?", (username, email))
            existing = cursor.fetchone()

            if existing:
                flash("Username or Email already exists.", "error")
                conn.close()
                return redirect(url_for('Ulogin'))

            cursor.execute("INSERT INTO login_info (username, password, email) VALUES (?, ?, ?)",
                           (username, password, email)) 
            conn.commit()
            conn.close()
            flash("Registered successfully! Please log in.", "success")
            return redirect(url_for('Ulogin'))

    return render_template('Userlogin.html')

    
    
    
#return render_template('Userlogin.html')
def get_logged_in_user():
    if 'user' in session:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM login_info WHERE username = ?", (session['user'],))
        user = cur.fetchone()
        conn.close()
        return user
    return None

#Userdashboard
@app.route('/dashboard')
def dashboard():
    if 'user' in session:
        username = session['user']
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM login_info WHERE username = ?", (username,))
        user_data = cur.fetchone()
        conn.close()
        if user_data:
            return render_template('dashboard.html', username=user_data['username'], email=user_data['email'])
    return redirect(url_for('Ulogin'))


@app.route('/logout', methods=['POST'])
def logout():
    if 'admin' in session:
        session.clear()
        return redirect(url_for('adminlogin'))  

    elif 'user' in session:
        session.clear()
        return redirect(url_for('Ulogin'))  


    session.clear()
    return redirect(url_for('Ulogin'))

# Hot issues page
@app.route('/hotissue')
def hotissue():
    sort_by = request.args.get('sort', 'votes')
    category = request.args.get('category', 'all') 

    base_query = "SELECT * FROM issues"
    filters = []
    params = []
    
    if category and category != 'all':
        filters.append("assign_to = ?")
        params.append(category)

    if filters:
        base_query += " WHERE " + " AND ".join(filters)

    if sort_by == 'votes':
        base_query += " ORDER BY vote DESC"
    elif sort_by == 'date':
        base_query += " ORDER BY datetime(created_at) DESC"
    else:
        base_query += " ORDER BY id DESC"

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(base_query, params)
    iss = cur.fetchall()
    conn.close()

    user = get_logged_in_user()
    if not user:
        return redirect(url_for('Ulogin'))

    return render_template('hotissue.html', iss=iss, sort_by=sort_by, username=user['username'], email=user['email'], selected_category=category)

# About Us
@app.route('/aboutus')
def aboutus():
    user = get_logged_in_user()
    if user:
        return render_template('aboutus.html', username=user['username'], email=user['email'])
    return redirect(url_for('Ulogin'))

# Track Issues page
@app.route('/trackissue',methods=['GET', 'POST'])
def trackissue():   
    user = get_logged_in_user()
    if not user:
        return redirect(url_for('Ulogin'))
    results = []
    if request.method == 'POST':
        email = request.form['email']

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM issues WHERE email = ? ORDER BY id DESC", (email,))
        results = cur.fetchall()
        conn.close()
        

    return render_template('trackissue.html', results=results , username=user['username'], email=user['email'])
  
# Help page
@app.route('/help', methods=['GET', 'POST'])
def help_page():
    user = get_logged_in_user()
    if not user:
        return redirect(url_for('Ulogin'))

    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('''
            INSERT INTO general_queries (name, email, message)
            VALUES (?, ?, ?)
        ''', (name, email, message))
        conn.commit()
        conn.close()

    return render_template('helppage.html', username=user['username'], email=user['email'])

#Escalate issue 
@app.route('/get_issue/<int:issue_id>')
def get_issue(issue_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT created_at FROM issues WHERE id = ?", (issue_id,))
    row = cur.fetchone()
    conn.close()

    if row:
        return jsonify({'created_at': row['created_at']})
    else:
        return jsonify({'error': 'Issue not found'}), 404


# Issue Reporting form
@app.route('/reportform', methods=['GET', 'POST'])
def reportform():
    user = get_logged_in_user()
    if not user:
        return redirect(url_for('Ulogin'))
    if request.method == 'POST':
        name = request.form['name']
        address = request.form['address']
        pincode = request.form['pincode']
        email = request.form['email']
        phone = request.form['phone']
        issue_type = request.form['issue_type']
        description = request.form['description']

       
        image_file = request.files.get('image')
        image_filename = None

        if image_file and image_file.filename != '':
            filename = secure_filename(image_file.filename)
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image_file.save(image_path)
            image_filename = filename
            
        created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

       
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('''
            INSERT INTO issues (name, address, pincode, email, phone, issue_type, description, image, status, vote, assign_to, created_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
''', (name, address, pincode, email, phone, issue_type, description, image_filename, "Pending", 0, None, created_at))
        conn.commit()
        conn.close()

        return redirect(url_for('thank_you'))

    return render_template('reportform.html' ,username=user['username'], email=user['email'])

#thankyou page
@app.route('/thank_you')
def thank_you():
    return render_template('thankyou.html')  


# Admin dashboard home + Hotissues
@app.route('/adminissueshome')
def adminissueshome():
    if 'admin' not in session:
        return redirect(url_for('adminlogin'))

    sort_by = request.args.get('sort', 'votes')
    category = request.args.get('category', 'all')

    base_query = "SELECT * FROM issues"
    filters = []
    params = []

    if category and category != 'all':
        filters.append("assign_to = ?")
        params.append(category)

    if filters:
        base_query += " WHERE " + " AND ".join(filters)

    if sort_by == 'votes':
        base_query += " ORDER BY vote DESC"
    elif sort_by == 'date':
        base_query += " ORDER BY datetime(created_at) DESC"
    else:
        base_query += " ORDER BY id DESC"

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(base_query, params)
    issues = cur.fetchall()
    conn.close()

    return render_template(
        'Adminissueshome.html',
        issues=issues,
        sort_by=sort_by,
        admin_name=session['admin'],
        selected_category=category
    )


@app.route('/Userlogin')
def Userlogin():
    return render_template('Userlogin.html')

@app.route('/adminlogin', methods=['GET', 'POST'])
def adminlogin():
    if request.method == 'POST':
        username = request.form.get('admin_username')
        password = request.form.get('admin_password')

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM admin_login WHERE adm_username=? AND adm_password=?', (username, password))
        admin = cursor.fetchone()
        conn.close()

        if admin:
            session['admin'] = username
            flash("Admin login successful!", "success")
            return redirect(url_for('adminissueshome'))
        else:
            flash("Invalid admin credentials.", "error")
            return redirect(url_for('adminlogin'))

    return render_template('adminlogin.html')


#Admin Page Query
@app.route('/Adminquery')
def Adminquery():
    
    if 'admin' not in session:
        return redirect(url_for('adminlogin')) 
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM general_queries")
    queries = cur.fetchall()
    conn.close()
    return render_template('Adminquery.html', queries=queries,admin_name=session['admin'] )

@app.route('/api/reply', methods=['POST'])
def api_reply():
    data = request.get_json()
    query_id = data.get('id')
    reply = data.get('reply')

    if not query_id or not reply:
        return {"error": "Missing id or reply"}, 400

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("UPDATE general_queries SET answer = ? WHERE id = ?", (reply, query_id))
    conn.commit()
    conn.close()

    return {"message": "Reply updated successfully"}, 200

# Messages page
@app.route('/message')
def message():
    user = get_logged_in_user()
    if not user:
        return redirect(url_for('Ulogin'))

    user_email = user['email']  

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM general_queries WHERE email = ?", (user_email,))
    messages = cur.fetchall()
    conn.close()

    return render_template('message.html', messages=messages, username=user['username'], email=user['email'])

@app.route('/vote/<int:issue_id>', methods=['POST'])
def vote(issue_id):
    if 'user' not in session:
        return jsonify({'success': False, 'message': 'User not logged in'}), 401

    user_session = session.get('user_id')  

    if not user_session:
        user_session = str(uuid.uuid4())
        session['user_id'] = user_session

    conn = get_db_connection()
    cur = conn.cursor()


    cur.execute('SELECT 1 FROM votes WHERE issue_id = ? AND user_session = ?', (issue_id, user_session))
    if cur.fetchone():
        conn.close()
        return jsonify({'success': False, 'message': 'You already voted on this issue'}), 403

  
    cur.execute('INSERT INTO votes (issue_id, user_session) VALUES (?, ?)', (issue_id, user_session))
    cur.execute('UPDATE issues SET vote = vote + 1 WHERE id = ?', (issue_id,))
    conn.commit()
    conn.close()

    return jsonify({'success': True, 'message': 'Vote counted'})

#issue Updation
@app.route('/adminissueshome/update-issue', methods=['POST'])
def update_issue():
    data = request.get_json()
    issue_id = data.get('id')
    status = data.get('status')
    assign_to = data.get('assign_to')

    if not issue_id:
        return jsonify({'error': 'Missing issue ID'}), 400

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
        UPDATE issues
        SET status = ?, assign_to = ?
        WHERE id = ?
    ''', (status, assign_to, issue_id))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Issue updated successfully'})



if __name__ == '__main__':
    app.run(debug=True, use_reloader=False ,  host='0.0.0.0'
)
