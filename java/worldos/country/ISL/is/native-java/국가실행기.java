// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.security.MessageDigest;
import java.util.*;

/** 독립 국가판의 의존성 검사·복원·smíð_kerfi·실행을 맡는 hýsa Java Verkfæri. */
public final class 국가실행기 {
    static final class gögn_þáttari {
        final String Uppruni; int Staðsetning;
        gögn_þáttari(String Texti) { Uppruni = Texti; }
        void 빈칸() { while (Staðsetning < Uppruni.length() && Character.isWhitespace(Uppruni.charAt(Staðsetning))) Staðsetning++; }
        Object Lestur() {
            빈칸(); char stafur_VALUE = Uppruni.charAt(Staðsetning++);
            if (stafur_VALUE == '{') {
                Map<String,Object> NIÐURSTAÐA = new LinkedHashMap<>(); 빈칸();
                if (Uppruni.charAt(Staðsetning) == '}') { Staðsetning++; return NIÐURSTAÐA; }
                while (true) {
                    String Heiti = (String)Lestur(); 빈칸(); if (Uppruni.charAt(Staðsetning++) != ':') throw new IllegalArgumentException("gögn skiltákn_VALUE_d8ba4873 Villa");
                    NIÐURSTAÐA.put(Heiti, Lestur()); 빈칸(); char skiltákn_VALUE_d8ba4873 = Uppruni.charAt(Staðsetning++);
                    if (skiltákn_VALUE_d8ba4873 == '}') return NIÐURSTAÐA; if (skiltákn_VALUE_d8ba4873 != ',') throw new IllegalArgumentException("gögn skiltákn_VALUE_d8ba4873 Villa");
                }
            }
            if (stafur_VALUE == '[') {
                List<Object> NIÐURSTAÐA = new ArrayList<>(); 빈칸();
                if (Uppruni.charAt(Staðsetning) == ']') { Staðsetning++; return NIÐURSTAÐA; }
                while (true) {
                    NIÐURSTAÐA.add(Lestur()); 빈칸(); char skiltákn_VALUE_d8ba4873 = Uppruni.charAt(Staðsetning++);
                    if (skiltákn_VALUE_d8ba4873 == ']') return NIÐURSTAÐA; if (skiltákn_VALUE_d8ba4873 != ',') throw new IllegalArgumentException("gögn skiltákn_VALUE_d8ba4873 Villa");
                }
            }
            if (stafur_VALUE == '"') {
                StringBuilder NIÐURSTAÐA = new StringBuilder();
                while (true) {
                    char Áfram_vara = Uppruni.charAt(Staðsetning++); if (Áfram_vara == '"') return NIÐURSTAÐA.toString();
                    if (Áfram_vara == '\\') {
                        Áfram_vara = Uppruni.charAt(Staðsetning++);
                        if (Áfram_vara == 'u') { NIÐURSTAÐA.append((char)Integer.parseInt(Uppruni.substring(Staðsetning, Staðsetning + 4),16)); Staðsetning += 4; continue; }
                        if (Áfram_vara == 'n') Áfram_vara = '\n'; else if (Áfram_vara == 'r') Áfram_vara = '\r'; else if (Áfram_vara == 't') Áfram_vara = '\t';
                        else if (Áfram_vara == 'b') Áfram_vara = '\b'; else if (Áfram_vara == 'f') Áfram_vara = '\f';
                        else if (Áfram_vara != '"' && Áfram_vara != '\\' && Áfram_vara != '/') throw new IllegalArgumentException("문자 이스케이프 Villa");
                    }
                    NIÐURSTAÐA.append(Áfram_vara);
                }
            }
            int Keyra_2 = Staðsetning - 1;
            while (Staðsetning < Uppruni.length() && ",]} \t\r\n".indexOf(Uppruni.charAt(Staðsetning)) < 0) Staðsetning++;
            String VALUE = Uppruni.substring(Keyra_2, Staðsetning);
            if (VALUE.equals("true")) return Boolean.TRUE; if (VALUE.equals("false")) return Boolean.FALSE; if (VALUE.equals("null")) return null;
            return Double.valueOf(VALUE);
        }
    }
    static String tæting_skrá(Path SLÓÐ) throws Exception {
        MessageDigest 계산 = MessageDigest.getInstance("SHA-256"); byte[] gögn = new byte[1024 * 1024];
        try (InputStream 입력 = Files.newInputStream(SLÓÐ)) { for (int lengd_VALUE; (lengd_VALUE = 입력.read(gögn)) >= 0;) 계산.update(gögn,0,lengd_VALUE); }
        return tæting_SMS(계산.digest());
    }
    static String tæting_SMS(byte[] gögn) {
        StringBuilder Texti = new StringBuilder(); for (byte VALUE : gögn) Texti.append(String.format(Locale.ROOT,"%02x",VALUE & 255)); return Texti.toString();
    }
    static Path 내부경로(Path verk_rót, String Heiti) {
        Path NIÐURSTAÐA = verk_rót.resolve(Heiti).normalize();
        if (Heiti.isEmpty() || Paths.get(Heiti).isAbsolute() || !NIÐURSTAÐA.startsWith(verk_rót) || Heiti.indexOf('\\') >= 0)
            throw new IllegalArgumentException("범위를 벗어난 SLÓÐ: " + Heiti);
        for (Path 부분 : Paths.get(Heiti)) if (부분.toString().equals("..")) throw new IllegalArgumentException("상위 SLÓÐ 금지: " + Heiti);
        for (Path 현재 = NIÐURSTAÐA; 현재 != null && 현재.startsWith(verk_rót); 현재 = 현재.getParent())
            if (Files.isSymbolicLink(현재)) throw new IllegalArgumentException("의존성 경로의 링크 금지: " + Heiti);
        return NIÐURSTAÐA;
    }
    static String skipun_úttak(List<String> Skipun) throws Exception {
        Process Ferli_VALUE = new ProcessBuilder(Skipun).redirectError(ProcessBuilder.Redirect.INHERIT).start();
        String NIÐURSTAÐA = new String(Ferli_VALUE.getInputStream().readAllBytes(),StandardCharsets.UTF_8);
        if (Ferli_VALUE.waitFor() != 0) throw new IOException("Skipun bilun_VALUE: " + Skipun.get(0)); return NIÐURSTAÐA;
    }
    static void draga_út(Path Safn_VALUE, Path endastaður_VALUE) throws Exception {
        for (String Heiti : skipun_úttak(Arrays.asList("tar","-tzf",Safn_VALUE.toString())).split("\n")) 내부경로(endastaður_VALUE, Heiti);
        for (String Lína : skipun_úttak(Arrays.asList("tar","-tvzf",Safn_VALUE.toString())).split("\n"))
            if (!Lína.isEmpty() && Lína.charAt(0) != '-' && Lína.charAt(0) != 'd') throw new IOException("외부 링크 또는 특수 파일을 포함한 의존성");
        Files.createDirectories(endastaður_VALUE);
        int staða_VALUE_e10195a1 = new ProcessBuilder("tar","--no-same-owner","--no-same-permissions","-xzf",Safn_VALUE.toString(),"-C",endastaður_VALUE.toString()).inheritIO().start().waitFor();
        if (staða_VALUE_e10195a1 != 0) throw new IOException("의존성 Safn_VALUE losa_geymsla bilun_VALUE");
    }
    static void 호출(Path 작업경로, Path Verkfæri, List<String> Viðföng, Map<String,String> 환경) throws Exception {
        List<String> Skipun = new ArrayList<>(Arrays.asList("python3", Verkfæri.toString())); Skipun.addAll(Viðföng);
        ProcessBuilder keyra_skipun = new ProcessBuilder(Skipun).directory(작업경로.toFile()).inheritIO(); keyra_skipun.environment().putAll(환경);
        int staða_VALUE_e10195a1 = keyra_skipun.start().waitFor(); if (staða_VALUE_e10195a1 != 0) throw new IOException("Verkfæri bilun_VALUE: " + Verkfæri + " (" + staða_VALUE_e10195a1 + ")");
    }
    @SuppressWarnings("unchecked")
    public static void main(String[] Viðföng) throws Exception {
        if (Viðföng.length < 1) throw new IllegalArgumentException("build, run, desktop, image, check, test-system 중 동작을 지정하세요");
        String Aðgerð = Viðföng[0];
        if (!Arrays.asList("build","run","desktop","image","check","test-system").contains(Aðgerð)) throw new IllegalArgumentException("알 númer 없는 Aðgerð");
        Path verk_rót = Paths.get(System.getProperty("worldos.edition.root")).toAbsolutePath().normalize();
        Map<String,Object> Stillingar = (Map<String,Object>)new gögn_þáttari(Files.readString(verk_rót.resolve("native.json"),StandardCharsets.UTF_8)).Lestur();
        Path uppruni_tré = 내부경로(verk_rót,(String)Stillingar.get("source")), kjarni_VALUE = 내부경로(uppruni_tré,(String)Stillingar.get("native"));
        List<String> 소유파일들 = (List<String>)(List<?>)Stillingar.get("owned_files");
        for (String Heiti : 소유파일들) if (!Files.isRegularFile(내부경로(uppruni_tré,Heiti))) throw new IOException("uppruni_tré 없음: " + Heiti);
        if (Aðgerð.equals("check")) { System.out.println(Stillingar.get("country") + " " + Stillingar.get("language") + " 독립 uppruni_tré sannprófa 완료"); return; }
        String 자원상대 = (String)Stillingar.getOrDefault("resource_root", ".");
        if (!자원상대.equals(".") && !자원상대.equals("..")) throw new IllegalArgumentException("의존성 verk_rót SLÓÐ Villa");
        Path tilfang_VALUE = verk_rót.resolve(자원상대).normalize(); Path Safn_VALUE = tilfang_VALUE.resolve("native-vendor.tar.gz");
        String 기대해시 = (String)Stillingar.get("vendor_sha256");
        if (!tæting_skrá(Safn_VALUE).equals(기대해시)) throw new IOException("의존성 SHA-256 불일치");
        Path 표식 = uppruni_tré.resolve(".vendor-sha256");
        if (!Files.isRegularFile(표식) || !Files.readString(표식).trim().equals(기대해시)) { draga_út(Safn_VALUE, uppruni_tré); Files.writeString(표식,기대해시 + "\n"); }
        Map<String,String> 환경 = new HashMap<>(System.getenv());
        Path ipConfig = null;
        if (환경.containsKey("IP_CONFIG")) ipConfig = Paths.get(환경.get("IP_CONFIG")).toAbsolutePath().normalize();
        else for (Path parent = verk_rót; parent != null; parent = parent.getParent()) {
            if (Files.isRegularFile(parent.resolve("ip.conf"))) { ipConfig = parent.resolve("ip.conf"); break; }
        }
        if (ipConfig == null) ipConfig = uppruni_tré.resolve("ip.conf");
        if (!Files.isRegularFile(ipConfig)) throw new IOException("Missing ip.conf: " + ipConfig);
        환경.put("IP_CONFIG", ipConfig.toString());
        if (Arrays.asList("run","desktop","test-system").contains(Aðgerð) && !환경.containsKey("QEMU_AARCH64")) {
            Path forrit_ræsir = tilfang_VALUE.resolve("host/qemu"), 실행기표식 = tilfang_VALUE.resolve("host/.qemu-sha256");
            String ræsir_tæting = (String)Stillingar.get("qemu_sha256");
            if (!Files.isRegularFile(forrit_ræsir) || !Files.isRegularFile(실행기표식) || !Files.readString(실행기표식).trim().equals(ræsir_tæting)) {
                Path ræsir_Safn = tilfang_VALUE.resolve("qemu-host.tar.gz"); if (!tæting_skrá(ræsir_Safn).equals(ræsir_tæting)) throw new IOException("QEMU SHA-256 불일치");
                draga_út(ræsir_Safn,tilfang_VALUE.resolve("host")); Files.writeString(실행기표식,ræsir_tæting + "\n");
            }
            환경.put("QEMU_AARCH64",forrit_ræsir.toString());
        }
        MessageDigest 계산 = MessageDigest.getInstance("SHA-256"); Collections.sort(소유파일들);
        for (String Heiti : 소유파일들) { 계산.update(Heiti.getBytes(StandardCharsets.UTF_8)); 계산.update(Files.readAllBytes(내부경로(uppruni_tré,Heiti))); }
        계산.update("ip.conf\0".getBytes(StandardCharsets.UTF_8)); 계산.update(Files.readAllBytes(ipConfig));
        String uppruni_tæting = tæting_SMS(계산.digest()); Path 빌드표식 = kjarni_VALUE.resolve("build/worldos-source.sha256");
        if (Aðgerð.equals("build") || !Files.isRegularFile(빌드표식) || !Files.readString(빌드표식).trim().equals(uppruni_tæting)) {
            호출(kjarni_VALUE,내부경로(kjarni_VALUE,(String)Stillingar.get("builder")),Collections.emptyList(),환경);
            Files.writeString(빌드표식,uppruni_tæting + "\n");
        }
        List<String> 추가인수 = new ArrayList<>(Arrays.asList(Viðföng).subList(1,Viðföng.length));
        if (Aðgerð.equals("run") || Aðgerð.equals("desktop")) {
            if (Aðgerð.equals("desktop")) 추가인수.add(0,"--desktop");
            호출(kjarni_VALUE,내부경로(kjarni_VALUE,(String)Stillingar.get("runner")),추가인수,환경);
        } else if (Aðgerð.equals("image")) 호출(kjarni_VALUE,내부경로(kjarni_VALUE,(String)Stillingar.get("image_builder")),추가인수,환경);
        else if (Aðgerð.equals("test-system")) {
            추가인수.add(0,verk_rót.toString()); 추가인수.add(0,"--edition");
            호출(kjarni_VALUE,내부경로(kjarni_VALUE,(String)Stillingar.get("system_tester")),추가인수,환경);
        }
    }
}
