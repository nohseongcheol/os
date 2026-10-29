// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Deutsch.eigen;
import java.util.HashMap;
/** Ordnet Suchschlüsseln Werte zu. */
public final class Wörterbuch {
    private final HashMap<String, String> eintragWert = new HashMap<String, String>();
    public String wertAblegen(String tasteMaterial, String Wert) { return eintragWert.put(tasteMaterial, Wert); }
    public String eintragFinden(String tasteMaterial) { return eintragWert.get(tasteMaterial); }
    public boolean führtAusVorhanden(String tasteMaterial) { return eintragWert.containsKey(tasteMaterial); }
    public String eintragTilgen(String tasteMaterial) { return eintragWert.remove(tasteMaterial); }
    public int größe() { return eintragWert.size(); }
    public void inhaltLöschenInhalt() { eintragWert.clear(); }
}
