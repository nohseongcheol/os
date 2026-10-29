// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.security.MessageDigest;
import java.util.*;

/** 독립 국가판의 의존성 검사·복원·build_system·실행을 맡는 host Java Mga_Tool. */
public final class 국가실행기 {
    static final class data_parser {
        final String pinagmulan; int posisyon;
        data_parser(String SMS) { pinagmulan = SMS; }
        void 빈칸() { while (posisyon < pinagmulan.length() && Character.isWhitespace(pinagmulan.charAt(posisyon))) posisyon++; }
        Object 읽기() {
            빈칸(); char karakter_VALUE = pinagmulan.charAt(posisyon++);
            if (karakter_VALUE == '{') {
                Map<String,Object> sukat = new LinkedHashMap<>(); 빈칸();
                if (pinagmulan.charAt(posisyon) == '}') { posisyon++; return sukat; }
                while (true) {
                    String pangalan = (String)읽기(); 빈칸(); if (pinagmulan.charAt(posisyon++) != ':') throw new IllegalArgumentException("data panghiwalay_VALUE error");
                    sukat.put(pangalan, 읽기()); 빈칸(); char panghiwalay_VALUE = pinagmulan.charAt(posisyon++);
                    if (panghiwalay_VALUE == '}') return sukat; if (panghiwalay_VALUE != ',') throw new IllegalArgumentException("data panghiwalay_VALUE error");
                }
            }
            if (karakter_VALUE == '[') {
                List<Object> sukat = new ArrayList<>(); 빈칸();
                if (pinagmulan.charAt(posisyon) == ']') { posisyon++; return sukat; }
                while (true) {
                    sukat.add(읽기()); 빈칸(); char panghiwalay_VALUE = pinagmulan.charAt(posisyon++);
                    if (panghiwalay_VALUE == ']') return sukat; if (panghiwalay_VALUE != ',') throw new IllegalArgumentException("data panghiwalay_VALUE error");
                }
            }
            if (karakter_VALUE == '"') {
                StringBuilder sukat = new StringBuilder();
                while (true) {
                    char Susunod_item = pinagmulan.charAt(posisyon++); if (Susunod_item == '"') return sukat.toString();
                    if (Susunod_item == '\\') {
                        Susunod_item = pinagmulan.charAt(posisyon++);
                        if (Susunod_item == 'u') { sukat.append((char)Integer.parseInt(pinagmulan.substring(posisyon, posisyon + 4),16)); posisyon += 4; continue; }
                        if (Susunod_item == 'n') Susunod_item = '\n'; else if (Susunod_item == 'r') Susunod_item = '\r'; else if (Susunod_item == 't') Susunod_item = '\t';
                        else if (Susunod_item == 'b') Susunod_item = '\b'; else if (Susunod_item == 'f') Susunod_item = '\f';
                        else if (Susunod_item != '"' && Susunod_item != '\\' && Susunod_item != '/') throw new IllegalArgumentException("문자 이스케이프 error");
                    }
                    sukat.append(Susunod_item);
                }
            }
            int run = posisyon - 1;
            while (posisyon < pinagmulan.length() && ",]} \t\r\n".indexOf(pinagmulan.charAt(posisyon)) < 0) posisyon++;
            String VALUE = pinagmulan.substring(run, posisyon);
            if (VALUE.equals("true")) return Boolean.TRUE; if (VALUE.equals("false")) return Boolean.FALSE; if (VALUE.equals("null")) return null;
            return Double.valueOf(VALUE);
        }
    }
    static String hash_file(Path path) throws Exception {
        MessageDigest 계산 = MessageDigest.getInstance("SHA-256"); byte[] data = new byte[1024 * 1024];
        try (InputStream 입력 = Files.newInputStream(path)) { for (int haba_VALUE; (haba_VALUE = 입력.read(data)) >= 0;) 계산.update(data,0,haba_VALUE); }
        return hash_SMS(계산.digest());
    }
    static String hash_SMS(byte[] data) {
        StringBuilder SMS = new StringBuilder(); for (byte VALUE : data) SMS.append(String.format(Locale.ROOT,"%02x",VALUE & 255)); return SMS.toString();
    }
    static Path 내부경로(Path Project_root, String pangalan) {
        Path sukat = Project_root.resolve(pangalan).normalize();
        if (pangalan.isEmpty() || Paths.get(pangalan).isAbsolute() || !sukat.startsWith(Project_root) || pangalan.indexOf('\\') >= 0)
            throw new IllegalArgumentException("범위를 벗어난 path: " + pangalan);
        for (Path 부분 : Paths.get(pangalan)) if (부분.toString().equals("..")) throw new IllegalArgumentException("상위 path 금지: " + pangalan);
        for (Path 현재 = sukat; 현재 != null && 현재.startsWith(Project_root); 현재 = 현재.getParent())
            if (Files.isSymbolicLink(현재)) throw new IllegalArgumentException("의존성 경로의 링크 금지: " + pangalan);
        return sukat;
    }
    static String 명령출력(List<String> utos) throws Exception {
        Process Proseso_VALUE = new ProcessBuilder(utos).redirectError(ProcessBuilder.Redirect.INHERIT).start();
        String sukat = new String(Proseso_VALUE.getInputStream().readAllBytes(),StandardCharsets.UTF_8);
        if (Proseso_VALUE.waitFor() != 0) throw new IOException("utos pagpalya_VALUE: " + utos.get(0)); return sukat;
    }
    static void I_extract(Path Archive_VALUE, Path patutunguhan_VALUE) throws Exception {
        for (String pangalan : 명령출력(Arrays.asList("tar","-tzf",Archive_VALUE.toString())).split("\n")) 내부경로(patutunguhan_VALUE, pangalan);
        for (String linya : 명령출력(Arrays.asList("tar","-tvzf",Archive_VALUE.toString())).split("\n"))
            if (!linya.isEmpty() && linya.charAt(0) != '-' && linya.charAt(0) != 'd') throw new IOException("외부 링크 또는 특수 파일을 포함한 의존성");
        Files.createDirectories(patutunguhan_VALUE);
        int katayuan_VALUE = new ProcessBuilder("tar","--no-same-owner","--no-same-permissions","-xzf",Archive_VALUE.toString(),"-C",patutunguhan_VALUE.toString()).inheritIO().start().waitFor();
        if (katayuan_VALUE != 0) throw new IOException("의존성 Archive_VALUE release_Storage pagpalya_VALUE");
    }
    static void 호출(Path 작업경로, Path Mga_Tool, List<String> 인수, Map<String,String> 환경) throws Exception {
        List<String> utos = new ArrayList<>(Arrays.asList("python3", Mga_Tool.toString())); utos.addAll(인수);
        ProcessBuilder Mag_execute_utos = new ProcessBuilder(utos).directory(작업경로.toFile()).inheritIO(); Mag_execute_utos.environment().putAll(환경);
        int katayuan_VALUE = Mag_execute_utos.start().waitFor(); if (katayuan_VALUE != 0) throw new IOException("Mga_Tool pagpalya_VALUE: " + Mga_Tool + " (" + katayuan_VALUE + ")");
    }
    @SuppressWarnings("unchecked")
    public static void main(String[] 인수) throws Exception {
        if (인수.length < 1) throw new IllegalArgumentException("build, run, desktop, image, check, test-system 중 동작을 지정하세요");
        String aksyon = 인수[0];
        if (!Arrays.asList("build","run","desktop","image","check","test-system").contains(aksyon)) throw new IllegalArgumentException("알 수 없는 aksyon");
        Path Project_root = Paths.get(System.getProperty("worldos.edition.root")).toAbsolutePath().normalize();
        Map<String,Object> Mga_Setting = (Map<String,Object>)new data_parser(Files.readString(Project_root.resolve("native.json"),StandardCharsets.UTF_8)).읽기();
        Path pinagmulan_balangkas = 내부경로(Project_root,(String)Mga_Setting.get("source")), kernel_VALUE = 내부경로(pinagmulan_balangkas,(String)Mga_Setting.get("native"));
        List<String> 소유파일들 = (List<String>)(List<?>)Mga_Setting.get("owned_files");
        for (String pangalan : 소유파일들) if (!Files.isRegularFile(내부경로(pinagmulan_balangkas,pangalan))) throw new IOException("pinagmulan_balangkas 없음: " + pangalan);
        if (aksyon.equals("check")) { System.out.println(Mga_Setting.get("country") + " " + Mga_Setting.get("language") + " 독립 pinagmulan_balangkas tiyakin_kumpirmahin 완료"); return; }
        String 자원상대 = (String)Mga_Setting.getOrDefault("resource_root", ".");
        if (!자원상대.equals(".") && !자원상대.equals("..")) throw new IllegalArgumentException("의존성 Project_root path error");
        Path resource_VALUE = Project_root.resolve(자원상대).normalize(); Path Archive_VALUE = resource_VALUE.resolve("native-vendor.tar.gz");
        String 기대해시 = (String)Mga_Setting.get("vendor_sha256");
        if (!hash_file(Archive_VALUE).equals(기대해시)) throw new IOException("의존성 SHA-256 불일치");
        Path 표식 = pinagmulan_balangkas.resolve(".vendor-sha256");
        if (!Files.isRegularFile(표식) || !Files.readString(표식).trim().equals(기대해시)) { I_extract(Archive_VALUE, pinagmulan_balangkas); Files.writeString(표식,기대해시 + "\n"); }
        Map<String,String> 환경 = new HashMap<>(System.getenv());
        Path ipConfig = null;
        if (환경.containsKey("IP_CONFIG")) ipConfig = Paths.get(환경.get("IP_CONFIG")).toAbsolutePath().normalize();
        else for (Path parent = Project_root; parent != null; parent = parent.getParent()) {
            if (Files.isRegularFile(parent.resolve("ip.conf"))) { ipConfig = parent.resolve("ip.conf"); break; }
        }
        if (ipConfig == null) ipConfig = pinagmulan_balangkas.resolve("ip.conf");
        if (!Files.isRegularFile(ipConfig)) throw new IOException("Missing ip.conf: " + ipConfig);
        환경.put("IP_CONFIG", ipConfig.toString());
        if (Arrays.asList("run","desktop","test-system").contains(aksyon) && !환경.containsKey("QEMU_AARCH64")) {
            Path app_launcher = resource_VALUE.resolve("host/qemu"), 실행기표식 = resource_VALUE.resolve("host/.qemu-sha256");
            String launcher_hash = (String)Mga_Setting.get("qemu_sha256");
            if (!Files.isRegularFile(app_launcher) || !Files.isRegularFile(실행기표식) || !Files.readString(실행기표식).trim().equals(launcher_hash)) {
                Path launcher_Archive = resource_VALUE.resolve("qemu-host.tar.gz"); if (!hash_file(launcher_Archive).equals(launcher_hash)) throw new IOException("QEMU SHA-256 불일치");
                I_extract(launcher_Archive,resource_VALUE.resolve("host")); Files.writeString(실행기표식,launcher_hash + "\n");
            }
            환경.put("QEMU_AARCH64",app_launcher.toString());
        }
        MessageDigest 계산 = MessageDigest.getInstance("SHA-256"); Collections.sort(소유파일들);
        for (String pangalan : 소유파일들) { 계산.update(pangalan.getBytes(StandardCharsets.UTF_8)); 계산.update(Files.readAllBytes(내부경로(pinagmulan_balangkas,pangalan))); }
        계산.update("ip.conf\0".getBytes(StandardCharsets.UTF_8)); 계산.update(Files.readAllBytes(ipConfig));
        String pinagmulan_hash = hash_SMS(계산.digest()); Path 빌드표식 = kernel_VALUE.resolve("build/worldos-source.sha256");
        if (aksyon.equals("build") || !Files.isRegularFile(빌드표식) || !Files.readString(빌드표식).trim().equals(pinagmulan_hash)) {
            호출(kernel_VALUE,내부경로(kernel_VALUE,(String)Mga_Setting.get("builder")),Collections.emptyList(),환경);
            Files.writeString(빌드표식,pinagmulan_hash + "\n");
        }
        List<String> 추가인수 = new ArrayList<>(Arrays.asList(인수).subList(1,인수.length));
        if (aksyon.equals("run") || aksyon.equals("desktop")) {
            if (aksyon.equals("desktop")) 추가인수.add(0,"--desktop");
            호출(kernel_VALUE,내부경로(kernel_VALUE,(String)Mga_Setting.get("runner")),추가인수,환경);
        } else if (aksyon.equals("image")) 호출(kernel_VALUE,내부경로(kernel_VALUE,(String)Mga_Setting.get("image_builder")),추가인수,환경);
        else if (aksyon.equals("test-system")) {
            추가인수.add(0,Project_root.toString()); 추가인수.add(0,"--edition");
            호출(kernel_VALUE,내부경로(kernel_VALUE,(String)Mga_Setting.get("system_tester")),추가인수,환경);
        }
    }
}
