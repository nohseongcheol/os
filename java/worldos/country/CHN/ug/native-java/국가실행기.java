// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.security.MessageDigest;
import java.util.*;

/** 독립 국가판의 의존성 검사·복원·نۇسخا_سىستېما·실행을 맡는 باقار Java قوراللار. */
public final class 국가실행기 {
    static final class 자료해석기 {
        final String مەنبە; int ئورۇن;
        자료해석기(String تېكىست) { مەنبە = تېكىست; }
        void 빈칸() { while (ئورۇن < مەنبە.length() && Character.isWhitespace(مەنبە.charAt(ئورۇن))) ئورۇن++; }
        Object ئوقۇ() {
            빈칸(); char ھەرپ_بەلگە_قىممىتى = مەنبە.charAt(ئورۇن++);
            if (ھەرپ_بەلگە_قىممىتى == '{') {
                Map<String,Object> ئۆلچەم = new LinkedHashMap<>(); 빈칸();
                if (مەنبە.charAt(ئورۇن) == '}') { ئورۇن++; return ئۆلچەم; }
                while (true) {
                    String ئاتى = (String)ئوقۇ(); 빈칸(); if (مەنبە.charAt(ئورۇن++) != ':') throw new IllegalArgumentException("مەلۇمات ئېنىقلىما_بەلگىسى_قىممىتى خاتالىق");
                    ئۆلچەم.put(ئاتى, ئوقۇ()); 빈칸(); char ئېنىقلىما_بەلگىسى_قىممىتى = مەنبە.charAt(ئورۇن++);
                    if (ئېنىقلىما_بەلگىسى_قىممىتى == '}') return ئۆلچەم; if (ئېنىقلىما_بەلگىسى_قىممىتى != ',') throw new IllegalArgumentException("مەلۇمات ئېنىقلىما_بەلگىسى_قىممىتى خاتالىق");
                }
            }
            if (ھەرپ_بەلگە_قىممىتى == '[') {
                List<Object> ئۆلچەم = new ArrayList<>(); 빈칸();
                if (مەنبە.charAt(ئورۇن) == ']') { ئورۇن++; return ئۆلچەم; }
                while (true) {
                    ئۆلچەم.add(ئوقۇ()); 빈칸(); char ئېنىقلىما_بەلگىسى_قىممىتى = مەنبە.charAt(ئورۇن++);
                    if (ئېنىقلىما_بەلگىسى_قىممىتى == ']') return ئۆلچەم; if (ئېنىقلىما_بەلگىسى_قىممىتى != ',') throw new IllegalArgumentException("مەلۇمات ئېنىقلىما_بەلگىسى_قىممىتى خاتالىق");
                }
            }
            if (ھەرپ_بەلگە_قىممىتى == '"') {
                StringBuilder ئۆلچەم = new StringBuilder();
                while (true) {
                    char كېيىنكى_تۈر = مەنبە.charAt(ئورۇن++); if (كېيىنكى_تۈر == '"') return ئۆلچەم.toString();
                    if (كېيىنكى_تۈر == '\\') {
                        كېيىنكى_تۈر = مەنبە.charAt(ئورۇن++);
                        if (كېيىنكى_تۈر == 'u') { ئۆلچەم.append((char)Integer.parseInt(مەنبە.substring(ئورۇن, ئورۇن + 4),16)); ئورۇن += 4; continue; }
                        if (كېيىنكى_تۈر == 'n') كېيىنكى_تۈر = '\n'; else if (كېيىنكى_تۈر == 'r') كېيىنكى_تۈر = '\r'; else if (كېيىنكى_تۈر == 't') كېيىنكى_تۈر = '\t';
                        else if (كېيىنكى_تۈر == 'b') كېيىنكى_تۈر = '\b'; else if (كېيىنكى_تۈر == 'f') كېيىنكى_تۈر = '\f';
                        else if (كېيىنكى_تۈر != '"' && كېيىنكى_تۈر != '\\' && كېيىنكى_تۈر != '/') throw new IllegalArgumentException("문자 이스케이프 خاتالىق");
                    }
                    ئۆلچەم.append(كېيىنكى_تۈر);
                }
            }
            int ئىجرا_قىل_2 = ئورۇن - 1;
            while (ئورۇن < مەنبە.length() && ",]} \t\r\n".indexOf(مەنبە.charAt(ئورۇن)) < 0) ئورۇن++;
            String قىممىتى = مەنبە.substring(ئىجرا_قىل_2, ئورۇن);
            if (قىممىتى.equals("true")) return Boolean.TRUE; if (قىممىتى.equals("false")) return Boolean.FALSE; if (قىممىتى.equals("null")) return null;
            return Double.valueOf(قىممىتى);
        }
    }
    static String چاچما_ھۆججەت(Path يول) throws Exception {
        MessageDigest 계산 = MessageDigest.getInstance("SHA-256"); byte[] مەلۇمات = new byte[1024 * 1024];
        try (InputStream 입력 = Files.newInputStream(يول)) { for (int ئۇزۇنلۇق_قىممىتى; (ئۇزۇنلۇق_قىممىتى = 입력.read(مەلۇمات)) >= 0;) 계산.update(مەلۇمات,0,ئۇزۇنلۇق_قىممىتى); }
        return چاچما_تېكست(계산.digest());
    }
    static String چاچما_تېكست(byte[] مەلۇمات) {
        StringBuilder تېكىست = new StringBuilder(); for (byte قىممىتى : مەلۇمات) تېكىست.append(String.format(Locale.ROOT,"%02x",قىممىتى & 255)); return تېكىست.toString();
    }
    static Path 내부경로(Path كۆرسىتىش_يىلتىز, String ئاتى) {
        Path ئۆلچەم = كۆرسىتىش_يىلتىز.resolve(ئاتى).normalize();
        if (ئاتى.isEmpty() || Paths.get(ئاتى).isAbsolute() || !ئۆلچەم.startsWith(كۆرسىتىش_يىلتىز) || ئاتى.indexOf('\\') >= 0)
            throw new IllegalArgumentException("범위를 벗어난 يول: " + ئاتى);
        for (Path 부분 : Paths.get(ئاتى)) if (부분.toString().equals("..")) throw new IllegalArgumentException("상위 يول 금지: " + ئاتى);
        for (Path 현재 = ئۆلچەم; 현재 != null && 현재.startsWith(كۆرسىتىش_يىلتىز); 현재 = 현재.getParent())
            if (Files.isSymbolicLink(현재)) throw new IllegalArgumentException("의존성 경로의 링크 금지: " + ئاتى);
        return ئۆلچەم;
    }
    static String 명령출력(List<String> بۇيرۇق) throws Exception {
        Process جەريان_قىممىتى = new ProcessBuilder(بۇيرۇق).redirectError(ProcessBuilder.Redirect.INHERIT).start();
        String ئۆلچەم = new String(جەريان_قىممىتى.getInputStream().readAllBytes(),StandardCharsets.UTF_8);
        if (جەريان_قىممىتى.waitFor() != 0) throw new IOException("بۇيرۇق مەغلۇپ_بولۇش_قىممىتى: " + بۇيرۇق.get(0)); return ئۆلچەم;
    }
    static void يايماق(Path ئارخىپ_قىممىتى, Path نىشان_قىممىتى) throws Exception {
        for (String ئاتى : 명령출력(Arrays.asList("tar","-tzf",ئارخىپ_قىممىتى.toString())).split("\n")) 내부경로(نىشان_قىممىتى, ئاتى);
        for (String قۇر : 명령출력(Arrays.asList("tar","-tvzf",ئارخىپ_قىممىتى.toString())).split("\n"))
            if (!قۇر.isEmpty() && قۇر.charAt(0) != '-' && قۇر.charAt(0) != 'd') throw new IOException("외부 링크 또는 특수 파일을 포함한 의존성");
        Files.createDirectories(نىشان_قىممىتى);
        int ھالەت_قىممىتى = new ProcessBuilder("tar","--no-same-owner","--no-same-permissions","-xzf",ئارخىپ_قىممىتى.toString(),"-C",نىشان_قىممىتى.toString()).inheritIO().start().waitFor();
        if (ھالەت_قىممىتى != 0) throw new IOException("의존성 ئارخىپ_قىممىتى تارقىتىش_بوشلۇق مەغلۇپ_بولۇش_قىممىتى");
    }
    static void 호출(Path 작업경로, Path قوراللار, List<String> ئۆزگەرگۈچىلەر, Map<String,String> 환경) throws Exception {
        List<String> بۇيرۇق = new ArrayList<>(Arrays.asList("python3", قوراللار.toString())); بۇيرۇق.addAll(ئۆزگەرگۈچىلەر);
        ProcessBuilder ئىجرا_قىلىش_بۇيرۇق = new ProcessBuilder(بۇيرۇق).directory(작업경로.toFile()).inheritIO(); ئىجرا_قىلىش_بۇيرۇق.environment().putAll(환경);
        int ھالەت_قىممىتى = ئىجرا_قىلىش_بۇيرۇق.start().waitFor(); if (ھالەت_قىممىتى != 0) throw new IOException("قوراللار مەغلۇپ_بولۇش_قىممىتى: " + قوراللار + " (" + ھالەت_قىممىتى + ")");
    }
    @SuppressWarnings("unchecked")
    public static void main(String[] ئۆزگەرگۈچىلەر) throws Exception {
        if (ئۆزگەرگۈچىلەر.length < 1) throw new IllegalArgumentException("build, run, desktop, image, check, test-system 중 동작을 지정하세요");
        String مەشغۇلات = ئۆزگەرگۈچىلەر[0];
        if (!Arrays.asList("build","run","desktop","image","check","test-system").contains(مەشغۇلات)) throw new IllegalArgumentException("알 수 없는 مەشغۇلات");
        Path كۆرسىتىش_يىلتىز = Paths.get(System.getProperty("worldos.edition.root")).toAbsolutePath().normalize();
        Map<String,Object> تەڭشەكلەر = (Map<String,Object>)new 자료해석기(Files.readString(كۆرسىتىش_يىلتىز.resolve("native.json"),StandardCharsets.UTF_8)).ئوقۇ();
        Path مەنبە_دەرەخ = 내부경로(كۆرسىتىش_يىلتىز,(String)تەڭشەكلەر.get("source")), يادرو_قىممىتى = 내부경로(مەنبە_دەرەخ,(String)تەڭشەكلەر.get("native"));
        List<String> 소유파일들 = (List<String>)(List<?>)تەڭشەكلەر.get("owned_files");
        for (String ئاتى : 소유파일들) if (!Files.isRegularFile(내부경로(مەنبە_دەرەخ,ئاتى))) throw new IOException("مەنبە_دەرەخ 없음: " + ئاتى);
        if (مەشغۇلات.equals("check")) { System.out.println(تەڭشەكلەر.get("country") + " " + تەڭشەكلەر.get("language") + " 독립 مەنبە_دەرەخ دەلىللىمەك 완료"); return; }
        String 자원상대 = (String)تەڭشەكلەر.getOrDefault("resource_root", ".");
        if (!자원상대.equals(".") && !자원상대.equals("..")) throw new IllegalArgumentException("의존성 كۆرسىتىش_يىلتىز يول خاتالىق");
        Path مەنبە_قىممىتى = كۆرسىتىش_يىلتىز.resolve(자원상대).normalize(); Path ئارخىپ_قىممىتى = مەنبە_قىممىتى.resolve("native-vendor.tar.gz");
        String 기대해시 = (String)تەڭشەكلەر.get("vendor_sha256");
        if (!چاچما_ھۆججەت(ئارخىپ_قىممىتى).equals(기대해시)) throw new IOException("의존성 SHA-256 불일치");
        Path 표식 = مەنبە_دەرەخ.resolve(".vendor-sha256");
        if (!Files.isRegularFile(표식) || !Files.readString(표식).trim().equals(기대해시)) { يايماق(ئارخىپ_قىممىتى, مەنبە_دەرەخ); Files.writeString(표식,기대해시 + "\n"); }
        Map<String,String> 환경 = new HashMap<>(System.getenv());
        Path ipConfig = null;
        if (환경.containsKey("IP_CONFIG")) ipConfig = Paths.get(환경.get("IP_CONFIG")).toAbsolutePath().normalize();
        else for (Path parent = كۆرسىتىش_يىلتىز; parent != null; parent = parent.getParent()) {
            if (Files.isRegularFile(parent.resolve("ip.conf"))) { ipConfig = parent.resolve("ip.conf"); break; }
        }
        if (ipConfig == null) ipConfig = مەنبە_دەرەخ.resolve("ip.conf");
        if (!Files.isRegularFile(ipConfig)) throw new IOException("Missing ip.conf: " + ipConfig);
        환경.put("IP_CONFIG", ipConfig.toString());
        if (Arrays.asList("run","desktop","test-system").contains(مەشغۇلات) && !환경.containsKey("QEMU_AARCH64")) {
            Path ئەپ_خادىم = مەنبە_قىممىتى.resolve("host/qemu"), 실행기표식 = مەنبە_قىممىتى.resolve("host/.qemu-sha256");
            String خادىم_چاچما = (String)تەڭشەكلەر.get("qemu_sha256");
            if (!Files.isRegularFile(ئەپ_خادىم) || !Files.isRegularFile(실행기표식) || !Files.readString(실행기표식).trim().equals(خادىم_چاچما)) {
                Path خادىم_ئارخىپ = مەنبە_قىممىتى.resolve("qemu-host.tar.gz"); if (!چاچما_ھۆججەت(خادىم_ئارخىپ).equals(خادىم_چاچما)) throw new IOException("QEMU SHA-256 불일치");
                يايماق(خادىم_ئارخىپ,مەنبە_قىممىتى.resolve("host")); Files.writeString(실행기표식,خادىم_چاچما + "\n");
            }
            환경.put("QEMU_AARCH64",ئەپ_خادىم.toString());
        }
        MessageDigest 계산 = MessageDigest.getInstance("SHA-256"); Collections.sort(소유파일들);
        for (String ئاتى : 소유파일들) { 계산.update(ئاتى.getBytes(StandardCharsets.UTF_8)); 계산.update(Files.readAllBytes(내부경로(مەنبە_دەرەخ,ئاتى))); }
        계산.update("ip.conf\0".getBytes(StandardCharsets.UTF_8)); 계산.update(Files.readAllBytes(ipConfig));
        String مەنبە_چاچما = چاچما_تېكست(계산.digest()); Path 빌드표식 = يادرو_قىممىتى.resolve("build/worldos-source.sha256");
        if (مەشغۇلات.equals("build") || !Files.isRegularFile(빌드표식) || !Files.readString(빌드표식).trim().equals(مەنبە_چاچما)) {
            호출(يادرو_قىممىتى,내부경로(يادرو_قىممىتى,(String)تەڭشەكلەر.get("builder")),Collections.emptyList(),환경);
            Files.writeString(빌드표식,مەنبە_چاچما + "\n");
        }
        List<String> 추가인수 = new ArrayList<>(Arrays.asList(ئۆزگەرگۈچىلەر).subList(1,ئۆزگەرگۈچىلەر.length));
        if (مەشغۇلات.equals("run") || مەشغۇلات.equals("desktop")) {
            if (مەشغۇلات.equals("desktop")) 추가인수.add(0,"--desktop");
            호출(يادرو_قىممىتى,내부경로(يادرو_قىممىتى,(String)تەڭشەكلەر.get("runner")),추가인수,환경);
        } else if (مەشغۇلات.equals("image")) 호출(يادرو_قىممىتى,내부경로(يادرو_قىممىتى,(String)تەڭشەكلەر.get("image_builder")),추가인수,환경);
        else if (مەشغۇلات.equals("test-system")) {
            추가인수.add(0,كۆرسىتىش_يىلتىز.toString()); 추가인수.add(0,"--edition");
            호출(يادرو_قىممىتى,내부경로(يادرو_قىممىتى,(String)تەڭشەكلەر.get("system_tester")),추가인수,환경);
        }
    }
}
