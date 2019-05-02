from flask import Flask, request, redirect, render_template,session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:Ethan061616@localhost:3306/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key='penny'

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(1500))
    owner_id=db.Column(db.Integer,db.ForeignKey('user.id'))

    def __init__(self, title, body,owner):
        self.title = title
        self.body = body
        self.owner =owner

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120),unique=True)
    password = db.Column(db.String(120))
    blogs= db.relationship('Blog',backref= 'owner')

    def __init__(self, username, password):
        self.username = username
        self.password = password


@app.before_request
def require_login():
    allowed_routes=['login','signup','blog']
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('/login')

@app.route('/login',methods=['POST','GET'])
def login():
    username=""
    user_error=""
    password_error=""

    if request.method=='POST':
        username=request.form['username']
        password=request.form['password']
        user = User.query.filter_by(username=username).first()

        if not user:
            user_error = "invalid username"
        if username =='':
            user_error="Please enter a valid username"
        if password =="":
            password_error = "please enter your password"

        if user and user.password != password:
            password_error = "Enter a valid password"


    if request.method=='POST' and username and user.password == password:
        session['username'] = username
            

    #Validate password and user
    #new_user.password not in db throw error

        #ession['username']= username
     #Validate password and user
        return redirect('/newpost')
    
    else:
        return render_template('login.html',username = username,username_error = user_error,password_error = password_error)

@app.route('/logout')
def logout():
    del session['username']
    return redirect('login.html')
    


@app.route('/blog',methods=['POST','GET'])
def index():
    blogs = Blog.query.all()

    return render_template('main-blog-page.html',bloglist=blogs)


@app.route('/newpost', methods=['POST','GET'])
def new_blog():
    title_error=''
    body_error=''
    title = ''
    body = ''
    owner = User.query.filter_by(username=session['username']).first()
    
    if request.method == 'POST':
        title = request.form['blog_title']
        body = request.form['blog_body'] 

        if title=='':
            title_error="Please fill in the title"
        if body=='':
            body_error="Please fill in the body"
    if request.method=='POST' and not title_error and not body_error:
        new_entry=Blog(title,body,owner)
        db.session.add(new_entry)
        db.session.commit()

        blogs = Blog.query.all()
        #return redirect('/blog?id={0}'.format(new_entry.id))
        return render_template('main-blog-page.html',bloglist=blogs)
    else:
        return render_template('new-blog.html',title_error=title_error,body_error=body_error, blog_title=title, blog_body=body)


@app.route('/new-entry',methods=['POST','GET'])
def new_entry():
    id=request.args.get('id')
    blog=Blog.query.filter_by(id=id).first()
    return render_template('new-entry.html',blog=blog)

@app.route('/signup',methods=['POST','GET'])
def signup():
    username=''
    user_error=''
    password_error=''
    verify_error=''
    existing_username=''   
    password=''
    
    if request.method =='POST':
        username = request.form['username']
        password = request.form['password']
        verify =request.form['verify']

        existing_username = User.query.filter_by(username=username).first()
    
    
    #Verify username
        if username =='':
            user_error="Please enter a valid username"
        elif len(username)<3 or len(username)>20:
            user_error="Username must be between 3 and 20 characters long"
            username = ''
        elif ' ' in username:
            user_error= "Your username cannot contain any spaces"
        


    #verify first password
        if password =='':
            password_error = "Please enter a valid password"
        elif len(password)<3 or len(password)>20:
            password_error="Password must be between 3 and 20 characters long."
        elif " "in password:
             password_error="Your password cannot contain spaces."
    
    #verify second password
        if verify == '' or verify != password:
            verify_error="Please ensure that passwords match."
            verify = ''
  
    #without errors
    if request.method == 'POST' and not user_error and not password_error and not verify_error:
            if not existing_username:
                new_user = User(username,password)
                db.session.add(new_user)
                db.session.commit()
                session['username']= new_user.username
            return redirect('/newpost')                
    else:
            #user_error ="username already exist"

     return render_template('signup.html',user_error = user_error,password_error = password_error, verify_error=verify_error)



@app.route('/index_2',methods=['POST','GET'])
def index_2():
    return render_template(index_2.html)




    
if __name__ == '__main__':
    app.run()