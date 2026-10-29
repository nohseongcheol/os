// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.util.Arrays;

/** Ruft den wirklichen Java-Protokollbehandler in einer JVM auf, um Grenzen und beschädigte Eingaben schnell zu prüfen. */
public final class PaketPrüfung {
    static int wiederholungAnzahl = 0;
    static void überprüfen(boolean Wert) { if (!Wert) throw new AssertionError("case " + wiederholungAnzahl); wiederholungAnzahl++; }
    static int kontrollsumme(int[] Wert, int ausführenVorgang, int Länge, int anfänglichStatuswert) {
        int summeWert = anfänglichStatuswert;
        for (int Nummer = 0; Nummer < Länge; Nummer++) summeWert += Wert[ausführenVorgang + Nummer] << ((Nummer & 1) == 0 ? 8 : 0);
        summeWert = (summeWert & 65535) + (summeWert >>> 16);
        summeWert = (summeWert & 65535) + (summeWert >>> 16);
        return ~summeWert & 65535;
    }
    static void vorbereiten(int Länge) {
        Netzwerkstapel.bereinigenProzess();
        überprüfen(Netzwerkstapel.öffnen(5000) == 3);
        int[] rahmenIndex = Netzwerkstapel.eingabeRahmen;
        Arrays.fill(rahmenIndex, 0);
        for (int Nummer = 0; Nummer < 6; Nummer++) rahmenIndex[Nummer] = Netzwerktreiber.gerätAdresse[Nummer];
        Netzwerkstapel.ablegen16Bit(rahmenIndex, 12, 0x0800);
        rahmenIndex[14] = 0x45; rahmenIndex[22] = 64; rahmenIndex[23] = 17;
        Netzwerkstapel.ablegen16Bit(rahmenIndex, 16, 28 + Länge);
        Netzwerkstapel.ablegen32Bit(rahmenIndex, 26, 0x0a000202); Netzwerkstapel.ablegen32Bit(rahmenIndex, 30, Netzwerkstapel.eigenAdresse);
        Netzwerkstapel.ablegen16Bit(rahmenIndex, 34, 4321); Netzwerkstapel.ablegen16Bit(rahmenIndex, 36, 5000); Netzwerkstapel.ablegen16Bit(rahmenIndex, 38, Länge + 8);
        for (int Nummer = 0; Nummer < Länge; Nummer++) rahmenIndex[42 + Nummer] = Nummer & 255;
        kontrollsummeSetzen(Länge);
    }
    static void kontrollsummeSetzen(int Länge) {
        int[] rahmenIndex = Netzwerkstapel.eingabeRahmen;
        Netzwerkstapel.ablegen16Bit(rahmenIndex, 24, 0); Netzwerkstapel.ablegen16Bit(rahmenIndex, 40, 0);
        Netzwerkstapel.ablegen16Bit(rahmenIndex, 24, kontrollsumme(rahmenIndex, 14, 20, 0));
        int anfänglichStatuswert = Netzwerkstapel.scheinKopfKontrollsumme(Netzwerkstapel.ganzzahl32(rahmenIndex, 26), Netzwerkstapel.eigenAdresse, Länge + 8);
        int summeWert = kontrollsumme(rahmenIndex, 34, Länge + 8, anfänglichStatuswert);
        Netzwerkstapel.ablegen16Bit(rahmenIndex, 40, summeWert == 0 ? 65535 : summeWert);
    }
    static void wertZurückweisen(int Länge) { Netzwerkstapel.prozessRahmen(Länge); überprüfen(Netzwerkstapel.empfangenWertLänge[0] == -1); }
    public static void main(String[] argumente) {
        for (int Länge : new int[]{0, 1, 2, 7, 1023, 1024}) {
            vorbereiten(Länge); Netzwerkstapel.prozessRahmen(Länge + 42);
            überprüfen(Netzwerkstapel.empfangenWertLänge[0] == Länge);
            überprüfen(Netzwerkstapel.empfangenWertAdresse[0] == 0x0a000202 && Netzwerkstapel.empfangenWertPortNummer[0] == 4321);
            for (int Nummer = 0; Nummer < Länge; Nummer++) überprüfen(Netzwerkstapel.empfangenWertDaten[Nummer] == (Nummer & 255));
        }
        for (int Länge = 0; Länge < 42; Länge++) { vorbereiten(0); wertZurückweisen(Länge); }
        vorbereiten(1025); wertZurückweisen(1067);
        vorbereiten(2); Netzwerkstapel.eingabeRahmen[24] ^= 1; wertZurückweisen(44);
        vorbereiten(2); Netzwerkstapel.eingabeRahmen[42] ^= 1; wertZurückweisen(44);
        vorbereiten(2); Netzwerkstapel.ablegen16Bit(Netzwerkstapel.eingabeRahmen, 38, 7); wertZurückweisen(44);
        vorbereiten(2); Netzwerkstapel.ablegen16Bit(Netzwerkstapel.eingabeRahmen, 38, 65535); wertZurückweisen(44);
        vorbereiten(2); Netzwerkstapel.eingabeRahmen[14] = 0x4f; wertZurückweisen(44);
        vorbereiten(2); Netzwerkstapel.eingabeRahmen[14] = 0x44; wertZurückweisen(44);
        vorbereiten(2); Netzwerkstapel.eingabeRahmen[20] = 0x20; kontrollsummeSetzen(2); wertZurückweisen(44);
        vorbereiten(2); Netzwerkstapel.eingabeRahmen[21] = 1; kontrollsummeSetzen(2); wertZurückweisen(44);
        vorbereiten(2); Netzwerkstapel.eingabeRahmen[33] = 99; kontrollsummeSetzen(2); wertZurückweisen(44);
        vorbereiten(2); Netzwerkstapel.eingabeRahmen[0] ^= 1; wertZurückweisen(44);
        vorbereiten(2); Netzwerkstapel.eingabeRahmen[23] = 6; kontrollsummeSetzen(2); wertZurückweisen(44);
        vorbereiten(2); Netzwerkstapel.ablegen16Bit(Netzwerkstapel.eingabeRahmen, 40, 0); Netzwerkstapel.prozessRahmen(44); überprüfen(Netzwerkstapel.empfangenWertLänge[0] == 2);
        int[] ergebnis = new int[4];
        überprüfen(Netzwerkstapel.empfangen(3, ergebnis, 1, 0) == -90);
        überprüfen(Netzwerkstapel.empfangen(3, ergebnis, 4, 0) == -11);
        vorbereiten(2); Netzwerkstapel.prozessRahmen(44); int wertVerwerfen = Netzwerkstapel.verworfenAnzahl;
        Netzwerkstapel.prozessRahmen(44); überprüfen(Netzwerkstapel.verworfenAnzahl == wertVerwerfen + 1);
        Netzwerkstapel.bereinigenProzess(); überprüfen(Netzwerkstapel.öffnen(5000) == 3);
        überprüfen(Netzwerkstapel.öffnen(5000) == -98); überprüfen(Netzwerkstapel.öffnen(0) == 4);
        überprüfen(Netzwerkstapel.öffnen(0) == 5); überprüfen(Netzwerkstapel.öffnen(0) == 6); überprüfen(Netzwerkstapel.öffnen(0) == -24);
        überprüfen(Netzwerkstapel.schließen(4) == 0); überprüfen(Netzwerkstapel.schließen(4) == -9);
        Netzwerkstapel.gefundenAdresse = Netzwerkstapel.netzübergangWert;
        überprüfen(Netzwerkstapel.senden(3, Netzwerkstapel.netzübergangWert, 4321, new int[]{1, 2, 3}, 3) == 3);
        int[] hatGesendet = Netzwerktreiber.kürzlichWert;
        überprüfen(kontrollsumme(hatGesendet, 14, 20, 0) == 0);
        überprüfen(kontrollsumme(hatGesendet, 34, 11, Netzwerkstapel.scheinKopfKontrollsumme(Netzwerkstapel.eigenAdresse, Netzwerkstapel.netzübergangWert, 11)) == 0);
        überprüfen(hatGesendet[42] == 1 && hatGesendet[44] == 3);
        System.out.println("PACKET TEST PASS: " + wiederholungAnzahl + " assertions");
    }
}
