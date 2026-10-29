// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.security.MessageDigest;
import java.util.*;

/** 독립 국가판의 의존성 검사·복원·graditev_sistem·실행을 맡는 gostiti Java Orodja. */
public final class Country_zaganjalnik {
    static final class podatki_razčlenjevalnik {
        final String VIR; int Položaj;
        podatki_razčlenjevalnik(String Besedilo) { VIR = Besedilo; }
        void 빈칸() { while (Položaj < VIR.length() && Character.isWhitespace(VIR.charAt(Položaj))) Položaj++; }
        Object Branje() {
            빈칸(); char znak_VALUE = VIR.charAt(Položaj++);
            if (znak_VALUE == '{') {
                Map<String,Object> REZULTAT = new LinkedHashMap<>(); 빈칸();
                if (VIR.charAt(Položaj) == '}') { Položaj++; return REZULTAT; }
                while (true) {
                    String Ime = (String)Branje(); 빈칸(); if (VIR.charAt(Položaj++) != ':') throw new IllegalArgumentException("podatki ločilo_VALUE_d8ba4873 NAPAKA");
                    REZULTAT.put(Ime, Branje()); 빈칸(); char ločilo_VALUE_d8ba4873 = VIR.charAt(Položaj++);
                    if (ločilo_VALUE_d8ba4873 == '}') return REZULTAT; if (ločilo_VALUE_d8ba4873 != ',') throw new IllegalArgumentException("podatki ločilo_VALUE_d8ba4873 NAPAKA");
                }
            }
            if (znak_VALUE == '[') {
                List<Object> REZULTAT = new ArrayList<>(); 빈칸();
                if (VIR.charAt(Položaj) == ']') { Položaj++; return REZULTAT; }
                while (true) {
                    REZULTAT.add(Branje()); 빈칸(); char ločilo_VALUE_d8ba4873 = VIR.charAt(Položaj++);
                    if (ločilo_VALUE_d8ba4873 == ']') return REZULTAT; if (ločilo_VALUE_d8ba4873 != ',') throw new IllegalArgumentException("podatki ločilo_VALUE_d8ba4873 NAPAKA");
                }
            }
            if (znak_VALUE == '"') {
                StringBuilder REZULTAT = new StringBuilder();
                while (true) {
                    char Naprej_element = VIR.charAt(Položaj++); if (Naprej_element == '"') return REZULTAT.toString();
                    if (Naprej_element == '\\') {
                        Naprej_element = VIR.charAt(Položaj++);
                        if (Naprej_element == 'u') { REZULTAT.append((char)Integer.parseInt(VIR.substring(Položaj, Položaj + 4),16)); Položaj += 4; continue; }
                        if (Naprej_element == 'n') Naprej_element = '\n'; else if (Naprej_element == 'r') Naprej_element = '\r'; else if (Naprej_element == 't') Naprej_element = '\t';
                        else if (Naprej_element == 'b') Naprej_element = '\b'; else if (Naprej_element == 'f') Naprej_element = '\f';
                        else if (Naprej_element != '"' && Naprej_element != '\\' && Naprej_element != '/') throw new IllegalArgumentException("문자 이스케이프 NAPAKA");
                    }
                    REZULTAT.append(Naprej_element);
                }
            }
            int Zaženi = Položaj - 1;
            while (Položaj < VIR.length() && ",]} \t\r\n".indexOf(VIR.charAt(Položaj)) < 0) Položaj++;
            String VALUE = VIR.substring(Zaženi, Položaj);
            if (VALUE.equals("true")) return Boolean.TRUE; if (VALUE.equals("false")) return Boolean.FALSE; if (VALUE.equals("null")) return null;
            return Double.valueOf(VALUE);
        }
    }
    static String zgoščena_vrednost_Datoteka(Path POT) throws Exception {
        MessageDigest 계산 = MessageDigest.getInstance("SHA-256"); byte[] podatki = new byte[1024 * 1024];
        try (InputStream 입력 = Files.newInputStream(POT)) { for (int 길이; (길이 = 입력.read(podatki)) >= 0;) 계산.update(podatki,0,길이); }
        return zgoščena_vrednost_SMS(계산.digest());
    }
    static String zgoščena_vrednost_SMS(byte[] podatki) {
        StringBuilder Besedilo = new StringBuilder(); for (byte VALUE : podatki) Besedilo.append(String.format(Locale.ROOT,"%02x",VALUE & 255)); return Besedilo.toString();
    }
    static Path notranji_pot(Path pobuda_koren, String Ime) {
        Path REZULTAT = pobuda_koren.resolve(Ime).normalize();
        if (Ime.isEmpty() || Paths.get(Ime).isAbsolute() || !REZULTAT.startsWith(pobuda_koren) || Ime.indexOf('\\') >= 0)
            throw new IllegalArgumentException("범위를 벗어난 POT: " + Ime);
        for (Path 부분 : Paths.get(Ime)) if (부분.toString().equals("..")) throw new IllegalArgumentException("상위 POT 금지: " + Ime);
        for (Path sprotno_element = REZULTAT; sprotno_element != null && sprotno_element.startsWith(pobuda_koren); sprotno_element = sprotno_element.getParent())
            if (Files.isSymbolicLink(sprotno_element)) throw new IllegalArgumentException("의존성 경로의 링크 금지: " + Ime);
        return REZULTAT;
    }
    static String 명령출력(List<String> Ukaz) throws Exception {
        Process Proces_VALUE = new ProcessBuilder(Ukaz).redirectError(ProcessBuilder.Redirect.INHERIT).start();
        String REZULTAT = new String(Proces_VALUE.getInputStream().readAllBytes(),StandardCharsets.UTF_8);
        if (Proces_VALUE.waitFor() != 0) throw new IOException("Ukaz napaka_VALUE: " + Ukaz.get(0)); return REZULTAT;
    }
    static void izvleči(Path Arhiv_VALUE, Path cilj_VALUE) throws Exception {
        for (String Ime : 명령출력(Arrays.asList("tar","-tzf",Arhiv_VALUE.toString())).split("\n")) notranji_pot(cilj_VALUE, Ime);
        for (String Črtni : 명령출력(Arrays.asList("tar","-tvzf",Arhiv_VALUE.toString())).split("\n"))
            if (!Črtni.isEmpty() && Črtni.charAt(0) != '-' && Črtni.charAt(0) != 'd') throw new IOException("zunanji_VALUE 링크 또는 특수 파일을 포함한 의존성");
        Files.createDirectories(cilj_VALUE);
        int stanje_VALUE = new ProcessBuilder("tar","--no-same-owner","--no-same-permissions","-xzf",Arhiv_VALUE.toString(),"-C",cilj_VALUE.toString()).inheritIO().start().waitFor();
        if (stanje_VALUE != 0) throw new IOException("의존성 Arhiv_VALUE izdaja_Senzor_prostora napaka_VALUE");
    }
    static void 호출(Path 작업경로, Path Orodja, List<String> Argumenti, Map<String,String> 환경) throws Exception {
        List<String> Ukaz = new ArrayList<>(Arrays.asList("python3", Orodja.toString())); Ukaz.addAll(Argumenti);
        ProcessBuilder Izvedi_ukaz = new ProcessBuilder(Ukaz).directory(작업경로.toFile()).inheritIO(); Izvedi_ukaz.environment().putAll(환경);
        int stanje_VALUE = Izvedi_ukaz.start().waitFor(); if (stanje_VALUE != 0) throw new IOException("Orodja napaka_VALUE: " + Orodja + " (" + stanje_VALUE + ")");
    }
    @SuppressWarnings("unchecked")
    public static void main(String[] Argumenti) throws Exception {
        if (Argumenti.length < 1) throw new IllegalArgumentException("build, run, desktop, image, check, test-system 중 동작을 지정하세요");
        String Dejanje = Argumenti[0];
        if (!Arrays.asList("build","run","desktop","image","check","test-system").contains(Dejanje)) throw new IllegalArgumentException("알 수 없는 Dejanje");
        Path pobuda_koren = Paths.get(System.getProperty("worldos.edition.root")).toAbsolutePath().normalize();
        Map<String,Object> Nastavitve = (Map<String,Object>)new podatki_razčlenjevalnik(Files.readString(pobuda_koren.resolve("native.json"),StandardCharsets.UTF_8)).Branje();
        Path vir_drevo = notranji_pot(pobuda_koren,(String)Nastavitve.get("source")), jedro_VALUE = notranji_pot(vir_drevo,(String)Nastavitve.get("native"));
        List<String> 소유파일들 = (List<String>)(List<?>)Nastavitve.get("owned_files");
        for (String Ime : 소유파일들) if (!Files.isRegularFile(notranji_pot(vir_drevo,Ime))) throw new IOException("vir_drevo 없음: " + Ime);
        if (Dejanje.equals("check")) { System.out.println(Nastavitve.get("country") + " " + Nastavitve.get("language") + " 독립 vir_drevo 확인 완료"); return; }
        String vir_relativna_pot = (String)Nastavitve.getOrDefault("resource_root", ".");
        if (!vir_relativna_pot.equals(".") && !vir_relativna_pot.equals("..")) throw new IllegalArgumentException("의존성 pobuda_koren POT NAPAKA");
        Path vir_VALUE = pobuda_koren.resolve(vir_relativna_pot).normalize(); Path Arhiv_VALUE = vir_VALUE.resolve("native-vendor.tar.gz");
        String 기대해시 = (String)Nastavitve.get("vendor_sha256");
        if (!zgoščena_vrednost_Datoteka(Arhiv_VALUE).equals(기대해시)) throw new IOException("의존성 SHA-256 불일치");
        Path oznaka_VALUE_7e8f90bd = vir_drevo.resolve(".vendor-sha256");
        if (!Files.isRegularFile(oznaka_VALUE_7e8f90bd) || !Files.readString(oznaka_VALUE_7e8f90bd).trim().equals(기대해시)) { izvleči(Arhiv_VALUE, vir_drevo); Files.writeString(oznaka_VALUE_7e8f90bd,기대해시 + "\n"); }
        Map<String,String> 환경 = new HashMap<>(System.getenv());
        Path ipConfig = null;
        if (환경.containsKey("IP_CONFIG")) ipConfig = Paths.get(환경.get("IP_CONFIG")).toAbsolutePath().normalize();
        else for (Path parent = pobuda_koren; parent != null; parent = parent.getParent()) {
            if (Files.isRegularFile(parent.resolve("ip.conf"))) { ipConfig = parent.resolve("ip.conf"); break; }
        }
        if (ipConfig == null) ipConfig = vir_drevo.resolve("ip.conf");
        if (!Files.isRegularFile(ipConfig)) throw new IOException("Missing ip.conf: " + ipConfig);
        환경.put("IP_CONFIG", ipConfig.toString());
        if (Arrays.asList("run","desktop","test-system").contains(Dejanje) && !환경.containsKey("QEMU_AARCH64")) {
            Path aplikacija_zaganjalnik = vir_VALUE.resolve("host/qemu"), zaganjalnik_oznaka = vir_VALUE.resolve("host/.qemu-sha256");
            String zaganjalnik_zgoščena_vrednost = (String)Nastavitve.get("qemu_sha256");
            if (!Files.isRegularFile(aplikacija_zaganjalnik) || !Files.isRegularFile(zaganjalnik_oznaka) || !Files.readString(zaganjalnik_oznaka).trim().equals(zaganjalnik_zgoščena_vrednost)) {
                Path zaganjalnik_Arhiv = vir_VALUE.resolve("qemu-host.tar.gz"); if (!zgoščena_vrednost_Datoteka(zaganjalnik_Arhiv).equals(zaganjalnik_zgoščena_vrednost)) throw new IOException("QEMU SHA-256 불일치");
                izvleči(zaganjalnik_Arhiv,vir_VALUE.resolve("host")); Files.writeString(zaganjalnik_oznaka,zaganjalnik_zgoščena_vrednost + "\n");
            }
            환경.put("QEMU_AARCH64",aplikacija_zaganjalnik.toString());
        }
        MessageDigest 계산 = MessageDigest.getInstance("SHA-256"); Collections.sort(소유파일들);
        for (String Ime : 소유파일들) { 계산.update(Ime.getBytes(StandardCharsets.UTF_8)); 계산.update(Files.readAllBytes(notranji_pot(vir_drevo,Ime))); }
        계산.update("ip.conf\0".getBytes(StandardCharsets.UTF_8)); 계산.update(Files.readAllBytes(ipConfig));
        String vir_zgoščena_vrednost = zgoščena_vrednost_SMS(계산.digest()); Path graditev_oznaka = jedro_VALUE.resolve("build/worldos-source.sha256");
        if (Dejanje.equals("build") || !Files.isRegularFile(graditev_oznaka) || !Files.readString(graditev_oznaka).trim().equals(vir_zgoščena_vrednost)) {
            호출(jedro_VALUE,notranji_pot(jedro_VALUE,(String)Nastavitve.get("builder")),Collections.emptyList(),환경);
            Files.writeString(graditev_oznaka,vir_zgoščena_vrednost + "\n");
        }
        List<String> 추가인수 = new ArrayList<>(Arrays.asList(Argumenti).subList(1,Argumenti.length));
        if (Dejanje.equals("run") || Dejanje.equals("desktop")) {
            if (Dejanje.equals("desktop")) 추가인수.add(0,"--desktop");
            호출(jedro_VALUE,notranji_pot(jedro_VALUE,(String)Nastavitve.get("runner")),추가인수,환경);
        } else if (Dejanje.equals("image")) 호출(jedro_VALUE,notranji_pot(jedro_VALUE,(String)Nastavitve.get("image_builder")),추가인수,환경);
        else if (Dejanje.equals("test-system")) {
            추가인수.add(0,pobuda_koren.toString()); 추가인수.add(0,"--edition");
            호출(jedro_VALUE,notranji_pot(jedro_VALUE,(String)Nastavitve.get("system_tester")),추가인수,환경);
        }
    }
}
