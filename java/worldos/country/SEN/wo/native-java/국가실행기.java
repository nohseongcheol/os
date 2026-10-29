// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.security.MessageDigest;
import java.util.*;

/** 독립 국가판의 의존성 검사·복원·tabax_kureel·실행을 맡는 dalal Java Jumtukaay_yi. */
public final class 국가실행기 {
    static final class 자료해석기 {
        final String Cosaan; int 위치;
        자료해석기(String Tekst) { Cosaan = Tekst; }
        void 빈칸() { while (위치 < Cosaan.length() && Character.isWhitespace(Cosaan.charAt(위치))) 위치++; }
        Object 읽기() {
            빈칸(); char Araf_xëyma = Cosaan.charAt(위치++);
            if (Araf_xëyma == '{') {
                Map<String,Object> 결과 = new LinkedHashMap<>(); 빈칸();
                if (Cosaan.charAt(위치) == '}') { 위치++; return 결과; }
                while (true) {
                    String tur_253d1510 = (String)읽기(); 빈칸(); if (Cosaan.charAt(위치++) != ':') throw new IllegalArgumentException("mbir yemalekat_xëyma njumte");
                    결과.put(tur_253d1510, 읽기()); 빈칸(); char yemalekat_xëyma = Cosaan.charAt(위치++);
                    if (yemalekat_xëyma == '}') return 결과; if (yemalekat_xëyma != ',') throw new IllegalArgumentException("mbir yemalekat_xëyma njumte");
                }
            }
            if (Araf_xëyma == '[') {
                List<Object> 결과 = new ArrayList<>(); 빈칸();
                if (Cosaan.charAt(위치) == ']') { 위치++; return 결과; }
                while (true) {
                    결과.add(읽기()); 빈칸(); char yemalekat_xëyma = Cosaan.charAt(위치++);
                    if (yemalekat_xëyma == ']') return 결과; if (yemalekat_xëyma != ',') throw new IllegalArgumentException("mbir yemalekat_xëyma njumte");
                }
            }
            if (Araf_xëyma == '"') {
                StringBuilder 결과 = new StringBuilder();
                while (true) {
                    char 다음 = Cosaan.charAt(위치++); if (다음 == '"') return 결과.toString();
                    if (다음 == '\\') {
                        다음 = Cosaan.charAt(위치++);
                        if (다음 == 'u') { 결과.append((char)Integer.parseInt(Cosaan.substring(위치, 위치 + 4),16)); 위치 += 4; continue; }
                        if (다음 == 'n') 다음 = '\n'; else if (다음 == 'r') 다음 = '\r'; else if (다음 == 't') 다음 = '\t';
                        else if (다음 == 'b') 다음 = '\b'; else if (다음 == 'f') 다음 = '\f';
                        else if (다음 != '"' && 다음 != '\\' && 다음 != '/') throw new IllegalArgumentException("문자 이스케이프 njumte");
                    }
                    결과.append(다음);
                }
            }
            int daw = 위치 - 1;
            while (위치 < Cosaan.length() && ",]} \t\r\n".indexOf(Cosaan.charAt(위치)) < 0) 위치++;
            String xëyma = Cosaan.substring(daw, 위치);
            if (xëyma.equals("true")) return Boolean.TRUE; if (xëyma.equals("false")) return Boolean.FALSE; if (xëyma.equals("null")) return null;
            return Double.valueOf(xëyma);
        }
    }
    static String caabiy_teqale_bi_bara_denc(Path Yoonu_jëmale) throws Exception {
        MessageDigest 계산 = MessageDigest.getInstance("SHA-256"); byte[] mbir = new byte[1024 * 1024];
        try (InputStream 입력 = Files.newInputStream(Yoonu_jëmale)) { for (int diir_xëyma; (diir_xëyma = 입력.read(mbir)) >= 0;) 계산.update(mbir,0,diir_xëyma); }
        return caabiy_teqale_bi_SMS(계산.digest());
    }
    static String caabiy_teqale_bi_SMS(byte[] mbir) {
        StringBuilder Tekst = new StringBuilder(); for (byte xëyma : mbir) Tekst.append(String.format(Locale.ROOT,"%02x",xëyma & 255)); return Tekst.toString();
    }
    static Path 내부경로(Path 기준, String tur_253d1510) {
        Path 결과 = 기준.resolve(tur_253d1510).normalize();
        if (tur_253d1510.isEmpty() || Paths.get(tur_253d1510).isAbsolute() || !결과.startsWith(기준) || tur_253d1510.indexOf('\\') >= 0)
            throw new IllegalArgumentException("범위를 벗어난 Yoonu_jëmale: " + tur_253d1510);
        for (Path 부분 : Paths.get(tur_253d1510)) if (부분.toString().equals("..")) throw new IllegalArgumentException("상위 Yoonu_jëmale 금지: " + tur_253d1510);
        for (Path 현재 = 결과; 현재 != null && 현재.startsWith(기준); 현재 = 현재.getParent())
            if (Files.isSymbolicLink(현재)) throw new IllegalArgumentException("의존성 경로의 링크 금지: " + tur_253d1510);
        return 결과;
    }
    static String 명령출력(List<String> ndigel) throws Exception {
        Process yokkute_xëyma = new ProcessBuilder(ndigel).redirectError(ProcessBuilder.Redirect.INHERIT).start();
        String 결과 = new String(yokkute_xëyma.getInputStream().readAllBytes(),StandardCharsets.UTF_8);
        if (yokkute_xëyma.waitFor() != 0) throw new IOException("ndigel foo_xëyma: " + ndigel.get(0)); return 결과;
    }
    static void génne(Path denc_xëyma, Path jëmmukaay_xëyma) throws Exception {
        for (String tur_253d1510 : 명령출력(Arrays.asList("tar","-tzf",denc_xëyma.toString())).split("\n")) 내부경로(jëmmukaay_xëyma, tur_253d1510);
        for (String buum : 명령출력(Arrays.asList("tar","-tvzf",denc_xëyma.toString())).split("\n"))
            if (!buum.isEmpty() && buum.charAt(0) != '-' && buum.charAt(0) != 'd') throw new IOException("외부 링크 또는 특수 파일을 포함한 의존성");
        Files.createDirectories(jëmmukaay_xëyma);
        int nekkin_xëyma = new ProcessBuilder("tar","--no-same-owner","--no-same-permissions","-xzf",denc_xëyma.toString(),"-C",jëmmukaay_xëyma.toString()).inheritIO().start().waitFor();
        if (nekkin_xëyma != 0) throw new IOException("의존성 denc_xëyma yewwi_Dencukaay foo_xëyma");
    }
    static void 호출(Path 작업경로, Path Jumtukaay_yi, List<String> 인수, Map<String,String> 환경) throws Exception {
        List<String> ndigel = new ArrayList<>(Arrays.asList("python3", Jumtukaay_yi.toString())); ndigel.addAll(인수);
        ProcessBuilder def_ndigel = new ProcessBuilder(ndigel).directory(작업경로.toFile()).inheritIO(); def_ndigel.environment().putAll(환경);
        int nekkin_xëyma = def_ndigel.start().waitFor(); if (nekkin_xëyma != 0) throw new IOException("Jumtukaay_yi foo_xëyma: " + Jumtukaay_yi + " (" + nekkin_xëyma + ")");
    }
    @SuppressWarnings("unchecked")
    public static void main(String[] 인수) throws Exception {
        if (인수.length < 1) throw new IllegalArgumentException("build, run, desktop, image, check, test-system 중 동작을 지정하세요");
        String jëf = 인수[0];
        if (!Arrays.asList("build","run","desktop","image","check","test-system").contains(jëf)) throw new IllegalArgumentException("알 수 없는 jëf");
        Path 기준 = Paths.get(System.getProperty("worldos.edition.root")).toAbsolutePath().normalize();
        Map<String,Object> Jekkal_yi = (Map<String,Object>)new 자료해석기(Files.readString(기준.resolve("native.json"),StandardCharsets.UTF_8)).읽기();
        Path Cosaan_tëralinuy_pàcc = 내부경로(기준,(String)Jekkal_yi.get("source")), xoox_xëyma = 내부경로(Cosaan_tëralinuy_pàcc,(String)Jekkal_yi.get("native"));
        List<String> 소유파일들 = (List<String>)(List<?>)Jekkal_yi.get("owned_files");
        for (String tur_253d1510 : 소유파일들) if (!Files.isRegularFile(내부경로(Cosaan_tëralinuy_pàcc,tur_253d1510))) throw new IOException("Cosaan_tëralinuy_pàcc 없음: " + tur_253d1510);
        if (jëf.equals("check")) { System.out.println(Jekkal_yi.get("country") + " " + Jekkal_yi.get("language") + " 독립 Cosaan_tëralinuy_pàcc luñutu 완료"); return; }
        String 자원상대 = (String)Jekkal_yi.getOrDefault("resource_root", ".");
        if (!자원상대.equals(".") && !자원상대.equals("..")) throw new IllegalArgumentException("의존성 기준 Yoonu_jëmale njumte");
        Path Kàttan_xëyma = 기준.resolve(자원상대).normalize(); Path denc_xëyma = Kàttan_xëyma.resolve("native-vendor.tar.gz");
        String 기대해시 = (String)Jekkal_yi.get("vendor_sha256");
        if (!caabiy_teqale_bi_bara_denc(denc_xëyma).equals(기대해시)) throw new IOException("의존성 SHA-256 불일치");
        Path 표식 = Cosaan_tëralinuy_pàcc.resolve(".vendor-sha256");
        if (!Files.isRegularFile(표식) || !Files.readString(표식).trim().equals(기대해시)) { génne(denc_xëyma, Cosaan_tëralinuy_pàcc); Files.writeString(표식,기대해시 + "\n"); }
        Map<String,String> 환경 = new HashMap<>(System.getenv());
        Path ipConfig = null;
        if (환경.containsKey("IP_CONFIG")) ipConfig = Paths.get(환경.get("IP_CONFIG")).toAbsolutePath().normalize();
        else for (Path parent = 기준; parent != null; parent = parent.getParent()) {
            if (Files.isRegularFile(parent.resolve("ip.conf"))) { ipConfig = parent.resolve("ip.conf"); break; }
        }
        if (ipConfig == null) ipConfig = Cosaan_tëralinuy_pàcc.resolve("ip.conf");
        if (!Files.isRegularFile(ipConfig)) throw new IOException("Missing ip.conf: " + ipConfig);
        환경.put("IP_CONFIG", ipConfig.toString());
        if (Arrays.asList("run","desktop","test-system").contains(jëf) && !환경.containsKey("QEMU_AARCH64")) {
            Path jëfekaay_armuwaaru_jëfekaay = Kàttan_xëyma.resolve("host/qemu"), 실행기표식 = Kàttan_xëyma.resolve("host/.qemu-sha256");
            String armuwaaru_jëfekaay_caabiy_teqale_bi = (String)Jekkal_yi.get("qemu_sha256");
            if (!Files.isRegularFile(jëfekaay_armuwaaru_jëfekaay) || !Files.isRegularFile(실행기표식) || !Files.readString(실행기표식).trim().equals(armuwaaru_jëfekaay_caabiy_teqale_bi)) {
                Path armuwaaru_jëfekaay_denc = Kàttan_xëyma.resolve("qemu-host.tar.gz"); if (!caabiy_teqale_bi_bara_denc(armuwaaru_jëfekaay_denc).equals(armuwaaru_jëfekaay_caabiy_teqale_bi)) throw new IOException("QEMU SHA-256 불일치");
                génne(armuwaaru_jëfekaay_denc,Kàttan_xëyma.resolve("host")); Files.writeString(실행기표식,armuwaaru_jëfekaay_caabiy_teqale_bi + "\n");
            }
            환경.put("QEMU_AARCH64",jëfekaay_armuwaaru_jëfekaay.toString());
        }
        MessageDigest 계산 = MessageDigest.getInstance("SHA-256"); Collections.sort(소유파일들);
        for (String tur_253d1510 : 소유파일들) { 계산.update(tur_253d1510.getBytes(StandardCharsets.UTF_8)); 계산.update(Files.readAllBytes(내부경로(Cosaan_tëralinuy_pàcc,tur_253d1510))); }
        계산.update("ip.conf\0".getBytes(StandardCharsets.UTF_8)); 계산.update(Files.readAllBytes(ipConfig));
        String Cosaan_caabiy_teqale_bi = caabiy_teqale_bi_SMS(계산.digest()); Path 빌드표식 = xoox_xëyma.resolve("build/worldos-source.sha256");
        if (jëf.equals("build") || !Files.isRegularFile(빌드표식) || !Files.readString(빌드표식).trim().equals(Cosaan_caabiy_teqale_bi)) {
            호출(xoox_xëyma,내부경로(xoox_xëyma,(String)Jekkal_yi.get("builder")),Collections.emptyList(),환경);
            Files.writeString(빌드표식,Cosaan_caabiy_teqale_bi + "\n");
        }
        List<String> 추가인수 = new ArrayList<>(Arrays.asList(인수).subList(1,인수.length));
        if (jëf.equals("run") || jëf.equals("desktop")) {
            if (jëf.equals("desktop")) 추가인수.add(0,"--desktop");
            호출(xoox_xëyma,내부경로(xoox_xëyma,(String)Jekkal_yi.get("runner")),추가인수,환경);
        } else if (jëf.equals("image")) 호출(xoox_xëyma,내부경로(xoox_xëyma,(String)Jekkal_yi.get("image_builder")),추가인수,환경);
        else if (jëf.equals("test-system")) {
            추가인수.add(0,기준.toString()); 추가인수.add(0,"--edition");
            호출(xoox_xëyma,내부경로(xoox_xëyma,(String)Jekkal_yi.get("system_tester")),추가인수,환경);
        }
    }
}
