// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.security.MessageDigest;
import java.util.*;

/** 독립 국가판의 의존성 검사·복원·ᎪᏢᏍᎩ_ᏄᏍᏗᏓᏅᎢ·실행을 맡는 ᎠᏁᏢᏍᎩ Java 도구. */
public final class 국가실행기 {
    static final class 자료해석기 {
        final String ᎦᏟᏌᏅᎯ_0201f362; int 위치;
        자료해석기(String ᎠᎪᎵᏰᏗ) { ᎦᏟᏌᏅᎯ_0201f362 = ᎠᎪᎵᏰᏗ; }
        void 빈칸() { while (위치 < ᎦᏟᏌᏅᎯ_0201f362.length() && Character.isWhitespace(ᎦᏟᏌᏅᎯ_0201f362.charAt(위치))) 위치++; }
        Object 읽기() {
            빈칸(); char ᎪᏪᎸ_ᏧᎬᏩᎶᏗᏯ = ᎦᏟᏌᏅᎯ_0201f362.charAt(위치++);
            if (ᎪᏪᎸ_ᏧᎬᏩᎶᏗᏯ == '{') {
                Map<String,Object> 결과 = new LinkedHashMap<>(); 빈칸();
                if (ᎦᏟᏌᏅᎯ_0201f362.charAt(위치) == '}') { 위치++; return 결과; }
                while (true) {
                    String ᏚᏙᎥᎢ = (String)읽기(); 빈칸(); if (ᎦᏟᏌᏅᎯ_0201f362.charAt(위치++) != ':') throw new IllegalArgumentException("ᎦᏟᏌᏅᎯ ᏩᏍᏛᏍᎩᏊ_ᏧᎬᏩᎶᏗᏯ ᎦᎵᏓᏍᏔᏅ");
                    결과.put(ᏚᏙᎥᎢ, 읽기()); 빈칸(); char ᏩᏍᏛᏍᎩᏊ_ᏧᎬᏩᎶᏗᏯ = ᎦᏟᏌᏅᎯ_0201f362.charAt(위치++);
                    if (ᏩᏍᏛᏍᎩᏊ_ᏧᎬᏩᎶᏗᏯ == '}') return 결과; if (ᏩᏍᏛᏍᎩᏊ_ᏧᎬᏩᎶᏗᏯ != ',') throw new IllegalArgumentException("ᎦᏟᏌᏅᎯ ᏩᏍᏛᏍᎩᏊ_ᏧᎬᏩᎶᏗᏯ ᎦᎵᏓᏍᏔᏅ");
                }
            }
            if (ᎪᏪᎸ_ᏧᎬᏩᎶᏗᏯ == '[') {
                List<Object> 결과 = new ArrayList<>(); 빈칸();
                if (ᎦᏟᏌᏅᎯ_0201f362.charAt(위치) == ']') { 위치++; return 결과; }
                while (true) {
                    결과.add(읽기()); 빈칸(); char ᏩᏍᏛᏍᎩᏊ_ᏧᎬᏩᎶᏗᏯ = ᎦᏟᏌᏅᎯ_0201f362.charAt(위치++);
                    if (ᏩᏍᏛᏍᎩᏊ_ᏧᎬᏩᎶᏗᏯ == ']') return 결과; if (ᏩᏍᏛᏍᎩᏊ_ᏧᎬᏩᎶᏗᏯ != ',') throw new IllegalArgumentException("ᎦᏟᏌᏅᎯ ᏩᏍᏛᏍᎩᏊ_ᏧᎬᏩᎶᏗᏯ ᎦᎵᏓᏍᏔᏅ");
                }
            }
            if (ᎪᏪᎸ_ᏧᎬᏩᎶᏗᏯ == '"') {
                StringBuilder 결과 = new StringBuilder();
                while (true) {
                    char 다음 = ᎦᏟᏌᏅᎯ_0201f362.charAt(위치++); if (다음 == '"') return 결과.toString();
                    if (다음 == '\\') {
                        다음 = ᎦᏟᏌᏅᎯ_0201f362.charAt(위치++);
                        if (다음 == 'u') { 결과.append((char)Integer.parseInt(ᎦᏟᏌᏅᎯ_0201f362.substring(위치, 위치 + 4),16)); 위치 += 4; continue; }
                        if (다음 == 'n') 다음 = '\n'; else if (다음 == 'r') 다음 = '\r'; else if (다음 == 't') 다음 = '\t';
                        else if (다음 == 'b') 다음 = '\b'; else if (다음 == 'f') 다음 = '\f';
                        else if (다음 != '"' && 다음 != '\\' && 다음 != '/') throw new IllegalArgumentException("문자 이스케이프 ᎦᎵᏓᏍᏔᏅ");
                    }
                    결과.append(다음);
                }
            }
            int ᎠᎢᏎᏍᏗ = 위치 - 1;
            while (위치 < ᎦᏟᏌᏅᎯ_0201f362.length() && ",]} \t\r\n".indexOf(ᎦᏟᏌᏅᎯ_0201f362.charAt(위치)) < 0) 위치++;
            String ᏧᎬᏩᎶᏗᏯ = ᎦᏟᏌᏅᎯ_0201f362.substring(ᎠᎢᏎᏍᏗ, 위치);
            if (ᏧᎬᏩᎶᏗᏯ.equals("true")) return Boolean.TRUE; if (ᏧᎬᏩᎶᏗᏯ.equals("false")) return Boolean.FALSE; if (ᏧᎬᏩᎶᏗᏯ.equals("null")) return null;
            return Double.valueOf(ᏧᎬᏩᎶᏗᏯ);
        }
    }
    static String 해시(Path ᎠᏍᏓᏩᏛᏍᏗ) throws Exception {
        MessageDigest 계산 = MessageDigest.getInstance("SHA-256"); byte[] ᎦᏟᏌᏅᎯ = new byte[1024 * 1024];
        try (InputStream 입력 = Files.newInputStream(ᎠᏍᏓᏩᏛᏍᏗ)) { for (int ᏱᎦᏅᎯᏓ_ᏧᎬᏩᎶᏗᏯ; (ᏱᎦᏅᎯᏓ_ᏧᎬᏩᎶᏗᏯ = 입력.read(ᎦᏟᏌᏅᎯ)) >= 0;) 계산.update(ᎦᏟᏌᏅᎯ,0,ᏱᎦᏅᎯᏓ_ᏧᎬᏩᎶᏗᏯ); }
        return 해시글(계산.digest());
    }
    static String 해시글(byte[] ᎦᏟᏌᏅᎯ) {
        StringBuilder ᎠᎪᎵᏰᏗ = new StringBuilder(); for (byte ᏧᎬᏩᎶᏗᏯ : ᎦᏟᏌᏅᎯ) ᎠᎪᎵᏰᏗ.append(String.format(Locale.ROOT,"%02x",ᏧᎬᏩᎶᏗᏯ & 255)); return ᎠᎪᎵᏰᏗ.toString();
    }
    static Path 내부경로(Path 기준, String ᏚᏙᎥᎢ) {
        Path 결과 = 기준.resolve(ᏚᏙᎥᎢ).normalize();
        if (ᏚᏙᎥᎢ.isEmpty() || Paths.get(ᏚᏙᎥᎢ).isAbsolute() || !결과.startsWith(기준) || ᏚᏙᎥᎢ.indexOf('\\') >= 0)
            throw new IllegalArgumentException("범위를 벗어난 ᎠᏍᏓᏩᏛᏍᏗ: " + ᏚᏙᎥᎢ);
        for (Path 부분 : Paths.get(ᏚᏙᎥᎢ)) if (부분.toString().equals("..")) throw new IllegalArgumentException("상위 ᎠᏍᏓᏩᏛᏍᏗ 금지: " + ᏚᏙᎥᎢ);
        for (Path 현재 = 결과; 현재 != null && 현재.startsWith(기준); 현재 = 현재.getParent())
            if (Files.isSymbolicLink(현재)) throw new IllegalArgumentException("의존성 경로의 링크 금지: " + ᏚᏙᎥᎢ);
        return 결과;
    }
    static String 명령출력(List<String> ᎤᏁᏤᎸᎩ) throws Exception {
        Process ᎢᏯᏛᏁᎵᏓᏍᏗ_ᏧᎬᏩᎶᏗᏯ = new ProcessBuilder(ᎤᏁᏤᎸᎩ).redirectError(ProcessBuilder.Redirect.INHERIT).start();
        String 결과 = new String(ᎢᏯᏛᏁᎵᏓᏍᏗ_ᏧᎬᏩᎶᏗᏯ.getInputStream().readAllBytes(),StandardCharsets.UTF_8);
        if (ᎢᏯᏛᏁᎵᏓᏍᏗ_ᏧᎬᏩᎶᏗᏯ.waitFor() != 0) throw new IOException("ᎤᏁᏤᎸᎩ ᎤᏄᎸᎲᎦ_ᏧᎬᏩᎶᏗᏯ: " + ᎤᏁᏤᎸᎩ.get(0)); return 결과;
    }
    static void ᏱᎬᏅᏕᏍᏗ(Path ᎠᏍᏆᏂᎪᏛᎢ_ᏧᎬᏩᎶᏗᏯ, Path ᏮᎦᏛᎢ_ᏧᎬᏩᎶᏗᏯ) throws Exception {
        for (String ᏚᏙᎥᎢ : 명령출력(Arrays.asList("tar","-tzf",ᎠᏍᏆᏂᎪᏛᎢ_ᏧᎬᏩᎶᏗᏯ.toString())).split("\n")) 내부경로(ᏮᎦᏛᎢ_ᏧᎬᏩᎶᏗᏯ, ᏚᏙᎥᎢ);
        for (String ᏚᏓᏅᏅᎢ : 명령출력(Arrays.asList("tar","-tvzf",ᎠᏍᏆᏂᎪᏛᎢ_ᏧᎬᏩᎶᏗᏯ.toString())).split("\n"))
            if (!ᏚᏓᏅᏅᎢ.isEmpty() && ᏚᏓᏅᏅᎢ.charAt(0) != '-' && ᏚᏓᏅᏅᎢ.charAt(0) != 'd') throw new IOException("외부 링크 또는 특수 파일을 포함한 의존성");
        Files.createDirectories(ᏮᎦᏛᎢ_ᏧᎬᏩᎶᏗᏯ);
        int ᏄᏍᏗᏓᏅ_ᏧᎬᏩᎶᏗᏯ = new ProcessBuilder("tar","--no-same-owner","--no-same-permissions","-xzf",ᎠᏍᏆᏂᎪᏛᎢ_ᏧᎬᏩᎶᏗᏯ.toString(),"-C",ᏮᎦᏛᎢ_ᏧᎬᏩᎶᏗᏯ.toString()).inheritIO().start().waitFor();
        if (ᏄᏍᏗᏓᏅ_ᏧᎬᏩᎶᏗᏯ != 0) throw new IOException("의존성 ᎠᏍᏆᏂᎪᏛᎢ_ᏧᎬᏩᎶᏗᏯ 해제 ᎤᏄᎸᎲᎦ_ᏧᎬᏩᎶᏗᏯ");
    }
    static void 호출(Path 작업경로, Path 도구, List<String> 인수, Map<String,String> 환경) throws Exception {
        List<String> ᎤᏁᏤᎸᎩ = new ArrayList<>(Arrays.asList("python3", 도구.toString())); ᎤᏁᏤᎸᎩ.addAll(인수);
        ProcessBuilder ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ = new ProcessBuilder(ᎤᏁᏤᎸᎩ).directory(작업경로.toFile()).inheritIO(); ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ.environment().putAll(환경);
        int ᏄᏍᏗᏓᏅ_ᏧᎬᏩᎶᏗᏯ = ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ.start().waitFor(); if (ᏄᏍᏗᏓᏅ_ᏧᎬᏩᎶᏗᏯ != 0) throw new IOException("도구 ᎤᏄᎸᎲᎦ_ᏧᎬᏩᎶᏗᏯ: " + 도구 + " (" + ᏄᏍᏗᏓᏅ_ᏧᎬᏩᎶᏗᏯ + ")");
    }
    @SuppressWarnings("unchecked")
    public static void main(String[] 인수) throws Exception {
        if (인수.length < 1) throw new IllegalArgumentException("build, run, desktop, image, check, test-system 중 동작을 지정하세요");
        String ᎠᏛᏁᎵᏓ = 인수[0];
        if (!Arrays.asList("build","run","desktop","image","check","test-system").contains(ᎠᏛᏁᎵᏓ)) throw new IllegalArgumentException("알 수 없는 ᎠᏛᏁᎵᏓ");
        Path 기준 = Paths.get(System.getProperty("worldos.edition.root")).toAbsolutePath().normalize();
        Map<String,Object> ᏕᎦᎧᎲᎢ = (Map<String,Object>)new 자료해석기(Files.readString(기준.resolve("native.json"),StandardCharsets.UTF_8)).읽기();
        Path ᎦᏟᏌᏅᎯ_ᏡᎬ = 내부경로(기준,(String)ᏕᎦᎧᎲᎢ.get("source")), kernel_ᏧᎬᏩᎶᏗᏯ = 내부경로(ᎦᏟᏌᏅᎯ_ᏡᎬ,(String)ᏕᎦᎧᎲᎢ.get("native"));
        List<String> 소유파일들 = (List<String>)(List<?>)ᏕᎦᎧᎲᎢ.get("owned_files");
        for (String ᏚᏙᎥᎢ : 소유파일들) if (!Files.isRegularFile(내부경로(ᎦᏟᏌᏅᎯ_ᏡᎬ,ᏚᏙᎥᎢ))) throw new IOException("ᎦᏟᏌᏅᎯ_ᏡᎬ 없음: " + ᏚᏙᎥᎢ);
        if (ᎠᏛᏁᎵᏓ.equals("check")) { System.out.println(ᏕᎦᎧᎲᎢ.get("country") + " " + ᏕᎦᎧᎲᎢ.get("language") + " 독립 ᎦᏟᏌᏅᎯ_ᏡᎬ ᎰᎯᏳᏓ 완료"); return; }
        String 자원상대 = (String)ᏕᎦᎧᎲᎢ.getOrDefault("resource_root", ".");
        if (!자원상대.equals(".") && !자원상대.equals("..")) throw new IllegalArgumentException("의존성 기준 ᎠᏍᏓᏩᏛᏍᏗ ᎦᎵᏓᏍᏔᏅ");
        Path ᎠᏓᏁᏢᎢ_ᏧᎬᏩᎶᏗᏯ = 기준.resolve(자원상대).normalize(); Path ᎠᏍᏆᏂᎪᏛᎢ_ᏧᎬᏩᎶᏗᏯ = ᎠᏓᏁᏢᎢ_ᏧᎬᏩᎶᏗᏯ.resolve("native-vendor.tar.gz");
        String 기대해시 = (String)ᏕᎦᎧᎲᎢ.get("vendor_sha256");
        if (!해시(ᎠᏍᏆᏂᎪᏛᎢ_ᏧᎬᏩᎶᏗᏯ).equals(기대해시)) throw new IOException("의존성 SHA-256 불일치");
        Path 표식 = ᎦᏟᏌᏅᎯ_ᏡᎬ.resolve(".vendor-sha256");
        if (!Files.isRegularFile(표식) || !Files.readString(표식).trim().equals(기대해시)) { ᏱᎬᏅᏕᏍᏗ(ᎠᏍᏆᏂᎪᏛᎢ_ᏧᎬᏩᎶᏗᏯ, ᎦᏟᏌᏅᎯ_ᏡᎬ); Files.writeString(표식,기대해시 + "\n"); }
        Map<String,String> 환경 = new HashMap<>(System.getenv());
        Path ipConfig = null;
        if (환경.containsKey("IP_CONFIG")) ipConfig = Paths.get(환경.get("IP_CONFIG")).toAbsolutePath().normalize();
        else for (Path parent = 기준; parent != null; parent = parent.getParent()) {
            if (Files.isRegularFile(parent.resolve("ip.conf"))) { ipConfig = parent.resolve("ip.conf"); break; }
        }
        if (ipConfig == null) ipConfig = ᎦᏟᏌᏅᎯ_ᏡᎬ.resolve("ip.conf");
        if (!Files.isRegularFile(ipConfig)) throw new IOException("Missing ip.conf: " + ipConfig);
        환경.put("IP_CONFIG", ipConfig.toString());
        if (Arrays.asList("run","desktop","test-system").contains(ᎠᏛᏁᎵᏓ) && !환경.containsKey("QEMU_AARCH64")) {
            Path 실행기 = ᎠᏓᏁᏢᎢ_ᏧᎬᏩᎶᏗᏯ.resolve("host/qemu"), 실행기표식 = ᎠᏓᏁᏢᎢ_ᏧᎬᏩᎶᏗᏯ.resolve("host/.qemu-sha256");
            String 실행기해시 = (String)ᏕᎦᎧᎲᎢ.get("qemu_sha256");
            if (!Files.isRegularFile(실행기) || !Files.isRegularFile(실행기표식) || !Files.readString(실행기표식).trim().equals(실행기해시)) {
                Path 실행기압축 = ᎠᏓᏁᏢᎢ_ᏧᎬᏩᎶᏗᏯ.resolve("qemu-host.tar.gz"); if (!해시(실행기압축).equals(실행기해시)) throw new IOException("QEMU SHA-256 불일치");
                ᏱᎬᏅᏕᏍᏗ(실행기압축,ᎠᏓᏁᏢᎢ_ᏧᎬᏩᎶᏗᏯ.resolve("host")); Files.writeString(실행기표식,실행기해시 + "\n");
            }
            환경.put("QEMU_AARCH64",실행기.toString());
        }
        MessageDigest 계산 = MessageDigest.getInstance("SHA-256"); Collections.sort(소유파일들);
        for (String ᏚᏙᎥᎢ : 소유파일들) { 계산.update(ᏚᏙᎥᎢ.getBytes(StandardCharsets.UTF_8)); 계산.update(Files.readAllBytes(내부경로(ᎦᏟᏌᏅᎯ_ᏡᎬ,ᏚᏙᎥᎢ))); }
        계산.update("ip.conf\0".getBytes(StandardCharsets.UTF_8)); 계산.update(Files.readAllBytes(ipConfig));
        String 소스해시 = 해시글(계산.digest()); Path 빌드표식 = kernel_ᏧᎬᏩᎶᏗᏯ.resolve("build/worldos-source.sha256");
        if (ᎠᏛᏁᎵᏓ.equals("build") || !Files.isRegularFile(빌드표식) || !Files.readString(빌드표식).trim().equals(소스해시)) {
            호출(kernel_ᏧᎬᏩᎶᏗᏯ,내부경로(kernel_ᏧᎬᏩᎶᏗᏯ,(String)ᏕᎦᎧᎲᎢ.get("builder")),Collections.emptyList(),환경);
            Files.writeString(빌드표식,소스해시 + "\n");
        }
        List<String> 추가인수 = new ArrayList<>(Arrays.asList(인수).subList(1,인수.length));
        if (ᎠᏛᏁᎵᏓ.equals("run") || ᎠᏛᏁᎵᏓ.equals("desktop")) {
            if (ᎠᏛᏁᎵᏓ.equals("desktop")) 추가인수.add(0,"--desktop");
            호출(kernel_ᏧᎬᏩᎶᏗᏯ,내부경로(kernel_ᏧᎬᏩᎶᏗᏯ,(String)ᏕᎦᎧᎲᎢ.get("runner")),추가인수,환경);
        } else if (ᎠᏛᏁᎵᏓ.equals("image")) 호출(kernel_ᏧᎬᏩᎶᏗᏯ,내부경로(kernel_ᏧᎬᏩᎶᏗᏯ,(String)ᏕᎦᎧᎲᎢ.get("image_builder")),추가인수,환경);
        else if (ᎠᏛᏁᎵᏓ.equals("test-system")) {
            추가인수.add(0,기준.toString()); 추가인수.add(0,"--edition");
            호출(kernel_ᏧᎬᏩᎶᏗᏯ,내부경로(kernel_ᏧᎬᏩᎶᏗᏯ,(String)ᏕᎦᎧᎲᎢ.get("system_tester")),추가인수,환경);
        }
    }
}
