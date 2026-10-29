// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.security.MessageDigest;
import java.util.*;

/** 독립 국가판의 의존성 검사·복원·verzija_sistem·실행을 맡는 host Java Alatke. */
public final class Kantri_pokretač {
    static final class podaci_analizator {
        final String izvor; int pozicija;
        podaci_analizator(String SMS) { izvor = SMS; }
        void 빈칸() { while (pozicija < izvor.length() && Character.isWhitespace(izvor.charAt(pozicija))) pozicija++; }
        Object 읽기() {
            빈칸(); char znak_VALUE = izvor.charAt(pozicija++);
            if (znak_VALUE == '{') {
                Map<String,Object> KR = new LinkedHashMap<>(); 빈칸();
                if (izvor.charAt(pozicija) == '}') { pozicija++; return KR; }
                while (true) {
                    String ime = (String)읽기(); 빈칸(); if (izvor.charAt(pozicija++) != ':') throw new IllegalArgumentException("podaci znak_za_razgraničavanje_VALUE greška");
                    KR.put(ime, 읽기()); 빈칸(); char znak_za_razgraničavanje_VALUE = izvor.charAt(pozicija++);
                    if (znak_za_razgraničavanje_VALUE == '}') return KR; if (znak_za_razgraničavanje_VALUE != ',') throw new IllegalArgumentException("podaci znak_za_razgraničavanje_VALUE greška");
                }
            }
            if (znak_VALUE == '[') {
                List<Object> KR = new ArrayList<>(); 빈칸();
                if (izvor.charAt(pozicija) == ']') { pozicija++; return KR; }
                while (true) {
                    KR.add(읽기()); 빈칸(); char znak_za_razgraničavanje_VALUE = izvor.charAt(pozicija++);
                    if (znak_za_razgraničavanje_VALUE == ']') return KR; if (znak_za_razgraničavanje_VALUE != ',') throw new IllegalArgumentException("podaci znak_za_razgraničavanje_VALUE greška");
                }
            }
            if (znak_VALUE == '"') {
                StringBuilder KR = new StringBuilder();
                while (true) {
                    char Dalje_stavka = izvor.charAt(pozicija++); if (Dalje_stavka == '"') return KR.toString();
                    if (Dalje_stavka == '\\') {
                        Dalje_stavka = izvor.charAt(pozicija++);
                        if (Dalje_stavka == 'u') { KR.append((char)Integer.parseInt(izvor.substring(pozicija, pozicija + 4),16)); pozicija += 4; continue; }
                        if (Dalje_stavka == 'n') Dalje_stavka = '\n'; else if (Dalje_stavka == 'r') Dalje_stavka = '\r'; else if (Dalje_stavka == 't') Dalje_stavka = '\t';
                        else if (Dalje_stavka == 'b') Dalje_stavka = '\b'; else if (Dalje_stavka == 'f') Dalje_stavka = '\f';
                        else if (Dalje_stavka != '"' && Dalje_stavka != '\\' && Dalje_stavka != '/') throw new IllegalArgumentException("문자 이스케이프 greška");
                    }
                    KR.append(Dalje_stavka);
                }
            }
            int koristiti = pozicija - 1;
            while (pozicija < izvor.length() && ",]} \t\r\n".indexOf(izvor.charAt(pozicija)) < 0) pozicija++;
            String VALUE = izvor.substring(koristiti, pozicija);
            if (VALUE.equals("true")) return Boolean.TRUE; if (VALUE.equals("false")) return Boolean.FALSE; if (VALUE.equals("null")) return null;
            return Double.valueOf(VALUE);
        }
    }
    static String heš_Datoteka(Path putanja) throws Exception {
        MessageDigest 계산 = MessageDigest.getInstance("SHA-256"); byte[] podaci = new byte[1024 * 1024];
        try (InputStream 입력 = Files.newInputStream(putanja)) { for (int 길이; (길이 = 입력.read(podaci)) >= 0;) 계산.update(podaci,0,길이); }
        return heš_SMS(계산.digest());
    }
    static String heš_SMS(byte[] podaci) {
        StringBuilder SMS = new StringBuilder(); for (byte VALUE : podaci) SMS.append(String.format(Locale.ROOT,"%02x",VALUE & 255)); return SMS.toString();
    }
    static Path unutrašnji_putanja(Path radnja_koren, String ime) {
        Path KR = radnja_koren.resolve(ime).normalize();
        if (ime.isEmpty() || Paths.get(ime).isAbsolute() || !KR.startsWith(radnja_koren) || ime.indexOf('\\') >= 0)
            throw new IllegalArgumentException("범위를 벗어난 putanja: " + ime);
        for (Path 부분 : Paths.get(ime)) if (부분.toString().equals("..")) throw new IllegalArgumentException("상위 putanja 금지: " + ime);
        for (Path aktuelno_stavka = KR; aktuelno_stavka != null && aktuelno_stavka.startsWith(radnja_koren); aktuelno_stavka = aktuelno_stavka.getParent())
            if (Files.isSymbolicLink(aktuelno_stavka)) throw new IllegalArgumentException("의존성 경로의 링크 금지: " + ime);
        return KR;
    }
    static String 명령출력(List<String> komanda) throws Exception {
        Process Proces_VALUE = new ProcessBuilder(komanda).redirectError(ProcessBuilder.Redirect.INHERIT).start();
        String KR = new String(Proces_VALUE.getInputStream().readAllBytes(),StandardCharsets.UTF_8);
        if (Proces_VALUE.waitFor() != 0) throw new IOException("komanda otkazivanje_VALUE: " + komanda.get(0)); return KR;
    }
    static void izdvojiti(Path Arhiva_VALUE, Path odredište_VALUE) throws Exception {
        for (String ime : 명령출력(Arrays.asList("tar","-tzf",Arhiva_VALUE.toString())).split("\n")) unutrašnji_putanja(odredište_VALUE, ime);
        for (String red : 명령출력(Arrays.asList("tar","-tvzf",Arhiva_VALUE.toString())).split("\n"))
            if (!red.isEmpty() && red.charAt(0) != '-' && red.charAt(0) != 'd') throw new IOException("spoljni_VALUE 링크 또는 특수 파일을 포함한 의존성");
        Files.createDirectories(odredište_VALUE);
        int Status_VALUE = new ProcessBuilder("tar","--no-same-owner","--no-same-permissions","-xzf",Arhiva_VALUE.toString(),"-C",odredište_VALUE.toString()).inheritIO().start().waitFor();
        if (Status_VALUE != 0) throw new IOException("의존성 Arhiva_VALUE izdanje_Skladište otkazivanje_VALUE");
    }
    static void 호출(Path 작업경로, Path Alatke, List<String> 인수, Map<String,String> 환경) throws Exception {
        List<String> komanda = new ArrayList<>(Arrays.asList("python3", Alatke.toString())); komanda.addAll(인수);
        ProcessBuilder Izvrši_komanda = new ProcessBuilder(komanda).directory(작업경로.toFile()).inheritIO(); Izvrši_komanda.environment().putAll(환경);
        int Status_VALUE = Izvrši_komanda.start().waitFor(); if (Status_VALUE != 0) throw new IOException("Alatke otkazivanje_VALUE: " + Alatke + " (" + Status_VALUE + ")");
    }
    @SuppressWarnings("unchecked")
    public static void main(String[] 인수) throws Exception {
        if (인수.length < 1) throw new IllegalArgumentException("build, run, desktop, image, check, test-system 중 동작을 지정하세요");
        String radnja = 인수[0];
        if (!Arrays.asList("build","run","desktop","image","check","test-system").contains(radnja)) throw new IllegalArgumentException("알 수 없는 radnja");
        Path radnja_koren = Paths.get(System.getProperty("worldos.edition.root")).toAbsolutePath().normalize();
        Map<String,Object> Postavke = (Map<String,Object>)new podaci_analizator(Files.readString(radnja_koren.resolve("native.json"),StandardCharsets.UTF_8)).읽기();
        Path izvor_stablo = unutrašnji_putanja(radnja_koren,(String)Postavke.get("source")), jezgro_VALUE = unutrašnji_putanja(izvor_stablo,(String)Postavke.get("native"));
        List<String> 소유파일들 = (List<String>)(List<?>)Postavke.get("owned_files");
        for (String ime : 소유파일들) if (!Files.isRegularFile(unutrašnji_putanja(izvor_stablo,ime))) throw new IOException("izvor_stablo 없음: " + ime);
        if (radnja.equals("check")) { System.out.println(Postavke.get("country") + " " + Postavke.get("language") + " 독립 izvor_stablo verifikovati 완료"); return; }
        String resurs_relativna_putanja = (String)Postavke.getOrDefault("resource_root", ".");
        if (!resurs_relativna_putanja.equals(".") && !resurs_relativna_putanja.equals("..")) throw new IllegalArgumentException("의존성 radnja_koren putanja greška");
        Path resurs_VALUE = radnja_koren.resolve(resurs_relativna_putanja).normalize(); Path Arhiva_VALUE = resurs_VALUE.resolve("native-vendor.tar.gz");
        String 기대해시 = (String)Postavke.get("vendor_sha256");
        if (!heš_Datoteka(Arhiva_VALUE).equals(기대해시)) throw new IOException("의존성 SHA-256 불일치");
        Path označivač_VALUE = izvor_stablo.resolve(".vendor-sha256");
        if (!Files.isRegularFile(označivač_VALUE) || !Files.readString(označivač_VALUE).trim().equals(기대해시)) { izdvojiti(Arhiva_VALUE, izvor_stablo); Files.writeString(označivač_VALUE,기대해시 + "\n"); }
        Map<String,String> 환경 = new HashMap<>(System.getenv());
        Path ipConfig = null;
        if (환경.containsKey("IP_CONFIG")) ipConfig = Paths.get(환경.get("IP_CONFIG")).toAbsolutePath().normalize();
        else for (Path parent = radnja_koren; parent != null; parent = parent.getParent()) {
            if (Files.isRegularFile(parent.resolve("ip.conf"))) { ipConfig = parent.resolve("ip.conf"); break; }
        }
        if (ipConfig == null) ipConfig = izvor_stablo.resolve("ip.conf");
        if (!Files.isRegularFile(ipConfig)) throw new IOException("Missing ip.conf: " + ipConfig);
        환경.put("IP_CONFIG", ipConfig.toString());
        if (Arrays.asList("run","desktop","test-system").contains(radnja) && !환경.containsKey("QEMU_AARCH64")) {
            Path program_pokretač = resurs_VALUE.resolve("host/qemu"), pokretač_označivač = resurs_VALUE.resolve("host/.qemu-sha256");
            String pokretač_heš = (String)Postavke.get("qemu_sha256");
            if (!Files.isRegularFile(program_pokretač) || !Files.isRegularFile(pokretač_označivač) || !Files.readString(pokretač_označivač).trim().equals(pokretač_heš)) {
                Path pokretač_Arhiva = resurs_VALUE.resolve("qemu-host.tar.gz"); if (!heš_Datoteka(pokretač_Arhiva).equals(pokretač_heš)) throw new IOException("QEMU SHA-256 불일치");
                izdvojiti(pokretač_Arhiva,resurs_VALUE.resolve("host")); Files.writeString(pokretač_označivač,pokretač_heš + "\n");
            }
            환경.put("QEMU_AARCH64",program_pokretač.toString());
        }
        MessageDigest 계산 = MessageDigest.getInstance("SHA-256"); Collections.sort(소유파일들);
        for (String ime : 소유파일들) { 계산.update(ime.getBytes(StandardCharsets.UTF_8)); 계산.update(Files.readAllBytes(unutrašnji_putanja(izvor_stablo,ime))); }
        계산.update("ip.conf\0".getBytes(StandardCharsets.UTF_8)); 계산.update(Files.readAllBytes(ipConfig));
        String izvor_heš = heš_SMS(계산.digest()); Path verzija_označivač = jezgro_VALUE.resolve("build/worldos-source.sha256");
        if (radnja.equals("build") || !Files.isRegularFile(verzija_označivač) || !Files.readString(verzija_označivač).trim().equals(izvor_heš)) {
            호출(jezgro_VALUE,unutrašnji_putanja(jezgro_VALUE,(String)Postavke.get("builder")),Collections.emptyList(),환경);
            Files.writeString(verzija_označivač,izvor_heš + "\n");
        }
        List<String> 추가인수 = new ArrayList<>(Arrays.asList(인수).subList(1,인수.length));
        if (radnja.equals("run") || radnja.equals("desktop")) {
            if (radnja.equals("desktop")) 추가인수.add(0,"--desktop");
            호출(jezgro_VALUE,unutrašnji_putanja(jezgro_VALUE,(String)Postavke.get("runner")),추가인수,환경);
        } else if (radnja.equals("image")) 호출(jezgro_VALUE,unutrašnji_putanja(jezgro_VALUE,(String)Postavke.get("image_builder")),추가인수,환경);
        else if (radnja.equals("test-system")) {
            추가인수.add(0,radnja_koren.toString()); 추가인수.add(0,"--edition");
            호출(jezgro_VALUE,unutrašnji_putanja(jezgro_VALUE,(String)Postavke.get("system_tester")),추가인수,환경);
        }
    }
}
