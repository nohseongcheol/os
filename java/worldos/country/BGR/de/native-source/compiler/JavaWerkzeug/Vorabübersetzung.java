// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.security.MessageDigest;
import java.util.*;
import java.util.regex.*;

/** Erzeugt aus Java-Klassendateien C-Quellcode für einen eigenständigen ARM64-Kernel. Läuft auf dem Host-JDK. */
public final class Vorabübersetzung {
    static final class ÜbersetzungFehler extends RuntimeException {
        ÜbersetzungFehler(String beschreibung) { super(beschreibung); }
    }
    static final class DatenLeser {
        final byte[] Daten;
        int position;
        DatenLeser(byte[] eingabeDaten) { Daten = eingabeDaten; }
        byte[] lesen(int Länge) {
            if (Länge < 0 || Länge > Daten.length - position) throw new ÜbersetzungFehler("beschnittenWert klasseWert 또는 befehl Daten");
            byte[] ergebnis = Arrays.copyOfRange(Daten, position, position + Länge); position += Länge; return ergebnis;
        }
        int byteLesen() { if (position >= Daten.length) throw new ÜbersetzungFehler("beschnittenWert befehl Daten"); return Daten[position++] & 255; }
        int kurzLesen() { return (byteLesen() << 8) | byteLesen(); }
        int ganzzahltypLesen() { return (kurzLesen() << 16) | kurzLesen(); }
        int vorzeichenbehaftetByteLesen() { return (byte) byteLesen(); }
        int vorzeichenbehaftetKurzLesen() { return (short) kurzLesen(); }
    }
    static final class MitgliedDaten {
        final int zugriffEintrag;
        final String Name, beschreibungWert;
        final Map<String, byte[]> attributWert;
        MitgliedDaten(int zugriffWert, String nameWert, String deskriptorDaten, Map<String, byte[]> attributDaten) {
            zugriffEintrag = zugriffWert; Name = nameWert; beschreibungWert = deskriptorDaten; attributWert = attributDaten;
        }
    }
    static final class MethodeVerweis implements Comparable<MethodeVerweis> {
        final String eigentümerWert, Name, beschreibungWert;
        MethodeVerweis(String eigenständigWert, String nameWert, String deskriptorDaten) { eigentümerWert = eigenständigWert; Name = nameWert; beschreibungWert = deskriptorDaten; }
        String[] teile() { return new String[]{eigentümerWert, Name, beschreibungWert}; }
        public int compareTo(MethodeVerweis gegenstelleWert) {
            int vergleichWert = eigentümerWert.compareTo(gegenstelleWert.eigentümerWert);
            if (vergleichWert == 0) vergleichWert = Name.compareTo(gegenstelleWert.Name);
            return vergleichWert == 0 ? beschreibungWert.compareTo(gegenstelleWert.beschreibungWert) : vergleichWert;
        }
        public boolean equals(Object gegenstelleWert) { return gegenstelleWert instanceof MethodeVerweis && compareTo((MethodeVerweis) gegenstelleWert) == 0; }
        public int hashCode() { return Objects.hash(eigentümerWert, Name, beschreibungWert); }
    }
    static final class KlasseDaten {
        final int[] konstanteArt;
        final Object[] konstanteDaten;
        final String Name;
        final List<MitgliedDaten> feldWert, Funktion;
        KlasseDaten(Path pfad) throws IOException {
            DatenLeser leserWert = new DatenLeser(Files.readAllBytes(pfad));
            if (leserWert.ganzzahltypLesen() != 0xcafebabe) throw new ÜbersetzungFehler("Java klasseWert 표식이 아님");
            leserWert.lesen(4);
            int elementeintragAnzahl = leserWert.kurzLesen(); konstanteArt = new int[elementeintragAnzahl]; konstanteDaten = new Object[elementeintragAnzahl];
            for (int ordnungszahlIndex = 1; ordnungszahlIndex < elementeintragAnzahl; ordnungszahlIndex++) {
                int artWert = leserWert.byteLesen(); konstanteArt[ordnungszahlIndex] = artWert;
                switch (artWert) {
                    case 1:
                        int Länge = leserWert.kurzLesen();
                        byte[] zeichenPuffer = leserWert.lesen(Länge), längeMitVorsilbeDaten = new byte[Länge + 2];
                        längeMitVorsilbeDaten[0] = (byte)(Länge >> 8); längeMitVorsilbeDaten[1] = (byte)Länge;
                        System.arraycopy(zeichenPuffer, 0, längeMitVorsilbeDaten, 2, Länge);
                        konstanteDaten[ordnungszahlIndex] = new DataInputStream(new ByteArrayInputStream(längeMitVorsilbeDaten)).readUTF(); break;
                    case 3: konstanteDaten[ordnungszahlIndex] = leserWert.ganzzahltypLesen(); break;
                    case 4: leserWert.lesen(4); break;
                    case 5: case 6: leserWert.lesen(8); ordnungszahlIndex++; break;
                    case 7: case 8: case 16: konstanteDaten[ordnungszahlIndex] = leserWert.kurzLesen(); break;
                    case 9: case 10: case 11: case 12: case 18:
                        konstanteDaten[ordnungszahlIndex] = new int[]{leserWert.kurzLesen(), leserWert.kurzLesen()}; break;
                    case 15: konstanteDaten[ordnungszahlIndex] = new int[]{leserWert.byteLesen(), leserWert.kurzLesen()}; break;
                    default: throw new ÜbersetzungFehler("지원하지 않는 konstanteWert artWert: " + artWert);
                }
            }
            leserWert.kurzLesen(); Name = klasseName(leserWert.kurzLesen());
            if (!klasseName(leserWert.kurzLesen()).equals("java/lang/Object") || leserWert.kurzLesen() != 0)
                throw new ÜbersetzungFehler(Name + ": 상속 및 인터페이스 istNichtUnterstützt");
            feldWert = mitgliederLesen(leserWert); Funktion = mitgliederLesen(leserWert); attributlisteLesen(leserWert);
            if (leserWert.position != leserWert.Daten.length) throw new ÜbersetzungFehler("klasseWert 뒤에 남은 Daten");
        }
        String Zeichen(int Nummer) {
            if (Nummer < 1 || Nummer >= konstanteArt.length || konstanteArt[Nummer] != 1) throw new ÜbersetzungFehler("Zeichen konstanteWert Nummer fehler");
            return (String) konstanteDaten[Nummer];
        }
        String klasseName(int Nummer) {
            if (Nummer < 1 || Nummer >= konstanteArt.length || konstanteArt[Nummer] != 7) throw new ÜbersetzungFehler("klasseWert verweis fehler");
            return Zeichen((Integer)konstanteDaten[Nummer]);
        }
        MethodeVerweis verweis(int Nummer) {
            if (Nummer < 1 || Nummer >= konstanteArt.length || konstanteArt[Nummer] < 9 || konstanteArt[Nummer] > 11) throw new ÜbersetzungFehler("멤버 verweis fehler");
            int[] paarWert = (int[])konstanteDaten[Nummer], namePaar = (int[])konstanteDaten[paarWert[1]];
            return new MethodeVerweis(klasseName(paarWert[0]), Zeichen(namePaar[0]), Zeichen(namePaar[1]));
        }
        Map<String, byte[]> attributlisteLesen(DatenLeser leserWert) {
            Map<String, byte[]> ergebnis = new LinkedHashMap<>();
            int elementeintragAnzahl = leserWert.kurzLesen();
            for (int ordnungszahlIndex = 0; ordnungszahlIndex < elementeintragAnzahl; ordnungszahlIndex++) {
                String attributName = Zeichen(leserWert.kurzLesen()); byte[] Wert = leserWert.lesen(leserWert.ganzzahltypLesen());
                if (ergebnis.put(attributName, Wert) != null) throw new ÜbersetzungFehler("겹친 attributWert: " + attributName);
            }
            return ergebnis;
        }
        List<MitgliedDaten> mitgliederLesen(DatenLeser leserWert) {
            List<MitgliedDaten> ergebnis = new ArrayList<>(); int elementeintragAnzahl = leserWert.kurzLesen();
            for (int ordnungszahlIndex = 0; ordnungszahlIndex < elementeintragAnzahl; ordnungszahlIndex++) {
                int zugriffEintrag = leserWert.kurzLesen(); String methodeEintragName = Zeichen(leserWert.kurzLesen()), beschreibungWert = Zeichen(leserWert.kurzLesen());
                ergebnis.add(new MitgliedDaten(zugriffEintrag, methodeEintragName, beschreibungWert, attributlisteLesen(leserWert)));
            }
            return ergebnis;
        }
    }
    static final class MethodeDeskriptor {
        final List<String> argumente = new ArrayList<>();
        final String zurückkehrenErgebnis;
        MethodeDeskriptor(String beschreibungWert) {
            if (!beschreibungWert.startsWith("(")) throw new ÜbersetzungFehler("Funktion beschreibungWert fehler: " + beschreibungWert);
            int endung = beschreibungWert.indexOf(')'); if (endung < 0) throw new ÜbersetzungFehler("Funktion beschreibungWert fehler: " + beschreibungWert);
            argumente.addAll(typenAnalysieren(beschreibungWert.substring(1, endung)));
            List<String> zurückgegebenWerte = typenAnalysieren(beschreibungWert.substring(endung + 1));
            if (argumente.contains("V") || zurückgegebenWerte.size() != 1) throw new ÜbersetzungFehler("Funktion beschreibungWert fehler: " + beschreibungWert);
            zurückkehrenErgebnis = zurückgegebenWerte.get(0);
        }
    }
    static List<String> typenAnalysieren(String beschreibungWert) {
        List<String> ergebnis = new ArrayList<>();
        String[] erlaubtFormat = {"Ljava/lang/String;", "[I", "I", "Z", "B", "C", "S", "V"};
        for (int position = 0; position < beschreibungWert.length();) {
            String auswahlWert = null;
            for (String formatWert : erlaubtFormat) if (beschreibungWert.startsWith(formatWert, position)) { auswahlWert = formatWert; break; }
            if (auswahlWert == null) throw new ÜbersetzungFehler("지원하지 않는 datenTyp: " + beschreibungWert);
            ergebnis.add(auswahlWert); position += auswahlWert.length();
        }
        return ergebnis;
    }
    static String symbol(String artWert, String... teile) {
        try {
            byte[] prüfsummeDatei = MessageDigest.getInstance("SHA-256").digest(String.join("\0", teile).getBytes(StandardCharsets.UTF_8));
            StringBuilder Text = new StringBuilder("j_" + artWert + "_");
            for (int ordnungszahlIndex = 0; ordnungszahlIndex < 12; ordnungszahlIndex++) Text.append(String.format(Locale.ROOT, "%02x", prüfsummeDatei[ordnungszahlIndex] & 255));
            return Text.toString();
        } catch (Exception fehler) { throw new ÜbersetzungFehler(fehler.toString()); }
    }
    final Map<String, KlasseDaten> klassenListe = new TreeMap<>();
    final Map<MethodeVerweis, MitgliedDaten> methodenListe = new TreeMap<>(), datenfelderListe = new TreeMap<>();
    final Map<String, String> zeichenketteWerte = new LinkedHashMap<>(), maschineFunktionen = new LinkedHashMap<>();
    final String ausführungZielobjekt, maschineKlasse;
    final int speicherhaldeMaschinenwortAnzahl;
    final Path betriebsmittelEintragPfad;
    Vorabübersetzung(List<Path> pfadListe, String zielobjektWert, int lexikalischMaschinenwortAnzahl, Path betriebsmittelEintragWert) throws IOException {
        if ((!zielobjektWert.equals("kernel") && !zielobjektWert.equals("user")) || lexikalischMaschinenwortAnzahl < 1024 || lexikalischMaschinenwortAnzahl > 1048576) throw new ÜbersetzungFehler("befehlAusführen zielobjektWert 또는 Speicher adresseGebiet größe fehler");
        ausführungZielobjekt = zielobjektWert; speicherhaldeMaschinenwortAnzahl = lexikalischMaschinenwortAnzahl; betriebsmittelEintragPfad = betriebsmittelEintragWert;
        // Auch dieser Name wird beim Erzeugen der Länderquellen übersetzt.
        maschineKlasse = zielobjektWert.equals("kernel") ? "Platine" : "Benutzer";
        for (String zeile : Files.readAllLines(betriebsmittelEintragWert.resolve("MaschineFunktionen.tsv"), StandardCharsets.UTF_8)) {
            String[] teile = zeile.split("\t", -1);
            if (teile.length != 4) throw new ÜbersetzungFehler("maschine Funktion Daten fehler");
            if (teile[0].equals(zielobjektWert)) maschineFunktionen.put(teile[1] + teile[2], teile[3]);
        }
        for (Path pfad : pfadListe) {
            KlasseDaten Daten = new KlasseDaten(pfad);
            if (klassenListe.put(Daten.Name, Daten) != null) throw new ÜbersetzungFehler("중복 klasseWert: " + Daten.Name);
            for (MitgliedDaten feldWert : Daten.feldWert) {
                if ((feldWert.zugriffEintrag & 8) == 0 || typenAnalysieren(feldWert.beschreibungWert).equals(Collections.singletonList("V"))) throw new ÜbersetzungFehler("statischWert 필드만 unterstützungWert");
                if (datenfelderListe.put(new MethodeVerweis(Daten.Name, feldWert.Name, feldWert.beschreibungWert), feldWert) != null) throw new ÜbersetzungFehler("중복 feldWert");
            }
            for (MitgliedDaten Funktion : Daten.Funktion) {
                if (Funktion.Name.equals("<init>")) continue;
                if ((Funktion.zugriffEintrag & 8) == 0 || (Funktion.zugriffEintrag & (0x20 | 0x400)) != 0) throw new ÜbersetzungFehler("statischWert 비동기화 함수만 unterstützungWert");
                new MethodeDeskriptor(Funktion.beschreibungWert);
                if (methodenListe.put(new MethodeVerweis(Daten.Name, Funktion.Name, Funktion.beschreibungWert), Funktion) != null) throw new ÜbersetzungFehler("중복 Funktion");
            }
        }
    }
    String zeichenketteSymbol(String Text) { return zeichenketteWerte.computeIfAbsent(Text, Wert -> "j_text_" + zeichenketteWerte.size()); }
    String konstanteAusdruck(KlasseDaten Daten, int Nummer) {
        if (Nummer < 1 || Nummer >= Daten.konstanteArt.length) throw new ÜbersetzungFehler("konstanteWert Nummer beschneiden fehler");
        if (Daten.konstanteArt[Nummer] == 3) return "(word)(uint32_t)(" + Daten.konstanteDaten[Nummer] + ")";
        if (Daten.konstanteArt[Nummer] == 8) return "(word)" + zeichenketteSymbol(Daten.Zeichen((Integer)Daten.konstanteDaten[Nummer]));
        throw new ÜbersetzungFehler("정수와 Zeichenkette 상수만 unterstützungWert");
    }
    String methodePrototyp(MethodeVerweis verweis) {
        List<String> argumenteListe = new ArrayList<>(); int elementeintragAnzahl = new MethodeDeskriptor(verweis.beschreibungWert).argumente.size();
        for (int ordnungszahlIndex = 0; ordnungszahlIndex < elementeintragAnzahl; ordnungszahlIndex++) argumenteListe.add("word a" + ordnungszahlIndex);
        return "static word " + symbol("method", verweis.teile()) + "(" + (elementeintragAnzahl == 0 ? "void" : String.join(", ", argumenteListe)) + ")";
    }
    void lokalPrüfen(int Nummer, int lokalVariableAnzahl) { if (Nummer < 0 || Nummer >= lokalVariableAnzahl) throw new ÜbersetzungFehler("lokalGültigkeitsbereich variableWert Nummer beschneiden fehler"); }
    void verzweigungAusgeben(List<String> Ausgabe, Set<Integer> verzweigungListe, int position, int bewegungGesamtmenge, String bedingung) {
        int zielWert = position + bewegungGesamtmenge; verzweigungListe.add(zielWert);
        Ausgabe.add((bedingung == null ? "" : "if (" + bedingung + ") ") + "goto b" + zielWert + ";");
    }
    String methodeRumpf(MethodeVerweis Funktion, MitgliedDaten Daten) {
        byte[] rumpfDaten = Daten.attributWert.get("Code"); if (rumpfDaten == null) throw new ÜbersetzungFehler("Funktion 몸체가 fehlendMethode: " + Funktion.Name);
        DatenLeser leserWert = new DatenLeser(rumpfDaten); int stapelTiefe = leserWert.kurzLesen(), lokalVariableAnzahl = leserWert.kurzLesen();
        DatenLeser befehlDaten = new DatenLeser(leserWert.lesen(leserWert.ganzzahltypLesen()));
        if (leserWert.kurzLesen() != 0) throw new ÜbersetzungFehler("try/catch/finally istNichtUnterstützt");
        MethodeDeskriptor formatWert = new MethodeDeskriptor(Funktion.beschreibungWert); if (lokalVariableAnzahl < formatWert.argumente.size()) throw new ÜbersetzungFehler("매개변수보다 적은 lokalGültigkeitsbereich variableWert");
        KlasseDaten klasseWert = klassenListe.get(Funktion.eigentümerWert);
        List<String> Ausgabe = new ArrayList<>(); Ausgabe.add(methodePrototyp(Funktion) + " {");
        Ausgabe.add("word s[" + Math.max(stapelTiefe, 1) + "], l[" + Math.max(lokalVariableAnzahl, 1) + "] = {0}, a,b,c,d; size_t sp = 0;");
        for (int ordnungszahlIndex = 0; ordnungszahlIndex < formatWert.argumente.size(); ordnungszahlIndex++) Ausgabe.add("l[" + ordnungszahlIndex + "] = a" + ordnungszahlIndex + ";");
        Set<Integer> grenzstellenListe = new HashSet<>(), verzweigungListe = new HashSet<>();
        String[] vergleicheListe = {"==", "!=", "<", ">=", ">", "<=", "==", "!="};
        while (befehlDaten.position < befehlDaten.Daten.length) {
            int position = befehlDaten.position, befehl = befehlDaten.byteLesen(); grenzstellenListe.add(position); Ausgabe.add("b" + position + ":;");
            if (befehl == 0) continue;
            if (befehl == 1) Ausgabe.add("PUSH(0);");
            else if (befehl >= 2 && befehl <= 8) Ausgabe.add("PUSH((uint32_t)(" + (befehl - 3) + "));");
            else if (befehl == 16 || befehl == 17) Ausgabe.add("PUSH((uint32_t)(" + (befehl == 16 ? befehlDaten.vorzeichenbehaftetByteLesen() : befehlDaten.vorzeichenbehaftetKurzLesen()) + "));");
            else if (befehl == 18 || befehl == 19) Ausgabe.add("PUSH(" + konstanteAusdruck(klasseWert, befehl == 18 ? befehlDaten.byteLesen() : befehlDaten.kurzLesen()) + ");");
            else if (befehl == 21 || befehl == 25 || (befehl >= 26 && befehl <= 29) || (befehl >= 42 && befehl <= 45)) {
                int Nummer = befehl == 21 || befehl == 25 ? befehlDaten.byteLesen() : befehl - (befehl <= 29 ? 26 : 42);
                lokalPrüfen(Nummer, lokalVariableAnzahl); Ausgabe.add("PUSH(l[" + Nummer + "]);");
            } else if (befehl == 54 || befehl == 58 || (befehl >= 59 && befehl <= 62) || (befehl >= 75 && befehl <= 78)) {
                int Nummer = befehl == 54 || befehl == 58 ? befehlDaten.byteLesen() : befehl - (befehl <= 62 ? 59 : 75);
                lokalPrüfen(Nummer, lokalVariableAnzahl); Ausgabe.add("l[" + Nummer + "] = POP();");
            } else if (befehl == 46) Ausgabe.add("b = POP(); a = POP(); PUSH(*checked(a,(int32_t)b));");
            else if (befehl == 79) Ausgabe.add("c = POP(); b = POP(); a = POP(); *checked(a,(int32_t)b) = (uint32_t)c;");
            else if (befehl == 87 || befehl == 88) Ausgabe.add(befehl == 87 ? "(void)POP();" : "(void)POP(); (void)POP();");
            else if (befehl >= 89 && befehl <= 95) {
                int[] elementeintragAnzahlen = {1,2,3,2,3,4,2}; String[] reihenfolgeListe = {"aa","aba","acba","baba","bacba","badcba","ab"};
                for (int ordnungszahlIndex = 0; ordnungszahlIndex < elementeintragAnzahlen[befehl - 89]; ordnungszahlIndex++) Ausgabe.add("abcd".charAt(ordnungszahlIndex) + " = POP();");
                for (char Wert : reihenfolgeListe[befehl - 89].toCharArray()) Ausgabe.add("PUSH(" + Wert + ");");
            } else if (befehl == 96 || befehl == 100 || befehl == 104 || befehl == 126 || befehl == 128 || befehl == 130) {
                String vorgangWert = befehl == 96 ? "+" : befehl == 100 ? "-" : befehl == 104 ? "*" : befehl == 126 ? "&" : befehl == 128 ? "|" : "^";
                Ausgabe.add("b = POP(); a = POP(); PUSH((uint32_t)a " + vorgangWert + " (uint32_t)b);");
            } else if (befehl == 108 || befehl == 112) Ausgabe.add("b = POP(); a = POP(); PUSH(divide(a,b," + (befehl == 112 ? 1 : 0) + "));");
            else if (befehl == 116) Ausgabe.add("a = POP(); PUSH(0u-(uint32_t)a);");
            else if (befehl == 120 || befehl == 122 || befehl == 124) {
                Ausgabe.add("b = POP(); a = POP();"); Ausgabe.add("PUSH(" + (befehl == 122 ? "arithmetic_shift(a,b)" : "(uint32_t)a " + (befehl == 120 ? "<<" : ">>") + " ((uint32_t)b & 31)") + ");");
            } else if (befehl == 132) {
                int Nummer = befehlDaten.byteLesen(), erhöhenSchrittGesamtmenge = befehlDaten.vorzeichenbehaftetByteLesen(); lokalPrüfen(Nummer, lokalVariableAnzahl);
                Ausgabe.add("l[" + Nummer + "] = (uint32_t)l[" + Nummer + "] + (uint32_t)(" + erhöhenSchrittGesamtmenge + ");");
            } else if (befehl >= 145 && befehl <= 147) Ausgabe.add("a = POP(); PUSH((uint32_t)(" + (befehl == 145 ? "int8_t" : befehl == 146 ? "uint16_t" : "int16_t") + ")a);");
            else if (befehl >= 153 && befehl <= 158) {
                Ausgabe.add("a = POP();"); verzweigungAusgeben(Ausgabe, verzweigungListe, position, befehlDaten.vorzeichenbehaftetKurzLesen(), "(int32_t)a " + vergleicheListe[befehl - 153] + " 0");
            } else if (befehl >= 159 && befehl <= 166) {
                Ausgabe.add("b = POP(); a = POP();"); verzweigungAusgeben(Ausgabe, verzweigungListe, position, befehlDaten.vorzeichenbehaftetKurzLesen(), befehl >= 165 ? "a " + vergleicheListe[befehl - 159] + " b" : "(int32_t)a " + vergleicheListe[befehl - 159] + " (int32_t)b");
            } else if (befehl == 167 || befehl == 200) verzweigungAusgeben(Ausgabe, verzweigungListe, position, befehl == 167 ? befehlDaten.vorzeichenbehaftetKurzLesen() : befehlDaten.ganzzahltypLesen(), null);
            else if (befehl == 170 || befehl == 171) {
                while (befehlDaten.position % 4 != 0) befehlDaten.byteLesen();
                int standardwertWert = befehlDaten.ganzzahltypLesen(); Ausgabe.add("a = POP();");
                if (befehl == 170) {
                    int unterkanteWert = befehlDaten.ganzzahltypLesen(), oberkanteWert = befehlDaten.ganzzahltypLesen(); long elementeintragAnzahl = (long)oberkanteWert - unterkanteWert + 1;
                    if (elementeintragAnzahl < 1 || elementeintragAnzahl > (befehlDaten.Daten.length - befehlDaten.position) / 4) throw new ÜbersetzungFehler("switch beschneiden fehler");
                    for (long Wert = unterkanteWert; Wert <= oberkanteWert; Wert++) verzweigungAusgeben(Ausgabe, verzweigungListe, position, befehlDaten.ganzzahltypLesen(), "(int32_t)a == (" + Wert + ")");
                } else {
                    int elementeintragAnzahl = befehlDaten.ganzzahltypLesen(), vorderseiteDaten = 0;
                    if (elementeintragAnzahl < 0 || elementeintragAnzahl > (befehlDaten.Daten.length - befehlDaten.position) / 8) throw new ÜbersetzungFehler("switch größe fehler");
                    for (int ordnungszahlIndex = 0; ordnungszahlIndex < elementeintragAnzahl; ordnungszahlIndex++) {
                        int Wert = befehlDaten.ganzzahltypLesen(); if (ordnungszahlIndex > 0 && Wert <= vorderseiteDaten) throw new ÜbersetzungFehler("switch reihenfolgeWert fehler"); vorderseiteDaten = Wert;
                        verzweigungAusgeben(Ausgabe, verzweigungListe, position, befehlDaten.ganzzahltypLesen(), "(int32_t)a == (" + Wert + ")");
                    }
                }
                verzweigungAusgeben(Ausgabe, verzweigungListe, position, standardwertWert, null);
            } else if (befehl == 172 || befehl == 176 || befehl == 177) Ausgabe.add("return " + (befehl == 177 ? "0" : "POP()") + ";");
            else if (befehl == 178 || befehl == 179) {
                MethodeVerweis verweis = klasseWert.verweis(befehlDaten.kurzLesen()); if (!datenfelderListe.containsKey(verweis)) throw new ÜbersetzungFehler("알 Zahl 없는 feldWert");
                Ausgabe.add(symbol("init", verweis.eigentümerWert) + "();"); String feldWert = symbol("field", verweis.teile());
                Ausgabe.add(befehl == 178 ? "PUSH(" + feldWert + ");" : feldWert + " = POP();");
            } else if (befehl == 184) {
                MethodeVerweis verweis = klasseWert.verweis(befehlDaten.kurzLesen()); if (!methodenListe.containsKey(verweis)) throw new ÜbersetzungFehler("알 Zahl 없는 Funktion");
                MethodeDeskriptor aufrufTyp = new MethodeDeskriptor(verweis.beschreibungWert); int elementeintragAnzahl = aufrufTyp.argumente.size();
                Ausgabe.add(symbol("init", verweis.eigentümerWert) + "();"); Ausgabe.add("if(sp < " + elementeintragAnzahl + ") kernel_panic(\"call stack underflow\"); sp -= " + elementeintragAnzahl + ";");
                List<String> aufrufArgumente = new ArrayList<>(); for (int ordnungszahlIndex = 0; ordnungszahlIndex < elementeintragAnzahl; ordnungszahlIndex++) aufrufArgumente.add("s[sp + " + ordnungszahlIndex + "]");
                Ausgabe.add("a = " + symbol("method", verweis.teile()) + "(" + String.join(",", aufrufArgumente) + ");");
                if (!aufrufTyp.zurückkehrenErgebnis.equals("V")) Ausgabe.add("PUSH(a);");
            } else if (befehl == 182) {
                MethodeVerweis verweis = klasseWert.verweis(befehlDaten.kurzLesen());
                if (verweis.equals(new MethodeVerweis("java/lang/String", "length", "()I"))) Ausgabe.add("a = POP(); PUSH(length(a));");
                else if (verweis.equals(new MethodeVerweis("java/lang/String", "charAt", "(I)C"))) Ausgabe.add("b = POP(); a = POP(); PUSH(*checked(a,(int32_t)b));");
                else throw new ÜbersetzungFehler("가상 Funktion aufrufen istNichtUnterstützt");
            } else if (befehl == 188) {
                if (befehlDaten.byteLesen() != 10) throw new ÜbersetzungFehler("new int[]만 unterstützungWert"); Ausgabe.add("a = POP(); PUSH(new_array((int32_t)a));");
            } else if (befehl == 190) Ausgabe.add("a = POP(); PUSH(length(a));");
            else if (befehl == 196) {
                int erweiterungWert = befehlDaten.byteLesen(), Nummer = befehlDaten.kurzLesen(); lokalPrüfen(Nummer, lokalVariableAnzahl);
                if (erweiterungWert == 21 || erweiterungWert == 25) Ausgabe.add("PUSH(l[" + Nummer + "]);");
                else if (erweiterungWert == 54 || erweiterungWert == 58) Ausgabe.add("l[" + Nummer + "] = POP();");
                else if (erweiterungWert == 132) Ausgabe.add("l[" + Nummer + "] = (uint32_t)l[" + Nummer + "] + (uint32_t)(" + befehlDaten.vorzeichenbehaftetKurzLesen() + ");");
                else throw new ÜbersetzungFehler("istNichtUnterstützt wide befehl");
            } else if (befehl == 198 || befehl == 199) {
                Ausgabe.add("a = POP();"); verzweigungAusgeben(Ausgabe, verzweigungListe, position, befehlDaten.vorzeichenbehaftetKurzLesen(), "a " + (befehl == 198 ? "==" : "!=") + " 0");
            } else throw new ÜbersetzungFehler(Funktion.eigentümerWert + "." + Funktion.Name + ", byteWert " + position + ": istNichtUnterstützt befehl " + befehl);
        }
        if (!grenzstellenListe.containsAll(verzweigungListe)) throw new ÜbersetzungFehler("befehl 경계가 아닌 곳으로 verzweigung");
        Ausgabe.add("kernel_panic(\"method fell through\"); }"); return String.join("\n", Ausgabe);
    }
    String exportierenMethode(String bindenSymbol, String zielobjektWert, boolean hatEintragPunkt) {
        int positionIndex = zielobjektWert.lastIndexOf('.'); if (positionIndex < 0 || !bindenSymbol.matches("[A-Za-z_][A-Za-z0-9_]*")) throw new ÜbersetzungFehler("wertAusgeben zuweisenWert fehler");
        String eigentümerWert = zielobjektWert.substring(0, positionIndex).replace('.', '/'), Name = zielobjektWert.substring(positionIndex + 1); MethodeVerweis auswahlWert = null;
        for (MethodeVerweis verweis : methodenListe.keySet()) if (verweis.eigentümerWert.equals(eigentümerWert) && verweis.Name.equals(Name)) {
            if (auswahlWert != null) throw new ÜbersetzungFehler("겹친 wertAusgeben zielobjektWert"); auswahlWert = verweis;
        }
        if (auswahlWert == null || (methodenListe.get(auswahlWert).zugriffEintrag & 0x100) != 0) throw new ÜbersetzungFehler("내보낼 함수가 fehlendMethode 또는 native Funktion");
        MethodeDeskriptor formatWert = new MethodeDeskriptor(auswahlWert.beschreibungWert);
        if ((hatEintragPunkt && !formatWert.argumente.isEmpty()) || !Arrays.asList("V", "I").contains(formatWert.zurückkehrenErgebnis)) throw new ÜbersetzungFehler("eintragPunktWert 또는 C grenzstelleWert formatWert fehler");
        List<String> argumenteListe = new ArrayList<>(), aufrufArgumente = new ArrayList<>();
        for (int ordnungszahlIndex = 0; ordnungszahlIndex < formatWert.argumente.size(); ordnungszahlIndex++) {
            if (!formatWert.argumente.get(ordnungszahlIndex).equals("I")) throw new ÜbersetzungFehler("C 경계는 int 인수만 unterstützungWert");
            argumenteListe.add("int32_t a" + ordnungszahlIndex); aufrufArgumente.add("(uint32_t)a" + ordnungszahlIndex);
        }
        return (formatWert.zurückkehrenErgebnis.equals("V") ? "void " : "int32_t ") + bindenSymbol + "(" + (argumenteListe.isEmpty() ? "void" : String.join(",", argumenteListe)) + ") { " + symbol("init", auswahlWert.eigentümerWert) + "(); " + (formatWert.zurückkehrenErgebnis.equals("V") ? "" : "return (int32_t)") + symbol("method", auswahlWert.teile()) + "(" + String.join(",", aufrufArgumente) + "); }";
    }
    String generieren(String eintragPunkt, List<String> exportierenEinträge, boolean allgemeingültigSchreibweise) throws IOException {
        List<String> deklarationenListe = new ArrayList<>(), rümpfeListe = new ArrayList<>(), feldDeklarationen = new ArrayList<>();
        for (Map.Entry<MethodeVerweis, MitgliedDaten> eintragWert : methodenListe.entrySet()) {
            MethodeVerweis verweis = eintragWert.getKey(); MitgliedDaten Daten = eintragWert.getValue(); deklarationenListe.add(methodePrototyp(verweis) + ";");
            if ((Daten.zugriffEintrag & 0x100) != 0) {
                String verbinden = maschineFunktionen.get(verweis.Name + verweis.beschreibungWert);
                if (!verweis.eigentümerWert.equals(maschineKlasse) || verbinden == null) throw new ÜbersetzungFehler("허용되지 않은 native Funktion: " + verweis.Name);
                int elementeintragAnzahl = new MethodeDeskriptor(verweis.beschreibungWert).argumente.size(); List<String> argumenteListe = new ArrayList<>();
                for (int ordnungszahlIndex = 0; ordnungszahlIndex < elementeintragAnzahl; ordnungszahlIndex++) argumenteListe.add("a" + ordnungszahlIndex);
                deklarationenListe.add("extern word " + verbinden + "(" + (elementeintragAnzahl == 0 ? "void" : String.join(",", Collections.nCopies(elementeintragAnzahl, "word"))) + ");");
                rümpfeListe.add(methodePrototyp(verweis) + " { return " + verbinden + "(" + String.join(",", argumenteListe) + "); }");
            } else rümpfeListe.add(methodeRumpf(verweis, Daten));
        }
        for (Map.Entry<MethodeVerweis, MitgliedDaten> eintragWert : datenfelderListe.entrySet()) {
            MethodeVerweis verweis = eintragWert.getKey(); byte[] konstanteWert = eintragWert.getValue().attributWert.get("ConstantValue");
            String Wert = konstanteWert == null ? "0" : konstanteAusdruck(klassenListe.get(verweis.eigentümerWert), new DatenLeser(konstanteWert).kurzLesen());
            feldDeklarationen.add("static word " + symbol("field", verweis.teile()) + " = " + Wert + ";");
        }
        for (String Name : klassenListe.keySet()) {
            String initialisieren = symbol("init", Name), statuswertWert = symbol("state", Name);
            deklarationenListe.add("static void " + initialisieren + "(void);"); feldDeklarationen.add("static unsigned " + statuswertWert + ";");
            MethodeVerweis verweis = new MethodeVerweis(Name, "<clinit>", "()V");
            rümpfeListe.add("static void " + initialisieren + "(void) { if(" + statuswertWert + ") return; " + statuswertWert + " = 1; " + (methodenListe.containsKey(verweis) ? symbol("method", verweis.teile()) + "(); " : "") + statuswertWert + " = 2; }");
        }
        rümpfeListe.add(exportierenMethode("java_entry", eintragPunkt, true)); Set<String> exportiertName = new HashSet<>();
        for (String zuweisenWert : exportierenEinträge) {
            int positionIndex = zuweisenWert.indexOf('='); if (positionIndex < 1) throw new ÜbersetzungFehler("wertAusgeben zuweisenWert fehler");
            String Name = zuweisenWert.substring(0, positionIndex); exportiertName.add(Name); rümpfeListe.add(exportierenMethode(Name, zuweisenWert.substring(positionIndex + 1), false));
        }
        List<String> zeichenketteDeklarationen = new ArrayList<>();
        for (Map.Entry<String, String> eintragWert : zeichenketteWerte.entrySet()) {
            String Text = eintragWert.getKey(); StringBuilder datenfeldWert = new StringBuilder("static const word " + eintragWert.getValue() + "[] = {" + Text.length());
            for (int ordnungszahlIndex = 0; ordnungszahlIndex < Text.length(); ordnungszahlIndex++) datenfeldWert.append(", ").append((int)Text.charAt(ordnungszahlIndex));
            zeichenketteDeklarationen.add(datenfeldWert.append("};").toString());
        }
        String unterstützungWert = Files.readString(betriebsmittelEintragPfad.resolve("LaufzeitUnterstützung.c.txt"), StandardCharsets.UTF_8).replace("262144", Integer.toString(speicherhaldeMaschinenwortAnzahl));
        return erzeugtQuelltextLokalisieren(unterstützungWert + String.join("\n", zeichenketteDeklarationen) + "\n" + String.join("\n", deklarationenListe) + "\n" + String.join("\n", feldDeklarationen) + "\n" + String.join("\n", rümpfeListe) + "\n", exportiertName, allgemeingültigSchreibweise);
    }
    String erzeugtQuelltextLokalisieren(String Quelltext, Set<String> exportiertName, boolean allgemeingültigSchreibweise) throws IOException {
        Map<String, String> nameTabelle = new HashMap<>();
        for (String zeile : Files.readAllLines(betriebsmittelEintragPfad.resolve("ErzeugtNamen.tsv"), StandardCharsets.UTF_8)) {
            String[] paarWert = zeile.split("\t"); nameTabelle.put(paarWert[0], paarWert[1]);
        }
        Pattern teilblockAusdruck = Pattern.compile("//[^\\n]*|/\\*[\\s\\S]*?\\*/|\"(?:\\\\.|[^\"\\\\])*\"|'(?:\\\\.|[^'\\\\])*'|\\b[A-Za-z_]\\w*\\b");
        Matcher sucherWert = teilblockAusdruck.matcher(Quelltext); StringBuffer ergebnis = new StringBuffer();
        while (sucherWert.find()) {
            String Name = sucherWert.group(), neuName = Name;
            if (!Name.startsWith("//") && !Name.startsWith("/*") && !Name.startsWith("\"") && !Name.startsWith("'") && !exportiertName.contains(Name)) {
                neuName = nameTabelle.getOrDefault(Name, Name);
                if (Name.matches("a[0-9]+")) neuName = "argumente" + Name.substring(1);
                if (Name.matches("b[0-9]+")) neuName = "verzweigung" + Name.substring(1);
                if (allgemeingültigSchreibweise) {
                    StringBuilder schreibweiseWert = new StringBuilder();
                    for (char zeichenWert : neuName.toCharArray()) schreibweiseWert.append(zeichenWert < 128 ? Character.toString(zeichenWert) : String.format(Locale.ROOT, "\\u%04x", (int)zeichenWert));
                    neuName = schreibweiseWert.toString();
                }
            }
            sucherWert.appendReplacement(ergebnis, Matcher.quoteReplacement(neuName));
        }
        sucherWert.appendTail(ergebnis); return ergebnis.toString();
    }
    String x86Methodenrumpf(MethodeVerweis Funktion, MitgliedDaten Daten, Map<String,String> maschineTabelle, String zielobjektWert) {
        String markierungWert = symbol("method", Funktion.teile());
        List<String> zeile = new ArrayList<>();
        if ((Daten.zugriffEintrag & 0x100) != 0) {
            String verbinden = maschineTabelle.get(Funktion.Name + Funktion.beschreibungWert);
            if (!Funktion.eigentümerWert.equals(zielobjektWert.equals("kernel") ? "Gerät" : "Benutzer") || verbinden == null) throw new ÜbersetzungFehler("허용되지 않은 native Funktion");
            return ".text\n" + markierungWert + ":\njmp " + verbinden;
        }
        byte[] rumpfText = Daten.attributWert.get("Code"); if (rumpfText == null) throw new ÜbersetzungFehler("Funktion 몸체가 fehlendMethode");
        DatenLeser leserWert = new DatenLeser(rumpfText); leserWert.kurzLesen(); int lokalAnzahl = leserWert.kurzLesen();
        DatenLeser befehlDaten = new DatenLeser(leserWert.lesen(leserWert.ganzzahltypLesen()));
        if (leserWert.kurzLesen() != 0) throw new ÜbersetzungFehler("try/catch/finally istNichtUnterstützt");
        MethodeDeskriptor formatWert = new MethodeDeskriptor(Funktion.beschreibungWert); if (lokalAnzahl < formatWert.argumente.size()) throw new ÜbersetzungFehler("매개변수보다 적은 lokalGültigkeitsbereich variableWert");
        Collections.addAll(zeile,".text",".globl " + markierungWert,".type " + markierungWert + ", @function",markierungWert + ":","pushl %ebp","movl %esp, %ebp","subl $" + lokalAnzahl * 4 + ", %esp");
        for (int ordnungszahlIndex = 0; ordnungszahlIndex < formatWert.argumente.size(); ordnungszahlIndex++) Collections.addAll(zeile,"movl " + (8 + 4 * (formatWert.argumente.size() - ordnungszahlIndex - 1)) + "(%ebp), %eax","movl %eax, -" + (4 * (ordnungszahlIndex + 1)) + "(%ebp)");
        KlasseDaten klasseWert = klassenListe.get(Funktion.eigentümerWert); Set<Integer> grenzstellenListe = new HashSet<>(), verzweigungListe = new HashSet<>();
        String[] vergleicheListe = {"je","jne","jl","jge","jg","jle","je","jne"};
        while (befehlDaten.position < befehlDaten.Daten.length) {
            int position = befehlDaten.position, befehl = befehlDaten.byteLesen(); String positionIndex = markierungWert + "_b" + position;
            zeile.add(positionIndex + ":"); grenzstellenListe.add(position);
            if (befehl == 0) zeile.add("nop");
            else if (befehl == 1) zeile.add("pushl $0");
            else if (befehl >= 2 && befehl <= 8) zeile.add("pushl $" + (befehl - 3));
            else if (befehl == 16 || befehl == 17) zeile.add("pushl $" + (befehl == 16 ? befehlDaten.vorzeichenbehaftetByteLesen() : befehlDaten.vorzeichenbehaftetKurzLesen()));
            else if (befehl == 18 || befehl == 19) {
                int Nummer = befehl == 18 ? befehlDaten.byteLesen() : befehlDaten.kurzLesen();
                zeile.add("pushl $" + x86Konstante(klasseWert,Nummer));
            } else if (befehl == 21 || befehl == 25 || (befehl >= 26 && befehl <= 29) || (befehl >= 42 && befehl <= 45) || befehl == 54 || befehl == 58 || (befehl >= 59 && befehl <= 62) || (befehl >= 75 && befehl <= 78)) {
                boolean ergebnisLesen = befehl < 54; int Nummer = befehl == 21 || befehl == 25 || befehl == 54 || befehl == 58 ? befehlDaten.byteLesen() : befehl - (befehl <= 29 ? 26 : befehl <= 45 ? 42 : befehl <= 62 ? 59 : 75);
                lokalPrüfen(Nummer,lokalAnzahl); zeile.add((ergebnisLesen ? "pushl " : "popl ") + "-" + (4 * (Nummer + 1)) + "(%ebp)");
            } else if (befehl == 46) Collections.addAll(zeile,"popl %ecx","popl %eax","call rt_array_check","pushl 4(%eax,%ecx,4)");
            else if (befehl == 79) Collections.addAll(zeile,"popl %edx","popl %ecx","popl %eax","call rt_array_check","movl %edx, 4(%eax,%ecx,4)");
            else if (befehl == 87 || befehl == 88) zeile.add("addl $" + (befehl == 87 ? 4 : 8) + ", %esp");
            else if (befehl >= 89 && befehl <= 95) {
                int[] elementeintragAnzahlen = {1,2,3,2,3,4,2}; int[][] reihenfolgeListe = {{0,0},{0,1,0},{0,2,1,0},{1,0,1,0},{1,0,2,1,0},{1,0,3,2,1,0},{0,1}}; String[] werteRegister = {"%eax","%ecx","%edx","%ebx"};
                for (int ordnungszahlIndex = 0; ordnungszahlIndex < elementeintragAnzahlen[befehl - 89]; ordnungszahlIndex++) zeile.add("popl " + werteRegister[ordnungszahlIndex]);
                for (int ordnungszahlIndex : reihenfolgeListe[befehl - 89]) zeile.add("pushl " + werteRegister[ordnungszahlIndex]);
            } else if (befehl == 96 || befehl == 100 || befehl == 104 || befehl == 126 || befehl == 128 || befehl == 130) {
                String vorgangWert = befehl == 96 ? "addl" : befehl == 100 ? "subl" : befehl == 104 ? "imull" : befehl == 126 ? "andl" : befehl == 128 ? "orl" : "xorl";
                Collections.addAll(zeile,"popl %ecx","popl %eax",vorgangWert + " %ecx, %eax","pushl %eax");
            } else if (befehl == 108 || befehl == 112) Collections.addAll(zeile,"popl %ecx","popl %eax","testl %ecx, %ecx","jz rt_div_zero","cmpl $-1, %ecx","jne " + positionIndex + "_divide","cmpl $0x80000000, %eax","jne " + positionIndex + "_divide","xorl %edx, %edx","jmp " + positionIndex + "_done",positionIndex + "_divide:","cltd","idivl %ecx",positionIndex + "_done:","pushl " + (befehl == 108 ? "%eax" : "%edx"));
            else if (befehl == 116) zeile.add("negl (%esp)");
            else if (befehl == 120 || befehl == 122 || befehl == 124) Collections.addAll(zeile,"popl %ecx","popl %eax",(befehl == 120 ? "sall" : befehl == 122 ? "sarl" : "shrl") + " %cl, %eax","pushl %eax");
            else if (befehl == 132) {
                int Nummer = befehlDaten.byteLesen(), erhöhenSchrittWert = befehlDaten.vorzeichenbehaftetByteLesen(); lokalPrüfen(Nummer,lokalAnzahl); zeile.add("addl $" + erhöhenSchrittWert + ", -" + (4 * (Nummer + 1)) + "(%ebp)");
            } else if (befehl >= 145 && befehl <= 147) Collections.addAll(zeile,"popl %eax",befehl == 145 ? "movsbl %al, %eax" : befehl == 146 ? "movzwl %ax, %eax" : "movswl %ax, %eax","pushl %eax");
            else if (befehl >= 153 && befehl <= 166) {
                if (befehl <= 158) Collections.addAll(zeile,"popl %eax","testl %eax, %eax");
                else Collections.addAll(zeile,"popl %ecx","popl %eax","cmpl %ecx, %eax");
                int zielWert = position + befehlDaten.vorzeichenbehaftetKurzLesen(); verzweigungListe.add(zielWert); zeile.add(vergleicheListe[befehl - (befehl <= 158 ? 153 : 159)] + " " + markierungWert + "_b" + zielWert);
            } else if (befehl == 167 || befehl == 200) {
                int zielWert = position + (befehl == 167 ? befehlDaten.vorzeichenbehaftetKurzLesen() : befehlDaten.ganzzahltypLesen()); verzweigungListe.add(zielWert); zeile.add("jmp " + markierungWert + "_b" + zielWert);
            } else if (befehl == 170 || befehl == 171) {
                while (befehlDaten.position % 4 != 0) befehlDaten.byteLesen();
                int standardwertWert = position + befehlDaten.ganzzahltypLesen(); verzweigungListe.add(standardwertWert); zeile.add("popl %eax");
                int elementeintragAnzahl, unterkanteWert = 0;
                if (befehl == 170) { unterkanteWert = befehlDaten.ganzzahltypLesen(); int oberkanteWert = befehlDaten.ganzzahltypLesen(); long Länge = (long)oberkanteWert - unterkanteWert + 1; if (Länge < 1 || Länge > (befehlDaten.Daten.length - befehlDaten.position) / 4) throw new ÜbersetzungFehler("switch beschneiden fehler"); elementeintragAnzahl = (int)Länge; }
                else { elementeintragAnzahl = befehlDaten.ganzzahltypLesen(); if (elementeintragAnzahl < 0 || elementeintragAnzahl > (befehlDaten.Daten.length - befehlDaten.position) / 8) throw new ÜbersetzungFehler("switch größe fehler"); }
                for (int ordnungszahlIndex = 0; ordnungszahlIndex < elementeintragAnzahl; ordnungszahlIndex++) {
                    int Wert = befehl == 170 ? unterkanteWert + ordnungszahlIndex : befehlDaten.ganzzahltypLesen(), zielWert = position + befehlDaten.ganzzahltypLesen(); verzweigungListe.add(zielWert);
                    Collections.addAll(zeile,"cmpl $" + Wert + ", %eax","je " + markierungWert + "_b" + zielWert);
                }
                zeile.add("jmp " + markierungWert + "_b" + standardwertWert);
            } else if (befehl == 172 || befehl == 176 || befehl == 177) {
                if (befehl != 177) zeile.add("popl %eax"); Collections.addAll(zeile,"leave","ret");
            } else if (befehl == 178 || befehl == 179) {
                MethodeVerweis verweis = klasseWert.verweis(befehlDaten.kurzLesen()); if (!datenfelderListe.containsKey(verweis)) throw new ÜbersetzungFehler("알 Zahl 없는 feldWert");
                Collections.addAll(zeile,"call " + symbol("init",verweis.eigentümerWert),(befehl == 178 ? "pushl " : "popl ") + symbol("field",verweis.teile()));
            } else if (befehl == 184) {
                MethodeVerweis verweis = klasseWert.verweis(befehlDaten.kurzLesen()); if (!methodenListe.containsKey(verweis)) throw new ÜbersetzungFehler("알 Zahl 없는 Funktion");
                MethodeDeskriptor aufrufTyp = new MethodeDeskriptor(verweis.beschreibungWert); Collections.addAll(zeile,"call " + symbol("init",verweis.eigentümerWert),"call " + symbol("method",verweis.teile()));
                if (!aufrufTyp.argumente.isEmpty()) zeile.add("addl $" + aufrufTyp.argumente.size() * 4 + ", %esp");
                if (!aufrufTyp.zurückkehrenErgebnis.equals("V")) zeile.add("pushl %eax");
            } else if (befehl == 182) {
                MethodeVerweis verweis = klasseWert.verweis(befehlDaten.kurzLesen());
                if (verweis.equals(new MethodeVerweis("java/lang/String","length","()I"))) Collections.addAll(zeile,"popl %eax","testl %eax, %eax","jz rt_null","pushl (%eax)");
                else if (verweis.equals(new MethodeVerweis("java/lang/String","charAt","(I)C"))) Collections.addAll(zeile,"popl %ecx","popl %eax","call rt_array_check","pushl 4(%eax,%ecx,4)");
                else throw new ÜbersetzungFehler("가상 Funktion aufrufen istNichtUnterstützt");
            } else if (befehl == 188) {
                if (befehlDaten.byteLesen() != 10) throw new ÜbersetzungFehler("new int[]만 unterstützungWert"); Collections.addAll(zeile,"popl %eax","call rt_new_array","pushl %eax");
            } else if (befehl == 190) Collections.addAll(zeile,"popl %eax","testl %eax, %eax","jz rt_null","pushl (%eax)");
            else if (befehl == 196) {
                int erweiterungWert = befehlDaten.byteLesen(), Nummer = befehlDaten.kurzLesen(); lokalPrüfen(Nummer,lokalAnzahl);
                if (erweiterungWert == 21 || erweiterungWert == 25 || erweiterungWert == 54 || erweiterungWert == 58) zeile.add((erweiterungWert <= 25 ? "pushl " : "popl ") + "-" + 4 * (Nummer + 1) + "(%ebp)");
                else if (erweiterungWert == 132) zeile.add("addl $" + befehlDaten.vorzeichenbehaftetKurzLesen() + ", -" + 4 * (Nummer + 1) + "(%ebp)");
                else throw new ÜbersetzungFehler("wide befehl istNichtUnterstützt");
            } else if (befehl == 198 || befehl == 199) {
                int zielWert = position + befehlDaten.vorzeichenbehaftetKurzLesen(); verzweigungListe.add(zielWert); Collections.addAll(zeile,"popl %eax","testl %eax, %eax",(befehl == 198 ? "je " : "jne ") + markierungWert + "_b" + zielWert);
            } else throw new ÜbersetzungFehler("istNichtUnterstützt befehl: " + befehl);
        }
        if (!grenzstellenListe.containsAll(verzweigungListe)) throw new ÜbersetzungFehler("befehl 경계가 아닌 곳으로 verzweigung");
        zeile.add(".size " + markierungWert + ", .-" + markierungWert); return String.join("\n",zeile);
    }
    String x86Konstante(KlasseDaten Daten, int Nummer) {
        if (Daten.konstanteArt[Nummer] == 3) return Daten.konstanteDaten[Nummer].toString();
        if (Daten.konstanteArt[Nummer] == 8) return zeichenketteSymbol(Daten.Zeichen((Integer)Daten.konstanteDaten[Nummer]));
        throw new ÜbersetzungFehler("정수와 Zeichenkette 상수만 unterstützungWert");
    }
    String x86Assemblertext(String eintragPunkt, List<String> exportiertWert, String zielobjektWert) throws IOException {
        Map<String,String> maschineTabelle = new HashMap<>();
        for (String zeile : Files.readAllLines(betriebsmittelEintragPfad.resolve("x86Maschinenfunktionen.tsv"))) { String[] paarWert = zeile.split("\t"); if (paarWert[0].equals(zielobjektWert)) maschineTabelle.put(paarWert[1] + paarWert[2],paarWert[3]); }
        int positionIndex = eintragPunkt.lastIndexOf('.'); if (positionIndex < 0) throw new ÜbersetzungFehler("eintragPunkt zuweisenWert fehler");
        String eigentümerWert = eintragPunkt.substring(0,positionIndex).replace('.','/'), methodeEintragName = eintragPunkt.substring(positionIndex + 1); MethodeVerweis eintragPunktWert = null;
        for (String beschreibungWert : Arrays.asList("()I","()V")) { MethodeVerweis verweis = new MethodeVerweis(eigentümerWert,methodeEintragName,beschreibungWert); if (methodenListe.containsKey(verweis)) { if (eintragPunktWert != null) throw new ÜbersetzungFehler("겹친 eintragPunkt"); eintragPunktWert = verweis; } }
        if (eintragPunktWert == null || (methodenListe.get(eintragPunktWert).zugriffEintrag & 0x100) != 0) throw new ÜbersetzungFehler("eintragPunktWert Funktion formatWert fehler");
        List<String> zeile = new ArrayList<>(); zeile.add(".code32");
        for (KlasseDaten Daten : klassenListe.values()) {
            String statuswertWert = symbol("state",Daten.Name), initialisieren = symbol("init",Daten.Name);
            Collections.addAll(zeile,".bss",".balign 4",statuswertWert + ": .long 0",".text",initialisieren + ":","cmpl $0, " + statuswertWert,"jne " + initialisieren + "_done","movl $1, " + statuswertWert);
            MethodeVerweis initialisiererVerweis = new MethodeVerweis(Daten.Name,"<clinit>","()V"); if (methodenListe.containsKey(initialisiererVerweis)) zeile.add("call " + symbol("method",initialisiererVerweis.teile()));
            Collections.addAll(zeile,"movl $2, " + statuswertWert,initialisieren + "_done:","ret");
            for (MitgliedDaten feldWert : Daten.feldWert) {
                byte[] konstanteWert = feldWert.attributWert.get("ConstantValue"); String Wert = konstanteWert == null ? "0" : x86Konstante(Daten,new DatenLeser(konstanteWert).kurzLesen());
                Collections.addAll(zeile,".data",".balign 4",symbol("field",Daten.Name,feldWert.Name,feldWert.beschreibungWert) + ": .long " + Wert);
            }
            for (MitgliedDaten Funktion : Daten.Funktion) if (!Funktion.Name.equals("<init>")) zeile.add(x86Methodenrumpf(new MethodeVerweis(Daten.Name,Funktion.Name,Funktion.beschreibungWert),Funktion,maschineTabelle,zielobjektWert));
        }
        Collections.addAll(zeile,".text",".globl java_entry","java_entry:","call " + symbol("init",eintragPunktWert.eigentümerWert),"call " + symbol("method",eintragPunktWert.teile()));
        if (eintragPunktWert.beschreibungWert.equals("()V")) zeile.add("xorl %eax, %eax"); zeile.add("ret");
        for (String zuweisenWert : exportiertWert) {
            int trennzeichenWert = zuweisenWert.indexOf('='); if (trennzeichenWert < 1) throw new ÜbersetzungFehler("wertAusgeben zuweisenWert fehler");
            String externWert = zuweisenWert.substring(0,trennzeichenWert), Funktion = zuweisenWert.substring(trennzeichenWert + 1); int divisionErgebnis = Funktion.lastIndexOf('.');
            if (divisionErgebnis < 0 || !externWert.matches("[A-Za-z_][A-Za-z0-9_]*")) throw new ÜbersetzungFehler("wertAusgeben symbol fehler");
            String klasseWert = Funktion.substring(0,divisionErgebnis).replace('.','/'), Name = Funktion.substring(divisionErgebnis + 1); MethodeVerweis auswahlWert = null;
            for (MethodeVerweis verweis : methodenListe.keySet()) if (verweis.eigentümerWert.equals(klasseWert) && verweis.Name.equals(Name)) { if (auswahlWert != null) throw new ÜbersetzungFehler("겹친 wertAusgeben zielobjektWert"); auswahlWert = verweis; }
            if (auswahlWert == null) throw new ÜbersetzungFehler("내보낼 함수가 fehlendMethode");
            Collections.addAll(zeile,".text",".globl " + externWert,externWert + ":","call " + symbol("init",auswahlWert.eigentümerWert),"jmp " + symbol("method",auswahlWert.teile()));
        }
        zeile.add(".section .rodata");
        for (Map.Entry<String,String> eintragWert : zeichenketteWerte.entrySet()) {
            Collections.addAll(zeile,".balign 4",eintragWert.getValue() + ":",".long " + eintragWert.getKey().length());
            List<String> einheitenListe = new ArrayList<>(); for (char einheitWert : eintragWert.getKey().toCharArray()) einheitenListe.add(Integer.toString(einheitWert)); if (!einheitenListe.isEmpty()) zeile.add(".long " + String.join(",",einheitenListe));
        }
        zeile.add(".section .note.GNU-stack,\"\",@progbits"); return String.join("\n",zeile) + "\n";
    }
    static void werkzeugAusführen(List<String> befehl) throws Exception {
        if (new ProcessBuilder(befehl).inheritIO().start().waitFor() != 0) throw new ÜbersetzungFehler("quelltextÜbersetzen fehler: " + befehl.get(0));
    }
    static String datenZeichenkette(String Text) { return "\"" + Text.replace("\\","\\\\").replace("\"","\\\"").replace("\n","\\n").replace("\r","\\r").replace("\t","\\t") + "\""; }
    static void x86Übersetzung(List<Path> eingabeListe, String zielobjektWert, String eintragPunkt, List<String> exportiertWert, Path Ausgabe, Path betriebsmittelEintragWert) throws Exception {
        Path vorläufigWert = Files.createTempDirectory("jkoros-java-x86-"), klassePfad = vorläufigWert.resolve("classes"); Files.createDirectory(klassePfad);
        try {
            List<String> javaBefehl = new ArrayList<>(Arrays.asList("javac","-J-XX:-UsePerfData","--release","8","-encoding","UTF-8","-g:none","-proc:none","-implicit:none","-classpath",klassePfad.toString(),"-sourcepath",klassePfad.toString(),"-d",klassePfad.toString()));
            List<Path> bytecode = new ArrayList<>(); int quelltextAnzahl = 0;
            for (Path Eingabewert : eingabeListe) {
                if (Ausgabe.toAbsolutePath().normalize().equals(Eingabewert.toAbsolutePath().normalize())) throw new ÜbersetzungFehler("Ausgabe 파일과 입력이 gleichText");
                if (Eingabewert.toString().endsWith(".java")) { javaBefehl.add(Eingabewert.toString()); quelltextAnzahl++; }
                else if (Eingabewert.toString().endsWith(".class")) bytecode.add(Eingabewert);
                else throw new ÜbersetzungFehler(".java 또는 .class만 unterstützungWert");
            }
            if (quelltextAnzahl > 0) werkzeugAusführen(javaBefehl);
            try (java.util.stream.Stream<Path> pfadListe = Files.walk(klassePfad)) { pfadListe.filter(pfad -> pfad.toString().endsWith(".class")).sorted().forEach(bytecode::add); }
            Vorabübersetzung wertUmwandeln = new Vorabübersetzung(bytecode,zielobjektWert.equals("user") ? "user" : "kernel",262144,betriebsmittelEintragWert);
            String wertZusammenbauen = wertUmwandeln.x86Assemblertext(eintragPunkt,exportiertWert,zielobjektWert); Files.writeString(vorläufigWert.resolve("program.s"),wertZusammenbauen,StandardCharsets.UTF_8);
            Path werkzeugPosition = betriebsmittelEintragWert.getParent();
            werkzeugAusführen(Arrays.asList("as","--32","-o",vorläufigWert.resolve("program.o").toString(),vorläufigWert.resolve("program.s").toString()));
            werkzeugAusführen(Arrays.asList("as","--32","-o",vorläufigWert.resolve("runtime.o").toString(),werkzeugPosition.resolve("LaufzeitUnterstützung.s").toString()));
            List<String> verbinden = new ArrayList<>(Arrays.asList("ld","-m","elf_i386"));
            if (zielobjektWert.equals("kernel")) verbinden.add("-r");
            else {
                werkzeugAusführen(Arrays.asList("as","--32","-o",vorläufigWert.resolve("start.o").toString(),werkzeugPosition.resolve(zielobjektWert.equals("user") ? "benutzerProgrammStarten.s" : "linuxAnlauf.s").toString()));
                Collections.addAll(verbinden,"-e","_start",vorläufigWert.resolve("start.o").toString());
                if (zielobjektWert.equals("user")) Collections.addAll(verbinden,"-T",werkzeugPosition.resolve("benutzerBindenAnordnung.ld").toString());
            }
            Collections.addAll(verbinden,"-o",vorläufigWert.resolve("result").toString(),vorläufigWert.resolve("program.o").toString(),vorläufigWert.resolve("runtime.o").toString()); werkzeugAusführen(verbinden);
            Ausgabe = Ausgabe.toAbsolutePath(); Files.createDirectories(Ausgabe.getParent()); Path veröffentlichenWert = Files.createTempFile(Ausgabe.getParent(),".elf-",".tmp");
            try { Files.copy(vorläufigWert.resolve("result"),veröffentlichenWert,StandardCopyOption.REPLACE_EXISTING); Files.move(veröffentlichenWert,Ausgabe,StandardCopyOption.REPLACE_EXISTING); } finally { Files.deleteIfExists(veröffentlichenWert); }
            Files.setPosixFilePermissions(Ausgabe,java.nio.file.attribute.PosixFilePermissions.fromString(zielobjektWert.equals("linux") ? "rwxr-xr-x" : "rw-r--r--"));
            Files.writeString(Paths.get(Ausgabe + ".s"),wertZusammenbauen,StandardCharsets.UTF_8);
            List<String> symbolDaten = new ArrayList<>(), quelltextDaten = new ArrayList<>();
            for (MethodeVerweis verweis : wertUmwandeln.methodenListe.keySet()) symbolDaten.add(datenZeichenkette(symbol("method",verweis.teile())) + ":" + datenZeichenkette(verweis.eigentümerWert + "." + verweis.Name + verweis.beschreibungWert));
            for (Path Eingabewert : eingabeListe) {
                byte[] prüfsummeDatei = MessageDigest.getInstance("SHA-256").digest(Files.readAllBytes(Eingabewert)); StringBuilder Text = new StringBuilder(); for (byte Wert : prüfsummeDatei) Text.append(String.format(Locale.ROOT,"%02x",Wert & 255));
                quelltextDaten.add(datenZeichenkette(Eingabewert.toAbsolutePath().toString()) + ":" + datenZeichenkette(Text.toString()));
            }
            Files.writeString(Paths.get(Ausgabe + ".json"),"{\"target\":" + datenZeichenkette(zielobjektWert) + ",\"entry\":" + datenZeichenkette(eintragPunkt) + ",\"format\":\"ELF32 i386\",\"runtime_jvm\":false,\"symbols\":{" + String.join(",",symbolDaten) + "},\"sources\":{" + String.join(",",quelltextDaten) + "}}\n",StandardCharsets.UTF_8);
        } finally {
            try (java.util.stream.Stream<Path> pfadListe = Files.walk(vorläufigWert)) { for (Path pfad : (Iterable<Path>)pfadListe.sorted(Comparator.reverseOrder())::iterator) Files.deleteIfExists(pfad); }
        }
    }
    public static void main(String[] argumente) {
        try {
            String eintragPunkt = null, zielobjektWert = "kernel", x86Übersetzungsziel = null; Path ausgabePfad = null; int lexikalischMaschinenwortAnzahl = 262144; boolean allgemeingültigSchreibweise = false;
            List<String> exportiertWert = new ArrayList<>(); List<Path> pfadListe = new ArrayList<>();
            for (int ordnungszahlIndex = 0; ordnungszahlIndex < argumente.length; ordnungszahlIndex++) {
                String Wert = argumente[ordnungszahlIndex];
                switch (Wert) {
                    case "--target": x86Übersetzungsziel = argumente[++ordnungszahlIndex]; break;
                    case "--help": case "-h": System.out.println("사용법: --entry klasseWert.Funktion -o Ausgabe [--target linux|kernel|user] [--profile kernel|user] [--export symbol=klasseWert.Funktion] 클래스파일 또는 Java원문"); return;
                    case "--entry": eintragPunkt = argumente[++ordnungszahlIndex]; break;
                    case "--profile": zielobjektWert = argumente[++ordnungszahlIndex]; break;
                    case "--heap-words": lexikalischMaschinenwortAnzahl = Integer.parseInt(argumente[++ordnungszahlIndex]); break;
                    case "--export": exportiertWert.add(argumente[++ordnungszahlIndex]); break;
                    case "-o": ausgabePfad = Paths.get(argumente[++ordnungszahlIndex]); break;
                    case "--ucn": allgemeingültigSchreibweise = true; break;
                    default: if (Wert.startsWith("-")) throw new ÜbersetzungFehler("알 Zahl 없는 옵션: " + Wert); pfadListe.add(Paths.get(Wert));
                }
            }
            if (eintragPunkt == null || ausgabePfad == null || pfadListe.isEmpty()) throw new ÜbersetzungFehler("--entry, -o, klasseWert 파일이 필요합니다");
            Path betriebsmittelEintragWert = Paths.get(System.getProperty("jkoros.compiler.resources"));
            if (x86Übersetzungsziel != null) {
                if (!Arrays.asList("linux","kernel","user").contains(x86Übersetzungsziel)) throw new ÜbersetzungFehler("알 Zahl 없는 befehlAusführen zielobjektWert");
                x86Übersetzung(pfadListe,x86Übersetzungsziel,eintragPunkt,exportiertWert,ausgabePfad,betriebsmittelEintragWert); return;
            }
            String Quelltext = new Vorabübersetzung(pfadListe, zielobjektWert, lexikalischMaschinenwortAnzahl, betriebsmittelEintragWert).generieren(eintragPunkt, exportiertWert, allgemeingültigSchreibweise);
            ausgabePfad = ausgabePfad.toAbsolutePath(); Files.createDirectories(ausgabePfad.getParent());
            Path vorläufigWert = Files.createTempFile(ausgabePfad.getParent(), ".aot-", ".tmp");
            try { Files.writeString(vorläufigWert, Quelltext, StandardCharsets.UTF_8); Files.move(vorläufigWert, ausgabePfad, StandardCopyOption.REPLACE_EXISTING); }
            finally { Files.deleteIfExists(vorläufigWert); }
        } catch (Exception fehler) { System.err.println("quelltextÜbersetzen fehler: " + fehler.getMessage()); System.exit(1); }
    }
}
