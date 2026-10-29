// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.security.MessageDigest;
import java.util.*;

/** Java-Hostwerkzeug zum Prüfen und Wiederherstellen von Abhängigkeiten sowie Bauen und Starten einer unabhängigen Länderausgabe. */
public final class Länderstarter {
    static final class DatenStrukturanalysierer {
        final String Quelltext; int position;
        DatenStrukturanalysierer(String Text) { Quelltext = Text; }
        void leerraumÜberspringen() { while (position < Quelltext.length() && Character.isWhitespace(Quelltext.charAt(position))) position++; }
        Object lesen() {
            leerraumÜberspringen(); char zeichenWert = Quelltext.charAt(position++);
            if (zeichenWert == '{') {
                Map<String,Object> ergebnis = new LinkedHashMap<>(); leerraumÜberspringen();
                if (Quelltext.charAt(position) == '}') { position++; return ergebnis; }
                while (true) {
                    String Name = (String)lesen(); leerraumÜberspringen(); if (Quelltext.charAt(position++) != ':') throw new IllegalArgumentException("Daten trennzeichenWert fehler");
                    ergebnis.put(Name, lesen()); leerraumÜberspringen(); char trennzeichenWert = Quelltext.charAt(position++);
                    if (trennzeichenWert == '}') return ergebnis; if (trennzeichenWert != ',') throw new IllegalArgumentException("Daten trennzeichenWert fehler");
                }
            }
            if (zeichenWert == '[') {
                List<Object> ergebnis = new ArrayList<>(); leerraumÜberspringen();
                if (Quelltext.charAt(position) == ']') { position++; return ergebnis; }
                while (true) {
                    ergebnis.add(lesen()); leerraumÜberspringen(); char trennzeichenWert = Quelltext.charAt(position++);
                    if (trennzeichenWert == ']') return ergebnis; if (trennzeichenWert != ',') throw new IllegalArgumentException("Daten trennzeichenWert fehler");
                }
            }
            if (zeichenWert == '"') {
                StringBuilder ergebnis = new StringBuilder();
                while (true) {
                    char nächsterElementeintrag = Quelltext.charAt(position++); if (nächsterElementeintrag == '"') return ergebnis.toString();
                    if (nächsterElementeintrag == '\\') {
                        nächsterElementeintrag = Quelltext.charAt(position++);
                        if (nächsterElementeintrag == 'u') { ergebnis.append((char)Integer.parseInt(Quelltext.substring(position, position + 4),16)); position += 4; continue; }
                        if (nächsterElementeintrag == 'n') nächsterElementeintrag = '\n'; else if (nächsterElementeintrag == 'r') nächsterElementeintrag = '\r'; else if (nächsterElementeintrag == 't') nächsterElementeintrag = '\t';
                        else if (nächsterElementeintrag == 'b') nächsterElementeintrag = '\b'; else if (nächsterElementeintrag == 'f') nächsterElementeintrag = '\f';
                        else if (nächsterElementeintrag != '"' && nächsterElementeintrag != '\\' && nächsterElementeintrag != '/') throw new IllegalArgumentException("Zeichen 이스케이프 fehler");
                    }
                    ergebnis.append(nächsterElementeintrag);
                }
            }
            int ausführenVorgang = position - 1;
            while (position < Quelltext.length() && ",]} \t\r\n".indexOf(Quelltext.charAt(position)) < 0) position++;
            String Wert = Quelltext.substring(ausführenVorgang, position);
            if (Wert.equals("true")) return Boolean.TRUE; if (Wert.equals("false")) return Boolean.FALSE; if (Wert.equals("null")) return null;
            return Double.valueOf(Wert);
        }
    }
    static String prüfsummeDatei(Path pfad) throws Exception {
        MessageDigest berechnung = MessageDigest.getInstance("SHA-256"); byte[] Daten = new byte[1024 * 1024];
        try (InputStream Eingabewert = Files.newInputStream(pfad)) { for (int Länge; (Länge = Eingabewert.read(Daten)) >= 0;) berechnung.update(Daten,0,Länge); }
        return prüfsummeText(berechnung.digest());
    }
    static String prüfsummeText(byte[] Daten) {
        StringBuilder Text = new StringBuilder(); for (byte Wert : Daten) Text.append(String.format(Locale.ROOT,"%02x",Wert & 255)); return Text.toString();
    }
    static Path internPfad(Path projektWurzel, String Name) {
        Path ergebnis = projektWurzel.resolve(Name).normalize();
        if (Name.isEmpty() || Paths.get(Name).isAbsolute() || !ergebnis.startsWith(projektWurzel) || Name.indexOf('\\') >= 0)
            throw new IllegalArgumentException("범위를 벗어난 pfad: " + Name);
        for (Path unterteilWert : Paths.get(Name)) if (unterteilWert.toString().equals("..")) throw new IllegalArgumentException("상위 pfad unzulässigWert: " + Name);
        for (Path aktuellElementeintrag = ergebnis; aktuellElementeintrag != null && aktuellElementeintrag.startsWith(projektWurzel); aktuellElementeintrag = aktuellElementeintrag.getParent())
            if (Files.isSymbolicLink(aktuellElementeintrag)) throw new IllegalArgumentException("abhängigkeiten 경로의 링크 unzulässigWert: " + Name);
        return ergebnis;
    }
    static String befehlAusgabe(List<String> befehl) throws Exception {
        Process prozessWert = new ProcessBuilder(befehl).redirectError(ProcessBuilder.Redirect.INHERIT).start();
        String ergebnis = new String(prozessWert.getInputStream().readAllBytes(),StandardCharsets.UTF_8);
        if (prozessWert.waitFor() != 0) throw new IOException("befehl fehlschlagWert: " + befehl.get(0)); return ergebnis;
    }
    static void extrahieren(Path archivWert, Path zielWert) throws Exception {
        for (String Name : befehlAusgabe(Arrays.asList("tar","-tzf",archivWert.toString())).split("\n")) internPfad(zielWert, Name);
        for (String zeile : befehlAusgabe(Arrays.asList("tar","-tvzf",archivWert.toString())).split("\n"))
            if (!zeile.isEmpty() && zeile.charAt(0) != '-' && zeile.charAt(0) != 'd') throw new IOException("externWert 링크 또는 besondersWert 파일을 포함한 abhängigkeiten");
        Files.createDirectories(zielWert);
        int statuswertWert = new ProcessBuilder("tar","--no-same-owner","--no-same-permissions","-xzf",archivWert.toString(),"-C",zielWert.toString()).inheritIO().start().waitFor();
        if (statuswertWert != 0) throw new IOException("abhängigkeiten archivWert speichergerätFreigeben fehlschlagWert");
    }
    static void aufrufen(Path arbeitendPfad, Path Werkzeuge, List<String> argumente, Map<String,String> umgebung) throws Exception {
        List<String> befehl = new ArrayList<>(Arrays.asList("python3", Werkzeuge.toString())); befehl.addAll(argumente);
        ProcessBuilder befehlAusführen = new ProcessBuilder(befehl).directory(arbeitendPfad.toFile()).inheritIO(); befehlAusführen.environment().putAll(umgebung);
        int statuswertWert = befehlAusführen.start().waitFor(); if (statuswertWert != 0) throw new IOException("Werkzeuge fehlschlagWert: " + Werkzeuge + " (" + statuswertWert + ")");
    }
    @SuppressWarnings("unchecked")
    public static void main(String[] argumente) throws Exception {
        if (argumente.length < 1) throw new IllegalArgumentException("build, run, desktop, image, check, test-system 중 동작을 지정하세요");
        String aktion = argumente[0];
        if (!Arrays.asList("build","run","desktop","image","check","test-system").contains(aktion)) throw new IllegalArgumentException("알 Zahl 없는 aktion");
        Path projektWurzel = Paths.get(System.getProperty("worldos.edition.root")).toAbsolutePath().normalize();
        Map<String,Object> einstellungen = (Map<String,Object>)new DatenStrukturanalysierer(Files.readString(projektWurzel.resolve("native.json"),StandardCharsets.UTF_8)).lesen();
        Path quelltextBaum = internPfad(projektWurzel,(String)einstellungen.get("source")), betriebskernWert = internPfad(quelltextBaum,(String)einstellungen.get("native"));
        List<String> eigenständigDateien = (List<String>)(List<?>)einstellungen.get("owned_files");
        for (String Name : eigenständigDateien) if (!Files.isRegularFile(internPfad(quelltextBaum,Name))) throw new IOException("quelltextBaum fehlendMethode: " + Name);
        if (aktion.equals("check")) { System.out.println(einstellungen.get("country") + " " + einstellungen.get("language") + " 독립 quelltextBaum überprüfen istFertig"); return; }
        String betriebsmittelEintragRelativPfad = (String)einstellungen.getOrDefault("resource_root", ".");
        if (!betriebsmittelEintragRelativPfad.equals(".") && !betriebsmittelEintragRelativPfad.equals("..")) throw new IllegalArgumentException("abhängigkeiten projektWurzel pfad fehler");
        Path betriebsmittelEintragWert = projektWurzel.resolve(betriebsmittelEintragRelativPfad).normalize(); Path archivWert = betriebsmittelEintragWert.resolve("native-vendor.tar.gz");
        String erwartetPrüfsumme = (String)einstellungen.get("vendor_sha256");
        if (!prüfsummeDatei(archivWert).equals(erwartetPrüfsumme)) throw new IOException("abhängigkeiten SHA-256 불일치");
        Path markierungWert = quelltextBaum.resolve(".vendor-sha256");
        if (!Files.isRegularFile(markierungWert) || !Files.readString(markierungWert).trim().equals(erwartetPrüfsumme)) { extrahieren(archivWert, quelltextBaum); Files.writeString(markierungWert,erwartetPrüfsumme + "\n"); }
        Map<String,String> umgebung = new HashMap<>(System.getenv());
        Path ipConfig = null;
        if (umgebung.containsKey("IP_CONFIG")) ipConfig = Paths.get(umgebung.get("IP_CONFIG")).toAbsolutePath().normalize();
        else for (Path parent = projektWurzel; parent != null; parent = parent.getParent()) {
            if (Files.isRegularFile(parent.resolve("ip.conf"))) { ipConfig = parent.resolve("ip.conf"); break; }
        }
        if (ipConfig == null) ipConfig = quelltextBaum.resolve("ip.conf");
        if (!Files.isRegularFile(ipConfig)) throw new IOException("Missing ip.conf: " + ipConfig);
        umgebung.put("IP_CONFIG", ipConfig.toString());
        if (Arrays.asList("run","desktop","test-system").contains(aktion) && !umgebung.containsKey("QEMU_AARCH64")) {
            Path ProgrammStarter = betriebsmittelEintragWert.resolve("host/qemu"), starterMarkierung = betriebsmittelEintragWert.resolve("host/.qemu-sha256");
            String starterPrüfsumme = (String)einstellungen.get("qemu_sha256");
            if (!Files.isRegularFile(ProgrammStarter) || !Files.isRegularFile(starterMarkierung) || !Files.readString(starterMarkierung).trim().equals(starterPrüfsumme)) {
                Path starterArchiv = betriebsmittelEintragWert.resolve("qemu-host.tar.gz"); if (!prüfsummeDatei(starterArchiv).equals(starterPrüfsumme)) throw new IOException("QEMU SHA-256 불일치");
                extrahieren(starterArchiv,betriebsmittelEintragWert.resolve("host")); Files.writeString(starterMarkierung,starterPrüfsumme + "\n");
            }
            umgebung.put("QEMU_AARCH64",ProgrammStarter.toString());
        }
        MessageDigest berechnung = MessageDigest.getInstance("SHA-256"); Collections.sort(eigenständigDateien);
        for (String Name : eigenständigDateien) { berechnung.update(Name.getBytes(StandardCharsets.UTF_8)); berechnung.update(Files.readAllBytes(internPfad(quelltextBaum,Name))); }
        berechnung.update("ip.conf\0".getBytes(StandardCharsets.UTF_8)); berechnung.update(Files.readAllBytes(ipConfig));
        String quelltextPrüfsumme = prüfsummeText(berechnung.digest()); Path markierungErzeugenAbbild = betriebskernWert.resolve("build/worldos-source.sha256");
        if (aktion.equals("build") || !Files.isRegularFile(markierungErzeugenAbbild) || !Files.readString(markierungErzeugenAbbild).trim().equals(quelltextPrüfsumme)) {
            aufrufen(betriebskernWert,internPfad(betriebskernWert,(String)einstellungen.get("builder")),Collections.emptyList(),umgebung);
            Files.writeString(markierungErzeugenAbbild,quelltextPrüfsumme + "\n");
        }
        List<String> starterArgumente = new ArrayList<>(Arrays.asList(argumente).subList(1,argumente.length));
        if (aktion.equals("run") || aktion.equals("desktop")) {
            if (aktion.equals("desktop")) starterArgumente.add(0,"--desktop");
            aufrufen(betriebskernWert,internPfad(betriebskernWert,(String)einstellungen.get("runner")),starterArgumente,umgebung);
        } else if (aktion.equals("image")) aufrufen(betriebskernWert,internPfad(betriebskernWert,(String)einstellungen.get("image_builder")),starterArgumente,umgebung);
        else if (aktion.equals("test-system")) {
            starterArgumente.add(0,projektWurzel.toString()); starterArgumente.add(0,"--edition");
            aufrufen(betriebskernWert,internPfad(betriebskernWert,(String)einstellungen.get("system_tester")),starterArgumente,umgebung);
        }
    }
}
