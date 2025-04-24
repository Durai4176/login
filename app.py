from flask import Flask, request, session, redirect, render_template_string
import os

app = Flask(__name__)
app.secret_key = 'x'
users = {}

tpl = ''' 
<title>{{t}}</title>
<h2>{{t}}</h2>
<form method="post"> 
    <input name="username" placeholder="User" required><br><br> 
    <input name="password" type="password" placeholder="Pass" required><br><br> 
    <button>{{t}}</button>
</form> 
<p><a href="{{l}}">{{txt}}</a></p>
{% if m %}
<p style="color:red">{{m}}</p>
{% endif %}
'''

@app.route('/')
def home():
    return redirect('/login')

@app.route('/signup', methods=['GET', 'POST'])
def up():
    if request.method == 'POST':
        u, p = request.form['username'], request.form['password']
        if u in users:
            return render_template_string(tpl, t='Sign Up', l='/login', txt='Login', m='User exists')
        users[u] = p
        return redirect('/login')
    return render_template_string(tpl, t='Sign Up', l='/login', txt='Login', m='')

@app.route('/login', methods=['GET', 'POST'])
def log():
    if request.method == 'POST':
        u, p = request.form['username'], request.form['password']
        if users.get(u) == p:
            session['u'] = u
            return redirect('/dash')
        return render_template_string(tpl, t='Login', l='/signup', txt='Sign up', m='Invalid')
    return render_template_string(tpl, t='Login', l='/signup', txt='Sign up', m='')

@app.route('/dash')
def dash():
    if 'u' in session:
        return f"<h3>Welcome back to our web page, {session['u']}!</h3><a href='/logout'>Logout</a>"
    return redirect('/login')

@app.route('/logout')
def logout():
    session.pop('u', None)
    return redirect('/login')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # for Render
    app.run(debug=True, host='0.0.0.0', port=port)  # binds to external traffic
