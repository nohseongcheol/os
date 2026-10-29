// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Deutsch.eigen;
/** Befehlszeilenargumente, die die eigene JVM an die Einstiegsmethode übergibt; ohne Klassennamen. */
public final class Argumente {
    private Argumente() {}
    public static native int elementeintragAnzahl();
    public static native String Text(int ordnungszahlIndex) throws GrenzenAusnahme;
}
