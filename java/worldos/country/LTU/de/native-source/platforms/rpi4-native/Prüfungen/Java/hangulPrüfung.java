// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import Deutsch.eigen.Zeichen;
import Deutsch.eigen.Datei;
import Deutsch.eigen.eintragListe;
import Deutsch.eigen.Wörterbuch;
import Deutsch.eigen.Ausgabe;
public class hangulPrüfung {
    public static void main(String[] a) throws Exception {
        String Gruß = "안녕하세요 · 日本語 · العربية · 😀";
        Ausgabe.zeileSchreiben(Zeichen.datenEntschlüsseln(Zeichen.kodieren(Gruß))); Ausgabe.nummerSchreiben(Zeichen.kodePunktAnzahl("한글😀"));
        Datei.schreiben("한글자료.txt", Gruß); Ausgabe.zeileSchreiben(Datei.lesen("한글자료.txt"));
        eintragListe namenListe = new eintragListe(); namenListe.werteHinzufügen("가람"); namenListe.werteHinzufügen("누리"); Ausgabe.zeileSchreiben(namenListe.lesen(1));
        Wörterbuch bedeutungWert = new Wörterbuch(); bedeutungWert.wertAblegen("가람", "강"); System.gc(); Ausgabe.zeileSchreiben(bedeutungWert.eintragFinden("가람"));
        try { Zeichen.datenEntschlüsseln(new byte[] {(byte)0xc0, (byte)0xaf}); } catch (IllegalArgumentException e) { Ausgabe.zeileSchreiben("UTF-8 fehler wertZurückweisen"); }
        Ausgabe.zeileSchreiben("Deutsch bibliothek istFertig");
    }
}
