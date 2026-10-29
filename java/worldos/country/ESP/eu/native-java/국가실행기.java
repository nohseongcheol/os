// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.security.MessageDigest;
import java.util.*;

/** 독립 국가판의 의존성 검사·복원·eraiki_sistema·실행을 맡는 Ostalari Java Tresnak. */
public final class 국가실행기 {
    static final class datuak_analizatzaile {
        final String ITURBURUA; int Posizioa;
        datuak_analizatzaile(String Testua) { ITURBURUA = Testua; }
        void 빈칸() { while (Posizioa < ITURBURUA.length() && Character.isWhitespace(ITURBURUA.charAt(Posizioa))) Posizioa++; }
        Object Irakurri() {
            빈칸(); char karaktere_balio = ITURBURUA.charAt(Posizioa++);
            if (karaktere_balio == '{') {
                Map<String,Object> EMAITZA = new LinkedHashMap<>(); 빈칸();
                if (ITURBURUA.charAt(Posizioa) == '}') { Posizioa++; return EMAITZA; }
                while (true) {
                    String Izena = (String)Irakurri(); 빈칸(); if (ITURBURUA.charAt(Posizioa++) != ':') throw new IllegalArgumentException("datuak mugatzaile_balio errorea");
                    EMAITZA.put(Izena, Irakurri()); 빈칸(); char mugatzaile_balio = ITURBURUA.charAt(Posizioa++);
                    if (mugatzaile_balio == '}') return EMAITZA; if (mugatzaile_balio != ',') throw new IllegalArgumentException("datuak mugatzaile_balio errorea");
                }
            }
            if (karaktere_balio == '[') {
                List<Object> EMAITZA = new ArrayList<>(); 빈칸();
                if (ITURBURUA.charAt(Posizioa) == ']') { Posizioa++; return EMAITZA; }
                while (true) {
                    EMAITZA.add(Irakurri()); 빈칸(); char mugatzaile_balio = ITURBURUA.charAt(Posizioa++);
                    if (mugatzaile_balio == ']') return EMAITZA; if (mugatzaile_balio != ',') throw new IllegalArgumentException("datuak mugatzaile_balio errorea");
                }
            }
            if (karaktere_balio == '"') {
                StringBuilder EMAITZA = new StringBuilder();
                while (true) {
                    char Hurrengoa_elementu = ITURBURUA.charAt(Posizioa++); if (Hurrengoa_elementu == '"') return EMAITZA.toString();
                    if (Hurrengoa_elementu == '\\') {
                        Hurrengoa_elementu = ITURBURUA.charAt(Posizioa++);
                        if (Hurrengoa_elementu == 'u') { EMAITZA.append((char)Integer.parseInt(ITURBURUA.substring(Posizioa, Posizioa + 4),16)); Posizioa += 4; continue; }
                        if (Hurrengoa_elementu == 'n') Hurrengoa_elementu = '\n'; else if (Hurrengoa_elementu == 'r') Hurrengoa_elementu = '\r'; else if (Hurrengoa_elementu == 't') Hurrengoa_elementu = '\t';
                        else if (Hurrengoa_elementu == 'b') Hurrengoa_elementu = '\b'; else if (Hurrengoa_elementu == 'f') Hurrengoa_elementu = '\f';
                        else if (Hurrengoa_elementu != '"' && Hurrengoa_elementu != '\\' && Hurrengoa_elementu != '/') throw new IllegalArgumentException("문자 이스케이프 errorea");
                    }
                    EMAITZA.append(Hurrengoa_elementu);
                }
            }
            int Exekutatu_2 = Posizioa - 1;
            while (Posizioa < ITURBURUA.length() && ",]} \t\r\n".indexOf(ITURBURUA.charAt(Posizioa)) < 0) Posizioa++;
            String balio = ITURBURUA.substring(Exekutatu_2, Posizioa);
            if (balio.equals("true")) return Boolean.TRUE; if (balio.equals("false")) return Boolean.FALSE; if (balio.equals("null")) return null;
            return Double.valueOf(balio);
        }
    }
    static String hash_fitxategi(Path Bide_izena) throws Exception {
        MessageDigest 계산 = MessageDigest.getInstance("SHA-256"); byte[] datuak = new byte[1024 * 1024];
        try (InputStream 입력 = Files.newInputStream(Bide_izena)) { for (int luzera_balio; (luzera_balio = 입력.read(datuak)) >= 0;) 계산.update(datuak,0,luzera_balio); }
        return hash_SMS(계산.digest());
    }
    static String hash_SMS(byte[] datuak) {
        StringBuilder Testua = new StringBuilder(); for (byte balio : datuak) Testua.append(String.format(Locale.ROOT,"%02x",balio & 255)); return Testua.toString();
    }
    static Path 내부경로(Path Project_erro, String Izena) {
        Path EMAITZA = Project_erro.resolve(Izena).normalize();
        if (Izena.isEmpty() || Paths.get(Izena).isAbsolute() || !EMAITZA.startsWith(Project_erro) || Izena.indexOf('\\') >= 0)
            throw new IllegalArgumentException("범위를 벗어난 Bide_izena: " + Izena);
        for (Path 부분 : Paths.get(Izena)) if (부분.toString().equals("..")) throw new IllegalArgumentException("상위 Bide_izena 금지: " + Izena);
        for (Path 현재 = EMAITZA; 현재 != null && 현재.startsWith(Project_erro); 현재 = 현재.getParent())
            if (Files.isSymbolicLink(현재)) throw new IllegalArgumentException("의존성 경로의 링크 금지: " + Izena);
        return EMAITZA;
    }
    static String 명령출력(List<String> Komandoa) throws Exception {
        Process prozesu_balio = new ProcessBuilder(Komandoa).redirectError(ProcessBuilder.Redirect.INHERIT).start();
        String EMAITZA = new String(prozesu_balio.getInputStream().readAllBytes(),StandardCharsets.UTF_8);
        if (prozesu_balio.waitFor() != 0) throw new IOException("Komandoa hutsegite_balio: " + Komandoa.get(0)); return EMAITZA;
    }
    static void atera(Path artxibo_balio, Path helburu_balio_a0fbc067) throws Exception {
        for (String Izena : 명령출력(Arrays.asList("tar","-tzf",artxibo_balio.toString())).split("\n")) 내부경로(helburu_balio_a0fbc067, Izena);
        for (String Marra : 명령출력(Arrays.asList("tar","-tvzf",artxibo_balio.toString())).split("\n"))
            if (!Marra.isEmpty() && Marra.charAt(0) != '-' && Marra.charAt(0) != 'd') throw new IOException("외부 링크 또는 특수 파일을 포함한 의존성");
        Files.createDirectories(helburu_balio_a0fbc067);
        int Egoera_balio = new ProcessBuilder("tar","--no-same-owner","--no-same-permissions","-xzf",artxibo_balio.toString(),"-C",helburu_balio_a0fbc067.toString()).inheritIO().start().waitFor();
        if (Egoera_balio != 0) throw new IOException("의존성 artxibo_balio askatu_biltegi hutsegite_balio");
    }
    static void 호출(Path 작업경로, Path Tresnak, List<String> Argumentuak, Map<String,String> 환경) throws Exception {
        List<String> Komandoa = new ArrayList<>(Arrays.asList("python3", Tresnak.toString())); Komandoa.addAll(Argumentuak);
        ProcessBuilder exekutatu_komando = new ProcessBuilder(Komandoa).directory(작업경로.toFile()).inheritIO(); exekutatu_komando.environment().putAll(환경);
        int Egoera_balio = exekutatu_komando.start().waitFor(); if (Egoera_balio != 0) throw new IOException("Tresnak hutsegite_balio: " + Tresnak + " (" + Egoera_balio + ")");
    }
    @SuppressWarnings("unchecked")
    public static void main(String[] Argumentuak) throws Exception {
        if (Argumentuak.length < 1) throw new IllegalArgumentException("build, run, desktop, image, check, test-system 중 동작을 지정하세요");
        String Ekintza = Argumentuak[0];
        if (!Arrays.asList("build","run","desktop","image","check","test-system").contains(Ekintza)) throw new IllegalArgumentException("알 수 없는 Ekintza");
        Path Project_erro = Paths.get(System.getProperty("worldos.edition.root")).toAbsolutePath().normalize();
        Map<String,Object> Ezarpenak = (Map<String,Object>)new datuak_analizatzaile(Files.readString(Project_erro.resolve("native.json"),StandardCharsets.UTF_8)).Irakurri();
        Path iturburu_zuhaitz = 내부경로(Project_erro,(String)Ezarpenak.get("source")), nukleo_balio = 내부경로(iturburu_zuhaitz,(String)Ezarpenak.get("native"));
        List<String> 소유파일들 = (List<String>)(List<?>)Ezarpenak.get("owned_files");
        for (String Izena : 소유파일들) if (!Files.isRegularFile(내부경로(iturburu_zuhaitz,Izena))) throw new IOException("iturburu_zuhaitz 없음: " + Izena);
        if (Ekintza.equals("check")) { System.out.println(Ezarpenak.get("country") + " " + Ezarpenak.get("language") + " 독립 iturburu_zuhaitz egiaztatu 완료"); return; }
        String 자원상대 = (String)Ezarpenak.getOrDefault("resource_root", ".");
        if (!자원상대.equals(".") && !자원상대.equals("..")) throw new IllegalArgumentException("의존성 Project_erro Bide_izena errorea");
        Path baliabide_balio = Project_erro.resolve(자원상대).normalize(); Path artxibo_balio = baliabide_balio.resolve("native-vendor.tar.gz");
        String 기대해시 = (String)Ezarpenak.get("vendor_sha256");
        if (!hash_fitxategi(artxibo_balio).equals(기대해시)) throw new IOException("의존성 SHA-256 불일치");
        Path 표식 = iturburu_zuhaitz.resolve(".vendor-sha256");
        if (!Files.isRegularFile(표식) || !Files.readString(표식).trim().equals(기대해시)) { atera(artxibo_balio, iturburu_zuhaitz); Files.writeString(표식,기대해시 + "\n"); }
        Map<String,String> 환경 = new HashMap<>(System.getenv());
        Path ipConfig = null;
        if (환경.containsKey("IP_CONFIG")) ipConfig = Paths.get(환경.get("IP_CONFIG")).toAbsolutePath().normalize();
        else for (Path parent = Project_erro; parent != null; parent = parent.getParent()) {
            if (Files.isRegularFile(parent.resolve("ip.conf"))) { ipConfig = parent.resolve("ip.conf"); break; }
        }
        if (ipConfig == null) ipConfig = iturburu_zuhaitz.resolve("ip.conf");
        if (!Files.isRegularFile(ipConfig)) throw new IOException("Missing ip.conf: " + ipConfig);
        환경.put("IP_CONFIG", ipConfig.toString());
        if (Arrays.asList("run","desktop","test-system").contains(Ekintza) && !환경.containsKey("QEMU_AARCH64")) {
            Path aplik_abiarazle = baliabide_balio.resolve("host/qemu"), 실행기표식 = baliabide_balio.resolve("host/.qemu-sha256");
            String abiarazle_hash = (String)Ezarpenak.get("qemu_sha256");
            if (!Files.isRegularFile(aplik_abiarazle) || !Files.isRegularFile(실행기표식) || !Files.readString(실행기표식).trim().equals(abiarazle_hash)) {
                Path abiarazle_artxibo = baliabide_balio.resolve("qemu-host.tar.gz"); if (!hash_fitxategi(abiarazle_artxibo).equals(abiarazle_hash)) throw new IOException("QEMU SHA-256 불일치");
                atera(abiarazle_artxibo,baliabide_balio.resolve("host")); Files.writeString(실행기표식,abiarazle_hash + "\n");
            }
            환경.put("QEMU_AARCH64",aplik_abiarazle.toString());
        }
        MessageDigest 계산 = MessageDigest.getInstance("SHA-256"); Collections.sort(소유파일들);
        for (String Izena : 소유파일들) { 계산.update(Izena.getBytes(StandardCharsets.UTF_8)); 계산.update(Files.readAllBytes(내부경로(iturburu_zuhaitz,Izena))); }
        계산.update("ip.conf\0".getBytes(StandardCharsets.UTF_8)); 계산.update(Files.readAllBytes(ipConfig));
        String iturburu_hash = hash_SMS(계산.digest()); Path 빌드표식 = nukleo_balio.resolve("build/worldos-source.sha256");
        if (Ekintza.equals("build") || !Files.isRegularFile(빌드표식) || !Files.readString(빌드표식).trim().equals(iturburu_hash)) {
            호출(nukleo_balio,내부경로(nukleo_balio,(String)Ezarpenak.get("builder")),Collections.emptyList(),환경);
            Files.writeString(빌드표식,iturburu_hash + "\n");
        }
        List<String> 추가인수 = new ArrayList<>(Arrays.asList(Argumentuak).subList(1,Argumentuak.length));
        if (Ekintza.equals("run") || Ekintza.equals("desktop")) {
            if (Ekintza.equals("desktop")) 추가인수.add(0,"--desktop");
            호출(nukleo_balio,내부경로(nukleo_balio,(String)Ezarpenak.get("runner")),추가인수,환경);
        } else if (Ekintza.equals("image")) 호출(nukleo_balio,내부경로(nukleo_balio,(String)Ezarpenak.get("image_builder")),추가인수,환경);
        else if (Ekintza.equals("test-system")) {
            추가인수.add(0,Project_erro.toString()); 추가인수.add(0,"--edition");
            호출(nukleo_balio,내부경로(nukleo_balio,(String)Ezarpenak.get("system_tester")),추가인수,환경);
        }
    }
}
