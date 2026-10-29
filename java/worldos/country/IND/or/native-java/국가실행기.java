// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.security.MessageDigest;
import java.util.*;

/** 독립 국가판의 의존성 검사·복원·ବିଲ୍ଡ୍_ସିଷ୍ଟମ·실행을 맡는 ଆୟୋଜକ Java ଉପକରଣସମୂହ. */
public final class 국가실행기 {
    static final class 자료해석기 {
        final String ଉତ୍ସ; int ଅବସ୍ଥାନ;
        자료해석기(String ପାଠ୍ଯ) { ଉତ୍ସ = ପାଠ୍ଯ; }
        void 빈칸() { while (ଅବସ୍ଥାନ < ଉତ୍ସ.length() && Character.isWhitespace(ଉତ୍ସ.charAt(ଅବସ୍ଥାନ))) ଅବସ୍ଥାନ++; }
        Object ପଢନ୍ତୁ() {
            빈칸(); char ବର୍ଣ୍ଣ_ମୂଲ୍ୟ = ଉତ୍ସ.charAt(ଅବସ୍ଥାନ++);
            if (ବର୍ଣ୍ଣ_ମୂଲ୍ୟ == '{') {
                Map<String,Object> ମାପ = new LinkedHashMap<>(); 빈칸();
                if (ଉତ୍ସ.charAt(ଅବସ୍ଥାନ) == '}') { ଅବସ୍ଥାନ++; return ମାପ; }
                while (true) {
                    String ନାମ = (String)ପଢନ୍ତୁ(); 빈칸(); if (ଉତ୍ସ.charAt(ଅବସ୍ଥାନ++) != ':') throw new IllegalArgumentException("ଡାଟା ଡେଲିମିଟର_ମୂଲ୍ୟ ତ୍ରୁଟି");
                    ମାପ.put(ନାମ, ପଢନ୍ତୁ()); 빈칸(); char ଡେଲିମିଟର_ମୂଲ୍ୟ = ଉତ୍ସ.charAt(ଅବସ୍ଥାନ++);
                    if (ଡେଲିମିଟର_ମୂଲ୍ୟ == '}') return ମାପ; if (ଡେଲିମିଟର_ମୂଲ୍ୟ != ',') throw new IllegalArgumentException("ଡାଟା ଡେଲିମିଟର_ମୂଲ୍ୟ ତ୍ରୁଟି");
                }
            }
            if (ବର୍ଣ୍ଣ_ମୂଲ୍ୟ == '[') {
                List<Object> ମାପ = new ArrayList<>(); 빈칸();
                if (ଉତ୍ସ.charAt(ଅବସ୍ଥାନ) == ']') { ଅବସ୍ଥାନ++; return ମାପ; }
                while (true) {
                    ମାପ.add(ପଢନ୍ତୁ()); 빈칸(); char ଡେଲିମିଟର_ମୂଲ୍ୟ = ଉତ୍ସ.charAt(ଅବସ୍ଥାନ++);
                    if (ଡେଲିମିଟର_ମୂଲ୍ୟ == ']') return ମାପ; if (ଡେଲିମିଟର_ମୂଲ୍ୟ != ',') throw new IllegalArgumentException("ଡାଟା ଡେଲିମିଟର_ମୂଲ୍ୟ ତ୍ରୁଟି");
                }
            }
            if (ବର୍ଣ୍ଣ_ମୂଲ୍ୟ == '"') {
                StringBuilder ମାପ = new StringBuilder();
                while (true) {
                    char ପରବର୍ତ୍ତୀ_ଆଇଟମ୍ = ଉତ୍ସ.charAt(ଅବସ୍ଥାନ++); if (ପରବର୍ତ୍ତୀ_ଆଇଟମ୍ == '"') return ମାପ.toString();
                    if (ପରବର୍ତ୍ତୀ_ଆଇଟମ୍ == '\\') {
                        ପରବର୍ତ୍ତୀ_ଆଇଟମ୍ = ଉତ୍ସ.charAt(ଅବସ୍ଥାନ++);
                        if (ପରବର୍ତ୍ତୀ_ଆଇଟମ୍ == 'u') { ମାପ.append((char)Integer.parseInt(ଉତ୍ସ.substring(ଅବସ୍ଥାନ, ଅବସ୍ଥାନ + 4),16)); ଅବସ୍ଥାନ += 4; continue; }
                        if (ପରବର୍ତ୍ତୀ_ଆଇଟମ୍ == 'n') ପରବର୍ତ୍ତୀ_ଆଇଟମ୍ = '\n'; else if (ପରବର୍ତ୍ତୀ_ଆଇଟମ୍ == 'r') ପରବର୍ତ୍ତୀ_ଆଇଟମ୍ = '\r'; else if (ପରବର୍ତ୍ତୀ_ଆଇଟମ୍ == 't') ପରବର୍ତ୍ତୀ_ଆଇଟମ୍ = '\t';
                        else if (ପରବର୍ତ୍ତୀ_ଆଇଟମ୍ == 'b') ପରବର୍ତ୍ତୀ_ଆଇଟମ୍ = '\b'; else if (ପରବର୍ତ୍ତୀ_ଆଇଟମ୍ == 'f') ପରବର୍ତ୍ତୀ_ଆଇଟମ୍ = '\f';
                        else if (ପରବର୍ତ୍ତୀ_ଆଇଟମ୍ != '"' && ପରବର୍ତ୍ତୀ_ଆଇଟମ୍ != '\\' && ପରବର୍ତ୍ତୀ_ଆଇଟମ୍ != '/') throw new IllegalArgumentException("문자 이스케이프 ତ୍ରୁଟି");
                    }
                    ମାପ.append(ପରବର୍ତ୍ତୀ_ଆଇଟମ୍);
                }
            }
            int ଚଳାନ୍ତୁ = ଅବସ୍ଥାନ - 1;
            while (ଅବସ୍ଥାନ < ଉତ୍ସ.length() && ",]} \t\r\n".indexOf(ଉତ୍ସ.charAt(ଅବସ୍ଥାନ)) < 0) ଅବସ୍ଥାନ++;
            String ମୂଲ୍ୟ = ଉତ୍ସ.substring(ଚଳାନ୍ତୁ, ଅବସ୍ଥାନ);
            if (ମୂଲ୍ୟ.equals("true")) return Boolean.TRUE; if (ମୂଲ୍ୟ.equals("false")) return Boolean.FALSE; if (ମୂଲ୍ୟ.equals("null")) return null;
            return Double.valueOf(ମୂଲ୍ୟ);
        }
    }
    static String ହାସ୍_ଫାଇଲ୍(Path ପଥ) throws Exception {
        MessageDigest 계산 = MessageDigest.getInstance("SHA-256"); byte[] ଡାଟା = new byte[1024 * 1024];
        try (InputStream 입력 = Files.newInputStream(ପଥ)) { for (int ଦୈର୍ଘ୍ୟ_ମୂଲ୍ୟ; (ଦୈର୍ଘ୍ୟ_ମୂଲ୍ୟ = 입력.read(ଡାଟା)) >= 0;) 계산.update(ଡାଟା,0,ଦୈର୍ଘ୍ୟ_ମୂଲ୍ୟ); }
        return ହାସ୍_ପାଠ(계산.digest());
    }
    static String ହାସ୍_ପାଠ(byte[] ଡାଟା) {
        StringBuilder ପାଠ୍ଯ = new StringBuilder(); for (byte ମୂଲ୍ୟ : ଡାଟା) ପାଠ୍ଯ.append(String.format(Locale.ROOT,"%02x",ମୂଲ୍ୟ & 255)); return ପାଠ୍ଯ.toString();
    }
    static Path 내부경로(Path ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍, String ନାମ) {
        Path ମାପ = ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍.resolve(ନାମ).normalize();
        if (ନାମ.isEmpty() || Paths.get(ନାମ).isAbsolute() || !ମାପ.startsWith(ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍) || ନାମ.indexOf('\\') >= 0)
            throw new IllegalArgumentException("범위를 벗어난 ପଥ: " + ନାମ);
        for (Path 부분 : Paths.get(ନାମ)) if (부분.toString().equals("..")) throw new IllegalArgumentException("상위 ପଥ 금지: " + ନାମ);
        for (Path 현재 = ମାପ; 현재 != null && 현재.startsWith(ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍); 현재 = 현재.getParent())
            if (Files.isSymbolicLink(현재)) throw new IllegalArgumentException("의존성 경로의 링크 금지: " + ନାମ);
        return ମାପ;
    }
    static String 명령출력(List<String> ନିର୍ଦ୍ଦେଶ) throws Exception {
        Process ପ୍ରୋସେସ୍_ମୂଲ୍ୟ = new ProcessBuilder(ନିର୍ଦ୍ଦେଶ).redirectError(ProcessBuilder.Redirect.INHERIT).start();
        String ମାପ = new String(ପ୍ରୋସେସ୍_ମୂଲ୍ୟ.getInputStream().readAllBytes(),StandardCharsets.UTF_8);
        if (ପ୍ରୋସେସ୍_ମୂଲ୍ୟ.waitFor() != 0) throw new IOException("ନିର୍ଦ୍ଦେଶ ବିଫଳତା_ମୂଲ୍ୟ: " + ନିର୍ଦ୍ଦେଶ.get(0)); return ମାପ;
    }
    static void ବାହାର_କରିବା(Path ଅଭିଲେଖାଗାର_ମୂଲ୍ୟ, Path ଲକ୍ଷସ୍ଥଳ_ମୂଲ୍ୟ) throws Exception {
        for (String ନାମ : 명령출력(Arrays.asList("tar","-tzf",ଅଭିଲେଖାଗାର_ମୂଲ୍ୟ.toString())).split("\n")) 내부경로(ଲକ୍ଷସ୍ଥଳ_ମୂଲ୍ୟ, ନାମ);
        for (String ରେଖା : 명령출력(Arrays.asList("tar","-tvzf",ଅଭିଲେଖାଗାର_ମୂଲ୍ୟ.toString())).split("\n"))
            if (!ରେଖା.isEmpty() && ରେଖା.charAt(0) != '-' && ରେଖା.charAt(0) != 'd') throw new IOException("외부 링크 또는 특수 파일을 포함한 의존성");
        Files.createDirectories(ଲକ୍ଷସ୍ଥଳ_ମୂଲ୍ୟ);
        int ସ୍ଥିତି_ମୂଲ୍ୟ_e10195a1 = new ProcessBuilder("tar","--no-same-owner","--no-same-permissions","-xzf",ଅଭିଲେଖାଗାର_ମୂଲ୍ୟ.toString(),"-C",ଲକ୍ଷସ୍ଥଳ_ମୂଲ୍ୟ.toString()).inheritIO().start().waitFor();
        if (ସ୍ଥିତି_ମୂଲ୍ୟ_e10195a1 != 0) throw new IOException("의존성 ଅଭିଲେଖାଗାର_ମୂଲ୍ୟ ରିଲିଜ୍_ଷ୍ଟୋରେଜ୍ ବିଫଳତା_ମୂଲ୍ୟ");
    }
    static void 호출(Path 작업경로, Path ଉପକରଣସମୂହ, List<String> 인수, Map<String,String> 환경) throws Exception {
        List<String> ନିର୍ଦ୍ଦେଶ = new ArrayList<>(Arrays.asList("python3", ଉପକରଣସମୂହ.toString())); ନିର୍ଦ୍ଦେଶ.addAll(인수);
        ProcessBuilder ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ = new ProcessBuilder(ନିର୍ଦ୍ଦେଶ).directory(작업경로.toFile()).inheritIO(); ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ.environment().putAll(환경);
        int ସ୍ଥିତି_ମୂଲ୍ୟ_e10195a1 = ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ.start().waitFor(); if (ସ୍ଥିତି_ମୂଲ୍ୟ_e10195a1 != 0) throw new IOException("ଉପକରଣସମୂହ ବିଫଳତା_ମୂଲ୍ୟ: " + ଉପକରଣସମୂହ + " (" + ସ୍ଥିତି_ମୂଲ୍ୟ_e10195a1 + ")");
    }
    @SuppressWarnings("unchecked")
    public static void main(String[] 인수) throws Exception {
        if (인수.length < 1) throw new IllegalArgumentException("build, run, desktop, image, check, test-system 중 동작을 지정하세요");
        String କାମ = 인수[0];
        if (!Arrays.asList("build","run","desktop","image","check","test-system").contains(କାମ)) throw new IllegalArgumentException("알 수 없는 କାମ");
        Path ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍ = Paths.get(System.getProperty("worldos.edition.root")).toAbsolutePath().normalize();
        Map<String,Object> ବିନ୍ଯାସ = (Map<String,Object>)new 자료해석기(Files.readString(ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍.resolve("native.json"),StandardCharsets.UTF_8)).ପଢନ୍ତୁ();
        Path ଉତ୍ସ_ବୃକ୍ଷ = 내부경로(ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍,(String)ବିନ୍ଯାସ.get("source")), କେନ୍ଦ୍ରିକ_ମୂଲ୍ୟ = 내부경로(ଉତ୍ସ_ବୃକ୍ଷ,(String)ବିନ୍ଯାସ.get("native"));
        List<String> 소유파일들 = (List<String>)(List<?>)ବିନ୍ଯାସ.get("owned_files");
        for (String ନାମ : 소유파일들) if (!Files.isRegularFile(내부경로(ଉତ୍ସ_ବୃକ୍ଷ,ନାମ))) throw new IOException("ଉତ୍ସ_ବୃକ୍ଷ 없음: " + ନାମ);
        if (କାମ.equals("check")) { System.out.println(ବିନ୍ଯାସ.get("country") + " " + ବିନ୍ଯାସ.get("language") + " 독립 ଉତ୍ସ_ବୃକ୍ଷ ଯାଞ୍ଚ୍_କରିବା 완료"); return; }
        String 자원상대 = (String)ବିନ୍ଯାସ.getOrDefault("resource_root", ".");
        if (!자원상대.equals(".") && !자원상대.equals("..")) throw new IllegalArgumentException("의존성 ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍ ପଥ ତ୍ରୁଟି");
        Path ଉତ୍ସ_ମୂଲ୍ୟ = ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍.resolve(자원상대).normalize(); Path ଅଭିଲେଖାଗାର_ମୂଲ୍ୟ = ଉତ୍ସ_ମୂଲ୍ୟ.resolve("native-vendor.tar.gz");
        String 기대해시 = (String)ବିନ୍ଯାସ.get("vendor_sha256");
        if (!ହାସ୍_ଫାଇଲ୍(ଅଭିଲେଖାଗାର_ମୂଲ୍ୟ).equals(기대해시)) throw new IOException("의존성 SHA-256 불일치");
        Path 표식 = ଉତ୍ସ_ବୃକ୍ଷ.resolve(".vendor-sha256");
        if (!Files.isRegularFile(표식) || !Files.readString(표식).trim().equals(기대해시)) { ବାହାର_କରିବା(ଅଭିଲେଖାଗାର_ମୂଲ୍ୟ, ଉତ୍ସ_ବୃକ୍ଷ); Files.writeString(표식,기대해시 + "\n"); }
        Map<String,String> 환경 = new HashMap<>(System.getenv());
        Path ipConfig = null;
        if (환경.containsKey("IP_CONFIG")) ipConfig = Paths.get(환경.get("IP_CONFIG")).toAbsolutePath().normalize();
        else for (Path parent = ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍; parent != null; parent = parent.getParent()) {
            if (Files.isRegularFile(parent.resolve("ip.conf"))) { ipConfig = parent.resolve("ip.conf"); break; }
        }
        if (ipConfig == null) ipConfig = ଉତ୍ସ_ବୃକ୍ଷ.resolve("ip.conf");
        if (!Files.isRegularFile(ipConfig)) throw new IOException("Missing ip.conf: " + ipConfig);
        환경.put("IP_CONFIG", ipConfig.toString());
        if (Arrays.asList("run","desktop","test-system").contains(କାମ) && !환경.containsKey("QEMU_AARCH64")) {
            Path ଅନୁପ୍ରୟୋଗ_ଆପ୍ଲିକେସନ୍_ଡ୍ରୟର୍ = ଉତ୍ସ_ମୂଲ୍ୟ.resolve("host/qemu"), 실행기표식 = ଉତ୍ସ_ମୂଲ୍ୟ.resolve("host/.qemu-sha256");
            String ଆପ୍ଲିକେସନ୍_ଡ୍ରୟର୍_ହାସ୍ = (String)ବିନ୍ଯାସ.get("qemu_sha256");
            if (!Files.isRegularFile(ଅନୁପ୍ରୟୋଗ_ଆପ୍ଲିକେସନ୍_ଡ୍ରୟର୍) || !Files.isRegularFile(실행기표식) || !Files.readString(실행기표식).trim().equals(ଆପ୍ଲିକେସନ୍_ଡ୍ରୟର୍_ହାସ୍)) {
                Path ଆପ୍ଲିକେସନ୍_ଡ୍ରୟର୍_ଅଭିଲେଖାଗାର = ଉତ୍ସ_ମୂଲ୍ୟ.resolve("qemu-host.tar.gz"); if (!ହାସ୍_ଫାଇଲ୍(ଆପ୍ଲିକେସନ୍_ଡ୍ରୟର୍_ଅଭିଲେଖାଗାର).equals(ଆପ୍ଲିକେସନ୍_ଡ୍ରୟର୍_ହାସ୍)) throw new IOException("QEMU SHA-256 불일치");
                ବାହାର_କରିବା(ଆପ୍ଲିକେସନ୍_ଡ୍ରୟର୍_ଅଭିଲେଖାଗାର,ଉତ୍ସ_ମୂଲ୍ୟ.resolve("host")); Files.writeString(실행기표식,ଆପ୍ଲିକେସନ୍_ଡ୍ରୟର୍_ହାସ୍ + "\n");
            }
            환경.put("QEMU_AARCH64",ଅନୁପ୍ରୟୋଗ_ଆପ୍ଲିକେସନ୍_ଡ୍ରୟର୍.toString());
        }
        MessageDigest 계산 = MessageDigest.getInstance("SHA-256"); Collections.sort(소유파일들);
        for (String ନାମ : 소유파일들) { 계산.update(ନାମ.getBytes(StandardCharsets.UTF_8)); 계산.update(Files.readAllBytes(내부경로(ଉତ୍ସ_ବୃକ୍ଷ,ନାମ))); }
        계산.update("ip.conf\0".getBytes(StandardCharsets.UTF_8)); 계산.update(Files.readAllBytes(ipConfig));
        String ଉତ୍ସ_ହାସ୍ = ହାସ୍_ପାଠ(계산.digest()); Path 빌드표식 = କେନ୍ଦ୍ରିକ_ମୂଲ୍ୟ.resolve("build/worldos-source.sha256");
        if (କାମ.equals("build") || !Files.isRegularFile(빌드표식) || !Files.readString(빌드표식).trim().equals(ଉତ୍ସ_ହାସ୍)) {
            호출(କେନ୍ଦ୍ରିକ_ମୂଲ୍ୟ,내부경로(କେନ୍ଦ୍ରିକ_ମୂଲ୍ୟ,(String)ବିନ୍ଯାସ.get("builder")),Collections.emptyList(),환경);
            Files.writeString(빌드표식,ଉତ୍ସ_ହାସ୍ + "\n");
        }
        List<String> 추가인수 = new ArrayList<>(Arrays.asList(인수).subList(1,인수.length));
        if (କାମ.equals("run") || କାମ.equals("desktop")) {
            if (କାମ.equals("desktop")) 추가인수.add(0,"--desktop");
            호출(କେନ୍ଦ୍ରିକ_ମୂଲ୍ୟ,내부경로(କେନ୍ଦ୍ରିକ_ମୂଲ୍ୟ,(String)ବିନ୍ଯାସ.get("runner")),추가인수,환경);
        } else if (କାମ.equals("image")) 호출(କେନ୍ଦ୍ରିକ_ମୂଲ୍ୟ,내부경로(କେନ୍ଦ୍ରିକ_ମୂଲ୍ୟ,(String)ବିନ୍ଯାସ.get("image_builder")),추가인수,환경);
        else if (କାମ.equals("test-system")) {
            추가인수.add(0,ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍.toString()); 추가인수.add(0,"--edition");
            호출(କେନ୍ଦ୍ରିକ_ମୂଲ୍ୟ,내부경로(କେନ୍ଦ୍ରିକ_ମୂଲ୍ୟ,(String)ବିନ୍ଯାସ.get("system_tester")),추가인수,환경);
        }
    }
}
