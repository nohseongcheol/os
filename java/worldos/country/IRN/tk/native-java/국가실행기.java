// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.security.MessageDigest;
import java.util.*;

/** 독립 국가판의 의존성 검사·복원·düz_ulgam·실행을 맡는 esasy Java Gurallar. */
public final class 국가실행기 {
    static final class 자료해석기 {
        final String Çeşme; int 위치;
        자료해석기(String Metin) { Çeşme = Metin; }
        void 빈칸() { while (위치 < Çeşme.length() && Character.isWhitespace(Çeşme.charAt(위치))) 위치++; }
        Object Oka() {
            빈칸(); char nyşan_baha_068c2631 = Çeşme.charAt(위치++);
            if (nyşan_baha_068c2631 == '{') {
                Map<String,Object> 결과 = new LinkedHashMap<>(); 빈칸();
                if (Çeşme.charAt(위치) == '}') { 위치++; return 결과; }
                while (true) {
                    String Ad = (String)Oka(); 빈칸(); if (Çeşme.charAt(위치++) != ':') throw new IllegalArgumentException("maglumat bölüji_baha_d8ba4873 Hata");
                    결과.put(Ad, Oka()); 빈칸(); char bölüji_baha_d8ba4873 = Çeşme.charAt(위치++);
                    if (bölüji_baha_d8ba4873 == '}') return 결과; if (bölüji_baha_d8ba4873 != ',') throw new IllegalArgumentException("maglumat bölüji_baha_d8ba4873 Hata");
                }
            }
            if (nyşan_baha_068c2631 == '[') {
                List<Object> 결과 = new ArrayList<>(); 빈칸();
                if (Çeşme.charAt(위치) == ']') { 위치++; return 결과; }
                while (true) {
                    결과.add(Oka()); 빈칸(); char bölüji_baha_d8ba4873 = Çeşme.charAt(위치++);
                    if (bölüji_baha_d8ba4873 == ']') return 결과; if (bölüji_baha_d8ba4873 != ',') throw new IllegalArgumentException("maglumat bölüji_baha_d8ba4873 Hata");
                }
            }
            if (nyşan_baha_068c2631 == '"') {
                StringBuilder 결과 = new StringBuilder();
                while (true) {
                    char 다음 = Çeşme.charAt(위치++); if (다음 == '"') return 결과.toString();
                    if (다음 == '\\') {
                        다음 = Çeşme.charAt(위치++);
                        if (다음 == 'u') { 결과.append((char)Integer.parseInt(Çeşme.substring(위치, 위치 + 4),16)); 위치 += 4; continue; }
                        if (다음 == 'n') 다음 = '\n'; else if (다음 == 'r') 다음 = '\r'; else if (다음 == 't') 다음 = '\t';
                        else if (다음 == 'b') 다음 = '\b'; else if (다음 == 'f') 다음 = '\f';
                        else if (다음 != '"' && 다음 != '\\' && 다음 != '/') throw new IllegalArgumentException("문자 이스케이프 Hata");
                    }
                    결과.append(다음);
                }
            }
            int Bitir = 위치 - 1;
            while (위치 < Çeşme.length() && ",]} \t\r\n".indexOf(Çeşme.charAt(위치)) < 0) 위치++;
            String baha = Çeşme.substring(Bitir, 위치);
            if (baha.equals("true")) return Boolean.TRUE; if (baha.equals("false")) return Boolean.FALSE; if (baha.equals("null")) return null;
            return Double.valueOf(baha);
        }
    }
    static String heş_kody_faýl(Path Ýol) throws Exception {
        MessageDigest 계산 = MessageDigest.getInstance("SHA-256"); byte[] maglumat = new byte[1024 * 1024];
        try (InputStream 입력 = Files.newInputStream(Ýol)) { for (int dowamlylyk_baha; (dowamlylyk_baha = 입력.read(maglumat)) >= 0;) 계산.update(maglumat,0,dowamlylyk_baha); }
        return heş_kody_SMS(계산.digest());
    }
    static String heş_kody_SMS(byte[] maglumat) {
        StringBuilder Metin = new StringBuilder(); for (byte baha : maglumat) Metin.append(String.format(Locale.ROOT,"%02x",baha & 255)); return Metin.toString();
    }
    static Path 내부경로(Path 기준, String Ad) {
        Path 결과 = 기준.resolve(Ad).normalize();
        if (Ad.isEmpty() || Paths.get(Ad).isAbsolute() || !결과.startsWith(기준) || Ad.indexOf('\\') >= 0)
            throw new IllegalArgumentException("범위를 벗어난 Ýol: " + Ad);
        for (Path 부분 : Paths.get(Ad)) if (부분.toString().equals("..")) throw new IllegalArgumentException("상위 Ýol 금지: " + Ad);
        for (Path 현재 = 결과; 현재 != null && 현재.startsWith(기준); 현재 = 현재.getParent())
            if (Files.isSymbolicLink(현재)) throw new IllegalArgumentException("의존성 경로의 링크 금지: " + Ad);
        return 결과;
    }
    static String 명령출력(List<String> buýruk) throws Exception {
        Process Proses_baha = new ProcessBuilder(buýruk).redirectError(ProcessBuilder.Redirect.INHERIT).start();
        String 결과 = new String(Proses_baha.getInputStream().readAllBytes(),StandardCharsets.UTF_8);
        if (Proses_baha.waitFor() != 0) throw new IOException("buýruk näsazlyk_baha: " + buýruk.get(0)); return 결과;
    }
    static void sapla(Path Arhiw_baha, Path barylmaly_ýer_baha) throws Exception {
        for (String Ad : 명령출력(Arrays.asList("tar","-tzf",Arhiw_baha.toString())).split("\n")) 내부경로(barylmaly_ýer_baha, Ad);
        for (String setir : 명령출력(Arrays.asList("tar","-tvzf",Arhiw_baha.toString())).split("\n"))
            if (!setir.isEmpty() && setir.charAt(0) != '-' && setir.charAt(0) != 'd') throw new IOException("외부 링크 또는 특수 파일을 포함한 의존성");
        Files.createDirectories(barylmaly_ýer_baha);
        int ýagdaý_baha = new ProcessBuilder("tar","--no-same-owner","--no-same-permissions","-xzf",Arhiw_baha.toString(),"-C",barylmaly_ýer_baha.toString()).inheritIO().start().waitFor();
        if (ýagdaý_baha != 0) throw new IOException("의존성 Arhiw_baha goýbermek_Ammar näsazlyk_baha");
    }
    static void 호출(Path 작업경로, Path Gurallar, List<String> 인수, Map<String,String> 환경) throws Exception {
        List<String> buýruk = new ArrayList<>(Arrays.asList("python3", Gurallar.toString())); buýruk.addAll(인수);
        ProcessBuilder ýerine_ýetir_buýruk = new ProcessBuilder(buýruk).directory(작업경로.toFile()).inheritIO(); ýerine_ýetir_buýruk.environment().putAll(환경);
        int ýagdaý_baha = ýerine_ýetir_buýruk.start().waitFor(); if (ýagdaý_baha != 0) throw new IOException("Gurallar näsazlyk_baha: " + Gurallar + " (" + ýagdaý_baha + ")");
    }
    @SuppressWarnings("unchecked")
    public static void main(String[] 인수) throws Exception {
        if (인수.length < 1) throw new IllegalArgumentException("build, run, desktop, image, check, test-system 중 동작을 지정하세요");
        String iş = 인수[0];
        if (!Arrays.asList("build","run","desktop","image","check","test-system").contains(iş)) throw new IllegalArgumentException("알 수 없는 iş");
        Path 기준 = Paths.get(System.getProperty("worldos.edition.root")).toAbsolutePath().normalize();
        Map<String,Object> Düzümler = (Map<String,Object>)new 자료해석기(Files.readString(기준.resolve("native.json"),StandardCharsets.UTF_8)).Oka();
        Path gor_agaç = 내부경로(기준,(String)Düzümler.get("source")), ýadro_baha = 내부경로(gor_agaç,(String)Düzümler.get("native"));
        List<String> 소유파일들 = (List<String>)(List<?>)Düzümler.get("owned_files");
        for (String Ad : 소유파일들) if (!Files.isRegularFile(내부경로(gor_agaç,Ad))) throw new IOException("gor_agaç 없음: " + Ad);
        if (iş.equals("check")) { System.out.println(Düzümler.get("country") + " " + Düzümler.get("language") + " 독립 gor_agaç barla 완료"); return; }
        String 자원상대 = (String)Düzümler.getOrDefault("resource_root", ".");
        if (!자원상대.equals(".") && !자원상대.equals("..")) throw new IllegalArgumentException("의존성 기준 Ýol Hata");
        Path gor_baha = 기준.resolve(자원상대).normalize(); Path Arhiw_baha = gor_baha.resolve("native-vendor.tar.gz");
        String 기대해시 = (String)Düzümler.get("vendor_sha256");
        if (!heş_kody_faýl(Arhiw_baha).equals(기대해시)) throw new IOException("의존성 SHA-256 불일치");
        Path 표식 = gor_agaç.resolve(".vendor-sha256");
        if (!Files.isRegularFile(표식) || !Files.readString(표식).trim().equals(기대해시)) { sapla(Arhiw_baha, gor_agaç); Files.writeString(표식,기대해시 + "\n"); }
        Map<String,String> 환경 = new HashMap<>(System.getenv());
        Path ipConfig = null;
        if (환경.containsKey("IP_CONFIG")) ipConfig = Paths.get(환경.get("IP_CONFIG")).toAbsolutePath().normalize();
        else for (Path parent = 기준; parent != null; parent = parent.getParent()) {
            if (Files.isRegularFile(parent.resolve("ip.conf"))) { ipConfig = parent.resolve("ip.conf"); break; }
        }
        if (ipConfig == null) ipConfig = gor_agaç.resolve("ip.conf");
        if (!Files.isRegularFile(ipConfig)) throw new IOException("Missing ip.conf: " + ipConfig);
        환경.put("IP_CONFIG", ipConfig.toString());
        if (Arrays.asList("run","desktop","test-system").contains(iş) && !환경.containsKey("QEMU_AARCH64")) {
            Path programma_programma_paneli = gor_baha.resolve("host/qemu"), 실행기표식 = gor_baha.resolve("host/.qemu-sha256");
            String programma_paneli_heş_kody = (String)Düzümler.get("qemu_sha256");
            if (!Files.isRegularFile(programma_programma_paneli) || !Files.isRegularFile(실행기표식) || !Files.readString(실행기표식).trim().equals(programma_paneli_heş_kody)) {
                Path programma_paneli_Arhiw = gor_baha.resolve("qemu-host.tar.gz"); if (!heş_kody_faýl(programma_paneli_Arhiw).equals(programma_paneli_heş_kody)) throw new IOException("QEMU SHA-256 불일치");
                sapla(programma_paneli_Arhiw,gor_baha.resolve("host")); Files.writeString(실행기표식,programma_paneli_heş_kody + "\n");
            }
            환경.put("QEMU_AARCH64",programma_programma_paneli.toString());
        }
        MessageDigest 계산 = MessageDigest.getInstance("SHA-256"); Collections.sort(소유파일들);
        for (String Ad : 소유파일들) { 계산.update(Ad.getBytes(StandardCharsets.UTF_8)); 계산.update(Files.readAllBytes(내부경로(gor_agaç,Ad))); }
        계산.update("ip.conf\0".getBytes(StandardCharsets.UTF_8)); 계산.update(Files.readAllBytes(ipConfig));
        String gor_heş_kody = heş_kody_SMS(계산.digest()); Path 빌드표식 = ýadro_baha.resolve("build/worldos-source.sha256");
        if (iş.equals("build") || !Files.isRegularFile(빌드표식) || !Files.readString(빌드표식).trim().equals(gor_heş_kody)) {
            호출(ýadro_baha,내부경로(ýadro_baha,(String)Düzümler.get("builder")),Collections.emptyList(),환경);
            Files.writeString(빌드표식,gor_heş_kody + "\n");
        }
        List<String> 추가인수 = new ArrayList<>(Arrays.asList(인수).subList(1,인수.length));
        if (iş.equals("run") || iş.equals("desktop")) {
            if (iş.equals("desktop")) 추가인수.add(0,"--desktop");
            호출(ýadro_baha,내부경로(ýadro_baha,(String)Düzümler.get("runner")),추가인수,환경);
        } else if (iş.equals("image")) 호출(ýadro_baha,내부경로(ýadro_baha,(String)Düzümler.get("image_builder")),추가인수,환경);
        else if (iş.equals("test-system")) {
            추가인수.add(0,기준.toString()); 추가인수.add(0,"--edition");
            호출(ýadro_baha,내부경로(ýadro_baha,(String)Düzümler.get("system_tester")),추가인수,환경);
        }
    }
}
