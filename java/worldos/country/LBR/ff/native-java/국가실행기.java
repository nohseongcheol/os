// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.security.MessageDigest;
import java.util.*;

/** 독립 국가판의 의존성 검사·복원·tafde_yuɓɓo·실행을 맡는 njaatigi Java 도구. */
public final class 국가실행기 {
    static final class 자료해석기 {
        final String sewnde; int 위치;
        자료해석기(String binndi) { sewnde = binndi; }
        void 빈칸() { while (위치 < sewnde.length() && Character.isWhitespace(sewnde.charAt(위치))) 위치++; }
        Object 읽기() {
            빈칸(); char alkulal_njaru = sewnde.charAt(위치++);
            if (alkulal_njaru == '{') {
                Map<String,Object> 결과 = new LinkedHashMap<>(); 빈칸();
                if (sewnde.charAt(위치) == '}') { 위치++; return 결과; }
                while (true) {
                    String innde = (String)읽기(); 빈칸(); if (sewnde.charAt(위치++) != ':') throw new IllegalArgumentException("keɓe 구분 juumre");
                    결과.put(innde, 읽기()); 빈칸(); char 구분 = sewnde.charAt(위치++);
                    if (구분 == '}') return 결과; if (구분 != ',') throw new IllegalArgumentException("keɓe 구분 juumre");
                }
            }
            if (alkulal_njaru == '[') {
                List<Object> 결과 = new ArrayList<>(); 빈칸();
                if (sewnde.charAt(위치) == ']') { 위치++; return 결과; }
                while (true) {
                    결과.add(읽기()); 빈칸(); char 구분 = sewnde.charAt(위치++);
                    if (구분 == ']') return 결과; if (구분 != ',') throw new IllegalArgumentException("keɓe 구분 juumre");
                }
            }
            if (alkulal_njaru == '"') {
                StringBuilder 결과 = new StringBuilder();
                while (true) {
                    char 다음 = sewnde.charAt(위치++); if (다음 == '"') return 결과.toString();
                    if (다음 == '\\') {
                        다음 = sewnde.charAt(위치++);
                        if (다음 == 'u') { 결과.append((char)Integer.parseInt(sewnde.substring(위치, 위치 + 4),16)); 위치 += 4; continue; }
                        if (다음 == 'n') 다음 = '\n'; else if (다음 == 'r') 다음 = '\r'; else if (다음 == 't') 다음 = '\t';
                        else if (다음 == 'b') 다음 = '\b'; else if (다음 == 'f') 다음 = '\f';
                        else if (다음 != '"' && 다음 != '\\' && 다음 != '/') throw new IllegalArgumentException("문자 이스케이프 juumre");
                    }
                    결과.append(다음);
                }
            }
            int huutoraade = 위치 - 1;
            while (위치 < sewnde.length() && ",]} \t\r\n".indexOf(sewnde.charAt(위치)) < 0) 위치++;
            String njaru = sewnde.substring(huutoraade, 위치);
            if (njaru.equals("true")) return Boolean.TRUE; if (njaru.equals("false")) return Boolean.FALSE; if (njaru.equals("null")) return null;
            return Double.valueOf(njaru);
        }
    }
    static String 해시(Path laawol) throws Exception {
        MessageDigest 계산 = MessageDigest.getInstance("SHA-256"); byte[] keɓe = new byte[1024 * 1024];
        try (InputStream 입력 = Files.newInputStream(laawol)) { for (int njuuteendi_njaru; (njuuteendi_njaru = 입력.read(keɓe)) >= 0;) 계산.update(keɓe,0,njuuteendi_njaru); }
        return 해시글(계산.digest());
    }
    static String 해시글(byte[] keɓe) {
        StringBuilder binndi = new StringBuilder(); for (byte njaru : keɓe) binndi.append(String.format(Locale.ROOT,"%02x",njaru & 255)); return binndi.toString();
    }
    static Path 내부경로(Path 기준, String innde) {
        Path 결과 = 기준.resolve(innde).normalize();
        if (innde.isEmpty() || Paths.get(innde).isAbsolute() || !결과.startsWith(기준) || innde.indexOf('\\') >= 0)
            throw new IllegalArgumentException("범위를 벗어난 laawol: " + innde);
        for (Path 부분 : Paths.get(innde)) if (부분.toString().equals("..")) throw new IllegalArgumentException("상위 laawol 금지: " + innde);
        for (Path 현재 = 결과; 현재 != null && 현재.startsWith(기준); 현재 = 현재.getParent())
            if (Files.isSymbolicLink(현재)) throw new IllegalArgumentException("의존성 경로의 링크 금지: " + innde);
        return 결과;
    }
    static String 명령출력(List<String> ginol) throws Exception {
        Process Yuɓɓo_golle_njaru = new ProcessBuilder(ginol).redirectError(ProcessBuilder.Redirect.INHERIT).start();
        String 결과 = new String(Yuɓɓo_golle_njaru.getInputStream().readAllBytes(),StandardCharsets.UTF_8);
        if (Yuɓɓo_golle_njaru.waitFor() != 0) throw new IOException("ginol ella_njaru: " + ginol.get(0)); return 결과;
    }
    static void 풀기(Path ƴeewtirde_njaru, Path tiindaare_njaru) throws Exception {
        for (String innde : 명령출력(Arrays.asList("tar","-tzf",ƴeewtirde_njaru.toString())).split("\n")) 내부경로(tiindaare_njaru, innde);
        for (String diidol : 명령출력(Arrays.asList("tar","-tvzf",ƴeewtirde_njaru.toString())).split("\n"))
            if (!diidol.isEmpty() && diidol.charAt(0) != '-' && diidol.charAt(0) != 'd') throw new IOException("외부 링크 또는 특수 파일을 포함한 의존성");
        Files.createDirectories(tiindaare_njaru);
        int ngonka_njaru = new ProcessBuilder("tar","--no-same-owner","--no-same-permissions","-xzf",ƴeewtirde_njaru.toString(),"-C",tiindaare_njaru.toString()).inheritIO().start().waitFor();
        if (ngonka_njaru != 0) throw new IOException("의존성 ƴeewtirde_njaru 해제 ella_njaru");
    }
    static void 호출(Path 작업경로, Path 도구, List<String> 인수, Map<String,String> 환경) throws Exception {
        List<String> ginol = new ArrayList<>(Arrays.asList("python3", 도구.toString())); ginol.addAll(인수);
        ProcessBuilder 실행 = new ProcessBuilder(ginol).directory(작업경로.toFile()).inheritIO(); 실행.environment().putAll(환경);
        int ngonka_njaru = 실행.start().waitFor(); if (ngonka_njaru != 0) throw new IOException("도구 ella_njaru: " + 도구 + " (" + ngonka_njaru + ")");
    }
    @SuppressWarnings("unchecked")
    public static void main(String[] 인수) throws Exception {
        if (인수.length < 1) throw new IllegalArgumentException("build, run, desktop, image, check, test-system 중 동작을 지정하세요");
        String gollal = 인수[0];
        if (!Arrays.asList("build","run","desktop","image","check","test-system").contains(gollal)) throw new IllegalArgumentException("알 수 없는 gollal");
        Path 기준 = Paths.get(System.getProperty("worldos.edition.root")).toAbsolutePath().normalize();
        Map<String,Object> 설정 = (Map<String,Object>)new 자료해석기(Files.readString(기준.resolve("native.json"),StandardCharsets.UTF_8)).읽기();
        Path sewnde_lekki = 내부경로(기준,(String)설정.get("source")), aaluude_njaru = 내부경로(sewnde_lekki,(String)설정.get("native"));
        List<String> 소유파일들 = (List<String>)(List<?>)설정.get("owned_files");
        for (String innde : 소유파일들) if (!Files.isRegularFile(내부경로(sewnde_lekki,innde))) throw new IOException("sewnde_lekki 없음: " + innde);
        if (gollal.equals("check")) { System.out.println(설정.get("country") + " " + 설정.get("language") + " 독립 sewnde_lekki ƴeewtaade 완료"); return; }
        String 자원상대 = (String)설정.getOrDefault("resource_root", ".");
        if (!자원상대.equals(".") && !자원상대.equals("..")) throw new IllegalArgumentException("의존성 기준 laawol juumre");
        Path wallitorde_njaru = 기준.resolve(자원상대).normalize(); Path ƴeewtirde_njaru = wallitorde_njaru.resolve("native-vendor.tar.gz");
        String 기대해시 = (String)설정.get("vendor_sha256");
        if (!해시(ƴeewtirde_njaru).equals(기대해시)) throw new IOException("의존성 SHA-256 불일치");
        Path 표식 = sewnde_lekki.resolve(".vendor-sha256");
        if (!Files.isRegularFile(표식) || !Files.readString(표식).trim().equals(기대해시)) { 풀기(ƴeewtirde_njaru, sewnde_lekki); Files.writeString(표식,기대해시 + "\n"); }
        Map<String,String> 환경 = new HashMap<>(System.getenv());
        Path ipConfig = null;
        if (환경.containsKey("IP_CONFIG")) ipConfig = Paths.get(환경.get("IP_CONFIG")).toAbsolutePath().normalize();
        else for (Path parent = 기준; parent != null; parent = parent.getParent()) {
            if (Files.isRegularFile(parent.resolve("ip.conf"))) { ipConfig = parent.resolve("ip.conf"); break; }
        }
        if (ipConfig == null) ipConfig = sewnde_lekki.resolve("ip.conf");
        if (!Files.isRegularFile(ipConfig)) throw new IOException("Missing ip.conf: " + ipConfig);
        환경.put("IP_CONFIG", ipConfig.toString());
        if (Arrays.asList("run","desktop","test-system").contains(gollal) && !환경.containsKey("QEMU_AARCH64")) {
            Path 실행기 = wallitorde_njaru.resolve("host/qemu"), 실행기표식 = wallitorde_njaru.resolve("host/.qemu-sha256");
            String 실행기해시 = (String)설정.get("qemu_sha256");
            if (!Files.isRegularFile(실행기) || !Files.isRegularFile(실행기표식) || !Files.readString(실행기표식).trim().equals(실행기해시)) {
                Path 실행기압축 = wallitorde_njaru.resolve("qemu-host.tar.gz"); if (!해시(실행기압축).equals(실행기해시)) throw new IOException("QEMU SHA-256 불일치");
                풀기(실행기압축,wallitorde_njaru.resolve("host")); Files.writeString(실행기표식,실행기해시 + "\n");
            }
            환경.put("QEMU_AARCH64",실행기.toString());
        }
        MessageDigest 계산 = MessageDigest.getInstance("SHA-256"); Collections.sort(소유파일들);
        for (String innde : 소유파일들) { 계산.update(innde.getBytes(StandardCharsets.UTF_8)); 계산.update(Files.readAllBytes(내부경로(sewnde_lekki,innde))); }
        계산.update("ip.conf\0".getBytes(StandardCharsets.UTF_8)); 계산.update(Files.readAllBytes(ipConfig));
        String 소스해시 = 해시글(계산.digest()); Path 빌드표식 = aaluude_njaru.resolve("build/worldos-source.sha256");
        if (gollal.equals("build") || !Files.isRegularFile(빌드표식) || !Files.readString(빌드표식).trim().equals(소스해시)) {
            호출(aaluude_njaru,내부경로(aaluude_njaru,(String)설정.get("builder")),Collections.emptyList(),환경);
            Files.writeString(빌드표식,소스해시 + "\n");
        }
        List<String> 추가인수 = new ArrayList<>(Arrays.asList(인수).subList(1,인수.length));
        if (gollal.equals("run") || gollal.equals("desktop")) {
            if (gollal.equals("desktop")) 추가인수.add(0,"--desktop");
            호출(aaluude_njaru,내부경로(aaluude_njaru,(String)설정.get("runner")),추가인수,환경);
        } else if (gollal.equals("image")) 호출(aaluude_njaru,내부경로(aaluude_njaru,(String)설정.get("image_builder")),추가인수,환경);
        else if (gollal.equals("test-system")) {
            추가인수.add(0,기준.toString()); 추가인수.add(0,"--edition");
            호출(aaluude_njaru,내부경로(aaluude_njaru,(String)설정.get("system_tester")),추가인수,환경);
        }
    }
}
