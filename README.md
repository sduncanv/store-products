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

### 1. Create a type product

**endpoint:** `POST /types_products`  
**description:** Crea un nuevo tipo de producto.

#### Request body (JSON)

```json
{
  "name": "string",
  "description": "string"
}
```
#### Response
```json
{
  "statusCode": 200,
  "message": "Ok",
  "data": {
    "type_product_id": 1
  }
}
```

### 2. Get a type product

**endpoint:** `POST /types_products`  
**description:** Create a type product.

#### Params (Optionals)

```json
type_product_id: int
```
#### Response
```json
{
  "statusCode": 200,
  "message": "Ok",
  "data": [
    {
      "type_product_id": 1,
      "name": "Electrónica",
      "description": "Productos de tipo electronica.",
      "active": 1,
      "created_at": "2025-04-14 22:14:21",
      "updated_at": "2025-04-14 22:14:21"
    },
    {
      "type_product_id": 2,
      "name": "Calzado",
      "description": "Productos de tipo calzado.",
      "active": 1,
      "created_at": "2025-04-15 16:36:48",
      "updated_at": "2025-04-15 16:36:48"
    }
  ]
}
```

### 3. Create a product

**endpoint:** `POST /products`  
**description:** Crea un nuevo producto.

#### Request body (JSON)

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

### 4. Get a product

**endpoint:** `GET /products`  
**description:** Get a product or all products.

#### Params (Optionals)

```json
product_id: int
```
#### Response
```json
{
  "statusCode": 200,
  "message": "Ok",
  "data": [
    {
      "product_id": 1,
      "name": "Iphone",
      "price": 1000,
      "type_product_id": 1,
      "description": "Celular Iphone.",
      "user_id": 1,
      "active": 1,
      "created_at": "2025-04-15 17:05:32",
      "updated_at": "2025-04-15 17:05:32",
      "url": "https://res.cloudinary.com/cloudname/image/upload/filename",
      "product_type_name": "Electrónica"
    }
  ]
}
```