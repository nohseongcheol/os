// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64-Maschinengrenze. Zeiger niemals auf einen Java-int kürzen. */
public final class Platine {
    public static native int darstellenBildpunktLesen(int waagerechtPosition, int senkrechtPosition);
    public static native void darstellenBildpunktSchreiben(int waagerechtPosition, int senkrechtPosition, int farbeWert);
    public static native int entferntSteuerung(int artWert, int aktion);
    public static native void endeEntferntBefehl(int statuswertWert);
    public static native void entferntWarten(int statuswertWert);
    public static native void seriellSchreiben(int Wert);
    public static native int seriellLesen();
    public static native int millisekunden();
    public static native int cPUVorrechtEbene();
    public static native int bildschirmVorbereiten();
    public static native int bildschirmBreite();
    public static native int bildschirmHöhe();
    public static native void bildschirmBildpunktAblegen(int waagerechtPosition, int senkrechtPosition, int farbeWert);
    public static native void prozessorAbgeben();
    public static native int aufgabeErstellen(int Nummer);
    public static native int aufgabeStatuswert(int Nummer);
    public static native void stoppen(int statuswertWert);
    public static native int cppPrüfung();
    public static native int benutzerProgrammAusführenVorgang(int Nummer);
    public static native int benutzerProgrammPrüfen();
    public static native int argumenteVorbereiten(int elementeintragAnzahl);
    public static native int benutzerDateiAusführen();
    public static native int linuxDateiAusführen();
    public static native int argumentByte(int Nummer, int position, int Wert);
    public static native int terminal(int aktion);
    public static native int steuerungBenutzerProgramm(int aktion);
    public static native void umschaltenEinAusgabe(int aktion);
    public static native int dateiÜbertragungDienst(int aktion);
    public static native int netzwerkZustand(int eintragWert, int Nummer);
    public static native int netzwerkEinstellungen(int aktion, int adresse, int maskeWert, int netzübergangWert);
    public static native int rückmeldungSenden(int adresse, int reihenfolgeWert);
    public static native int rückmeldungLesen(int eintragWert);
    public static native int abfragenSystem(int eintragWert, int Nummer);
    public static native void stromversorgungAusgeschaltet();
}
