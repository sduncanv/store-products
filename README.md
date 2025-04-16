# store-products
Repositorio encargado de la gestión de **productos** en la aplicación principal.

Este repositorio maneja todo lo relacionado con productos: creación, lectura, actualización y eliminación de productos, tipos y archivos relacionados. Forma parte de un ecosistema de microservicios junto a:

- [`store-users`](https://github.com/sduncanv/store-users)
- [`store-tools`](https://github.com/sduncanv/store-tools)

## 🧰 Tecnologías propias del repositorio

- Cloudinary


## Project Structure
```
.
├── Classes
│   ├── Products.py
│   ├── __init__.py
├── Models
│   ├── Products.py
│   ├── ProductsFiles.py
│   ├── ProductsTypes.py
│   ├── __init__.py
├── README.md
├── handlers
│   ├── ProductsHandler.py
├── .env
├── .gitignore
├── locked-requirements.txt
├── pyproject.toml
├── script.py
├── serverless.yml
├── setup.py
```



## ⚙️ Setup and Installation

1. **Create and activate a virtual environment**
  ```sh
    python3 -m venv venv
    source venv/bin/activate
  ```

2. **Make sure you have your variables in .env with your credentials for: database, cloudinary**

3. **Create a requirements.txt**
  ```sh
    python3 script.py
  ```

4. **Install dependencies**
  ```sh
    pip install -r requirements.txt
  ```

5. **Run the application**
  ```sh
    serverless offline
  ```
The server will start and provide an IP address (e.g., `http://127.0.0.1:3003`).

## 🔌 Funciones

### 1. Create a product

**endpoint:** `POST /products`  
**description:** Crea un nuevo producto.

#### Request Body (JSON)

```json
{
  "name": "string",
  "price": int,
  "type_product_id": int,
  "description": "string",
  "user_id": int,
  "file": {
    "filename": "string",
    "image": "string"
  }
}
```
#### Response (JSON)
```json
{
  "statusCode": 200,
  "message": "Ok",
  "data": {
      "product_id": 1
  }
}
```
