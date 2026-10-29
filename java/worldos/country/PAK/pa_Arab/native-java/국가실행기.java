// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.security.MessageDigest;
import java.util.*;

/** 독립 국가판의 의존성 검사·복원·بلڈ_نظام·실행을 맡는 مہمان_b78e430d Java اوزار. */
public final class 국가실행기 {
    static final class 자료해석기 {
        final String ماخذ; int 위치;
        자료해석기(String متن) { ماخذ = متن; }
        void 빈칸() { while (위치 < ماخذ.length() && Character.isWhitespace(ماخذ.charAt(위치))) 위치++; }
        Object 읽기() {
            빈칸(); char کریکٹر_قدر = ماخذ.charAt(위치++);
            if (کریکٹر_قدر == '{') {
                Map<String,Object> 결과 = new LinkedHashMap<>(); 빈칸();
                if (ماخذ.charAt(위치) == '}') { 위치++; return 결과; }
                while (true) {
                    String ناں = (String)읽기(); 빈칸(); if (ماخذ.charAt(위치++) != ':') throw new IllegalArgumentException("کوائف حد_بندی_کرنڑ_آلا_قدر نقص");
                    결과.put(ناں, 읽기()); 빈칸(); char حد_بندی_کرنڑ_آلا_قدر = ماخذ.charAt(위치++);
                    if (حد_بندی_کرنڑ_آلا_قدر == '}') return 결과; if (حد_بندی_کرنڑ_آلا_قدر != ',') throw new IllegalArgumentException("کوائف حد_بندی_کرنڑ_آلا_قدر نقص");
                }
            }
            if (کریکٹر_قدر == '[') {
                List<Object> 결과 = new ArrayList<>(); 빈칸();
                if (ماخذ.charAt(위치) == ']') { 위치++; return 결과; }
                while (true) {
                    결과.add(읽기()); 빈칸(); char حد_بندی_کرنڑ_آلا_قدر = ماخذ.charAt(위치++);
                    if (حد_بندی_کرنڑ_آلا_قدر == ']') return 결과; if (حد_بندی_کرنڑ_آلا_قدر != ',') throw new IllegalArgumentException("کوائف حد_بندی_کرنڑ_آلا_قدر نقص");
                }
            }
            if (کریکٹر_قدر == '"') {
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
            int چلاؤ = 위치 - 1;
            while (위치 < ماخذ.length() && ",]} \t\r\n".indexOf(ماخذ.charAt(위치)) < 0) 위치++;
            String قدر = ماخذ.substring(چلاؤ, 위치);
            if (قدر.equals("true")) return Boolean.TRUE; if (قدر.equals("false")) return Boolean.FALSE; if (قدر.equals("null")) return null;
            return Double.valueOf(قدر);
        }
    }
    static String ہیش_فائل(Path راہ) throws Exception {
        MessageDigest 계산 = MessageDigest.getInstance("SHA-256"); byte[] کوائف = new byte[1024 * 1024];
        try (InputStream 입력 = Files.newInputStream(راہ)) { for (int لمبائی_قدر; (لمبائی_قدر = 입력.read(کوائف)) >= 0;) 계산.update(کوائف,0,لمبائی_قدر); }
        return ہیش_متن(계산.digest());
    }
    static String ہیش_متن(byte[] کوائف) {
        StringBuilder متن = new StringBuilder(); for (byte قدر : کوائف) متن.append(String.format(Locale.ROOT,"%02x",قدر & 255)); return متن.toString();
    }
    static Path 내부경로(Path 기준, String ناں) {
        Path 결과 = 기준.resolve(ناں).normalize();
        if (ناں.isEmpty() || Paths.get(ناں).isAbsolute() || !결과.startsWith(기준) || ناں.indexOf('\\') >= 0)
            throw new IllegalArgumentException("범위를 벗어난 راہ: " + ناں);
        for (Path 부분 : Paths.get(ناں)) if (부분.toString().equals("..")) throw new IllegalArgumentException("상위 راہ 금지: " + ناں);
        for (Path 현재 = 결과; 현재 != null && 현재.startsWith(기준); 현재 = 현재.getParent())
            if (Files.isSymbolicLink(현재)) throw new IllegalArgumentException("의존성 경로의 링크 금지: " + ناں);
        return 결과;
    }
    static String 명령출력(List<String> حکم) throws Exception {
        Process عمل_قدر = new ProcessBuilder(حکم).redirectError(ProcessBuilder.Redirect.INHERIT).start();
        String 결과 = new String(عمل_قدر.getInputStream().readAllBytes(),StandardCharsets.UTF_8);
        if (عمل_قدر.waitFor() != 0) throw new IOException("حکم ناکامی_قدر: " + حکم.get(0)); return 결과;
    }
    static void باہر_کھچو(Path محفوظہ_قدر, Path منزل_مقصود_قدر) throws Exception {
        for (String ناں : 명령출력(Arrays.asList("tar","-tzf",محفوظہ_قدر.toString())).split("\n")) 내부경로(منزل_مقصود_قدر, ناں);
        for (String لائن : 명령출력(Arrays.asList("tar","-tvzf",محفوظہ_قدر.toString())).split("\n"))
            if (!لائن.isEmpty() && لائن.charAt(0) != '-' && لائن.charAt(0) != 'd') throw new IOException("외부 링크 또는 특수 파일을 포함한 의존성");
        Files.createDirectories(منزل_مقصود_قدر);
        int حالت_قدر = new ProcessBuilder("tar","--no-same-owner","--no-same-permissions","-xzf",محفوظہ_قدر.toString(),"-C",منزل_مقصود_قدر.toString()).inheritIO().start().waitFor();
        if (حالت_قدر != 0) throw new IOException("의존성 محفوظہ_قدر اجراء_ذخیرہ ناکامی_قدر");
    }
    static void 호출(Path 작업경로, Path اوزار, List<String> 인수, Map<String,String> 환경) throws Exception {
        List<String> حکم = new ArrayList<>(Arrays.asList("python3", اوزار.toString())); حکم.addAll(인수);
        ProcessBuilder نفاذ_کرو_حکم = new ProcessBuilder(حکم).directory(작업경로.toFile()).inheritIO(); نفاذ_کرو_حکم.environment().putAll(환경);
        int حالت_قدر = نفاذ_کرو_حکم.start().waitFor(); if (حالت_قدر != 0) throw new IOException("اوزار ناکامی_قدر: " + اوزار + " (" + حالت_قدر + ")");
    }
    @SuppressWarnings("unchecked")
    public static void main(String[] 인수) throws Exception {
        if (인수.length < 1) throw new IllegalArgumentException("build, run, desktop, image, check, test-system 중 동작을 지정하세요");
        String کم = 인수[0];
        if (!Arrays.asList("build","run","desktop","image","check","test-system").contains(کم)) throw new IllegalArgumentException("알 수 없는 کم");
        Path 기준 = Paths.get(System.getProperty("worldos.edition.root")).toAbsolutePath().normalize();
        Map<String,Object> سیٹنگاں = (Map<String,Object>)new 자료해석기(Files.readString(기준.resolve("native.json"),StandardCharsets.UTF_8)).읽기();
        Path ماخذ_شجرہ = 내부경로(기준,(String)سیٹنگاں.get("source")), کرنل_قدر = 내부경로(ماخذ_شجرہ,(String)سیٹنگاں.get("native"));
        List<String> 소유파일들 = (List<String>)(List<?>)سیٹنگاں.get("owned_files");
        for (String ناں : 소유파일들) if (!Files.isRegularFile(내부경로(ماخذ_شجرہ,ناں))) throw new IOException("ماخذ_شجرہ 없음: " + ناں);
        if (کم.equals("check")) { System.out.println(سیٹنگاں.get("country") + " " + سیٹنگاں.get("language") + " 독립 ماخذ_شجرہ تصدیق_کرو 완료"); return; }
        String 자원상대 = (String)سیٹنگاں.getOrDefault("resource_root", ".");
        if (!자원상대.equals(".") && !자원상대.equals("..")) throw new IllegalArgumentException("의존성 기준 راہ نقص");
        Path ذریعہ_قدر = 기준.resolve(자원상대).normalize(); Path محفوظہ_قدر = ذریعہ_قدر.resolve("native-vendor.tar.gz");
        String 기대해시 = (String)سیٹنگاں.get("vendor_sha256");
        if (!ہیش_فائل(محفوظہ_قدر).equals(기대해시)) throw new IOException("의존성 SHA-256 불일치");
        Path 표식 = ماخذ_شجرہ.resolve(".vendor-sha256");
        if (!Files.isRegularFile(표식) || !Files.readString(표식).trim().equals(기대해시)) { باہر_کھچو(محفوظہ_قدر, ماخذ_شجرہ); Files.writeString(표식,기대해시 + "\n"); }
        Map<String,String> 환경 = new HashMap<>(System.getenv());
        Path ipConfig = null;
        if (환경.containsKey("IP_CONFIG")) ipConfig = Paths.get(환경.get("IP_CONFIG")).toAbsolutePath().normalize();
        else for (Path parent = 기준; parent != null; parent = parent.getParent()) {
            if (Files.isRegularFile(parent.resolve("ip.conf"))) { ipConfig = parent.resolve("ip.conf"); break; }
        }
        if (ipConfig == null) ipConfig = ماخذ_شجرہ.resolve("ip.conf");
        if (!Files.isRegularFile(ipConfig)) throw new IOException("Missing ip.conf: " + ipConfig);
        환경.put("IP_CONFIG", ipConfig.toString());
        if (Arrays.asList("run","desktop","test-system").contains(کم) && !환경.containsKey("QEMU_AARCH64")) {
            Path ایپ_عملے_دا_رکن = ذریعہ_قدر.resolve("host/qemu"), 실행기표식 = ذریعہ_قدر.resolve("host/.qemu-sha256");
            String عملے_دا_رکن_ہیش = (String)سیٹنگاں.get("qemu_sha256");
            if (!Files.isRegularFile(ایپ_عملے_دا_رکن) || !Files.isRegularFile(실행기표식) || !Files.readString(실행기표식).trim().equals(عملے_دا_رکن_ہیش)) {
                Path عملے_دا_رکن_محفوظہ = ذریعہ_قدر.resolve("qemu-host.tar.gz"); if (!ہیش_فائل(عملے_دا_رکن_محفوظہ).equals(عملے_دا_رکن_ہیش)) throw new IOException("QEMU SHA-256 불일치");
                باہر_کھچو(عملے_دا_رکن_محفوظہ,ذریعہ_قدر.resolve("host")); Files.writeString(실행기표식,عملے_دا_رکن_ہیش + "\n");
            }
            환경.put("QEMU_AARCH64",ایپ_عملے_دا_رکن.toString());
        }
        MessageDigest 계산 = MessageDigest.getInstance("SHA-256"); Collections.sort(소유파일들);
        for (String ناں : 소유파일들) { 계산.update(ناں.getBytes(StandardCharsets.UTF_8)); 계산.update(Files.readAllBytes(내부경로(ماخذ_شجرہ,ناں))); }
        계산.update("ip.conf\0".getBytes(StandardCharsets.UTF_8)); 계산.update(Files.readAllBytes(ipConfig));
        String ماخذ_ہیش = ہیش_متن(계산.digest()); Path 빌드표식 = کرنل_قدر.resolve("build/worldos-source.sha256");
        if (کم.equals("build") || !Files.isRegularFile(빌드표식) || !Files.readString(빌드표식).trim().equals(ماخذ_ہیش)) {
            호출(کرنل_قدر,내부경로(کرنل_قدر,(String)سیٹنگاں.get("builder")),Collections.emptyList(),환경);
            Files.writeString(빌드표식,ماخذ_ہیش + "\n");
        }
        List<String> 추가인수 = new ArrayList<>(Arrays.asList(인수).subList(1,인수.length));
        if (کم.equals("run") || کم.equals("desktop")) {
            if (کم.equals("desktop")) 추가인수.add(0,"--desktop");
            호출(کرنل_قدر,내부경로(کرنل_قدر,(String)سیٹنگاں.get("runner")),추가인수,환경);
        } else if (کم.equals("image")) 호출(کرنل_قدر,내부경로(کرنل_قدر,(String)سیٹنگاں.get("image_builder")),추가인수,환경);
        else if (کم.equals("test-system")) {
            추가인수.add(0,기준.toString()); 추가인수.add(0,"--edition");
            호출(کرنل_قدر,내부경로(کرنل_قدر,(String)سیٹنگاں.get("system_tester")),추가인수,환경);
        }
    }
}
