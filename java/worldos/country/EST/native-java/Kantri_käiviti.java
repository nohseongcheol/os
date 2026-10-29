// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.security.MessageDigest;
import java.util.*;

/** 독립 국가판의 의존성 검사·복원·järk_süsteem·실행을 맡는 host Java Tööriistad. */
public final class Kantri_käiviti {
    static final class andmed_parser {
        final String ALLIKAS; int Asukoht;
        andmed_parser(String Tekst) { ALLIKAS = Tekst; }
        void 빈칸() { while (Asukoht < ALLIKAS.length() && Character.isWhitespace(ALLIKAS.charAt(Asukoht))) Asukoht++; }
        Object Lugemine() {
            빈칸(); char märk_VALUE = ALLIKAS.charAt(Asukoht++);
            if (märk_VALUE == '{') {
                Map<String,Object> TULEMUS = new LinkedHashMap<>(); 빈칸();
                if (ALLIKAS.charAt(Asukoht) == '}') { Asukoht++; return TULEMUS; }
                while (true) {
                    String Nimi_2 = (String)Lugemine(); 빈칸(); if (ALLIKAS.charAt(Asukoht++) != ':') throw new IllegalArgumentException("andmed eraldaja_VALUE_d8ba4873 VIGA");
                    TULEMUS.put(Nimi_2, Lugemine()); 빈칸(); char eraldaja_VALUE_d8ba4873 = ALLIKAS.charAt(Asukoht++);
                    if (eraldaja_VALUE_d8ba4873 == '}') return TULEMUS; if (eraldaja_VALUE_d8ba4873 != ',') throw new IllegalArgumentException("andmed eraldaja_VALUE_d8ba4873 VIGA");
                }
            }
            if (märk_VALUE == '[') {
                List<Object> TULEMUS = new ArrayList<>(); 빈칸();
                if (ALLIKAS.charAt(Asukoht) == ']') { Asukoht++; return TULEMUS; }
                while (true) {
                    TULEMUS.add(Lugemine()); 빈칸(); char eraldaja_VALUE_d8ba4873 = ALLIKAS.charAt(Asukoht++);
                    if (eraldaja_VALUE_d8ba4873 == ']') return TULEMUS; if (eraldaja_VALUE_d8ba4873 != ',') throw new IllegalArgumentException("andmed eraldaja_VALUE_d8ba4873 VIGA");
                }
            }
            if (märk_VALUE == '"') {
                StringBuilder TULEMUS = new StringBuilder();
                while (true) {
                    char Edasi_kaup = ALLIKAS.charAt(Asukoht++); if (Edasi_kaup == '"') return TULEMUS.toString();
                    if (Edasi_kaup == '\\') {
                        Edasi_kaup = ALLIKAS.charAt(Asukoht++);
                        if (Edasi_kaup == 'u') { TULEMUS.append((char)Integer.parseInt(ALLIKAS.substring(Asukoht, Asukoht + 4),16)); Asukoht += 4; continue; }
                        if (Edasi_kaup == 'n') Edasi_kaup = '\n'; else if (Edasi_kaup == 'r') Edasi_kaup = '\r'; else if (Edasi_kaup == 't') Edasi_kaup = '\t';
                        else if (Edasi_kaup == 'b') Edasi_kaup = '\b'; else if (Edasi_kaup == 'f') Edasi_kaup = '\f';
                        else if (Edasi_kaup != '"' && Edasi_kaup != '\\' && Edasi_kaup != '/') throw new IllegalArgumentException("문자 이스케이프 VIGA");
                    }
                    TULEMUS.append(Edasi_kaup);
                }
            }
            int Käivita_2 = Asukoht - 1;
            while (Asukoht < ALLIKAS.length() && ",]} \t\r\n".indexOf(ALLIKAS.charAt(Asukoht)) < 0) Asukoht++;
            String VALUE = ALLIKAS.substring(Käivita_2, Asukoht);
            if (VALUE.equals("true")) return Boolean.TRUE; if (VALUE.equals("false")) return Boolean.FALSE; if (VALUE.equals("null")) return null;
            return Double.valueOf(VALUE);
        }
    }
    static String räsikood_Fail(Path RADA) throws Exception {
        MessageDigest 계산 = MessageDigest.getInstance("SHA-256"); byte[] andmed = new byte[1024 * 1024];
        try (InputStream 입력 = Files.newInputStream(RADA)) { for (int 길이; (길이 = 입력.read(andmed)) >= 0;) 계산.update(andmed,0,길이); }
        return räsikood_SMS(계산.digest());
    }
    static String räsikood_SMS(byte[] andmed) {
        StringBuilder Tekst = new StringBuilder(); for (byte VALUE : andmed) Tekst.append(String.format(Locale.ROOT,"%02x",VALUE & 255)); return Tekst.toString();
    }
    static Path sisemine_tee(Path Project_juur, String Nimi_2) {
        Path TULEMUS = Project_juur.resolve(Nimi_2).normalize();
        if (Nimi_2.isEmpty() || Paths.get(Nimi_2).isAbsolute() || !TULEMUS.startsWith(Project_juur) || Nimi_2.indexOf('\\') >= 0)
            throw new IllegalArgumentException("범위를 벗어난 RADA: " + Nimi_2);
        for (Path 부분 : Paths.get(Nimi_2)) if (부분.toString().equals("..")) throw new IllegalArgumentException("상위 RADA 금지: " + Nimi_2);
        for (Path tähtaja_piires_kaup = TULEMUS; tähtaja_piires_kaup != null && tähtaja_piires_kaup.startsWith(Project_juur); tähtaja_piires_kaup = tähtaja_piires_kaup.getParent())
            if (Files.isSymbolicLink(tähtaja_piires_kaup)) throw new IllegalArgumentException("의존성 경로의 링크 금지: " + Nimi_2);
        return TULEMUS;
    }
    static String käsk_toodang(List<String> Käsk) throws Exception {
        Process Joonis_VALUE = new ProcessBuilder(Käsk).redirectError(ProcessBuilder.Redirect.INHERIT).start();
        String TULEMUS = new String(Joonis_VALUE.getInputStream().readAllBytes(),StandardCharsets.UTF_8);
        if (Joonis_VALUE.waitFor() != 0) throw new IOException("Käsk tõrge_VALUE: " + Käsk.get(0)); return TULEMUS;
    }
    static void ekstraktima(Path Arhiiv_VALUE, Path sihtkoht_VALUE) throws Exception {
        for (String Nimi_2 : käsk_toodang(Arrays.asList("tar","-tzf",Arhiiv_VALUE.toString())).split("\n")) sisemine_tee(sihtkoht_VALUE, Nimi_2);
        for (String Joon : käsk_toodang(Arrays.asList("tar","-tvzf",Arhiiv_VALUE.toString())).split("\n"))
            if (!Joon.isEmpty() && Joon.charAt(0) != '-' && Joon.charAt(0) != 'd') throw new IOException("väline_VALUE 링크 또는 특수 파일을 포함한 의존성");
        Files.createDirectories(sihtkoht_VALUE);
        int Olek_VALUE = new ProcessBuilder("tar","--no-same-owner","--no-same-permissions","-xzf",Arhiiv_VALUE.toString(),"-C",sihtkoht_VALUE.toString()).inheritIO().start().waitFor();
        if (Olek_VALUE != 0) throw new IOException("의존성 Arhiiv_VALUE vabastama_salvesti tõrge_VALUE");
    }
    static void 호출(Path 작업경로, Path Tööriistad, List<String> Argumendid, Map<String,String> 환경) throws Exception {
        List<String> Käsk = new ArrayList<>(Arrays.asList("python3", Tööriistad.toString())); Käsk.addAll(Argumendid);
        ProcessBuilder Täida_käsk = new ProcessBuilder(Käsk).directory(작업경로.toFile()).inheritIO(); Täida_käsk.environment().putAll(환경);
        int Olek_VALUE = Täida_käsk.start().waitFor(); if (Olek_VALUE != 0) throw new IOException("Tööriistad tõrge_VALUE: " + Tööriistad + " (" + Olek_VALUE + ")");
    }
    @SuppressWarnings("unchecked")
    public static void main(String[] Argumendid) throws Exception {
        if (Argumendid.length < 1) throw new IllegalArgumentException("build, run, desktop, image, check, test-system 중 동작을 지정하세요");
        String Nimi = Argumendid[0];
        if (!Arrays.asList("build","run","desktop","image","check","test-system").contains(Nimi)) throw new IllegalArgumentException("알 number 없는 Nimi");
        Path Project_juur = Paths.get(System.getProperty("worldos.edition.root")).toAbsolutePath().normalize();
        Map<String,Object> Seaded = (Map<String,Object>)new andmed_parser(Files.readString(Project_juur.resolve("native.json"),StandardCharsets.UTF_8)).Lugemine();
        Path lähe_puu = sisemine_tee(Project_juur,(String)Seaded.get("source")), tuum_VALUE = sisemine_tee(lähe_puu,(String)Seaded.get("native"));
        List<String> 소유파일들 = (List<String>)(List<?>)Seaded.get("owned_files");
        for (String Nimi_2 : 소유파일들) if (!Files.isRegularFile(sisemine_tee(lähe_puu,Nimi_2))) throw new IOException("lähe_puu 없음: " + Nimi_2);
        if (Nimi.equals("check")) { System.out.println(Seaded.get("country") + " " + Seaded.get("language") + " 독립 lähe_puu kinnitama 완료"); return; }
        String ressurss_suhteline_tee = (String)Seaded.getOrDefault("resource_root", ".");
        if (!ressurss_suhteline_tee.equals(".") && !ressurss_suhteline_tee.equals("..")) throw new IllegalArgumentException("의존성 Project_juur RADA VIGA");
        Path ressurss_VALUE = Project_juur.resolve(ressurss_suhteline_tee).normalize(); Path Arhiiv_VALUE = ressurss_VALUE.resolve("native-vendor.tar.gz");
        String 기대해시 = (String)Seaded.get("vendor_sha256");
        if (!räsikood_Fail(Arhiiv_VALUE).equals(기대해시)) throw new IOException("의존성 SHA-256 불일치");
        Path marker_VALUE = lähe_puu.resolve(".vendor-sha256");
        if (!Files.isRegularFile(marker_VALUE) || !Files.readString(marker_VALUE).trim().equals(기대해시)) { ekstraktima(Arhiiv_VALUE, lähe_puu); Files.writeString(marker_VALUE,기대해시 + "\n"); }
        Map<String,String> 환경 = new HashMap<>(System.getenv());
        Path ipConfig = null;
        if (환경.containsKey("IP_CONFIG")) ipConfig = Paths.get(환경.get("IP_CONFIG")).toAbsolutePath().normalize();
        else for (Path parent = Project_juur; parent != null; parent = parent.getParent()) {
            if (Files.isRegularFile(parent.resolve("ip.conf"))) { ipConfig = parent.resolve("ip.conf"); break; }
        }
        if (ipConfig == null) ipConfig = lähe_puu.resolve("ip.conf");
        if (!Files.isRegularFile(ipConfig)) throw new IOException("Missing ip.conf: " + ipConfig);
        환경.put("IP_CONFIG", ipConfig.toString());
        if (Arrays.asList("run","desktop","test-system").contains(Nimi) && !환경.containsKey("QEMU_AARCH64")) {
            Path programm_käiviti = ressurss_VALUE.resolve("host/qemu"), käiviti_marker = ressurss_VALUE.resolve("host/.qemu-sha256");
            String käiviti_räsikood = (String)Seaded.get("qemu_sha256");
            if (!Files.isRegularFile(programm_käiviti) || !Files.isRegularFile(käiviti_marker) || !Files.readString(käiviti_marker).trim().equals(käiviti_räsikood)) {
                Path käiviti_Arhiiv = ressurss_VALUE.resolve("qemu-host.tar.gz"); if (!räsikood_Fail(käiviti_Arhiiv).equals(käiviti_räsikood)) throw new IOException("QEMU SHA-256 불일치");
                ekstraktima(käiviti_Arhiiv,ressurss_VALUE.resolve("host")); Files.writeString(käiviti_marker,käiviti_räsikood + "\n");
            }
            환경.put("QEMU_AARCH64",programm_käiviti.toString());
        }
        MessageDigest 계산 = MessageDigest.getInstance("SHA-256"); Collections.sort(소유파일들);
        for (String Nimi_2 : 소유파일들) { 계산.update(Nimi_2.getBytes(StandardCharsets.UTF_8)); 계산.update(Files.readAllBytes(sisemine_tee(lähe_puu,Nimi_2))); }
        계산.update("ip.conf\0".getBytes(StandardCharsets.UTF_8)); 계산.update(Files.readAllBytes(ipConfig));
        String lähe_räsikood = räsikood_SMS(계산.digest()); Path järk_marker = tuum_VALUE.resolve("build/worldos-source.sha256");
        if (Nimi.equals("build") || !Files.isRegularFile(järk_marker) || !Files.readString(järk_marker).trim().equals(lähe_räsikood)) {
            호출(tuum_VALUE,sisemine_tee(tuum_VALUE,(String)Seaded.get("builder")),Collections.emptyList(),환경);
            Files.writeString(järk_marker,lähe_räsikood + "\n");
        }
        List<String> 추가인수 = new ArrayList<>(Arrays.asList(Argumendid).subList(1,Argumendid.length));
        if (Nimi.equals("run") || Nimi.equals("desktop")) {
            if (Nimi.equals("desktop")) 추가인수.add(0,"--desktop");
            호출(tuum_VALUE,sisemine_tee(tuum_VALUE,(String)Seaded.get("runner")),추가인수,환경);
        } else if (Nimi.equals("image")) 호출(tuum_VALUE,sisemine_tee(tuum_VALUE,(String)Seaded.get("image_builder")),추가인수,환경);
        else if (Nimi.equals("test-system")) {
            추가인수.add(0,Project_juur.toString()); 추가인수.add(0,"--edition");
            호출(tuum_VALUE,sisemine_tee(tuum_VALUE,(String)Seaded.get("system_tester")),추가인수,환경);
        }
    }
}
