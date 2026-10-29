// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Finnland.JFinOS.Prüfungen;

import java.nio.charset.StandardCharsets;
import java.util.Arrays;
import Finnland.JFinOS.Speicherraum.SpeicherVerwalter;
import Finnland.JFinOS.Speicherraum.SeiteVerwalter;
import Finnland.JFinOS.Eingabewert.eingabeEreignis;
import Finnland.JFinOS.Aufgabe.prozessWert;
import Finnland.JFinOS.Systemaufruf.Systemaufruf;
import Finnland.JFinOS.DateiSystem.AusführdateiLader;
import Finnland.JFinOS.Betriebskern.Betriebskern;
import Finnland.JFinOS.Wirtssystem.WirtssystemHardware;
import Finnland.JFinOS.unterbrechen.UnterbrechenVerwalter;
import Finnland.JFinOS.deskriptorEintrag.GlobalDeskriptorTabelle;
import Finnland.JFinOS.speichergerätGerät.FortgeschrittenTechnikAnhang;
import Finnland.JFinOS.Gerät.PeripherieBusVerwalter;
import Finnland.JFinOS.Netzwerkstapel.NetzwerkWerkzeuge;
import Finnland.JFinOS.Netzwerkstapel.NetzwerkSchicht;
import Finnland.JFinOS.Gerät.Uhr;
import Finnland.JFinOS.deskriptorEintrag.AufgabeStatuswertSegment;
import Finnland.JFinOS.Bildschirm.zeichenDarstellen;
import Finnland.JFinOS.DateiSystem.hauptPartitionTabelle;

public final class allePrüfung {
    private static int durchgangAnzahl;

    private allePrüfung() {
    }

    public static void main(String[] parameterArgument) {
        WirtssystemHardware Gerät = new WirtssystemHardware();
        Betriebskern betriebskernWert = new Betriebskern(Gerät);
        betriebskernWert.ausführenVorgang();

        speicherPrüfung(betriebskernWert);
        seiteVerwaltungPrüfung(betriebskernWert);
        dateienUndProzessePrüfung(betriebskernWert);
        eLFPrüfung(betriebskernWert);
        eingabePrüfung(betriebskernWert);
        hardwarePrüfung(Gerät);
        unterbrechungenUndDeskriptorenPrüfung();
        speichergerätUndNetzbetriebPrüfung();
        bildschirmUndUhrPrüfung();

        System.out.println("JFinOS Prüfungen durchgangWert: " + durchgangAnzahl);
    }

    private static void speicherPrüfung(Betriebskern betriebskernWert) {
        SpeicherVerwalter verwalterWert = betriebskernWert.Speicherraum();
        int ersterAdresse = verwalterWert.ausgerichtetZuteilen(100, 64);
        überprüfen((ersterAdresse & 63) == 0, "ausrichtenWert speichergerätZuteilen");
        verwalterWert.byteWertSchreiben(ersterAdresse, (byte) 0x5a);
        überprüfen(verwalterWert.byteWertLesen(ersterAdresse) == (byte) 0x5a, "물리 Speicherraum 읽고 schreiben");
        int davorBenutzen = verwalterWert.benutztGröße();
        verwalterWert.speichergerätFreigeben(ersterAdresse);
        überprüfen(verwalterWert.benutztGröße() < davorBenutzen, "Speicherraum speichergerätFreigeben");
    }

    private static void seiteVerwaltungPrüfung(Betriebskern betriebskernWert) {
        SeiteVerwalter verwalterWert = betriebskernWert.seiteVerwaltung();
        SeiteVerwalter.AdresseRaum elternknotenRaum = verwalterWert.neuAdresseRaum();
        verwalterWert.abbildungSeite(elternknotenRaum, 0x1000, true);
        verwalterWert.byteWertSchreiben(elternknotenRaum, 0x1010, (byte) 7);
        SeiteVerwalter.AdresseRaum kindRaum = verwalterWert.klonenKopierenEingeschaltetSchreiben(elternknotenRaum);
        verwalterWert.byteWertSchreiben(kindRaum, 0x1010, (byte) 9);
        überprüfen(verwalterWert.byteWertLesen(elternknotenRaum, 0x1010) == 7, "schreiben 시 wertKopieren elternknotenWert 격리");
        überprüfen(verwalterWert.byteWertLesen(kindRaum, 0x1010) == 9, "schreiben 시 wertKopieren kindWert schreiben");
    }

    private static void dateienUndProzessePrüfung(Betriebskern betriebskernWert) {
        byte[] inhaltswertWert = "안녕하세요".getBytes(StandardCharsets.UTF_8);
        betriebskernWert.DateiSystem().dateiAnhängen("Prüfungen", inhaltswertWert);
        prozessWert elternknotenWert = betriebskernWert.ersterProzess();
        Systemaufruf aufrufen = betriebskernWert.Systemaufruf();
        int deskriptorEintrag = aufrufen.öffnen(elternknotenWert, "/Prüfungen", Systemaufruf.ausschließlichMerkmalbitLesen);
        überprüfen(deskriptorEintrag >= 3, "Datei öffnen");

        byte[] zielEmpfangen = new byte[inhaltswertWert.length];
        überprüfen(aufrufen.lesen(elternknotenWert, deskriptorEintrag, zielEmpfangen, zielEmpfangen.length) == inhaltswertWert.length, "Datei lesen");
        überprüfen(Arrays.equals(inhaltswertWert, zielEmpfangen), "Datei inhaltswertWert");
        überprüfen(aufrufen.bewegenPosition(elternknotenWert, deskriptorEintrag, 0, Systemaufruf.startenSuchen) == 0, "Datei position bewegenWert");

        int geklontDeskriptor = aufrufen.duplikatDeskriptor(elternknotenWert, deskriptorEintrag);
        überprüfen(geklontDeskriptor >= 0, "deskriptorEintrag klonenWert");
        prozessWert kindWert = aufrufen.klonenProzess(elternknotenWert);
        überprüfen(kindWert.bezeichnerWert() != elternknotenWert.bezeichnerWert(), "prozessWert bezeichnerWert 분리");
        überprüfen(kindWert.elternknotenBezeichner() == elternknotenWert.bezeichnerWert(), "elternknotenWert prozessWert bezeichnerWert");
        überprüfen(aufrufen.schließen(kindWert, deskriptorEintrag) == 0 && elternknotenWert.dateiDeskriptor().istÖffnen(deskriptorEintrag), "kindWert schließen 격리");

        int vorherigEnde = aufrufen.programmAbbrechenVergrößern(elternknotenWert, 8192);
        überprüfen(vorherigEnde == 0x06000000, "Programm endung 늘리기");
        überprüfen(elternknotenWert.programmAbbrechen() == 0x06002000, "Programm endung 반영");
        überprüfen(kindWert.programmAbbrechen() == 0x06000000, "과정별 Programm endung 격리");

        kindWert.verlassenProzessProgramm(7);
        überprüfen(aufrufen.fürKindWarten(elternknotenWert, kindWert.bezeichnerWert(), false) == (7 << 8), "kindWert verlassenProzessProgramm abwarten");
        überprüfen(aufrufen.istZugänglich("Prüfungen", 1) == -13, "befehlAusführen erlaubnisWert wertZurückweisen");
        überprüfen(aufrufen.benutzerBezeichner() == 0 && aufrufen.gruppeBezeichner() == 0, "사용자와 무리 bezeichnerWert");
        überprüfen("/".equals(aufrufen.aktuellAufgabeListe(2)) && aufrufen.umschaltenAufgabeListe("/") == 0, "aktuellElementeintrag Aufgabe eintragListe");
        überprüfen(aufrufen.istTerminal(elternknotenWert, 1), "표준 Ausgabe TerminalEinAusgabe");
        überprüfen("JFinOS".equals(aufrufen.systemEinzelheiten().systemName()), "betriebSystemWert systemInformation");
    }

    private static void eLFPrüfung(Betriebskern betriebskernWert) {
        byte[] Daten = new byte[92];
        Daten[0] = 0x7f;
        Daten[1] = 'E';
        Daten[2] = 'L';
        Daten[3] = 'F';
        Daten[4] = 1;
        Daten[5] = 1;
        ganzzahlWertSchreiben(Daten, 24, 0x04001000);
        ganzzahlWertSchreiben(Daten, 32, 52);
        kurzGanzzahlSchreiben(Daten, 46, 40);
        kurzGanzzahlSchreiben(Daten, 48, 1);
        ganzzahlWertSchreiben(Daten, 56, 8);
        ganzzahlWertSchreiben(Daten, 60, 2);
        ganzzahlWertSchreiben(Daten, 64, 0x04002000);
        ganzzahlWertSchreiben(Daten, 72, 64);

        AusführdateiLader.abbild abbildWert = new AusführdateiLader().Prüfpunkte(Daten);
        überprüfen(abbildWert.adresseStarten() == 0x04001000, "ELF ausführenVorgang adresse");
        überprüfen(abbildWert.abschnitteListe().size() == 1 && abbildWert.abschnitteListe().get(0).artWert() == 8, "ELF 빈 Daten abschnittWert");
        int deskriptorEintrag = betriebskernWert.Systemaufruf().öffnen(betriebskernWert.ersterProzess(), "Prüfungen", Systemaufruf.ausschließlichMerkmalbitLesen);
        überprüfen(betriebskernWert.Systemaufruf().dateiSteuerung(betriebskernWert.ersterProzess(), deskriptorEintrag, 2, 1) == 0, "befehlAusführen 시 schließen einstellungen");
        überprüfen(betriebskernWert.Systemaufruf().befehlAusführen(betriebskernWert.ersterProzess(), Daten, new String[] {"Prüfungen", "값"}, new String[] {"Sprache=Deutsch"}) == 0, "ELF befehlAusführen abbildWert 적재");
        überprüfen(betriebskernWert.ersterProzess().ausführungStartenAdresse() == 0x04001000, "befehlAusführen ausführenVorgang adresse 반영");
        überprüfen(betriebskernWert.ersterProzess().ausführungArgument().length == 2 && betriebskernWert.ersterProzess().umgebungWert().length == 1, "befehlAusführen 인자와 umgebung");
        überprüfen(!betriebskernWert.ersterProzess().dateiDeskriptor().istÖffnen(deskriptorEintrag), "befehlAusführen 시 deskriptorEintrag schließen");
        überprüfen(betriebskernWert.seiteVerwaltung().byteWertLesen(betriebskernWert.ersterProzess().AdresseRaum(), 0x04002000) == 0, "빈 Daten abschnittWert nullwertOperand initialisieren");
    }

    private static void eingabePrüfung(Betriebskern betriebskernWert) {
        betriebskernWert.EingabeVerwaltung().tasteAbwärts('가');
        betriebskernWert.EingabeVerwaltung().mausBewegung(3, -2);
        eingabeEreignis ersterEreignis = betriebskernWert.EingabeVerwaltung().nächsterEreignis();
        eingabeEreignis zweiterEreignis = betriebskernWert.EingabeVerwaltung().nächsterEreignis();
        überprüfen(ersterEreignis.ereignisArt() == eingabeEreignis.artWert.tasteAbwärts, "자판 ereignis");
        überprüfen(zweiterEreignis.ersterWert() == 3 && zweiterEreignis.zweiterWert() == -2, "쥐 bewegenWert ereignis");
    }

    private static void hardwarePrüfung(WirtssystemHardware Gerät) {
        Gerät.portByteSchreiben(0x3f8, 0xab);
        überprüfen(Gerät.portByteLesen(0x3f8) == 0xab, "hardwarePort eingabeAusgabe grenzstelleWert");
        überprüfen(Gerät.seriellProtokolldatei().contains("JFinOS"), "seriellWert protokolldateiAufzeichnung");
    }

    private static void unterbrechungenUndDeskriptorenPrüfung() {
        UnterbrechenVerwalter verwalterWert = new UnterbrechenVerwalter();
        verwalterWert.eintragRegister(0x21, speichergerätAdresse -> speichergerätAdresse + 4);
        verwalterWert.aktivieren();
        überprüfen(verwalterWert.wertVerteilen(0x21, 100) == 104, "unterbrechen wertVerteilen");
        verwalterWert.deaktivieren();
        überprüfen(verwalterWert.wertVerteilen(0x21, 100) == 100, "unterbrechen deaktivieren");

        GlobalDeskriptorTabelle deskriptorTabelle = new GlobalDeskriptorTabelle();
        deskriptorTabelle.standardwertWertSetzen();
        überprüfen(deskriptorTabelle.fragmenteListe().size() == 5, "전역 deskriptorTabelle");
        AufgabeStatuswertSegment aufgabeStatuswert = new AufgabeStatuswertSegment();
        aufgabeStatuswert.bevorrechtigtStapelSetzen(0x10, 0x800000);
        überprüfen(aufgabeStatuswert.stapelNullwertBlock() == 0x10 && aufgabeStatuswert.stapelNullwertAdresse() == 0x800000, "Aufgabe statuswertWert abschnittWert");
    }

    private static void speichergerätUndNetzbetriebPrüfung() {
        FortgeschrittenTechnikAnhang speichergerätGerät = new FortgeschrittenTechnikAnhang(4, false);
        byte[] datenNachSchreiben = new byte[FortgeschrittenTechnikAnhang.abschnittGröße];
        byte[] datenWertLesen = new byte[FortgeschrittenTechnikAnhang.abschnittGröße];
        datenNachSchreiben[17] = 42;
        speichergerätGerät.schreiben(2, datenNachSchreiben);
        speichergerätGerät.lesen(2, datenWertLesen);
        überprüfen(datenWertLesen[17] == 42, "ATA abschnittWert 읽고 schreiben");

        PeripherieBusVerwalter peripherie = new PeripherieBusVerwalter();
        peripherie.entdecktWert(new PeripherieBusVerwalter.Gerät(0x1022, 0x2000, 0xc000, 11));
        überprüfen(peripherie.eintragFinden(0x1022, 0x2000) != null, "주변 Gerät eintragFinden");

        byte[] ethernetRahmen = new byte[34];
        ethernetRahmen[12] = 0x08;
        ethernetRahmen[13] = 0x00;
        ethernetRahmen[14] = 0x45;
        überprüfen(NetzwerkWerkzeuge.ethernetObererProtokoll(ethernetRahmen) == 0x0800, "이더넷 상위 vertragWert");
        überprüfen(NetzwerkWerkzeuge.istIPVersion4Protokoll(ethernetRahmen, 14), "상호통신망규약 4판");
        überprüfen(NetzwerkWerkzeuge.internetKontrollsumme(new byte[] {0, 0}, 0, 2) == 0xffff, "인터넷 kontrollsumme");

        byte[] ersterAbschnitt = new byte[512];
        ersterAbschnitt[510] = 0x55;
        ersterAbschnitt[511] = (byte) 0xaa;
        ersterAbschnitt[450] = 0x0b;
        ganzzahlWertSchreiben(ersterAbschnitt, 454, 63);
        ganzzahlWertSchreiben(ersterAbschnitt, 458, 1024);
        überprüfen(new hauptPartitionTabelle().lesen(ersterAbschnitt).size() == 1, "standardwertWert 분할 영역표");

        NetzwerkSchicht schichtWert = new NetzwerkSchicht();
        int[] empfangenWertAnzahl = new int[1];
        schichtWert.benutzerDatenEinheitRegister(7, (Daten, ausführenVorgang, Länge) -> empfangenWertAnzahl[0]++);
        byte[] rahmenIndex = new byte[14 + 20 + 8];
        rahmenIndex[12] = 0x08;
        rahmenIndex[13] = 0x00;
        rahmenIndex[14] = 0x45;
        rahmenIndex[16] = 0;
        rahmenIndex[17] = 28;
        rahmenIndex[23] = 17;
        rahmenIndex[36] = 0;
        rahmenIndex[37] = 7;
        überprüfen(schichtWert.ethernetEmpfangen(rahmenIndex) && empfangenWertAnzahl[0] == 1, "Benutzer Daten einheitWert wertVerteilen");
    }

    private static void bildschirmUndUhrPrüfung() {
        zeichenDarstellen Bildschirm = new zeichenDarstellen();
        Bildschirm.Ausgabe("가나\n다");
        überprüfen(Bildschirm.Zeichen(0, 0) == '가' && Bildschirm.Zeichen(0, 1) == '다', "Zeichen Bildschirm Ausgabe");
        Uhr Uhr = new Uhr(100);
        for (int Nummer = 0; Nummer < 10; Nummer++) {
            Uhr.taktWert();
        }
        überprüfen(Uhr.vergangenMillisekunden() == 100, "Uhr taktWert wertUmwandeln");
    }

    private static void ganzzahlWertSchreiben(byte[] Daten, int position, int Wert) {
        Daten[position] = (byte) Wert;
        Daten[position + 1] = (byte) (Wert >>> 8);
        Daten[position + 2] = (byte) (Wert >>> 16);
        Daten[position + 3] = (byte) (Wert >>> 24);
    }

    private static void kurzGanzzahlSchreiben(byte[] Daten, int position, int Wert) {
        Daten[position] = (byte) Wert;
        Daten[position + 1] = (byte) (Wert >>> 8);
    }

    private static void überprüfen(boolean bedingung, String Name) {
        if (!bedingung) {
            throw new AssertionError("fehlschlagWert: " + Name);
        }
        durchgangAnzahl++;
        System.out.println("durchgangWert: " + Name);
    }
}
