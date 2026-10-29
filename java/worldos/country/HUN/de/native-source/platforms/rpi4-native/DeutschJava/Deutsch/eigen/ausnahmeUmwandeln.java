// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Deutsch.eigen;

/** Wandelt Standard-Java-Fehler an der deutschen API-Grenze um, ohne die Bedeutung standardmäßiger catch-Klauseln zu ändern. */
final class ausnahmeUmwandeln {
    private ausnahmeUmwandeln() {}
    public static EingabeAusgabeAusnahme eingabeAusgabe(java.io.IOException fehler) {
        if (fehler instanceof EingabeAusgabeAusnahme) return (EingabeAusgabeAusnahme)fehler;
        if (fehler instanceof java.net.SocketTimeoutException) return new WartenZeitüberschreitungAusnahme("Die Wartezeit für die Verbindung wurde überschritten.");
        if (fehler instanceof java.net.UnknownHostException) return new AdresseNachschlagenAusnahme("Die Adresse lässt sich nicht auflösen. Verwenden Sie vorerst eine numerische IPv4-Adresse.");
        if (fehler instanceof java.io.FileNotFoundException) return new FehlendDateiAusnahme("Die Datei lässt sich nicht öffnen.");
        if (fehler instanceof java.net.SocketException) return new KommunikationAusnahme("Verbindungsaufbau fehlgeschlagen: " + fehler.getMessage());
        return new EingabeAusgabeAusnahme("Ein-/Ausgabe fehlgeschlagen: " + fehler.getMessage());
    }
    public static RuntimeException befehlAusführen(RuntimeException fehler) {
        if (fehler instanceof java.lang.NumberFormatException) return new NummerFormatFehlschlag("Prüfen Sie das Zahlenformat und den Wertebereich.");
        if (fehler instanceof java.lang.IllegalArgumentException) return new UngültigArgumentAusnahme("Prüfen Sie Wert und Bereich des Arguments.");
        if (fehler instanceof java.lang.ArrayIndexOutOfBoundsException) return new DatenfeldGrenzenAusnahme("Der Feldindex liegt außerhalb des gültigen Bereichs.");
        if (fehler instanceof java.lang.StringIndexOutOfBoundsException) return new ZeichenketteGrenzenAusnahme("Der Zeichenkettenindex liegt außerhalb des gültigen Bereichs.");
        if (fehler instanceof java.lang.IndexOutOfBoundsException) return new GrenzenAusnahme("Der zulässige Bereich wurde überschritten.");
        if (fehler instanceof java.lang.NullPointerException) return new NullverweisVerweisAusnahme("Die Referenz ist leer.");
        return new AusführungAusnahme(fehler.getMessage());
    }
}
