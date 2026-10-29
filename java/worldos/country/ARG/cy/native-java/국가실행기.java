// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.security.MessageDigest;
import java.util.*;

/** 독립 국가판의 의존성 검사·복원·llunio_system·실행을 맡는 lletya Java Offer. */
public final class 국가실행기 {
    static final class 자료해석기 {
        final String FFYNHONNELL; int safle;
        자료해석기(String Testun) { FFYNHONNELL = Testun; }
        void 빈칸() { while (safle < FFYNHONNELL.length() && Character.isWhitespace(FFYNHONNELL.charAt(safle))) safle++; }
        Object Darllen() {
            빈칸(); char nod_VALUE = FFYNHONNELL.charAt(safle++);
            if (nod_VALUE == '{') {
                Map<String,Object> mesur = new LinkedHashMap<>(); 빈칸();
                if (FFYNHONNELL.charAt(safle) == '}') { safle++; return mesur; }
                while (true) {
                    String Enw = (String)Darllen(); 빈칸(); if (FFYNHONNELL.charAt(safle++) != ':') throw new IllegalArgumentException("data amffinydd_VALUE Gwall");
                    mesur.put(Enw, Darllen()); 빈칸(); char amffinydd_VALUE = FFYNHONNELL.charAt(safle++);
                    if (amffinydd_VALUE == '}') return mesur; if (amffinydd_VALUE != ',') throw new IllegalArgumentException("data amffinydd_VALUE Gwall");
                }
            }
            if (nod_VALUE == '[') {
                List<Object> mesur = new ArrayList<>(); 빈칸();
                if (FFYNHONNELL.charAt(safle) == ']') { safle++; return mesur; }
                while (true) {
                    mesur.add(Darllen()); 빈칸(); char amffinydd_VALUE = FFYNHONNELL.charAt(safle++);
                    if (amffinydd_VALUE == ']') return mesur; if (amffinydd_VALUE != ',') throw new IllegalArgumentException("data amffinydd_VALUE Gwall");
                }
            }
            if (nod_VALUE == '"') {
                StringBuilder mesur = new StringBuilder();
                while (true) {
                    char Nesaf_eitem = FFYNHONNELL.charAt(safle++); if (Nesaf_eitem == '"') return mesur.toString();
                    if (Nesaf_eitem == '\\') {
                        Nesaf_eitem = FFYNHONNELL.charAt(safle++);
                        if (Nesaf_eitem == 'u') { mesur.append((char)Integer.parseInt(FFYNHONNELL.substring(safle, safle + 4),16)); safle += 4; continue; }
                        if (Nesaf_eitem == 'n') Nesaf_eitem = '\n'; else if (Nesaf_eitem == 'r') Nesaf_eitem = '\r'; else if (Nesaf_eitem == 't') Nesaf_eitem = '\t';
                        else if (Nesaf_eitem == 'b') Nesaf_eitem = '\b'; else if (Nesaf_eitem == 'f') Nesaf_eitem = '\f';
                        else if (Nesaf_eitem != '"' && Nesaf_eitem != '\\' && Nesaf_eitem != '/') throw new IllegalArgumentException("문자 이스케이프 Gwall");
                    }
                    mesur.append(Nesaf_eitem);
                }
            }
            int Gweithredu_2 = safle - 1;
            while (safle < FFYNHONNELL.length() && ",]} \t\r\n".indexOf(FFYNHONNELL.charAt(safle)) < 0) safle++;
            String VALUE = FFYNHONNELL.substring(Gweithredu_2, safle);
            if (VALUE.equals("true")) return Boolean.TRUE; if (VALUE.equals("false")) return Boolean.FALSE; if (VALUE.equals("null")) return null;
            return Double.valueOf(VALUE);
        }
    }
    static String hash_ffeil(Path LLWYBR) throws Exception {
        MessageDigest 계산 = MessageDigest.getInstance("SHA-256"); byte[] data = new byte[1024 * 1024];
        try (InputStream 입력 = Files.newInputStream(LLWYBR)) { for (int hyd_VALUE; (hyd_VALUE = 입력.read(data)) >= 0;) 계산.update(data,0,hyd_VALUE); }
        return hash_SMS(계산.digest());
    }
    static String hash_SMS(byte[] data) {
        StringBuilder Testun = new StringBuilder(); for (byte VALUE : data) Testun.append(String.format(Locale.ROOT,"%02x",VALUE & 255)); return Testun.toString();
    }
    static Path 내부경로(Path prosiect_gwraidd, String Enw) {
        Path mesur = prosiect_gwraidd.resolve(Enw).normalize();
        if (Enw.isEmpty() || Paths.get(Enw).isAbsolute() || !mesur.startsWith(prosiect_gwraidd) || Enw.indexOf('\\') >= 0)
            throw new IllegalArgumentException("범위를 벗어난 LLWYBR: " + Enw);
        for (Path 부분 : Paths.get(Enw)) if (부분.toString().equals("..")) throw new IllegalArgumentException("상위 LLWYBR 금지: " + Enw);
        for (Path 현재 = mesur; 현재 != null && 현재.startsWith(prosiect_gwraidd); 현재 = 현재.getParent())
            if (Files.isSymbolicLink(현재)) throw new IllegalArgumentException("의존성 경로의 링크 금지: " + Enw);
        return mesur;
    }
    static String 명령출력(List<String> Gorchymyn) throws Exception {
        Process Proses_VALUE = new ProcessBuilder(Gorchymyn).redirectError(ProcessBuilder.Redirect.INHERIT).start();
        String mesur = new String(Proses_VALUE.getInputStream().readAllBytes(),StandardCharsets.UTF_8);
        if (Proses_VALUE.waitFor() != 0) throw new IOException("Gorchymyn methiant_VALUE: " + Gorchymyn.get(0)); return mesur;
    }
    static void echdynnu(Path Archif_VALUE, Path cyrchfan_VALUE) throws Exception {
        for (String Enw : 명령출력(Arrays.asList("tar","-tzf",Archif_VALUE.toString())).split("\n")) 내부경로(cyrchfan_VALUE, Enw);
        for (String llinell : 명령출력(Arrays.asList("tar","-tvzf",Archif_VALUE.toString())).split("\n"))
            if (!llinell.isEmpty() && llinell.charAt(0) != '-' && llinell.charAt(0) != 'd') throw new IOException("외부 링크 또는 특수 파일을 포함한 의존성");
        Files.createDirectories(cyrchfan_VALUE);
        int cyflwr_VALUE = new ProcessBuilder("tar","--no-same-owner","--no-same-permissions","-xzf",Archif_VALUE.toString(),"-C",cyrchfan_VALUE.toString()).inheritIO().start().waitFor();
        if (cyflwr_VALUE != 0) throw new IOException("의존성 Archif_VALUE rhyddhau_Storio methiant_VALUE");
    }
    static void 호출(Path 작업경로, Path Offer, List<String> 인수, Map<String,String> 환경) throws Exception {
        List<String> Gorchymyn = new ArrayList<>(Arrays.asList("python3", Offer.toString())); Gorchymyn.addAll(인수);
        ProcessBuilder Gweithredu_gorchymyn = new ProcessBuilder(Gorchymyn).directory(작업경로.toFile()).inheritIO(); Gweithredu_gorchymyn.environment().putAll(환경);
        int cyflwr_VALUE = Gweithredu_gorchymyn.start().waitFor(); if (cyflwr_VALUE != 0) throw new IOException("Offer methiant_VALUE: " + Offer + " (" + cyflwr_VALUE + ")");
    }
    @SuppressWarnings("unchecked")
    public static void main(String[] 인수) throws Exception {
        if (인수.length < 1) throw new IllegalArgumentException("build, run, desktop, image, check, test-system 중 동작을 지정하세요");
        String Gweithrediad = 인수[0];
        if (!Arrays.asList("build","run","desktop","image","check","test-system").contains(Gweithrediad)) throw new IllegalArgumentException("알 수 없는 Gweithrediad");
        Path prosiect_gwraidd = Paths.get(System.getProperty("worldos.edition.root")).toAbsolutePath().normalize();
        Map<String,Object> Gosodiadau = (Map<String,Object>)new 자료해석기(Files.readString(prosiect_gwraidd.resolve("native.json"),StandardCharsets.UTF_8)).Darllen();
        Path ffynhonnell_coeden = 내부경로(prosiect_gwraidd,(String)Gosodiadau.get("source")), cnewyllyn_VALUE = 내부경로(ffynhonnell_coeden,(String)Gosodiadau.get("native"));
        List<String> 소유파일들 = (List<String>)(List<?>)Gosodiadau.get("owned_files");
        for (String Enw : 소유파일들) if (!Files.isRegularFile(내부경로(ffynhonnell_coeden,Enw))) throw new IOException("ffynhonnell_coeden 없음: " + Enw);
        if (Gweithrediad.equals("check")) { System.out.println(Gosodiadau.get("country") + " " + Gosodiadau.get("language") + " 독립 ffynhonnell_coeden dilysu 완료"); return; }
        String 자원상대 = (String)Gosodiadau.getOrDefault("resource_root", ".");
        if (!자원상대.equals(".") && !자원상대.equals("..")) throw new IllegalArgumentException("의존성 prosiect_gwraidd LLWYBR Gwall");
        Path adnodd_VALUE = prosiect_gwraidd.resolve(자원상대).normalize(); Path Archif_VALUE = adnodd_VALUE.resolve("native-vendor.tar.gz");
        String 기대해시 = (String)Gosodiadau.get("vendor_sha256");
        if (!hash_ffeil(Archif_VALUE).equals(기대해시)) throw new IOException("의존성 SHA-256 불일치");
        Path 표식 = ffynhonnell_coeden.resolve(".vendor-sha256");
        if (!Files.isRegularFile(표식) || !Files.readString(표식).trim().equals(기대해시)) { echdynnu(Archif_VALUE, ffynhonnell_coeden); Files.writeString(표식,기대해시 + "\n"); }
        Map<String,String> 환경 = new HashMap<>(System.getenv());
        Path ipConfig = null;
        if (환경.containsKey("IP_CONFIG")) ipConfig = Paths.get(환경.get("IP_CONFIG")).toAbsolutePath().normalize();
        else for (Path parent = prosiect_gwraidd; parent != null; parent = parent.getParent()) {
            if (Files.isRegularFile(parent.resolve("ip.conf"))) { ipConfig = parent.resolve("ip.conf"); break; }
        }
        if (ipConfig == null) ipConfig = ffynhonnell_coeden.resolve("ip.conf");
        if (!Files.isRegularFile(ipConfig)) throw new IOException("Missing ip.conf: " + ipConfig);
        환경.put("IP_CONFIG", ipConfig.toString());
        if (Arrays.asList("run","desktop","test-system").contains(Gweithrediad) && !환경.containsKey("QEMU_AARCH64")) {
            Path Rhaglen_lansiwr = adnodd_VALUE.resolve("host/qemu"), 실행기표식 = adnodd_VALUE.resolve("host/.qemu-sha256");
            String lansiwr_hash = (String)Gosodiadau.get("qemu_sha256");
            if (!Files.isRegularFile(Rhaglen_lansiwr) || !Files.isRegularFile(실행기표식) || !Files.readString(실행기표식).trim().equals(lansiwr_hash)) {
                Path lansiwr_Archif = adnodd_VALUE.resolve("qemu-host.tar.gz"); if (!hash_ffeil(lansiwr_Archif).equals(lansiwr_hash)) throw new IOException("QEMU SHA-256 불일치");
                echdynnu(lansiwr_Archif,adnodd_VALUE.resolve("host")); Files.writeString(실행기표식,lansiwr_hash + "\n");
            }
            환경.put("QEMU_AARCH64",Rhaglen_lansiwr.toString());
        }
        MessageDigest 계산 = MessageDigest.getInstance("SHA-256"); Collections.sort(소유파일들);
        for (String Enw : 소유파일들) { 계산.update(Enw.getBytes(StandardCharsets.UTF_8)); 계산.update(Files.readAllBytes(내부경로(ffynhonnell_coeden,Enw))); }
        계산.update("ip.conf\0".getBytes(StandardCharsets.UTF_8)); 계산.update(Files.readAllBytes(ipConfig));
        String ffynhonnell_hash = hash_SMS(계산.digest()); Path 빌드표식 = cnewyllyn_VALUE.resolve("build/worldos-source.sha256");
        if (Gweithrediad.equals("build") || !Files.isRegularFile(빌드표식) || !Files.readString(빌드표식).trim().equals(ffynhonnell_hash)) {
            호출(cnewyllyn_VALUE,내부경로(cnewyllyn_VALUE,(String)Gosodiadau.get("builder")),Collections.emptyList(),환경);
            Files.writeString(빌드표식,ffynhonnell_hash + "\n");
        }
        List<String> 추가인수 = new ArrayList<>(Arrays.asList(인수).subList(1,인수.length));
        if (Gweithrediad.equals("run") || Gweithrediad.equals("desktop")) {
            if (Gweithrediad.equals("desktop")) 추가인수.add(0,"--desktop");
            호출(cnewyllyn_VALUE,내부경로(cnewyllyn_VALUE,(String)Gosodiadau.get("runner")),추가인수,환경);
        } else if (Gweithrediad.equals("image")) 호출(cnewyllyn_VALUE,내부경로(cnewyllyn_VALUE,(String)Gosodiadau.get("image_builder")),추가인수,환경);
        else if (Gweithrediad.equals("test-system")) {
            추가인수.add(0,prosiect_gwraidd.toString()); 추가인수.add(0,"--edition");
            호출(cnewyllyn_VALUE,내부경로(cnewyllyn_VALUE,(String)Gosodiadau.get("system_tester")),추가인수,환경);
        }
    }
}
