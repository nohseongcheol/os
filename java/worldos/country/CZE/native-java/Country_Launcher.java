// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.security.MessageDigest;
import java.util.*;

/** 독립 국가판의 의존성 검사·복원·BLD_Systém·실행을 맡는 hostit Java nástroje. */
public final class Country_Launcher {
    static final class data_analyzátor {
        final String zdrojový_soubor; int pozice;
        data_analyzátor(String text) { zdrojový_soubor = text; }
        void 빈칸() { while (pozice < zdrojový_soubor.length() && Character.isWhitespace(zdrojový_soubor.charAt(pozice))) pozice++; }
        Object Čtení() {
            빈칸(); char znak_HODNOTA = zdrojový_soubor.charAt(pozice++);
            if (znak_HODNOTA == '{') {
                Map<String,Object> VÝSLEDEK = new LinkedHashMap<>(); 빈칸();
                if (zdrojový_soubor.charAt(pozice) == '}') { pozice++; return VÝSLEDEK; }
                while (true) {
                    String Název = (String)Čtení(); 빈칸(); if (zdrojový_soubor.charAt(pozice++) != ':') throw new IllegalArgumentException("data oddělovač_HODNOTA_d8ba4873 chyba");
                    VÝSLEDEK.put(Název, Čtení()); 빈칸(); char oddělovač_HODNOTA_d8ba4873 = zdrojový_soubor.charAt(pozice++);
                    if (oddělovač_HODNOTA_d8ba4873 == '}') return VÝSLEDEK; if (oddělovač_HODNOTA_d8ba4873 != ',') throw new IllegalArgumentException("data oddělovač_HODNOTA_d8ba4873 chyba");
                }
            }
            if (znak_HODNOTA == '[') {
                List<Object> VÝSLEDEK = new ArrayList<>(); 빈칸();
                if (zdrojový_soubor.charAt(pozice) == ']') { pozice++; return VÝSLEDEK; }
                while (true) {
                    VÝSLEDEK.add(Čtení()); 빈칸(); char oddělovač_HODNOTA_d8ba4873 = zdrojový_soubor.charAt(pozice++);
                    if (oddělovač_HODNOTA_d8ba4873 == ']') return VÝSLEDEK; if (oddělovač_HODNOTA_d8ba4873 != ',') throw new IllegalArgumentException("data oddělovač_HODNOTA_d8ba4873 chyba");
                }
            }
            if (znak_HODNOTA == '"') {
                StringBuilder VÝSLEDEK = new StringBuilder();
                while (true) {
                    char Další_zboží = zdrojový_soubor.charAt(pozice++); if (Další_zboží == '"') return VÝSLEDEK.toString();
                    if (Další_zboží == '\\') {
                        Další_zboží = zdrojový_soubor.charAt(pozice++);
                        if (Další_zboží == 'u') { VÝSLEDEK.append((char)Integer.parseInt(zdrojový_soubor.substring(pozice, pozice + 4),16)); pozice += 4; continue; }
                        if (Další_zboží == 'n') Další_zboží = '\n'; else if (Další_zboží == 'r') Další_zboží = '\r'; else if (Další_zboží == 't') Další_zboží = '\t';
                        else if (Další_zboží == 'b') Další_zboží = '\b'; else if (Další_zboží == 'f') Další_zboží = '\f';
                        else if (Další_zboží != '"' && Další_zboží != '\\' && Další_zboží != '/') throw new IllegalArgumentException("문자 이스케이프 chyba");
                    }
                    VÝSLEDEK.append(Další_zboží);
                }
            }
            int Spustit_2 = pozice - 1;
            while (pozice < zdrojový_soubor.length() && ",]} \t\r\n".indexOf(zdrojový_soubor.charAt(pozice)) < 0) pozice++;
            String HODNOTA = zdrojový_soubor.substring(Spustit_2, pozice);
            if (HODNOTA.equals("true")) return Boolean.TRUE; if (HODNOTA.equals("false")) return Boolean.FALSE; if (HODNOTA.equals("null")) return null;
            return Double.valueOf(HODNOTA);
        }
    }
    static String hodnota_hash_Soubor(Path cesta_2) throws Exception {
        MessageDigest 계산 = MessageDigest.getInstance("SHA-256"); byte[] data = new byte[1024 * 1024];
        try (InputStream vstup_HODNOTA = Files.newInputStream(cesta_2)) { for (int délka_HODNOTA; (délka_HODNOTA = vstup_HODNOTA.read(data)) >= 0;) 계산.update(data,0,délka_HODNOTA); }
        return hodnota_hash_SMS(계산.digest());
    }
    static String hodnota_hash_SMS(byte[] data) {
        StringBuilder text = new StringBuilder(); for (byte HODNOTA : data) text.append(String.format(Locale.ROOT,"%02x",HODNOTA & 255)); return text.toString();
    }
    static Path interní_cesta(Path akce_kořen, String Název) {
        Path VÝSLEDEK = akce_kořen.resolve(Název).normalize();
        if (Název.isEmpty() || Paths.get(Název).isAbsolute() || !VÝSLEDEK.startsWith(akce_kořen) || Název.indexOf('\\') >= 0)
            throw new IllegalArgumentException("범위를 벗어난 cesta_2: " + Název);
        for (Path 부분 : Paths.get(Název)) if (부분.toString().equals("..")) throw new IllegalArgumentException("상위 cesta_2 금지: " + Název);
        for (Path dobrá_zboží = VÝSLEDEK; dobrá_zboží != null && dobrá_zboží.startsWith(akce_kořen); dobrá_zboží = dobrá_zboží.getParent())
            if (Files.isSymbolicLink(dobrá_zboží)) throw new IllegalArgumentException("의존성 경로의 링크 금지: " + Název);
        return VÝSLEDEK;
    }
    static String příkaz_výstup(List<String> příkaz) throws Exception {
        Process Proces_HODNOTA = new ProcessBuilder(příkaz).redirectError(ProcessBuilder.Redirect.INHERIT).start();
        String VÝSLEDEK = new String(Proces_HODNOTA.getInputStream().readAllBytes(),StandardCharsets.UTF_8);
        if (Proces_HODNOTA.waitFor() != 0) throw new IOException("příkaz selhání_HODNOTA: " + příkaz.get(0)); return VÝSLEDEK;
    }
    static void extrahovat(Path Archiv_HODNOTA, Path cíl_HODNOTA) throws Exception {
        for (String Název : příkaz_výstup(Arrays.asList("tar","-tzf",Archiv_HODNOTA.toString())).split("\n")) interní_cesta(cíl_HODNOTA, Název);
        for (String vstupní_řádek : příkaz_výstup(Arrays.asList("tar","-tvzf",Archiv_HODNOTA.toString())).split("\n"))
            if (!vstupní_řádek.isEmpty() && vstupní_řádek.charAt(0) != '-' && vstupní_řádek.charAt(0) != 'd') throw new IOException("externí_HODNOTA 링크 또는 특수 파일을 포함한 의존성");
        Files.createDirectories(cíl_HODNOTA);
        int Stav_HODNOTA = new ProcessBuilder("tar","--no-same-owner","--no-same-permissions","-xzf",Archiv_HODNOTA.toString(),"-C",cíl_HODNOTA.toString()).inheritIO().start().waitFor();
        if (Stav_HODNOTA != 0) throw new IOException("의존성 Archiv_HODNOTA verze_Storage selhání_HODNOTA");
    }
    static void 호출(Path 작업경로, Path nástroje, List<String> argumenty, Map<String,String> prostředí_5d36e09c) throws Exception {
        List<String> příkaz = new ArrayList<>(Arrays.asList("python3", nástroje.toString())); příkaz.addAll(argumenty);
        ProcessBuilder Provést_příkaz = new ProcessBuilder(příkaz).directory(작업경로.toFile()).inheritIO(); Provést_příkaz.environment().putAll(prostředí_5d36e09c);
        int Stav_HODNOTA = Provést_příkaz.start().waitFor(); if (Stav_HODNOTA != 0) throw new IOException("nástroje selhání_HODNOTA: " + nástroje + " (" + Stav_HODNOTA + ")");
    }
    @SuppressWarnings("unchecked")
    public static void main(String[] argumenty) throws Exception {
        if (argumenty.length < 1) throw new IllegalArgumentException("build, run, desktop, image, check, test-system 중 동작을 지정하세요");
        String Akce = argumenty[0];
        if (!Arrays.asList("build","run","desktop","image","check","test-system").contains(Akce)) throw new IllegalArgumentException("알 číslo 없는 Akce");
        Path akce_kořen = Paths.get(System.getProperty("worldos.edition.root")).toAbsolutePath().normalize();
        Map<String,Object> Nastavení = (Map<String,Object>)new data_analyzátor(Files.readString(akce_kořen.resolve("native.json"),StandardCharsets.UTF_8)).Čtení();
        Path zdroj_strom = interní_cesta(akce_kořen,(String)Nastavení.get("source")), jádro_HODNOTA = interní_cesta(zdroj_strom,(String)Nastavení.get("native"));
        List<String> 소유파일들 = (List<String>)(List<?>)Nastavení.get("owned_files");
        for (String Název : 소유파일들) if (!Files.isRegularFile(interní_cesta(zdroj_strom,Název))) throw new IOException("zdroj_strom 없음: " + Název);
        if (Akce.equals("check")) { System.out.println(Nastavení.get("country") + " " + Nastavení.get("language") + " 독립 zdroj_strom ověřit 완료"); return; }
        String zdroj_relativní_cesta = (String)Nastavení.getOrDefault("resource_root", ".");
        if (!zdroj_relativní_cesta.equals(".") && !zdroj_relativní_cesta.equals("..")) throw new IllegalArgumentException("의존성 akce_kořen cesta_2 chyba");
        Path zdroj_HODNOTA = akce_kořen.resolve(zdroj_relativní_cesta).normalize(); Path Archiv_HODNOTA = zdroj_HODNOTA.resolve("native-vendor.tar.gz");
        String 기대해시 = (String)Nastavení.get("vendor_sha256");
        if (!hodnota_hash_Soubor(Archiv_HODNOTA).equals(기대해시)) throw new IOException("의존성 SHA-256 불일치");
        Path značka_HODNOTA_7e8f90bd = zdroj_strom.resolve(".vendor-sha256");
        if (!Files.isRegularFile(značka_HODNOTA_7e8f90bd) || !Files.readString(značka_HODNOTA_7e8f90bd).trim().equals(기대해시)) { extrahovat(Archiv_HODNOTA, zdroj_strom); Files.writeString(značka_HODNOTA_7e8f90bd,기대해시 + "\n"); }
        Map<String,String> prostředí_5d36e09c = new HashMap<>(System.getenv());
        Path ipConfig = null;
        if (prostředí_5d36e09c.containsKey("IP_CONFIG")) ipConfig = Paths.get(prostředí_5d36e09c.get("IP_CONFIG")).toAbsolutePath().normalize();
        else for (Path parent = akce_kořen; parent != null; parent = parent.getParent()) {
            if (Files.isRegularFile(parent.resolve("ip.conf"))) { ipConfig = parent.resolve("ip.conf"); break; }
        }
        if (ipConfig == null) ipConfig = zdroj_strom.resolve("ip.conf");
        if (!Files.isRegularFile(ipConfig)) throw new IOException("Missing ip.conf: " + ipConfig);
        prostředí_5d36e09c.put("IP_CONFIG", ipConfig.toString());
        if (Arrays.asList("run","desktop","test-system").contains(Akce) && !prostředí_5d36e09c.containsKey("QEMU_AARCH64")) {
            Path program_Launcher = zdroj_HODNOTA.resolve("host/qemu"), Launcher_značka = zdroj_HODNOTA.resolve("host/.qemu-sha256");
            String Launcher_hodnota_hash = (String)Nastavení.get("qemu_sha256");
            if (!Files.isRegularFile(program_Launcher) || !Files.isRegularFile(Launcher_značka) || !Files.readString(Launcher_značka).trim().equals(Launcher_hodnota_hash)) {
                Path Launcher_Archiv = zdroj_HODNOTA.resolve("qemu-host.tar.gz"); if (!hodnota_hash_Soubor(Launcher_Archiv).equals(Launcher_hodnota_hash)) throw new IOException("QEMU SHA-256 불일치");
                extrahovat(Launcher_Archiv,zdroj_HODNOTA.resolve("host")); Files.writeString(Launcher_značka,Launcher_hodnota_hash + "\n");
            }
            prostředí_5d36e09c.put("QEMU_AARCH64",program_Launcher.toString());
        }
        MessageDigest 계산 = MessageDigest.getInstance("SHA-256"); Collections.sort(소유파일들);
        for (String Název : 소유파일들) { 계산.update(Název.getBytes(StandardCharsets.UTF_8)); 계산.update(Files.readAllBytes(interní_cesta(zdroj_strom,Název))); }
        계산.update("ip.conf\0".getBytes(StandardCharsets.UTF_8)); 계산.update(Files.readAllBytes(ipConfig));
        String zdroj_hodnota_hash = hodnota_hash_SMS(계산.digest()); Path BLD_značka = jádro_HODNOTA.resolve("build/worldos-source.sha256");
        if (Akce.equals("build") || !Files.isRegularFile(BLD_značka) || !Files.readString(BLD_značka).trim().equals(zdroj_hodnota_hash)) {
            호출(jádro_HODNOTA,interní_cesta(jádro_HODNOTA,(String)Nastavení.get("builder")),Collections.emptyList(),prostředí_5d36e09c);
            Files.writeString(BLD_značka,zdroj_hodnota_hash + "\n");
        }
        List<String> 추가인수 = new ArrayList<>(Arrays.asList(argumenty).subList(1,argumenty.length));
        if (Akce.equals("run") || Akce.equals("desktop")) {
            if (Akce.equals("desktop")) 추가인수.add(0,"--desktop");
            호출(jádro_HODNOTA,interní_cesta(jádro_HODNOTA,(String)Nastavení.get("runner")),추가인수,prostředí_5d36e09c);
        } else if (Akce.equals("image")) 호출(jádro_HODNOTA,interní_cesta(jádro_HODNOTA,(String)Nastavení.get("image_builder")),추가인수,prostředí_5d36e09c);
        else if (Akce.equals("test-system")) {
            추가인수.add(0,akce_kořen.toString()); 추가인수.add(0,"--edition");
            호출(jádro_HODNOTA,interní_cesta(jádro_HODNOTA,(String)Nastavení.get("system_tester")),추가인수,prostředí_5d36e09c);
        }
    }
}
