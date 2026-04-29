# Mini DSS Logístico con Streamlit

## Descripción
Este proyecto implementa un sistema de soporte a decisiones (DSS) para asignación de rutas y transportistas en logística.  
La aplicación se ejecuta con **Streamlit** y permite ajustar umbrales dinámicos para simular escenarios y visualizar resultados en tiempo real.

---

## Ejecución

1. Clonar o descargar este repositorio.  
2. Abrir una terminal en la carpeta donde se encuentra el archivo `.py` (por ejemplo `Supply_chain_optmización.py`).  
3. Ejecutar el siguiente comando:
   ```bash
   streamlit run Supply_chain_optmización.py

Nota importante
Para que el sistema funcione correctamente es necesario configurar la conexión a PostgreSQL en el script Python.
Por motivos de protección de información, las credenciales no están incluidas en este repositorio.
Sin embargo, los entregables y la lógica del DSS están claros y reproducibles: basta con añadir tus credenciales de conexión en la línea de create_engine.

engine = create_engine("postgresql://usuario:password@localhost:5432/tu_bd")
