// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.security.MessageDigest;
import java.util.*;

/** 독립 국가판의 의존성 검사·복원·בנייה·실행을 맡는 ארח Java כלים. */
public final class מוסיקת_קאנטרי_מפעיל {
    static final class נתונים_מנתח {
        final String קודמקור; int מיקום;
        נתונים_מנתח(String טקסט) { קודמקור = טקסט; }
        void 빈칸() { while (מיקום < קודמקור.length() && Character.isWhitespace(קודמקור.charAt(מיקום))) מיקום++; }
        Object קרא() {
            빈칸(); char תו_ערך = קודמקור.charAt(מיקום++);
            if (תו_ערך == '{') {
                Map<String,Object> תוצאה = new LinkedHashMap<>(); 빈칸();
                if (קודמקור.charAt(מיקום) == '}') { מיקום++; return תוצאה; }
                while (true) {
                    String שם = (String)קרא(); 빈칸(); if (קודמקור.charAt(מיקום++) != ':') throw new IllegalArgumentException("נתונים מפריד_ערך_d8ba4873 שגיאה");
                    תוצאה.put(שם, קרא()); 빈칸(); char מפריד_ערך_d8ba4873 = קודמקור.charAt(מיקום++);
                    if (מפריד_ערך_d8ba4873 == '}') return תוצאה; if (מפריד_ערך_d8ba4873 != ',') throw new IllegalArgumentException("נתונים מפריד_ערך_d8ba4873 שגיאה");
                }
            }
            if (תו_ערך == '[') {
                List<Object> תוצאה = new ArrayList<>(); 빈칸();
                if (קודמקור.charAt(מיקום) == ']') { מיקום++; return תוצאה; }
                while (true) {
                    תוצאה.add(קרא()); 빈칸(); char מפריד_ערך_d8ba4873 = קודמקור.charAt(מיקום++);
                    if (מפריד_ערך_d8ba4873 == ']') return תוצאה; if (מפריד_ערך_d8ba4873 != ',') throw new IllegalArgumentException("נתונים מפריד_ערך_d8ba4873 שגיאה");
                }
            }
            if (תו_ערך == '"') {
                StringBuilder תוצאה = new StringBuilder();
                while (true) {
                    char הבא_פריט = קודמקור.charAt(מיקום++); if (הבא_פריט == '"') return תוצאה.toString();
                    if (הבא_פריט == '\\') {
                        הבא_פריט = קודמקור.charAt(מיקום++);
                        if (הבא_פריט == 'u') { תוצאה.append((char)Integer.parseInt(קודמקור.substring(מיקום, מיקום + 4),16)); מיקום += 4; continue; }
                        if (הבא_פריט == 'n') הבא_פריט = '\n'; else if (הבא_פריט == 'r') הבא_פריט = '\r'; else if (הבא_פריט == 't') הבא_פריט = '\t';
                        else if (הבא_פריט == 'b') הבא_פריט = '\b'; else if (הבא_פריט == 'f') הבא_פריט = '\f';
                        else if (הבא_פריט != '"' && הבא_פריט != '\\' && הבא_פריט != '/') throw new IllegalArgumentException("문자 이스케이프 שגיאה");
                    }
                    תוצאה.append(הבא_פריט);
                }
            }
            int הפעלה = מיקום - 1;
            while (מיקום < קודמקור.length() && ",]} \t\r\n".indexOf(קודמקור.charAt(מיקום)) < 0) מיקום++;
            String ערך = קודמקור.substring(הפעלה, מיקום);
            if (ערך.equals("true")) return Boolean.TRUE; if (ערך.equals("false")) return Boolean.FALSE; if (ערך.equals("null")) return null;
            return Double.valueOf(ערך);
        }
    }
    static String קוד_Hash_קובץ(Path נתיב) throws Exception {
        MessageDigest 계산 = MessageDigest.getInstance("SHA-256"); byte[] נתונים = new byte[1024 * 1024];
        try (InputStream קלט_ערך = Files.newInputStream(נתיב)) { for (int 길이; (길이 = קלט_ערך.read(נתונים)) >= 0;) 계산.update(נתונים,0,길이); }
        return קוד_Hash_טקסט(계산.digest());
    }
    static String קוד_Hash_טקסט(byte[] נתונים) {
        StringBuilder טקסט = new StringBuilder(); for (byte ערך : נתונים) טקסט.append(String.format(Locale.ROOT,"%02x",ערך & 255)); return טקסט.toString();
    }
    static Path פנימי_נתיב(Path לשקף_בסיס, String שם) {
        Path תוצאה = לשקף_בסיס.resolve(שם).normalize();
        if (שם.isEmpty() || Paths.get(שם).isAbsolute() || !תוצאה.startsWith(לשקף_בסיס) || שם.indexOf('\\') >= 0)
            throw new IllegalArgumentException("범위를 벗어난 נתיב: " + שם);
        for (Path 부분 : Paths.get(שם)) if (부분.toString().equals("..")) throw new IllegalArgumentException("상위 נתיב 금지: " + שם);
        for (Path נוכחי_פריט = תוצאה; נוכחי_פריט != null && נוכחי_פריט.startsWith(לשקף_בסיס); נוכחי_פריט = נוכחי_פריט.getParent())
            if (Files.isSymbolicLink(נוכחי_פריט)) throw new IllegalArgumentException("의존성 경로의 링크 금지: " + שם);
        return תוצאה;
    }
    static String פקודה_פלט(List<String> פקודה) throws Exception {
        Process תהליך_ערך = new ProcessBuilder(פקודה).redirectError(ProcessBuilder.Redirect.INHERIT).start();
        String תוצאה = new String(תהליך_ערך.getInputStream().readAllBytes(),StandardCharsets.UTF_8);
        if (תהליך_ערך.waitFor() != 0) throw new IOException("פקודה כשל_ערך: " + פקודה.get(0)); return תוצאה;
    }
    static void חלץ(Path ארכיון_ערך, Path יעד_ערך) throws Exception {
        for (String שם : פקודה_פלט(Arrays.asList("tar","-tzf",ארכיון_ערך.toString())).split("\n")) פנימי_נתיב(יעד_ערך, שם);
        for (String שורה : פקודה_פלט(Arrays.asList("tar","-tvzf",ארכיון_ערך.toString())).split("\n"))
            if (!שורה.isEmpty() && שורה.charAt(0) != '-' && שורה.charAt(0) != 'd') throw new IOException("חיצוני_ערך 링크 또는 특수 파일을 포함한 의존성");
        Files.createDirectories(יעד_ערך);
        int מצב_ערך = new ProcessBuilder("tar","--no-same-owner","--no-same-permissions","-xzf",ארכיון_ערך.toString(),"-C",יעד_ערך.toString()).inheritIO().start().waitFor();
        if (מצב_ערך != 0) throw new IOException("의존성 ארכיון_ערך לשחרר_אחסון כשל_ערך");
    }
    static void 호출(Path 작업경로, Path כלים, List<String> ארגומנטים, Map<String,String> סביבה) throws Exception {
        List<String> פקודה = new ArrayList<>(Arrays.asList("python3", כלים.toString())); פקודה.addAll(ארגומנטים);
        ProcessBuilder לבצע_פקודה = new ProcessBuilder(פקודה).directory(작업경로.toFile()).inheritIO(); לבצע_פקודה.environment().putAll(סביבה);
        int מצב_ערך = לבצע_פקודה.start().waitFor(); if (מצב_ערך != 0) throw new IOException("כלים כשל_ערך: " + כלים + " (" + מצב_ערך + ")");
    }
    @SuppressWarnings("unchecked")
    public static void main(String[] ארגומנטים) throws Exception {
        if (ארגומנטים.length < 1) throw new IllegalArgumentException("build, run, desktop, image, check, test-system 중 동작을 지정하세요");
        String פעולה = ארגומנטים[0];
        if (!Arrays.asList("build","run","desktop","image","check","test-system").contains(פעולה)) throw new IllegalArgumentException("알 수 없는 פעולה");
        Path לשקף_בסיס = Paths.get(System.getProperty("worldos.edition.root")).toAbsolutePath().normalize();
        Map<String,Object> הגדרות = (Map<String,Object>)new נתונים_מנתח(Files.readString(לשקף_בסיס.resolve("native.json"),StandardCharsets.UTF_8)).קרא();
        Path מקור_עץ = פנימי_נתיב(לשקף_בסיס,(String)הגדרות.get("source")), ליבה_ערך = פנימי_נתיב(מקור_עץ,(String)הגדרות.get("native"));
        List<String> 소유파일들 = (List<String>)(List<?>)הגדרות.get("owned_files");
        for (String שם : 소유파일들) if (!Files.isRegularFile(פנימי_נתיב(מקור_עץ,שם))) throw new IOException("מקור_עץ 없음: " + שם);
        if (פעולה.equals("check")) { System.out.println(הגדרות.get("country") + " " + הגדרות.get("language") + " 독립 מקור_עץ ודא_אמת 완료"); return; }
        String משאב_נתיב_יחסי = (String)הגדרות.getOrDefault("resource_root", ".");
        if (!משאב_נתיב_יחסי.equals(".") && !משאב_נתיב_יחסי.equals("..")) throw new IllegalArgumentException("의존성 לשקף_בסיס נתיב שגיאה");
        Path משאב_ערך = לשקף_בסיס.resolve(משאב_נתיב_יחסי).normalize(); Path ארכיון_ערך = משאב_ערך.resolve("native-vendor.tar.gz");
        String 기대해시 = (String)הגדרות.get("vendor_sha256");
        if (!קוד_Hash_קובץ(ארכיון_ערך).equals(기대해시)) throw new IOException("의존성 SHA-256 불일치");
        Path סמן_ערך = מקור_עץ.resolve(".vendor-sha256");
        if (!Files.isRegularFile(סמן_ערך) || !Files.readString(סמן_ערך).trim().equals(기대해시)) { חלץ(ארכיון_ערך, מקור_עץ); Files.writeString(סמן_ערך,기대해시 + "\n"); }
        Map<String,String> סביבה = new HashMap<>(System.getenv());
        Path ipConfig = null;
        if (סביבה.containsKey("IP_CONFIG")) ipConfig = Paths.get(סביבה.get("IP_CONFIG")).toAbsolutePath().normalize();
        else for (Path parent = לשקף_בסיס; parent != null; parent = parent.getParent()) {
            if (Files.isRegularFile(parent.resolve("ip.conf"))) { ipConfig = parent.resolve("ip.conf"); break; }
        }
        if (ipConfig == null) ipConfig = מקור_עץ.resolve("ip.conf");
        if (!Files.isRegularFile(ipConfig)) throw new IOException("Missing ip.conf: " + ipConfig);
        סביבה.put("IP_CONFIG", ipConfig.toString());
        if (Arrays.asList("run","desktop","test-system").contains(פעולה) && !סביבה.containsKey("QEMU_AARCH64")) {
            Path תוכנית_מפעיל = משאב_ערך.resolve("host/qemu"), מפעיל_סמן = משאב_ערך.resolve("host/.qemu-sha256");
            String מפעיל_קוד_Hash = (String)הגדרות.get("qemu_sha256");
            if (!Files.isRegularFile(תוכנית_מפעיל) || !Files.isRegularFile(מפעיל_סמן) || !Files.readString(מפעיל_סמן).trim().equals(מפעיל_קוד_Hash)) {
                Path מפעיל_ארכיון = משאב_ערך.resolve("qemu-host.tar.gz"); if (!קוד_Hash_קובץ(מפעיל_ארכיון).equals(מפעיל_קוד_Hash)) throw new IOException("QEMU SHA-256 불일치");
                חלץ(מפעיל_ארכיון,משאב_ערך.resolve("host")); Files.writeString(מפעיל_סמן,מפעיל_קוד_Hash + "\n");
            }
            סביבה.put("QEMU_AARCH64",תוכנית_מפעיל.toString());
        }
        MessageDigest 계산 = MessageDigest.getInstance("SHA-256"); Collections.sort(소유파일들);
        for (String שם : 소유파일들) { 계산.update(שם.getBytes(StandardCharsets.UTF_8)); 계산.update(Files.readAllBytes(פנימי_נתיב(מקור_עץ,שם))); }
        계산.update("ip.conf\0".getBytes(StandardCharsets.UTF_8)); 계산.update(Files.readAllBytes(ipConfig));
        String מקור_קוד_Hash = קוד_Hash_טקסט(계산.digest()); Path בנה_סמן = ליבה_ערך.resolve("build/worldos-source.sha256");
        if (פעולה.equals("build") || !Files.isRegularFile(בנה_סמן) || !Files.readString(בנה_סמן).trim().equals(מקור_קוד_Hash)) {
            호출(ליבה_ערך,פנימי_נתיב(ליבה_ערך,(String)הגדרות.get("builder")),Collections.emptyList(),סביבה);
            Files.writeString(בנה_סמן,מקור_קוד_Hash + "\n");
        }
        List<String> 추가인수 = new ArrayList<>(Arrays.asList(ארגומנטים).subList(1,ארגומנטים.length));
        if (פעולה.equals("run") || פעולה.equals("desktop")) {
            if (פעולה.equals("desktop")) 추가인수.add(0,"--desktop");
            호출(ליבה_ערך,פנימי_נתיב(ליבה_ערך,(String)הגדרות.get("runner")),추가인수,סביבה);
        } else if (פעולה.equals("image")) 호출(ליבה_ערך,פנימי_נתיב(ליבה_ערך,(String)הגדרות.get("image_builder")),추가인수,סביבה);
        else if (פעולה.equals("test-system")) {
            추가인수.add(0,לשקף_בסיס.toString()); 추가인수.add(0,"--edition");
            호출(ליבה_ערך,פנימי_נתיב(ליבה_ערך,(String)הגדרות.get("system_tester")),추가인수,סביבה);
        }
    }
}
