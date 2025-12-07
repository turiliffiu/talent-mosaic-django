# 🌱 Guida Script Popolamento Database - Talent Mosaic

## 📋 Panoramica

Lo script `populate_db` popola il database con **dati realistici e completi** per una demo professionale di Talent Mosaic.

---

## 🎯 Cosa Crea

### **👤 10 Utenti Realistici**
- Mario Rossi (Senior Software Engineer)
- Giulia Bianchi (UX/UI Designer)
- Luca Verdi (Junior Developer)
- Anna Neri (Marketing Manager)
- Francesco Russo (Data Scientist)
- Sara Ferrari (Project Manager)
- Davide Esposito (DevOps Engineer)
- Elena Conti (Content Specialist)
- Marco Ricci (Business Analyst)
- Chiara Lombardi (HR Specialist)

**Tutti con password:** `demo123`

### **📊 Dati Completi**
- ✅ 6 Categorie Competenze
- ✅ 70+ Competenze specifiche
- ✅ 50+ Associazioni Competenze-Utente
- ✅ 7 Badge con rarità diverse
- ✅ 15+ Badge assegnati agli utenti
- ✅ 6 Eventi (workshop, webinar, conference)
- ✅ 50+ Registrazioni eventi
- ✅ 5 Relazioni Mentorship
- ✅ 15+ Sessioni Mentorship
- ✅ 3 Challenge collaborative
- ✅ 20+ Partecipazioni Challenge

---

## 🎭 Credenziali Demo

### **Login Utenti Demo**

Tutti gli utenti hanno password: **`demo123`**

**Esempi di login:**

| Username | Ruolo | Dipartimento |
|----------|-------|--------------|
| `mario.rossi` | Senior Software Engineer | IT Development |
| `giulia.bianchi` | UX/UI Designer | Design |
| `luca.verdi` | Junior Developer | IT Development |
| `anna.neri` | Marketing Manager | Marketing |
| `francesco.russo` | Data Scientist | Data Analytics |

### **Login Admin**

Se hai creato un superuser:
```
Username: admin (o quello che hai scelto)
Password: <quella che hai scelto>
```

Vai su: `http://localhost:8000/admin/`

---

## 📊 Output dello Script

### **Output Standard**

```bash
$ python manage.py populate_db

🎯 TALENT MOSAIC - Popolamento Database Demo
======================================================================
📊 Inizio creazione dati di esempio...

📁 Categorie Competenze...
  ✓ Programmazione
  ✓ Design & Creatività
  ✓ Marketing & Comunicazione
  ✓ Management & Leadership
  ✓ Data & Analytics
  ✓ Soft Skills
🧠 Competenze...
  ✓ 70 competenze create
👤 Utenti e Profili...
  ✓ 10 utenti creati (password: demo123)
🎯 Associazione Competenze Utenti...
  ✓ 52 associazioni create
🏅 Badge...
  ✓ 7 badge creati
🎖️  Assegnazione Badge...
  ✓ 18 badge assegnati
📅 Eventi...
  ✓ 6 eventi creati
📝 Registrazioni Eventi...
  ✓ 54 registrazioni create
👥 Mentorship...
  ✓ 5 mentorship create
📖 Sessioni Mentorship...
  ✓ 17 sessioni create
🏆 Challenge...
  ✓ 3 challenge create
🎯 Partecipazioni Challenge...
  ✓ 21 partecipazioni create

======================================================================
✅ Popolamento completato con successo!

📊 RIEPILOGO DATI:
   👤 Utenti: 10
   📁 Categorie Competenze: 6
   🧠 Competenze: 70
   🎯 Competenze-Utente: 52
   🏅 Badge: 7
   🎖️  Badge Assegnati: 18
   📅 Eventi: 6
   📝 Registrazioni: 54
   👥 Mentorship: 5
   📖 Sessioni: 17
   🏆 Challenge: 3
   🎯 Partecipazioni: 21

💡 CREDENZIALI DEMO:
   Username: [qualsiasi utente sopra]
   Password: demo123

   Es: mario.rossi / demo123
```

---

## 🎨 Cosa Puoi Vedere nella Demo

### **1. Dashboard Utente**
- Profili completi con bio, dipartimento, job title
- Avatar (se aggiunti manualmente)
- Lista competenze con livelli di proficiency

### **2. Competenze**
- 70+ competenze organizzate in 6 categorie
- Ogni utente ha 4-7 competenze realistiche per il ruolo
- Livelli da Principiante a Esperto

### **3. Eventi**
- Workshop, training, webinar, social
- Eventi futuri e passati
- Registrazioni con partecipanti
- Feedback e rating per eventi completati

### **4. Mentorship**
- 5 relazioni attive mentor-mentee
- Sessioni programmate con note e feedback
- Focus areas specifiche

### **5. Challenge**
- Challenge attive e completate
- Partecipanti con punti guadagnati
- Progress tracking

### **6. Badge**
- Sistema di rarità (Common → Legendary)
- Badge assegnati agli utenti
- Punti associati

---

## 🔧 Personalizzazione

### **Modificare Dati Utenti**

Modifica il file `populate_db.py` alla sezione `create_users()`:

```python
users_data = [
    {
        'username': 'tuo.utente',
        'first_name': 'Tuo',
        'last_name': 'Utente',
        'email': 'tuo@example.com',
        'profile': {
            'job_title': 'Tuo Ruolo',
            'department': 'Tuo Dipartimento',
            # ...
        }
    },
    # Aggiungi altri utenti...
]
```

### **Aggiungere Più Competenze**

Modifica `create_skills()`:

```python
skills_data = {
    'Programmazione': [
        'Python', 'JavaScript', 
        'NuovaSkill',  # ← Aggiungi qui
    ],
    # ...
}
```

### **Cambiare Password Demo**

Nella funzione `create_users()`, cambia:

```python
user.set_password('demo123')  # ← Cambia qui
```

---

## ⚠️ Note Importanti

### **Performance**
- Lo script è veloce (< 5 secondi su hardware moderno)
- Usa `get_or_create` per evitare duplicati
- Safe per esecuzioni multiple

### **Database**
- Funziona con SQLite e PostgreSQL
- Non modifica superuser esistenti
- Preserva dati se non usi `--flush`

### **Immagini**
- Avatar e icon badge **non** sono creati (ImageField)
- Devi caricarli manualmente dall'admin se desiderati

### **Idempotenza**
```bash
# Eseguire 2 volte senza --flush
python manage.py populate_db
python manage.py populate_db  # ← Non crea duplicati
```

---

## 🎯 Scenari Demo Suggeriti

### **Scenario 1: Onboarding Nuovo Utente**
1. Login come `luca.verdi` (junior developer)
2. Mostra profilo incompleto
3. Aggiungi competenze
4. Richiedi mentorship a `mario.rossi`

### **Scenario 2: Programma Mentorship**
1. Login come `mario.rossi` (mentor)
2. Vedi mentorship con `luca.verdi`
3. Programma nuova sessione
4. Lascia feedback

### **Scenario 3: Partecipazione Eventi**
1. Login come qualsiasi utente
2. Sfoglia eventi disponibili
3. Registrati a un workshop
4. Check feedback eventi passati

### **Scenario 4: Challenge Diversità**
1. Vedi challenge attive
2. Partecipa a "Innovazione Inclusiva 2024"
3. Mostra team eterogenei
4. Traccia progressi

### **Scenario 5: Sistema Badge**
1. Login come utente con badge
2. Mostra badge ricevuti
3. Spiega sistema rarità
4. Mostra leaderboard punti

---

## ✅ Checklist Pre-Demo

- [ ] Database popolato (`populate_db` eseguito)
- [ ] Server in running (`runserver`)
- [ ] Credenziali demo pronte (mario.rossi / demo123)
- [ ] Browser aperto su http://localhost:8000
- [ ] Admin panel testato (se serve)
- [ ] 2-3 scenari demo preparati

---

