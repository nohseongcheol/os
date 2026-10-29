// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.security.MessageDigest;
import java.util.*;

/** 독립 국가판의 의존성 검사·복원·međuverzija_sustav·실행을 맡는 domaćin Java Alati. */
public final class Country_pokretač {
    static final class podaci_analizator {
        final String IZVOR; int Položaj;
        podaci_analizator(String Tekst) { IZVOR = Tekst; }
        void 빈칸() { while (Položaj < IZVOR.length() && Character.isWhitespace(IZVOR.charAt(Položaj))) Položaj++; }
        Object Čitaj() {
            빈칸(); char znak_VALUE = IZVOR.charAt(Položaj++);
            if (znak_VALUE == '{') {
                Map<String,Object> REZULTAT = new LinkedHashMap<>(); 빈칸();
                if (IZVOR.charAt(Položaj) == '}') { Položaj++; return REZULTAT; }
                while (true) {
                    String Ime = (String)Čitaj(); 빈칸(); if (IZVOR.charAt(Položaj++) != ':') throw new IllegalArgumentException("podaci graničnik_VALUE GREŠKA");
                    REZULTAT.put(Ime, Čitaj()); 빈칸(); char graničnik_VALUE = IZVOR.charAt(Položaj++);
                    if (graničnik_VALUE == '}') return REZULTAT; if (graničnik_VALUE != ',') throw new IllegalArgumentException("podaci graničnik_VALUE GREŠKA");
                }
            }
            if (znak_VALUE == '[') {
                List<Object> REZULTAT = new ArrayList<>(); 빈칸();
                if (IZVOR.charAt(Položaj) == ']') { Položaj++; return REZULTAT; }
                while (true) {
                    REZULTAT.add(Čitaj()); 빈칸(); char graničnik_VALUE = IZVOR.charAt(Položaj++);
                    if (graničnik_VALUE == ']') return REZULTAT; if (graničnik_VALUE != ',') throw new IllegalArgumentException("podaci graničnik_VALUE GREŠKA");
                }
            }
            if (znak_VALUE == '"') {
                StringBuilder REZULTAT = new StringBuilder();
                while (true) {
                    char Dalje_artikl = IZVOR.charAt(Položaj++); if (Dalje_artikl == '"') return REZULTAT.toString();
                    if (Dalje_artikl == '\\') {
                        Dalje_artikl = IZVOR.charAt(Položaj++);
                        if (Dalje_artikl == 'u') { REZULTAT.append((char)Integer.parseInt(IZVOR.substring(Položaj, Položaj + 4),16)); Položaj += 4; continue; }
                        if (Dalje_artikl == 'n') Dalje_artikl = '\n'; else if (Dalje_artikl == 'r') Dalje_artikl = '\r'; else if (Dalje_artikl == 't') Dalje_artikl = '\t';
                        else if (Dalje_artikl == 'b') Dalje_artikl = '\b'; else if (Dalje_artikl == 'f') Dalje_artikl = '\f';
                        else if (Dalje_artikl != '"' && Dalje_artikl != '\\' && Dalje_artikl != '/') throw new IllegalArgumentException("문자 이스케이프 GREŠKA");
                    }
                    REZULTAT.append(Dalje_artikl);
                }
            }
            int Pokreni = Položaj - 1;
            while (Položaj < IZVOR.length() && ",]} \t\r\n".indexOf(IZVOR.charAt(Položaj)) < 0) Položaj++;
            String VALUE = IZVOR.substring(Pokreni, Položaj);
            if (VALUE.equals("true")) return Boolean.TRUE; if (VALUE.equals("false")) return Boolean.FALSE; if (VALUE.equals("null")) return null;
            return Double.valueOf(VALUE);
        }
    }
    static String raspršivanje_Datoteka(Path PUTANJA) throws Exception {
        MessageDigest 계산 = MessageDigest.getInstance("SHA-256"); byte[] podaci = new byte[1024 * 1024];
        try (InputStream 입력 = Files.newInputStream(PUTANJA)) { for (int 길이; (길이 = 입력.read(podaci)) >= 0;) 계산.update(podaci,0,길이); }
        return raspršivanje_SMS(계산.digest());
    }
    static String raspršivanje_SMS(byte[] podaci) {
        StringBuilder Tekst = new StringBuilder(); for (byte VALUE : podaci) Tekst.append(String.format(Locale.ROOT,"%02x",VALUE & 255)); return Tekst.toString();
    }
    static Path interni_put(Path akcija_korijen, String Ime) {
        Path REZULTAT = akcija_korijen.resolve(Ime).normalize();
        if (Ime.isEmpty() || Paths.get(Ime).isAbsolute() || !REZULTAT.startsWith(akcija_korijen) || Ime.indexOf('\\') >= 0)
            throw new IllegalArgumentException("범위를 벗어난 PUTANJA: " + Ime);
        for (Path 부분 : Paths.get(Ime)) if (부분.toString().equals("..")) throw new IllegalArgumentException("상위 PUTANJA 금지: " + Ime);
        for (Path redovno_artikl = REZULTAT; redovno_artikl != null && redovno_artikl.startsWith(akcija_korijen); redovno_artikl = redovno_artikl.getParent())
            if (Files.isSymbolicLink(redovno_artikl)) throw new IllegalArgumentException("의존성 경로의 링크 금지: " + Ime);
        return REZULTAT;
    }
    static String 명령출력(List<String> Naredba) throws Exception {
        Process Proces_VALUE = new ProcessBuilder(Naredba).redirectError(ProcessBuilder.Redirect.INHERIT).start();
        String REZULTAT = new String(Proces_VALUE.getInputStream().readAllBytes(),StandardCharsets.UTF_8);
        if (Proces_VALUE.waitFor() != 0) throw new IOException("Naredba kvar_VALUE: " + Naredba.get(0)); return REZULTAT;
    }
    static void izdvojiti(Path Arhiva_VALUE, Path odredište_VALUE) throws Exception {
        for (String Ime : 명령출력(Arrays.asList("tar","-tzf",Arhiva_VALUE.toString())).split("\n")) interni_put(odredište_VALUE, Ime);
        for (String red : 명령출력(Arrays.asList("tar","-tvzf",Arhiva_VALUE.toString())).split("\n"))
            if (!red.isEmpty() && red.charAt(0) != '-' && red.charAt(0) != 'd') throw new IOException("vanjski_VALUE 링크 또는 특수 파일을 포함한 의존성");
        Files.createDirectories(odredište_VALUE);
        int Stanje_VALUE = new ProcessBuilder("tar","--no-same-owner","--no-same-permissions","-xzf",Arhiva_VALUE.toString(),"-C",odredište_VALUE.toString()).inheritIO().start().waitFor();
        if (Stanje_VALUE != 0) throw new IOException("의존성 Arhiva_VALUE izdati_Pohrana kvar_VALUE");
    }
    static void 호출(Path 작업경로, Path Alati, List<String> Argumenti, Map<String,String> okruženje) throws Exception {
        List<String> Naredba = new ArrayList<>(Arrays.asList("python3", Alati.toString())); Naredba.addAll(Argumenti);
        ProcessBuilder Izvrši_naredba = new ProcessBuilder(Naredba).directory(작업경로.toFile()).inheritIO(); Izvrši_naredba.environment().putAll(okruženje);
        int Stanje_VALUE = Izvrši_naredba.start().waitFor(); if (Stanje_VALUE != 0) throw new IOException("Alati kvar_VALUE: " + Alati + " (" + Stanje_VALUE + ")");
    }
    @SuppressWarnings("unchecked")
    public static void main(String[] Argumenti) throws Exception {
        if (Argumenti.length < 1) throw new IllegalArgumentException("build, run, desktop, image, check, test-system 중 동작을 지정하세요");
        String Aktivnost = Argumenti[0];
        if (!Arrays.asList("build","run","desktop","image","check","test-system").contains(Aktivnost)) throw new IllegalArgumentException("알 수 없는 Aktivnost");
        Path akcija_korijen = Paths.get(System.getProperty("worldos.edition.root")).toAbsolutePath().normalize();
        Map<String,Object> Postavke = (Map<String,Object>)new podaci_analizator(Files.readString(akcija_korijen.resolve("native.json"),StandardCharsets.UTF_8)).Čitaj();
        Path izvor_stablo = interni_put(akcija_korijen,(String)Postavke.get("source")), jezgra_sustava_VALUE = interni_put(izvor_stablo,(String)Postavke.get("native"));
        List<String> 소유파일들 = (List<String>)(List<?>)Postavke.get("owned_files");
        for (String Ime : 소유파일들) if (!Files.isRegularFile(interni_put(izvor_stablo,Ime))) throw new IOException("izvor_stablo 없음: " + Ime);
        if (Aktivnost.equals("check")) { System.out.println(Postavke.get("country") + " " + Postavke.get("language") + " 독립 izvor_stablo provjeriti 완료"); return; }
        String resurs_relativni_put = (String)Postavke.getOrDefault("resource_root", ".");
        if (!resurs_relativni_put.equals(".") && !resurs_relativni_put.equals("..")) throw new IllegalArgumentException("의존성 akcija_korijen PUTANJA GREŠKA");
        Path resurs_VALUE = akcija_korijen.resolve(resurs_relativni_put).normalize(); Path Arhiva_VALUE = resurs_VALUE.resolve("native-vendor.tar.gz");
        String 기대해시 = (String)Postavke.get("vendor_sha256");
        if (!raspršivanje_Datoteka(Arhiva_VALUE).equals(기대해시)) throw new IOException("의존성 SHA-256 불일치");
        Path marker_VALUE = izvor_stablo.resolve(".vendor-sha256");
        if (!Files.isRegularFile(marker_VALUE) || !Files.readString(marker_VALUE).trim().equals(기대해시)) { izdvojiti(Arhiva_VALUE, izvor_stablo); Files.writeString(marker_VALUE,기대해시 + "\n"); }
        Map<String,String> okruženje = new HashMap<>(System.getenv());
        Path ipConfig = null;
        if (okruženje.containsKey("IP_CONFIG")) ipConfig = Paths.get(okruženje.get("IP_CONFIG")).toAbsolutePath().normalize();
        else for (Path parent = akcija_korijen; parent != null; parent = parent.getParent()) {
            if (Files.isRegularFile(parent.resolve("ip.conf"))) { ipConfig = parent.resolve("ip.conf"); break; }
        }
        if (ipConfig == null) ipConfig = izvor_stablo.resolve("ip.conf");
        if (!Files.isRegularFile(ipConfig)) throw new IOException("Missing ip.conf: " + ipConfig);
        okruženje.put("IP_CONFIG", ipConfig.toString());
        if (Arrays.asList("run","desktop","test-system").contains(Aktivnost) && !okruženje.containsKey("QEMU_AARCH64")) {
            Path program_pokretač = resurs_VALUE.resolve("host/qemu"), pokretač_marker = resurs_VALUE.resolve("host/.qemu-sha256");
            String pokretač_raspršivanje = (String)Postavke.get("qemu_sha256");
            if (!Files.isRegularFile(program_pokretač) || !Files.isRegularFile(pokretač_marker) || !Files.readString(pokretač_marker).trim().equals(pokretač_raspršivanje)) {
                Path pokretač_Arhiva = resurs_VALUE.resolve("qemu-host.tar.gz"); if (!raspršivanje_Datoteka(pokretač_Arhiva).equals(pokretač_raspršivanje)) throw new IOException("QEMU SHA-256 불일치");
                izdvojiti(pokretač_Arhiva,resurs_VALUE.resolve("host")); Files.writeString(pokretač_marker,pokretač_raspršivanje + "\n");
            }
            okruženje.put("QEMU_AARCH64",program_pokretač.toString());
        }
        MessageDigest 계산 = MessageDigest.getInstance("SHA-256"); Collections.sort(소유파일들);
        for (String Ime : 소유파일들) { 계산.update(Ime.getBytes(StandardCharsets.UTF_8)); 계산.update(Files.readAllBytes(interni_put(izvor_stablo,Ime))); }
        계산.update("ip.conf\0".getBytes(StandardCharsets.UTF_8)); 계산.update(Files.readAllBytes(ipConfig));
        String izvor_raspršivanje = raspršivanje_SMS(계산.digest()); Path međuverzija_marker = jezgra_sustava_VALUE.resolve("build/worldos-source.sha256");
        if (Aktivnost.equals("build") || !Files.isRegularFile(međuverzija_marker) || !Files.readString(međuverzija_marker).trim().equals(izvor_raspršivanje)) {
            호출(jezgra_sustava_VALUE,interni_put(jezgra_sustava_VALUE,(String)Postavke.get("builder")),Collections.emptyList(),okruženje);
            Files.writeString(međuverzija_marker,izvor_raspršivanje + "\n");
        }
        List<String> 추가인수 = new ArrayList<>(Arrays.asList(Argumenti).subList(1,Argumenti.length));
        if (Aktivnost.equals("run") || Aktivnost.equals("desktop")) {
            if (Aktivnost.equals("desktop")) 추가인수.add(0,"--desktop");
            호출(jezgra_sustava_VALUE,interni_put(jezgra_sustava_VALUE,(String)Postavke.get("runner")),추가인수,okruženje);
        } else if (Aktivnost.equals("image")) 호출(jezgra_sustava_VALUE,interni_put(jezgra_sustava_VALUE,(String)Postavke.get("image_builder")),추가인수,okruženje);
        else if (Aktivnost.equals("test-system")) {
            추가인수.add(0,akcija_korijen.toString()); 추가인수.add(0,"--edition");
            호출(jezgra_sustava_VALUE,interni_put(jezgra_sustava_VALUE,(String)Postavke.get("system_tester")),추가인수,okruženje);
        }
    }
}
