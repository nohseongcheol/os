// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.security.MessageDigest;
import java.util.*;

/** 독립 국가판의 의존성 검사·복원·qurmaq_sistem·실행을 맡는 host Java Alətlər. */
public final class 국가실행기 {
    static final class verilənlər_parser {
        final String QAYNAQ; int yerinə_qoymaq;
        verilənlər_parser(String Mətn) { QAYNAQ = Mətn; }
        void 빈칸() { while (yerinə_qoymaq < QAYNAQ.length() && Character.isWhitespace(QAYNAQ.charAt(yerinə_qoymaq))) yerinə_qoymaq++; }
        Object Oxuma() {
            빈칸(); char simvol_VALUE_068c2631 = QAYNAQ.charAt(yerinə_qoymaq++);
            if (simvol_VALUE_068c2631 == '{') {
                Map<String,Object> ölçü = new LinkedHashMap<>(); 빈칸();
                if (QAYNAQ.charAt(yerinə_qoymaq) == '}') { yerinə_qoymaq++; return ölçü; }
                while (true) {
                    String Ad = (String)Oxuma(); 빈칸(); if (QAYNAQ.charAt(yerinə_qoymaq++) != ':') throw new IllegalArgumentException("verilənlər ayırıcı_VALUE_d8ba4873 XƏTA");
                    ölçü.put(Ad, Oxuma()); 빈칸(); char ayırıcı_VALUE_d8ba4873 = QAYNAQ.charAt(yerinə_qoymaq++);
                    if (ayırıcı_VALUE_d8ba4873 == '}') return ölçü; if (ayırıcı_VALUE_d8ba4873 != ',') throw new IllegalArgumentException("verilənlər ayırıcı_VALUE_d8ba4873 XƏTA");
                }
            }
            if (simvol_VALUE_068c2631 == '[') {
                List<Object> ölçü = new ArrayList<>(); 빈칸();
                if (QAYNAQ.charAt(yerinə_qoymaq) == ']') { yerinə_qoymaq++; return ölçü; }
                while (true) {
                    ölçü.add(Oxuma()); 빈칸(); char ayırıcı_VALUE_d8ba4873 = QAYNAQ.charAt(yerinə_qoymaq++);
                    if (ayırıcı_VALUE_d8ba4873 == ']') return ölçü; if (ayırıcı_VALUE_d8ba4873 != ',') throw new IllegalArgumentException("verilənlər ayırıcı_VALUE_d8ba4873 XƏTA");
                }
            }
            if (simvol_VALUE_068c2631 == '"') {
                StringBuilder ölçü = new StringBuilder();
                while (true) {
                    char Sonrakı_element = QAYNAQ.charAt(yerinə_qoymaq++); if (Sonrakı_element == '"') return ölçü.toString();
                    if (Sonrakı_element == '\\') {
                        Sonrakı_element = QAYNAQ.charAt(yerinə_qoymaq++);
                        if (Sonrakı_element == 'u') { ölçü.append((char)Integer.parseInt(QAYNAQ.substring(yerinə_qoymaq, yerinə_qoymaq + 4),16)); yerinə_qoymaq += 4; continue; }
                        if (Sonrakı_element == 'n') Sonrakı_element = '\n'; else if (Sonrakı_element == 'r') Sonrakı_element = '\r'; else if (Sonrakı_element == 't') Sonrakı_element = '\t';
                        else if (Sonrakı_element == 'b') Sonrakı_element = '\b'; else if (Sonrakı_element == 'f') Sonrakı_element = '\f';
                        else if (Sonrakı_element != '"' && Sonrakı_element != '\\' && Sonrakı_element != '/') throw new IllegalArgumentException("문자 이스케이프 XƏTA");
                    }
                    ölçü.append(Sonrakı_element);
                }
            }
            int İcra_Et = yerinə_qoymaq - 1;
            while (yerinə_qoymaq < QAYNAQ.length() && ",]} \t\r\n".indexOf(QAYNAQ.charAt(yerinə_qoymaq)) < 0) yerinə_qoymaq++;
            String VALUE = QAYNAQ.substring(İcra_Et, yerinə_qoymaq);
            if (VALUE.equals("true")) return Boolean.TRUE; if (VALUE.equals("false")) return Boolean.FALSE; if (VALUE.equals("null")) return null;
            return Double.valueOf(VALUE);
        }
    }
    static String heş_fayl(Path Cığır) throws Exception {
        MessageDigest 계산 = MessageDigest.getInstance("SHA-256"); byte[] verilənlər = new byte[1024 * 1024];
        try (InputStream 입력 = Files.newInputStream(Cığır)) { for (int uzunluq_VALUE; (uzunluq_VALUE = 입력.read(verilənlər)) >= 0;) 계산.update(verilənlər,0,uzunluq_VALUE); }
        return heş_SMS(계산.digest());
    }
    static String heş_SMS(byte[] verilənlər) {
        StringBuilder Mətn = new StringBuilder(); for (byte VALUE : verilənlər) Mətn.append(String.format(Locale.ROOT,"%02x",VALUE & 255)); return Mətn.toString();
    }
    static Path 내부경로(Path Project_kök, String Ad) {
        Path ölçü = Project_kök.resolve(Ad).normalize();
        if (Ad.isEmpty() || Paths.get(Ad).isAbsolute() || !ölçü.startsWith(Project_kök) || Ad.indexOf('\\') >= 0)
            throw new IllegalArgumentException("범위를 벗어난 Cığır: " + Ad);
        for (Path 부분 : Paths.get(Ad)) if (부분.toString().equals("..")) throw new IllegalArgumentException("상위 Cığır 금지: " + Ad);
        for (Path 현재 = ölçü; 현재 != null && 현재.startsWith(Project_kök); 현재 = 현재.getParent())
            if (Files.isSymbolicLink(현재)) throw new IllegalArgumentException("의존성 경로의 링크 금지: " + Ad);
        return ölçü;
    }
    static String 명령출력(List<String> Əmr) throws Exception {
        Process Proses_VALUE = new ProcessBuilder(Əmr).redirectError(ProcessBuilder.Redirect.INHERIT).start();
        String ölçü = new String(Proses_VALUE.getInputStream().readAllBytes(),StandardCharsets.UTF_8);
        if (Proses_VALUE.waitFor() != 0) throw new IOException("Əmr xəta_VALUE: " + Əmr.get(0)); return ölçü;
    }
    static void çıxartmaq(Path Arxiv_VALUE, Path təyinat_VALUE_a0fbc067) throws Exception {
        for (String Ad : 명령출력(Arrays.asList("tar","-tzf",Arxiv_VALUE.toString())).split("\n")) 내부경로(təyinat_VALUE_a0fbc067, Ad);
        for (String Giriş : 명령출력(Arrays.asList("tar","-tvzf",Arxiv_VALUE.toString())).split("\n"))
            if (!Giriş.isEmpty() && Giriş.charAt(0) != '-' && Giriş.charAt(0) != 'd') throw new IOException("외부 링크 또는 특수 파일을 포함한 의존성");
        Files.createDirectories(təyinat_VALUE_a0fbc067);
        int vəziyyət_VALUE = new ProcessBuilder("tar","--no-same-owner","--no-same-permissions","-xzf",Arxiv_VALUE.toString(),"-C",təyinat_VALUE_a0fbc067.toString()).inheritIO().start().waitFor();
        if (vəziyyət_VALUE != 0) throw new IOException("의존성 Arxiv_VALUE burax_Yaddaş xəta_VALUE");
    }
    static void 호출(Path 작업경로, Path Alətlər, List<String> 인수, Map<String,String> 환경) throws Exception {
        List<String> Əmr = new ArrayList<>(Arrays.asList("python3", Alətlər.toString())); Əmr.addAll(인수);
        ProcessBuilder icra_etmək_əmr = new ProcessBuilder(Əmr).directory(작업경로.toFile()).inheritIO(); icra_etmək_əmr.environment().putAll(환경);
        int vəziyyət_VALUE = icra_etmək_əmr.start().waitFor(); if (vəziyyət_VALUE != 0) throw new IOException("Alətlər xəta_VALUE: " + Alətlər + " (" + vəziyyət_VALUE + ")");
    }
    @SuppressWarnings("unchecked")
    public static void main(String[] 인수) throws Exception {
        if (인수.length < 1) throw new IllegalArgumentException("build, run, desktop, image, check, test-system 중 동작을 지정하세요");
        String Gedişat = 인수[0];
        if (!Arrays.asList("build","run","desktop","image","check","test-system").contains(Gedişat)) throw new IllegalArgumentException("알 수 없는 Gedişat");
        Path Project_kök = Paths.get(System.getProperty("worldos.edition.root")).toAbsolutePath().normalize();
        Map<String,Object> Sazlama = (Map<String,Object>)new verilənlər_parser(Files.readString(Project_kök.resolve("native.json"),StandardCharsets.UTF_8)).Oxuma();
        Path mənbə_ağac = 내부경로(Project_kök,(String)Sazlama.get("source")), nüvə_VALUE = 내부경로(mənbə_ağac,(String)Sazlama.get("native"));
        List<String> 소유파일들 = (List<String>)(List<?>)Sazlama.get("owned_files");
        for (String Ad : 소유파일들) if (!Files.isRegularFile(내부경로(mənbə_ağac,Ad))) throw new IOException("mənbə_ağac 없음: " + Ad);
        if (Gedişat.equals("check")) { System.out.println(Sazlama.get("country") + " " + Sazlama.get("language") + " 독립 mənbə_ağac yoxlamaq 완료"); return; }
        String 자원상대 = (String)Sazlama.getOrDefault("resource_root", ".");
        if (!자원상대.equals(".") && !자원상대.equals("..")) throw new IllegalArgumentException("의존성 Project_kök Cığır XƏTA");
        Path resurs_VALUE = Project_kök.resolve(자원상대).normalize(); Path Arxiv_VALUE = resurs_VALUE.resolve("native-vendor.tar.gz");
        String 기대해시 = (String)Sazlama.get("vendor_sha256");
        if (!heş_fayl(Arxiv_VALUE).equals(기대해시)) throw new IOException("의존성 SHA-256 불일치");
        Path 표식 = mənbə_ağac.resolve(".vendor-sha256");
        if (!Files.isRegularFile(표식) || !Files.readString(표식).trim().equals(기대해시)) { çıxartmaq(Arxiv_VALUE, mənbə_ağac); Files.writeString(표식,기대해시 + "\n"); }
        Map<String,String> 환경 = new HashMap<>(System.getenv());
        Path ipConfig = null;
        if (환경.containsKey("IP_CONFIG")) ipConfig = Paths.get(환경.get("IP_CONFIG")).toAbsolutePath().normalize();
        else for (Path parent = Project_kök; parent != null; parent = parent.getParent()) {
            if (Files.isRegularFile(parent.resolve("ip.conf"))) { ipConfig = parent.resolve("ip.conf"); break; }
        }
        if (ipConfig == null) ipConfig = mənbə_ağac.resolve("ip.conf");
        if (!Files.isRegularFile(ipConfig)) throw new IOException("Missing ip.conf: " + ipConfig);
        환경.put("IP_CONFIG", ipConfig.toString());
        if (Arrays.asList("run","desktop","test-system").contains(Gedişat) && !환경.containsKey("QEMU_AARCH64")) {
            Path proqram_işəsalma = resurs_VALUE.resolve("host/qemu"), 실행기표식 = resurs_VALUE.resolve("host/.qemu-sha256");
            String işəsalma_heş = (String)Sazlama.get("qemu_sha256");
            if (!Files.isRegularFile(proqram_işəsalma) || !Files.isRegularFile(실행기표식) || !Files.readString(실행기표식).trim().equals(işəsalma_heş)) {
                Path işəsalma_Arxiv = resurs_VALUE.resolve("qemu-host.tar.gz"); if (!heş_fayl(işəsalma_Arxiv).equals(işəsalma_heş)) throw new IOException("QEMU SHA-256 불일치");
                çıxartmaq(işəsalma_Arxiv,resurs_VALUE.resolve("host")); Files.writeString(실행기표식,işəsalma_heş + "\n");
            }
            환경.put("QEMU_AARCH64",proqram_işəsalma.toString());
        }
        MessageDigest 계산 = MessageDigest.getInstance("SHA-256"); Collections.sort(소유파일들);
        for (String Ad : 소유파일들) { 계산.update(Ad.getBytes(StandardCharsets.UTF_8)); 계산.update(Files.readAllBytes(내부경로(mənbə_ağac,Ad))); }
        계산.update("ip.conf\0".getBytes(StandardCharsets.UTF_8)); 계산.update(Files.readAllBytes(ipConfig));
        String mənbə_heş = heş_SMS(계산.digest()); Path 빌드표식 = nüvə_VALUE.resolve("build/worldos-source.sha256");
        if (Gedişat.equals("build") || !Files.isRegularFile(빌드표식) || !Files.readString(빌드표식).trim().equals(mənbə_heş)) {
            호출(nüvə_VALUE,내부경로(nüvə_VALUE,(String)Sazlama.get("builder")),Collections.emptyList(),환경);
            Files.writeString(빌드표식,mənbə_heş + "\n");
        }
        List<String> 추가인수 = new ArrayList<>(Arrays.asList(인수).subList(1,인수.length));
        if (Gedişat.equals("run") || Gedişat.equals("desktop")) {
            if (Gedişat.equals("desktop")) 추가인수.add(0,"--desktop");
            호출(nüvə_VALUE,내부경로(nüvə_VALUE,(String)Sazlama.get("runner")),추가인수,환경);
        } else if (Gedişat.equals("image")) 호출(nüvə_VALUE,내부경로(nüvə_VALUE,(String)Sazlama.get("image_builder")),추가인수,환경);
        else if (Gedişat.equals("test-system")) {
            추가인수.add(0,Project_kök.toString()); 추가인수.add(0,"--edition");
            호출(nüvə_VALUE,내부경로(nüvə_VALUE,(String)Sazlama.get("system_tester")),추가인수,환경);
        }
    }
}
