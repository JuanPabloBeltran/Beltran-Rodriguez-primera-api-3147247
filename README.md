cat > README.md << EOF
# Mi Primera API FastAPI - Bootcamp

**👤 Desarrollador**: $(git config user.name)
**📧 Email**: $(git config user.email)
**🔒 Privacidad**: Email configurado según mejores prácticas de GitHub
**📅 Fecha de creación**: $(date '+%Y-%m-%d %H:%M:%S')
**📂 Ruta del proyecto**: $(pwd)
**💻 Equipo de trabajo**: $(hostname)

## 🔧 Configuración Local

Este proyecto está configurado para trabajo en equipo compartido:

- **Entorno virtual aislado**: \`venv-personal/\`
- **Configuración Git local**: Solo para este proyecto
- **Dependencias independientes**: No afecta otras instalaciones

## 🚀 Instalación y Ejecución

\`\`\`bash
# 1. Activar entorno virtual personal
source venv-personal/bin/activate

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Ejecutar servidor de desarrollo
uvicorn main:app --reload --port 8000
\`\`\`

## 🆕 Semana 2 - Consolidación
**Objetivo:** Integrar Type Hints + Pydantic + Endpoints POST

### Nuevos Features (Semana 2)
- ✅ Type hints en todas las funciones
- ✅ Validación automática con Pydantic
- ✅ Endpoint POST para crear productos (/products)
- ✅ Parámetros de ruta (/products/{id})
- ✅ Búsqueda con parámetros query (/search?name=...)

### Endpoints principales
- GET /: Mensaje de bienvenida
- POST /products: Crear nuevo producto
- GET /products: Ver todos los productos
- GET /products/{id}: Ver producto específico
- GET /search?name=...: Buscar productos

### Documentación
http://127.0.0.1:8000/docs

### Mi progreso
- Semana 1: API básica con Hello World  
- Semana 2: API con validación y type hints

### Reflexión
Esta semana aprendí cómo Pydantic facilita la validación de datos y cómo los type hints mejoran la legibilidad y robustez de la API. Crear endpoints POST con modelos Pydantic me permite manejar datos de manera más segura y clara. Fue complicado al inicio, pero se aprendió mucho y ahora la API funciona de manera más profesional.

## 🛠️ Troubleshooting Personal
- Si el entorno virtual no se activa: \`rm -rf venv-personal && python3 -m venv venv-personal\`
- Si hay conflictos de puerto: cambiar \`--port\` en uvicorn
- Si Git no funciona: verificar \`git config user.name\` y \`git config user.email\`
- Si necesitas cambiar el email: usar el email privado de GitHub desde Settings → Emails
EOF
