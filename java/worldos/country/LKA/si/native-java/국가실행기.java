// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.security.MessageDigest;
import java.util.*;

/** 독립 국가판의 의존성 검사·복원·තැනුම_පද්ධතිය·실행을 맡는 ධාරකය Java මෙවලම්. */
public final class 국가실행기 {
    static final class 자료해석기 {
        final String මූලය; int පිහිටීම;
        자료해석기(String පෙළ) { මූලය = පෙළ; }
        void 빈칸() { while (පිහිටීම < මූලය.length() && Character.isWhitespace(මූලය.charAt(පිහිටීම))) පිහිටීම++; }
        Object කියවීම() {
            빈칸(); char අනුලකුණ_අගය = මූලය.charAt(පිහිටීම++);
            if (අනුලකුණ_අගය == '{') {
                Map<String,Object> 결과 = new LinkedHashMap<>(); 빈칸();
                if (මූලය.charAt(පිහිටීම) == '}') { පිහිටීම++; return 결과; }
                while (true) {
                    String නම = (String)කියවීම(); 빈칸(); if (මූලය.charAt(පිහිටීම++) != ':') throw new IllegalArgumentException("දත්ත පරිසීමකය_අගය දෝෂය");
                    결과.put(නම, කියවීම()); 빈칸(); char පරිසීමකය_අගය = මූලය.charAt(පිහිටීම++);
                    if (පරිසීමකය_අගය == '}') return 결과; if (පරිසීමකය_අගය != ',') throw new IllegalArgumentException("දත්ත පරිසීමකය_අගය දෝෂය");
                }
            }
            if (අනුලකුණ_අගය == '[') {
                List<Object> 결과 = new ArrayList<>(); 빈칸();
                if (මූලය.charAt(පිහිටීම) == ']') { පිහිටීම++; return 결과; }
                while (true) {
                    결과.add(කියවීම()); 빈칸(); char පරිසීමකය_අගය = මූලය.charAt(පිහිටීම++);
                    if (පරිසීමකය_අගය == ']') return 결과; if (පරිසීමකය_අගය != ',') throw new IllegalArgumentException("දත්ත පරිසීමකය_අගය දෝෂය");
                }
            }
            if (අනුලකුණ_අගය == '"') {
                StringBuilder 결과 = new StringBuilder();
                while (true) {
                    char 다음 = මූලය.charAt(පිහිටීම++); if (다음 == '"') return 결과.toString();
                    if (다음 == '\\') {
                        다음 = මූලය.charAt(පිහිටීම++);
                        if (다음 == 'u') { 결과.append((char)Integer.parseInt(මූලය.substring(පිහිටීම, පිහිටීම + 4),16)); පිහිටීම += 4; continue; }
                        if (다음 == 'n') 다음 = '\n'; else if (다음 == 'r') 다음 = '\r'; else if (다음 == 't') 다음 = '\t';
                        else if (다음 == 'b') 다음 = '\b'; else if (다음 == 'f') 다음 = '\f';
                        else if (다음 != '"' && 다음 != '\\' && 다음 != '/') throw new IllegalArgumentException("문자 이스케이프 දෝෂය");
                    }
                    결과.append(다음);
                }
            }
            int ක්_රියාත්මක_කරන්න_2 = පිහිටීම - 1;
            while (පිහිටීම < මූලය.length() && ",]} \t\r\n".indexOf(මූලය.charAt(පිහිටීම)) < 0) පිහිටීම++;
            String අගය = මූලය.substring(ක්_රියාත්මක_කරන්න_2, පිහිටීම);
            if (අගය.equals("true")) return Boolean.TRUE; if (අගය.equals("false")) return Boolean.FALSE; if (අගය.equals("null")) return null;
            return Double.valueOf(අගය);
        }
    }
    static String හෑෂ්_ගොනුව(Path මාර්_ගය) throws Exception {
        MessageDigest 계산 = MessageDigest.getInstance("SHA-256"); byte[] දත්ත = new byte[1024 * 1024];
        try (InputStream 입력 = Files.newInputStream(මාර්_ගය)) { for (int දිග_අගය; (දිග_අගය = 입력.read(දත්ත)) >= 0;) 계산.update(දත්ත,0,දිග_අගය); }
        return හෑෂ්_පෙළ(계산.digest());
    }
    static String හෑෂ්_පෙළ(byte[] දත්ත) {
        StringBuilder පෙළ = new StringBuilder(); for (byte අගය : දත්ත) පෙළ.append(String.format(Locale.ROOT,"%02x",අගය & 255)); return පෙළ.toString();
    }
    static Path 내부경로(Path 기준, String නම) {
        Path 결과 = 기준.resolve(නම).normalize();
        if (නම.isEmpty() || Paths.get(නම).isAbsolute() || !결과.startsWith(기준) || නම.indexOf('\\') >= 0)
            throw new IllegalArgumentException("범위를 벗어난 මාර්_ගය: " + නම);
        for (Path 부분 : Paths.get(නම)) if (부분.toString().equals("..")) throw new IllegalArgumentException("상위 මාර්_ගය 금지: " + නම);
        for (Path 현재 = 결과; 현재 != null && 현재.startsWith(기준); 현재 = 현재.getParent())
            if (Files.isSymbolicLink(현재)) throw new IllegalArgumentException("의존성 경로의 링크 금지: " + නම);
        return 결과;
    }
    static String 명령출력(List<String> විධානය) throws Exception {
        Process ක්_රියාවලිය_අගය = new ProcessBuilder(විධානය).redirectError(ProcessBuilder.Redirect.INHERIT).start();
        String 결과 = new String(ක්_රියාවලිය_අගය.getInputStream().readAllBytes(),StandardCharsets.UTF_8);
        if (ක්_රියාවලිය_අගය.waitFor() != 0) throw new IOException("විධානය අසමත්වීම_අගය: " + විධානය.get(0)); return 결과;
    }
    static void උපුටා_ගන්න(Path සංරක්ෂිතය_අගය, Path ගමනාන්තය_අගය) throws Exception {
        for (String නම : 명령출력(Arrays.asList("tar","-tzf",සංරක්ෂිතය_අගය.toString())).split("\n")) 내부경로(ගමනාන්තය_අගය, නම);
        for (String පේළිය : 명령출력(Arrays.asList("tar","-tvzf",සංරක්ෂිතය_අගය.toString())).split("\n"))
            if (!පේළිය.isEmpty() && පේළිය.charAt(0) != '-' && පේළිය.charAt(0) != 'd') throw new IOException("외부 링크 또는 특수 파일을 포함한 의존성");
        Files.createDirectories(ගමනාන්තය_අගය);
        int තත්වය_අගය = new ProcessBuilder("tar","--no-same-owner","--no-same-permissions","-xzf",සංරක්ෂිතය_අගය.toString(),"-C",ගමනාන්තය_අගය.toString()).inheritIO().start().waitFor();
        if (තත්වය_අගය != 0) throw new IOException("의존성 සංරක්ෂිතය_අගය මුදාහැරීම_ගබඩාව අසමත්වීම_අගය");
    }
    static void 호출(Path 작업경로, Path මෙවලම්, List<String> විස්තාරක, Map<String,String> 환경) throws Exception {
        List<String> විධානය = new ArrayList<>(Arrays.asList("python3", මෙවලම්.toString())); විධානය.addAll(විස්තාරක);
        ProcessBuilder ක්_රියාත්මක_කරන්න_විධානය = new ProcessBuilder(විධානය).directory(작업경로.toFile()).inheritIO(); ක්_රියාත්මක_කරන්න_විධානය.environment().putAll(환경);
        int තත්වය_අගය = ක්_රියාත්මක_කරන්න_විධානය.start().waitFor(); if (තත්වය_අගය != 0) throw new IOException("මෙවලම් අසමත්වීම_අගය: " + මෙවලම් + " (" + තත්වය_අගය + ")");
    }
    @SuppressWarnings("unchecked")
    public static void main(String[] විස්තාරක) throws Exception {
        if (විස්තාරක.length < 1) throw new IllegalArgumentException("build, run, desktop, image, check, test-system 중 동작을 지정하세요");
        String ක්_රීයාව = විස්තාරක[0];
        if (!Arrays.asList("build","run","desktop","image","check","test-system").contains(ක්_රීයාව)) throw new IllegalArgumentException("알 수 없는 ක්_රීයාව");
        Path 기준 = Paths.get(System.getProperty("worldos.edition.root")).toAbsolutePath().normalize();
        Map<String,Object> සැකසුම් = (Map<String,Object>)new 자료해석기(Files.readString(기준.resolve("native.json"),StandardCharsets.UTF_8)).කියවීම();
        Path මූලය_රුක = 내부경로(기준,(String)සැකසුම්.get("source")), කර්නලය_අගය = 내부경로(මූලය_රුක,(String)සැකසුම්.get("native"));
        List<String> 소유파일들 = (List<String>)(List<?>)සැකසුම්.get("owned_files");
        for (String නම : 소유파일들) if (!Files.isRegularFile(내부경로(මූලය_රුක,නම))) throw new IOException("මූලය_රුක 없음: " + නම);
        if (ක්_රීයාව.equals("check")) { System.out.println(සැකසුම්.get("country") + " " + සැකසුම්.get("language") + " 독립 මූලය_රුක තහවුරු_කරන්න 완료"); return; }
        String 자원상대 = (String)සැකසුම්.getOrDefault("resource_root", ".");
        if (!자원상대.equals(".") && !자원상대.equals("..")) throw new IllegalArgumentException("의존성 기준 මාර්_ගය දෝෂය");
        Path සම්පත_අගය = 기준.resolve(자원상대).normalize(); Path සංරක්ෂිතය_අගය = සම්පත_අගය.resolve("native-vendor.tar.gz");
        String 기대해시 = (String)සැකසුම්.get("vendor_sha256");
        if (!හෑෂ්_ගොනුව(සංරක්ෂිතය_අගය).equals(기대해시)) throw new IOException("의존성 SHA-256 불일치");
        Path 표식 = මූලය_රුක.resolve(".vendor-sha256");
        if (!Files.isRegularFile(표식) || !Files.readString(표식).trim().equals(기대해시)) { උපුටා_ගන්න(සංරක්ෂිතය_අගය, මූලය_රුක); Files.writeString(표식,기대해시 + "\n"); }
        Map<String,String> 환경 = new HashMap<>(System.getenv());
        Path ipConfig = null;
        if (환경.containsKey("IP_CONFIG")) ipConfig = Paths.get(환경.get("IP_CONFIG")).toAbsolutePath().normalize();
        else for (Path parent = 기준; parent != null; parent = parent.getParent()) {
            if (Files.isRegularFile(parent.resolve("ip.conf"))) { ipConfig = parent.resolve("ip.conf"); break; }
        }
        if (ipConfig == null) ipConfig = මූලය_රුක.resolve("ip.conf");
        if (!Files.isRegularFile(ipConfig)) throw new IOException("Missing ip.conf: " + ipConfig);
        환경.put("IP_CONFIG", ipConfig.toString());
        if (Arrays.asList("run","desktop","test-system").contains(ක්_රීයාව) && !환경.containsKey("QEMU_AARCH64")) {
            Path යෙදු_යෙදුම්_ලාච්චුව = සම්පත_අගය.resolve("host/qemu"), 실행기표식 = සම්පත_අගය.resolve("host/.qemu-sha256");
            String යෙදුම්_ලාච්චුව_හෑෂ් = (String)සැකසුම්.get("qemu_sha256");
            if (!Files.isRegularFile(යෙදු_යෙදුම්_ලාච්චුව) || !Files.isRegularFile(실행기표식) || !Files.readString(실행기표식).trim().equals(යෙදුම්_ලාච්චුව_හෑෂ්)) {
                Path යෙදුම්_ලාච්චුව_සංරක්ෂිතය = සම්පත_අගය.resolve("qemu-host.tar.gz"); if (!හෑෂ්_ගොනුව(යෙදුම්_ලාච්චුව_සංරක්ෂිතය).equals(යෙදුම්_ලාච්චුව_හෑෂ්)) throw new IOException("QEMU SHA-256 불일치");
                උපුටා_ගන්න(යෙදුම්_ලාච්චුව_සංරක්ෂිතය,සම්පත_අගය.resolve("host")); Files.writeString(실행기표식,යෙදුම්_ලාච්චුව_හෑෂ් + "\n");
            }
            환경.put("QEMU_AARCH64",යෙදු_යෙදුම්_ලාච්චුව.toString());
        }
        MessageDigest 계산 = MessageDigest.getInstance("SHA-256"); Collections.sort(소유파일들);
        for (String නම : 소유파일들) { 계산.update(නම.getBytes(StandardCharsets.UTF_8)); 계산.update(Files.readAllBytes(내부경로(මූලය_රුක,නම))); }
        계산.update("ip.conf\0".getBytes(StandardCharsets.UTF_8)); 계산.update(Files.readAllBytes(ipConfig));
        String මූලය_හෑෂ් = හෑෂ්_පෙළ(계산.digest()); Path 빌드표식 = කර්නලය_අගය.resolve("build/worldos-source.sha256");
        if (ක්_රීයාව.equals("build") || !Files.isRegularFile(빌드표식) || !Files.readString(빌드표식).trim().equals(මූලය_හෑෂ්)) {
            호출(කර්නලය_අගය,내부경로(කර්නලය_අගය,(String)සැකසුම්.get("builder")),Collections.emptyList(),환경);
            Files.writeString(빌드표식,මූලය_හෑෂ් + "\n");
        }
        List<String> 추가인수 = new ArrayList<>(Arrays.asList(විස්තාරක).subList(1,විස්තාරක.length));
        if (ක්_රීයාව.equals("run") || ක්_රීයාව.equals("desktop")) {
            if (ක්_රීයාව.equals("desktop")) 추가인수.add(0,"--desktop");
            호출(කර්නලය_අගය,내부경로(කර්නලය_අගය,(String)සැකසුම්.get("runner")),추가인수,환경);
        } else if (ක්_රීයාව.equals("image")) 호출(කර්නලය_අගය,내부경로(කර්නලය_අගය,(String)සැකසුම්.get("image_builder")),추가인수,환경);
        else if (ක්_රීයාව.equals("test-system")) {
            추가인수.add(0,기준.toString()); 추가인수.add(0,"--edition");
            호출(කර්නලය_අගය,내부경로(කර්නලය_අගය,(String)සැකසුම්.get("system_tester")),추가인수,환경);
        }
    }
}
