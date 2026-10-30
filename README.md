# ENOSA Calculadora PRO WEB — V4

Calculadora web referencial de consumo BT5B con 7 recibos históricos anonimizados (abril–octubre de 2026). Incluye el recibo de octubre: 342 kWh / S/ 319.20.

## Ejecutar en local

```bash
pip install -r requirements.txt
python app.py
```

Abre http://127.0.0.1:5000

## Publicar en Render

Sube **el contenido de esta carpeta** a la raíz de un repositorio GitHub. Crea un Web Service de Render conectado al repositorio, o usa el archivo `render.yaml` como Blueprint. El inicio usa `gunicorn app:app`.

## Limitaciones

El modelo interpola los importes totales de los siete recibos y extrapola fuera del rango. No descarga el pliego tarifario vigente, no determina automáticamente FOSE ni otros beneficios, y no garantiza precisión para otros suministros o zonas. La aproximación de 342 kWh reproduce S/ 319.20 por ser un punto de referencia del modelo, **no es una validación independiente**.

Las lecturas deben corresponder al mismo medidor y periodo facturado. Si el medidor es nuevo y comenzó en cero, marca la casilla correspondiente; en periodos siguientes usa la última lectura facturada como lectura anterior.
