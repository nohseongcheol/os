// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** Trennt Dateideskriptoren eines einzelnen Benutzerprozesses von Beschreibungen geöffneter Dateien. Aufrufnummern stehen im POSIX-ABI-Dokument. */
public final class Dateideskriptorverwaltung {
    static final int deskriptorGrenzwert = 32;
    static final int schreibenMerkmalbitLesen = 2, eintragErstellen = 64, ausschließendErstellen = 128, inhaltLöschenInhalt = 512;
    static final int fortsetzungAnhängen = 1024, tunNichtBedingungWarten = 2048, eingeschaltetAusführungsvorgangSchließen = 524288;
    static int[] kennwertÖffnen = new int[deskriptorGrenzwert], deskriptorSetzen = new int[deskriptorGrenzwert];
    static int[] artWert = new int[deskriptorGrenzwert], zielobjektWert = new int[deskriptorGrenzwert];
    static int[] dateiPosition = new int[deskriptorGrenzwert], einstellungenÖffnen = new int[deskriptorGrenzwert], verweisAnzahl = new int[deskriptorGrenzwert];
    static int[] netzwerkKennwert = new int[deskriptorGrenzwert], zeitüberschreitungMillisekundenEmpfangen = new int[deskriptorGrenzwert];
    static int[] pfadName = new int[64], übertragungDaten = new int[1024];

    static int deskriptorFinden(int dateiDeskriptor) {
        if (dateiDeskriptor < 0 || dateiDeskriptor >= deskriptorGrenzwert) return -9;
        return kennwertÖffnen[dateiDeskriptor] - 1;
    }
    static int leerwertDeskriptor(int ausführenVorgang) {
        for (int Nummer = ausführenVorgang; Nummer < deskriptorGrenzwert; Nummer++) if (kennwertÖffnen[Nummer] == 0) return Nummer;
        return -24;
    }
    static int leerwertKennwert() {
        for (int Nummer = 0; Nummer < deskriptorGrenzwert; Nummer++) if (verweisAnzahl[Nummer] == 0) return Nummer;
        return -24;
    }
    static int verbinden(int deskriptorEintrag, int deskriptorWert, int dateiArt, int dateiZielobjektWert, int einstellungen) {
        kennwertÖffnen[deskriptorEintrag] = deskriptorWert + 1; deskriptorSetzen[deskriptorEintrag] = (einstellungen & eingeschaltetAusführungsvorgangSchließen) != 0 ? 1 : 0;
        artWert[deskriptorWert] = dateiArt; zielobjektWert[deskriptorWert] = dateiZielobjektWert; verweisAnzahl[deskriptorWert] = 1;
        einstellungenÖffnen[deskriptorWert] = einstellungen & (3 | fortsetzungAnhängen | tunNichtBedingungWarten); dateiPosition[deskriptorWert] = 0;
        netzwerkKennwert[deskriptorWert] = 0; zeitüberschreitungMillisekundenEmpfangen[deskriptorWert] = 0;
        return deskriptorEintrag;
    }
    static void prozessStarten() {
        bereinigenProzess();
        for (int Nummer = 0; Nummer < 3; Nummer++) verbinden(Nummer, Nummer, 1, Nummer, Nummer == 0 ? 0 : 1);
    }
    static void bereinigenProzess() {
        for (int Nummer = 0; Nummer < deskriptorGrenzwert; Nummer++) if (kennwertÖffnen[Nummer] != 0) dateiSchließen(Nummer);
    }
    static int dateiSchließen(int deskriptorEintrag) {
        int deskriptorWert = deskriptorFinden(deskriptorEintrag);
        if (deskriptorWert < 0) return -9;
        kennwertÖffnen[deskriptorEintrag] = 0; deskriptorSetzen[deskriptorEintrag] = 0;
        verweisAnzahl[deskriptorWert]--;
        if (verweisAnzahl[deskriptorWert] == 0) {
            if (artWert[deskriptorWert] == 2) ArbeitsspeicherDateisystem.anzahlÖffnen[zielobjektWert[deskriptorWert]]--;
            if (artWert[deskriptorWert] == 3 && netzwerkKennwert[deskriptorWert] != 0) Netzwerkstapel.schließen(netzwerkKennwert[deskriptorWert]);
            artWert[deskriptorWert] = 0;
        }
        return 0;
    }
    // C-Pfade sind NUL-terminierte Byteketten. Unterstützt wird nur ein Name direkt unter der Wurzel.
    static int pfadLesen(int adresse) {
        if (!Ausführungsverwaltung.beschneiden(adresse, 1)) return -14;
        int position = Gerät.speicherLesen(adresse) == '/' ? 1 : 0;
        for (int Länge = 0; Länge < 64; Länge++) {
            if (!Ausführungsverwaltung.beschneiden(adresse + position + Länge, 1)) return -14;
            int Wert = Gerät.speicherLesen(adresse + position + Länge);
            pfadName[Länge] = Wert;
            if (Wert == 0) return Länge == 0 ? -2 : (ArbeitsspeicherDateisystem.namePrüfen(pfadName, Länge) ? Länge : -22);
            if (Wert == '/') return -20;
        }
        return -36;
    }
    static int dateiÖffnen(int nameAdresse, int einstellungen, int erlaubnisGewähren) {
        int Länge = pfadLesen(nameAdresse);
        if (Länge < 0) return Länge;
        if ((einstellungen & ~(3 | eintragErstellen | ausschließendErstellen | inhaltLöschenInhalt | fortsetzungAnhängen | tunNichtBedingungWarten | eingeschaltetAusführungsvorgangSchließen)) != 0) return -95;
        if ((einstellungen & 3) == 3 || ((einstellungen & inhaltLöschenInhalt) != 0 && (einstellungen & 3) == 0)) return -22;
        int Datei = ArbeitsspeicherDateisystem.eintragFinden(pfadName, Länge);
        if (Datei >= 0 && (einstellungen & (eintragErstellen | ausschließendErstellen)) == (eintragErstellen | ausschließendErstellen)) return -17;
        if (Datei == -2 && (einstellungen & eintragErstellen) == 0) return -2;
        int deskriptorEintrag = leerwertDeskriptor(0), deskriptorWert = leerwertKennwert();
        if (deskriptorEintrag < 0 || deskriptorWert < 0) return -24;
        if (Datei == -2) {
            int ergebnis = ArbeitsspeicherDateisystem.ablegenDatenWert(pfadName, Länge, pfadName, 0);
            if (ergebnis < 0) return ergebnis;
            Datei = ArbeitsspeicherDateisystem.eintragFinden(pfadName, Länge);
            ArbeitsspeicherDateisystem.erlaubnisBerechtigungen[Datei] = erlaubnisGewähren & 511;
        }
        if (Datei < 0) return Datei;
        if ((einstellungen & inhaltLöschenInhalt) != 0) ArbeitsspeicherDateisystem.größeListe[Datei] = 0;
        ArbeitsspeicherDateisystem.anzahlÖffnen[Datei]++;
        return verbinden(deskriptorEintrag, deskriptorWert, 2, Datei, einstellungen);
    }
    static int dateiLesen(int deskriptorEintrag, int datenAdresse, int Länge) {
        int deskriptorWert = deskriptorFinden(deskriptorEintrag);
        if (deskriptorWert < 0 || (einstellungenÖffnen[deskriptorWert] & 3) == 1) return -9;
        if (Länge < 0) return -22;
        if (Länge == 0) return 0;
        if (!Ausführungsverwaltung.beschneiden(datenAdresse, Länge)) return -14;
        if (artWert[deskriptorWert] == 3) return datagrammDatenEmpfangen(deskriptorEintrag, datenAdresse, Länge, 0, 0);
        if (artWert[deskriptorWert] == 1) {
            int empfangenWertAnzahl = 0;
            while (empfangenWertAnzahl < Länge) {
                int Wert = Zeichenterminal.seriellLesen();
                if (Wert < 0) Wert = Tastatur.lesen();
                if (Wert < 0) {
                    if (empfangenWertAnzahl > 0) return empfangenWertAnzahl;
                    if ((einstellungenÖffnen[deskriptorWert] & tunNichtBedingungWarten) != 0) return -11;
                    if (Gerät.benutzerVerbleibendMillisekunden() <= 10) return -11;
                    Netzwerkstapel.überprüfen(); Gerät.kurzzeitigTunAbgeben();
                } else {
                    Gerät.speicherSchreiben(datenAdresse + empfangenWertAnzahl, Wert); empfangenWertAnzahl++;
                }
            }
            return empfangenWertAnzahl;
        }
        int Datei = zielobjektWert[deskriptorWert], position = dateiPosition[deskriptorWert];
        if (position >= ArbeitsspeicherDateisystem.größeListe[Datei]) return 0;
        if (Länge > ArbeitsspeicherDateisystem.größeListe[Datei] - position) Länge = ArbeitsspeicherDateisystem.größeListe[Datei] - position;
        int ursprünglichAdresse = Gerät.dateiSpeicher() + Datei * ArbeitsspeicherDateisystem.höchstwertGröße + position;
        for (int Nummer = 0; Nummer < Länge; Nummer++) Gerät.speicherSchreiben(datenAdresse + Nummer, Gerät.speicherLesen(ursprünglichAdresse + Nummer));
        dateiPosition[deskriptorWert] += Länge;
        return Länge;
    }
    static int dateiSchreiben(int deskriptorEintrag, int datenAdresse, int Länge) {
        int deskriptorWert = deskriptorFinden(deskriptorEintrag);
        if (deskriptorWert < 0 || (einstellungenÖffnen[deskriptorWert] & 3) == 0) return -9;
        if (Länge < 0) return -22;
        if (Länge == 0) return 0;
        if (!Ausführungsverwaltung.beschneiden(datenAdresse, Länge)) return -14;
        if (artWert[deskriptorWert] == 3) return -89; // Ein unverbundener Datagrammendpunkt braucht eine Zieladresse.
        if (artWert[deskriptorWert] == 1) {
            if (Länge > 16384) Länge = 16384;
            for (int Nummer = 0; Nummer < Länge; Nummer++) {
                int Wert = Gerät.speicherLesen(datenAdresse + Nummer);
                Zeichenterminal.seriellByte(Wert); Zeichenterminal.bildschirmZeichen(Wert);
            }
            return Länge;
        }
        int Datei = zielobjektWert[deskriptorWert], größe = ArbeitsspeicherDateisystem.größeListe[Datei];
        int position = (einstellungenÖffnen[deskriptorWert] & fortsetzungAnhängen) != 0 ? größe : dateiPosition[deskriptorWert];
        if (position >= ArbeitsspeicherDateisystem.höchstwertGröße) return -27;
        if (Länge > ArbeitsspeicherDateisystem.höchstwertGröße - position) Länge = ArbeitsspeicherDateisystem.höchstwertGröße - position;
        int zielAdresse = Gerät.dateiSpeicher() + Datei * ArbeitsspeicherDateisystem.höchstwertGröße;
        for (int Nummer = größe; Nummer < position; Nummer++) Gerät.speicherSchreiben(zielAdresse + Nummer, 0);
        for (int Nummer = 0; Nummer < Länge; Nummer++) Gerät.speicherSchreiben(zielAdresse + position + Nummer, Gerät.speicherLesen(datenAdresse + Nummer));
        dateiPosition[deskriptorWert] = position + Länge;
        if (position + Länge > größe) ArbeitsspeicherDateisystem.größeListe[Datei] = position + Länge;
        return Länge;
    }
    static int dateiPositionieren(int deskriptorEintrag, int versatzwertWert, int projektWurzel) {
        int deskriptorWert = deskriptorFinden(deskriptorEintrag);
        if (deskriptorWert < 0) return -9;
        if (artWert[deskriptorWert] != 2) return -29;
        if (projektWurzel < 0 || projektWurzel > 2) return -22;
        int hintergrundWert = projektWurzel == 0 ? 0 : (projektWurzel == 1 ? dateiPosition[deskriptorWert] : ArbeitsspeicherDateisystem.größeListe[zielobjektWert[deskriptorWert]]);
        if (versatzwertWert > 0 && hintergrundWert > 2147483647 - versatzwertWert) return -75;
        if (versatzwertWert < 0 && versatzwertWert < -hintergrundWert) return -22;
        dateiPosition[deskriptorWert] = hintergrundWert + versatzwertWert;
        return dateiPosition[deskriptorWert];
    }
    static int duplikatDeskriptor(int deskriptorEintrag, int neuDeskriptor, boolean zuweisenWert, int einstellungen) {
        int deskriptorWert = deskriptorFinden(deskriptorEintrag);
        if (deskriptorWert < 0) return -9;
        if (neuDeskriptor < 0 || neuDeskriptor >= deskriptorGrenzwert) return zuweisenWert ? -9 : -22;
        if (zuweisenWert && deskriptorEintrag == neuDeskriptor) return neuDeskriptor;
        if (zuweisenWert) { if (kennwertÖffnen[neuDeskriptor] != 0) dateiSchließen(neuDeskriptor); }
        else { neuDeskriptor = leerwertDeskriptor(neuDeskriptor); if (neuDeskriptor < 0) return neuDeskriptor; }
        kennwertÖffnen[neuDeskriptor] = deskriptorWert + 1; deskriptorSetzen[neuDeskriptor] = einstellungen; verweisAnzahl[deskriptorWert]++;
        return neuDeskriptor;
    }
    static int dateiEintragNameEntfernen(int nameAdresse) {
        int Länge = pfadLesen(nameAdresse);
        if (Länge < 0) return Länge;
        int Datei = ArbeitsspeicherDateisystem.eintragFinden(pfadName, Länge);
        if (Datei < 0) return Datei;
        ArbeitsspeicherDateisystem.namenListe[Datei * 64] = 0;
        return 0;
    }
    static int dateiLängeSetzen(int deskriptorEintrag, int Länge) {
        int deskriptorWert = deskriptorFinden(deskriptorEintrag);
        if (deskriptorWert < 0) return -9;
        if (artWert[deskriptorWert] != 2 || (einstellungenÖffnen[deskriptorWert] & 3) == 0 || Länge < 0) return -22;
        if (Länge > ArbeitsspeicherDateisystem.höchstwertGröße) return -27;
        int Datei = zielobjektWert[deskriptorWert], adresse = Gerät.dateiSpeicher() + Datei * ArbeitsspeicherDateisystem.höchstwertGröße;
        for (int Nummer = ArbeitsspeicherDateisystem.größeListe[Datei]; Nummer < Länge; Nummer++) Gerät.speicherSchreiben(adresse + Nummer, 0);
        ArbeitsspeicherDateisystem.größeListe[Datei] = Länge;
        return 0;
    }
    static int dateiZustandLesen(int deskriptorEintrag, int adresse) {
        int deskriptorWert = deskriptorFinden(deskriptorEintrag);
        if (deskriptorWert < 0) return -9;
        if (!Ausführungsverwaltung.beschneiden(adresse, 48)) return -14;
        for (int Nummer = 0; Nummer < 12; Nummer++) Ausführungsverwaltung.nummerSchreiben(adresse + Nummer * 4, 0);
        int Datei = zielobjektWert[deskriptorWert], größe = artWert[deskriptorWert] == 2 ? ArbeitsspeicherDateisystem.größeListe[Datei] : 0;
        int erlaubnisGewähren = artWert[deskriptorWert] == 2 ? ArbeitsspeicherDateisystem.erlaubnisBerechtigungen[Datei] : 438;
        Ausführungsverwaltung.nummerSchreiben(adresse, 1);
        Ausführungsverwaltung.nummerSchreiben(adresse + 4, artWert[deskriptorWert] == 2 ? Datei + 1 : 100 + deskriptorWert);
        Ausführungsverwaltung.nummerSchreiben(adresse + 8, (artWert[deskriptorWert] == 2 ? 32768 : (artWert[deskriptorWert] == 1 ? 8192 : 49152)) | erlaubnisGewähren);
        Ausführungsverwaltung.nummerSchreiben(adresse + 12, artWert[deskriptorWert] == 2 && ArbeitsspeicherDateisystem.namenListe[Datei * 64] == 0 ? 0 : 1);
        Ausführungsverwaltung.nummerSchreiben(adresse + 28, größe); Ausführungsverwaltung.nummerSchreiben(adresse + 32, 512);
        Ausführungsverwaltung.nummerSchreiben(adresse + 36, (größe + 511) / 512);
        return 0;
    }
    static int steuerungDeskriptor(int deskriptorEintrag, int befehl, int Wert) {
        int deskriptorWert = deskriptorFinden(deskriptorEintrag);
        if (deskriptorWert < 0) return -9;
        if (befehl == 0 || befehl == 1030) return duplikatDeskriptor(deskriptorEintrag, Wert, false, befehl == 1030 ? 1 : 0);
        if (befehl == 1) return deskriptorSetzen[deskriptorEintrag];
        if (befehl == 2) { if ((Wert & ~1) != 0) return -22; deskriptorSetzen[deskriptorEintrag] = Wert; return 0; }
        if (befehl == 3) return einstellungenÖffnen[deskriptorWert];
        if (befehl == 4) {
            if ((Wert & ~(3 | fortsetzungAnhängen | tunNichtBedingungWarten)) != 0) return -95;
            einstellungenÖffnen[deskriptorWert] = (einstellungenÖffnen[deskriptorWert] & 3) | (Wert & (fortsetzungAnhängen | tunNichtBedingungWarten)); return 0;
        }
        return -95;
    }
    static int endpunktErstellen(int adresseSchema, int netzwerkArt, int vertragNummer) {
        if (adresseSchema != 2) return -97;
        if (netzwerkArt != 2) return -93;
        if (vertragNummer != 0 && vertragNummer != 17) return -93;
        int deskriptorEintrag = leerwertDeskriptor(0), deskriptorWert = leerwertKennwert();
        if (deskriptorEintrag < 0 || deskriptorWert < 0) return -24;
        return verbinden(deskriptorEintrag, deskriptorWert, 3, 0, schreibenMerkmalbitLesen);
    }
    static int endpunktDeskriptor(int deskriptorEintrag) {
        int deskriptorWert = deskriptorFinden(deskriptorEintrag);
        if (deskriptorWert < 0) return -9;
        return artWert[deskriptorWert] == 3 ? deskriptorWert : -88;
    }
    static int adresse32(int adresse) {
        return Gerät.speicherLesen(adresse) << 24 | Gerät.speicherLesen(adresse + 1) << 16
            | Gerät.speicherLesen(adresse + 2) << 8 | Gerät.speicherLesen(adresse + 3);
    }
    static int adressePrüfen(int adresse, int Länge) {
        if (Länge < 16) return -22;
        if (!Ausführungsverwaltung.beschneiden(adresse, 16)) return -14;
        return Ausführungsverwaltung.kurzWert(adresse) == 2 ? 0 : -97;
    }
    static int adresseZuordnen(int deskriptorEintrag, int adresse, int Länge) {
        int deskriptorWert = endpunktDeskriptor(deskriptorEintrag);
        if (deskriptorWert < 0) return deskriptorWert;
        int ergebnis = adressePrüfen(adresse, Länge);
        if (ergebnis < 0) return ergebnis;
        if (netzwerkKennwert[deskriptorWert] != 0) return -22;
        int netzwerkAdresse = adresse32(adresse + 4);
        if (netzwerkAdresse != 0 && netzwerkAdresse != Netzwerkstapel.eigenAdresse) return -99;
        int portNummer = Gerät.speicherLesen(adresse + 2) << 8 | Gerät.speicherLesen(adresse + 3);
        ergebnis = Netzwerkstapel.öffnen(portNummer);
        if (ergebnis < 0) return ergebnis;
        netzwerkKennwert[deskriptorWert] = ergebnis; zielobjektWert[deskriptorWert] = netzwerkAdresse;
        return 0;
    }
    static int automatikZuordnen(int deskriptorWert) {
        if (netzwerkKennwert[deskriptorWert] != 0) return 0;
        int ergebnis = Netzwerkstapel.öffnen(0);
        if (ergebnis < 0) return ergebnis;
        netzwerkKennwert[deskriptorWert] = ergebnis;
        return 0;
    }
    // Die letzten beiden sendto/recvfrom-Argumente werden in einer 8-Byte-Anforderungsstruktur übergeben.
    static int datagrammDatenSenden(int deskriptorEintrag, int datenAdresse, int Länge, int einstellungen, int angefordertAdresse) {
        int deskriptorWert = endpunktDeskriptor(deskriptorEintrag);
        if (deskriptorWert < 0) return deskriptorWert;
        if (einstellungen != 0) return -95;
        if (Länge < 0 || Länge > 1024) return -90;
        if (Länge != 0 && !Ausführungsverwaltung.beschneiden(datenAdresse, Länge)) return -14;
        if (!Ausführungsverwaltung.beschneiden(angefordertAdresse, 8)) return -14;
        int adresse = Ausführungsverwaltung.Zahl(angefordertAdresse);
        int ergebnis = adressePrüfen(adresse, Ausführungsverwaltung.Zahl(angefordertAdresse + 4));
        if (ergebnis < 0) return ergebnis;
        int portNummer = Gerät.speicherLesen(adresse + 2) << 8 | Gerät.speicherLesen(adresse + 3);
        if (portNummer == 0) return -22;
        ergebnis = automatikZuordnen(deskriptorWert);
        if (ergebnis < 0) return ergebnis;
        for (int Nummer = 0; Nummer < Länge; Nummer++) übertragungDaten[Nummer] = Gerät.speicherLesen(datenAdresse + Nummer);
        return Netzwerkstapel.senden(netzwerkKennwert[deskriptorWert], adresse32(adresse + 4), portNummer, übertragungDaten, Länge);
    }
    static void adresseSchreiben(int adresse, int Länge, int netzwerkAdresse, int portNummer) {
        for (int Nummer = 0; Nummer < Länge && Nummer < 16; Nummer++) {
            int Wert = 0;
            if (Nummer == 0) Wert = 2;
            if (Nummer == 2) Wert = portNummer >>> 8;
            if (Nummer == 3) Wert = portNummer;
            if (Nummer >= 4 && Nummer < 8) Wert = netzwerkAdresse >>> (56 - Nummer * 8);
            Gerät.speicherSchreiben(adresse + Nummer, Wert & 255);
        }
    }
    static int datagrammDatenEmpfangen(int deskriptorEintrag, int datenAdresse, int Länge, int einstellungen, int angefordertAdresse) {
        int deskriptorWert = endpunktDeskriptor(deskriptorEintrag);
        if (deskriptorWert < 0) return deskriptorWert;
        if ((einstellungen & ~64) != 0) return -95;
        if (Länge < 0) return -22;
        if (Länge != 0 && !Ausführungsverwaltung.beschneiden(datenAdresse, Länge)) return -14;
        int adresse = 0, adresseLängeAdresse = 0, adresseLänge = 0;
        if (angefordertAdresse != 0) {
            if (!Ausführungsverwaltung.beschneiden(angefordertAdresse, 8)) return -14;
            adresse = Ausführungsverwaltung.Zahl(angefordertAdresse); adresseLängeAdresse = Ausführungsverwaltung.Zahl(angefordertAdresse + 4);
            if (adresse != 0) {
                if (!Ausführungsverwaltung.beschneiden(adresseLängeAdresse, 4)) return -14;
                adresseLänge = Ausführungsverwaltung.Zahl(adresseLängeAdresse);
                if (adresseLänge < 0) return -22;
                if (!Ausführungsverwaltung.beschneiden(adresse, adresseLänge < 16 ? adresseLänge : 16)) return -14;
            }
        }
        int ergebnis = automatikZuordnen(deskriptorWert);
        if (ergebnis < 0) return ergebnis;
        int ausführenVorgang = Gerät.millisekunden();
        while (true) {
            ergebnis = Netzwerkstapel.empfangen(netzwerkKennwert[deskriptorWert], übertragungDaten, 1024, 0);
            if (ergebnis != -11) break;
            if ((einstellungen & 64) != 0 || (einstellungenÖffnen[deskriptorWert] & tunNichtBedingungWarten) != 0) return -11;
            if (zeitüberschreitungMillisekundenEmpfangen[deskriptorWert] > 0 && Gerät.millisekunden() - ausführenVorgang >= zeitüberschreitungMillisekundenEmpfangen[deskriptorWert]) return -11;
            if (Gerät.benutzerVerbleibendMillisekunden() <= 10) return -11;
            Gerät.kurzzeitigTunAbgeben();
        }
        if (ergebnis < 0) return ergebnis;
        if (ergebnis > Länge) ergebnis = Länge;
        for (int Nummer = 0; Nummer < ergebnis; Nummer++) Gerät.speicherSchreiben(datenAdresse + Nummer, übertragungDaten[Nummer]);
        if (adresse != 0) {
            adresseSchreiben(adresse, adresseLänge, Netzwerkstapel.gegenstelleAdresse(netzwerkKennwert[deskriptorWert]), Netzwerkstapel.gegenstellePortNummer(netzwerkKennwert[deskriptorWert]));
            Ausführungsverwaltung.nummerSchreiben(adresseLängeAdresse, 16);
        }
        return ergebnis;
    }
    static int netzbuchseAdresseLesen(int deskriptorEintrag, int adresse, int längeAdresse) {
        int deskriptorWert = endpunktDeskriptor(deskriptorEintrag);
        if (deskriptorWert < 0) return deskriptorWert;
        if (!Ausführungsverwaltung.beschneiden(längeAdresse, 4)) return -14;
        int Länge = Ausführungsverwaltung.Zahl(längeAdresse);
        if (Länge < 0) return -22;
        if (!Ausführungsverwaltung.beschneiden(adresse, Länge < 16 ? Länge : 16)) return -14;
        int platzEintrag = Netzwerkstapel.Nummer(netzwerkKennwert[deskriptorWert]);
        adresseSchreiben(adresse, Länge, zielobjektWert[deskriptorWert], platzEintrag < 0 ? 0 : Netzwerkstapel.ports[platzEintrag]);
        Ausführungsverwaltung.nummerSchreiben(längeAdresse, 16);
        return 0;
    }
    static int empfangenZeitüberschreitungSetzen(int deskriptorEintrag, int millisekunden) {
        int deskriptorWert = endpunktDeskriptor(deskriptorEintrag);
        if (deskriptorWert < 0) return deskriptorWert;
        if (millisekunden < 0 || millisekunden > 2000) return -22;
        zeitüberschreitungMillisekundenEmpfangen[deskriptorWert] = millisekunden;
        return 0;
    }
}
