from flask import Flask, render_template, request, jsonify
from math import isfinite

app = Flask(__name__)

# Registros anonimizados; importes facturados reales (no tarifas oficiales).
RECIBOS = [
    {'mes':'Abril 2026','kwh':176,'total':159.10,'energia_unitaria':0.6708,'alumbrado':10.25,'fijo':3.51,'mantenimiento':1.37,'igv':23.97,'aporte':1.94},
    {'mes':'Mayo 2026','kwh':111,'total':103.30,'energia_unitaria':0.6884,'alumbrado':5.04,'fijo':3.58,'mantenimiento':1.40,'igv':15.58,'aporte':1.22},
    {'mes':'Junio 2026','kwh':167,'total':158.20,'energia_unitaria':0.6952,'alumbrado':11.25,'fijo':3.60,'mantenimiento':1.41,'igv':23.85,'aporte':1.84},
    {'mes':'Julio 2026','kwh':121,'total':112.40,'energia_unitaria':0.6933,'alumbrado':5.52,'fijo':3.57,'mantenimiento':1.40,'igv':17.03,'aporte':1.33},
    {'mes':'Agosto 2026','kwh':8,'total':12.70,'energia_unitaria':0.7075,'alumbrado':0.55,'fijo':3.56,'mantenimiento':1.39,'igv':2.05,'aporte':0.09},
    {'mes':'Septiembre 2026','kwh':12,'total':16.20,'energia_unitaria':0.7184,'alumbrado':0.55,'fijo':3.57,'mantenimiento':1.39,'igv':2.54,'aporte':0.13},
    {'mes':'Octubre 2026','kwh':342,'total':319.20,'energia_unitaria':0.7210,'alumbrado':15.75,'fijo':3.61,'mantenimiento':1.40,'igv':48.12,'aporte':3.76},
]
POINTS = sorted((r['kwh'],r['total']) for r in RECIBOS)

def estimate(kwh):
    # Interpolación por puntos históricos: respeta los recibos observados.
    # La extrapolación fuera del rango es menos fiable.
    if kwh <= POINTS[0][0]: a,b=POINTS[0],POINTS[1]
    elif kwh >= POINTS[-1][0]: a,b=POINTS[-2],POINTS[-1]
    else:
        a,b=POINTS[0],POINTS[1]
        for i in range(len(POINTS)-1):
            if POINTS[i][0] <= kwh <= POINTS[i+1][0]:
                a,b=POINTS[i],POINTS[i+1]
                break
    return max(0.0, a[1]+(kwh-a[0])*(b[1]-a[1])/(b[0]-a[0]))

@app.get('/')
def home():
    return render_template('index.html', recibos=RECIBOS)

@app.post('/api/calcular')
def calcular():
    data=request.get_json(silent=True) or {}
    try:
        anterior=float(data['anterior'])
        actual=float(data['actual'])
        if not (isfinite(anterior) and isfinite(actual) and 0 <= anterior <= actual <= 100000000):
            raise ValueError()
    except (KeyError, TypeError, ValueError, OverflowError):
        return jsonify(error='Ingresa lecturas válidas; la actual debe ser mayor o igual a la anterior.'),400
    consumo=round(actual-anterior,3)
    monto=round(estimate(consumo),2)
    return jsonify(consumo=consumo,monto=monto,rango_min=round(monto*.90,2),rango_max=round(monto*1.10,2),
        metodo='Estimación estadística con siete recibos históricos de referencia (abril-octubre 2026). No es tarifa oficial.',
        advertencia='Fuera del rango observado (8–342 kWh): extrapolación menos confiable.' if consumo < 8 or consumo > 342 else '')

if __name__=='__main__':
    app.run(debug=True)
