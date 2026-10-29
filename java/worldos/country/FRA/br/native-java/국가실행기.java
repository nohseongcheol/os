// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.security.MessageDigest;
import java.util.*;

/** 독립 국가판의 의존성 검사·복원·빌드·실행을 맡는 호스트 Java 도구. */
public final class 국가실행기 {
    static final class 자료해석기 {
        final String Tarzh; int Lec_hiadur;
        자료해석기(String Testenn) { Tarzh = Testenn; }
        void 빈칸() { while (Lec_hiadur < Tarzh.length() && Character.isWhitespace(Tarzh.charAt(Lec_hiadur))) Lec_hiadur++; }
        Object Lenn() {
            빈칸(); char 글자 = Tarzh.charAt(Lec_hiadur++);
            if (글자 == '{') {
                Map<String,Object> 결과 = new LinkedHashMap<>(); 빈칸();
                if (Tarzh.charAt(Lec_hiadur) == '}') { Lec_hiadur++; return 결과; }
                while (true) {
                    String Anv = (String)Lenn(); 빈칸(); if (Tarzh.charAt(Lec_hiadur++) != ':') throw new IllegalArgumentException("자료 구분 Fazi");
                    결과.put(Anv, Lenn()); 빈칸(); char 구분 = Tarzh.charAt(Lec_hiadur++);
                    if (구분 == '}') return 결과; if (구분 != ',') throw new IllegalArgumentException("자료 구분 Fazi");
                }
            }
            if (글자 == '[') {
                List<Object> 결과 = new ArrayList<>(); 빈칸();
                if (Tarzh.charAt(Lec_hiadur) == ']') { Lec_hiadur++; return 결과; }
                while (true) {
                    결과.add(Lenn()); 빈칸(); char 구분 = Tarzh.charAt(Lec_hiadur++);
                    if (구분 == ']') return 결과; if (구분 != ',') throw new IllegalArgumentException("자료 구분 Fazi");
                }
            }
            if (글자 == '"') {
                StringBuilder 결과 = new StringBuilder();
                while (true) {
                    char 다음 = Tarzh.charAt(Lec_hiadur++); if (다음 == '"') return 결과.toString();
                    if (다음 == '\\') {
                        다음 = Tarzh.charAt(Lec_hiadur++);
                        if (다음 == 'u') { 결과.append((char)Integer.parseInt(Tarzh.substring(Lec_hiadur, Lec_hiadur + 4),16)); Lec_hiadur += 4; continue; }
                        if (다음 == 'n') 다음 = '\n'; else if (다음 == 'r') 다음 = '\r'; else if (다음 == 't') 다음 = '\t';
                        else if (다음 == 'b') 다음 = '\b'; else if (다음 == 'f') 다음 = '\f';
                        else if (다음 != '"' && 다음 != '\\' && 다음 != '/') throw new IllegalArgumentException("문자 이스케이프 Fazi");
                    }
                    결과.append(다음);
                }
            }
            int Seveniñ_2 = Lec_hiadur - 1;
            while (Lec_hiadur < Tarzh.length() && ",]} \t\r\n".indexOf(Tarzh.charAt(Lec_hiadur)) < 0) Lec_hiadur++;
            String 값 = Tarzh.substring(Seveniñ_2, Lec_hiadur);
            if (값.equals("true")) return Boolean.TRUE; if (값.equals("false")) return Boolean.FALSE; if (값.equals("null")) return null;
            return Double.valueOf(값);
        }
    }
    static String 해시(Path TREUG) throws Exception {
        MessageDigest 계산 = MessageDigest.getInstance("SHA-256"); byte[] 자료 = new byte[1024 * 1024];
        try (InputStream 입력 = Files.newInputStream(TREUG)) { for (int 길이; (길이 = 입력.read(자료)) >= 0;) 계산.update(자료,0,길이); }
        return 해시글(계산.digest());
    }
    static String 해시글(byte[] 자료) {
        StringBuilder Testenn = new StringBuilder(); for (byte 값 : 자료) Testenn.append(String.format(Locale.ROOT,"%02x",값 & 255)); return Testenn.toString();
    }
    static Path 내부경로(Path 기준, String Anv) {
        Path 결과 = 기준.resolve(Anv).normalize();
        if (Anv.isEmpty() || Paths.get(Anv).isAbsolute() || !결과.startsWith(기준) || Anv.indexOf('\\') >= 0)
            throw new IllegalArgumentException("범위를 벗어난 TREUG: " + Anv);
        for (Path 부분 : Paths.get(Anv)) if (부분.toString().equals("..")) throw new IllegalArgumentException("상위 TREUG 금지: " + Anv);
        for (Path 현재 = 결과; 현재 != null && 현재.startsWith(기준); 현재 = 현재.getParent())
            if (Files.isSymbolicLink(현재)) throw new IllegalArgumentException("의존성 경로의 링크 금지: " + Anv);
        return 결과;
    }
    static String 명령출력(List<String> Arc_had) throws Exception {
        Process 과정 = new ProcessBuilder(Arc_had).redirectError(ProcessBuilder.Redirect.INHERIT).start();
        String 결과 = new String(과정.getInputStream().readAllBytes(),StandardCharsets.UTF_8);
        if (과정.waitFor() != 0) throw new IOException("Arc_had 실패: " + Arc_had.get(0)); return 결과;
    }
    static void 풀기(Path 압축, Path 목적) throws Exception {
        for (String Anv : 명령출력(Arrays.asList("tar","-tzf",압축.toString())).split("\n")) 내부경로(목적, Anv);
        for (String 줄 : 명령출력(Arrays.asList("tar","-tvzf",압축.toString())).split("\n"))
            if (!줄.isEmpty() && 줄.charAt(0) != '-' && 줄.charAt(0) != 'd') throw new IOException("외부 링크 또는 특수 파일을 포함한 의존성");
        Files.createDirectories(목적);
        int 상태 = new ProcessBuilder("tar","--no-same-owner","--no-same-permissions","-xzf",압축.toString(),"-C",목적.toString()).inheritIO().start().waitFor();
        if (상태 != 0) throw new IOException("의존성 압축 해제 실패");
    }
    static void 호출(Path 작업경로, Path 도구, List<String> Arventennoù, Map<String,String> 환경) throws Exception {
        List<String> Arc_had = new ArrayList<>(Arrays.asList("python3", 도구.toString())); Arc_had.addAll(Arventennoù);
        ProcessBuilder 실행 = new ProcessBuilder(Arc_had).directory(작업경로.toFile()).inheritIO(); 실행.environment().putAll(환경);
        int 상태 = 실행.start().waitFor(); if (상태 != 0) throw new IOException("도구 실패: " + 도구 + " (" + 상태 + ")");
    }
    @SuppressWarnings("unchecked")
    public static void main(String[] Arventennoù) throws Exception {
        if (Arventennoù.length < 1) throw new IllegalArgumentException("build, run, desktop, image, check, test-system 중 동작을 지정하세요");
        String Gwezhiad = Arventennoù[0];
        if (!Arrays.asList("build","run","desktop","image","check","test-system").contains(Gwezhiad)) throw new IllegalArgumentException("알 수 없는 Gwezhiad");
        Path 기준 = Paths.get(System.getProperty("worldos.edition.root")).toAbsolutePath().normalize();
        Map<String,Object> Arventennoù_2 = (Map<String,Object>)new 자료해석기(Files.readString(기준.resolve("native.json"),StandardCharsets.UTF_8)).Lenn();
        Path 소스 = 내부경로(기준,(String)Arventennoù_2.get("source")), 커널 = 내부경로(소스,(String)Arventennoù_2.get("native"));
        List<String> 소유파일들 = (List<String>)(List<?>)Arventennoù_2.get("owned_files");
        for (String Anv : 소유파일들) if (!Files.isRegularFile(내부경로(소스,Anv))) throw new IOException("소스 없음: " + Anv);
        if (Gwezhiad.equals("check")) { System.out.println(Arventennoù_2.get("country") + " " + Arventennoù_2.get("language") + " 독립 소스 확인 완료"); return; }
        String 자원상대 = (String)Arventennoù_2.getOrDefault("resource_root", ".");
        if (!자원상대.equals(".") && !자원상대.equals("..")) throw new IllegalArgumentException("의존성 기준 TREUG Fazi");
        Path 자원 = 기준.resolve(자원상대).normalize(); Path 압축 = 자원.resolve("native-vendor.tar.gz");
        String 기대해시 = (String)Arventennoù_2.get("vendor_sha256");
        if (!해시(압축).equals(기대해시)) throw new IOException("의존성 SHA-256 불일치");
        Path 표식 = 소스.resolve(".vendor-sha256");
        if (!Files.isRegularFile(표식) || !Files.readString(표식).trim().equals(기대해시)) { 풀기(압축, 소스); Files.writeString(표식,기대해시 + "\n"); }
        Map<String,String> 환경 = new HashMap<>(System.getenv());
        Path ipConfig = null;
        if (환경.containsKey("IP_CONFIG")) ipConfig = Paths.get(환경.get("IP_CONFIG")).toAbsolutePath().normalize();
        else for (Path parent = 기준; parent != null; parent = parent.getParent()) {
            if (Files.isRegularFile(parent.resolve("ip.conf"))) { ipConfig = parent.resolve("ip.conf"); break; }
        }
        if (ipConfig == null) ipConfig = 소스.resolve("ip.conf");
        if (!Files.isRegularFile(ipConfig)) throw new IOException("Missing ip.conf: " + ipConfig);
        환경.put("IP_CONFIG", ipConfig.toString());
        if (Arrays.asList("run","desktop","test-system").contains(Gwezhiad) && !환경.containsKey("QEMU_AARCH64")) {
            Path 실행기 = 자원.resolve("host/qemu"), 실행기표식 = 자원.resolve("host/.qemu-sha256");
            String 실행기해시 = (String)Arventennoù_2.get("qemu_sha256");
            if (!Files.isRegularFile(실행기) || !Files.isRegularFile(실행기표식) || !Files.readString(실행기표식).trim().equals(실행기해시)) {
                Path 실행기압축 = 자원.resolve("qemu-host.tar.gz"); if (!해시(실행기압축).equals(실행기해시)) throw new IOException("QEMU SHA-256 불일치");
                풀기(실행기압축,자원.resolve("host")); Files.writeString(실행기표식,실행기해시 + "\n");
            }
            환경.put("QEMU_AARCH64",실행기.toString());
        }
        MessageDigest 계산 = MessageDigest.getInstance("SHA-256"); Collections.sort(소유파일들);
        for (String Anv : 소유파일들) { 계산.update(Anv.getBytes(StandardCharsets.UTF_8)); 계산.update(Files.readAllBytes(내부경로(소스,Anv))); }
        계산.update("ip.conf\0".getBytes(StandardCharsets.UTF_8)); 계산.update(Files.readAllBytes(ipConfig));
        String 소스해시 = 해시글(계산.digest()); Path 빌드표식 = 커널.resolve("build/worldos-source.sha256");
        if (Gwezhiad.equals("build") || !Files.isRegularFile(빌드표식) || !Files.readString(빌드표식).trim().equals(소스해시)) {
            호출(커널,내부경로(커널,(String)Arventennoù_2.get("builder")),Collections.emptyList(),환경);
            Files.writeString(빌드표식,소스해시 + "\n");
        }
        List<String> 추가인수 = new ArrayList<>(Arrays.asList(Arventennoù).subList(1,Arventennoù.length));
        if (Gwezhiad.equals("run") || Gwezhiad.equals("desktop")) {
            if (Gwezhiad.equals("desktop")) 추가인수.add(0,"--desktop");
            호출(커널,내부경로(커널,(String)Arventennoù_2.get("runner")),추가인수,환경);
        } else if (Gwezhiad.equals("image")) 호출(커널,내부경로(커널,(String)Arventennoù_2.get("image_builder")),추가인수,환경);
        else if (Gwezhiad.equals("test-system")) {
            추가인수.add(0,기준.toString()); 추가인수.add(0,"--edition");
            호출(커널,내부경로(커널,(String)Arventennoù_2.get("system_tester")),추가인수,환경);
        }
    }
}
