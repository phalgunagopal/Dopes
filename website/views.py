from io import BytesIO
from flask import Blueprint,render_template,request,flash,send_file,redirect,url_for
from .models import User, Repository, Project, Commit, Domain,Joined,Commit
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from sqlalchemy import func,delete
from flask_login import login_user, login_required, logout_user, current_user
views = Blueprint('views', __name__)
import datetime
import mysql.connector


cnx = mysql.connector.connect(user='root', database='dopes')


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        name=request.form.get('name')

        collaborators=request.form.get('collaborators')
        access=request.form.get('access')
        
        file = request.files['file']
        user=current_user
        if collaborators!="" and (access=="public" or access=="private"):
            repository=Repository(user_id=user.id,access=access, creator=user.email,name=name)
            
            db.session.add(repository)
       
            db.session.commit()
            repid=repository.id
            for i in collaborators.split(","):
                if i!="":
                    joined=Joined(repo_id=repid,user_email=i,user_id=user.id)
                    db.session.add(joined)
                    db.session.commit()
                


            project = Project(filename=file.filename, data=file.read(),repo_id=repid)
            db.session.add(project)
            db.session.commit()
            return redirect(url_for('views.home',user=current_user))
        return f'Uploaded: {file.filename}'

    else:
        user=current_user
        cursor = cnx.cursor()
        query = (f"SELECT id,date from repository where creator='{user.email}'")
        cursor.execute(query)
        a=cursor.fetchall()

        l=[]    
        for i in a:
            query = (f"SELECT user_email from joined where repo_id='{i[0]}'")
            cursor.execute(query)
            b=cursor.fetchall()
            l.append((i[0],b,i[1]))
               

    
        cnx.commit()
        cursor.close()
        return render_template('home.html',value=l)

@views.route('/delete', methods=['GET', 'POST'])
@login_required
def deleted():
    
    if request.method=="POST":
        
        projectid=request.form.get('projectid')
        cursor = cnx.cursor()
        print("hello")
        query = (f"DELETE from project where id={projectid}")
        cursor.execute(query)
        cnx.commit()
        cursor.close()
        # dele=delete(Project).where(Project.id==projectid)
        # db.session.execute(dele)
        # db.session.commit()
         
        return render_template('delete.html',value=projectid)
    return render_template('delete.html',value="hello")

@views.route('/commit', methods=['GET', 'POST'])
@login_required
def commit():
    if request.method == 'POST':
        repoid=request.form.get('repoid')
        comment=request.form.get('comment')
        reposit=Repository.id
        
        file = request.files['file']
        user=current_user
        
        commit=Commit(user_id=user.id,filename=file.filename, data=file.read(),comment=comment,repo_id=repoid)
        
        db.session.add(commit)
    
        db.session.commit()
        cursor = cnx.cursor()
        
        query = (f"UPDATE project SET data='{file.read()}', filename='{file.filename}' WHERE repo_id='{repoid}'")
        cursor.execute(query)
        cnx.commit()
        cursor.close()
        
        
    return render_template('commit.html')

@views.route('/see',methods=['POST', 'GET'])
def see():
    user=current_user
    cursor = cnx.cursor(buffered=True)
        
    query = (f"SELECT user_email from allcollaborators WHERE user_id ='{user.id}';")
    cursor.execute(query)
    ab=cursor.fetchall()
    cnx.commit()
    cursor.close()

    # cursor = cnx.cursor(buffered=True)
        
    # query = (f"SELECT id, nocommits('{user.id}') AS c FROM commit;")
    # cursor.execute(query, multi=True)
    # ba=cursor.fetchall()
    # cnx.commit()
    # cursor.close()
    # db.engine.execute(dpes("SELECT function_name(:parm_1, :parm_2)").execution_options(autocommit=True), :parm_1 = :parm_1, :parm_2 = :parm_2)


    return render_template('see.html',value=ab)

@views.route('/seemore', methods=['GET','POST'])
@login_required
def seemore():
    user=current_user
    cursor = cnx.cursor(buffered=True)
        
    query = (f"SELECT id, nocommits('{user.id}') AS c FROM commit;")
    cursor.execute(query)
    ba=cursor.fetchall()
    
    cnx.commit()
    cursor.close()
    return render_template('seemore.html',value=ba)


def call_procedure(id):
    cursor = cnx.cursor(buffered=True)
    data = []
    cursor.callproc('commitsmade', [id])
    data = cursor.stored_results()
    print(data)
    return data
    