// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.security.MessageDigest;
import java.util.*;

/** 독립 국가판의 의존성 검사·복원·ബിൽഡ്_సిస్టమ్·실행을 맡는 ഹോസ്റ്റ് Java ഉപകരണങ്ങൾ. */
public final class 국가실행기 {
    static final class ഡാറ്റാ_പാഴ്_സർ {
        final String ഉറവിടം; int സ്ഥാനം;
        ഡാറ്റാ_പാഴ്_സർ(String പദാവലി) { ഉറവിടം = പദാവലി; }
        void 빈칸() { while (സ്ഥാനം < ഉറവിടം.length() && Character.isWhitespace(ഉറവിടം.charAt(സ്ഥാനം))) സ്ഥാനം++; }
        Object വായന() {
            빈칸(); char പ്രതീകം_മൂല്യം = ഉറവിടം.charAt(സ്ഥാനം++);
            if (പ്രതീകം_മൂല്യം == '{') {
                Map<String,Object> അളവ് = new LinkedHashMap<>(); 빈칸();
                if (ഉറവിടം.charAt(സ്ഥാനം) == '}') { സ്ഥാനം++; return അളവ്; }
                while (true) {
                    String പേരു് = (String)വായന(); 빈칸(); if (ഉറവിടം.charAt(സ്ഥാനം++) != ':') throw new IllegalArgumentException("ഡാറ്റാ അതിര്_വരമ്പ്_മൂല്യം പിശക്");
                    അളവ്.put(പേരു്, വായന()); 빈칸(); char അതിര്_വരമ്പ്_മൂല്യം = ഉറവിടം.charAt(സ്ഥാനം++);
                    if (അതിര്_വരമ്പ്_മൂല്യം == '}') return അളവ്; if (അതിര്_വരമ്പ്_മൂല്യം != ',') throw new IllegalArgumentException("ഡാറ്റാ അതിര്_വരമ്പ്_മൂല്യം പിശക്");
                }
            }
            if (പ്രതീകം_മൂല്യം == '[') {
                List<Object> അളവ് = new ArrayList<>(); 빈칸();
                if (ഉറവിടം.charAt(സ്ഥാനം) == ']') { സ്ഥാനം++; return അളവ്; }
                while (true) {
                    അളവ്.add(വായന()); 빈칸(); char അതിര്_വരമ്പ്_മൂല്യം = ഉറവിടം.charAt(സ്ഥാനം++);
                    if (അതിര്_വരമ്പ്_മൂല്യം == ']') return അളവ്; if (അതിര്_വരമ്പ്_മൂല്യം != ',') throw new IllegalArgumentException("ഡാറ്റാ അതിര്_വരമ്പ്_മൂല്യം പിശക്");
                }
            }
            if (പ്രതീകം_മൂല്യം == '"') {
                StringBuilder അളവ് = new StringBuilder();
                while (true) {
                    char അടുത്തത്_ഇനം = ഉറവിടം.charAt(സ്ഥാനം++); if (അടുത്തത്_ഇനം == '"') return അളവ്.toString();
                    if (അടുത്തത്_ഇനം == '\\') {
                        അടുത്തത്_ഇനം = ഉറവിടം.charAt(സ്ഥാനം++);
                        if (അടുത്തത്_ഇനം == 'u') { അളവ്.append((char)Integer.parseInt(ഉറവിടം.substring(സ്ഥാനം, സ്ഥാനം + 4),16)); സ്ഥാനം += 4; continue; }
                        if (അടുത്തത്_ഇനം == 'n') അടുത്തത്_ഇനം = '\n'; else if (അടുത്തത്_ഇനം == 'r') അടുത്തത്_ഇനം = '\r'; else if (അടുത്തത്_ഇനം == 't') അടുത്തത്_ഇനം = '\t';
                        else if (അടുത്തത്_ഇനം == 'b') അടുത്തത്_ഇനം = '\b'; else if (അടുത്തത്_ഇനം == 'f') അടുത്തത്_ഇനം = '\f';
                        else if (അടുത്തത്_ഇനം != '"' && അടുത്തത്_ഇനം != '\\' && അടുത്തത്_ഇനം != '/') throw new IllegalArgumentException("문자 이스케이프 പിശക്");
                    }
                    അളവ്.append(അടുത്തത്_ഇനം);
                }
            }
            int നടപ്പിലാക്കുക = സ്ഥാനം - 1;
            while (സ്ഥാനം < ഉറവിടം.length() && ",]} \t\r\n".indexOf(ഉറവിടം.charAt(സ്ഥാനം)) < 0) സ്ഥാനം++;
            String മൂല്യം = ഉറവിടം.substring(നടപ്പിലാക്കുക, സ്ഥാനം);
            if (മൂല്യം.equals("true")) return Boolean.TRUE; if (മൂല്യം.equals("false")) return Boolean.FALSE; if (മൂല്യം.equals("null")) return null;
            return Double.valueOf(മൂല്യം);
        }
    }
    static String ഹാഷ്_ഫയല്(Path വഴി) throws Exception {
        MessageDigest 계산 = MessageDigest.getInstance("SHA-256"); byte[] ഡാറ്റാ = new byte[1024 * 1024];
        try (InputStream 입력 = Files.newInputStream(വഴി)) { for (int ദൈര്_ഘ്യം_മൂല്യം; (ദൈര്_ഘ്യം_മൂല്യം = 입력.read(ഡാറ്റാ)) >= 0;) 계산.update(ഡാറ്റാ,0,ദൈര്_ഘ്യം_മൂല്യം); }
        return ഹാഷ്_ലിഖിതം(계산.digest());
    }
    static String ഹാഷ്_ലിഖിതം(byte[] ഡാറ്റാ) {
        StringBuilder പദാവലി = new StringBuilder(); for (byte മൂല്യം : ഡാറ്റാ) പദാവലി.append(String.format(Locale.ROOT,"%02x",മൂല്യം & 255)); return പദാവലി.toString();
    }
    static Path 내부경로(Path പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം, String പേരു്) {
        Path അളവ് = പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം.resolve(പേരു്).normalize();
        if (പേരു്.isEmpty() || Paths.get(പേരു്).isAbsolute() || !അളവ്.startsWith(പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം) || പേരു്.indexOf('\\') >= 0)
            throw new IllegalArgumentException("범위를 벗어난 വഴി: " + പേരു്);
        for (Path 부분 : Paths.get(പേരു്)) if (부분.toString().equals("..")) throw new IllegalArgumentException("상위 വഴി 금지: " + പേരു്);
        for (Path 현재 = അളവ്; 현재 != null && 현재.startsWith(പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം); 현재 = 현재.getParent())
            if (Files.isSymbolicLink(현재)) throw new IllegalArgumentException("의존성 경로의 링크 금지: " + പേരു്);
        return അളവ്;
    }
    static String 명령출력(List<String> ആജ്ഞ) throws Exception {
        Process പ്രോസസ്_മൂല്യം = new ProcessBuilder(ആജ്ഞ).redirectError(ProcessBuilder.Redirect.INHERIT).start();
        String അളവ് = new String(പ്രോസസ്_മൂല്യം.getInputStream().readAllBytes(),StandardCharsets.UTF_8);
        if (പ്രോസസ്_മൂല്യം.waitFor() != 0) throw new IOException("ആജ്ഞ പരാജയം_മൂല്യം: " + ആജ്ഞ.get(0)); return അളവ്;
    }
    static void വേർതിരിക്കുക(Path ശേഖരം_മൂല്യം, Path ഉദ്ദിഷ്ടസ്ഥാനം_മൂല്യം) throws Exception {
        for (String പേരു് : 명령출력(Arrays.asList("tar","-tzf",ശേഖരം_മൂല്യം.toString())).split("\n")) 내부경로(ഉദ്ദിഷ്ടസ്ഥാനം_മൂല്യം, പേരു്);
        for (String ലൈൻ : 명령출력(Arrays.asList("tar","-tvzf",ശേഖരം_മൂല്യം.toString())).split("\n"))
            if (!ലൈൻ.isEmpty() && ലൈൻ.charAt(0) != '-' && ലൈൻ.charAt(0) != 'd') throw new IOException("외부 링크 또는 특수 파일을 포함한 의존성");
        Files.createDirectories(ഉദ്ദിഷ്ടസ്ഥാനം_മൂല്യം);
        int അവസ്ഥ_മൂല്യം = new ProcessBuilder("tar","--no-same-owner","--no-same-permissions","-xzf",ശേഖരം_മൂല്യം.toString(),"-C",ഉദ്ദിഷ്ടസ്ഥാനം_മൂല്യം.toString()).inheritIO().start().waitFor();
        if (അവസ്ഥ_മൂല്യം != 0) throw new IOException("의존성 ശേഖരം_മൂല്യം റിലീസ്_സംഭരണം പരാജയം_മൂല്യം");
    }
    static void 호출(Path 작업경로, Path ഉപകരണങ്ങൾ, List<String> 인수, Map<String,String> 환경) throws Exception {
        List<String> ആജ്ഞ = new ArrayList<>(Arrays.asList("python3", ഉപകരണങ്ങൾ.toString())); ആജ്ഞ.addAll(인수);
        ProcessBuilder നടപ്പാക്കുക_കമാന്_ഡ് = new ProcessBuilder(ആജ്ഞ).directory(작업경로.toFile()).inheritIO(); നടപ്പാക്കുക_കമാന്_ഡ്.environment().putAll(환경);
        int അവസ്ഥ_മൂല്യം = നടപ്പാക്കുക_കമാന്_ഡ്.start().waitFor(); if (അവസ്ഥ_മൂല്യം != 0) throw new IOException("ഉപകരണങ്ങൾ പരാജയം_മൂല്യം: " + ഉപകരണങ്ങൾ + " (" + അവസ്ഥ_മൂല്യം + ")");
    }
    @SuppressWarnings("unchecked")
    public static void main(String[] 인수) throws Exception {
        if (인수.length < 1) throw new IllegalArgumentException("build, run, desktop, image, check, test-system 중 동작을 지정하세요");
        String നടപടി = 인수[0];
        if (!Arrays.asList("build","run","desktop","image","check","test-system").contains(നടപടി)) throw new IllegalArgumentException("알 수 없는 നടപടി");
        Path പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം = Paths.get(System.getProperty("worldos.edition.root")).toAbsolutePath().normalize();
        Map<String,Object> സജ്ജീകരണം = (Map<String,Object>)new ഡാറ്റാ_പാഴ്_സർ(Files.readString(പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം.resolve("native.json"),StandardCharsets.UTF_8)).വായന();
        Path ഉറവിടം_ശാഖി = 내부경로(പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം,(String)സജ്ജീകരണം.get("source")), കെര്_ണല്_മൂല്യം = 내부경로(ഉറവിടം_ശാഖി,(String)സജ്ജീകരണം.get("native"));
        List<String> 소유파일들 = (List<String>)(List<?>)സജ്ജീകരണം.get("owned_files");
        for (String പേരു് : 소유파일들) if (!Files.isRegularFile(내부경로(ഉറവിടം_ശാഖി,പേരു്))) throw new IOException("ഉറവിടം_ശാഖി 없음: " + പേരു്);
        if (നടപടി.equals("check")) { System.out.println(സജ്ജീകരണം.get("country") + " " + സജ്ജീകരണം.get("language") + " 독립 ഉറവിടം_ശാഖി പരിശോധിക്കുക 완료"); return; }
        String ഉറവിടം_ആപേക്ഷിക_പാത = (String)സജ്ജീകരണം.getOrDefault("resource_root", ".");
        if (!ഉറവിടം_ആപേക്ഷിക_പാത.equals(".") && !ഉറവിടം_ആപേക്ഷിക_പാത.equals("..")) throw new IllegalArgumentException("의존성 പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം വഴി പിശക്");
        Path ഉറവിടം_മൂല്യം = പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം.resolve(ഉറവിടം_ആപേക്ഷിക_പാത).normalize(); Path ശേഖരം_മൂല്യം = ഉറവിടം_മൂല്യം.resolve("native-vendor.tar.gz");
        String 기대해시 = (String)സജ്ജീകരണം.get("vendor_sha256");
        if (!ഹാഷ്_ഫയല്(ശേഖരം_മൂല്യം).equals(기대해시)) throw new IOException("의존성 SHA-256 불일치");
        Path 표식 = ഉറവിടം_ശാഖി.resolve(".vendor-sha256");
        if (!Files.isRegularFile(표식) || !Files.readString(표식).trim().equals(기대해시)) { വേർതിരിക്കുക(ശേഖരം_മൂല്യം, ഉറവിടം_ശാഖി); Files.writeString(표식,기대해시 + "\n"); }
        Map<String,String> 환경 = new HashMap<>(System.getenv());
        Path ipConfig = null;
        if (환경.containsKey("IP_CONFIG")) ipConfig = Paths.get(환경.get("IP_CONFIG")).toAbsolutePath().normalize();
        else for (Path parent = പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം; parent != null; parent = parent.getParent()) {
            if (Files.isRegularFile(parent.resolve("ip.conf"))) { ipConfig = parent.resolve("ip.conf"); break; }
        }
        if (ipConfig == null) ipConfig = ഉറവിടം_ശാഖി.resolve("ip.conf");
        if (!Files.isRegularFile(ipConfig)) throw new IOException("Missing ip.conf: " + ipConfig);
        환경.put("IP_CONFIG", ipConfig.toString());
        if (Arrays.asList("run","desktop","test-system").contains(നടപടി) && !환경.containsKey("QEMU_AARCH64")) {
            Path പ്രോഗ്രാം_ആപ്പ്_ഡ്രോയർ = ഉറവിടം_മൂല്യം.resolve("host/qemu"), 실행기표식 = ഉറവിടം_മൂല്യം.resolve("host/.qemu-sha256");
            String ആപ്പ്_ഡ്രോയർ_ഹാഷ് = (String)സജ്ജീകരണം.get("qemu_sha256");
            if (!Files.isRegularFile(പ്രോഗ്രാം_ആപ്പ്_ഡ്രോയർ) || !Files.isRegularFile(실행기표식) || !Files.readString(실행기표식).trim().equals(ആപ്പ്_ഡ്രോയർ_ഹാഷ്)) {
                Path ആപ്പ്_ഡ്രോയർ_ശേഖരം = ഉറവിടം_മൂല്യം.resolve("qemu-host.tar.gz"); if (!ഹാഷ്_ഫയല്(ആപ്പ്_ഡ്രോയർ_ശേഖരം).equals(ആപ്പ്_ഡ്രോയർ_ഹാഷ്)) throw new IOException("QEMU SHA-256 불일치");
                വേർതിരിക്കുക(ആപ്പ്_ഡ്രോയർ_ശേഖരം,ഉറവിടം_മൂല്യം.resolve("host")); Files.writeString(실행기표식,ആപ്പ്_ഡ്രോയർ_ഹാഷ് + "\n");
            }
            환경.put("QEMU_AARCH64",പ്രോഗ്രാം_ആപ്പ്_ഡ്രോയർ.toString());
        }
        MessageDigest 계산 = MessageDigest.getInstance("SHA-256"); Collections.sort(소유파일들);
        for (String പേരു് : 소유파일들) { 계산.update(പേരു്.getBytes(StandardCharsets.UTF_8)); 계산.update(Files.readAllBytes(내부경로(ഉറവിടം_ശാഖി,പേരു്))); }
        계산.update("ip.conf\0".getBytes(StandardCharsets.UTF_8)); 계산.update(Files.readAllBytes(ipConfig));
        String ഉറവിടം_ഹാഷ് = ഹാഷ്_ലിഖിതം(계산.digest()); Path 빌드표식 = കെര്_ണല്_മൂല്യം.resolve("build/worldos-source.sha256");
        if (നടപടി.equals("build") || !Files.isRegularFile(빌드표식) || !Files.readString(빌드표식).trim().equals(ഉറവിടം_ഹാഷ്)) {
            호출(കെര്_ണല്_മൂല്യം,내부경로(കെര്_ണല്_മൂല്യം,(String)സജ്ജീകരണം.get("builder")),Collections.emptyList(),환경);
            Files.writeString(빌드표식,ഉറവിടം_ഹാഷ് + "\n");
        }
        List<String> 추가인수 = new ArrayList<>(Arrays.asList(인수).subList(1,인수.length));
        if (നടപടി.equals("run") || നടപടി.equals("desktop")) {
            if (നടപടി.equals("desktop")) 추가인수.add(0,"--desktop");
            호출(കെര്_ണല്_മൂല്യം,내부경로(കെര്_ണല്_മൂല്യം,(String)സജ്ജീകരണം.get("runner")),추가인수,환경);
        } else if (നടപടി.equals("image")) 호출(കെര്_ണല്_മൂല്യം,내부경로(കെര്_ണല്_മൂല്യം,(String)സജ്ജീകരണം.get("image_builder")),추가인수,환경);
        else if (നടപടി.equals("test-system")) {
            추가인수.add(0,പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം.toString()); 추가인수.add(0,"--edition");
            호출(കെര്_ണല്_മൂല്യം,내부경로(കെര്_ണല്_മൂല്യം,(String)സജ്ജീകരണം.get("system_tester")),추가인수,환경);
        }
    }
}
