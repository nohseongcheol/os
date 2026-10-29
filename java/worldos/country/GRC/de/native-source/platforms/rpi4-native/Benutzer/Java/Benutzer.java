// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** SVC-Anbindung für Java-Werkzeuge auf ARM64 EL0. Wird mit den vorhandenen x86-Werkzeugquellen gebaut. */
public final class Benutzer {
    public static native int dateiDeskriptorÖffnen(int[] Name, int einstellungen);
    public static native int einsDateiByteLesen(int deskriptorEintrag);
    public static native int einsDateiByteSchreiben(int deskriptorEintrag, int Wert);
    public static native int dateiDeskriptorSchließen(int deskriptorEintrag);
    public static native int dateiLesen(int[] Name, int[] Daten);
    public static native int dateiSchreiben(int[] Name, int[] Daten, int Länge);
    public static native int schreiben(String Text);
    public static native int zeichenWertSchreiben(int Wert);
    public static native int argumenteAnzahl();
    public static native String argumente(int Nummer);
    public static native int werkzeugNummer();
    public static native int bildschirmVerbindung(int aktion, int Nummer, int ersterOperand, int zweiterOperand, int dritterOperand, int vierterOperand);
    public static native int bildschirmText(int Nummer, int[] Text, int Länge);
    public static native int bildschirmBreite();
    public static native int bildschirmHöhe();
    public static native int datenstromSteuerung(int aktion, int deskriptorEintrag, int Wert);
    public static native int datenstromVerbinden(int deskriptorEintrag, int adresse, int portWert);
    public static native int netzwerkÖffnen(int portWert);
    public static native int netzwerkSenden(int deskriptorEintrag, int adresse, int portWert, int[] Daten, int Länge);
    public static native int netzwerkEmpfangen(int deskriptorEintrag, int[] Daten, int Länge);
    public static native int netzwerkPort(int deskriptorEintrag);
    public static native int millisekunden();
    public static native int fürAbbildWarten();
    public static native int rechteck(int waagerechtPosition, int senkrechtPosition, int breiteSpannweite, int höheWert, int farbeWert);
}
