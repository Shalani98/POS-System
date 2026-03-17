
# POS System

A simple **Point of Sale (POS) system** built with **Flask** and **MySQL**, containerized with **Docker** and deployed via **CI/CD** using **GitHub Actions** and **Railway**.

---

## Features

- Admin login and session management  
- Add, sell, and view products  
- Sales history tracking  
- Supports both **local MySQL** (XAMPP) and **cloud MySQL** via environment variables  
- Fully containerized for CI/CD automation  

---

## Technologies

- **Python 3.10**  
- **Flask**  
- **MySQL**  
- **Docker**  
- **GitHub Actions** (CI)  
- **Railway** (CD)  

---

## Project Structure

```

POS-System/
├─ app.py
├─ templates/
│  ├─ login.html
│  ├─ index.html
│  ├─ add_product.html
│  ├─ sales.html
├─ Dockerfile
├─ requirements.txt
├─ .github/workflows/ci.yml

````

---

## Getting Started

### **Local Development**

1. Install **XAMPP** and start MySQL server  
2. Clone the repo:

```bash
git clone https://github.com/Shalani98/POS-System.git
cd POS-System
````

3. Install dependencies:

```bash
pip install flask mysql-connector-python
```

4. Run locally:

```bash
python app.py
```

* Access your app at: `http://127.0.0.1:5000`
* Database defaults:

| Variable | Value      |
| -------- | ---------- |
| DB_HOST  | localhost  |
| DB_USER  | root       |
| DB_PASS  | (empty)    |
| DB_NAME  | pos_system |

---

### **Docker Development**

1. Build Docker image:

```bash
docker build -t pos-system .
```

2. Run container:

```bash
docker run -d -p 5000:5000 pos-system
```

* Access app at: `http://localhost:5000`

---

### **Cloud Deployment (Railway)**

1. Connect GitHub repo to Railway
2. Add **environment variables** in Railway:

| Variable | Example Value            |
| -------- | ------------------------ |
| DB_HOST  | `<cloud_mysql_host>`     |
| DB_USER  | `<cloud_mysql_user>`     |
| DB_PASS  | `<cloud_mysql_password>` |
| DB_NAME  | `<cloud_mysql_db>`       |
| PORT     | 5000                     |

3. Railway automatically builds and deploys Docker container
4. App URL: `https://<your-service>.up.railway.app`

---

## CI/CD Workflow

* **GitHub Actions CI**:

  1. Triggered on push to `main` branch
  2. Builds Docker image
  3. Runs container and tests Flask app

* **Railway CD**:

  1. Deploys Docker container automatically once CI passes
  2. Supports environment variables for cloud DB
  3. Live application available online

---



* `app.py` uses environment variables to support both **local** and **cloud** DB connections:

```python
host=os.environ.get("DB_HOST","localhost")
user=os.environ.get("DB_USER","root")
password=os.environ.get("DB_PASS","")
database=os.environ.get("DB_NAME","pos_system")
```

* Flask listens on `0.0.0.0` and `PORT` for cloud deployments:

```python
port = int(os.environ.get("PORT",5000))
app.run(host="0.0.0.0", port=port, debug=True)
```

* You **don’t need to modify CI/CD workflow** for future updates. Just push code → CI runs → CD deploys.

---

## License

MIT License

---

```


