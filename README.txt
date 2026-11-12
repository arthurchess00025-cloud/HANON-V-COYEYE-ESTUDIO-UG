ATENCIÓN: TODOS LOS CONTENIDOS USADOS POR COYEYE ESTUDIO SON PERTENECIENTES AL PROGRAMA BACHILLERATO GENERAL PLAN 2020 DE LA UNIVERSIDAD DE GUANAJUATO, Y LOS DERECHOS CORRESPONDIENTES A ELLOS. LA GUÍA DE ESTUDIO NO SE LUCRA DE ESTE PROGRAMA, PUES SUS FUENTES DE INGRESOS PROVIENEN ÚNICAMENTE DE LAS FUNDAS DE TELA RECICLADA PARA DISPOSITIVOS MÓVILES, Y SOLAMENTE SUSTENTAN LA PRODUCCIÓN DE MÁS FUNDAS Y EL TRABAJO DE LOS RESPONSABLES DE ESTE PROYECTO.

HANON-V — ES UNA APLICACIÓN LOCAL QUE USA STREAMLIT PARA EJECUTARSE

OJO: De ser posible, crea una copia de este archivo, pues si alteras alguna línea del código este dejará de funcionar

CONTENIDO
- app.py: La interfaz general de programa, sus buscadores y lo que incluye como vista
- hanon_data.json: Contenidos de todos los semestres
- logo_hanon.png: logotipo extraído del documento de diseño proporcionado
- Hanon_V_original.py: copia intacta del programa en Python 3.15, del cual, yo, Arturo, el programador de esa monstruosidad, sufrí sobreexplotación laboral.
- requirements.txt: dependencias (básicamente lo que ocupa tu computadora para correr el programa y no explotar)

DISEÑO Y ORGANIZACIÓN (por si el usuario desea saber)
- El programa sigue la proporción áurea según los números de la sucesión de Fibonacci (es una proporción muy usada en la naturaleza y en distintos cuadros de la naturaleza en donde se divide la pantalla de los elementos principales a lo más secundario), y que si bien no la sigue por completo, pues por el bienestar mental y humanitario del programador (quien esta escribiendo esto) así se decidió para no sacrificar lo poco de salud mental y minutos de sueño que le quedaban

REQUISITOS
- Python 3.10 o posterior.
- Conexión a internet para instalar Streamlit la primera vez.
- La fotografía de José José se carga desde el sitio del INBAL, por lo que requiere internet para mostrarse.

INSTALACIÓN Y EJECUCIÓN
1. Descomprime la carpeta del proyecto
2. Abre una terminal dentro de la carpeta HanonV_6_Streamlit
3. Ejecuta: python -m pip install -r requirements.txt
4. Para abrirla en la red local, inicia: python -m streamlit run app.py --server.address 0.0.0.0
5. En el mismo dispositivo abre http://localhost:8501. Desde otro dispositivo conectado a la misma red, abre http://IP_LOCAL_DEL_EQUIPO:8501. Si Windows lo solicita, permite el acceso en el firewall para redes privadas.

DETENER
En la terminal donde se está ejecutando, pulsa Ctrl+C.

ESTIMACIÓN AMBIENTAL
Los valores de agua y electricidad son aproximaciones de consumo por ocho consultas breves de IA que podrían evitarse; no son mediciones directas de Hanon-V (tampoco hacemos milagros). El tiempo utiliza un promedio estimado de 2 minutos por consulta definido en el documento del proyecto. NO SE INCLUYE EL CONSUMO ELECTRICO DEL DISPOSITIVO, NI DE LA RED A LA QUE ESTÁ CONECTADA (para programar eso ya no daba mi salario inframínimo).
