// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** Eingeschränkte native Übersetzergrenze ausschließlich für x86-Anweisungen und physische Adresszugriffe. */
public final class Gerät {
    public static native int dateiSpeicher();
    public static native int javaDateiBündel();
    public static native int javaDateiBündelGröße();
    public static native int einAusgabeByteLesen(int Nummer);
    public static native void einAusgabeByteSchreiben(int Nummer, int Wert);
    public static native int speicherLesen(int adresse);
    public static native void speicherSchreiben(int adresse, int Wert);
    public static native int startvorgangMarkierung();
    public static native int startvorgangInformation();
    public static native int datenfeldNutzung();
    public static native void kurzzeitigTunAbgeben();
    public static native void anhaltenAusführung();
    public static native void prüfungBeenden(int Wert);
    public static native int einAusgabeGanzzahlLesen(int Nummer);
    public static native void einAusgabeGanzzahlSchreiben(int Nummer, int Wert);
    public static native void einAusgabeKurzSchreiben(int Nummer, int Wert);
    public static native int einAusgabeKurzLesen(int Nummer);
    public static native void benutzerProgrammVorbereiten();
    public static native void benutzerLöschenInhaltInhalt();
    public static native int benutzerProgrammAusführenVorgang(int eintragAdresse, int operandStapelAdresse);
    public static native int millisekunden();
    public static native int benutzerVerbleibendMillisekunden();
    public static native int AusführdateiBündel();
    public static native int ausführdateiBündelGröße();
    public static native int netzwerkSpeicher();
}
