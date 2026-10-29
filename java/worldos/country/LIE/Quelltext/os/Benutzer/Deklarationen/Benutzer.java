// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** API ausschließlich für jkoros-Benutzer-ELF, weder Linux/JVM-JNI noch java.net. */
public final class Benutzer {
    public static native int dateiDeskriptorÖffnen(int[] dateiEintragName, int einstellungenÖffnen);
    public static native int einsDateiByteLesen(int dateiDeskriptor);
    public static native int einsDateiByteSchreiben(int dateiDeskriptor, int byteWert);
    public static native int dateiDeskriptorSchließen(int dateiDeskriptor);
    public static native int bestätigenDateiSpeichergerät(int dateiDeskriptor);
    public static native int dateiLesen(int[] Name, int[] Daten);
    public static native int zeichenWertSchreiben(int Zeichen);
    public static native int dateiSchreiben(int[] Name, int[] Daten, int Länge);
    public static native int schreiben(String inhaltswertWert);
    public static native int argumenteAnzahl();
    public static native String argumente(int Nummer);
    public static native int ausführungErlaubnis();
    public static native int netzwerkÖffnen(int lokalPort);
    public static native int datenSenden(int kennwertWert, int adresse, int zielPort, int[] Daten, int Länge);
    public static native int datenEmpfangen(int kennwertWert, int[] Daten, int grenzwertMillisekunden);
    public static native int netzwerkSchließen(int kennwertWert);
    public static native int eigenAdresse();
    public static native int gesendetAdresse(int kennwertWert);
    public static native int gesendetPort(int kennwertWert);
}
