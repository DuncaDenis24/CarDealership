## Descriere Proiect

**CarDealership** este o soluție software modulară, dezvoltată pe o arhitectură bazată pe microservicii, menită să gestioneze operațiunile complete ale unui dealer auto: inventar, închirieri, vânzări și administrare.

Sistemul este împărțit în patru componente principale: un backend robust Spring Boot, o interfață modernă Vue.js, un microserviciu AI pentru interacțiuni bazate pe chat și o aplicație desktop pentru administrarea internă.

## Arhitectura Sistemului

Arhitectura urmează principiul separării responsabilităților (Controller-Service-Repository) și este structurată pe patru componente majore:

### 1. Spring API (Backend Principal)
* **Tehnologie:** Java, Spring Boot
* **Responsabilitate:** Gestiunea principală a datelor (CRUD) și logica de business pentru mașini (`Car`), închirieri (`Rental`), și achiziții (`Purchase`).
* **Model de Date Cheie:**
    * **Car:** Clasa centrală care leagă închirierile (`0..*`) și achizițiile (`0..1`).
    * **Rental/Purchase:** Gestiunea tranzacțiilor cu detalii complete despre clienți și stare.
    * **Servicii Auxiliare:** `EmailService` pentru trimiterea notificărilor.

### 2. Vue SPA (Frontend Public)
* **Tehnologie:** JavaScript, Vue.js
* **Responsabilitate:** Interfața utilizatorului pentru vizualizarea catalogului, completarea formularelor de închiriere (`RentalForm`) și inițierea achizițiilor (`PurchaseForm`).

### 3. Desktop Admin (Interfață Internă)
* **Tehnologie:** Python, PyQt
* **Responsabilitate:** Aplicație desktop internă utilizată de personal pentru administrarea inventarului și a tranzacțiilor (vizualizare, modificare, ștergere). Comunică cu **Spring API** prin REST.

### 4. AI Service (Microserviciu Suplimentar)
* **Tehnologie:** Node.js, Express (presupunând Node pentru serviciul AI din diagramă)
* **Responsabilitate:** Oferă o interfață de chat/chatbot, acționând ca un **Proxy REST** pentru a interoga date din API-ul principal (e.g., `/api/cars`).

---

## Tehnologii Utilizate

| Componentă | Tehnologii Principale |
| :--- | :--- |
| **Backend** | Java 17+, **Spring Boot**, Spring Data JPA, H2/PostgreSQL (DB), REST |
| **Frontend** | **Vue.js** (Sistem SPA), Vue Router, JavaScript/TypeScript |
| **Admin App** | **Python**, **PyQt** (Interfață Desktop), Requests |
| **AI Service** | **Node.js**, Express (sau framework similar) |

---

## Instalare și Rulare Locală

Pentru a rula întregul proiect, trebuie să pornești fiecare microserviciu separat.

### 1. Backend (Spring API)

1.  **Clonați depozitul:**
    ```bash
    git clone [https://github.com/DuncaDenis24/CarDealership.git](https://github.com/DuncaDenis24/CarDealership.git)
    cd CarDealership/spring-api
    ```
2.  **Configurare:** Editați `application.properties` pentru a seta conexiunea la baza de date (sau folosiți setările implicite H2).
3.  **Rulare:**
    ```bash
    ./mvnw spring-boot:run
    # API-ul va rula pe http://localhost:8080
    ```

### 2. Frontend (Vue SPA)

1.  **Navigați:**
    ```bash
    cd ../vue-frontend
    ```
2.  **Instalați dependențele:**
    ```bash
    npm install
    ```
3.  **Rulare:**
    ```bash
    npm run serve
    # Aplicația va rula pe http://localhost:8081 (sau portul configurat)
    ```

### 3. AI Service (Node.js)

*(Presupunând structura tipică Node.js)*

1.  **Navigați:**
    ```bash
    cd ../ai-service
    ```
2.  **Instalați și Rulați:**
    ```bash
    npm install
    node server.js
    ```

---

## Endpoint-uri REST Principale

Toate endpoint-urile sunt prefixate cu `/api`.

| Controller | Endpoint | Metodă | Descriere |
| :--- | :--- | :--- | :--- |
| `CarController` | `/api/cars` | `GET` | Returnează lista tuturor mașinilor. |
| `CarController` | `/api/cars/available` | `GET` | Returnează mașinile disponibile pentru închiriere. |
| `RentalController` | `/api/rentals` | `POST` | Crează o nouă rezervare de închiriere. |
| `PurchaseController`| `/api/purchases/{id}/status` | `PUT` | Actualizează starea unei achiziții. |
