secretarius
===========

A personal information manager, trying to provide a fully integrated cloud experience.

Ich bin sehr dankbar für jeden, der mir auch nur einen Tipp oder seine Meinung hierzu abgibt. Ich bin sehr offen für jede Form von Vorschlägen und natürlich auch Beteiligung. Ich kann auch gerne Featurevorschläge sammeln. Nur mir erzählen, dass die Idee komplett sinnlos ist, wird nicht klappen, dafür habe ich mich schon zusehr damit beschäftigt.
Vermutlich sollte dieser Text in Englisch sein, um ihn besser zu veröffentlichen, aber ich bin in Deutsch besser in der Lage meine Gedanken zu fokussieren.

Die Idee:

Im täglichen Umgang am Computer und mit der Umwelt, sind wir den Umgang mit vielen Unterschiedlichen Informationsquellen gewohnt. Wir haben viele Programme, die nur dafür da sind, Informationen zu speichern und aufzuarbeiten.
Informationen können aus einem breitem Spektrum kommen, die wichtigsten sind selbst generiert oder Bestandteil von Kommunikation.
Die Idee von secretarius ist es die Informationen zentral zu speichern und zu verwalten.
Es gibt für viele Formen von Informationen tolle Programme, die die Daten aufbereiten und zwischen unterschiedlichen Geräten synchronisieren.
Das Problem: 
1. Jedes Programm ist anders, man muss sich immer wieder an die Bedienung und kleinen Macken gewöhnen.
2. Synchronisation von Daten ist komplett uneinheitlich und kompliziert. Für jeden Anwendungstyp muss ich auf jedem Gerät eine Anwendung installieren und sehen, dass die Daten synchronisiert sind.
3. Integration: Es gibt soviele Unterschiedliche Formen von Information bzw. Kommunikation. So gut jede Anwendung, die sich auf einen Informationtyp beschränkt auch sein kann. Sie ist nie in der Lage sie in den Kontext und die große Übersicht, in der man sie meiner Meinung nach heutzutage braucht ich sie gerne hätte zu setzen.

Mir ist bewusst, das so ein Programm nie vollständig sein kann und wie ein Mammutprojekt aussieht. Ist es vermutlich auch...
Deswegen ziele ich persönlich auch darauf ab, dass das Programm am Anfang vor allem die Informationen verarbeiten kann, die für mich persönlich am relevantesten sind.
Und offensichtlich muss man dabei darauf achten, dass es einfach ist beliebig neue Datentypen einzupflegen.
Außerdem sind die Anzahl der Funktionen, die ein Programm, wie z. B. ein Chatclient oder Mailclient zum Beispiel braucht gar nicht so groß. Ich bin ein Fan von schlanker Software. Wenn man all diese Programme verschmilzt hat man natürlich auch den Vorteil, dass unnötige Redundanzen wegfallen.

Das Projekt heißt secretarius, weil mir kein besserer Name eingefallen ist. Er ändert sich auch manchmal... Für Vorschläge bin ich offen.

Die Bausteine:
* Die Datenbank bietet eine sichere Lagerung aller Daten, sie ist das Herz der Sache. Ich arbeite hierbei momentan mit Postgresql.
* Kern des Projekts sind eigentlich nur die Tabellen in der Datenbank.
* Ein HTTP Server geschrieben mit Flask und Python der ein Restful API bereitstellt, die den Clients die SQL Arbeit abnimmt. Diesen zu verwenden ist natürlich optional.
* Daemons und Watcher, diese Anwendung braucht selbstverständlich viele Schnittstellen, die Informationen von überall einspeisen oder aussenden: Mailclients, Chatclients, Systemüberwacher, RSS-Reader... Ein paar Daten sind eventuell vom Konzept her so, dass man auf der Datenbank Überwachungsprogramme braucht, die die Integrität der Daten gewährleisten. Dies würde ich aber gerne vermeiden z. B. durch intelligentes Design oder intelligente Client Libraries.
* Libraries: Damit das schreiben von Clients und Daemons möglichst einfach ist, sollte es Libraries geben, die die Kommunikation mit der Datenbank erleichtern.
* Clients, Hier gibt es ein breites Spektrum, je mehr es gibt desto besser. CLI, Webinterfaces, GUI-Tools, Mobile-Apps, Pop-Up Notifier... Die Idee ist, dass jeder Client schlank sein kann/sollte, denn er kann sich ja auf die Datenbank verlassen. Man kann sowohl Clients schreiben, die genau eine Aufgabe übernehmen. bspw. Ein einfaches Chatfenster für genau einen Kontakt. Aber auch welche, die beliebige Informationen kombinieren und im Kontext anzeigen.
* Schnittstellen: Damit diese Programm irgendeine Chance hat verwendet werden zu können, sollte es Möglichkeiten für bewährte Programme geben damit zu interagieren. Ich möchte mich nicht einschränken lassen durch andere Protokolle, dass heißt die Datenbank behält die Datenhoheit. Wenn Protokolle damit nicht klar kommen gibt es halt nur Lesezugriff oder gar keine Kompatibiltät.
Export Möglichkeiten könnten sein: LDAP für Kontakte, iCal Dateien für Termine, POP oder sogar IMAP für Mails, RSS...
Dem messe ich allerdings momentan keine sehr hohe Priorität bei...

GTD
Meine Idee ist es die Informationen mit dem Getting Things Done Konzept zu verarbeiten:
Neu Informationen landen in der Inbox.
Das meiste wird entweder direkt gelöscht oder einfach archiviert.
Man kann eine Beliebige Information auch vertagen und einstellen, dass man sie später noch einmal sehen möchte (dann landet sie wieder in der Inbox)
Man kann entscheiden, dass die Information bearbeitet werden muss. Nach Getting Things Done, sollte man das tun, wenn es schneller als 2 Minuten geht.
Ansonsten erstellt man ein Projekt, wenn mehrer Schritte zum erfüllen der Aufgabe nötig sind, oder einen Task, der in eine der ASAP-Kontexte einsortiert wird.

GTD muss man allerdings nicht verwenden, wenn man secretarius verwendet.
Das schöne ist ja, dass man die Clients, die man verwendet, frei wählen kann.

Informationen:
Dies sind alles Informationen, die verarbeitet werden könnten. Das ist natürlich immer individuell komplex/nötig.

Notizen (möglichen Formen, sind Text, Bild oder Sound)
Emails
Chatnachrichten (Jabber, IRC, ICQ... jedes beliebige Protokoll)
Dokumente (pdf..., eingescannt?)
News, Blogs (RSS-Feeds)
SMS?
Lesezeichen
Termine
Tasks
Projekte
Systemnachrichten

Roadmap:
Mir ist es am wichtigsten zuerst die Todo Funktionalität einzubauen. Als erste Information brauche ich also nur Notizen.
Als erste Client stelle ich mir ein paar CLI für Input vor, eventuell einen Notifier mit xosd und ansonsten Webinterfaces. Diese sind schnell und einfach zu erstellen, und überall zu erreichen.

Abschnitte:
für Detaillierte Planung:



Libraries

Welche Libraries braucht man denn?

Daemons

Ein Daemon verbindet sich mit einer konfigurierten Liste von Jabber Accounts.
Ein Daemon sollte sich um Emails kümmern. Er sollte optimalerweise mit IMAP Push oder direkt als Hook auf dem Mailserver arbeiten um Zeitverzögerungen zu vermeiden.
Auf jedem System kann man einen Daemon laufen lassen, der relevante Informationen über den Zustand sammelt und eventuell in die Datenbank speist.
Ein Daemon sollte eine konfigurierte Liste von RSS-Feeds watchen und neue Einträge einspeisen.
Abhängig von der Implementierung und den gewünschten Features wird es auch noch einen Daemon geben müssen, der die Konsistenz der Datenbank prüft.

Clients

Diese Clients haben alle eine einzelne Aufgabe wahrzunehmen und sollten einfach nur die Möglichkeit einen anderen aufzurufen anbieten sobald man ihre Kernkompetenz verlässt.

Eine Konfigurationsansicht wäre wahrscheinlich sehr sinnvoll, ist am Anfang aber nicht wichtig, da man ja durch editieren der Datenbank alles einstellen kann, was man will.

Eine Art Hauptmenü könnte nicht schaden. Mit Links zu allen relevanten Anzeigen. Schneller Zugriff auf die Suchfunktion und die ToDoLists ist essentiell. Die Funktion neue Notiz sollte überall zur Verfügung stehen. Wahrscheinlich auch neuer Termin. Hier könnte man auch einfach die Lesezeichen zur Verfügung stellen. (In der Webinterface Implementierung ist dies hier wahrscheinlich eine exzellente Startseite.

Notifications
Alles was ein Inbox und Urgent Flag hat sollte dafür sorgen, dass eine Nachricht über das Betriebssystem gesendet wird. Urgent ist gedacht hauptsächlich für Kommunikationen, die bestimmte Bedingungen erfüllen und kritische Systemnachrichten. Es sollte nicht zuviel sein, die meisten Dinge können warten und sollten nicht von der Arbeit ablenken, bis man das nächste mal in die Inbox sieht.

Inbox-View
Hier soll immer genau ein Element angezeigt werden. Nach Möglichkeiten in einer gut aufgearbeiteten Weise.
Folgende Optionen sollten zur Verfügung stehen: Löschen, Vertagen/in den Pot "später", Archivieren
Außerdem sollten noch folgende Optionen zur Verfügung stehen: "Erstelle verknüpftes Project", "Erstelle verknüpften Task", "Erstelle verknüpften Termin"

Later View
Hier kann man alle Informationen sehen, die auf einen unbestimmten Zeitpunkt vertagt wurden. Anders als die Inbox sollte dies nach Möglichkeiten eine Listen Ansicht sein.
Optionen: Löschen, Vertagen, Archivieren, Project, ToDO, Termin

ProjectView
Hier sollte ein guter Überblick über die Projekte erstellt werden können. Jedes Projekt kann einen Parent haben. Die Projekt Liste zeigt also alle ohne Parent an und davon ausgehend den Rest in Baumstruktur. Projekt und ToDos können immer auf eine beliebige Menge Referenzmaterialien verlinken. Die Frage ist, wie man die in jedem Kontext zur Verfügung stellt. Eventuell ein Link zu einer angepassten Anfragen an den Search View.

ToDoLists
Eine ToDo List zeigt die unsortierte Liste von ToDos, die in ihr stehen. Vielleicht will man ToDo Listen doch sortieren? Wahrscheinlich ist eine Möglichkeit Prioritäten festzulegen sinnvoll.

BuddyList
In der BuddyList sollen alle Kontakte angezeigt werden, Jeder Kontakt ein- bis keinmal. Sortiert werden kann nach unterschiedlichen Kriterien. Sinnvoll wäre: Online Status, Anzahl der Nachrichten von diesem Nutzer, Zeitpunkt der letzten Nachricht von diesem Nutzer, Alphabetisch. Hier sollte es eine einfach erreichbare Such-/Filterfunktion geben.

ContactView
Hier soll ein Kontakt komplett betrachtet werden können. Die Kontaktinformationen bearbeitet werden. Außerdem sollte eine Liste aller Kommunikationsformen mit diesem Kontakt angezeigt werden. Jeweils eventuell mit den letzten Nachrichten. Funktionen wie, Email verfassen und Chatöffnen sollten hier selbstverständlich existieren. btw für Kontakte hatte ich diese total coole Idee: Man könnte sie in Kreisen organisieren.

Chatwindow Single/Chatroom
Dieses Fenster soll wirklich nur den Chatverlauf (auch vergangener Chats) und eine Absende Zeil zeigen. Im Falle eines Chatraums natürlich auch die UserList. Die UserList könnte man auch irgendwie floating immer anzeigen, dann zeigt sie eventuell halt nur einen Benutzer dort sollte auf jeden Fall einen Link auf die Kontaktansicht existieren.

Search
Hier mit sollte es möglich sein beliebige Informationen, die in der Datenbank sind zu suchen. Eventuell möchte man unterschiedliche Suchfenster für Emails / Notes / Ähnliches haben, aber dies kann man aber auch über Filteroptionen realisieren. Insbesondere sollte es auch eine Suche geben, die wirklich "Alles" dursucht. Ein Fulltext Search gerade in Emails, wäre super.

Write Email
Auch ein sehr einfaches Menü, Ein paar Header Optionen, Ein Textfeld, anhängen. Optionen "Senden", "Save as Draft", "löschen"
Cool wäre ein Feld, dass eine Art Listenmanagment übernimmt, so dass jeder Empfänger nur sich unter To: sieht. Außerdem sollte in jedem Header die Möglichkeit bestehen Kreise einzutragen.

Calendar View
Day
Eine schlichte Tabelle, oben eine Auflistung Taglanger Ereignisse,
links die Zeit Skala, daneben die Termine. Diese Ansicht sollte man einfach in der Breite (Anzahl der Tage) beliebig einstellen können.

Features
Jabber, Mail, Notes, Facebook, Twitter, Google+, RSS, Blogs, Banking, Documente, Mensa integration, Wetter App, Lesezeichen
