// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.security.MessageDigest;
import java.util.*;

/** 독립 국가판의 의존성 검사·복원·verzija_sistem·실행을 맡는 organizator Java Alati. */
public final class 국가실행기 {
    static final class 자료해석기 {
        final String IZVOR; int Pozicija;
        자료해석기(String Tekst) { IZVOR = Tekst; }
        void 빈칸() { while (Pozicija < IZVOR.length() && Character.isWhitespace(IZVOR.charAt(Pozicija))) Pozicija++; }
        Object Čitaj() {
            빈칸(); char znak_VALUE = IZVOR.charAt(Pozicija++);
            if (znak_VALUE == '{') {
                Map<String,Object> mjera = new LinkedHashMap<>(); 빈칸();
                if (IZVOR.charAt(Pozicija) == '}') { Pozicija++; return mjera; }
                while (true) {
                    String Naziv = (String)Čitaj(); 빈칸(); if (IZVOR.charAt(Pozicija++) != ':') throw new IllegalArgumentException("podaci graničnik_VALUE GRESKA");
                    mjera.put(Naziv, Čitaj()); 빈칸(); char graničnik_VALUE = IZVOR.charAt(Pozicija++);
                    if (graničnik_VALUE == '}') return mjera; if (graničnik_VALUE != ',') throw new IllegalArgumentException("podaci graničnik_VALUE GRESKA");
                }
            }
            if (znak_VALUE == '[') {
                List<Object> mjera = new ArrayList<>(); 빈칸();
                if (IZVOR.charAt(Pozicija) == ']') { Pozicija++; return mjera; }
                while (true) {
                    mjera.add(Čitaj()); 빈칸(); char graničnik_VALUE = IZVOR.charAt(Pozicija++);
                    if (graničnik_VALUE == ']') return mjera; if (graničnik_VALUE != ',') throw new IllegalArgumentException("podaci graničnik_VALUE GRESKA");
                }
            }
            if (znak_VALUE == '"') {
                StringBuilder mjera = new StringBuilder();
                while (true) {
                    char Dalje_stavka = IZVOR.charAt(Pozicija++); if (Dalje_stavka == '"') return mjera.toString();
                    if (Dalje_stavka == '\\') {
                        Dalje_stavka = IZVOR.charAt(Pozicija++);
                        if (Dalje_stavka == 'u') { mjera.append((char)Integer.parseInt(IZVOR.substring(Pozicija, Pozicija + 4),16)); Pozicija += 4; continue; }
                        if (Dalje_stavka == 'n') Dalje_stavka = '\n'; else if (Dalje_stavka == 'r') Dalje_stavka = '\r'; else if (Dalje_stavka == 't') Dalje_stavka = '\t';
                        else if (Dalje_stavka == 'b') Dalje_stavka = '\b'; else if (Dalje_stavka == 'f') Dalje_stavka = '\f';
                        else if (Dalje_stavka != '"' && Dalje_stavka != '\\' && Dalje_stavka != '/') throw new IllegalArgumentException("문자 이스케이프 GRESKA");
                    }
                    mjera.append(Dalje_stavka);
                }
            }
            int Pokreni = Pozicija - 1;
            while (Pozicija < IZVOR.length() && ",]} \t\r\n".indexOf(IZVOR.charAt(Pozicija)) < 0) Pozicija++;
            String VALUE = IZVOR.substring(Pokreni, Pozicija);
            if (VALUE.equals("true")) return Boolean.TRUE; if (VALUE.equals("false")) return Boolean.FALSE; if (VALUE.equals("null")) return null;
            return Double.valueOf(VALUE);
        }
    }
    static String raspršivanje_fajl(Path Putanja) throws Exception {
        MessageDigest 계산 = MessageDigest.getInstance("SHA-256"); byte[] podaci = new byte[1024 * 1024];
        try (InputStream 입력 = Files.newInputStream(Putanja)) { for (int dužina_VALUE; (dužina_VALUE = 입력.read(podaci)) >= 0;) 계산.update(podaci,0,dužina_VALUE); }
        return raspršivanje_SMS(계산.digest());
    }
    static String raspršivanje_SMS(byte[] podaci) {
        StringBuilder Tekst = new StringBuilder(); for (byte VALUE : podaci) Tekst.append(String.format(Locale.ROOT,"%02x",VALUE & 255)); return Tekst.toString();
    }
    static Path 내부경로(Path projicirati_koijen, String Naziv) {
        Path mjera = projicirati_koijen.resolve(Naziv).normalize();
        if (Naziv.isEmpty() || Paths.get(Naziv).isAbsolute() || !mjera.startsWith(projicirati_koijen) || Naziv.indexOf('\\') >= 0)
            throw new IllegalArgumentException("범위를 벗어난 Putanja: " + Naziv);
        for (Path 부분 : Paths.get(Naziv)) if (부분.toString().equals("..")) throw new IllegalArgumentException("상위 Putanja 금지: " + Naziv);
        for (Path trenutno_stavka = mjera; trenutno_stavka != null && trenutno_stavka.startsWith(projicirati_koijen); trenutno_stavka = trenutno_stavka.getParent())
            if (Files.isSymbolicLink(trenutno_stavka)) throw new IllegalArgumentException("의존성 경로의 링크 금지: " + Naziv);
        return mjera;
    }
    static String 명령출력(List<String> Naredba) throws Exception {
        Process proces_VALUE = new ProcessBuilder(Naredba).redirectError(ProcessBuilder.Redirect.INHERIT).start();
        String mjera = new String(proces_VALUE.getInputStream().readAllBytes(),StandardCharsets.UTF_8);
        if (proces_VALUE.waitFor() != 0) throw new IOException("Naredba neuspjeh_VALUE: " + Naredba.get(0)); return mjera;
    }
    static void izdvojiti(Path Arhiva_VALUE, Path odredište_VALUE) throws Exception {
        for (String Naziv : 명령출력(Arrays.asList("tar","-tzf",Arhiva_VALUE.toString())).split("\n")) 내부경로(odredište_VALUE, Naziv);
        for (String Linija : 명령출력(Arrays.asList("tar","-tvzf",Arhiva_VALUE.toString())).split("\n"))
            if (!Linija.isEmpty() && Linija.charAt(0) != '-' && Linija.charAt(0) != 'd') throw new IOException("iz_eksternog_izvora_VALUE 링크 또는 특수 파일을 포함한 의존성");
        Files.createDirectories(odredište_VALUE);
        int stanje_VALUE = new ProcessBuilder("tar","--no-same-owner","--no-same-permissions","-xzf",Arhiva_VALUE.toString(),"-C",odredište_VALUE.toString()).inheritIO().start().waitFor();
        if (stanje_VALUE != 0) throw new IOException("의존성 Arhiva_VALUE izdanje_Pohrana neuspjeh_VALUE");
    }
    static void 호출(Path 작업경로, Path Alati, List<String> Argumenti, Map<String,String> operativno_okruženje) throws Exception {
        List<String> Naredba = new ArrayList<>(Arrays.asList("python3", Alati.toString())); Naredba.addAll(Argumenti);
        ProcessBuilder Izvrši_komanda = new ProcessBuilder(Naredba).directory(작업경로.toFile()).inheritIO(); Izvrši_komanda.environment().putAll(operativno_okruženje);
        int stanje_VALUE = Izvrši_komanda.start().waitFor(); if (stanje_VALUE != 0) throw new IOException("Alati neuspjeh_VALUE: " + Alati + " (" + stanje_VALUE + ")");
    }
    @SuppressWarnings("unchecked")
    public static void main(String[] Argumenti) throws Exception {
        if (Argumenti.length < 1) throw new IllegalArgumentException("build, run, desktop, image, check, test-system 중 동작을 지정하세요");
        String radnja = Argumenti[0];
        if (!Arrays.asList("build","run","desktop","image","check","test-system").contains(radnja)) throw new IllegalArgumentException("알 수 없는 radnja");
        Path projicirati_koijen = Paths.get(System.getProperty("worldos.edition.root")).toAbsolutePath().normalize();
        Map<String,Object> Postavke = (Map<String,Object>)new 자료해석기(Files.readString(projicirati_koijen.resolve("native.json"),StandardCharsets.UTF_8)).Čitaj();
        Path izvor_stablo = 내부경로(projicirati_koijen,(String)Postavke.get("source")), jezgro_VALUE = 내부경로(izvor_stablo,(String)Postavke.get("native"));
        List<String> 소유파일들 = (List<String>)(List<?>)Postavke.get("owned_files");
        for (String Naziv : 소유파일들) if (!Files.isRegularFile(내부경로(izvor_stablo,Naziv))) throw new IOException("izvor_stablo 없음: " + Naziv);
        if (radnja.equals("check")) { System.out.println(Postavke.get("country") + " " + Postavke.get("language") + " 독립 izvor_stablo potvrditi 완료"); return; }
        String 자원상대 = (String)Postavke.getOrDefault("resource_root", ".");
        if (!자원상대.equals(".") && !자원상대.equals("..")) throw new IllegalArgumentException("의존성 projicirati_koijen Putanja GRESKA");
        Path resurs_VALUE = projicirati_koijen.resolve(자원상대).normalize(); Path Arhiva_VALUE = resurs_VALUE.resolve("native-vendor.tar.gz");
        String 기대해시 = (String)Postavke.get("vendor_sha256");
        if (!raspršivanje_fajl(Arhiva_VALUE).equals(기대해시)) throw new IOException("의존성 SHA-256 불일치");
        Path 표식 = izvor_stablo.resolve(".vendor-sha256");
        if (!Files.isRegularFile(표식) || !Files.readString(표식).trim().equals(기대해시)) { izdvojiti(Arhiva_VALUE, izvor_stablo); Files.writeString(표식,기대해시 + "\n"); }
        Map<String,String> operativno_okruženje = new HashMap<>(System.getenv());
        Path ipConfig = null;
        if (operativno_okruženje.containsKey("IP_CONFIG")) ipConfig = Paths.get(operativno_okruženje.get("IP_CONFIG")).toAbsolutePath().normalize();
        else for (Path parent = projicirati_koijen; parent != null; parent = parent.getParent()) {
            if (Files.isRegularFile(parent.resolve("ip.conf"))) { ipConfig = parent.resolve("ip.conf"); break; }
        }
        if (ipConfig == null) ipConfig = izvor_stablo.resolve("ip.conf");
        if (!Files.isRegularFile(ipConfig)) throw new IOException("Missing ip.conf: " + ipConfig);
        operativno_okruženje.put("IP_CONFIG", ipConfig.toString());
        if (Arrays.asList("run","desktop","test-system").contains(radnja) && !operativno_okruženje.containsKey("QEMU_AARCH64")) {
            Path program_pokretač = resurs_VALUE.resolve("host/qemu"), 실행기표식 = resurs_VALUE.resolve("host/.qemu-sha256");
            String pokretač_raspršivanje = (String)Postavke.get("qemu_sha256");
            if (!Files.isRegularFile(program_pokretač) || !Files.isRegularFile(실행기표식) || !Files.readString(실행기표식).trim().equals(pokretač_raspršivanje)) {
                Path pokretač_Arhiva = resurs_VALUE.resolve("qemu-host.tar.gz"); if (!raspršivanje_fajl(pokretač_Arhiva).equals(pokretač_raspršivanje)) throw new IOException("QEMU SHA-256 불일치");
                izdvojiti(pokretač_Arhiva,resurs_VALUE.resolve("host")); Files.writeString(실행기표식,pokretač_raspršivanje + "\n");
            }
            operativno_okruženje.put("QEMU_AARCH64",program_pokretač.toString());
        }
        MessageDigest 계산 = MessageDigest.getInstance("SHA-256"); Collections.sort(소유파일들);
        for (String Naziv : 소유파일들) { 계산.update(Naziv.getBytes(StandardCharsets.UTF_8)); 계산.update(Files.readAllBytes(내부경로(izvor_stablo,Naziv))); }
        계산.update("ip.conf\0".getBytes(StandardCharsets.UTF_8)); 계산.update(Files.readAllBytes(ipConfig));
        String izvor_raspršivanje = raspršivanje_SMS(계산.digest()); Path 빌드표식 = jezgro_VALUE.resolve("build/worldos-source.sha256");
        if (radnja.equals("build") || !Files.isRegularFile(빌드표식) || !Files.readString(빌드표식).trim().equals(izvor_raspršivanje)) {
            호출(jezgro_VALUE,내부경로(jezgro_VALUE,(String)Postavke.get("builder")),Collections.emptyList(),operativno_okruženje);
            Files.writeString(빌드표식,izvor_raspršivanje + "\n");
        }
        List<String> 추가인수 = new ArrayList<>(Arrays.asList(Argumenti).subList(1,Argumenti.length));
        if (radnja.equals("run") || radnja.equals("desktop")) {
            if (radnja.equals("desktop")) 추가인수.add(0,"--desktop");
            호출(jezgro_VALUE,내부경로(jezgro_VALUE,(String)Postavke.get("runner")),추가인수,operativno_okruženje);
        } else if (radnja.equals("image")) 호출(jezgro_VALUE,내부경로(jezgro_VALUE,(String)Postavke.get("image_builder")),추가인수,operativno_okruženje);
        else if (radnja.equals("test-system")) {
            추가인수.add(0,projicirati_koijen.toString()); 추가인수.add(0,"--edition");
            호출(jezgro_VALUE,내부경로(jezgro_VALUE,(String)Postavke.get("system_tester")),추가인수,operativno_okruženje);
        }
    }
}
