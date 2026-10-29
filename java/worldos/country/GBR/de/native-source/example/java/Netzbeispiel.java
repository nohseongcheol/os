// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import Deutsch.eigen.Verbindung;
import Deutsch.eigen.Argumente;
import Deutsch.eigen.DatagrammKanal;
import Deutsch.eigen.Zeichen;
import Deutsch.eigen.Ausgabe;
import Deutsch.eigen.Prüfpunkte;
import Deutsch.eigen.EingabeDatenstrom;
import Deutsch.eigen.EingabeAusgabeAusnahme;

public class Netzbeispiel {
    public static void ausführenVorgang() throws EingabeAusgabeAusnahme {
        // Host: python3 Werkzeuge/beispielWiedergeben.py --tcp-port 9000 --udp-port 9001
        Verbindung verbinden = Verbindung.öffnen("10.0.2.2", Zeichen.ganzzahlAnalysieren(Argumente.Text(0)));
        try {
            verbinden.zeitüberschreitung(700);
            byte[] nachricht = Zeichen.kodieren("JAVA TCP de\n");
            verbinden.Ausgabe().schreiben(nachricht);
            EingabeDatenstrom Eingabewert = verbinden.Eingabewert();
            for (int Zahl = 0; Zahl < Zeichen.byteAnzahl(nachricht); Zahl++) {
                Prüfpunkte.erfordern(Eingabewert.lesen() == (nachricht[Zahl] & 255), "TCP antwort 불일치");
            }
        } finally { verbinden.schließen(); }
        DatagrammKanal endpunkt = DatagrammKanal.öffnen(0);
        try {
            endpunkt.zeitüberschreitung(700);
            endpunkt.senden("10.0.2.2", Zeichen.ganzzahlAnalysieren(Argumente.Text(1)), "JAVA UDP de");
            Prüfpunkte.erfordern(Zeichen.gleichText(endpunkt.empfangen(), "JAVA UDP de"), "UDP antwort 불일치");
        } finally { endpunkt.schließen(); }
        Ausgabe.zeileSchreiben("JAVA 네트워크 überprüfen: TCP UDP de");
    }
}
