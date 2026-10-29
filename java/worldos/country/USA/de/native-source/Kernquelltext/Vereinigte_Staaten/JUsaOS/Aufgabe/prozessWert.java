// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Vereinigte_Staaten.JUsaOS.Aufgabe;

import Vereinigte_Staaten.JUsaOS.Speicherraum.SeiteVerwalter;
import Vereinigte_Staaten.JUsaOS.DateiSystem.dateiDeskriptorTabelle;

public final class prozessWert {
    private final int bezeichnerWert;
    private final int elternknotenBezeichner;
    private final SeiteVerwalter.AdresseRaum AdresseRaum;
    private final dateiDeskriptorTabelle dateiDeskriptor;
    private prozessStatuswert statuswertWert = prozessStatuswert.vorbereiten;
    private int verlassenProzessKode;
    private int programmAbbrechen = 0x06000000;
    private int ausführungStartenAdresse;
    private String[] ausführungArgument = new String[0];
    private String[] umgebungWert = new String[0];

    prozessWert(int bezeichnerWert, int elternknotenBezeichner, SeiteVerwalter.AdresseRaum AdresseRaum, dateiDeskriptorTabelle dateiDeskriptor) {
        this.bezeichnerWert = bezeichnerWert;
        this.elternknotenBezeichner = elternknotenBezeichner;
        this.AdresseRaum = AdresseRaum;
        this.dateiDeskriptor = dateiDeskriptor;
    }

    public int bezeichnerWert() {
        return bezeichnerWert;
    }

    public int elternknotenBezeichner() {
        return elternknotenBezeichner;
    }

    public SeiteVerwalter.AdresseRaum AdresseRaum() {
        return AdresseRaum;
    }

    public dateiDeskriptorTabelle dateiDeskriptor() {
        return dateiDeskriptor;
    }

    public prozessStatuswert statuswertWert() {
        return statuswertWert;
    }

    public void statuswertSetzen(prozessStatuswert neuStatuswert) {
        statuswertWert = neuStatuswert;
    }

    public int verlassenProzessKode() {
        return verlassenProzessKode;
    }

    public void verlassenProzessProgramm(int Wert) {
        verlassenProzessKode = Wert & 0xff;
        statuswertWert = prozessStatuswert.verlassenProzessProgramm;
    }

    public int programmAbbrechen() {
        return programmAbbrechen;
    }

    public void programmAbbrechenSetzen(int neuEnde) {
        if (neuEnde < 0x06000000 || neuEnde > 0x07000000) {
            throw new IllegalArgumentException("Programm endung 범위를 벗어났습니다.");
        }
        programmAbbrechen = neuEnde;
    }

    public void ausführungKontextSetzen(int adresseStarten, String[] parameterArgument, String[] umgebung) {
        ausführungStartenAdresse = adresseStarten;
        ausführungArgument = parameterArgument.clone();
        umgebungWert = umgebung.clone();
    }

    public int ausführungStartenAdresse() { return ausführungStartenAdresse; }
    public String[] ausführungArgument() { return ausführungArgument.clone(); }
    public String[] umgebungWert() { return umgebungWert.clone(); }
}
