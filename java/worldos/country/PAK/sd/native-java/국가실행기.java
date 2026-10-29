// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.security.MessageDigest;
import java.util.*;

/** 독립 국가판의 의존성 검사·복원·گڏ_ڪريو_سسٽم·실행을 맡는 مهمان Java اوزار. */
public final class 국가실행기 {
    static final class 자료해석기 {
        final String ماخذ; int 위치;
        자료해석기(String متن) { ماخذ = متن; }
        void 빈칸() { while (위치 < ماخذ.length() && Character.isWhitespace(ماخذ.charAt(위치))) 위치++; }
        Object 읽기() {
            빈칸(); char ڪريڪٽر_قدر = ماخذ.charAt(위치++);
            if (ڪريڪٽر_قدر == '{') {
                Map<String,Object> 결과 = new LinkedHashMap<>(); 빈칸();
                if (ماخذ.charAt(위치) == '}') { 위치++; return 결과; }
                while (true) {
                    String نالو = (String)읽기(); 빈칸(); if (ماخذ.charAt(위치++) != ':') throw new IllegalArgumentException("ڪوائف حد_مقرر_ڪرڻ_وارو_قدر نقص");
                    결과.put(نالو, 읽기()); 빈칸(); char حد_مقرر_ڪرڻ_وارو_قدر = ماخذ.charAt(위치++);
                    if (حد_مقرر_ڪرڻ_وارو_قدر == '}') return 결과; if (حد_مقرر_ڪرڻ_وارو_قدر != ',') throw new IllegalArgumentException("ڪوائف حد_مقرر_ڪرڻ_وارو_قدر نقص");
                }
            }
            if (ڪريڪٽر_قدر == '[') {
                List<Object> 결과 = new ArrayList<>(); 빈칸();
                if (ماخذ.charAt(위치) == ']') { 위치++; return 결과; }
                while (true) {
                    결과.add(읽기()); 빈칸(); char حد_مقرر_ڪرڻ_وارو_قدر = ماخذ.charAt(위치++);
                    if (حد_مقرر_ڪرڻ_وارو_قدر == ']') return 결과; if (حد_مقرر_ڪرڻ_وارو_قدر != ',') throw new IllegalArgumentException("ڪوائف حد_مقرر_ڪرڻ_وارو_قدر نقص");
                }
            }
            if (ڪريڪٽر_قدر == '"') {
                StringBuilder 결과 = new StringBuilder();
                while (true) {
                    char 다음 = ماخذ.charAt(위치++); if (다음 == '"') return 결과.toString();
                    if (다음 == '\\') {
                        다음 = ماخذ.charAt(위치++);
                        if (다음 == 'u') { 결과.append((char)Integer.parseInt(ماخذ.substring(위치, 위치 + 4),16)); 위치 += 4; continue; }
                        if (다음 == 'n') 다음 = '\n'; else if (다음 == 'r') 다음 = '\r'; else if (다음 == 't') 다음 = '\t';
                        else if (다음 == 'b') 다음 = '\b'; else if (다음 == 'f') 다음 = '\f';
                        else if (다음 != '"' && 다음 != '\\' && 다음 != '/') throw new IllegalArgumentException("문자 이스케이프 نقص");
                    }
                    결과.append(다음);
                }
            }
            int هلائڻ = 위치 - 1;
            while (위치 < ماخذ.length() && ",]} \t\r\n".indexOf(ماخذ.charAt(위치)) < 0) 위치++;
            String قدر = ماخذ.substring(هلائڻ, 위치);
            if (قدر.equals("true")) return Boolean.TRUE; if (قدر.equals("false")) return Boolean.FALSE; if (قدر.equals("null")) return null;
            return Double.valueOf(قدر);
        }
    }
    static String هيش_فائل(Path راههه) throws Exception {
        MessageDigest 계산 = MessageDigest.getInstance("SHA-256"); byte[] ڪوائف = new byte[1024 * 1024];
        try (InputStream 입력 = Files.newInputStream(راههه)) { for (int لمبائي_قدر; (لمبائي_قدر = 입력.read(ڪوائف)) >= 0;) 계산.update(ڪوائف,0,لمبائي_قدر); }
        return هيش_متن(계산.digest());
    }
    static String هيش_متن(byte[] ڪوائف) {
        StringBuilder متن = new StringBuilder(); for (byte قدر : ڪوائف) متن.append(String.format(Locale.ROOT,"%02x",قدر & 255)); return متن.toString();
    }
    static Path 내부경로(Path 기준, String نالو) {
        Path 결과 = 기준.resolve(نالو).normalize();
        if (نالو.isEmpty() || Paths.get(نالو).isAbsolute() || !결과.startsWith(기준) || نالو.indexOf('\\') >= 0)
            throw new IllegalArgumentException("범위를 벗어난 راههه: " + نالو);
        for (Path 부분 : Paths.get(نالو)) if (부분.toString().equals("..")) throw new IllegalArgumentException("상위 راههه 금지: " + نالو);
        for (Path 현재 = 결과; 현재 != null && 현재.startsWith(기준); 현재 = 현재.getParent())
            if (Files.isSymbolicLink(현재)) throw new IllegalArgumentException("의존성 경로의 링크 금지: " + نالو);
        return 결과;
    }
    static String 명령출력(List<String> حڪم) throws Exception {
        Process عمل_قدر = new ProcessBuilder(حڪم).redirectError(ProcessBuilder.Redirect.INHERIT).start();
        String 결과 = new String(عمل_قدر.getInputStream().readAllBytes(),StandardCharsets.UTF_8);
        if (عمل_قدر.waitFor() != 0) throw new IOException("حڪم ناڪامي_قدر: " + حڪم.get(0)); return 결과;
    }
    static void ٻاهر_ڪڍڻ(Path محفوظ_قدر, Path منزل_مقصود_قدر) throws Exception {
        for (String نالو : 명령출력(Arrays.asList("tar","-tzf",محفوظ_قدر.toString())).split("\n")) 내부경로(منزل_مقصود_قدر, نالو);
        for (String لڪير : 명령출력(Arrays.asList("tar","-tvzf",محفوظ_قدر.toString())).split("\n"))
            if (!لڪير.isEmpty() && لڪير.charAt(0) != '-' && لڪير.charAt(0) != 'd') throw new IOException("외부 링크 또는 특수 파일을 포함한 의존성");
        Files.createDirectories(منزل_مقصود_قدر);
        int حالت_قدر = new ProcessBuilder("tar","--no-same-owner","--no-same-permissions","-xzf",محفوظ_قدر.toString(),"-C",منزل_مقصود_قدر.toString()).inheritIO().start().waitFor();
        if (حالت_قدر != 0) throw new IOException("의존성 محفوظ_قدر جاري_ڪريو_ذخيرو ناڪامي_قدر");
    }
    static void 호출(Path 작업경로, Path اوزار, List<String> 인수, Map<String,String> 환경) throws Exception {
        List<String> حڪم = new ArrayList<>(Arrays.asList("python3", اوزار.toString())); حڪم.addAll(인수);
        ProcessBuilder تعميل_ڪرڻ_حڪم = new ProcessBuilder(حڪم).directory(작업경로.toFile()).inheritIO(); تعميل_ڪرڻ_حڪم.environment().putAll(환경);
        int حالت_قدر = تعميل_ڪرڻ_حڪم.start().waitFor(); if (حالت_قدر != 0) throw new IOException("اوزار ناڪامي_قدر: " + اوزار + " (" + حالت_قدر + ")");
    }
    @SuppressWarnings("unchecked")
    public static void main(String[] 인수) throws Exception {
        if (인수.length < 1) throw new IllegalArgumentException("build, run, desktop, image, check, test-system 중 동작을 지정하세요");
        String عمل = 인수[0];
        if (!Arrays.asList("build","run","desktop","image","check","test-system").contains(عمل)) throw new IllegalArgumentException("알 수 없는 عمل");
        Path 기준 = Paths.get(System.getProperty("worldos.edition.root")).toAbsolutePath().normalize();
        Map<String,Object> سيٽنگون = (Map<String,Object>)new 자료해석기(Files.readString(기준.resolve("native.json"),StandardCharsets.UTF_8)).읽기();
        Path ماخذ_شجرو = 내부경로(기준,(String)سيٽنگون.get("source")), ڪرنل_قدر = 내부경로(ماخذ_شجرو,(String)سيٽنگون.get("native"));
        List<String> 소유파일들 = (List<String>)(List<?>)سيٽنگون.get("owned_files");
        for (String نالو : 소유파일들) if (!Files.isRegularFile(내부경로(ماخذ_شجرو,نالو))) throw new IOException("ماخذ_شجرو 없음: " + نالو);
        if (عمل.equals("check")) { System.out.println(سيٽنگون.get("country") + " " + سيٽنگون.get("language") + " 독립 ماخذ_شجرو تصديق_ڪريو 완료"); return; }
        String 자원상대 = (String)سيٽنگون.getOrDefault("resource_root", ".");
        if (!자원상대.equals(".") && !자원상대.equals("..")) throw new IllegalArgumentException("의존성 기준 راههه نقص");
        Path ذريعو_قدر = 기준.resolve(자원상대).normalize(); Path محفوظ_قدر = ذريعو_قدر.resolve("native-vendor.tar.gz");
        String 기대해시 = (String)سيٽنگون.get("vendor_sha256");
        if (!هيش_فائل(محفوظ_قدر).equals(기대해시)) throw new IOException("의존성 SHA-256 불일치");
        Path 표식 = ماخذ_شجرو.resolve(".vendor-sha256");
        if (!Files.isRegularFile(표식) || !Files.readString(표식).trim().equals(기대해시)) { ٻاهر_ڪڍڻ(محفوظ_قدر, ماخذ_شجرو); Files.writeString(표식,기대해시 + "\n"); }
        Map<String,String> 환경 = new HashMap<>(System.getenv());
        Path ipConfig = null;
        if (환경.containsKey("IP_CONFIG")) ipConfig = Paths.get(환경.get("IP_CONFIG")).toAbsolutePath().normalize();
        else for (Path parent = 기준; parent != null; parent = parent.getParent()) {
            if (Files.isRegularFile(parent.resolve("ip.conf"))) { ipConfig = parent.resolve("ip.conf"); break; }
        }
        if (ipConfig == null) ipConfig = ماخذ_شجرو.resolve("ip.conf");
        if (!Files.isRegularFile(ipConfig)) throw new IOException("Missing ip.conf: " + ipConfig);
        환경.put("IP_CONFIG", ipConfig.toString());
        if (Arrays.asList("run","desktop","test-system").contains(عمل) && !환경.containsKey("QEMU_AARCH64")) {
            Path ائپ_ائپ_ڊرائر = ذريعو_قدر.resolve("host/qemu"), 실행기표식 = ذريعو_قدر.resolve("host/.qemu-sha256");
            String ائپ_ڊرائر_هيش = (String)سيٽنگون.get("qemu_sha256");
            if (!Files.isRegularFile(ائپ_ائپ_ڊرائر) || !Files.isRegularFile(실행기표식) || !Files.readString(실행기표식).trim().equals(ائپ_ڊرائر_هيش)) {
                Path ائپ_ڊرائر_محفوظ = ذريعو_قدر.resolve("qemu-host.tar.gz"); if (!هيش_فائل(ائپ_ڊرائر_محفوظ).equals(ائپ_ڊرائر_هيش)) throw new IOException("QEMU SHA-256 불일치");
                ٻاهر_ڪڍڻ(ائپ_ڊرائر_محفوظ,ذريعو_قدر.resolve("host")); Files.writeString(실행기표식,ائپ_ڊرائر_هيش + "\n");
            }
            환경.put("QEMU_AARCH64",ائپ_ائپ_ڊرائر.toString());
        }
        MessageDigest 계산 = MessageDigest.getInstance("SHA-256"); Collections.sort(소유파일들);
        for (String نالو : 소유파일들) { 계산.update(نالو.getBytes(StandardCharsets.UTF_8)); 계산.update(Files.readAllBytes(내부경로(ماخذ_شجرو,نالو))); }
        계산.update("ip.conf\0".getBytes(StandardCharsets.UTF_8)); 계산.update(Files.readAllBytes(ipConfig));
        String ماخذ_هيش = هيش_متن(계산.digest()); Path 빌드표식 = ڪرنل_قدر.resolve("build/worldos-source.sha256");
        if (عمل.equals("build") || !Files.isRegularFile(빌드표식) || !Files.readString(빌드표식).trim().equals(ماخذ_هيش)) {
            호출(ڪرنل_قدر,내부경로(ڪرنل_قدر,(String)سيٽنگون.get("builder")),Collections.emptyList(),환경);
            Files.writeString(빌드표식,ماخذ_هيش + "\n");
        }
        List<String> 추가인수 = new ArrayList<>(Arrays.asList(인수).subList(1,인수.length));
        if (عمل.equals("run") || عمل.equals("desktop")) {
            if (عمل.equals("desktop")) 추가인수.add(0,"--desktop");
            호출(ڪرنل_قدر,내부경로(ڪرنل_قدر,(String)سيٽنگون.get("runner")),추가인수,환경);
        } else if (عمل.equals("image")) 호출(ڪرنل_قدر,내부경로(ڪرنل_قدر,(String)سيٽنگون.get("image_builder")),추가인수,환경);
        else if (عمل.equals("test-system")) {
            추가인수.add(0,기준.toString()); 추가인수.add(0,"--edition");
            호출(ڪرنل_قدر,내부경로(ڪرنل_قدر,(String)سيٽنگون.get("system_tester")),추가인수,환경);
        }
    }
}
