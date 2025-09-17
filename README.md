# Airline & Commerce App

Este proyecto se divide en dos partes principales: una **API** para la gestión de aerolíneas y vuelos, y una **interfaz de usuario (UI)** para un sistema de comercio electrónico.

---

## 🔗 URLs de las Aplicaciones

| Componente | URL |
|------------|-----|
| ✈️ API     | [https://cf-automation-airline-api.onrender.com/](https://cf-automation-airline-api.onrender.com/) |
| 🛍️ Web-UI  | [https://shophub-commerce.vercel.app/](https://shophub-commerce.vercel.app/) |

---

## ✈️ API - Documentación de Pruebas Automatizadas

La documentación de la API se basa en una suite de pruebas automatizadas que sigue un enfoque integral. Se han validado tanto los escenarios de éxito (**Happy Paths**) como los de fracaso (**Unhappy Paths**), prestando especial atención a la robustez, seguridad y la correcta validación de los datos.

### ⚙️ Metodología de Pruebas

- **Pruebas Funcionales:** Se validó la funcionalidad principal de cada endpoint (creación, obtención, actualización y eliminación de recursos).  
- **Validación de Esquemas y Datos:** Se verificó que los datos de entrada y salida cumplen con el esquema esperado. Todos los campos son validados estrictamente en la API, incluyendo tipos, formatos y obligatoriedad.  
- **Técnicas de Valores Límite:** Se realizaron pruebas para asegurar que los endpoints manejan correctamente los valores en los límites de los rangos definidos (ej. longitud de contraseñas, `tail_number`).  
- **Seguridad:** Se confirmó que solo los usuarios con los privilegios adecuados (admin vs. passenger) pueden acceder a recursos restringidos.  

### 📝 Resumen de Casos de Prueba por Módulo

| Módulo          | Puntos Clave de la Validación |
|-----------------|-------------------------------|
| **Aircrafts**   | CRUD completo con enfoque en seguridad (solo admins) y validación de longitud, tipo y unicidad de campos. |
| **Airports**    | CRUD con permisos de administrador y verificación de formato de código. |
| **Auth (Signup & Login)** | Registro e inicio de sesión con datos válidos e inválidos; validación robusta de todos los campos. |
| **Bookings**    | Permisos: usuarios gestionan sus reservas; admins pueden ver/modificar todas. |
| **Flights**     | Validación de IDs de aeropuertos y aeronaves; lógica de fechas correcta (llegada posterior a salida). |
| **Payments**    | Pagos solo para reservas existentes; valores coherentes (monto positivo). |
| **Users**       | Gestión restringida a admins. |

> Para más detalles sobre los casos de prueba, consulta este excel: **https://docs.google.com/spreadsheets/d/14Y6oEXpiVEY7FNYG8O7cOedH6oo7a-Ge/edit?usp=sharing&ouid=116596529286557480406&rtpof=true&sd=true**.

---

## 🛍️ Web-UI - Documentación de Pruebas Automatizadas

La validación de la interfaz de usuario se realizó mediante **Page Object Model (POM)**, un patrón de diseño que mejora la legibilidad y mantenibilidad del código de prueba.

### 🎨 Metodología de Pruebas

- **Pruebas E2E (End-to-End):** Validación del flujo completo de compra, desde registro hasta checkout.  
- **Validación de Flujos Críticos:** Pruebas específicas por página (Home, Cart, Checkout) para asegurar navegación e interacciones correctas.  
- **Validación de Campos:** Solo el campo de correo electrónico tiene validación estricta; los demás campos se prueban enfocándose en flujo general.  
- **Gestión de Defectos:** Se usan warnings en lugar de fallos totales para capturar múltiples hallazgos en una misma ejecución.  

### 📝 Resumen de Casos de Prueba por Página

| Página                  | Puntos Clave de la Validación |
|-------------------------|-------------------------------|
| **Home Page**           | Todos los enlaces de navegación redirigen correctamente. |
| **Páginas de Categoría** | Validación de productos, consistencia de paginación y existencia de elementos clave (imagen, nombre, precio). |
| **Detalle de Producto (PDP)** | Botones de cantidad y agregar al carrito funcionan correctamente; contador del carrito se actualiza. |
| **Carrito**             | Refleja con precisión los productos agregados; se puede cambiar cantidad o eliminar; checkout redirige a página de pago. |
| **Checkout**            | Campos obligatorios validados; sistema bloquea avance si faltan datos o email inválido. |

# 📋 Test Plan

## 🎯 Objetivo
El objetivo principal del plan de pruebas ha sido **validar que la API y la Web-UI funcionen correctamente**, asegurando la calidad tanto de los flujos críticos como de las validaciones en cada página y endpoint.

- **API:** ✅ Validar el **100% de los endpoints** de la URL [Airline API](https://cf-automation-airline-api.onrender.com/).  
  - Se aplicaron técnicas de validación estricta de esquemas, valores límite y pruebas de permisos.  
  - Se cubrieron tanto **Happy Paths** como **Unhappy Paths**.  

- **Web-UI:** ✅ Validar **todas las páginas de [Shophub Ecommerce](https://shophub-commerce.vercel.app/), cada una con sus **propias validaciones funcionales**.  
  - Se probó el flujo crítico de compra (registro, carrito, checkout).  
  - Además, se incluyeron casos **parametrizados** como la obligatoriedad de campos en checkout y validaciones de productos.  
  - Se aplicó tanto **Happy Path** como **Unhappy Path**.  
  - La validación se ejecutó únicamente en **Google Chrome**.  

En ambos componentes, el objetivo también fue **detectar y documentar bugs**, no solo validar que los flujos pasen correctamente.  
En la Web-UI, en algunos escenarios se optó por **warnings** en lugar de fallar la ejecución completa, permitiendo capturar múltiples hallazgos en una sola corrida.

---

## 📌 Alcance
- **Incluido:**  
  - API: Validación funcional de todos los endpoints y sus reglas de negocio, con énfasis en **permisos** (ej. admin vs passenger).  
  - Web-UI: Validación de **todas las páginas**, incluyendo pruebas de navegación, carrito, checkout, productos y campos obligatorios.  
  - Todos los datos de prueba fueron **generados de manera aleatoria**, sin uso de data sensible ni valores fijos.  

- **Excluido:**  
  - No se evaluó **performance** ni **carga**.  
  - No se realizaron pruebas de **seguridad avanzada** (ej. pruebas de penetración).  

---

## ⚙️ Estrategia de Pruebas
- **Técnicas aplicadas:**  
  - ✅ Pruebas funcionales.  
  - ✅ Validación de esquemas y datos.  
  - ✅ Valores límite.  
  - ✅ Happy Path y Unhappy Path en API y Web-UI.  
- **Frameworks / Lenguaje:**  
  - Toda la automatización se implementó en **Python**.  
  - API: Suite de pruebas automatizadas estructurada por módulos.  
  - Web-UI: Enfoque de **Page Object Model (POM)** para mejorar mantenibilidad.  
- **Gestión de defectos:**  
  - Bugs detectados fueron registrados como fallos en los reportes.  
  - En UI, algunos defectos fueron manejados con **warnings** para no interrumpir la ejecución total.  

---

## 🧩 Niveles de Prueba
- ✅ **Componente:** Validación de endpoints individuales (API) y páginas aisladas (UI).  
- ✅ **Integración:** Validación de interacciones entre módulos (ej. booking → payment).  
- ✅ **End-to-End:** Flujos completos (ej. creación de usuario → reserva → pago en API; registro → compra → checkout en UI).  
- ✅ **Aceptación:** Validación de que los flujos críticos y páginas completas funcionan de forma consistente en un entorno de pruebas.  

---

## ⚠️ Riesgos y Dependencias
- **Riesgos:**  
  - Ninguno relevante, dado que todas las pruebas se ejecutaron en entornos de prueba controlados.  
- **Dependencias:**  
  - API y UI deben estar desplegadas en sus respectivas URLs para ejecutar las suites.  

---

## 📊 Ejecución y Reportes
- Las suites están integradas en **GitHub Actions**, ejecutándose de manera automatizada.  
- El reporte final marca una ❌ en caso de que **alguna prueba falle**. Esto es esperado, ya que se encontraron bugs en **API y Web-UI**.  
- El uso de **warnings en UI** permite continuar la ejecución y detectar múltiples defectos en una misma corrida.  

---

# Ejecución en Github Actions

1. Para ejecutar los tests de API y UI, se debe dirigir a la sección de Actions: https://github.com/dianahuamant/Project-Automation-QA/actions
En el panel izquierdo elegir:
- Run API Tests
- Run UI Tests
2. Luego de elegir uno, hacer click en él y encontrará un mensaje "This workflow has a workflow_dispatch event trigger".
3. Tendrá que hacer clic en el botón "Run workflow" que está al lado de ese mensaje.
4. Hará click en el botón verde "Run workflow".
5. Aparecerá una sección que carga porque se están corriendo los tests.
6. Una vez termine de cargar hace click en el run y para ver el detalle del run va a la sección Artifacts que tiene el archivo con fecha y hora:
<img width="1189" height="210" alt="Captura de pantalla 2025-09-17 a la(s) 2 04 48 p  m" src="https://github.com/user-attachments/assets/d6e2f891-473e-4650-86bd-0ba7481c3b6f" />
7. Podrá descargar el archivo y ver el detalle de los tests.

