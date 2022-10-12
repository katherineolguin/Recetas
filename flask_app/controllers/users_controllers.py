from flask import render_template, redirect, request, session, flash, jsonify #jsonify es de ajax
from flask_app import app

#Importamos modelo
from flask_app.models.users import User
from flask_app.models.recipes import Recipe


#Importación de Bcrypt
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/register', methods=['POST'])
def register():
    
        # Validamos la informacion que recibimos
    if not User.valida_usuario(request.form):
        return redirect('/')


    #Guardar registro
    pwd = bcrypt.generate_password_hash(request.form['password'])#Encriptando la contraseña del usuario y guardandola en pwd

    #Creamos un diccionario con todos los datos de request.form
    #  request.form['password'] = pwd --> ERROR: request.form NO se puede cambiar
    formulario = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": pwd
    }

    id = User.save(formulario) #Recibit el ID del nuevo usuario


    session['user_id'] = id # Guardamos en session el indentificador del usuario
    
    return redirect('/dashboard')


@app.route('/login', methods=['POST'])
def login():
    #Verificamos que el email exista en la Base de datos
    user = User.get_by_email(request.form) #Recibimos una instancia de usuario O False


#Si user = False / sino se cumple con esta funcion sigue con a sigiente y la siguiente y así
    if not user: 
        # flash('E-mail no encontrado', 'login')  #DESCOMENTAR PARA HACER RECETAS NORMAL
        # return redirect('/')

        return jsonify (message="E-mail no encontrado")  #Esto es de ajax

    #user es una instancia con todos los datos de mi usuario

    if not bcrypt.check_password_hash(user.password, request.form['password']):
        # flash('Password incorrecto', 'login')   #DESCOMENTAR PARA HACER RECETAS NORMAL
        # return redirect('/')

        return jsonify (message="Passweord incorrecto")  #Esto es de ajax


    session['user_id'] = user.id

    # return redirect('/dashboard')   #DESCOMENTAR PARA HACER RECETAS NORMAL

    return jsonify (message="correcto")  #Esto es de ajax



@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/')

    #Yo sé que en sesión tengo el id de mi usuario (session['user_id'])
    #Queremos una función que en base a ese id me regrese una instancia del usuario
    formulario = {"id": session['user_id']}

    user = User.get_by_id(formulario) #Recibo la instancia de usuario en base a su ID

    #Listas con todas las recetas
    recipes = Recipe.get_all()

    return render_template('dashboard.html', user=user, recipes=recipes)




@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')
