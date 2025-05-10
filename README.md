# 🛡️ Implementación del Patrón Bulkhead con Docker Compose

Este proyecto demuestra el uso del patrón de resiliencia **Bulkhead**, que aísla componentes críticos de un sistema para evitar fallos en cascada. Utiliza **Docker Compose** para contenerizar servicios independientes y un **Nginx** que actúa como proxy inverso y gestor de límites de conexión.

---

## 📌 Objetivo

Simular un entorno donde:
- Dos servicios (`critical` y `slow`) están separados en contenedores distintos.
- Nginx aplica límites de conexiones concurrentes a cada servicio, evitando que una sobrecarga en uno afecte al otro.

---

## 🧱 Componentes del Sistema

| Componente   | Descripción |
|--------------|-------------|
| **nginx**    | Proxy inverso con configuración de `limit_conn` para aislar servicios (bulkhead lógico). |
| **slow**| Microservicio Flask simulado (puede incluir retardos). |
| **critical**| Otro microservicio Flask independiente. |
| **docker-compose** | Orquestador de contenedores para levantar toda la arquitectura. |
| **JMeter**   | Herramienta de pruebas de carga para verificar aislamiento entre servicios. |

---

## ⚙️ Tecnologías Usadas

- 🐳 Docker & Docker Compose
- 🔧 Nginx (como proxy inverso con límites)
- 🐍 Python 3.10 + Flask
- 📊 Apache JMeter (para pruebas de resiliencia)
- 📝 Bash / curl / hey (para pruebas básicas)

---

## 🚀 Prerequisitos

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)
- [Apache JMeter](https://jmeter.apache.org/download_jmeter.cgi) (opcional para pruebas avanzadas)
- (Opcional) [`hey`](https://github.com/rakyll/hey) o `curl`

---

## 📂 Estructura del Proyecto

```
.
├── docker-compose.yml
├── nginx.conf
├── service-critical/
│   ├── Dockerfile
│   └── app.py
├── service-slow/
│   ├── Dockerfile
│   └── app.py
└── README.md
```

---

## 🔧 Pasos para Ejecutar

1. **Clona este repositorio**  
```bash
git clone <https://github.com/juanpg10/bulkhead-demo.git>
```

2. **Levanta los servicios**  
```bash
docker-compose up --build
```

3. **Accede a los servicios**  
- Service Critical: [http://localhost:8080/critical](http://localhost:8080/critical)
- Service Slow: [http://localhost:8080/slow](http://localhost:8080/slow)

---

## 🧪 Verificar el Patrón Bulkhead

### Opción 1: Pruebas básicas con `hey`
```bash
# Sobrecargar service-slow
hey -n 10 -c 5 http://localhost:8080/slow

# Comprobar que service-critical sigue funcionando
curl http://localhost:8080/critical
```

### Opción 2: Pruebas con JMeter
1. Abre JMeter y crea dos Thread Groups:
   - Grupo A: 10 usuarios hacia `/slow`
   - Grupo B: 1 usuario con múltiples peticiones hacia `/critical`

2. Ejecuta ambos grupos en paralelo.

3. Observa que `/critical` mantiene tiempos de respuesta bajos, aunque `/slow` esté saturado.

---

## 🧠 ¿Cómo funciona el patrón Bulkhead aquí?

- Cada microservicio está en su propio contenedor (aislamiento físico).
- Nginx limita el número de conexiones simultáneas por ruta (`limit_conn`), evitando que un servicio consuma todos los recursos.
- Si `service-slow` se satura, `service-critical` sigue funcionando sin degradación: esto **demuestra el aislamiento**.

---

## 🧼 Limpieza

Para detener y eliminar los contenedores:
```bash
docker-compose down
```
