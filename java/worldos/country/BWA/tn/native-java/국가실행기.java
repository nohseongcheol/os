// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.security.MessageDigest;
import java.util.*;

/** 독립 국가판의 의존성 검사·복원·aga_tsamaiso·실행을 맡는 pinagare Java Thuluse. */
public final class 국가실행기 {
    static final class 자료해석기 {
        final String Motswedi; int 위치;
        자료해석기(String SMS) { Motswedi = SMS; }
        void 빈칸() { while (위치 < Motswedi.length() && Character.isWhitespace(Motswedi.charAt(위치))) 위치++; }
        Object 읽기() {
            빈칸(); char Letshwao_Boleng = Motswedi.charAt(위치++);
            if (Letshwao_Boleng == '{') {
                Map<String,Object> 결과 = new LinkedHashMap<>(); 빈칸();
                if (Motswedi.charAt(위치) == '}') { 위치++; return 결과; }
                while (true) {
                    String leina = (String)읽기(); 빈칸(); if (Motswedi.charAt(위치++) != ':') throw new IllegalArgumentException("tshedimosetso sekgaoganyi_Boleng phoso");
                    결과.put(leina, 읽기()); 빈칸(); char sekgaoganyi_Boleng = Motswedi.charAt(위치++);
                    if (sekgaoganyi_Boleng == '}') return 결과; if (sekgaoganyi_Boleng != ',') throw new IllegalArgumentException("tshedimosetso sekgaoganyi_Boleng phoso");
                }
            }
            if (Letshwao_Boleng == '[') {
                List<Object> 결과 = new ArrayList<>(); 빈칸();
                if (Motswedi.charAt(위치) == ']') { 위치++; return 결과; }
                while (true) {
                    결과.add(읽기()); 빈칸(); char sekgaoganyi_Boleng = Motswedi.charAt(위치++);
                    if (sekgaoganyi_Boleng == ']') return 결과; if (sekgaoganyi_Boleng != ',') throw new IllegalArgumentException("tshedimosetso sekgaoganyi_Boleng phoso");
                }
            }
            if (Letshwao_Boleng == '"') {
                StringBuilder 결과 = new StringBuilder();
                while (true) {
                    char 다음 = Motswedi.charAt(위치++); if (다음 == '"') return 결과.toString();
                    if (다음 == '\\') {
                        다음 = Motswedi.charAt(위치++);
                        if (다음 == 'u') { 결과.append((char)Integer.parseInt(Motswedi.substring(위치, 위치 + 4),16)); 위치 += 4; continue; }
                        if (다음 == 'n') 다음 = '\n'; else if (다음 == 'r') 다음 = '\r'; else if (다음 == 't') 다음 = '\t';
                        else if (다음 == 'b') 다음 = '\b'; else if (다음 == 'f') 다음 = '\f';
                        else if (다음 != '"' && 다음 != '\\' && 다음 != '/') throw new IllegalArgumentException("문자 이스케이프 phoso");
                    }
                    결과.append(다음);
                }
            }
            int dirisa = 위치 - 1;
            while (위치 < Motswedi.length() && ",]} \t\r\n".indexOf(Motswedi.charAt(위치)) < 0) 위치++;
            String Boleng = Motswedi.substring(dirisa, 위치);
            if (Boleng.equals("true")) return Boolean.TRUE; if (Boleng.equals("false")) return Boolean.FALSE; if (Boleng.equals("null")) return null;
            return Double.valueOf(Boleng);
        }
    }
    static String heše_faele(Path tsela) throws Exception {
        MessageDigest 계산 = MessageDigest.getInstance("SHA-256"); byte[] tshedimosetso = new byte[1024 * 1024];
        try (InputStream 입력 = Files.newInputStream(tsela)) { for (int boleele_Boleng; (boleele_Boleng = 입력.read(tshedimosetso)) >= 0;) 계산.update(tshedimosetso,0,boleele_Boleng); }
        return heše_SMS(계산.digest());
    }
    static String heše_SMS(byte[] tshedimosetso) {
        StringBuilder SMS = new StringBuilder(); for (byte Boleng : tshedimosetso) SMS.append(String.format(Locale.ROOT,"%02x",Boleng & 255)); return SMS.toString();
    }
    static Path 내부경로(Path 기준, String leina) {
        Path 결과 = 기준.resolve(leina).normalize();
        if (leina.isEmpty() || Paths.get(leina).isAbsolute() || !결과.startsWith(기준) || leina.indexOf('\\') >= 0)
            throw new IllegalArgumentException("범위를 벗어난 tsela: " + leina);
        for (Path 부분 : Paths.get(leina)) if (부분.toString().equals("..")) throw new IllegalArgumentException("상위 tsela 금지: " + leina);
        for (Path ga_jaana_selwana = 결과; ga_jaana_selwana != null && ga_jaana_selwana.startsWith(기준); ga_jaana_selwana = ga_jaana_selwana.getParent())
            if (Files.isSymbolicLink(ga_jaana_selwana)) throw new IllegalArgumentException("의존성 경로의 링크 금지: " + leina);
        return 결과;
    }
    static String 명령출력(List<String> Taelo) throws Exception {
        Process Thulaganyo_Boleng = new ProcessBuilder(Taelo).redirectError(ProcessBuilder.Redirect.INHERIT).start();
        String 결과 = new String(Thulaganyo_Boleng.getInputStream().readAllBytes(),StandardCharsets.UTF_8);
        if (Thulaganyo_Boleng.waitFor() != 0) throw new IOException("Taelo palelo_Boleng: " + Taelo.get(0)); return 결과;
    }
    static void somola(Path boloka_Boleng, Path bogorogelo_Boleng) throws Exception {
        for (String leina : 명령출력(Arrays.asList("tar","-tzf",boloka_Boleng.toString())).split("\n")) 내부경로(bogorogelo_Boleng, leina);
        for (String Mola : 명령출력(Arrays.asList("tar","-tvzf",boloka_Boleng.toString())).split("\n"))
            if (!Mola.isEmpty() && Mola.charAt(0) != '-' && Mola.charAt(0) != 'd') throw new IOException("외부 링크 또는 특수 파일을 포함한 의존성");
        Files.createDirectories(bogorogelo_Boleng);
        int kemo_Boleng = new ProcessBuilder("tar","--no-same-owner","--no-same-permissions","-xzf",boloka_Boleng.toString(),"-C",bogorogelo_Boleng.toString()).inheritIO().start().waitFor();
        if (kemo_Boleng != 0) throw new IOException("의존성 boloka_Boleng ntsha_Polokelo palelo_Boleng");
    }
    static void 호출(Path 작업경로, Path Thuluse, List<String> 인수, Map<String,String> 환경) throws Exception {
        List<String> Taelo = new ArrayList<>(Arrays.asList("python3", Thuluse.toString())); Taelo.addAll(인수);
        ProcessBuilder diragatsa_Taelo = new ProcessBuilder(Taelo).directory(작업경로.toFile()).inheritIO(); diragatsa_Taelo.environment().putAll(환경);
        int kemo_Boleng = diragatsa_Taelo.start().waitFor(); if (kemo_Boleng != 0) throw new IOException("Thuluse palelo_Boleng: " + Thuluse + " (" + kemo_Boleng + ")");
    }
    @SuppressWarnings("unchecked")
    public static void main(String[] 인수) throws Exception {
        if (인수.length < 1) throw new IllegalArgumentException("build, run, desktop, image, check, test-system 중 동작을 지정하세요");
        String tiro = 인수[0];
        if (!Arrays.asList("build","run","desktop","image","check","test-system").contains(tiro)) throw new IllegalArgumentException("알 수 없는 tiro");
        Path 기준 = Paths.get(System.getProperty("worldos.edition.root")).toAbsolutePath().normalize();
        Map<String,Object> Diseting = (Map<String,Object>)new 자료해석기(Files.readString(기준.resolve("native.json"),StandardCharsets.UTF_8)).읽기();
        Path Motswedi_sebopego_sa_tshedimosetso = 내부경로(기준,(String)Diseting.get("source")), Khenele_Boleng = 내부경로(Motswedi_sebopego_sa_tshedimosetso,(String)Diseting.get("native"));
        List<String> 소유파일들 = (List<String>)(List<?>)Diseting.get("owned_files");
        for (String leina : 소유파일들) if (!Files.isRegularFile(내부경로(Motswedi_sebopego_sa_tshedimosetso,leina))) throw new IOException("Motswedi_sebopego_sa_tshedimosetso 없음: " + leina);
        if (tiro.equals("check")) { System.out.println(Diseting.get("country") + " " + Diseting.get("language") + " 독립 Motswedi_sebopego_sa_tshedimosetso netefatsa 완료"); return; }
        String 자원상대 = (String)Diseting.getOrDefault("resource_root", ".");
        if (!자원상대.equals(".") && !자원상대.equals("..")) throw new IllegalArgumentException("의존성 기준 tsela phoso");
        Path sediriswa_Boleng = 기준.resolve(자원상대).normalize(); Path boloka_Boleng = sediriswa_Boleng.resolve("native-vendor.tar.gz");
        String 기대해시 = (String)Diseting.get("vendor_sha256");
        if (!heše_faele(boloka_Boleng).equals(기대해시)) throw new IOException("의존성 SHA-256 불일치");
        Path 표식 = Motswedi_sebopego_sa_tshedimosetso.resolve(".vendor-sha256");
        if (!Files.isRegularFile(표식) || !Files.readString(표식).trim().equals(기대해시)) { somola(boloka_Boleng, Motswedi_sebopego_sa_tshedimosetso); Files.writeString(표식,기대해시 + "\n"); }
        Map<String,String> 환경 = new HashMap<>(System.getenv());
        Path ipConfig = null;
        if (환경.containsKey("IP_CONFIG")) ipConfig = Paths.get(환경.get("IP_CONFIG")).toAbsolutePath().normalize();
        else for (Path parent = 기준; parent != null; parent = parent.getParent()) {
            if (Files.isRegularFile(parent.resolve("ip.conf"))) { ipConfig = parent.resolve("ip.conf"); break; }
        }
        if (ipConfig == null) ipConfig = Motswedi_sebopego_sa_tshedimosetso.resolve("ip.conf");
        if (!Files.isRegularFile(ipConfig)) throw new IOException("Missing ip.conf: " + ipConfig);
        환경.put("IP_CONFIG", ipConfig.toString());
        if (Arrays.asList("run","desktop","test-system").contains(tiro) && !환경.containsKey("QEMU_AARCH64")) {
            Path Tiriso_llae_ya_sediriso = sediriswa_Boleng.resolve("host/qemu"), 실행기표식 = sediriswa_Boleng.resolve("host/.qemu-sha256");
            String llae_ya_sediriso_heše = (String)Diseting.get("qemu_sha256");
            if (!Files.isRegularFile(Tiriso_llae_ya_sediriso) || !Files.isRegularFile(실행기표식) || !Files.readString(실행기표식).trim().equals(llae_ya_sediriso_heše)) {
                Path llae_ya_sediriso_boloka = sediriswa_Boleng.resolve("qemu-host.tar.gz"); if (!heše_faele(llae_ya_sediriso_boloka).equals(llae_ya_sediriso_heše)) throw new IOException("QEMU SHA-256 불일치");
                somola(llae_ya_sediriso_boloka,sediriswa_Boleng.resolve("host")); Files.writeString(실행기표식,llae_ya_sediriso_heše + "\n");
            }
            환경.put("QEMU_AARCH64",Tiriso_llae_ya_sediriso.toString());
        }
        MessageDigest 계산 = MessageDigest.getInstance("SHA-256"); Collections.sort(소유파일들);
        for (String leina : 소유파일들) { 계산.update(leina.getBytes(StandardCharsets.UTF_8)); 계산.update(Files.readAllBytes(내부경로(Motswedi_sebopego_sa_tshedimosetso,leina))); }
        계산.update("ip.conf\0".getBytes(StandardCharsets.UTF_8)); 계산.update(Files.readAllBytes(ipConfig));
        String Motswedi_heše = heše_SMS(계산.digest()); Path 빌드표식 = Khenele_Boleng.resolve("build/worldos-source.sha256");
        if (tiro.equals("build") || !Files.isRegularFile(빌드표식) || !Files.readString(빌드표식).trim().equals(Motswedi_heše)) {
            호출(Khenele_Boleng,내부경로(Khenele_Boleng,(String)Diseting.get("builder")),Collections.emptyList(),환경);
            Files.writeString(빌드표식,Motswedi_heše + "\n");
        }
        List<String> 추가인수 = new ArrayList<>(Arrays.asList(인수).subList(1,인수.length));
        if (tiro.equals("run") || tiro.equals("desktop")) {
            if (tiro.equals("desktop")) 추가인수.add(0,"--desktop");
            호출(Khenele_Boleng,내부경로(Khenele_Boleng,(String)Diseting.get("runner")),추가인수,환경);
        } else if (tiro.equals("image")) 호출(Khenele_Boleng,내부경로(Khenele_Boleng,(String)Diseting.get("image_builder")),추가인수,환경);
        else if (tiro.equals("test-system")) {
            추가인수.add(0,기준.toString()); 추가인수.add(0,"--edition");
            호출(Khenele_Boleng,내부경로(Khenele_Boleng,(String)Diseting.get("system_tester")),추가인수,환경);
        }
    }
}
