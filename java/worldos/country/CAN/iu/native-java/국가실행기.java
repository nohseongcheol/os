// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.security.MessageDigest;
import java.util.*;

/** 독립 국가판의 의존성 검사·복원·sanali_qarasaujaq·실행을 맡는 tuttarvik Java 도구. */
public final class 국가실행기 {
    static final class 자료해석기 {
        final String pivviujuq; int 위치;
        자료해석기(String titiqqaq) { pivviujuq = titiqqaq; }
        void 빈칸() { while (위치 < pivviujuq.length() && Character.isWhitespace(pivviujuq.charAt(위치))) 위치++; }
        Object 읽기() {
            빈칸(); char immikkuuqtuq_atuutilik = pivviujuq.charAt(위치++);
            if (immikkuuqtuq_atuutilik == '{') {
                Map<String,Object> 결과 = new LinkedHashMap<>(); 빈칸();
                if (pivviujuq.charAt(위치) == '}') { 위치++; return 결과; }
                while (true) {
                    String atiq = (String)읽기(); 빈칸(); if (pivviujuq.charAt(위치++) != ':') throw new IllegalArgumentException("titiqqat isuaguurut_atuutilik tammarniq");
                    결과.put(atiq, 읽기()); 빈칸(); char isuaguurut_atuutilik = pivviujuq.charAt(위치++);
                    if (isuaguurut_atuutilik == '}') return 결과; if (isuaguurut_atuutilik != ',') throw new IllegalArgumentException("titiqqat isuaguurut_atuutilik tammarniq");
                }
            }
            if (immikkuuqtuq_atuutilik == '[') {
                List<Object> 결과 = new ArrayList<>(); 빈칸();
                if (pivviujuq.charAt(위치) == ']') { 위치++; return 결과; }
                while (true) {
                    결과.add(읽기()); 빈칸(); char isuaguurut_atuutilik = pivviujuq.charAt(위치++);
                    if (isuaguurut_atuutilik == ']') return 결과; if (isuaguurut_atuutilik != ',') throw new IllegalArgumentException("titiqqat isuaguurut_atuutilik tammarniq");
                }
            }
            if (immikkuuqtuq_atuutilik == '"') {
                StringBuilder 결과 = new StringBuilder();
                while (true) {
                    char 다음 = pivviujuq.charAt(위치++); if (다음 == '"') return 결과.toString();
                    if (다음 == '\\') {
                        다음 = pivviujuq.charAt(위치++);
                        if (다음 == 'u') { 결과.append((char)Integer.parseInt(pivviujuq.substring(위치, 위치 + 4),16)); 위치 += 4; continue; }
                        if (다음 == 'n') 다음 = '\n'; else if (다음 == 'r') 다음 = '\r'; else if (다음 == 't') 다음 = '\t';
                        else if (다음 == 'b') 다음 = '\b'; else if (다음 == 'f') 다음 = '\f';
                        else if (다음 != '"' && 다음 != '\\' && 다음 != '/') throw new IllegalArgumentException("문자 이스케이프 tammarniq");
                    }
                    결과.append(다음);
                }
            }
            int 시작 = 위치 - 1;
            while (위치 < pivviujuq.length() && ",]} \t\r\n".indexOf(pivviujuq.charAt(위치)) < 0) 위치++;
            String atuutilik = pivviujuq.substring(시작, 위치);
            if (atuutilik.equals("true")) return Boolean.TRUE; if (atuutilik.equals("false")) return Boolean.FALSE; if (atuutilik.equals("null")) return null;
            return Double.valueOf(atuutilik);
        }
    }
    static String 해시(Path aqqut) throws Exception {
        MessageDigest 계산 = MessageDigest.getInstance("SHA-256"); byte[] titiqqat = new byte[1024 * 1024];
        try (InputStream 입력 = Files.newInputStream(aqqut)) { for (int takininga_atuutilik; (takininga_atuutilik = 입력.read(titiqqat)) >= 0;) 계산.update(titiqqat,0,takininga_atuutilik); }
        return 해시글(계산.digest());
    }
    static String 해시글(byte[] titiqqat) {
        StringBuilder titiqqaq = new StringBuilder(); for (byte atuutilik : titiqqat) titiqqaq.append(String.format(Locale.ROOT,"%02x",atuutilik & 255)); return titiqqaq.toString();
    }
    static Path 내부경로(Path 기준, String atiq) {
        Path 결과 = 기준.resolve(atiq).normalize();
        if (atiq.isEmpty() || Paths.get(atiq).isAbsolute() || !결과.startsWith(기준) || atiq.indexOf('\\') >= 0)
            throw new IllegalArgumentException("범위를 벗어난 aqqut: " + atiq);
        for (Path 부분 : Paths.get(atiq)) if (부분.toString().equals("..")) throw new IllegalArgumentException("상위 aqqut 금지: " + atiq);
        for (Path 현재 = 결과; 현재 != null && 현재.startsWith(기준); 현재 = 현재.getParent())
            if (Files.isSymbolicLink(현재)) throw new IllegalArgumentException("의존성 경로의 링크 금지: " + atiq);
        return 결과;
    }
    static String 명령출력(List<String> piqujijjut) throws Exception {
        Process Pivallianiq_atuutilik = new ProcessBuilder(piqujijjut).redirectError(ProcessBuilder.Redirect.INHERIT).start();
        String 결과 = new String(Pivallianiq_atuutilik.getInputStream().readAllBytes(),StandardCharsets.UTF_8);
        if (Pivallianiq_atuutilik.waitFor() != 0) throw new IOException("piqujijjut itigaqtuq_atuutilik: " + piqujijjut.get(0)); return 결과;
    }
    static void 풀기(Path tuqqurli_atuutilik_e917f8d5, Path namunngarvik_atuutilik) throws Exception {
        for (String atiq : 명령출력(Arrays.asList("tar","-tzf",tuqqurli_atuutilik_e917f8d5.toString())).split("\n")) 내부경로(namunngarvik_atuutilik, atiq);
        for (String titikutaak : 명령출력(Arrays.asList("tar","-tvzf",tuqqurli_atuutilik_e917f8d5.toString())).split("\n"))
            if (!titikutaak.isEmpty() && titikutaak.charAt(0) != '-' && titikutaak.charAt(0) != 'd') throw new IOException("외부 링크 또는 특수 파일을 포함한 의존성");
        Files.createDirectories(namunngarvik_atuutilik);
        int qanuilinganiq_atuutilik = new ProcessBuilder("tar","--no-same-owner","--no-same-permissions","-xzf",tuqqurli_atuutilik_e917f8d5.toString(),"-C",namunngarvik_atuutilik.toString()).inheritIO().start().waitFor();
        if (qanuilinganiq_atuutilik != 0) throw new IOException("의존성 tuqqurli_atuutilik_e917f8d5 해제 itigaqtuq_atuutilik");
    }
    static void 호출(Path 작업경로, Path 도구, List<String> 인수, Map<String,String> 환경) throws Exception {
        List<String> piqujijjut = new ArrayList<>(Arrays.asList("python3", 도구.toString())); piqujijjut.addAll(인수);
        ProcessBuilder 실행 = new ProcessBuilder(piqujijjut).directory(작업경로.toFile()).inheritIO(); 실행.environment().putAll(환경);
        int qanuilinganiq_atuutilik = 실행.start().waitFor(); if (qanuilinganiq_atuutilik != 0) throw new IOException("도구 itigaqtuq_atuutilik: " + 도구 + " (" + qanuilinganiq_atuutilik + ")");
    }
    @SuppressWarnings("unchecked")
    public static void main(String[] 인수) throws Exception {
        if (인수.length < 1) throw new IllegalArgumentException("build, run, desktop, image, check, test-system 중 동작을 지정하세요");
        String sugiarut = 인수[0];
        if (!Arrays.asList("build","run","desktop","image","check","test-system").contains(sugiarut)) throw new IllegalArgumentException("알 수 없는 sugiarut");
        Path 기준 = Paths.get(System.getProperty("worldos.edition.root")).toAbsolutePath().normalize();
        Map<String,Object> 설정 = (Map<String,Object>)new 자료해석기(Files.readString(기준.resolve("native.json"),StandardCharsets.UTF_8)).읽기();
        Path pivviujuq_attavigiit = 내부경로(기준,(String)설정.get("source")), kernel_atuutilik = 내부경로(pivviujuq_attavigiit,(String)설정.get("native"));
        List<String> 소유파일들 = (List<String>)(List<?>)설정.get("owned_files");
        for (String atiq : 소유파일들) if (!Files.isRegularFile(내부경로(pivviujuq_attavigiit,atiq))) throw new IOException("pivviujuq_attavigiit 없음: " + atiq);
        if (sugiarut.equals("check")) { System.out.println(설정.get("country") + " " + 설정.get("language") + " 독립 pivviujuq_attavigiit nalunairli_1aacb54c 완료"); return; }
        String 자원상대 = (String)설정.getOrDefault("resource_root", ".");
        if (!자원상대.equals(".") && !자원상대.equals("..")) throw new IllegalArgumentException("의존성 기준 aqqut tammarniq");
        Path qarasaujalirijjutiit_atuutilik = 기준.resolve(자원상대).normalize(); Path tuqqurli_atuutilik_e917f8d5 = qarasaujalirijjutiit_atuutilik.resolve("native-vendor.tar.gz");
        String 기대해시 = (String)설정.get("vendor_sha256");
        if (!해시(tuqqurli_atuutilik_e917f8d5).equals(기대해시)) throw new IOException("의존성 SHA-256 불일치");
        Path 표식 = pivviujuq_attavigiit.resolve(".vendor-sha256");
        if (!Files.isRegularFile(표식) || !Files.readString(표식).trim().equals(기대해시)) { 풀기(tuqqurli_atuutilik_e917f8d5, pivviujuq_attavigiit); Files.writeString(표식,기대해시 + "\n"); }
        Map<String,String> 환경 = new HashMap<>(System.getenv());
        Path ipConfig = null;
        if (환경.containsKey("IP_CONFIG")) ipConfig = Paths.get(환경.get("IP_CONFIG")).toAbsolutePath().normalize();
        else for (Path parent = 기준; parent != null; parent = parent.getParent()) {
            if (Files.isRegularFile(parent.resolve("ip.conf"))) { ipConfig = parent.resolve("ip.conf"); break; }
        }
        if (ipConfig == null) ipConfig = pivviujuq_attavigiit.resolve("ip.conf");
        if (!Files.isRegularFile(ipConfig)) throw new IOException("Missing ip.conf: " + ipConfig);
        환경.put("IP_CONFIG", ipConfig.toString());
        if (Arrays.asList("run","desktop","test-system").contains(sugiarut) && !환경.containsKey("QEMU_AARCH64")) {
            Path 실행기 = qarasaujalirijjutiit_atuutilik.resolve("host/qemu"), 실행기표식 = qarasaujalirijjutiit_atuutilik.resolve("host/.qemu-sha256");
            String 실행기해시 = (String)설정.get("qemu_sha256");
            if (!Files.isRegularFile(실행기) || !Files.isRegularFile(실행기표식) || !Files.readString(실행기표식).trim().equals(실행기해시)) {
                Path 실행기압축 = qarasaujalirijjutiit_atuutilik.resolve("qemu-host.tar.gz"); if (!해시(실행기압축).equals(실행기해시)) throw new IOException("QEMU SHA-256 불일치");
                풀기(실행기압축,qarasaujalirijjutiit_atuutilik.resolve("host")); Files.writeString(실행기표식,실행기해시 + "\n");
            }
            환경.put("QEMU_AARCH64",실행기.toString());
        }
        MessageDigest 계산 = MessageDigest.getInstance("SHA-256"); Collections.sort(소유파일들);
        for (String atiq : 소유파일들) { 계산.update(atiq.getBytes(StandardCharsets.UTF_8)); 계산.update(Files.readAllBytes(내부경로(pivviujuq_attavigiit,atiq))); }
        계산.update("ip.conf\0".getBytes(StandardCharsets.UTF_8)); 계산.update(Files.readAllBytes(ipConfig));
        String 소스해시 = 해시글(계산.digest()); Path 빌드표식 = kernel_atuutilik.resolve("build/worldos-source.sha256");
        if (sugiarut.equals("build") || !Files.isRegularFile(빌드표식) || !Files.readString(빌드표식).trim().equals(소스해시)) {
            호출(kernel_atuutilik,내부경로(kernel_atuutilik,(String)설정.get("builder")),Collections.emptyList(),환경);
            Files.writeString(빌드표식,소스해시 + "\n");
        }
        List<String> 추가인수 = new ArrayList<>(Arrays.asList(인수).subList(1,인수.length));
        if (sugiarut.equals("run") || sugiarut.equals("desktop")) {
            if (sugiarut.equals("desktop")) 추가인수.add(0,"--desktop");
            호출(kernel_atuutilik,내부경로(kernel_atuutilik,(String)설정.get("runner")),추가인수,환경);
        } else if (sugiarut.equals("image")) 호출(kernel_atuutilik,내부경로(kernel_atuutilik,(String)설정.get("image_builder")),추가인수,환경);
        else if (sugiarut.equals("test-system")) {
            추가인수.add(0,기준.toString()); 추가인수.add(0,"--edition");
            호출(kernel_atuutilik,내부경로(kernel_atuutilik,(String)설정.get("system_tester")),추가인수,환경);
        }
    }
}
