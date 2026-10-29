// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Namibia.JNamOS.Systemaufruf;

import Namibia.JNamOS.Speicherraum.SeiteVerwalter;
import Namibia.JNamOS.Aufgabe.prozessWert;
import Namibia.JNamOS.Aufgabe.Ablaufplaner;
import Namibia.JNamOS.DateiSystem.AusführdateiLader;
import Namibia.JNamOS.DateiSystem.DateiSystem;
import Namibia.JNamOS.DateiSystem.dateiInformation;
import Namibia.JNamOS.Betriebskern.hardwareWert;
import Namibia.JNamOS.Eingabewert.EingabeVerwalter;
import Namibia.JNamOS.Eingabewert.eingabeEreignis;

/** Java-Verwaltungsschicht für die erste Stufe der engos-POSIX-Aufrufe. */
public final class Systemaufruf {
    public static final int ausschließlichMerkmalbitLesen = 0;
    public static final int startenSuchen = 0;
    public static final int aktuellSuchen = 1;
    public static final int eintragEndeFinden = 2;

    private final DateiSystem DateiSystem;
    private final SeiteVerwalter seiteVerwaltung;
    private final Ablaufplaner Ablaufplaner;
    private final AusführdateiLader lader = new AusführdateiLader();
    private final hardwareWert Gerät;
    private final EingabeVerwalter EingabeVerwaltung;

    public Systemaufruf(DateiSystem DateiSystem, SeiteVerwalter seiteVerwaltung, Ablaufplaner Ablaufplaner, hardwareWert Gerät, EingabeVerwalter EingabeVerwaltung) {
        this.DateiSystem = DateiSystem;
        this.seiteVerwaltung = seiteVerwaltung;
        this.Ablaufplaner = Ablaufplaner;
        this.Gerät = Gerät;
        this.EingabeVerwaltung = EingabeVerwaltung;
    }

    public int prozessBezeichner(prozessWert aktuellProzess) {
        return aktuellProzess.bezeichnerWert();
    }

    public int elternknotenProzessBezeichner(prozessWert aktuellProzess) {
        return aktuellProzess.elternknotenBezeichner();
    }

    public int öffnen(prozessWert aktuellProzess, String Name, int merkmalbitWert) {
        if (merkmalbitWert != ausschließlichMerkmalbitLesen) {
            return -30;
        }
        return aktuellProzess.dateiDeskriptor().öffnen(Name);
    }

    public int lesen(prozessWert aktuellProzess, int deskriptorEintrag, byte[] zielEmpfangen, int größe) {
        if (deskriptorEintrag == 0) {
            if (größe <= 0 || zielEmpfangen.length == 0) {
                return 0;
            }
            eingabeEreignis ereignis = EingabeVerwaltung.nächsterEreignis();
            if (ereignis == null || ereignis.ereignisArt() != eingabeEreignis.artWert.tasteAbwärts) {
                return -11;
            }
            zielEmpfangen[0] = (byte) ereignis.ersterWert();
            return 1;
        }
        return aktuellProzess.dateiDeskriptor().lesen(deskriptorEintrag, zielEmpfangen, größe);
    }

    public int schreiben(prozessWert aktuellProzess, int deskriptorEintrag, byte[] Daten, int größe) {
        if (deskriptorEintrag != 1 && deskriptorEintrag != 2) {
            return aktuellProzess.dateiDeskriptor().istÖffnen(deskriptorEintrag) ? -30 : -9;
        }
        if (größe < 0 || größe > Daten.length) {
            return -22;
        }
        Gerät.seriellAusgabe(new String(Daten, 0, größe, java.nio.charset.StandardCharsets.UTF_8));
        return größe;
    }

    public int schließen(prozessWert aktuellProzess, int deskriptorEintrag) {
        return aktuellProzess.dateiDeskriptor().schließen(deskriptorEintrag);
    }

    public int bewegenPosition(prozessWert aktuellProzess, int deskriptorEintrag, int entfernungWert, int projektWurzel) {
        return aktuellProzess.dateiDeskriptor().bewegenPosition(deskriptorEintrag, entfernungWert, projektWurzel);
    }

    public int duplikatDeskriptor(prozessWert aktuellProzess, int deskriptorEintrag) {
        return aktuellProzess.dateiDeskriptor().geklontDeskriptor(deskriptorEintrag, 0);
    }

    public int duplikatDeskriptorAnStelle(prozessWert aktuellProzess, int deskriptorEintrag, int neuDeskriptor) {
        return aktuellProzess.dateiDeskriptor().duplikatAnStelle(deskriptorEintrag, neuDeskriptor);
    }

    public int istZugänglich(String Name, int methodeBetriebsart) {
        dateiInformation systemInformation = DateiSystem.systemInformation(Name);
        if (systemInformation == null) {
            return -2;
        }
        if ((methodeBetriebsart & 1) != 0 && (systemInformation.formArt() & 0111) == 0) {
            return -13;
        }
        if ((methodeBetriebsart & 2) != 0) {
            return -30;
        }
        return 0;
    }

    public int umschaltenAufgabeListe(String Name) {
        return "/".equals(Name) ? 0 : -20;
    }

    public String aktuellAufgabeListe(int größeEmpfangen) {
        return größeEmpfangen >= 2 ? "/" : null;
    }

    public int benutzerBezeichner() { return 0; }
    public int wirksamBenutzerBezeichner() { return 0; }
    public int gruppeBezeichner() { return 0; }
    public int wirksamGruppeBezeichner() { return 0; }

    public int dateiSynchronisieren(prozessWert aktuellProzess, int deskriptorEintrag) {
        return aktuellProzess.dateiDeskriptor().systemInformation(deskriptorEintrag) == null ? -9 : 0;
    }

    public void alleSynchronisieren() {
        // Das aktuelle Dateisystem ist schreibgeschützt, daher gibt es keine ausstehenden Schreibdaten.
    }

    public boolean istTerminal(prozessWert aktuellProzess, int deskriptorEintrag) {
        dateiInformation systemInformation = aktuellProzess.dateiDeskriptor().systemInformation(deskriptorEintrag);
        return systemInformation != null && (systemInformation.formArt() & 0170000) == 0020000;
    }

    public int dateiSteuerung(prozessWert aktuellProzess, int deskriptorEintrag, int befehl, int parameterArgument) {
        if (befehl == 0) {
            return aktuellProzess.dateiDeskriptor().geklontDeskriptor(deskriptorEintrag, parameterArgument);
        }
        if (befehl == 1) {
            return aktuellProzess.dateiDeskriptor().eingeschaltetAusführungsvorgangWertSchließen(deskriptorEintrag);
        }
        if (befehl == 2) {
            return aktuellProzess.dateiDeskriptor().schließenEingeschaltetAusführungsvorgangSetzen(deskriptorEintrag, (parameterArgument & 1) != 0);
        }
        if (befehl == 3) {
            return aktuellProzess.dateiDeskriptor().systemInformation(deskriptorEintrag) == null ? -9 : ausschließlichMerkmalbitLesen;
        }
        if (befehl == 4) {
            return parameterArgument == ausschließlichMerkmalbitLesen ? 0 : -30;
        }
        return -22;
    }

    public int eintragErstellen(String Name, int erlaubnisWert) {
        return -30;
    }

    public dateiInformation deskriptorInformation(prozessWert aktuellProzess, int deskriptorEintrag) {
        return aktuellProzess.dateiDeskriptor().systemInformation(deskriptorEintrag);
    }

    public systemEinzelheiten systemEinzelheiten() {
        return new systemEinzelheiten("JNamOS", "JNamOS", "0.1", "Java managed kernel", "i386");
    }

    public dateiInformation dateiInformation(String Name) {
        return DateiSystem.systemInformation(Name);
    }

    public prozessWert klonenProzess(prozessWert elternknotenWert) {
        return Ablaufplaner.klonenWert(elternknotenWert);
    }

    public int fürKindWarten(prozessWert elternknotenWert, int kindBezeichner, boolean nichtBlockierend) {
        return Ablaufplaner.fürKindWarten(elternknotenWert, kindBezeichner, nichtBlockierend);
    }

    public int programmAbbrechen(prozessWert aktuellProzess, int neuEnde) {
        int vorherigEnde = aktuellProzess.programmAbbrechen();
        if (neuEnde == 0) {
            return vorherigEnde;
        }
        if (neuEnde < 0x06000000 || neuEnde > 0x07000000) {
            return -12;
        }
        int ersterSeite = vorherigEnde / SeiteVerwalter.seiteGröße;
        int letzterSeite = (neuEnde + SeiteVerwalter.seiteGröße - 1) / SeiteVerwalter.seiteGröße;
        if (neuEnde > vorherigEnde) {
            for (int Nummer = ersterSeite; Nummer < letzterSeite; Nummer++) {
                int adresse = Nummer * SeiteVerwalter.seiteGröße;
                try {
                    seiteVerwaltung.byteWertLesen(aktuellProzess.AdresseRaum(), adresse);
                } catch (IllegalStateException fehler) {
                    seiteVerwaltung.abbildungSeite(aktuellProzess.AdresseRaum(), adresse, true);
                }
            }
        }
        aktuellProzess.programmAbbrechenSetzen(neuEnde);
        return neuEnde;
    }

    public int programmAbbrechenVergrößern(prozessWert aktuellProzess, int erhöhenSchrittGesamtmenge) {
        int vorherigEnde = aktuellProzess.programmAbbrechen();
        int ergebnis = programmAbbrechen(aktuellProzess, vorherigEnde + erhöhenSchrittGesamtmenge);
        return ergebnis < 0 ? ergebnis : vorherigEnde;
    }

    public int befehlAusführen(prozessWert aktuellProzess, byte[] ausführdateiDatei) {
        return befehlAusführen(aktuellProzess, ausführdateiDatei, new String[0], new String[0]);
    }

    public int befehlAusführen(prozessWert aktuellProzess, byte[] ausführdateiDatei, String[] parameterArgument, String[] umgebung) {
        AusführdateiLader.abbild abbildWert;
        try {
            abbildWert = lader.Prüfpunkte(ausführdateiDatei);
        } catch (IllegalArgumentException fehler) {
            return -8;
        }
        if (parameterArgument == null || umgebung == null || parameterArgument.length > 16 || umgebung.length > 16) {
            return -7;
        }
        for (AusführdateiLader.abschnittWert abschnittWert : abbildWert.abschnitteListe()) {
            if ((abschnittWert.merkmalbitWert() & 2) == 0 || abschnittWert.größe() == 0) {
                continue;
            }
            int ersterSeite = abschnittWert.adresse() / SeiteVerwalter.seiteGröße;
            int letzterSeite = (abschnittWert.adresse() + abschnittWert.größe() + SeiteVerwalter.seiteGröße - 1) / SeiteVerwalter.seiteGröße;
            for (int Nummer = ersterSeite; Nummer < letzterSeite; Nummer++) {
                int adresse = Nummer * SeiteVerwalter.seiteGröße;
                try {
                    seiteVerwaltung.byteWertLesen(aktuellProzess.AdresseRaum(), adresse);
                    seiteVerwaltung.privatBereichSchreiben(aktuellProzess.AdresseRaum(), adresse, SeiteVerwalter.seiteGröße);
                } catch (IllegalStateException fehler) {
                    seiteVerwaltung.abbildungSeite(aktuellProzess.AdresseRaum(), adresse, true);
                }
            }
            for (int Nummer = 0; Nummer < abschnittWert.größe(); Nummer++) {
                byte Wert = abschnittWert.artWert() == 8 ? 0 : ausführdateiDatei[abschnittWert.dateiPosition() + Nummer];
                seiteVerwaltung.byteWertSchreiben(aktuellProzess.AdresseRaum(), abschnittWert.adresse() + Nummer, Wert);
            }
        }
        aktuellProzess.ausführungKontextSetzen(abbildWert.adresseStarten(), parameterArgument, umgebung);
        aktuellProzess.dateiDeskriptor().eingeschaltetAusführungsvorgangSchließen();
        return 0;
    }

    public void aufhörenProgramm(prozessWert aktuellProzess, int statuswertWert) {
        aktuellProzess.verlassenProzessProgramm(statuswertWert);
    }
}
