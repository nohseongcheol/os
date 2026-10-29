// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.security.MessageDigest;
import java.util.*;

/** 독립 국가판의 의존성 검사·복원·направити_систем·실행을 맡는 хост_рачунар Java 도구. */
public final class 국가실행기 {
    static final class 자료해석기 {
        final String извор; int 위치;
        자료해석기(String текст) { извор = текст; }
        void 빈칸() { while (위치 < извор.length() && Character.isWhitespace(извор.charAt(위치))) 위치++; }
        Object 읽기() {
            빈칸(); char знак_вриједност = извор.charAt(위치++);
            if (знак_вриједност == '{') {
                Map<String,Object> 결과 = new LinkedHashMap<>(); 빈칸();
                if (извор.charAt(위치) == '}') { 위치++; return 결과; }
                while (true) {
                    String назив = (String)읽기(); 빈칸(); if (извор.charAt(위치++) != ':') throw new IllegalArgumentException("подаци граничник_вриједност грешка");
                    결과.put(назив, 읽기()); 빈칸(); char граничник_вриједност = извор.charAt(위치++);
                    if (граничник_вриједност == '}') return 결과; if (граничник_вриједност != ',') throw new IllegalArgumentException("подаци граничник_вриједност грешка");
                }
            }
            if (знак_вриједност == '[') {
                List<Object> 결과 = new ArrayList<>(); 빈칸();
                if (извор.charAt(위치) == ']') { 위치++; return 결과; }
                while (true) {
                    결과.add(읽기()); 빈칸(); char граничник_вриједност = извор.charAt(위치++);
                    if (граничник_вриједност == ']') return 결과; if (граничник_вриједност != ',') throw new IllegalArgumentException("подаци граничник_вриједност грешка");
                }
            }
            if (знак_вриједност == '"') {
                StringBuilder 결과 = new StringBuilder();
                while (true) {
                    char 다음 = извор.charAt(위치++); if (다음 == '"') return 결과.toString();
                    if (다음 == '\\') {
                        다음 = извор.charAt(위치++);
                        if (다음 == 'u') { 결과.append((char)Integer.parseInt(извор.substring(위치, 위치 + 4),16)); 위치 += 4; continue; }
                        if (다음 == 'n') 다음 = '\n'; else if (다음 == 'r') 다음 = '\r'; else if (다음 == 't') 다음 = '\t';
                        else if (다음 == 'b') 다음 = '\b'; else if (다음 == 'f') 다음 = '\f';
                        else if (다음 != '"' && 다음 != '\\' && 다음 != '/') throw new IllegalArgumentException("문자 이스케이프 грешка");
                    }
                    결과.append(다음);
                }
            }
            int 시작 = 위치 - 1;
            while (위치 < извор.length() && ",]} \t\r\n".indexOf(извор.charAt(위치)) < 0) 위치++;
            String вриједност = извор.substring(시작, 위치);
            if (вриједност.equals("true")) return Boolean.TRUE; if (вриједност.equals("false")) return Boolean.FALSE; if (вриједност.equals("null")) return null;
            return Double.valueOf(вриједност);
        }
    }
    static String 해시(Path пут) throws Exception {
        MessageDigest 계산 = MessageDigest.getInstance("SHA-256"); byte[] подаци = new byte[1024 * 1024];
        try (InputStream 입력 = Files.newInputStream(пут)) { for (int дужина_вриједност; (дужина_вриједност = 입력.read(подаци)) >= 0;) 계산.update(подаци,0,дужина_вриједност); }
        return 해시글(계산.digest());
    }
    static String 해시글(byte[] подаци) {
        StringBuilder текст = new StringBuilder(); for (byte вриједност : подаци) текст.append(String.format(Locale.ROOT,"%02x",вриједност & 255)); return текст.toString();
    }
    static Path 내부경로(Path 기준, String назив) {
        Path 결과 = 기준.resolve(назив).normalize();
        if (назив.isEmpty() || Paths.get(назив).isAbsolute() || !결과.startsWith(기준) || назив.indexOf('\\') >= 0)
            throw new IllegalArgumentException("범위를 벗어난 пут: " + назив);
        for (Path 부분 : Paths.get(назив)) if (부분.toString().equals("..")) throw new IllegalArgumentException("상위 пут 금지: " + назив);
        for (Path 현재 = 결과; 현재 != null && 현재.startsWith(기준); 현재 = 현재.getParent())
            if (Files.isSymbolicLink(현재)) throw new IllegalArgumentException("의존성 경로의 링크 금지: " + назив);
        return 결과;
    }
    static String 명령출력(List<String> команда) throws Exception {
        Process процес_вриједност = new ProcessBuilder(команда).redirectError(ProcessBuilder.Redirect.INHERIT).start();
        String 결과 = new String(процес_вриједност.getInputStream().readAllBytes(),StandardCharsets.UTF_8);
        if (процес_вриједност.waitFor() != 0) throw new IOException("команда неуспјех_вриједност: " + команда.get(0)); return 결과;
    }
    static void 풀기(Path архива_вриједност, Path одредиште_вриједност) throws Exception {
        for (String назив : 명령출력(Arrays.asList("tar","-tzf",архива_вриједност.toString())).split("\n")) 내부경로(одредиште_вриједност, назив);
        for (String редак : 명령출력(Arrays.asList("tar","-tvzf",архива_вриједност.toString())).split("\n"))
            if (!редак.isEmpty() && редак.charAt(0) != '-' && редак.charAt(0) != 'd') throw new IOException("외부 링크 또는 특수 파일을 포함한 의존성");
        Files.createDirectories(одредиште_вриједност);
        int стање_вриједност = new ProcessBuilder("tar","--no-same-owner","--no-same-permissions","-xzf",архива_вриједност.toString(),"-C",одредиште_вриједност.toString()).inheritIO().start().waitFor();
        if (стање_вриједност != 0) throw new IOException("의존성 архива_вриједност 해제 неуспјех_вриједност");
    }
    static void 호출(Path 작업경로, Path 도구, List<String> 인수, Map<String,String> 환경) throws Exception {
        List<String> команда = new ArrayList<>(Arrays.asList("python3", 도구.toString())); команда.addAll(인수);
        ProcessBuilder 실행 = new ProcessBuilder(команда).directory(작업경로.toFile()).inheritIO(); 실행.environment().putAll(환경);
        int стање_вриједност = 실행.start().waitFor(); if (стање_вриједност != 0) throw new IOException("도구 неуспјех_вриједност: " + 도구 + " (" + стање_вриједност + ")");
    }
    @SuppressWarnings("unchecked")
    public static void main(String[] 인수) throws Exception {
        if (인수.length < 1) throw new IllegalArgumentException("build, run, desktop, image, check, test-system 중 동작을 지정하세요");
        String радња = 인수[0];
        if (!Arrays.asList("build","run","desktop","image","check","test-system").contains(радња)) throw new IllegalArgumentException("알 수 없는 радња");
        Path 기준 = Paths.get(System.getProperty("worldos.edition.root")).toAbsolutePath().normalize();
        Map<String,Object> Подешавања = (Map<String,Object>)new 자료해석기(Files.readString(기준.resolve("native.json"),StandardCharsets.UTF_8)).읽기();
        Path извор_стабло = 내부경로(기준,(String)Подешавања.get("source")), језгро_вриједност = 내부경로(извор_стабло,(String)Подешавања.get("native"));
        List<String> 소유파일들 = (List<String>)(List<?>)Подешавања.get("owned_files");
        for (String назив : 소유파일들) if (!Files.isRegularFile(내부경로(извор_стабло,назив))) throw new IOException("извор_стабло 없음: " + назив);
        if (радња.equals("check")) { System.out.println(Подешавања.get("country") + " " + Подешавања.get("language") + " 독립 извор_стабло потврдити 완료"); return; }
        String 자원상대 = (String)Подешавања.getOrDefault("resource_root", ".");
        if (!자원상대.equals(".") && !자원상대.equals("..")) throw new IllegalArgumentException("의존성 기준 пут грешка");
        Path ресурс_вриједност = 기준.resolve(자원상대).normalize(); Path архива_вриједност = ресурс_вриједност.resolve("native-vendor.tar.gz");
        String 기대해시 = (String)Подешавања.get("vendor_sha256");
        if (!해시(архива_вриједност).equals(기대해시)) throw new IOException("의존성 SHA-256 불일치");
        Path 표식 = извор_стабло.resolve(".vendor-sha256");
        if (!Files.isRegularFile(표식) || !Files.readString(표식).trim().equals(기대해시)) { 풀기(архива_вриједност, извор_стабло); Files.writeString(표식,기대해시 + "\n"); }
        Map<String,String> 환경 = new HashMap<>(System.getenv());
        Path ipConfig = null;
        if (환경.containsKey("IP_CONFIG")) ipConfig = Paths.get(환경.get("IP_CONFIG")).toAbsolutePath().normalize();
        else for (Path parent = 기준; parent != null; parent = parent.getParent()) {
            if (Files.isRegularFile(parent.resolve("ip.conf"))) { ipConfig = parent.resolve("ip.conf"); break; }
        }
        if (ipConfig == null) ipConfig = извор_стабло.resolve("ip.conf");
        if (!Files.isRegularFile(ipConfig)) throw new IOException("Missing ip.conf: " + ipConfig);
        환경.put("IP_CONFIG", ipConfig.toString());
        if (Arrays.asList("run","desktop","test-system").contains(радња) && !환경.containsKey("QEMU_AARCH64")) {
            Path 실행기 = ресурс_вриједност.resolve("host/qemu"), 실행기표식 = ресурс_вриједност.resolve("host/.qemu-sha256");
            String 실행기해시 = (String)Подешавања.get("qemu_sha256");
            if (!Files.isRegularFile(실행기) || !Files.isRegularFile(실행기표식) || !Files.readString(실행기표식).trim().equals(실행기해시)) {
                Path 실행기압축 = ресурс_вриједност.resolve("qemu-host.tar.gz"); if (!해시(실행기압축).equals(실행기해시)) throw new IOException("QEMU SHA-256 불일치");
                풀기(실행기압축,ресурс_вриједност.resolve("host")); Files.writeString(실행기표식,실행기해시 + "\n");
            }
            환경.put("QEMU_AARCH64",실행기.toString());
        }
        MessageDigest 계산 = MessageDigest.getInstance("SHA-256"); Collections.sort(소유파일들);
        for (String назив : 소유파일들) { 계산.update(назив.getBytes(StandardCharsets.UTF_8)); 계산.update(Files.readAllBytes(내부경로(извор_стабло,назив))); }
        계산.update("ip.conf\0".getBytes(StandardCharsets.UTF_8)); 계산.update(Files.readAllBytes(ipConfig));
        String 소스해시 = 해시글(계산.digest()); Path 빌드표식 = језгро_вриједност.resolve("build/worldos-source.sha256");
        if (радња.equals("build") || !Files.isRegularFile(빌드표식) || !Files.readString(빌드표식).trim().equals(소스해시)) {
            호출(језгро_вриједност,내부경로(језгро_вриједност,(String)Подешавања.get("builder")),Collections.emptyList(),환경);
            Files.writeString(빌드표식,소스해시 + "\n");
        }
        List<String> 추가인수 = new ArrayList<>(Arrays.asList(인수).subList(1,인수.length));
        if (радња.equals("run") || радња.equals("desktop")) {
            if (радња.equals("desktop")) 추가인수.add(0,"--desktop");
            호출(језгро_вриједност,내부경로(језгро_вриједност,(String)Подешавања.get("runner")),추가인수,환경);
        } else if (радња.equals("image")) 호출(језгро_вриједност,내부경로(језгро_вриједност,(String)Подешавања.get("image_builder")),추가인수,환경);
        else if (радња.equals("test-system")) {
            추가인수.add(0,기준.toString()); 추가인수.add(0,"--edition");
            호출(језгро_вриједност,내부경로(језгро_вриједност,(String)Подешавања.get("system_tester")),추가인수,환경);
        }
    }
}
