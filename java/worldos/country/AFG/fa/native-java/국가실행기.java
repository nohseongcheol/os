// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.security.MessageDigest;
import java.util.*;

/** 독립 국가판의 의존성 검사·복원·ساخت_سیستم·실행을 맡는 میزبان Java ابزارها. */
public final class 국가실행기 {
    static final class داده_ها_مفسر {
        final String مبداء; int مرتب_کردن;
        داده_ها_مفسر(String متن) { مبداء = متن; }
        void 빈칸() { while (مرتب_کردن < مبداء.length() && Character.isWhitespace(مبداء.charAt(مرتب_کردن))) مرتب_کردن++; }
        Object خواندن() {
            빈칸(); char نویسه_مقدار = مبداء.charAt(مرتب_کردن++);
            if (نویسه_مقدار == '{') {
                Map<String,Object> سنجش = new LinkedHashMap<>(); 빈칸();
                if (مبداء.charAt(مرتب_کردن) == '}') { مرتب_کردن++; return سنجش; }
                while (true) {
                    String نام = (String)خواندن(); 빈칸(); if (مبداء.charAt(مرتب_کردن++) != ':') throw new IllegalArgumentException("داده_ها مرزبند_مقدار خطا");
                    سنجش.put(نام, خواندن()); 빈칸(); char مرزبند_مقدار = مبداء.charAt(مرتب_کردن++);
                    if (مرزبند_مقدار == '}') return سنجش; if (مرزبند_مقدار != ',') throw new IllegalArgumentException("داده_ها مرزبند_مقدار خطا");
                }
            }
            if (نویسه_مقدار == '[') {
                List<Object> سنجش = new ArrayList<>(); 빈칸();
                if (مبداء.charAt(مرتب_کردن) == ']') { مرتب_کردن++; return سنجش; }
                while (true) {
                    سنجش.add(خواندن()); 빈칸(); char مرزبند_مقدار = مبداء.charAt(مرتب_کردن++);
                    if (مرزبند_مقدار == ']') return سنجش; if (مرزبند_مقدار != ',') throw new IllegalArgumentException("داده_ها مرزبند_مقدار خطا");
                }
            }
            if (نویسه_مقدار == '"') {
                StringBuilder سنجش = new StringBuilder();
                while (true) {
                    char بعدی_مورد = مبداء.charAt(مرتب_کردن++); if (بعدی_مورد == '"') return سنجش.toString();
                    if (بعدی_مورد == '\\') {
                        بعدی_مورد = مبداء.charAt(مرتب_کردن++);
                        if (بعدی_مورد == 'u') { سنجش.append((char)Integer.parseInt(مبداء.substring(مرتب_کردن, مرتب_کردن + 4),16)); مرتب_کردن += 4; continue; }
                        if (بعدی_مورد == 'n') بعدی_مورد = '\n'; else if (بعدی_مورد == 'r') بعدی_مورد = '\r'; else if (بعدی_مورد == 't') بعدی_مورد = '\t';
                        else if (بعدی_مورد == 'b') بعدی_مورد = '\b'; else if (بعدی_مورد == 'f') بعدی_مورد = '\f';
                        else if (بعدی_مورد != '"' && بعدی_مورد != '\\' && بعدی_مورد != '/') throw new IllegalArgumentException("문자 이스케이프 خطا");
                    }
                    سنجش.append(بعدی_مورد);
                }
            }
            int اجرا_2 = مرتب_کردن - 1;
            while (مرتب_کردن < مبداء.length() && ",]} \t\r\n".indexOf(مبداء.charAt(مرتب_کردن)) < 0) مرتب_کردن++;
            String مقدار = مبداء.substring(اجرا_2, مرتب_کردن);
            if (مقدار.equals("true")) return Boolean.TRUE; if (مقدار.equals("false")) return Boolean.FALSE; if (مقدار.equals("null")) return null;
            return Double.valueOf(مقدار);
        }
    }
    static String هاشور_فایل(Path مسیر) throws Exception {
        MessageDigest 계산 = MessageDigest.getInstance("SHA-256"); byte[] داده_ها = new byte[1024 * 1024];
        try (InputStream 입력 = Files.newInputStream(مسیر)) { for (int طول_مقدار; (طول_مقدار = 입력.read(داده_ها)) >= 0;) 계산.update(داده_ها,0,طول_مقدار); }
        return هاشور_متن(계산.digest());
    }
    static String هاشور_متن(byte[] داده_ها) {
        StringBuilder متن = new StringBuilder(); for (byte مقدار : داده_ها) متن.append(String.format(Locale.ROOT,"%02x",مقدار & 255)); return متن.toString();
    }
    static Path 내부경로(Path نمایش_دادن_جذر, String نام) {
        Path سنجش = نمایش_دادن_جذر.resolve(نام).normalize();
        if (نام.isEmpty() || Paths.get(نام).isAbsolute() || !سنجش.startsWith(نمایش_دادن_جذر) || نام.indexOf('\\') >= 0)
            throw new IllegalArgumentException("범위를 벗어난 مسیر: " + نام);
        for (Path 부분 : Paths.get(نام)) if (부분.toString().equals("..")) throw new IllegalArgumentException("상위 مسیر 금지: " + نام);
        for (Path 현재 = سنجش; 현재 != null && 현재.startsWith(نمایش_دادن_جذر); 현재 = 현재.getParent())
            if (Files.isSymbolicLink(현재)) throw new IllegalArgumentException("의존성 경로의 링크 금지: " + نام);
        return سنجش;
    }
    static String 명령출력(List<String> فرمان) throws Exception {
        Process فرآیند_مقدار = new ProcessBuilder(فرمان).redirectError(ProcessBuilder.Redirect.INHERIT).start();
        String سنجش = new String(فرآیند_مقدار.getInputStream().readAllBytes(),StandardCharsets.UTF_8);
        if (فرآیند_مقدار.waitFor() != 0) throw new IOException("فرمان عدم_موفقیت_مقدار: " + فرمان.get(0)); return سنجش;
    }
    static void استخراج(Path آرشیو_مقدار, Path مقصد_مقدار) throws Exception {
        for (String نام : 명령출력(Arrays.asList("tar","-tzf",آرشیو_مقدار.toString())).split("\n")) 내부경로(مقصد_مقدار, نام);
        for (String خط : 명령출력(Arrays.asList("tar","-tvzf",آرشیو_مقدار.toString())).split("\n"))
            if (!خط.isEmpty() && خط.charAt(0) != '-' && خط.charAt(0) != 'd') throw new IOException("외부 링크 또는 특수 파일을 포함한 의존성");
        Files.createDirectories(مقصد_مقدار);
        int وضعیت_مقدار = new ProcessBuilder("tar","--no-same-owner","--no-same-permissions","-xzf",آرشیو_مقدار.toString(),"-C",مقصد_مقدار.toString()).inheritIO().start().waitFor();
        if (وضعیت_مقدار != 0) throw new IOException("의존성 آرشیو_مقدار انتشار_حافظه_تلفن عدم_موفقیت_مقدار");
    }
    static void 호출(Path 작업경로, Path ابزارها, List<String> نشانوندها, Map<String,String> 환경) throws Exception {
        List<String> فرمان = new ArrayList<>(Arrays.asList("python3", ابزارها.toString())); فرمان.addAll(نشانوندها);
        ProcessBuilder اجرا_فرمان = new ProcessBuilder(فرمان).directory(작업경로.toFile()).inheritIO(); اجرا_فرمان.environment().putAll(환경);
        int وضعیت_مقدار = اجرا_فرمان.start().waitFor(); if (وضعیت_مقدار != 0) throw new IOException("ابزارها عدم_موفقیت_مقدار: " + ابزارها + " (" + وضعیت_مقدار + ")");
    }
    @SuppressWarnings("unchecked")
    public static void main(String[] نشانوندها) throws Exception {
        if (نشانوندها.length < 1) throw new IllegalArgumentException("build, run, desktop, image, check, test-system 중 동작을 지정하세요");
        String کنش = نشانوندها[0];
        if (!Arrays.asList("build","run","desktop","image","check","test-system").contains(کنش)) throw new IllegalArgumentException("알 수 없는 کنش");
        Path نمایش_دادن_جذر = Paths.get(System.getProperty("worldos.edition.root")).toAbsolutePath().normalize();
        Map<String,Object> تنظیمات = (Map<String,Object>)new داده_ها_مفسر(Files.readString(نمایش_دادن_جذر.resolve("native.json"),StandardCharsets.UTF_8)).خواندن();
        Path منبع_درخت = 내부경로(نمایش_دادن_جذر,(String)تنظیمات.get("source")), هسته_مقدار = 내부경로(منبع_درخت,(String)تنظیمات.get("native"));
        List<String> 소유파일들 = (List<String>)(List<?>)تنظیمات.get("owned_files");
        for (String نام : 소유파일들) if (!Files.isRegularFile(내부경로(منبع_درخت,نام))) throw new IOException("منبع_درخت 없음: " + نام);
        if (کنش.equals("check")) { System.out.println(تنظیمات.get("country") + " " + تنظیمات.get("language") + " 독립 منبع_درخت تأیید_صحت 완료"); return; }
        String 자원상대 = (String)تنظیمات.getOrDefault("resource_root", ".");
        if (!자원상대.equals(".") && !자원상대.equals("..")) throw new IllegalArgumentException("의존성 نمایش_دادن_جذر مسیر خطا");
        Path منبع_مقدار = نمایش_دادن_جذر.resolve(자원상대).normalize(); Path آرشیو_مقدار = منبع_مقدار.resolve("native-vendor.tar.gz");
        String 기대해시 = (String)تنظیمات.get("vendor_sha256");
        if (!هاشور_فایل(آرشیو_مقدار).equals(기대해시)) throw new IOException("의존성 SHA-256 불일치");
        Path 표식 = منبع_درخت.resolve(".vendor-sha256");
        if (!Files.isRegularFile(표식) || !Files.readString(표식).trim().equals(기대해시)) { استخراج(آرشیو_مقدار, منبع_درخت); Files.writeString(표식,기대해시 + "\n"); }
        Map<String,String> 환경 = new HashMap<>(System.getenv());
        Path ipConfig = null;
        if (환경.containsKey("IP_CONFIG")) ipConfig = Paths.get(환경.get("IP_CONFIG")).toAbsolutePath().normalize();
        else for (Path parent = نمایش_دادن_جذر; parent != null; parent = parent.getParent()) {
            if (Files.isRegularFile(parent.resolve("ip.conf"))) { ipConfig = parent.resolve("ip.conf"); break; }
        }
        if (ipConfig == null) ipConfig = منبع_درخت.resolve("ip.conf");
        if (!Files.isRegularFile(ipConfig)) throw new IOException("Missing ip.conf: " + ipConfig);
        환경.put("IP_CONFIG", ipConfig.toString());
        if (Arrays.asList("run","desktop","test-system").contains(کنش) && !환경.containsKey("QEMU_AARCH64")) {
            Path برنامه_راه_انداز = منبع_مقدار.resolve("host/qemu"), 실행기표식 = منبع_مقدار.resolve("host/.qemu-sha256");
            String راه_انداز_هاشور = (String)تنظیمات.get("qemu_sha256");
            if (!Files.isRegularFile(برنامه_راه_انداز) || !Files.isRegularFile(실행기표식) || !Files.readString(실행기표식).trim().equals(راه_انداز_هاشور)) {
                Path راه_انداز_آرشیو = منبع_مقدار.resolve("qemu-host.tar.gz"); if (!هاشور_فایل(راه_انداز_آرشیو).equals(راه_انداز_هاشور)) throw new IOException("QEMU SHA-256 불일치");
                استخراج(راه_انداز_آرشیو,منبع_مقدار.resolve("host")); Files.writeString(실행기표식,راه_انداز_هاشور + "\n");
            }
            환경.put("QEMU_AARCH64",برنامه_راه_انداز.toString());
        }
        MessageDigest 계산 = MessageDigest.getInstance("SHA-256"); Collections.sort(소유파일들);
        for (String نام : 소유파일들) { 계산.update(نام.getBytes(StandardCharsets.UTF_8)); 계산.update(Files.readAllBytes(내부경로(منبع_درخت,نام))); }
        계산.update("ip.conf\0".getBytes(StandardCharsets.UTF_8)); 계산.update(Files.readAllBytes(ipConfig));
        String منبع_هاشور = هاشور_متن(계산.digest()); Path 빌드표식 = هسته_مقدار.resolve("build/worldos-source.sha256");
        if (کنش.equals("build") || !Files.isRegularFile(빌드표식) || !Files.readString(빌드표식).trim().equals(منبع_هاشور)) {
            호출(هسته_مقدار,내부경로(هسته_مقدار,(String)تنظیمات.get("builder")),Collections.emptyList(),환경);
            Files.writeString(빌드표식,منبع_هاشور + "\n");
        }
        List<String> 추가인수 = new ArrayList<>(Arrays.asList(نشانوندها).subList(1,نشانوندها.length));
        if (کنش.equals("run") || کنش.equals("desktop")) {
            if (کنش.equals("desktop")) 추가인수.add(0,"--desktop");
            호출(هسته_مقدار,내부경로(هسته_مقدار,(String)تنظیمات.get("runner")),추가인수,환경);
        } else if (کنش.equals("image")) 호출(هسته_مقدار,내부경로(هسته_مقدار,(String)تنظیمات.get("image_builder")),추가인수,환경);
        else if (کنش.equals("test-system")) {
            추가인수.add(0,نمایش_دادن_جذر.toString()); 추가인수.add(0,"--edition");
            호출(هسته_مقدار,내부경로(هسته_مقدار,(String)تنظیمات.get("system_tester")),추가인수,환경);
        }
    }
}
