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

# Ejecución en Github Actions

Para ejecutar los tests de API y UI, se debe dirigir a la sección de Actions y correr el workflow según preferencia.
Tanto en API como en UI es posible encontrar bugs, por lo que saldrá que el workflow en general no ha pasado, pero para ver mayor detalle,
es posible descargar el reporte de cada workflow ejecutado.
