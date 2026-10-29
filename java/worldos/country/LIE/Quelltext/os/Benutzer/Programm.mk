# 이름은 셸에서 사용하는 ASCII Datei Name, Java klasseWert/함수는 한국어다.
APP_NAMES := hello udp netcheck stress javac java
APP_SOURCE_javac := Benutzer/Java/JavaWerkzeug.java Benutzer/Java/JavaÜbersetzer.java Benutzer/Java/Bezeichnerzeichenregeln.java
APP_ENTRY_javac := JavaÜbersetzer.ausführenVorgang
APP_SOURCE_java := Benutzer/Java/JavaWerkzeug.java Benutzer/Java/VirtuelleJavaMaschine.java
APP_ENTRY_java := VirtuelleJavaMaschine.ausführenVorgang
APP_SOURCE_hello := Benutzer/Beispiele/Gruß.java
APP_ENTRY_hello := Gruß.ausführenVorgang
APP_SOURCE_udp := Benutzer/Beispiele/DatenKommunikation.java
APP_ENTRY_udp := DatenKommunikation.ausführenVorgang
APP_SOURCE_netcheck := Benutzer/Beispiele/netzbetriebPrüfung.java
APP_ENTRY_netcheck := netzbetriebPrüfung.ausführenVorgang
APP_SOURCE_stress := Benutzer/Beispiele/netzwerkSchleife.java
APP_ENTRY_stress := netzwerkSchleife.ausführenVorgang
