# Progetto di Tirocinio

## Indice
- [Descrizione](#Descrizione)
- [Struttura](#Struttura)
- [Installazione](#Installazione)
- [Demo](#Demo)
- [Contatti](#Contatti)

## Descrizione

Progetto di Tirocinio - Università di Trento

Descrizione: l'applicazione sviluppata fa uso del protocollo MQTT per lo scambio di messaggi. Di seguito le caratteristiche principali del progetto:
- Una dashboard accessibile via internet permette a uno o più subscriber di iscriversi a uno o più topic, riguardati statistiche di rete, ad esempio ping.
- Uno o più publisher pubblicheranno i dati sui topic specifici.
- Quando i dati vengono pubblicati su un topic, i subscriber, se iscritti al topic, visualizzano i messaggi tramite la dashboard
- Dei grafici, uno per ogni topic, mostrano l'andamento dati
- I subscriber possono iscriversi e disiscriversi ai topic in ogni momento, nonchè scegliere se visualizzare i grafici o meno tramite del pulsanti. 

L'applicazione funziona correttamente con qualsiasi numero di publisher e di subscriber


[Torna all'indice](#Indice)


## Struttura

Il progetto è composto da 3 file principali:
- generator.py: responsabile della pubblicazione dei dati sui topic, svolge il ruolo del publisher;
- index.html: è l'interfaccia utente dell'applicazione, contiene la dashboard e permette l'interazione con l'utente, svolge il ruolo di subscriber;
- app.py: che rappresenta il nucleo del sistema sviluppato, gestendo le comunicazioni e lo scambio dei messaggi tra le diverse entità.

[Torna all'indice](#Indice)


## Installazione

Iniziamo con le configurazioni preliminari:
1. Scaricare il progetto con i comandi git
2. Installare e avviare Mosquitto (broker MQTT): ```sudo apt install mosquitto```. Una volta installato dovrebbe avviarsi automaticamente, altrimenti avviarlo manualmente con: ```sudo systemctl start mosquitto```
3. Entrare nell'ambiente virtuale: ```source venv/bin/activate```
4. Scaricare tutte le dipendenze necessarie: ```pip install -r requirements.txt```


Ora il sistema è pronto per essere utilizzato:
5. aprire 2 terminali:

   - nel primo avviare app.py con ```python3 app.py```;

   - nel secondo avviare generator.py con ```python3 generator.py```

6. Accedere alla dashboard via internet con ```http://localhost:5000```

7. Interagire con l'applicazione (iscriversi e disiscriversi ai topic, mostrare e nascondere grafici)


[Torna all'indice](#Indice)

## Demo
Video dimostrativo di come funziona l'applicazione: [**Demo Link**](https://drive.google.com/file/d/1SqHk8vh59EZip0AyMr3dwAgmGSyi9bqv/view?usp=sharing) 

[Torna all'indice](#Indice)

## Contatti

Riccardo Zannoni - riccardo.zannoni@studenti.unitn.it

[Torna all'indice](#Indice)



