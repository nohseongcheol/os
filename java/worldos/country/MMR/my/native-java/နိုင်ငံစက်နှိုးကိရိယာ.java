// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.security.MessageDigest;
import java.util.*;

/** သီးခြားနိုင်ငံမူ၏ မှီခိုပစ္စည်းစစ်ဆေးမှု၊ ပြန်လည်ရယူမှု၊ တည်ဆောက်မှုနှင့် လုပ်ဆောင်မှုကို တာဝန်ယူသော အိမ်ရှင် Java ကိရိယာ။ */
public final class နိုင်ငံစက်နှိုးကိရိယာ {
    static final class ဒေတာသဒ္ဒါခွဲခြမ်းစက် {
        final String မူရင်းကုဒ်; int နေရာ;
        ဒေတာသဒ္ဒါခွဲခြမ်းစက်(String စာသား) { မူရင်းကုဒ် = စာသား; }
        void ကွက်လပ်ကျော်() { while (နေရာ < မူရင်းကုဒ်.length() && Character.isWhitespace(မူရင်းကုဒ်.charAt(နေရာ))) နေရာ++; }
        Object ဖတ်() {
            ကွက်လပ်ကျော်(); char အက္ခရာတန်ဖိုး = မူရင်းကုဒ်.charAt(နေရာ++);
            if (အက္ခရာတန်ဖိုး == '{') {
                Map<String,Object> ရလဒ် = new LinkedHashMap<>(); ကွက်လပ်ကျော်();
                if (မူရင်းကုဒ်.charAt(နေရာ) == '}') { နေရာ++; return ရလဒ်; }
                while (true) {
                    String အမည် = (String)ဖတ်(); ကွက်လပ်ကျော်(); if (မူရင်းကုဒ်.charAt(နေရာ++) != ':') throw new IllegalArgumentException("ဒေတာ ပိုင်းခြားအမှတ် အမှား");
                    ရလဒ်.put(အမည်, ဖတ်()); ကွက်လပ်ကျော်(); char ပိုင်းခြားအမှတ် = မူရင်းကုဒ်.charAt(နေရာ++);
                    if (ပိုင်းခြားအမှတ် == '}') return ရလဒ်; if (ပိုင်းခြားအမှတ် != ',') throw new IllegalArgumentException("ဒေတာ ပိုင်းခြားအမှတ် အမှား");
                }
            }
            if (အက္ခရာတန်ဖိုး == '[') {
                List<Object> ရလဒ် = new ArrayList<>(); ကွက်လပ်ကျော်();
                if (မူရင်းကုဒ်.charAt(နေရာ) == ']') { နေရာ++; return ရလဒ်; }
                while (true) {
                    ရလဒ်.add(ဖတ်()); ကွက်လပ်ကျော်(); char ပိုင်းခြားအမှတ် = မူရင်းကုဒ်.charAt(နေရာ++);
                    if (ပိုင်းခြားအမှတ် == ']') return ရလဒ်; if (ပိုင်းခြားအမှတ် != ',') throw new IllegalArgumentException("ဒေတာ ပိုင်းခြားအမှတ် အမှား");
                }
            }
            if (အက္ခရာတန်ဖိုး == '"') {
                StringBuilder ရလဒ် = new StringBuilder();
                while (true) {
                    char နောက်တစ်ခုအချက်အလက်တစ်ခု = မူရင်းကုဒ်.charAt(နေရာ++); if (နောက်တစ်ခုအချက်အလက်တစ်ခု == '"') return ရလဒ်.toString();
                    if (နောက်တစ်ခုအချက်အလက်တစ်ခု == '\\') {
                        နောက်တစ်ခုအချက်အလက်တစ်ခု = မူရင်းကုဒ်.charAt(နေရာ++);
                        if (နောက်တစ်ခုအချက်အလက်တစ်ခု == 'u') { ရလဒ်.append((char)Integer.parseInt(မူရင်းကုဒ်.substring(နေရာ, နေရာ + 4),16)); နေရာ += 4; continue; }
                        if (နောက်တစ်ခုအချက်အလက်တစ်ခု == 'n') နောက်တစ်ခုအချက်အလက်တစ်ခု = '\n'; else if (နောက်တစ်ခုအချက်အလက်တစ်ခု == 'r') နောက်တစ်ခုအချက်အလက်တစ်ခု = '\r'; else if (နောက်တစ်ခုအချက်အလက်တစ်ခု == 't') နောက်တစ်ခုအချက်အလက်တစ်ခု = '\t';
                        else if (နောက်တစ်ခုအချက်အလက်တစ်ခု == 'b') နောက်တစ်ခုအချက်အလက်တစ်ခု = '\b'; else if (နောက်တစ်ခုအချက်အလက်တစ်ခု == 'f') နောက်တစ်ခုအချက်အလက်တစ်ခု = '\f';
                        else if (နောက်တစ်ခုအချက်အလက်တစ်ခု != '"' && နောက်တစ်ခုအချက်အလက်တစ်ခု != '\\' && နောက်တစ်ခုအချက်အလက်တစ်ခု != '/') throw new IllegalArgumentException("အက္ခရာ 이스케이프 အမှား");
                    }
                    ရလဒ်.append(နောက်တစ်ခုအချက်အလက်တစ်ခု);
                }
            }
            int လုပ်ဆောင် = နေရာ - 1;
            while (နေရာ < မူရင်းကုဒ်.length() && ",]} \t\r\n".indexOf(မူရင်းကုဒ်.charAt(နေရာ)) < 0) နေရာ++;
            String တန်ဖိုး = မူရင်းကုဒ်.substring(လုပ်ဆောင်, နေရာ);
            if (တန်ဖိုး.equals("true")) return Boolean.TRUE; if (တန်ဖိုး.equals("false")) return Boolean.FALSE; if (တန်ဖိုး.equals("null")) return null;
            return Double.valueOf(တန်ဖိုး);
        }
    }
    static String ဖိုင်ဟက်ရှ်တွက်(Path လမ်း) throws Exception {
        MessageDigest တွက်ချက်မှု = MessageDigest.getInstance("SHA-256"); byte[] ဒေတာ = new byte[1024 * 1024];
        try (InputStream ဝင်ဒေတာ = Files.newInputStream(လမ်း)) { for (int အလျား; (အလျား = ဝင်ဒေတာ.read(ဒေတာ)) >= 0;) တွက်ချက်မှု.update(ဒေတာ,0,အလျား); }
        return ဟက်ရှ်စာသား(တွက်ချက်မှု.digest());
    }
    static String ဟက်ရှ်စာသား(byte[] ဒေတာ) {
        StringBuilder စာသား = new StringBuilder(); for (byte တန်ဖိုး : ဒေတာ) စာသား.append(String.format(Locale.ROOT,"%02x",တန်ဖိုး & 255)); return စာသား.toString();
    }
    static Path အတွင်းပိုင်းလမ်းကြောင်း(Path စီမံကိန်းအမြစ်, String အမည်) {
        Path ရလဒ် = စီမံကိန်းအမြစ်.resolve(အမည်).normalize();
        if (အမည်.isEmpty() || Paths.get(အမည်).isAbsolute() || !ရလဒ်.startsWith(စီမံကိန်းအမြစ်) || အမည်.indexOf('\\') >= 0)
            throw new IllegalArgumentException("범위를 벗어난 လမ်း: " + အမည်);
        for (Path အစိတ်အပိုင်းတန်ဖိုး : Paths.get(အမည်)) if (အစိတ်အပိုင်းတန်ဖိုး.toString().equals("..")) throw new IllegalArgumentException("상위 လမ်း 금지: " + အမည်);
        for (Path လက်ရှိအချက်အလက်တစ်ခု = ရလဒ်; လက်ရှိအချက်အလက်တစ်ခု != null && လက်ရှိအချက်အလက်တစ်ခု.startsWith(စီမံကိန်းအမြစ်); လက်ရှိအချက်အလက်တစ်ခု = လက်ရှိအချက်အလက်တစ်ခု.getParent())
            if (Files.isSymbolicLink(လက်ရှိအချက်အလက်တစ်ခု)) throw new IllegalArgumentException("의존성 경로의 링크 금지: " + အမည်);
        return ရလဒ်;
    }
    static String အမိန့်အထွက်(List<String> အမိန့်) throws Exception {
        Process လုပ်ငန်းစဉ် = new ProcessBuilder(အမိန့်).redirectError(ProcessBuilder.Redirect.INHERIT).start();
        String ရလဒ် = new String(လုပ်ငန်းစဉ်.getInputStream().readAllBytes(),StandardCharsets.UTF_8);
        if (လုပ်ငန်းစဉ်.waitFor() != 0) throw new IOException("အမိန့် မအောင်မြင်မှု: " + အမိန့်.get(0)); return ရလဒ်;
    }
    static void ထုတ်ယူ(Path မော်ကွန်းတန်ဖိုး, Path ဦးတည်ရာတန်ဖိုး) throws Exception {
        for (String အမည် : အမိန့်အထွက်(Arrays.asList("tar","-tzf",မော်ကွန်းတန်ဖိုး.toString())).split("\n")) အတွင်းပိုင်းလမ်းကြောင်း(ဦးတည်ရာတန်ဖိုး, အမည်);
        for (String စာကြောင်း : အမိန့်အထွက်(Arrays.asList("tar","-tvzf",မော်ကွန်းတန်ဖိုး.toString())).split("\n"))
            if (!စာကြောင်း.isEmpty() && စာကြောင်း.charAt(0) != '-' && စာကြောင်း.charAt(0) != 'd') throw new IOException("ပြင်ပတန်ဖိုး 링크 또는 အထူးတန်ဖိုး 파일을 포함한 의존성");
        Files.createDirectories(ဦးတည်ရာတန်ဖိုး);
        int အခြေအနေတန်ဖိုး = new ProcessBuilder("tar","--no-same-owner","--no-same-permissions","-xzf",မော်ကွန်းတန်ဖိုး.toString(),"-C",ဦးတည်ရာတန်ဖိုး.toString()).inheritIO().start().waitFor();
        if (အခြေအနေတန်ဖိုး != 0) throw new IOException("의존성 မော်ကွန်းတန်ဖိုး သိုလှောင်ရာလွှတ်ပေး မအောင်မြင်မှု");
    }
    static void ခေါ်လုပ်(Path လုပ်ဆောင်လမ်း, Path ကိရိယာစု, List<String> အချက်များ, Map<String,String> ဝန်းကျင်) throws Exception {
        List<String> အမိန့် = new ArrayList<>(Arrays.asList("python3", ကိရိယာစု.toString())); အမိန့်.addAll(အချက်များ);
        ProcessBuilder စက်မောင်း = new ProcessBuilder(အမိန့်).directory(လုပ်ဆောင်လမ်း.toFile()).inheritIO(); စက်မောင်း.environment().putAll(ဝန်းကျင်);
        int အခြေအနေတန်ဖိုး = စက်မောင်း.start().waitFor(); if (အခြေအနေတန်ဖိုး != 0) throw new IOException("ကိရိယာစု မအောင်မြင်မှု: " + ကိရိယာစု + " (" + အခြေအနေတန်ဖိုး + ")");
    }
    @SuppressWarnings("unchecked")
    public static void main(String[] အချက်များ) throws Exception {
        if (အချက်များ.length < 1) throw new IllegalArgumentException("build, run, desktop, image, check, test-system 중 동작을 지정하세요");
        String လှုပ်ရှားမှု = အချက်များ[0];
        if (!Arrays.asList("build","run","desktop","image","check","test-system").contains(လှုပ်ရှားမှု)) throw new IllegalArgumentException("알 ကိန်းတန်ဖိုး 없는 လှုပ်ရှားမှု");
        Path စီမံကိန်းအမြစ် = Paths.get(System.getProperty("worldos.edition.root")).toAbsolutePath().normalize();
        Map<String,Object> သတ်မှတ်ချက် = (Map<String,Object>)new ဒေတာသဒ္ဒါခွဲခြမ်းစက်(Files.readString(စီမံကိန်းအမြစ်.resolve("native.json"),StandardCharsets.UTF_8)).ဖတ်();
        Path မူရင်းကုဒ်အပင်ဖွဲ့စည်းပုံ = အတွင်းပိုင်းလမ်းကြောင်း(စီမံကိန်းအမြစ်,(String)သတ်မှတ်ချက်.get("source")), အူတိုင်တန်ဖိုး = အတွင်းပိုင်းလမ်းကြောင်း(မူရင်းကုဒ်အပင်ဖွဲ့စည်းပုံ,(String)သတ်မှတ်ချက်.get("native"));
        List<String> ပိုင်ဆိုင်ဖိုင်များ = (List<String>)(List<?>)သတ်မှတ်ချက်.get("owned_files");
        for (String အမည် : ပိုင်ဆိုင်ဖိုင်များ) if (!Files.isRegularFile(အတွင်းပိုင်းလမ်းကြောင်း(မူရင်းကုဒ်အပင်ဖွဲ့စည်းပုံ,အမည်))) throw new IOException("မူရင်းကုဒ်အပင်ဖွဲ့စည်းပုံ 없음: " + အမည်);
        if (လှုပ်ရှားမှု.equals("check")) { System.out.println(သတ်မှတ်ချက်.get("country") + " " + သတ်မှတ်ချက်.get("language") + " 독립 မူရင်းကုဒ်အပင်ဖွဲ့စည်းပုံ အတည်ပြု ဖြစ်သောအပြည့်အစုံ"); return; }
        String အရင်းအမြစ်နှိုင်းယှဉ်ဆက်နွယ်လမ်းကြောင်း = (String)သတ်မှတ်ချက်.getOrDefault("resource_root", ".");
        if (!အရင်းအမြစ်နှိုင်းယှဉ်ဆက်နွယ်လမ်းကြောင်း.equals(".") && !အရင်းအမြစ်နှိုင်းယှဉ်ဆက်နွယ်လမ်းကြောင်း.equals("..")) throw new IllegalArgumentException("의존성 စီမံကိန်းအမြစ် လမ်း အမှား");
        Path အရင်းအမြစ်တန်ဖိုး = စီမံကိန်းအမြစ်.resolve(အရင်းအမြစ်နှိုင်းယှဉ်ဆက်နွယ်လမ်းကြောင်း).normalize(); Path မော်ကွန်းတန်ဖိုး = အရင်းအမြစ်တန်ဖိုး.resolve("native-vendor.tar.gz");
        String မျှော်မှန်းဟက်ရှ် = (String)သတ်မှတ်ချက်.get("vendor_sha256");
        if (!ဖိုင်ဟက်ရှ်တွက်(မော်ကွန်းတန်ဖိုး).equals(မျှော်မှန်းဟက်ရှ်)) throw new IOException("의존성 SHA-256 불일치");
        Path အမှတ်အသား = မူရင်းကုဒ်အပင်ဖွဲ့စည်းပုံ.resolve(".vendor-sha256");
        if (!Files.isRegularFile(အမှတ်အသား) || !Files.readString(အမှတ်အသား).trim().equals(မျှော်မှန်းဟက်ရှ်)) { ထုတ်ယူ(မော်ကွန်းတန်ဖိုး, မူရင်းကုဒ်အပင်ဖွဲ့စည်းပုံ); Files.writeString(အမှတ်အသား,မျှော်မှန်းဟက်ရှ် + "\n"); }
        Map<String,String> ဝန်းကျင် = new HashMap<>(System.getenv());
        Path ipConfig = null;
        if (ဝန်းကျင်.containsKey("IP_CONFIG")) ipConfig = Paths.get(ဝန်းကျင်.get("IP_CONFIG")).toAbsolutePath().normalize();
        else for (Path parent = စီမံကိန်းအမြစ်; parent != null; parent = parent.getParent()) {
            if (Files.isRegularFile(parent.resolve("ip.conf"))) { ipConfig = parent.resolve("ip.conf"); break; }
        }
        if (ipConfig == null) ipConfig = မူရင်းကုဒ်အပင်ဖွဲ့စည်းပုံ.resolve("ip.conf");
        if (!Files.isRegularFile(ipConfig)) throw new IOException("Missing ip.conf: " + ipConfig);
        ဝန်းကျင်.put("IP_CONFIG", ipConfig.toString());
        if (Arrays.asList("run","desktop","test-system").contains(လှုပ်ရှားမှု) && !ဝန်းကျင်.containsKey("QEMU_AARCH64")) {
            Path ပရိုဂရမ်စက်နှိုးကိရိယာ = အရင်းအမြစ်တန်ဖိုး.resolve("host/qemu"), လည်ပတ်ကိရိယာအမှတ်အသား = အရင်းအမြစ်တန်ဖိုး.resolve("host/.qemu-sha256");
            String လည်ပတ်ကိရိယာဟက်ရှ် = (String)သတ်မှတ်ချက်.get("qemu_sha256");
            if (!Files.isRegularFile(ပရိုဂရမ်စက်နှိုးကိရိယာ) || !Files.isRegularFile(လည်ပတ်ကိရိယာအမှတ်အသား) || !Files.readString(လည်ပတ်ကိရိယာအမှတ်အသား).trim().equals(လည်ပတ်ကိရိယာဟက်ရှ်)) {
                Path စက်နှိုးကိရိယာမော်ကွန်း = အရင်းအမြစ်တန်ဖိုး.resolve("qemu-host.tar.gz"); if (!ဖိုင်ဟက်ရှ်တွက်(စက်နှိုးကိရိယာမော်ကွန်း).equals(လည်ပတ်ကိရိယာဟက်ရှ်)) throw new IOException("QEMU SHA-256 불일치");
                ထုတ်ယူ(စက်နှိုးကိရိယာမော်ကွန်း,အရင်းအမြစ်တန်ဖိုး.resolve("host")); Files.writeString(လည်ပတ်ကိရိယာအမှတ်အသား,လည်ပတ်ကိရိယာဟက်ရှ် + "\n");
            }
            ဝန်းကျင်.put("QEMU_AARCH64",ပရိုဂရမ်စက်နှိုးကိရိယာ.toString());
        }
        MessageDigest တွက်ချက်မှု = MessageDigest.getInstance("SHA-256"); Collections.sort(ပိုင်ဆိုင်ဖိုင်များ);
        for (String အမည် : ပိုင်ဆိုင်ဖိုင်များ) { တွက်ချက်မှု.update(အမည်.getBytes(StandardCharsets.UTF_8)); တွက်ချက်မှု.update(Files.readAllBytes(အတွင်းပိုင်းလမ်းကြောင်း(မူရင်းကုဒ်အပင်ဖွဲ့စည်းပုံ,အမည်))); }
        တွက်ချက်မှု.update("ip.conf\0".getBytes(StandardCharsets.UTF_8)); တွက်ချက်မှု.update(Files.readAllBytes(ipConfig));
        String မူရင်းကုဒ်ဟက်ရှ် = ဟက်ရှ်စာသား(တွက်ချက်မှု.digest()); Path တည်ဆောက်အမှတ်အသား = အူတိုင်တန်ဖိုး.resolve("build/worldos-source.sha256");
        if (လှုပ်ရှားမှု.equals("build") || !Files.isRegularFile(တည်ဆောက်အမှတ်အသား) || !Files.readString(တည်ဆောက်အမှတ်အသား).trim().equals(မူရင်းကုဒ်ဟက်ရှ်)) {
            ခေါ်လုပ်(အူတိုင်တန်ဖိုး,အတွင်းပိုင်းလမ်းကြောင်း(အူတိုင်တန်ဖိုး,(String)သတ်မှတ်ချက်.get("builder")),Collections.emptyList(),ဝန်းကျင်);
            Files.writeString(တည်ဆောက်အမှတ်အသား,မူရင်းကုဒ်ဟက်ရှ် + "\n");
        }
        List<String> စက်နှိုးကိရိယာပေးအချက်များ = new ArrayList<>(Arrays.asList(အချက်များ).subList(1,အချက်များ.length));
        if (လှုပ်ရှားမှု.equals("run") || လှုပ်ရှားမှု.equals("desktop")) {
            if (လှုပ်ရှားမှု.equals("desktop")) စက်နှိုးကိရိယာပေးအချက်များ.add(0,"--desktop");
            ခေါ်လုပ်(အူတိုင်တန်ဖိုး,အတွင်းပိုင်းလမ်းကြောင်း(အူတိုင်တန်ဖိုး,(String)သတ်မှတ်ချက်.get("runner")),စက်နှိုးကိရိယာပေးအချက်များ,ဝန်းကျင်);
        } else if (လှုပ်ရှားမှု.equals("image")) ခေါ်လုပ်(အူတိုင်တန်ဖိုး,အတွင်းပိုင်းလမ်းကြောင်း(အူတိုင်တန်ဖိုး,(String)သတ်မှတ်ချက်.get("image_builder")),စက်နှိုးကိရိယာပေးအချက်များ,ဝန်းကျင်);
        else if (လှုပ်ရှားမှု.equals("test-system")) {
            စက်နှိုးကိရိယာပေးအချက်များ.add(0,စီမံကိန်းအမြစ်.toString()); စက်နှိုးကိရိယာပေးအချက်များ.add(0,"--edition");
            ခေါ်လုပ်(အူတိုင်တန်ဖိုး,အတွင်းပိုင်းလမ်းကြောင်း(အူတိုင်တန်ဖိုး,(String)သတ်မှတ်ချက်.get("system_tester")),စက်နှိုးကိရိယာပေးအချက်များ,ဝန်းကျင်);
        }
    }
}
