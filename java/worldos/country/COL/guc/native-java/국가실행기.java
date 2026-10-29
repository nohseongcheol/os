// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.security.MessageDigest;
import java.util.*;

/** 독립 국가판의 의존성 검사·복원·akompiraajaa_a_yatawaajiraaya·실행을 맡는 epiajatü Java 도구. */
public final class 국가실행기 {
    static final class 자료해석기 {
        final String eejeejetülein; int 위치;
        자료해석기(String 글) { eejeejetülein = 글; }
        void 빈칸() { while (위치 < eejeejetülein.length() && Character.isWhitespace(eejeejetülein.charAt(위치))) 위치++; }
        Object 읽기() {
            빈칸(); char jeerü_ajutuu = eejeejetülein.charAt(위치++);
            if (jeerü_ajutuu == '{') {
                Map<String,Object> 결과 = new LinkedHashMap<>(); 빈칸();
                if (eejeejetülein.charAt(위치) == '}') { 위치++; return 결과; }
                while (true) {
                    String 이름 = (String)읽기(); 빈칸(); if (eejeejetülein.charAt(위치++) != ':') throw new IllegalArgumentException("atijaaya akatajülu_ajutuu ajachitia");
                    결과.put(이름, 읽기()); 빈칸(); char akatajülu_ajutuu = eejeejetülein.charAt(위치++);
                    if (akatajülu_ajutuu == '}') return 결과; if (akatajülu_ajutuu != ',') throw new IllegalArgumentException("atijaaya akatajülu_ajutuu ajachitia");
                }
            }
            if (jeerü_ajutuu == '[') {
                List<Object> 결과 = new ArrayList<>(); 빈칸();
                if (eejeejetülein.charAt(위치) == ']') { 위치++; return 결과; }
                while (true) {
                    결과.add(읽기()); 빈칸(); char akatajülu_ajutuu = eejeejetülein.charAt(위치++);
                    if (akatajülu_ajutuu == ']') return 결과; if (akatajülu_ajutuu != ',') throw new IllegalArgumentException("atijaaya akatajülu_ajutuu ajachitia");
                }
            }
            if (jeerü_ajutuu == '"') {
                StringBuilder 결과 = new StringBuilder();
                while (true) {
                    char 다음 = eejeejetülein.charAt(위치++); if (다음 == '"') return 결과.toString();
                    if (다음 == '\\') {
                        다음 = eejeejetülein.charAt(위치++);
                        if (다음 == 'u') { 결과.append((char)Integer.parseInt(eejeejetülein.substring(위치, 위치 + 4),16)); 위치 += 4; continue; }
                        if (다음 == 'n') 다음 = '\n'; else if (다음 == 'r') 다음 = '\r'; else if (다음 == 't') 다음 = '\t';
                        else if (다음 == 'b') 다음 = '\b'; else if (다음 == 'f') 다음 = '\f';
                        else if (다음 != '"' && 다음 != '\\' && 다음 != '/') throw new IllegalArgumentException("문자 이스케이프 ajachitia");
                    }
                    결과.append(다음);
                }
            }
            int 시작 = 위치 - 1;
            while (위치 < eejeejetülein.length() && ",]} \t\r\n".indexOf(eejeejetülein.charAt(위치)) < 0) 위치++;
            String ajutuu = eejeejetülein.substring(시작, 위치);
            if (ajutuu.equals("true")) return Boolean.TRUE; if (ajutuu.equals("false")) return Boolean.FALSE; if (ajutuu.equals("null")) return null;
            return Double.valueOf(ajutuu);
        }
    }
    static String 해시(Path wopu_a_ttaaleemüin) throws Exception {
        MessageDigest 계산 = MessageDigest.getInstance("SHA-256"); byte[] atijaaya = new byte[1024 * 1024];
        try (InputStream 입력 = Files.newInputStream(wopu_a_ttaaleemüin)) { for (int akaliaa_ajutuu; (akaliaa_ajutuu = 입력.read(atijaaya)) >= 0;) 계산.update(atijaaya,0,akaliaa_ajutuu); }
        return 해시글(계산.digest());
    }
    static String 해시글(byte[] atijaaya) {
        StringBuilder 글 = new StringBuilder(); for (byte ajutuu : atijaaya) 글.append(String.format(Locale.ROOT,"%02x",ajutuu & 255)); return 글.toString();
    }
    static Path 내부경로(Path 기준, String 이름) {
        Path 결과 = 기준.resolve(이름).normalize();
        if (이름.isEmpty() || Paths.get(이름).isAbsolute() || !결과.startsWith(기준) || 이름.indexOf('\\') >= 0)
            throw new IllegalArgumentException("범위를 벗어난 wopu_a_ttaaleemüin: " + 이름);
        for (Path 부분 : Paths.get(이름)) if (부분.toString().equals("..")) throw new IllegalArgumentException("상위 wopu_a_ttaaleemüin 금지: " + 이름);
        for (Path 현재 = 결과; 현재 != null && 현재.startsWith(기준); 현재 = 현재.getParent())
            if (Files.isSymbolicLink(현재)) throw new IllegalArgumentException("의존성 경로의 링크 금지: " + 이름);
        return 결과;
    }
    static String 명령출력(List<String> aluwataaya) throws Exception {
        Process 과정 = new ProcessBuilder(aluwataaya).redirectError(ProcessBuilder.Redirect.INHERIT).start();
        String 결과 = new String(과정.getInputStream().readAllBytes(),StandardCharsets.UTF_8);
        if (과정.waitFor() != 0) throw new IOException("aluwataaya ajachitia_ajutuu: " + aluwataaya.get(0)); return 결과;
    }
    static void 풀기(Path anaajawaa_ajutuu, Path jalamüinjatü_ajutuu) throws Exception {
        for (String 이름 : 명령출력(Arrays.asList("tar","-tzf",anaajawaa_ajutuu.toString())).split("\n")) 내부경로(jalamüinjatü_ajutuu, 이름);
        for (String liinia : 명령출력(Arrays.asList("tar","-tvzf",anaajawaa_ajutuu.toString())).split("\n"))
            if (!liinia.isEmpty() && liinia.charAt(0) != '-' && liinia.charAt(0) != 'd') throw new IOException("외부 링크 또는 특수 파일을 포함한 의존성");
        Files.createDirectories(jalamüinjatü_ajutuu);
        int jamakua_iparülein_ajutuu = new ProcessBuilder("tar","--no-same-owner","--no-same-permissions","-xzf",anaajawaa_ajutuu.toString(),"-C",jalamüinjatü_ajutuu.toString()).inheritIO().start().waitFor();
        if (jamakua_iparülein_ajutuu != 0) throw new IOException("의존성 anaajawaa_ajutuu 해제 ajachitia_ajutuu");
    }
    static void 호출(Path 작업경로, Path 도구, List<String> 인수, Map<String,String> 환경) throws Exception {
        List<String> aluwataaya = new ArrayList<>(Arrays.asList("python3", 도구.toString())); aluwataaya.addAll(인수);
        ProcessBuilder 실행 = new ProcessBuilder(aluwataaya).directory(작업경로.toFile()).inheritIO(); 실행.environment().putAll(환경);
        int jamakua_iparülein_ajutuu = 실행.start().waitFor(); if (jamakua_iparülein_ajutuu != 0) throw new IOException("도구 ajachitia_ajutuu: " + 도구 + " (" + jamakua_iparülein_ajutuu + ")");
    }
    @SuppressWarnings("unchecked")
    public static void main(String[] 인수) throws Exception {
        if (인수.length < 1) throw new IllegalArgumentException("build, run, desktop, image, check, test-system 중 동작을 지정하세요");
        String aa_inra_awai = 인수[0];
        if (!Arrays.asList("build","run","desktop","image","check","test-system").contains(aa_inra_awai)) throw new IllegalArgumentException("알 수 없는 aa_inra_awai");
        Path 기준 = Paths.get(System.getProperty("worldos.edition.root")).toAbsolutePath().normalize();
        Map<String,Object> 설정 = (Map<String,Object>)new 자료해석기(Files.readString(기준.resolve("native.json"),StandardCharsets.UTF_8)).읽기();
        Path eejeejetülein_wunu_ulia = 내부경로(기준,(String)설정.get("source")), keetnerü_ajutuu = 내부경로(eejeejetülein_wunu_ulia,(String)설정.get("native"));
        List<String> 소유파일들 = (List<String>)(List<?>)설정.get("owned_files");
        for (String 이름 : 소유파일들) if (!Files.isRegularFile(내부경로(eejeejetülein_wunu_ulia,이름))) throw new IOException("eejeejetülein_wunu_ulia 없음: " + 이름);
        if (aa_inra_awai.equals("check")) { System.out.println(설정.get("country") + " " + 설정.get("language") + " 독립 eejeejetülein_wunu_ulia 확인 완료"); return; }
        String 자원상대 = (String)설정.getOrDefault("resource_root", ".");
        if (!자원상대.equals(".") && !자원상대.equals("..")) throw new IllegalArgumentException("의존성 기준 wopu_a_ttaaleemüin ajachitia");
        Path ama_anaajatü_ajutuu = 기준.resolve(자원상대).normalize(); Path anaajawaa_ajutuu = ama_anaajatü_ajutuu.resolve("native-vendor.tar.gz");
        String 기대해시 = (String)설정.get("vendor_sha256");
        if (!해시(anaajawaa_ajutuu).equals(기대해시)) throw new IOException("의존성 SHA-256 불일치");
        Path 표식 = eejeejetülein_wunu_ulia.resolve(".vendor-sha256");
        if (!Files.isRegularFile(표식) || !Files.readString(표식).trim().equals(기대해시)) { 풀기(anaajawaa_ajutuu, eejeejetülein_wunu_ulia); Files.writeString(표식,기대해시 + "\n"); }
        Map<String,String> 환경 = new HashMap<>(System.getenv());
        Path ipConfig = null;
        if (환경.containsKey("IP_CONFIG")) ipConfig = Paths.get(환경.get("IP_CONFIG")).toAbsolutePath().normalize();
        else for (Path parent = 기준; parent != null; parent = parent.getParent()) {
            if (Files.isRegularFile(parent.resolve("ip.conf"))) { ipConfig = parent.resolve("ip.conf"); break; }
        }
        if (ipConfig == null) ipConfig = eejeejetülein_wunu_ulia.resolve("ip.conf");
        if (!Files.isRegularFile(ipConfig)) throw new IOException("Missing ip.conf: " + ipConfig);
        환경.put("IP_CONFIG", ipConfig.toString());
        if (Arrays.asList("run","desktop","test-system").contains(aa_inra_awai) && !환경.containsKey("QEMU_AARCH64")) {
            Path 실행기 = ama_anaajatü_ajutuu.resolve("host/qemu"), 실행기표식 = ama_anaajatü_ajutuu.resolve("host/.qemu-sha256");
            String 실행기해시 = (String)설정.get("qemu_sha256");
            if (!Files.isRegularFile(실행기) || !Files.isRegularFile(실행기표식) || !Files.readString(실행기표식).trim().equals(실행기해시)) {
                Path 실행기압축 = ama_anaajatü_ajutuu.resolve("qemu-host.tar.gz"); if (!해시(실행기압축).equals(실행기해시)) throw new IOException("QEMU SHA-256 불일치");
                풀기(실행기압축,ama_anaajatü_ajutuu.resolve("host")); Files.writeString(실행기표식,실행기해시 + "\n");
            }
            환경.put("QEMU_AARCH64",실행기.toString());
        }
        MessageDigest 계산 = MessageDigest.getInstance("SHA-256"); Collections.sort(소유파일들);
        for (String 이름 : 소유파일들) { 계산.update(이름.getBytes(StandardCharsets.UTF_8)); 계산.update(Files.readAllBytes(내부경로(eejeejetülein_wunu_ulia,이름))); }
        계산.update("ip.conf\0".getBytes(StandardCharsets.UTF_8)); 계산.update(Files.readAllBytes(ipConfig));
        String 소스해시 = 해시글(계산.digest()); Path 빌드표식 = keetnerü_ajutuu.resolve("build/worldos-source.sha256");
        if (aa_inra_awai.equals("build") || !Files.isRegularFile(빌드표식) || !Files.readString(빌드표식).trim().equals(소스해시)) {
            호출(keetnerü_ajutuu,내부경로(keetnerü_ajutuu,(String)설정.get("builder")),Collections.emptyList(),환경);
            Files.writeString(빌드표식,소스해시 + "\n");
        }
        List<String> 추가인수 = new ArrayList<>(Arrays.asList(인수).subList(1,인수.length));
        if (aa_inra_awai.equals("run") || aa_inra_awai.equals("desktop")) {
            if (aa_inra_awai.equals("desktop")) 추가인수.add(0,"--desktop");
            호출(keetnerü_ajutuu,내부경로(keetnerü_ajutuu,(String)설정.get("runner")),추가인수,환경);
        } else if (aa_inra_awai.equals("image")) 호출(keetnerü_ajutuu,내부경로(keetnerü_ajutuu,(String)설정.get("image_builder")),추가인수,환경);
        else if (aa_inra_awai.equals("test-system")) {
            추가인수.add(0,기준.toString()); 추가인수.add(0,"--edition");
            호출(keetnerü_ajutuu,내부경로(keetnerü_ajutuu,(String)설정.get("system_tester")),추가인수,환경);
        }
    }
}
