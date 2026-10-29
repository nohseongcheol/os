// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.security.MessageDigest;
import java.util.*;

/** 독립 국가판의 의존성 검사·복원·بنية_نظام·실행을 맡는 مضيف Java أدوات. */
public final class مشغلالبلد {
    static final class بيانات_المحلل {
        final String مصدر; int موضع;
        بيانات_المحلل(String نص) { مصدر = نص; }
        void 빈칸() { while (موضع < مصدر.length() && Character.isWhitespace(مصدر.charAt(موضع))) موضع++; }
        Object قراءة() {
            빈칸(); char حرف_قيمة = مصدر.charAt(موضع++);
            if (حرف_قيمة == '{') {
                Map<String,Object> نتيجة = new LinkedHashMap<>(); 빈칸();
                if (مصدر.charAt(موضع) == '}') { موضع++; return نتيجة; }
                while (true) {
                    String اسم = (String)قراءة(); 빈칸(); if (مصدر.charAt(موضع++) != ':') throw new IllegalArgumentException("بيانات محدِّد_قيمة خطأ");
                    نتيجة.put(اسم, قراءة()); 빈칸(); char محدِّد_قيمة = مصدر.charAt(موضع++);
                    if (محدِّد_قيمة == '}') return نتيجة; if (محدِّد_قيمة != ',') throw new IllegalArgumentException("بيانات محدِّد_قيمة خطأ");
                }
            }
            if (حرف_قيمة == '[') {
                List<Object> نتيجة = new ArrayList<>(); 빈칸();
                if (مصدر.charAt(موضع) == ']') { موضع++; return نتيجة; }
                while (true) {
                    نتيجة.add(قراءة()); 빈칸(); char محدِّد_قيمة = مصدر.charAt(موضع++);
                    if (محدِّد_قيمة == ']') return نتيجة; if (محدِّد_قيمة != ',') throw new IllegalArgumentException("بيانات محدِّد_قيمة خطأ");
                }
            }
            if (حرف_قيمة == '"') {
                StringBuilder نتيجة = new StringBuilder();
                while (true) {
                    char التالي_عنصر = مصدر.charAt(موضع++); if (التالي_عنصر == '"') return نتيجة.toString();
                    if (التالي_عنصر == '\\') {
                        التالي_عنصر = مصدر.charAt(موضع++);
                        if (التالي_عنصر == 'u') { نتيجة.append((char)Integer.parseInt(مصدر.substring(موضع, موضع + 4),16)); موضع += 4; continue; }
                        if (التالي_عنصر == 'n') التالي_عنصر = '\n'; else if (التالي_عنصر == 'r') التالي_عنصر = '\r'; else if (التالي_عنصر == 't') التالي_عنصر = '\t';
                        else if (التالي_عنصر == 'b') التالي_عنصر = '\b'; else if (التالي_عنصر == 'f') التالي_عنصر = '\f';
                        else if (التالي_عنصر != '"' && التالي_عنصر != '\\' && التالي_عنصر != '/') throw new IllegalArgumentException("문자 이스케이프 خطأ");
                    }
                    نتيجة.append(التالي_عنصر);
                }
            }
            int تشغيل = موضع - 1;
            while (موضع < مصدر.length() && ",]} \t\r\n".indexOf(مصدر.charAt(موضع)) < 0) موضع++;
            String قيمة = مصدر.substring(تشغيل, موضع);
            if (قيمة.equals("true")) return Boolean.TRUE; if (قيمة.equals("false")) return Boolean.FALSE; if (قيمة.equals("null")) return null;
            return Double.valueOf(قيمة);
        }
    }
    static String تجزئة_ملف(Path مسار) throws Exception {
        MessageDigest 계산 = MessageDigest.getInstance("SHA-256"); byte[] بيانات = new byte[1024 * 1024];
        try (InputStream إدخال_قيمة = Files.newInputStream(مسار)) { for (int 길이; (길이 = إدخال_قيمة.read(بيانات)) >= 0;) 계산.update(بيانات,0,길이); }
        return تجزئة_نص(계산.digest());
    }
    static String تجزئة_نص(byte[] بيانات) {
        StringBuilder نص = new StringBuilder(); for (byte قيمة : بيانات) نص.append(String.format(Locale.ROOT,"%02x",قيمة & 255)); return نص.toString();
    }
    static Path داخلي_مسار(Path يعرض_جذر, String اسم) {
        Path نتيجة = يعرض_جذر.resolve(اسم).normalize();
        if (اسم.isEmpty() || Paths.get(اسم).isAbsolute() || !نتيجة.startsWith(يعرض_جذر) || اسم.indexOf('\\') >= 0)
            throw new IllegalArgumentException("범위를 벗어난 مسار: " + اسم);
        for (Path 부분 : Paths.get(اسم)) if (부분.toString().equals("..")) throw new IllegalArgumentException("상위 مسار 금지: " + اسم);
        for (Path حديث_عنصر = نتيجة; حديث_عنصر != null && حديث_عنصر.startsWith(يعرض_جذر); حديث_عنصر = حديث_عنصر.getParent())
            if (Files.isSymbolicLink(حديث_عنصر)) throw new IllegalArgumentException("의존성 경로의 링크 금지: " + اسم);
        return نتيجة;
    }
    static String أمر_الناتج(List<String> أمر) throws Exception {
        Process عملية_قيمة = new ProcessBuilder(أمر).redirectError(ProcessBuilder.Redirect.INHERIT).start();
        String نتيجة = new String(عملية_قيمة.getInputStream().readAllBytes(),StandardCharsets.UTF_8);
        if (عملية_قيمة.waitFor() != 0) throw new IOException("أمر فشل_قيمة: " + أمر.get(0)); return نتيجة;
    }
    static void يستخرج(Path أرشيف_قيمة, Path وجهة_قيمة) throws Exception {
        for (String اسم : أمر_الناتج(Arrays.asList("tar","-tzf",أرشيف_قيمة.toString())).split("\n")) داخلي_مسار(وجهة_قيمة, اسم);
        for (String سطر : أمر_الناتج(Arrays.asList("tar","-tvzf",أرشيف_قيمة.toString())).split("\n"))
            if (!سطر.isEmpty() && سطر.charAt(0) != '-' && سطر.charAt(0) != 'd') throw new IOException("خارجي_قيمة 링크 또는 특수 파일을 포함한 의존성");
        Files.createDirectories(وجهة_قيمة);
        int حالة_قيمة = new ProcessBuilder("tar","--no-same-owner","--no-same-permissions","-xzf",أرشيف_قيمة.toString(),"-C",وجهة_قيمة.toString()).inheritIO().start().waitFor();
        if (حالة_قيمة != 0) throw new IOException("의존성 أرشيف_قيمة إصدار_تخزين فشل_قيمة");
    }
    static void 호출(Path 작업경로, Path أدوات, List<String> وسائط, Map<String,String> بيئة_التشغيل) throws Exception {
        List<String> أمر = new ArrayList<>(Arrays.asList("python3", أدوات.toString())); أمر.addAll(وسائط);
        ProcessBuilder ينفذ_أمر = new ProcessBuilder(أمر).directory(작업경로.toFile()).inheritIO(); ينفذ_أمر.environment().putAll(بيئة_التشغيل);
        int حالة_قيمة = ينفذ_أمر.start().waitFor(); if (حالة_قيمة != 0) throw new IOException("أدوات فشل_قيمة: " + أدوات + " (" + حالة_قيمة + ")");
    }
    @SuppressWarnings("unchecked")
    public static void main(String[] وسائط) throws Exception {
        if (وسائط.length < 1) throw new IllegalArgumentException("build, run, desktop, image, check, test-system 중 동작을 지정하세요");
        String إجراء = وسائط[0];
        if (!Arrays.asList("build","run","desktop","image","check","test-system").contains(إجراء)) throw new IllegalArgumentException("알 رقم 없는 إجراء");
        Path يعرض_جذر = Paths.get(System.getProperty("worldos.edition.root")).toAbsolutePath().normalize();
        Map<String,Object> إعدادات = (Map<String,Object>)new بيانات_المحلل(Files.readString(يعرض_جذر.resolve("native.json"),StandardCharsets.UTF_8)).قراءة();
        Path مصدر_شجرة = داخلي_مسار(يعرض_جذر,(String)إعدادات.get("source")), نواة_قيمة = داخلي_مسار(مصدر_شجرة,(String)إعدادات.get("native"));
        List<String> 소유파일들 = (List<String>)(List<?>)إعدادات.get("owned_files");
        for (String اسم : 소유파일들) if (!Files.isRegularFile(داخلي_مسار(مصدر_شجرة,اسم))) throw new IOException("مصدر_شجرة 없음: " + اسم);
        if (إجراء.equals("check")) { System.out.println(إعدادات.get("country") + " " + إعدادات.get("language") + " 독립 مصدر_شجرة يتحقق 완료"); return; }
        String مصدر_مسار_نسبي = (String)إعدادات.getOrDefault("resource_root", ".");
        if (!مصدر_مسار_نسبي.equals(".") && !مصدر_مسار_نسبي.equals("..")) throw new IllegalArgumentException("의존성 يعرض_جذر مسار خطأ");
        Path مصدر_قيمة = يعرض_جذر.resolve(مصدر_مسار_نسبي).normalize(); Path أرشيف_قيمة = مصدر_قيمة.resolve("native-vendor.tar.gz");
        String 기대해시 = (String)إعدادات.get("vendor_sha256");
        if (!تجزئة_ملف(أرشيف_قيمة).equals(기대해시)) throw new IOException("의존성 SHA-256 불일치");
        Path علامة_قيمة_7e8f90bd = مصدر_شجرة.resolve(".vendor-sha256");
        if (!Files.isRegularFile(علامة_قيمة_7e8f90bd) || !Files.readString(علامة_قيمة_7e8f90bd).trim().equals(기대해시)) { يستخرج(أرشيف_قيمة, مصدر_شجرة); Files.writeString(علامة_قيمة_7e8f90bd,기대해시 + "\n"); }
        Map<String,String> بيئة_التشغيل = new HashMap<>(System.getenv());
        Path ipConfig = null;
        if (بيئة_التشغيل.containsKey("IP_CONFIG")) ipConfig = Paths.get(بيئة_التشغيل.get("IP_CONFIG")).toAbsolutePath().normalize();
        else for (Path parent = يعرض_جذر; parent != null; parent = parent.getParent()) {
            if (Files.isRegularFile(parent.resolve("ip.conf"))) { ipConfig = parent.resolve("ip.conf"); break; }
        }
        if (ipConfig == null) ipConfig = مصدر_شجرة.resolve("ip.conf");
        if (!Files.isRegularFile(ipConfig)) throw new IOException("Missing ip.conf: " + ipConfig);
        بيئة_التشغيل.put("IP_CONFIG", ipConfig.toString());
        if (Arrays.asList("run","desktop","test-system").contains(إجراء) && !بيئة_التشغيل.containsKey("QEMU_AARCH64")) {
            Path تطبيق_مشغّل = مصدر_قيمة.resolve("host/qemu"), مشغّل_علامة = مصدر_قيمة.resolve("host/.qemu-sha256");
            String مشغّل_تجزئة = (String)إعدادات.get("qemu_sha256");
            if (!Files.isRegularFile(تطبيق_مشغّل) || !Files.isRegularFile(مشغّل_علامة) || !Files.readString(مشغّل_علامة).trim().equals(مشغّل_تجزئة)) {
                Path مشغّل_أرشيف = مصدر_قيمة.resolve("qemu-host.tar.gz"); if (!تجزئة_ملف(مشغّل_أرشيف).equals(مشغّل_تجزئة)) throw new IOException("QEMU SHA-256 불일치");
                يستخرج(مشغّل_أرشيف,مصدر_قيمة.resolve("host")); Files.writeString(مشغّل_علامة,مشغّل_تجزئة + "\n");
            }
            بيئة_التشغيل.put("QEMU_AARCH64",تطبيق_مشغّل.toString());
        }
        MessageDigest 계산 = MessageDigest.getInstance("SHA-256"); Collections.sort(소유파일들);
        for (String اسم : 소유파일들) { 계산.update(اسم.getBytes(StandardCharsets.UTF_8)); 계산.update(Files.readAllBytes(داخلي_مسار(مصدر_شجرة,اسم))); }
        계산.update("ip.conf\0".getBytes(StandardCharsets.UTF_8)); 계산.update(Files.readAllBytes(ipConfig));
        String مصدر_تجزئة = تجزئة_نص(계산.digest()); Path بنية_علامة = نواة_قيمة.resolve("build/worldos-source.sha256");
        if (إجراء.equals("build") || !Files.isRegularFile(بنية_علامة) || !Files.readString(بنية_علامة).trim().equals(مصدر_تجزئة)) {
            호출(نواة_قيمة,داخلي_مسار(نواة_قيمة,(String)إعدادات.get("builder")),Collections.emptyList(),بيئة_التشغيل);
            Files.writeString(بنية_علامة,مصدر_تجزئة + "\n");
        }
        List<String> 추가인수 = new ArrayList<>(Arrays.asList(وسائط).subList(1,وسائط.length));
        if (إجراء.equals("run") || إجراء.equals("desktop")) {
            if (إجراء.equals("desktop")) 추가인수.add(0,"--desktop");
            호출(نواة_قيمة,داخلي_مسار(نواة_قيمة,(String)إعدادات.get("runner")),추가인수,بيئة_التشغيل);
        } else if (إجراء.equals("image")) 호출(نواة_قيمة,داخلي_مسار(نواة_قيمة,(String)إعدادات.get("image_builder")),추가인수,بيئة_التشغيل);
        else if (إجراء.equals("test-system")) {
            추가인수.add(0,يعرض_جذر.toString()); 추가인수.add(0,"--edition");
            호출(نواة_قيمة,داخلي_مسار(نواة_قيمة,(String)إعدادات.get("system_tester")),추가인수,بيئة_التشغيل);
        }
    }
}
