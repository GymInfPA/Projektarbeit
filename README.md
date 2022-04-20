# Projektarbeit
Projektarbeit im Rahmen der GymInf-Ausbildung

Ziel des Projekts ist die Erstellung einer (kleinen) Datenanalyseplattform die auch im Unterricht von Schülern eingesetzt werden kann, um tabellarische Datensätze zu analysieren.
Im Rahmen verschiedener Open-Data-Initiativen sind viele Daten nun öffentlich zugänglich (in der Schweiz z.B. unter opendata.swiss).
Eine erhebliche Anzahl von falschen und manipulativen Behauptungen, die in sozialen Netzwerken verbreitet werden (Stichwort: Fake News), können durch Recherche und die Analyse der Faktenlage entkräftet werden.
Die oben genannte Plattform soll helfen, Schülern den Umgang mit und die Analyse von Daten näherzubringen, um sie in die Lage zu versetzen, sich selbst eine unabhängige Meinung zu bilden.

Die Analyseplattform besteht aus mehreren Komponenten:
* einer Komponente zum Einlesen und Vorbereiten von Datensätzen, z. B. das Laden von Spreadsheets in Datenstrukturen der Python-Library pandas.
* einer Komponente zum Visualisieren von Daten, z. B. das Plotten von zwei Spalten einer Tabelle als zwei Dimensionen in einem Diagramm.
* einer Komponente zum Anwenden verschiedener statistischer Verfahren auf die Daten, z. B. die Berechnung von Quantilen, Varianzen, Korrelationen, etc.



## Distributionen
### Windows
Alle Dateien inklusive lauffähige Python-Umgebung mit allen notwendigen Paketen vorinstalliert ist als *.exe Datei [hier](/Windows/anavis_v0_5.exe/) verfügbar.

### Linux
Folgende Pakete müssen installiert werden:
- python3-tk (wegen tkinter) - getestet mit Version 3.8.10
- matplotlib - getestet mit Version 3.5.1
- seaborn - geteste mit Version 0.11.2
- pandas - gestetet mit Version 1.4.0

Der Sourcecode des Programms als *.tar.gz ist [hier](/Linux/anavis_v05.tar.gz/) verfügbar.
