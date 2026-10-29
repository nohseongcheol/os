// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.security.MessageDigest;
import java.util.*;

/** 독립 국가판의 의존성 검사·복원·gusohora_sisitemu·실행을 맡는 gucumbikira Java Ibikoresho. */
public final class 국가실행기 {
    static final class 자료해석기 {
        final String Inkomoko; int 위치;
        자료해석기(String Umwandiko) { Inkomoko = Umwandiko; }
        void 빈칸() { while (위치 < Inkomoko.length() && Character.isWhitespace(Inkomoko.charAt(위치))) 위치++; }
        Object 읽기() {
            빈칸(); char inyuguti_agaciro = Inkomoko.charAt(위치++);
            if (inyuguti_agaciro == '{') {
                Map<String,Object> 결과 = new LinkedHashMap<>(); 빈칸();
                if (Inkomoko.charAt(위치) == '}') { 위치++; return 결과; }
                while (true) {
                    String Izina = (String)읽기(); 빈칸(); if (Inkomoko.charAt(위치++) != ':') throw new IllegalArgumentException("amakurushingiro mutandukanya_agaciro_d8ba4873 IKOSA");
                    결과.put(Izina, 읽기()); 빈칸(); char mutandukanya_agaciro_d8ba4873 = Inkomoko.charAt(위치++);
                    if (mutandukanya_agaciro_d8ba4873 == '}') return 결과; if (mutandukanya_agaciro_d8ba4873 != ',') throw new IllegalArgumentException("amakurushingiro mutandukanya_agaciro_d8ba4873 IKOSA");
                }
            }
            if (inyuguti_agaciro == '[') {
                List<Object> 결과 = new ArrayList<>(); 빈칸();
                if (Inkomoko.charAt(위치) == ']') { 위치++; return 결과; }
                while (true) {
                    결과.add(읽기()); 빈칸(); char mutandukanya_agaciro_d8ba4873 = Inkomoko.charAt(위치++);
                    if (mutandukanya_agaciro_d8ba4873 == ']') return 결과; if (mutandukanya_agaciro_d8ba4873 != ',') throw new IllegalArgumentException("amakurushingiro mutandukanya_agaciro_d8ba4873 IKOSA");
                }
            }
            if (inyuguti_agaciro == '"') {
                StringBuilder 결과 = new StringBuilder();
                while (true) {
                    char 다음 = Inkomoko.charAt(위치++); if (다음 == '"') return 결과.toString();
                    if (다음 == '\\') {
                        다음 = Inkomoko.charAt(위치++);
                        if (다음 == 'u') { 결과.append((char)Integer.parseInt(Inkomoko.substring(위치, 위치 + 4),16)); 위치 += 4; continue; }
                        if (다음 == 'n') 다음 = '\n'; else if (다음 == 'r') 다음 = '\r'; else if (다음 == 't') 다음 = '\t';
                        else if (다음 == 'b') 다음 = '\b'; else if (다음 == 'f') 다음 = '\f';
                        else if (다음 != '"' && 다음 != '\\' && 다음 != '/') throw new IllegalArgumentException("문자 이스케이프 IKOSA");
                    }
                    결과.append(다음);
                }
            }
            int ihuriro = 위치 - 1;
            while (위치 < Inkomoko.length() && ",]} \t\r\n".indexOf(Inkomoko.charAt(위치)) < 0) 위치++;
            String agaciro = Inkomoko.substring(ihuriro, 위치);
            if (agaciro.equals("true")) return Boolean.TRUE; if (agaciro.equals("false")) return Boolean.FALSE; if (agaciro.equals("null")) return null;
            return Double.valueOf(agaciro);
        }
    }
    static String hashi_dosiye(Path Inzira) throws Exception {
        MessageDigest 계산 = MessageDigest.getInstance("SHA-256"); byte[] amakurushingiro = new byte[1024 * 1024];
        try (InputStream 입력 = Files.newInputStream(Inzira)) { for (int uburebure_agaciro; (uburebure_agaciro = 입력.read(amakurushingiro)) >= 0;) 계산.update(amakurushingiro,0,uburebure_agaciro); }
        return hashi_SMS(계산.digest());
    }
    static String hashi_SMS(byte[] amakurushingiro) {
        StringBuilder Umwandiko = new StringBuilder(); for (byte agaciro : amakurushingiro) Umwandiko.append(String.format(Locale.ROOT,"%02x",agaciro & 255)); return Umwandiko.toString();
    }
    static Path 내부경로(Path 기준, String Izina) {
        Path 결과 = 기준.resolve(Izina).normalize();
        if (Izina.isEmpty() || Paths.get(Izina).isAbsolute() || !결과.startsWith(기준) || Izina.indexOf('\\') >= 0)
            throw new IllegalArgumentException("범위를 벗어난 Inzira: " + Izina);
        for (Path 부분 : Paths.get(Izina)) if (부분.toString().equals("..")) throw new IllegalArgumentException("상위 Inzira 금지: " + Izina);
        for (Path 현재 = 결과; 현재 != null && 현재.startsWith(기준); 현재 = 현재.getParent())
            if (Files.isSymbolicLink(현재)) throw new IllegalArgumentException("의존성 경로의 링크 금지: " + Izina);
        return 결과;
    }
    static String 명령출력(List<String> Icyo_wifuza) throws Exception {
        Process Inzira_agaciro = new ProcessBuilder(Icyo_wifuza).redirectError(ProcessBuilder.Redirect.INHERIT).start();
        String 결과 = new String(Inzira_agaciro.getInputStream().readAllBytes(),StandardCharsets.UTF_8);
        if (Inzira_agaciro.waitFor() != 0) throw new IOException("Icyo_wifuza kudakora_agaciro: " + Icyo_wifuza.get(0)); return 결과;
    }
    static void kuvanamo(Path gushyingura_agaciro, Path aho_ijya_agaciro) throws Exception {
        for (String Izina : 명령출력(Arrays.asList("tar","-tzf",gushyingura_agaciro.toString())).split("\n")) 내부경로(aho_ijya_agaciro, Izina);
        for (String umurongo : 명령출력(Arrays.asList("tar","-tvzf",gushyingura_agaciro.toString())).split("\n"))
            if (!umurongo.isEmpty() && umurongo.charAt(0) != '-' && umurongo.charAt(0) != 'd') throw new IOException("외부 링크 또는 특수 파일을 포함한 의존성");
        Files.createDirectories(aho_ijya_agaciro);
        int imimerere_agaciro = new ProcessBuilder("tar","--no-same-owner","--no-same-permissions","-xzf",gushyingura_agaciro.toString(),"-C",aho_ijya_agaciro.toString()).inheritIO().start().waitFor();
        if (imimerere_agaciro != 0) throw new IOException("의존성 gushyingura_agaciro kurekura_Ububiko kudakora_agaciro");
    }
    static void 호출(Path 작업경로, Path Ibikoresho, List<String> 인수, Map<String,String> 환경) throws Exception {
        List<String> Icyo_wifuza = new ArrayList<>(Arrays.asList("python3", Ibikoresho.toString())); Icyo_wifuza.addAll(인수);
        ProcessBuilder gukora_ibwiriza = new ProcessBuilder(Icyo_wifuza).directory(작업경로.toFile()).inheritIO(); gukora_ibwiriza.environment().putAll(환경);
        int imimerere_agaciro = gukora_ibwiriza.start().waitFor(); if (imimerere_agaciro != 0) throw new IOException("Ibikoresho kudakora_agaciro: " + Ibikoresho + " (" + imimerere_agaciro + ")");
    }
    @SuppressWarnings("unchecked")
    public static void main(String[] 인수) throws Exception {
        if (인수.length < 1) throw new IllegalArgumentException("build, run, desktop, image, check, test-system 중 동작을 지정하세요");
        String Igikorwa = 인수[0];
        if (!Arrays.asList("build","run","desktop","image","check","test-system").contains(Igikorwa)) throw new IllegalArgumentException("알 수 없는 Igikorwa");
        Path 기준 = Paths.get(System.getProperty("worldos.edition.root")).toAbsolutePath().normalize();
        Map<String,Object> Amagenamiterere = (Map<String,Object>)new 자료해석기(Files.readString(기준.resolve("native.json"),StandardCharsets.UTF_8)).읽기();
        Path inkomoko_igiti = 내부경로(기준,(String)Amagenamiterere.get("source")), intima_agaciro = 내부경로(inkomoko_igiti,(String)Amagenamiterere.get("native"));
        List<String> 소유파일들 = (List<String>)(List<?>)Amagenamiterere.get("owned_files");
        for (String Izina : 소유파일들) if (!Files.isRegularFile(내부경로(inkomoko_igiti,Izina))) throw new IOException("inkomoko_igiti 없음: " + Izina);
        if (Igikorwa.equals("check")) { System.out.println(Amagenamiterere.get("country") + " " + Amagenamiterere.get("language") + " 독립 inkomoko_igiti gusuzuma 완료"); return; }
        String 자원상대 = (String)Amagenamiterere.getOrDefault("resource_root", ".");
        if (!자원상대.equals(".") && !자원상대.equals("..")) throw new IllegalArgumentException("의존성 기준 Inzira IKOSA");
        Path umutungo_agaciro = 기준.resolve(자원상대).normalize(); Path gushyingura_agaciro = umutungo_agaciro.resolve("native-vendor.tar.gz");
        String 기대해시 = (String)Amagenamiterere.get("vendor_sha256");
        if (!hashi_dosiye(gushyingura_agaciro).equals(기대해시)) throw new IOException("의존성 SHA-256 불일치");
        Path 표식 = inkomoko_igiti.resolve(".vendor-sha256");
        if (!Files.isRegularFile(표식) || !Files.readString(표식).trim().equals(기대해시)) { kuvanamo(gushyingura_agaciro, inkomoko_igiti); Files.writeString(표식,기대해시 + "\n"); }
        Map<String,String> 환경 = new HashMap<>(System.getenv());
        Path ipConfig = null;
        if (환경.containsKey("IP_CONFIG")) ipConfig = Paths.get(환경.get("IP_CONFIG")).toAbsolutePath().normalize();
        else for (Path parent = 기준; parent != null; parent = parent.getParent()) {
            if (Files.isRegularFile(parent.resolve("ip.conf"))) { ipConfig = parent.resolve("ip.conf"); break; }
        }
        if (ipConfig == null) ipConfig = inkomoko_igiti.resolve("ip.conf");
        if (!Files.isRegularFile(ipConfig)) throw new IOException("Missing ip.conf: " + ipConfig);
        환경.put("IP_CONFIG", ipConfig.toString());
        if (Arrays.asList("run","desktop","test-system").contains(Igikorwa) && !환경.containsKey("QEMU_AARCH64")) {
            Path porogaramu_umukozi = umutungo_agaciro.resolve("host/qemu"), 실행기표식 = umutungo_agaciro.resolve("host/.qemu-sha256");
            String umukozi_hashi = (String)Amagenamiterere.get("qemu_sha256");
            if (!Files.isRegularFile(porogaramu_umukozi) || !Files.isRegularFile(실행기표식) || !Files.readString(실행기표식).trim().equals(umukozi_hashi)) {
                Path umukozi_gushyingura = umutungo_agaciro.resolve("qemu-host.tar.gz"); if (!hashi_dosiye(umukozi_gushyingura).equals(umukozi_hashi)) throw new IOException("QEMU SHA-256 불일치");
                kuvanamo(umukozi_gushyingura,umutungo_agaciro.resolve("host")); Files.writeString(실행기표식,umukozi_hashi + "\n");
            }
            환경.put("QEMU_AARCH64",porogaramu_umukozi.toString());
        }
        MessageDigest 계산 = MessageDigest.getInstance("SHA-256"); Collections.sort(소유파일들);
        for (String Izina : 소유파일들) { 계산.update(Izina.getBytes(StandardCharsets.UTF_8)); 계산.update(Files.readAllBytes(내부경로(inkomoko_igiti,Izina))); }
        계산.update("ip.conf\0".getBytes(StandardCharsets.UTF_8)); 계산.update(Files.readAllBytes(ipConfig));
        String inkomoko_hashi = hashi_SMS(계산.digest()); Path 빌드표식 = intima_agaciro.resolve("build/worldos-source.sha256");
        if (Igikorwa.equals("build") || !Files.isRegularFile(빌드표식) || !Files.readString(빌드표식).trim().equals(inkomoko_hashi)) {
            호출(intima_agaciro,내부경로(intima_agaciro,(String)Amagenamiterere.get("builder")),Collections.emptyList(),환경);
            Files.writeString(빌드표식,inkomoko_hashi + "\n");
        }
        List<String> 추가인수 = new ArrayList<>(Arrays.asList(인수).subList(1,인수.length));
        if (Igikorwa.equals("run") || Igikorwa.equals("desktop")) {
            if (Igikorwa.equals("desktop")) 추가인수.add(0,"--desktop");
            호출(intima_agaciro,내부경로(intima_agaciro,(String)Amagenamiterere.get("runner")),추가인수,환경);
        } else if (Igikorwa.equals("image")) 호출(intima_agaciro,내부경로(intima_agaciro,(String)Amagenamiterere.get("image_builder")),추가인수,환경);
        else if (Igikorwa.equals("test-system")) {
            추가인수.add(0,기준.toString()); 추가인수.add(0,"--edition");
            호출(intima_agaciro,내부경로(intima_agaciro,(String)Amagenamiterere.get("system_tester")),추가인수,환경);
        }
    }
}
