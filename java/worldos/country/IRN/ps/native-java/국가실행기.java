// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.security.MessageDigest;
import java.util.*;

/** 독립 국가판의 의존성 검사·복원·جوړول_غونډال·실행을 맡는 کوربه Java 도구. */
public final class 국가실행기 {
    static final class 자료해석기 {
        final String سرچينه; int ځای;
        자료해석기(String ليکنه) { سرچينه = ليکنه; }
        void 빈칸() { while (ځای < سرچينه.length() && Character.isWhitespace(سرچينه.charAt(ځای))) ځای++; }
        Object لوستل() {
            빈칸(); char لوښه_ارزښت = سرچينه.charAt(ځای++);
            if (لوښه_ارزښت == '{') {
                Map<String,Object> 결과 = new LinkedHashMap<>(); 빈칸();
                if (سرچينه.charAt(ځای) == '}') { ځای++; return 결과; }
                while (true) {
                    String نوم = (String)لوستل(); 빈칸(); if (سرچينه.charAt(ځای++) != ':') throw new IllegalArgumentException("اومتوک راچاپېرل_ارزښت تېروتنه");
                    결과.put(نوم, لوستل()); 빈칸(); char راچاپېرل_ارزښت = سرچينه.charAt(ځای++);
                    if (راچاپېرل_ارزښت == '}') return 결과; if (راچاپېرل_ارزښت != ',') throw new IllegalArgumentException("اومتوک راچاپېرل_ارزښت تېروتنه");
                }
            }
            if (لوښه_ارزښت == '[') {
                List<Object> 결과 = new ArrayList<>(); 빈칸();
                if (سرچينه.charAt(ځای) == ']') { ځای++; return 결과; }
                while (true) {
                    결과.add(لوستل()); 빈칸(); char راچاپېرل_ارزښت = سرچينه.charAt(ځای++);
                    if (راچاپېرل_ارزښت == ']') return 결과; if (راچاپېرل_ارزښت != ',') throw new IllegalArgumentException("اومتوک راچاپېرل_ارزښت تېروتنه");
                }
            }
            if (لوښه_ارزښت == '"') {
                StringBuilder 결과 = new StringBuilder();
                while (true) {
                    char 다음 = سرچينه.charAt(ځای++); if (다음 == '"') return 결과.toString();
                    if (다음 == '\\') {
                        다음 = سرچينه.charAt(ځای++);
                        if (다음 == 'u') { 결과.append((char)Integer.parseInt(سرچينه.substring(ځای, ځای + 4),16)); ځای += 4; continue; }
                        if (다음 == 'n') 다음 = '\n'; else if (다음 == 'r') 다음 = '\r'; else if (다음 == 't') 다음 = '\t';
                        else if (다음 == 'b') 다음 = '\b'; else if (다음 == 'f') 다음 = '\f';
                        else if (다음 != '"' && 다음 != '\\' && 다음 != '/') throw new IllegalArgumentException("문자 이스케이프 تېروتنه");
                    }
                    결과.append(다음);
                }
            }
            int ځغلول = ځای - 1;
            while (ځای < سرچينه.length() && ",]} \t\r\n".indexOf(سرچينه.charAt(ځای)) < 0) ځای++;
            String ارزښت = سرچينه.substring(ځغلول, ځای);
            if (ارزښت.equals("true")) return Boolean.TRUE; if (ارزښت.equals("false")) return Boolean.FALSE; if (ارزښت.equals("null")) return null;
            return Double.valueOf(ارزښت);
        }
    }
    static String 해시(Path يونلور) throws Exception {
        MessageDigest 계산 = MessageDigest.getInstance("SHA-256"); byte[] اومتوک = new byte[1024 * 1024];
        try (InputStream 입력 = Files.newInputStream(يونلور)) { for (int اوږدوالى_ارزښت; (اوږدوالى_ارزښت = 입력.read(اومتوک)) >= 0;) 계산.update(اومتوک,0,اوږدوالى_ارزښت); }
        return 해시글(계산.digest());
    }
    static String 해시글(byte[] اومتوک) {
        StringBuilder ليکنه = new StringBuilder(); for (byte ارزښت : اومتوک) ليکنه.append(String.format(Locale.ROOT,"%02x",ارزښت & 255)); return ليکنه.toString();
    }
    static Path 내부경로(Path 기준, String نوم) {
        Path 결과 = 기준.resolve(نوم).normalize();
        if (نوم.isEmpty() || Paths.get(نوم).isAbsolute() || !결과.startsWith(기준) || نوم.indexOf('\\') >= 0)
            throw new IllegalArgumentException("범위를 벗어난 يونلور: " + نوم);
        for (Path 부분 : Paths.get(نوم)) if (부분.toString().equals("..")) throw new IllegalArgumentException("상위 يونلور 금지: " + نوم);
        for (Path 현재 = 결과; 현재 != null && 현재.startsWith(기준); 현재 = 현재.getParent())
            if (Files.isSymbolicLink(현재)) throw new IllegalArgumentException("의존성 경로의 링크 금지: " + نوم);
        return 결과;
    }
    static String 명령출력(List<String> بولۍ) throws Exception {
        Process 과정 = new ProcessBuilder(بولۍ).redirectError(ProcessBuilder.Redirect.INHERIT).start();
        String 결과 = new String(과정.getInputStream().readAllBytes(),StandardCharsets.UTF_8);
        if (과정.waitFor() != 0) throw new IOException("بولۍ پاتېينه_ارزښت: " + بولۍ.get(0)); return 결과;
    }
    static void 풀기(Path ارشیف_ارزښت, Path موخه_ارزښت) throws Exception {
        for (String نوم : 명령출력(Arrays.asList("tar","-tzf",ارشیف_ارزښت.toString())).split("\n")) 내부경로(موخه_ارزښت, نوم);
        for (String ليکه : 명령출력(Arrays.asList("tar","-tvzf",ارشیف_ارزښت.toString())).split("\n"))
            if (!ليکه.isEmpty() && ليکه.charAt(0) != '-' && ليکه.charAt(0) != 'd') throw new IOException("외부 링크 또는 특수 파일을 포함한 의존성");
        Files.createDirectories(موخه_ارزښت);
        int انکړ_ارزښت = new ProcessBuilder("tar","--no-same-owner","--no-same-permissions","-xzf",ارشیف_ارزښت.toString(),"-C",موخه_ارزښت.toString()).inheritIO().start().waitFor();
        if (انکړ_ارزښت != 0) throw new IOException("의존성 ارشیف_ارزښت 해제 پاتېينه_ارزښت");
    }
    static void 호출(Path 작업경로, Path 도구, List<String> 인수, Map<String,String> 환경) throws Exception {
        List<String> بولۍ = new ArrayList<>(Arrays.asList("python3", 도구.toString())); بولۍ.addAll(인수);
        ProcessBuilder 실행 = new ProcessBuilder(بولۍ).directory(작업경로.toFile()).inheritIO(); 실행.environment().putAll(환경);
        int انکړ_ارزښت = 실행.start().waitFor(); if (انکړ_ارزښت != 0) throw new IOException("도구 پاتېينه_ارزښت: " + 도구 + " (" + انکړ_ارزښت + ")");
    }
    @SuppressWarnings("unchecked")
    public static void main(String[] 인수) throws Exception {
        if (인수.length < 1) throw new IllegalArgumentException("build, run, desktop, image, check, test-system 중 동작을 지정하세요");
        String چار = 인수[0];
        if (!Arrays.asList("build","run","desktop","image","check","test-system").contains(چار)) throw new IllegalArgumentException("알 수 없는 چار");
        Path 기준 = Paths.get(System.getProperty("worldos.edition.root")).toAbsolutePath().normalize();
        Map<String,Object> امستنې = (Map<String,Object>)new 자료해석기(Files.readString(기준.resolve("native.json"),StandardCharsets.UTF_8)).لوستل();
        Path سرچینه_ونه = 내부경로(기준,(String)امستنې.get("source")), نوغی_ارزښت = 내부경로(سرچینه_ونه,(String)امستنې.get("native"));
        List<String> 소유파일들 = (List<String>)(List<?>)امستنې.get("owned_files");
        for (String نوم : 소유파일들) if (!Files.isRegularFile(내부경로(سرچینه_ونه,نوم))) throw new IOException("سرچینه_ونه 없음: " + نوم);
        if (چار.equals("check")) { System.out.println(امستنې.get("country") + " " + امستنې.get("language") + " 독립 سرچینه_ونه 확인 완료"); return; }
        String 자원상대 = (String)امستنې.getOrDefault("resource_root", ".");
        if (!자원상대.equals(".") && !자원상대.equals("..")) throw new IllegalArgumentException("의존성 기준 يونلور تېروتنه");
        Path سرچينه_ارزښت = 기준.resolve(자원상대).normalize(); Path ارشیف_ارزښت = سرچينه_ارزښت.resolve("native-vendor.tar.gz");
        String 기대해시 = (String)امستنې.get("vendor_sha256");
        if (!해시(ارشیف_ارزښت).equals(기대해시)) throw new IOException("의존성 SHA-256 불일치");
        Path 표식 = سرچینه_ونه.resolve(".vendor-sha256");
        if (!Files.isRegularFile(표식) || !Files.readString(표식).trim().equals(기대해시)) { 풀기(ارشیف_ارزښت, سرچینه_ونه); Files.writeString(표식,기대해시 + "\n"); }
        Map<String,String> 환경 = new HashMap<>(System.getenv());
        Path ipConfig = null;
        if (환경.containsKey("IP_CONFIG")) ipConfig = Paths.get(환경.get("IP_CONFIG")).toAbsolutePath().normalize();
        else for (Path parent = 기준; parent != null; parent = parent.getParent()) {
            if (Files.isRegularFile(parent.resolve("ip.conf"))) { ipConfig = parent.resolve("ip.conf"); break; }
        }
        if (ipConfig == null) ipConfig = سرچینه_ونه.resolve("ip.conf");
        if (!Files.isRegularFile(ipConfig)) throw new IOException("Missing ip.conf: " + ipConfig);
        환경.put("IP_CONFIG", ipConfig.toString());
        if (Arrays.asList("run","desktop","test-system").contains(چار) && !환경.containsKey("QEMU_AARCH64")) {
            Path 실행기 = سرچينه_ارزښت.resolve("host/qemu"), 실행기표식 = سرچينه_ارزښت.resolve("host/.qemu-sha256");
            String 실행기해시 = (String)امستنې.get("qemu_sha256");
            if (!Files.isRegularFile(실행기) || !Files.isRegularFile(실행기표식) || !Files.readString(실행기표식).trim().equals(실행기해시)) {
                Path 실행기압축 = سرچينه_ارزښت.resolve("qemu-host.tar.gz"); if (!해시(실행기압축).equals(실행기해시)) throw new IOException("QEMU SHA-256 불일치");
                풀기(실행기압축,سرچينه_ارزښت.resolve("host")); Files.writeString(실행기표식,실행기해시 + "\n");
            }
            환경.put("QEMU_AARCH64",실행기.toString());
        }
        MessageDigest 계산 = MessageDigest.getInstance("SHA-256"); Collections.sort(소유파일들);
        for (String نوم : 소유파일들) { 계산.update(نوم.getBytes(StandardCharsets.UTF_8)); 계산.update(Files.readAllBytes(내부경로(سرچینه_ونه,نوم))); }
        계산.update("ip.conf\0".getBytes(StandardCharsets.UTF_8)); 계산.update(Files.readAllBytes(ipConfig));
        String 소스해시 = 해시글(계산.digest()); Path 빌드표식 = نوغی_ارزښت.resolve("build/worldos-source.sha256");
        if (چار.equals("build") || !Files.isRegularFile(빌드표식) || !Files.readString(빌드표식).trim().equals(소스해시)) {
            호출(نوغی_ارزښت,내부경로(نوغی_ارزښت,(String)امستنې.get("builder")),Collections.emptyList(),환경);
            Files.writeString(빌드표식,소스해시 + "\n");
        }
        List<String> 추가인수 = new ArrayList<>(Arrays.asList(인수).subList(1,인수.length));
        if (چار.equals("run") || چار.equals("desktop")) {
            if (چار.equals("desktop")) 추가인수.add(0,"--desktop");
            호출(نوغی_ارزښت,내부경로(نوغی_ارزښت,(String)امستنې.get("runner")),추가인수,환경);
        } else if (چار.equals("image")) 호출(نوغی_ارزښت,내부경로(نوغی_ارزښت,(String)امستنې.get("image_builder")),추가인수,환경);
        else if (چار.equals("test-system")) {
            추가인수.add(0,기준.toString()); 추가인수.add(0,"--edition");
            호출(نوغی_ارزښت,내부경로(نوغی_ارزښت,(String)امستنې.get("system_tester")),추가인수,환경);
        }
    }
}
