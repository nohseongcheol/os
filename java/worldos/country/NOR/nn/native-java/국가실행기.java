// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.security.MessageDigest;
import java.util.*;

/** 독립 국가판의 의존성 검사·복원·bygg_system·실행을 맡는 vert Java Verktøy. */
public final class 국가실행기 {
    static final class 자료해석기 {
        final String KJELDE; int Posisjon;
        자료해석기(String Tekst) { KJELDE = Tekst; }
        void 빈칸() { while (Posisjon < KJELDE.length() && Character.isWhitespace(KJELDE.charAt(Posisjon))) Posisjon++; }
        Object Les() {
            빈칸(); char teikn_VALUE = KJELDE.charAt(Posisjon++);
            if (teikn_VALUE == '{') {
                Map<String,Object> forretningsmål = new LinkedHashMap<>(); 빈칸();
                if (KJELDE.charAt(Posisjon) == '}') { Posisjon++; return forretningsmål; }
                while (true) {
                    String Namn = (String)Les(); 빈칸(); if (KJELDE.charAt(Posisjon++) != ':') throw new IllegalArgumentException("data skiljeteikn_VALUE FEIL");
                    forretningsmål.put(Namn, Les()); 빈칸(); char skiljeteikn_VALUE = KJELDE.charAt(Posisjon++);
                    if (skiljeteikn_VALUE == '}') return forretningsmål; if (skiljeteikn_VALUE != ',') throw new IllegalArgumentException("data skiljeteikn_VALUE FEIL");
                }
            }
            if (teikn_VALUE == '[') {
                List<Object> forretningsmål = new ArrayList<>(); 빈칸();
                if (KJELDE.charAt(Posisjon) == ']') { Posisjon++; return forretningsmål; }
                while (true) {
                    forretningsmål.add(Les()); 빈칸(); char skiljeteikn_VALUE = KJELDE.charAt(Posisjon++);
                    if (skiljeteikn_VALUE == ']') return forretningsmål; if (skiljeteikn_VALUE != ',') throw new IllegalArgumentException("data skiljeteikn_VALUE FEIL");
                }
            }
            if (teikn_VALUE == '"') {
                StringBuilder forretningsmål = new StringBuilder();
                while (true) {
                    char Neste_vare = KJELDE.charAt(Posisjon++); if (Neste_vare == '"') return forretningsmål.toString();
                    if (Neste_vare == '\\') {
                        Neste_vare = KJELDE.charAt(Posisjon++);
                        if (Neste_vare == 'u') { forretningsmål.append((char)Integer.parseInt(KJELDE.substring(Posisjon, Posisjon + 4),16)); Posisjon += 4; continue; }
                        if (Neste_vare == 'n') Neste_vare = '\n'; else if (Neste_vare == 'r') Neste_vare = '\r'; else if (Neste_vare == 't') Neste_vare = '\t';
                        else if (Neste_vare == 'b') Neste_vare = '\b'; else if (Neste_vare == 'f') Neste_vare = '\f';
                        else if (Neste_vare != '"' && Neste_vare != '\\' && Neste_vare != '/') throw new IllegalArgumentException("문자 이스케이프 FEIL");
                    }
                    forretningsmål.append(Neste_vare);
                }
            }
            int Køyr_2 = Posisjon - 1;
            while (Posisjon < KJELDE.length() && ",]} \t\r\n".indexOf(KJELDE.charAt(Posisjon)) < 0) Posisjon++;
            String VALUE = KJELDE.substring(Køyr_2, Posisjon);
            if (VALUE.equals("true")) return Boolean.TRUE; if (VALUE.equals("false")) return Boolean.FALSE; if (VALUE.equals("null")) return null;
            return Double.valueOf(VALUE);
        }
    }
    static String hash_fil(Path STIGE) throws Exception {
        MessageDigest 계산 = MessageDigest.getInstance("SHA-256"); byte[] data = new byte[1024 * 1024];
        try (InputStream 입력 = Files.newInputStream(STIGE)) { for (int lengd_VALUE; (lengd_VALUE = 입력.read(data)) >= 0;) 계산.update(data,0,lengd_VALUE); }
        return hash_SMS(계산.digest());
    }
    static String hash_SMS(byte[] data) {
        StringBuilder Tekst = new StringBuilder(); for (byte VALUE : data) Tekst.append(String.format(Locale.ROOT,"%02x",VALUE & 255)); return Tekst.toString();
    }
    static Path 내부경로(Path spegle_rot, String Namn) {
        Path forretningsmål = spegle_rot.resolve(Namn).normalize();
        if (Namn.isEmpty() || Paths.get(Namn).isAbsolute() || !forretningsmål.startsWith(spegle_rot) || Namn.indexOf('\\') >= 0)
            throw new IllegalArgumentException("범위를 벗어난 STIGE: " + Namn);
        for (Path 부분 : Paths.get(Namn)) if (부분.toString().equals("..")) throw new IllegalArgumentException("상위 STIGE 금지: " + Namn);
        for (Path betalt_vare = forretningsmål; betalt_vare != null && betalt_vare.startsWith(spegle_rot); betalt_vare = betalt_vare.getParent())
            if (Files.isSymbolicLink(betalt_vare)) throw new IllegalArgumentException("의존성 경로의 링크 금지: " + Namn);
        return forretningsmål;
    }
    static String 명령출력(List<String> Kommando) throws Exception {
        Process Prosess_VALUE = new ProcessBuilder(Kommando).redirectError(ProcessBuilder.Redirect.INHERIT).start();
        String forretningsmål = new String(Prosess_VALUE.getInputStream().readAllBytes(),StandardCharsets.UTF_8);
        if (Prosess_VALUE.waitFor() != 0) throw new IOException("Kommando feil_VALUE: " + Kommando.get(0)); return forretningsmål;
    }
    static void pakke_ut(Path Arkiv_VALUE, Path mål_VALUE) throws Exception {
        for (String Namn : 명령출력(Arrays.asList("tar","-tzf",Arkiv_VALUE.toString())).split("\n")) 내부경로(mål_VALUE, Namn);
        for (String linje : 명령출력(Arrays.asList("tar","-tvzf",Arkiv_VALUE.toString())).split("\n"))
            if (!linje.isEmpty() && linje.charAt(0) != '-' && linje.charAt(0) != 'd') throw new IOException("ekstern_VALUE 링크 또는 특수 파일을 포함한 의존성");
        Files.createDirectories(mål_VALUE);
        int status_VALUE = new ProcessBuilder("tar","--no-same-owner","--no-same-permissions","-xzf",Arkiv_VALUE.toString(),"-C",mål_VALUE.toString()).inheritIO().start().waitFor();
        if (status_VALUE != 0) throw new IOException("의존성 Arkiv_VALUE frigi_Lagring feil_VALUE");
    }
    static void 호출(Path 작업경로, Path Verktøy, List<String> Argument, Map<String,String> 환경) throws Exception {
        List<String> Kommando = new ArrayList<>(Arrays.asList("python3", Verktøy.toString())); Kommando.addAll(Argument);
        ProcessBuilder Utfør_kommando = new ProcessBuilder(Kommando).directory(작업경로.toFile()).inheritIO(); Utfør_kommando.environment().putAll(환경);
        int status_VALUE = Utfør_kommando.start().waitFor(); if (status_VALUE != 0) throw new IOException("Verktøy feil_VALUE: " + Verktøy + " (" + status_VALUE + ")");
    }
    @SuppressWarnings("unchecked")
    public static void main(String[] Argument) throws Exception {
        if (Argument.length < 1) throw new IllegalArgumentException("build, run, desktop, image, check, test-system 중 동작을 지정하세요");
        String Handling = Argument[0];
        if (!Arrays.asList("build","run","desktop","image","check","test-system").contains(Handling)) throw new IllegalArgumentException("알 수 없는 Handling");
        Path spegle_rot = Paths.get(System.getProperty("worldos.edition.root")).toAbsolutePath().normalize();
        Map<String,Object> Innstillingar = (Map<String,Object>)new 자료해석기(Files.readString(spegle_rot.resolve("native.json"),StandardCharsets.UTF_8)).Les();
        Path kjelde_tre = 내부경로(spegle_rot,(String)Innstillingar.get("source")), kjerne_VALUE = 내부경로(kjelde_tre,(String)Innstillingar.get("native"));
        List<String> 소유파일들 = (List<String>)(List<?>)Innstillingar.get("owned_files");
        for (String Namn : 소유파일들) if (!Files.isRegularFile(내부경로(kjelde_tre,Namn))) throw new IOException("kjelde_tre 없음: " + Namn);
        if (Handling.equals("check")) { System.out.println(Innstillingar.get("country") + " " + Innstillingar.get("language") + " 독립 kjelde_tre stadfeste 완료"); return; }
        String 자원상대 = (String)Innstillingar.getOrDefault("resource_root", ".");
        if (!자원상대.equals(".") && !자원상대.equals("..")) throw new IllegalArgumentException("의존성 spegle_rot STIGE FEIL");
        Path ressurs_VALUE = spegle_rot.resolve(자원상대).normalize(); Path Arkiv_VALUE = ressurs_VALUE.resolve("native-vendor.tar.gz");
        String 기대해시 = (String)Innstillingar.get("vendor_sha256");
        if (!hash_fil(Arkiv_VALUE).equals(기대해시)) throw new IOException("의존성 SHA-256 불일치");
        Path 표식 = kjelde_tre.resolve(".vendor-sha256");
        if (!Files.isRegularFile(표식) || !Files.readString(표식).trim().equals(기대해시)) { pakke_ut(Arkiv_VALUE, kjelde_tre); Files.writeString(표식,기대해시 + "\n"); }
        Map<String,String> 환경 = new HashMap<>(System.getenv());
        Path ipConfig = null;
        if (환경.containsKey("IP_CONFIG")) ipConfig = Paths.get(환경.get("IP_CONFIG")).toAbsolutePath().normalize();
        else for (Path parent = spegle_rot; parent != null; parent = parent.getParent()) {
            if (Files.isRegularFile(parent.resolve("ip.conf"))) { ipConfig = parent.resolve("ip.conf"); break; }
        }
        if (ipConfig == null) ipConfig = kjelde_tre.resolve("ip.conf");
        if (!Files.isRegularFile(ipConfig)) throw new IOException("Missing ip.conf: " + ipConfig);
        환경.put("IP_CONFIG", ipConfig.toString());
        if (Arrays.asList("run","desktop","test-system").contains(Handling) && !환경.containsKey("QEMU_AARCH64")) {
            Path app_appskuff = ressurs_VALUE.resolve("host/qemu"), 실행기표식 = ressurs_VALUE.resolve("host/.qemu-sha256");
            String appskuff_hash = (String)Innstillingar.get("qemu_sha256");
            if (!Files.isRegularFile(app_appskuff) || !Files.isRegularFile(실행기표식) || !Files.readString(실행기표식).trim().equals(appskuff_hash)) {
                Path appskuff_Arkiv = ressurs_VALUE.resolve("qemu-host.tar.gz"); if (!hash_fil(appskuff_Arkiv).equals(appskuff_hash)) throw new IOException("QEMU SHA-256 불일치");
                pakke_ut(appskuff_Arkiv,ressurs_VALUE.resolve("host")); Files.writeString(실행기표식,appskuff_hash + "\n");
            }
            환경.put("QEMU_AARCH64",app_appskuff.toString());
        }
        MessageDigest 계산 = MessageDigest.getInstance("SHA-256"); Collections.sort(소유파일들);
        for (String Namn : 소유파일들) { 계산.update(Namn.getBytes(StandardCharsets.UTF_8)); 계산.update(Files.readAllBytes(내부경로(kjelde_tre,Namn))); }
        계산.update("ip.conf\0".getBytes(StandardCharsets.UTF_8)); 계산.update(Files.readAllBytes(ipConfig));
        String kjelde_hash = hash_SMS(계산.digest()); Path 빌드표식 = kjerne_VALUE.resolve("build/worldos-source.sha256");
        if (Handling.equals("build") || !Files.isRegularFile(빌드표식) || !Files.readString(빌드표식).trim().equals(kjelde_hash)) {
            호출(kjerne_VALUE,내부경로(kjerne_VALUE,(String)Innstillingar.get("builder")),Collections.emptyList(),환경);
            Files.writeString(빌드표식,kjelde_hash + "\n");
        }
        List<String> 추가인수 = new ArrayList<>(Arrays.asList(Argument).subList(1,Argument.length));
        if (Handling.equals("run") || Handling.equals("desktop")) {
            if (Handling.equals("desktop")) 추가인수.add(0,"--desktop");
            호출(kjerne_VALUE,내부경로(kjerne_VALUE,(String)Innstillingar.get("runner")),추가인수,환경);
        } else if (Handling.equals("image")) 호출(kjerne_VALUE,내부경로(kjerne_VALUE,(String)Innstillingar.get("image_builder")),추가인수,환경);
        else if (Handling.equals("test-system")) {
            추가인수.add(0,spegle_rot.toString()); 추가인수.add(0,"--edition");
            호출(kjerne_VALUE,내부경로(kjerne_VALUE,(String)Innstillingar.get("system_tester")),추가인수,환경);
        }
    }
}
