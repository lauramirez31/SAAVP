from flask import Flask, render_template, request, redirect, url_for, flash, Response, session

app = Flask(__name__, template_folder='Templates')  # Parametro

# Creamos Ruta Principal
@app.route("/")
def Index():
    return render_template('imc.html')

@app.route("/imc", methods=["GET", "POST"])
def Oper():
    if request.method == "POST":
        a = int(request.form["t1"])
        b = float(request.form["t2"])
        c = b * b
        d = a / c
        if d>=0 and d<18.5:
            estado="bajo peso"
        elif d>=18.5 and d<24.9:
            estado="adecuado"
        elif d>=25 and d<29.9:
            estado="sobrepeso"
        elif d>=30 and d<34.9:
            estado="obesidad grado 1"
        elif d>=35 and d<39.9:
            estado="obesidad grado 2"
        else :
    
            estado="kilos mortales"    



        return render_template('imc.html', py=a, sy=b, sp=d, es=estado)
    else:
        return render_template('imc.html', sm=None)
    
    
    
   
        

if __name__ == "__main__":
    app.run(port=5000, debug=True)
