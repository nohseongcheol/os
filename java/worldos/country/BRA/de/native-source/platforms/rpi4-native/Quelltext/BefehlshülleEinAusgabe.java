// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** Pipes laufen in Abschnitten von 16 KiB nacheinander. Keine Nachbildung von Prozessen oder gleichzeitigen Pipelines. */
public final class BefehlshülleEinAusgabe {
    static int[] eingabeDaten = new int[16384], ausgabeDaten = new int[16384];
    static int eingabeLänge, eingabePosition, ausgabeLänge, eingabeDatei = -1, ausgabeDatei = -1;
    static boolean rohrleitungEingabe, rohrleitungAusgabe;
    static int fehlschlagWert;
    static boolean interaktivErlauben = true;
    public static int istInteraktiv() { return interaktivErlauben && eingabeDatei < 3 && ausgabeDatei < 3 && !rohrleitungEingabe && !rohrleitungAusgabe ? 1 : 0; }
    public static int Ausgabe(int kanalWert, int Wert) {
        if (kanalWert != 1) return 0;
        if (ausgabeDatei >= 3) { int verarbeitetWert = SpeicherDateien.schreiben(ausgabeDatei, Wert); if (verarbeitetWert < 0) fehlschlagWert = verarbeitetWert; return 1; }
        if (!rohrleitungAusgabe) return 0;
        if (ausgabeLänge == ausgabeDaten.length) fehlschlagWert = -28;
        else ausgabeDaten[ausgabeLänge++] = Wert;
        return 1;
    }
    public static int Eingabewert() {
        if (eingabeDatei >= 3) { int verarbeitetWert = SpeicherDateien.lesen(eingabeDatei); return verarbeitetWert == 256 ? -2 : verarbeitetWert; }
        if (rohrleitungEingabe) return eingabePosition < eingabeLänge ? eingabeDaten[eingabePosition++] : -2;
        return -3; // An UART weitergeben.
    }
    static void ausführenVorgang(boolean voranstehendRohrleitung, boolean nachlaufendRohrleitung) {
        rohrleitungEingabe = voranstehendRohrleitung; rohrleitungAusgabe = nachlaufendRohrleitung;
        eingabePosition = 0; ausgabeLänge = 0; eingabeDatei = -1; ausgabeDatei = -1; fehlschlagWert = 0;
    }
    static void endung() {
        Platine.umschaltenEinAusgabe(0);
        if (eingabeDatei >= 3) SpeicherDateien.schließen(eingabeDatei);
        if (ausgabeDatei >= 3) SpeicherDateien.schließen(ausgabeDatei);
        if (rohrleitungAusgabe) { eingabeLänge = ausgabeLänge; for (int schleifeIndex = 0; schleifeIndex < ausgabeLänge; schleifeIndex++) eingabeDaten[schleifeIndex] = ausgabeDaten[schleifeIndex]; }
        eingabeDatei = -1; ausgabeDatei = -1; rohrleitungEingabe = false; rohrleitungAusgabe = false;
    }
}
