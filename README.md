# README 

## Requirements: 
* Python 3
* sonarqube attivo su `http://localhost:9000/` loggato con `(admin, admin)`
* Docker 18.03 o superiore (richesto supporto a `host.docker.internal` per connettersi a sonarqube dal container)
	* Installa Docker: `https://docs.docker.com/install/linux/docker-ce/ubuntu/#install-using-the-repository`
	
## Installazione
* Installa Java 14, imposta `JAVA_HOME=/usr/lib/jvm/default-java`
* Installa Sonar su Ubuntu seguendo: `https://www.howtoforge.com/tutorial/how-to-install-sonarqube-on-ubuntu-1804/` o `https://kifarunix.com/install-sonarqube-on-ubuntu/`
	* `wget https://binaries.sonarsource.com/Distribution/sonarqube/sonarqube-8.8.0.42792.zip`
	* Unzippalo da qualche parte e fallo partire con `/path/to/sonarqube/bin/linux-x86-64/sonar.sh start`
	* Non serve fare nuovi utenti, basta che vai in `sonarqube-<versione a caso>/bin/linux-x86-64` e fai `./sonar.sh start` poi vai su `localhost:9000`
	* Salta tutta la roba di PostgreSQL, puoi usare il DB embedded di SonarQube
	* Credenziali di default: `(admin, admin)`, se vuoi modificarle aggiorna anche i valori nel Dockerfile
	* In Sonarqube (su `http://localhost:9000/`) vai su Administration, poi Security, e disattiva `Force user authentication` per potere usare l'API tramite Python

## Modifiche:
* Cambiare i files `groups.csv` e `default_pom.xml` con quelli del proprio scaglione
* Aggiungere le corrette dipendenze all'inizio del file `Dockerfile` per i diversi supporti ai tools
* Aggiungere il proprio `github_access_token` in un file `github_access_token.txt` per accedere ai repository in automatico
* (ottenere token: `https://help.github.com/en/github/authenticating-to-github/creating-a-personal-access-token-for-the-command-line`, metti solo cose di lettura)

## Esecuzione:
* `python m01_init_build.py` per creare in automatico i progetti su sonarqube tramite APIs e creare il file `m02_build.sh`. Prima di eseguire lo script, ricorda di attivare `sonar` (`./sonar.sh start` dalla cartella di `sonar`, vedi sopra), e poi aprilo nel browser su `localhost:9000`.
* `./m02_build.sh` per creare il docker container in cui ad uno ad uno vengono testati i progetti con Maven e inviati i dati a sonarqube
* `python m03_clean_logs.py` per pulire i log in automatico e mantenere solo le informazioni d'interesse
* `python m04_sonar_reports.py` per salvare tutti i dati di sonarqube in un file `.csv`

## OTHER DOCKER COMMANDS
* `docker build . -t <TAG> -f /path/to/Dockerfile`
* `docker run -d <TAG>`
* `docker container ls -a`
* `docker rm <ID>`
* `docker system prune -a -f`: Docker crea una valanga di file temporanei in `/var/lib/docker/overlay2`. Di tanto in tanto, cancellali tutti con questo comando
