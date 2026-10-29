// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.security.MessageDigest;
import java.util.*;

/** 독립 국가판의 의존성 검사·복원·بلڈ_نظام·실행을 맡는 میزبان Java ٹولز. */
public final class 국가실행기 {
    static final class 자료해석기 {
        final String ماخذ_فائل; int مقام;
        자료해석기(String متن) { ماخذ_فائل = متن; }
        void 빈칸() { while (مقام < ماخذ_فائل.length() && Character.isWhitespace(ماخذ_فائل.charAt(مقام))) مقام++; }
        Object پڑھیں() {
            빈칸(); char کریکٹر_قدر = ماخذ_فائل.charAt(مقام++);
            if (کریکٹر_قدر == '{') {
                Map<String,Object> پیمائش = new LinkedHashMap<>(); 빈칸();
                if (ماخذ_فائل.charAt(مقام) == '}') { مقام++; return پیمائش; }
                while (true) {
                    String نام = (String)پڑھیں(); 빈칸(); if (ماخذ_فائل.charAt(مقام++) != ':') throw new IllegalArgumentException("کوائف تحدیدکار_قدر غلطی");
                    پیمائش.put(نام, پڑھیں()); 빈칸(); char تحدیدکار_قدر = ماخذ_فائل.charAt(مقام++);
                    if (تحدیدکار_قدر == '}') return پیمائش; if (تحدیدکار_قدر != ',') throw new IllegalArgumentException("کوائف تحدیدکار_قدر غلطی");
                }
            }
            if (کریکٹر_قدر == '[') {
                List<Object> پیمائش = new ArrayList<>(); 빈칸();
                if (ماخذ_فائل.charAt(مقام) == ']') { مقام++; return پیمائش; }
                while (true) {
                    پیمائش.add(پڑھیں()); 빈칸(); char تحدیدکار_قدر = ماخذ_فائل.charAt(مقام++);
                    if (تحدیدکار_قدر == ']') return پیمائش; if (تحدیدکار_قدر != ',') throw new IllegalArgumentException("کوائف تحدیدکار_قدر غلطی");
                }
            }
            if (کریکٹر_قدر == '"') {
                StringBuilder پیمائش = new StringBuilder();
                while (true) {
                    char اگلا_شے = ماخذ_فائل.charAt(مقام++); if (اگلا_شے == '"') return پیمائش.toString();
                    if (اگلا_شے == '\\') {
                        اگلا_شے = ماخذ_فائل.charAt(مقام++);
                        if (اگلا_شے == 'u') { پیمائش.append((char)Integer.parseInt(ماخذ_فائل.substring(مقام, مقام + 4),16)); مقام += 4; continue; }
                        if (اگلا_شے == 'n') اگلا_شے = '\n'; else if (اگلا_شے == 'r') اگلا_شے = '\r'; else if (اگلا_شے == 't') اگلا_شے = '\t';
                        else if (اگلا_شے == 'b') اگلا_شے = '\b'; else if (اگلا_شے == 'f') اگلا_شے = '\f';
                        else if (اگلا_شے != '"' && اگلا_شے != '\\' && اگلا_شے != '/') throw new IllegalArgumentException("문자 이스케이프 غلطی");
                    }
                    پیمائش.append(اگلا_شے);
                }
            }
            int چلائیں = مقام - 1;
            while (مقام < ماخذ_فائل.length() && ",]} \t\r\n".indexOf(ماخذ_فائل.charAt(مقام)) < 0) مقام++;
            String قدر = ماخذ_فائل.substring(چلائیں, مقام);
            if (قدر.equals("true")) return Boolean.TRUE; if (قدر.equals("false")) return Boolean.FALSE; if (قدر.equals("null")) return null;
            return Double.valueOf(قدر);
        }
    }
    static String ہيش_فائل(Path راستہ_2) throws Exception {
        MessageDigest 계산 = MessageDigest.getInstance("SHA-256"); byte[] کوائف = new byte[1024 * 1024];
        try (InputStream 입력 = Files.newInputStream(راستہ_2)) { for (int لمبا_ئی_قدر; (لمبا_ئی_قدر = 입력.read(کوائف)) >= 0;) 계산.update(کوائف,0,لمبا_ئی_قدر); }
        return ہيش_متن(계산.digest());
    }
    static String ہيش_متن(byte[] کوائف) {
        StringBuilder متن = new StringBuilder(); for (byte قدر : کوائف) متن.append(String.format(Locale.ROOT,"%02x",قدر & 255)); return متن.toString();
    }
    static Path 내부경로(Path عکس_ڈالنا_روٹ, String نام) {
        Path پیمائش = عکس_ڈالنا_روٹ.resolve(نام).normalize();
        if (نام.isEmpty() || Paths.get(نام).isAbsolute() || !پیمائش.startsWith(عکس_ڈالنا_روٹ) || نام.indexOf('\\') >= 0)
            throw new IllegalArgumentException("범위를 벗어난 راستہ_2: " + نام);
        for (Path 부분 : Paths.get(نام)) if (부분.toString().equals("..")) throw new IllegalArgumentException("상위 راستہ_2 금지: " + نام);
        for (Path 현재 = پیمائش; 현재 != null && 현재.startsWith(عکس_ڈالنا_روٹ); 현재 = 현재.getParent())
            if (Files.isSymbolicLink(현재)) throw new IllegalArgumentException("의존성 경로의 링크 금지: " + نام);
        return پیمائش;
    }
    static String 명령출력(List<String> حکم) throws Exception {
        Process عمل_قدر = new ProcessBuilder(حکم).redirectError(ProcessBuilder.Redirect.INHERIT).start();
        String پیمائش = new String(عمل_قدر.getInputStream().readAllBytes(),StandardCharsets.UTF_8);
        if (عمل_قدر.waitFor() != 0) throw new IOException("حکم ناکامی_قدر: " + حکم.get(0)); return پیمائش;
    }
    static void اخذ_کریں(Path محفوظ_قدر, Path منزل_مقصود_قدر) throws Exception {
        for (String نام : 명령출력(Arrays.asList("tar","-tzf",محفوظ_قدر.toString())).split("\n")) 내부경로(منزل_مقصود_قدر, نام);
        for (String اندراج_کی_سطر : 명령출력(Arrays.asList("tar","-tvzf",محفوظ_قدر.toString())).split("\n"))
            if (!اندراج_کی_سطر.isEmpty() && اندراج_کی_سطر.charAt(0) != '-' && اندراج_کی_سطر.charAt(0) != 'd') throw new IOException("외부 링크 또는 특수 파일을 포함한 의존성");
        Files.createDirectories(منزل_مقصود_قدر);
        int حالت_قدر = new ProcessBuilder("tar","--no-same-owner","--no-same-permissions","-xzf",محفوظ_قدر.toString(),"-C",منزل_مقصود_قدر.toString()).inheritIO().start().waitFor();
        if (حالت_قدر != 0) throw new IOException("의존성 محفوظ_قدر ریلیز_ذخیرہ ناکامی_قدر");
    }
    static void 호출(Path 작업경로, Path ٹولز, List<String> دلائل, Map<String,String> 환경) throws Exception {
        List<String> حکم = new ArrayList<>(Arrays.asList("python3", ٹولز.toString())); حکم.addAll(دلائل);
        ProcessBuilder نفاذ_کریں_حکم = new ProcessBuilder(حکم).directory(작업경로.toFile()).inheritIO(); نفاذ_کریں_حکم.environment().putAll(환경);
        int حالت_قدر = نفاذ_کریں_حکم.start().waitFor(); if (حالت_قدر != 0) throw new IOException("ٹولز ناکامی_قدر: " + ٹولز + " (" + حالت_قدر + ")");
    }
    @SuppressWarnings("unchecked")
    public static void main(String[] دلائل) throws Exception {
        if (دلائل.length < 1) throw new IllegalArgumentException("build, run, desktop, image, check, test-system 중 동작을 지정하세요");
        String عمل = دلائل[0];
        if (!Arrays.asList("build","run","desktop","image","check","test-system").contains(عمل)) throw new IllegalArgumentException("알 수 없는 عمل");
        Path عکس_ڈالنا_روٹ = Paths.get(System.getProperty("worldos.edition.root")).toAbsolutePath().normalize();
        Map<String,Object> ترتیبات = (Map<String,Object>)new 자료해석기(Files.readString(عکس_ڈالنا_روٹ.resolve("native.json"),StandardCharsets.UTF_8)).پڑھیں();
        Path ماخذ_شجر = 내부경로(عکس_ڈالنا_روٹ,(String)ترتیبات.get("source")), کرنیل_قدر = 내부경로(ماخذ_شجر,(String)ترتیبات.get("native"));
        List<String> 소유파일들 = (List<String>)(List<?>)ترتیبات.get("owned_files");
        for (String نام : 소유파일들) if (!Files.isRegularFile(내부경로(ماخذ_شجر,نام))) throw new IOException("ماخذ_شجر 없음: " + نام);
        if (عمل.equals("check")) { System.out.println(ترتیبات.get("country") + " " + ترتیبات.get("language") + " 독립 ماخذ_شجر تصدیق_کریں 완료"); return; }
        String 자원상대 = (String)ترتیبات.getOrDefault("resource_root", ".");
        if (!자원상대.equals(".") && !자원상대.equals("..")) throw new IllegalArgumentException("의존성 عکس_ڈالنا_روٹ راستہ_2 غلطی");
        Path ذریعہ_قدر = عکس_ڈالنا_روٹ.resolve(자원상대).normalize(); Path محفوظ_قدر = ذریعہ_قدر.resolve("native-vendor.tar.gz");
        String 기대해시 = (String)ترتیبات.get("vendor_sha256");
        if (!ہيش_فائل(محفوظ_قدر).equals(기대해시)) throw new IOException("의존성 SHA-256 불일치");
        Path 표식 = ماخذ_شجر.resolve(".vendor-sha256");
        if (!Files.isRegularFile(표식) || !Files.readString(표식).trim().equals(기대해시)) { اخذ_کریں(محفوظ_قدر, ماخذ_شجر); Files.writeString(표식,기대해시 + "\n"); }
        Map<String,String> 환경 = new HashMap<>(System.getenv());
        Path ipConfig = null;
        if (환경.containsKey("IP_CONFIG")) ipConfig = Paths.get(환경.get("IP_CONFIG")).toAbsolutePath().normalize();
        else for (Path parent = عکس_ڈالنا_روٹ; parent != null; parent = parent.getParent()) {
            if (Files.isRegularFile(parent.resolve("ip.conf"))) { ipConfig = parent.resolve("ip.conf"); break; }
        }
        if (ipConfig == null) ipConfig = ماخذ_شجر.resolve("ip.conf");
        if (!Files.isRegularFile(ipConfig)) throw new IOException("Missing ip.conf: " + ipConfig);
        환경.put("IP_CONFIG", ipConfig.toString());
        if (Arrays.asList("run","desktop","test-system").contains(عمل) && !환경.containsKey("QEMU_AARCH64")) {
            Path ایپ_ایپ_دراز = ذریعہ_قدر.resolve("host/qemu"), 실행기표식 = ذریعہ_قدر.resolve("host/.qemu-sha256");
            String ایپ_دراز_ہيش = (String)ترتیبات.get("qemu_sha256");
            if (!Files.isRegularFile(ایپ_ایپ_دراز) || !Files.isRegularFile(실행기표식) || !Files.readString(실행기표식).trim().equals(ایپ_دراز_ہيش)) {
                Path ایپ_دراز_محفوظ = ذریعہ_قدر.resolve("qemu-host.tar.gz"); if (!ہيش_فائل(ایپ_دراز_محفوظ).equals(ایپ_دراز_ہيش)) throw new IOException("QEMU SHA-256 불일치");
                اخذ_کریں(ایپ_دراز_محفوظ,ذریعہ_قدر.resolve("host")); Files.writeString(실행기표식,ایپ_دراز_ہيش + "\n");
            }
            환경.put("QEMU_AARCH64",ایپ_ایپ_دراز.toString());
        }
        MessageDigest 계산 = MessageDigest.getInstance("SHA-256"); Collections.sort(소유파일들);
        for (String نام : 소유파일들) { 계산.update(نام.getBytes(StandardCharsets.UTF_8)); 계산.update(Files.readAllBytes(내부경로(ماخذ_شجر,نام))); }
        계산.update("ip.conf\0".getBytes(StandardCharsets.UTF_8)); 계산.update(Files.readAllBytes(ipConfig));
        String ماخذ_ہيش = ہيش_متن(계산.digest()); Path 빌드표식 = کرنیل_قدر.resolve("build/worldos-source.sha256");
        if (عمل.equals("build") || !Files.isRegularFile(빌드표식) || !Files.readString(빌드표식).trim().equals(ماخذ_ہيش)) {
            호출(کرنیل_قدر,내부경로(کرنیل_قدر,(String)ترتیبات.get("builder")),Collections.emptyList(),환경);
            Files.writeString(빌드표식,ماخذ_ہيش + "\n");
        }
        List<String> 추가인수 = new ArrayList<>(Arrays.asList(دلائل).subList(1,دلائل.length));
        if (عمل.equals("run") || عمل.equals("desktop")) {
            if (عمل.equals("desktop")) 추가인수.add(0,"--desktop");
            호출(کرنیل_قدر,내부경로(کرنیل_قدر,(String)ترتیبات.get("runner")),추가인수,환경);
        } else if (عمل.equals("image")) 호출(کرنیل_قدر,내부경로(کرنیل_قدر,(String)ترتیبات.get("image_builder")),추가인수,환경);
        else if (عمل.equals("test-system")) {
            추가인수.add(0,عکس_ڈالنا_روٹ.toString()); 추가인수.add(0,"--edition");
            호출(کرنیل_قدر,내부경로(کرنیل_قدر,(String)ترتیبات.get("system_tester")),추가인수,환경);
        }
    }
}
