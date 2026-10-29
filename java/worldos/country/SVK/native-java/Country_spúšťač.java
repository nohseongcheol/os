// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.security.MessageDigest;
import java.util.*;

/** 독립 국가판의 의존성 검사·복원·zostava_systém·실행을 맡는 hostiteľ Java Nástroje. */
public final class Country_spúšťač {
    static final class údaje_analyzátor {
        final String ZDROJ; int Pozícia;
        údaje_analyzátor(String Spracovanie_textu) { ZDROJ = Spracovanie_textu; }
        void 빈칸() { while (Pozícia < ZDROJ.length() && Character.isWhitespace(ZDROJ.charAt(Pozícia))) Pozícia++; }
        Object Čítanie() {
            빈칸(); char znak_VALUE = ZDROJ.charAt(Pozícia++);
            if (znak_VALUE == '{') {
                Map<String,Object> KR = new LinkedHashMap<>(); 빈칸();
                if (ZDROJ.charAt(Pozícia) == '}') { Pozícia++; return KR; }
                while (true) {
                    String Názov = (String)Čítanie(); 빈칸(); if (ZDROJ.charAt(Pozícia++) != ':') throw new IllegalArgumentException("údaje oddeľovač_VALUE_d8ba4873 chyba");
                    KR.put(Názov, Čítanie()); 빈칸(); char oddeľovač_VALUE_d8ba4873 = ZDROJ.charAt(Pozícia++);
                    if (oddeľovač_VALUE_d8ba4873 == '}') return KR; if (oddeľovač_VALUE_d8ba4873 != ',') throw new IllegalArgumentException("údaje oddeľovač_VALUE_d8ba4873 chyba");
                }
            }
            if (znak_VALUE == '[') {
                List<Object> KR = new ArrayList<>(); 빈칸();
                if (ZDROJ.charAt(Pozícia) == ']') { Pozícia++; return KR; }
                while (true) {
                    KR.add(Čítanie()); 빈칸(); char oddeľovač_VALUE_d8ba4873 = ZDROJ.charAt(Pozícia++);
                    if (oddeľovač_VALUE_d8ba4873 == ']') return KR; if (oddeľovač_VALUE_d8ba4873 != ',') throw new IllegalArgumentException("údaje oddeľovač_VALUE_d8ba4873 chyba");
                }
            }
            if (znak_VALUE == '"') {
                StringBuilder KR = new StringBuilder();
                while (true) {
                    char Ďalej_položka = ZDROJ.charAt(Pozícia++); if (Ďalej_položka == '"') return KR.toString();
                    if (Ďalej_položka == '\\') {
                        Ďalej_položka = ZDROJ.charAt(Pozícia++);
                        if (Ďalej_položka == 'u') { KR.append((char)Integer.parseInt(ZDROJ.substring(Pozícia, Pozícia + 4),16)); Pozícia += 4; continue; }
                        if (Ďalej_položka == 'n') Ďalej_položka = '\n'; else if (Ďalej_položka == 'r') Ďalej_položka = '\r'; else if (Ďalej_položka == 't') Ďalej_položka = '\t';
                        else if (Ďalej_položka == 'b') Ďalej_položka = '\b'; else if (Ďalej_položka == 'f') Ďalej_položka = '\f';
                        else if (Ďalej_položka != '"' && Ďalej_položka != '\\' && Ďalej_položka != '/') throw new IllegalArgumentException("문자 이스케이프 chyba");
                    }
                    KR.append(Ďalej_položka);
                }
            }
            int Spustiť_2 = Pozícia - 1;
            while (Pozícia < ZDROJ.length() && ",]} \t\r\n".indexOf(ZDROJ.charAt(Pozícia)) < 0) Pozícia++;
            String VALUE = ZDROJ.substring(Spustiť_2, Pozícia);
            if (VALUE.equals("true")) return Boolean.TRUE; if (VALUE.equals("false")) return Boolean.FALSE; if (VALUE.equals("null")) return null;
            return Double.valueOf(VALUE);
        }
    }
    static String hodnota_hash_Súbor(Path Cesta) throws Exception {
        MessageDigest 계산 = MessageDigest.getInstance("SHA-256"); byte[] údaje = new byte[1024 * 1024];
        try (InputStream vstup_VALUE = Files.newInputStream(Cesta)) { for (int dĺžka_VALUE; (dĺžka_VALUE = vstup_VALUE.read(údaje)) >= 0;) 계산.update(údaje,0,dĺžka_VALUE); }
        return hodnota_hash_SMS(계산.digest());
    }
    static String hodnota_hash_SMS(byte[] údaje) {
        StringBuilder Spracovanie_textu = new StringBuilder(); for (byte VALUE : údaje) Spracovanie_textu.append(String.format(Locale.ROOT,"%02x",VALUE & 255)); return Spracovanie_textu.toString();
    }
    static Path interný_cesta(Path akcia_koreň, String Názov) {
        Path KR = akcia_koreň.resolve(Názov).normalize();
        if (Názov.isEmpty() || Paths.get(Názov).isAbsolute() || !KR.startsWith(akcia_koreň) || Názov.indexOf('\\') >= 0)
            throw new IllegalArgumentException("범위를 벗어난 Cesta: " + Názov);
        for (Path 부분 : Paths.get(Názov)) if (부분.toString().equals("..")) throw new IllegalArgumentException("상위 Cesta 금지: " + Názov);
        for (Path v_termíne_splatnosti_položka = KR; v_termíne_splatnosti_položka != null && v_termíne_splatnosti_položka.startsWith(akcia_koreň); v_termíne_splatnosti_položka = v_termíne_splatnosti_položka.getParent())
            if (Files.isSymbolicLink(v_termíne_splatnosti_položka)) throw new IllegalArgumentException("의존성 경로의 링크 금지: " + Názov);
        return KR;
    }
    static String 명령출력(List<String> Príkaz) throws Exception {
        Process Proces_VALUE = new ProcessBuilder(Príkaz).redirectError(ProcessBuilder.Redirect.INHERIT).start();
        String KR = new String(Proces_VALUE.getInputStream().readAllBytes(),StandardCharsets.UTF_8);
        if (Proces_VALUE.waitFor() != 0) throw new IOException("Príkaz zlyhanie_VALUE: " + Príkaz.get(0)); return KR;
    }
    static void extrahovať(Path Archív_VALUE, Path cieľ_VALUE) throws Exception {
        for (String Názov : 명령출력(Arrays.asList("tar","-tzf",Archív_VALUE.toString())).split("\n")) interný_cesta(cieľ_VALUE, Názov);
        for (String riadok : 명령출력(Arrays.asList("tar","-tvzf",Archív_VALUE.toString())).split("\n"))
            if (!riadok.isEmpty() && riadok.charAt(0) != '-' && riadok.charAt(0) != 'd') throw new IOException("externý_VALUE 링크 또는 특수 파일을 포함한 의존성");
        Files.createDirectories(cieľ_VALUE);
        int Stav_VALUE = new ProcessBuilder("tar","--no-same-owner","--no-same-permissions","-xzf",Archív_VALUE.toString(),"-C",cieľ_VALUE.toString()).inheritIO().start().waitFor();
        if (Stav_VALUE != 0) throw new IOException("의존성 Archív_VALUE vydať_Úložisko zlyhanie_VALUE");
    }
    static void 호출(Path 작업경로, Path Nástroje, List<String> Argumenty, Map<String,String> 환경) throws Exception {
        List<String> Príkaz = new ArrayList<>(Arrays.asList("python3", Nástroje.toString())); Príkaz.addAll(Argumenty);
        ProcessBuilder Vykonať_príkaz = new ProcessBuilder(Príkaz).directory(작업경로.toFile()).inheritIO(); Vykonať_príkaz.environment().putAll(환경);
        int Stav_VALUE = Vykonať_príkaz.start().waitFor(); if (Stav_VALUE != 0) throw new IOException("Nástroje zlyhanie_VALUE: " + Nástroje + " (" + Stav_VALUE + ")");
    }
    @SuppressWarnings("unchecked")
    public static void main(String[] Argumenty) throws Exception {
        if (Argumenty.length < 1) throw new IllegalArgumentException("build, run, desktop, image, check, test-system 중 동작을 지정하세요");
        String Akcia = Argumenty[0];
        if (!Arrays.asList("build","run","desktop","image","check","test-system").contains(Akcia)) throw new IllegalArgumentException("알 수 없는 Akcia");
        Path akcia_koreň = Paths.get(System.getProperty("worldos.edition.root")).toAbsolutePath().normalize();
        Map<String,Object> Nastavenia = (Map<String,Object>)new údaje_analyzátor(Files.readString(akcia_koreň.resolve("native.json"),StandardCharsets.UTF_8)).Čítanie();
        Path zdroj_strom = interný_cesta(akcia_koreň,(String)Nastavenia.get("source")), jadro_VALUE = interný_cesta(zdroj_strom,(String)Nastavenia.get("native"));
        List<String> 소유파일들 = (List<String>)(List<?>)Nastavenia.get("owned_files");
        for (String Názov : 소유파일들) if (!Files.isRegularFile(interný_cesta(zdroj_strom,Názov))) throw new IOException("zdroj_strom 없음: " + Názov);
        if (Akcia.equals("check")) { System.out.println(Nastavenia.get("country") + " " + Nastavenia.get("language") + " 독립 zdroj_strom overiť 완료"); return; }
        String 자원상대 = (String)Nastavenia.getOrDefault("resource_root", ".");
        if (!자원상대.equals(".") && !자원상대.equals("..")) throw new IllegalArgumentException("의존성 akcia_koreň Cesta chyba");
        Path zdroj_VALUE = akcia_koreň.resolve(자원상대).normalize(); Path Archív_VALUE = zdroj_VALUE.resolve("native-vendor.tar.gz");
        String 기대해시 = (String)Nastavenia.get("vendor_sha256");
        if (!hodnota_hash_Súbor(Archív_VALUE).equals(기대해시)) throw new IOException("의존성 SHA-256 불일치");
        Path fixka_VALUE = zdroj_strom.resolve(".vendor-sha256");
        if (!Files.isRegularFile(fixka_VALUE) || !Files.readString(fixka_VALUE).trim().equals(기대해시)) { extrahovať(Archív_VALUE, zdroj_strom); Files.writeString(fixka_VALUE,기대해시 + "\n"); }
        Map<String,String> 환경 = new HashMap<>(System.getenv());
        Path ipConfig = null;
        if (환경.containsKey("IP_CONFIG")) ipConfig = Paths.get(환경.get("IP_CONFIG")).toAbsolutePath().normalize();
        else for (Path parent = akcia_koreň; parent != null; parent = parent.getParent()) {
            if (Files.isRegularFile(parent.resolve("ip.conf"))) { ipConfig = parent.resolve("ip.conf"); break; }
        }
        if (ipConfig == null) ipConfig = zdroj_strom.resolve("ip.conf");
        if (!Files.isRegularFile(ipConfig)) throw new IOException("Missing ip.conf: " + ipConfig);
        환경.put("IP_CONFIG", ipConfig.toString());
        if (Arrays.asList("run","desktop","test-system").contains(Akcia) && !환경.containsKey("QEMU_AARCH64")) {
            Path program_spúšťač = zdroj_VALUE.resolve("host/qemu"), spúšťač_fixka = zdroj_VALUE.resolve("host/.qemu-sha256");
            String spúšťač_hodnota_hash = (String)Nastavenia.get("qemu_sha256");
            if (!Files.isRegularFile(program_spúšťač) || !Files.isRegularFile(spúšťač_fixka) || !Files.readString(spúšťač_fixka).trim().equals(spúšťač_hodnota_hash)) {
                Path spúšťač_Archív = zdroj_VALUE.resolve("qemu-host.tar.gz"); if (!hodnota_hash_Súbor(spúšťač_Archív).equals(spúšťač_hodnota_hash)) throw new IOException("QEMU SHA-256 불일치");
                extrahovať(spúšťač_Archív,zdroj_VALUE.resolve("host")); Files.writeString(spúšťač_fixka,spúšťač_hodnota_hash + "\n");
            }
            환경.put("QEMU_AARCH64",program_spúšťač.toString());
        }
        MessageDigest 계산 = MessageDigest.getInstance("SHA-256"); Collections.sort(소유파일들);
        for (String Názov : 소유파일들) { 계산.update(Názov.getBytes(StandardCharsets.UTF_8)); 계산.update(Files.readAllBytes(interný_cesta(zdroj_strom,Názov))); }
        계산.update("ip.conf\0".getBytes(StandardCharsets.UTF_8)); 계산.update(Files.readAllBytes(ipConfig));
        String zdroj_hodnota_hash = hodnota_hash_SMS(계산.digest()); Path zostava_fixka = jadro_VALUE.resolve("build/worldos-source.sha256");
        if (Akcia.equals("build") || !Files.isRegularFile(zostava_fixka) || !Files.readString(zostava_fixka).trim().equals(zdroj_hodnota_hash)) {
            호출(jadro_VALUE,interný_cesta(jadro_VALUE,(String)Nastavenia.get("builder")),Collections.emptyList(),환경);
            Files.writeString(zostava_fixka,zdroj_hodnota_hash + "\n");
        }
        List<String> 추가인수 = new ArrayList<>(Arrays.asList(Argumenty).subList(1,Argumenty.length));
        if (Akcia.equals("run") || Akcia.equals("desktop")) {
            if (Akcia.equals("desktop")) 추가인수.add(0,"--desktop");
            호출(jadro_VALUE,interný_cesta(jadro_VALUE,(String)Nastavenia.get("runner")),추가인수,환경);
        } else if (Akcia.equals("image")) 호출(jadro_VALUE,interný_cesta(jadro_VALUE,(String)Nastavenia.get("image_builder")),추가인수,환경);
        else if (Akcia.equals("test-system")) {
            추가인수.add(0,akcia_koreň.toString()); 추가인수.add(0,"--edition");
            호출(jadro_VALUE,interný_cesta(jadro_VALUE,(String)Nastavenia.get("system_tester")),추가인수,환경);
        }
    }
}
