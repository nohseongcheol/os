# 이름은 셸에서 사용하는 ASCII Fichier nom, Java valeurClasse/함수는 한국어다.
APP_NAMES := hello udp netcheck stress javac java
APP_SOURCE_javac := Utilisateur/Java/OutilJava.java Utilisateur/Java/CompilateurJava.java Utilisateur/Java/RèglesCaractèresIdentifiants.java
APP_ENTRY_javac := CompilateurJava.lancer
APP_SOURCE_java := Utilisateur/Java/OutilJava.java Utilisateur/Java/MachineVirtuelleJava.java
APP_ENTRY_java := MachineVirtuelleJava.lancer
APP_SOURCE_hello := Utilisateur/Exemples/Salutation.java
APP_ENTRY_hello := Salutation.lancer
APP_SOURCE_udp := Utilisateur/Exemples/CommunicationDonnées.java
APP_ENTRY_udp := CommunicationDonnées.lancer
APP_SOURCE_netcheck := Utilisateur/Exemples/testMiseEnRéseau.java
APP_ENTRY_netcheck := testMiseEnRéseau.lancer
APP_SOURCE_stress := Utilisateur/Exemples/boucleRéseau.java
APP_ENTRY_stress := boucleRéseau.lancer
