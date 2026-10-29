// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import Deutsch.eigen.*;

/** Kommunikationsvertragstest mit identischem Bytecode auf OpenJDK und der eigenen JVM. */
public class koreanischNetzbetriebPrüfung {
    public static void main(String[] argumente) throws EingabeAusgabeAusnahme {
        portEmpfangen portWert = verbindungBeförderung.empfängerÖffnen(0);
        Verbindung gastWert = verbindungBeförderung.öffnen("127.0.0.1", portWert.portNummer());
        Verbindung eigentümerBezeichner = portWert.empfangen();
        gastWert.zeitüberschreitung(200); eigentümerBezeichner.zeitüberschreitung(200);
        Prüfpunkte.erfordern(gastWert.verbunden() && !gastWert.istGeschlossen(), "verbinden statuswertWert");
        Prüfpunkte.erfordern(eigentümerBezeichner.portNummer() == gastWert.lokalPortNummer(), "gegenstelleWert portNummer");
        Prüfpunkte.erfordern(gastWert.portNummer() == eigentümerBezeichner.lokalPortNummer(), "lokalGültigkeitsbereich portNummer");
        EingabeDatenstrom Eingabewert = eigentümerBezeichner.Eingabewert(); AusgabeDatenstrom ausgabeSeite = gastWert.Ausgabe();
        byte[] nachricht = Zeichen.kodieren("한글 datenstromWert");
        ausgabeSeite.schreiben(nachricht, 0, nachricht.length); ausgabeSeite.wertAusgeben();
        byte[] empfangenWertText = new byte[nachricht.length];
        int anzahlLesen = 0;
        while (anzahlLesen < empfangenWertText.length) {
            int zusätzlichLesen = Eingabewert.lesen(empfangenWertText, anzahlLesen, empfangenWertText.length - anzahlLesen);
            Prüfpunkte.erfordern(zusätzlichLesen > 0, "예상하지 않은 Datei endung"); anzahlLesen += zusätzlichLesen;
        }
        Prüfpunkte.erfordern(Zeichen.gleichText(Zeichen.datenEntschlüsseln(empfangenWertText), "한글 datenstromWert"), "unterteilWert 읽기와 schreiben");
        ausgabeSeite.schreiben(new byte[] {17, 18});
        byte[] kurzLesen = new byte[2];
        int ersterLesen = Eingabewert.lesen(kurzLesen);
        Prüfpunkte.erfordern(ersterLesen > 0 && kurzLesen[0] == 17, "datenfeldWert lesen");
        if (ersterLesen == 1) kurzLesen[1] = (byte)Eingabewert.lesen();
        Prüfpunkte.erfordern(kurzLesen[1] == 18, "restwertWert lesen");
        eigentümerBezeichner.Ausgabe().schreiben(255);
        Prüfpunkte.erfordern(gastWert.Eingabewert().lesen() == 255, "kodierungWert 없는 한 byteWert");
        ausgabeSeite.schließen();
        Prüfpunkte.erfordern(gastWert.istGeschlossen() && Eingabewert.lesen() == -1, "닫기와 Datei endung");
        Eingabewert.schließen(); Prüfpunkte.erfordern(eigentümerBezeichner.istGeschlossen(), "Eingabewert datenstromWert schließen");
        gastWert.schließen(); eigentümerBezeichner.schließen();
        portWert.zeitüberschreitung(15);
        boolean ausführungZeitüberschreitung = false;
        try { portWert.empfangen(); } catch (WartenZeitüberschreitungAusnahme erwartetFehler) { ausführungZeitüberschreitung = true; }
        Prüfpunkte.erfordern(ausführungZeitüberschreitung, "wertEmpfangen zeitüberschreitung");
        portWert.schließen(); Prüfpunkte.erfordern(portWert.istGeschlossen(), "portEmpfangen schließen");
        DatagrammKanal empfängerEndpunkt = DatagrammKanal.öffnen(0), sendendEndpunkt = DatagrammKanal.öffnen(0);
        empfängerEndpunkt.zeitüberschreitung(200);
        sendendEndpunkt.senden("127.0.0.1", empfängerEndpunkt.portNummer(), "datagramm 한글");
        Prüfpunkte.erfordern(Zeichen.gleichText(empfängerEndpunkt.empfangen(), "datagramm 한글"), "datagramm 송수신");
        sendendEndpunkt.schließen(); empfängerEndpunkt.schließen();
        Prüfpunkte.erfordern(sendendEndpunkt.istGeschlossen() && empfängerEndpunkt.istGeschlossen(), "datagramm schließen");
        Ausgabe.zeileSchreiben("Deutsch Kommunikation überprüfen: verbinden datagramm datenstromWert ausführungZeitüberschreitung schließen");
    }
}
