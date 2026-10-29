// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.security.MessageDigest;
import java.util.*;

/** 독립 국가판의 의존성 검사·복원·bouwen·실행을 맡는 host Java hulpmiddelen. */
public final class Country_app_lade {
    static final class gegevens_parser {
        final String broncode; int positie;
        gegevens_parser(String tekst) { broncode = tekst; }
        void 빈칸() { while (positie < broncode.length() && Character.isWhitespace(broncode.charAt(positie))) positie++; }
        Object Lezen() {
            빈칸(); char teken_WAARDE = broncode.charAt(positie++);
            if (teken_WAARDE == '{') {
                Map<String,Object> resultaat = new LinkedHashMap<>(); 빈칸();
                if (broncode.charAt(positie) == '}') { positie++; return resultaat; }
                while (true) {
                    String Naam = (String)Lezen(); 빈칸(); if (broncode.charAt(positie++) != ':') throw new IllegalArgumentException("gegevens scheidingsteken_WAARDE fout");
                    resultaat.put(Naam, Lezen()); 빈칸(); char scheidingsteken_WAARDE = broncode.charAt(positie++);
                    if (scheidingsteken_WAARDE == '}') return resultaat; if (scheidingsteken_WAARDE != ',') throw new IllegalArgumentException("gegevens scheidingsteken_WAARDE fout");
                }
            }
            if (teken_WAARDE == '[') {
                List<Object> resultaat = new ArrayList<>(); 빈칸();
                if (broncode.charAt(positie) == ']') { positie++; return resultaat; }
                while (true) {
                    resultaat.add(Lezen()); 빈칸(); char scheidingsteken_WAARDE = broncode.charAt(positie++);
                    if (scheidingsteken_WAARDE == ']') return resultaat; if (scheidingsteken_WAARDE != ',') throw new IllegalArgumentException("gegevens scheidingsteken_WAARDE fout");
                }
            }
            if (teken_WAARDE == '"') {
                StringBuilder resultaat = new StringBuilder();
                while (true) {
                    char Volgende_item = broncode.charAt(positie++); if (Volgende_item == '"') return resultaat.toString();
                    if (Volgende_item == '\\') {
                        Volgende_item = broncode.charAt(positie++);
                        if (Volgende_item == 'u') { resultaat.append((char)Integer.parseInt(broncode.substring(positie, positie + 4),16)); positie += 4; continue; }
                        if (Volgende_item == 'n') Volgende_item = '\n'; else if (Volgende_item == 'r') Volgende_item = '\r'; else if (Volgende_item == 't') Volgende_item = '\t';
                        else if (Volgende_item == 'b') Volgende_item = '\b'; else if (Volgende_item == 'f') Volgende_item = '\f';
                        else if (Volgende_item != '"' && Volgende_item != '\\' && Volgende_item != '/') throw new IllegalArgumentException("문자 이스케이프 fout");
                    }
                    resultaat.append(Volgende_item);
                }
            }
            int starten = positie - 1;
            while (positie < broncode.length() && ",]} \t\r\n".indexOf(broncode.charAt(positie)) < 0) positie++;
            String WAARDE = broncode.substring(starten, positie);
            if (WAARDE.equals("true")) return Boolean.TRUE; if (WAARDE.equals("false")) return Boolean.FALSE; if (WAARDE.equals("null")) return null;
            return Double.valueOf(WAARDE);
        }
    }
    static String hash_Bestand(Path pad) throws Exception {
        MessageDigest 계산 = MessageDigest.getInstance("SHA-256"); byte[] gegevens = new byte[1024 * 1024];
        try (InputStream invoer_WAARDE = Files.newInputStream(pad)) { for (int tijdsduur_WAARDE; (tijdsduur_WAARDE = invoer_WAARDE.read(gegevens)) >= 0;) 계산.update(gegevens,0,tijdsduur_WAARDE); }
        return hash_sms(계산.digest());
    }
    static String hash_sms(byte[] gegevens) {
        StringBuilder tekst = new StringBuilder(); for (byte WAARDE : gegevens) tekst.append(String.format(Locale.ROOT,"%02x",WAARDE & 255)); return tekst.toString();
    }
    static Path intern_pad(Path Taken_wortel, String Naam) {
        Path resultaat = Taken_wortel.resolve(Naam).normalize();
        if (Naam.isEmpty() || Paths.get(Naam).isAbsolute() || !resultaat.startsWith(Taken_wortel) || Naam.indexOf('\\') >= 0)
            throw new IllegalArgumentException("범위를 벗어난 pad: " + Naam);
        for (Path 부분 : Paths.get(Naam)) if (부분.toString().equals("..")) throw new IllegalArgumentException("상위 pad 금지: " + Naam);
        for (Path actueel_item = resultaat; actueel_item != null && actueel_item.startsWith(Taken_wortel); actueel_item = actueel_item.getParent())
            if (Files.isSymbolicLink(actueel_item)) throw new IllegalArgumentException("의존성 경로의 링크 금지: " + Naam);
        return resultaat;
    }
    static String opdracht_uitvoer(List<String> opdracht) throws Exception {
        Process Proces_WAARDE = new ProcessBuilder(opdracht).redirectError(ProcessBuilder.Redirect.INHERIT).start();
        String resultaat = new String(Proces_WAARDE.getInputStream().readAllBytes(),StandardCharsets.UTF_8);
        if (Proces_WAARDE.waitFor() != 0) throw new IOException("opdracht fout_WAARDE: " + opdracht.get(0)); return resultaat;
    }
    static void uitpakken(Path Archief_WAARDE, Path doel_WAARDE) throws Exception {
        for (String Naam : opdracht_uitvoer(Arrays.asList("tar","-tzf",Archief_WAARDE.toString())).split("\n")) intern_pad(doel_WAARDE, Naam);
        for (String invoerregel : opdracht_uitvoer(Arrays.asList("tar","-tvzf",Archief_WAARDE.toString())).split("\n"))
            if (!invoerregel.isEmpty() && invoerregel.charAt(0) != '-' && invoerregel.charAt(0) != 'd') throw new IOException("extern_WAARDE 링크 또는 특수 파일을 포함한 의존성");
        Files.createDirectories(doel_WAARDE);
        int Status_WAARDE = new ProcessBuilder("tar","--no-same-owner","--no-same-permissions","-xzf",Archief_WAARDE.toString(),"-C",doel_WAARDE.toString()).inheritIO().start().waitFor();
        if (Status_WAARDE != 0) throw new IOException("의존성 Archief_WAARDE versie_Opslag fout_WAARDE");
    }
    static void 호출(Path 작업경로, Path hulpmiddelen, List<String> argumenten, Map<String,String> omgeving) throws Exception {
        List<String> opdracht = new ArrayList<>(Arrays.asList("python3", hulpmiddelen.toString())); opdracht.addAll(argumenten);
        ProcessBuilder Uitvoeren_opdracht = new ProcessBuilder(opdracht).directory(작업경로.toFile()).inheritIO(); Uitvoeren_opdracht.environment().putAll(omgeving);
        int Status_WAARDE = Uitvoeren_opdracht.start().waitFor(); if (Status_WAARDE != 0) throw new IOException("hulpmiddelen fout_WAARDE: " + hulpmiddelen + " (" + Status_WAARDE + ")");
    }
    @SuppressWarnings("unchecked")
    public static void main(String[] argumenten) throws Exception {
        if (argumenten.length < 1) throw new IllegalArgumentException("build, run, desktop, image, check, test-system 중 동작을 지정하세요");
        String Actie = argumenten[0];
        if (!Arrays.asList("build","run","desktop","image","check","test-system").contains(Actie)) throw new IllegalArgumentException("알 nummer 없는 Actie");
        Path Taken_wortel = Paths.get(System.getProperty("worldos.edition.root")).toAbsolutePath().normalize();
        Map<String,Object> Instellingen = (Map<String,Object>)new gegevens_parser(Files.readString(Taken_wortel.resolve("native.json"),StandardCharsets.UTF_8)).Lezen();
        Path bron_structuur = intern_pad(Taken_wortel,(String)Instellingen.get("source")), kernel_WAARDE = intern_pad(bron_structuur,(String)Instellingen.get("native"));
        List<String> 소유파일들 = (List<String>)(List<?>)Instellingen.get("owned_files");
        for (String Naam : 소유파일들) if (!Files.isRegularFile(intern_pad(bron_structuur,Naam))) throw new IOException("bron_structuur 없음: " + Naam);
        if (Actie.equals("check")) { System.out.println(Instellingen.get("country") + " " + Instellingen.get("language") + " 독립 bron_structuur bevestigen 완료"); return; }
        String bron_relatief_pad = (String)Instellingen.getOrDefault("resource_root", ".");
        if (!bron_relatief_pad.equals(".") && !bron_relatief_pad.equals("..")) throw new IllegalArgumentException("의존성 Taken_wortel pad fout");
        Path bron_WAARDE = Taken_wortel.resolve(bron_relatief_pad).normalize(); Path Archief_WAARDE = bron_WAARDE.resolve("native-vendor.tar.gz");
        String 기대해시 = (String)Instellingen.get("vendor_sha256");
        if (!hash_Bestand(Archief_WAARDE).equals(기대해시)) throw new IOException("의존성 SHA-256 불일치");
        Path markering_WAARDE = bron_structuur.resolve(".vendor-sha256");
        if (!Files.isRegularFile(markering_WAARDE) || !Files.readString(markering_WAARDE).trim().equals(기대해시)) { uitpakken(Archief_WAARDE, bron_structuur); Files.writeString(markering_WAARDE,기대해시 + "\n"); }
        Map<String,String> omgeving = new HashMap<>(System.getenv());
        Path ipConfig = null;
        if (omgeving.containsKey("IP_CONFIG")) ipConfig = Paths.get(omgeving.get("IP_CONFIG")).toAbsolutePath().normalize();
        else for (Path parent = Taken_wortel; parent != null; parent = parent.getParent()) {
            if (Files.isRegularFile(parent.resolve("ip.conf"))) { ipConfig = parent.resolve("ip.conf"); break; }
        }
        if (ipConfig == null) ipConfig = bron_structuur.resolve("ip.conf");
        if (!Files.isRegularFile(ipConfig)) throw new IOException("Missing ip.conf: " + ipConfig);
        omgeving.put("IP_CONFIG", ipConfig.toString());
        if (Arrays.asList("run","desktop","test-system").contains(Actie) && !omgeving.containsKey("QEMU_AARCH64")) {
            Path app_app_lade = bron_WAARDE.resolve("host/qemu"), app_lade_markering = bron_WAARDE.resolve("host/.qemu-sha256");
            String app_lade_hash = (String)Instellingen.get("qemu_sha256");
            if (!Files.isRegularFile(app_app_lade) || !Files.isRegularFile(app_lade_markering) || !Files.readString(app_lade_markering).trim().equals(app_lade_hash)) {
                Path app_lade_Archief = bron_WAARDE.resolve("qemu-host.tar.gz"); if (!hash_Bestand(app_lade_Archief).equals(app_lade_hash)) throw new IOException("QEMU SHA-256 불일치");
                uitpakken(app_lade_Archief,bron_WAARDE.resolve("host")); Files.writeString(app_lade_markering,app_lade_hash + "\n");
            }
            omgeving.put("QEMU_AARCH64",app_app_lade.toString());
        }
        MessageDigest 계산 = MessageDigest.getInstance("SHA-256"); Collections.sort(소유파일들);
        for (String Naam : 소유파일들) { 계산.update(Naam.getBytes(StandardCharsets.UTF_8)); 계산.update(Files.readAllBytes(intern_pad(bron_structuur,Naam))); }
        계산.update("ip.conf\0".getBytes(StandardCharsets.UTF_8)); 계산.update(Files.readAllBytes(ipConfig));
        String bron_hash = hash_sms(계산.digest()); Path build_markering = kernel_WAARDE.resolve("build/worldos-source.sha256");
        if (Actie.equals("build") || !Files.isRegularFile(build_markering) || !Files.readString(build_markering).trim().equals(bron_hash)) {
            호출(kernel_WAARDE,intern_pad(kernel_WAARDE,(String)Instellingen.get("builder")),Collections.emptyList(),omgeving);
            Files.writeString(build_markering,bron_hash + "\n");
        }
        List<String> 추가인수 = new ArrayList<>(Arrays.asList(argumenten).subList(1,argumenten.length));
        if (Actie.equals("run") || Actie.equals("desktop")) {
            if (Actie.equals("desktop")) 추가인수.add(0,"--desktop");
            호출(kernel_WAARDE,intern_pad(kernel_WAARDE,(String)Instellingen.get("runner")),추가인수,omgeving);
        } else if (Actie.equals("image")) 호출(kernel_WAARDE,intern_pad(kernel_WAARDE,(String)Instellingen.get("image_builder")),추가인수,omgeving);
        else if (Actie.equals("test-system")) {
            추가인수.add(0,Taken_wortel.toString()); 추가인수.add(0,"--edition");
            호출(kernel_WAARDE,intern_pad(kernel_WAARDE,(String)Instellingen.get("system_tester")),추가인수,omgeving);
        }
    }
}
