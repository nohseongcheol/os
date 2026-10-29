// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Deutsch.eigen;
import java.util.ArrayList;
/** Geordnete Sammlung von Einträgen. Diese Ausgabe stellt Zeichenkettenlisten bereit. */
public final class eintragListe {
    private final ArrayList<String> eintragWert = new ArrayList<String>();
    public void werteHinzufügen(String Wert) { eintragWert.add(Wert); }
    public String lesen(int reihenfolgeWert) { return eintragWert.get(reihenfolgeWert); }
    public String wertErsetzen(int reihenfolgeWert, String Wert) { return eintragWert.set(reihenfolgeWert, Wert); }
    public String eintragTilgen(int reihenfolgeWert) { return eintragWert.remove(reihenfolgeWert); }
    public int größe() { return eintragWert.size(); }
    public boolean istLeerwertWert() { return eintragWert.isEmpty(); }
    public void inhaltLöschenInhalt() { eintragWert.clear(); }
}
