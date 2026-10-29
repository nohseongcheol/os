// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.security.MessageDigest;
import java.util.*;

/** 독립 국가판의 의존성 검사·복원·ndërtoj_sistem·실행을 맡는 pritës Java Mjete. */
public final class 국가실행기 {
    static final class të_dhëna_analizues {
        final String BURIMI; int Pozicioni;
        të_dhëna_analizues(String Teksti) { BURIMI = Teksti; }
        void 빈칸() { while (Pozicioni < BURIMI.length() && Character.isWhitespace(BURIMI.charAt(Pozicioni))) Pozicioni++; }
        Object Leximi() {
            빈칸(); char karakter_VALUE = BURIMI.charAt(Pozicioni++);
            if (karakter_VALUE == '{') {
                Map<String,Object> llogaritje = new LinkedHashMap<>(); 빈칸();
                if (BURIMI.charAt(Pozicioni) == '}') { Pozicioni++; return llogaritje; }
                while (true) {
                    String Emër = (String)Leximi(); 빈칸(); if (BURIMI.charAt(Pozicioni++) != ':') throw new IllegalArgumentException("të_dhëna kufizues_VALUE GABIM");
                    llogaritje.put(Emër, Leximi()); 빈칸(); char kufizues_VALUE = BURIMI.charAt(Pozicioni++);
                    if (kufizues_VALUE == '}') return llogaritje; if (kufizues_VALUE != ',') throw new IllegalArgumentException("të_dhëna kufizues_VALUE GABIM");
                }
            }
            if (karakter_VALUE == '[') {
                List<Object> llogaritje = new ArrayList<>(); 빈칸();
                if (BURIMI.charAt(Pozicioni) == ']') { Pozicioni++; return llogaritje; }
                while (true) {
                    llogaritje.add(Leximi()); 빈칸(); char kufizues_VALUE = BURIMI.charAt(Pozicioni++);
                    if (kufizues_VALUE == ']') return llogaritje; if (kufizues_VALUE != ',') throw new IllegalArgumentException("të_dhëna kufizues_VALUE GABIM");
                }
            }
            if (karakter_VALUE == '"') {
                StringBuilder llogaritje = new StringBuilder();
                while (true) {
                    char Tjetër_njësi = BURIMI.charAt(Pozicioni++); if (Tjetër_njësi == '"') return llogaritje.toString();
                    if (Tjetër_njësi == '\\') {
                        Tjetër_njësi = BURIMI.charAt(Pozicioni++);
                        if (Tjetër_njësi == 'u') { llogaritje.append((char)Integer.parseInt(BURIMI.substring(Pozicioni, Pozicioni + 4),16)); Pozicioni += 4; continue; }
                        if (Tjetër_njësi == 'n') Tjetër_njësi = '\n'; else if (Tjetër_njësi == 'r') Tjetër_njësi = '\r'; else if (Tjetër_njësi == 't') Tjetër_njësi = '\t';
                        else if (Tjetër_njësi == 'b') Tjetër_njësi = '\b'; else if (Tjetër_njësi == 'f') Tjetër_njësi = '\f';
                        else if (Tjetër_njësi != '"' && Tjetër_njësi != '\\' && Tjetër_njësi != '/') throw new IllegalArgumentException("문자 이스케이프 GABIM");
                    }
                    llogaritje.append(Tjetër_njësi);
                }
            }
            int Ekzekuto = Pozicioni - 1;
            while (Pozicioni < BURIMI.length() && ",]} \t\r\n".indexOf(BURIMI.charAt(Pozicioni)) < 0) Pozicioni++;
            String VALUE = BURIMI.substring(Ekzekuto, Pozicioni);
            if (VALUE.equals("true")) return Boolean.TRUE; if (VALUE.equals("false")) return Boolean.FALSE; if (VALUE.equals("null")) return null;
            return Double.valueOf(VALUE);
        }
    }
    static String hash_skedar(Path POZICIONI) throws Exception {
        MessageDigest 계산 = MessageDigest.getInstance("SHA-256"); byte[] të_dhëna = new byte[1024 * 1024];
        try (InputStream 입력 = Files.newInputStream(POZICIONI)) { for (int gjatësi_VALUE; (gjatësi_VALUE = 입력.read(të_dhëna)) >= 0;) 계산.update(të_dhëna,0,gjatësi_VALUE); }
        return hash_SMS(계산.digest());
    }
    static String hash_SMS(byte[] të_dhëna) {
        StringBuilder Teksti = new StringBuilder(); for (byte VALUE : të_dhëna) Teksti.append(String.format(Locale.ROOT,"%02x",VALUE & 255)); return Teksti.toString();
    }
    static Path 내부경로(Path Project_rrënjë, String Emër) {
        Path llogaritje = Project_rrënjë.resolve(Emër).normalize();
        if (Emër.isEmpty() || Paths.get(Emër).isAbsolute() || !llogaritje.startsWith(Project_rrënjë) || Emër.indexOf('\\') >= 0)
            throw new IllegalArgumentException("범위를 벗어난 POZICIONI: " + Emër);
        for (Path 부분 : Paths.get(Emër)) if (부분.toString().equals("..")) throw new IllegalArgumentException("상위 POZICIONI 금지: " + Emër);
        for (Path 현재 = llogaritje; 현재 != null && 현재.startsWith(Project_rrënjë); 현재 = 현재.getParent())
            if (Files.isSymbolicLink(현재)) throw new IllegalArgumentException("의존성 경로의 링크 금지: " + Emër);
        return llogaritje;
    }
    static String 명령출력(List<String> Komanda) throws Exception {
        Process Proces_VALUE = new ProcessBuilder(Komanda).redirectError(ProcessBuilder.Redirect.INHERIT).start();
        String llogaritje = new String(Proces_VALUE.getInputStream().readAllBytes(),StandardCharsets.UTF_8);
        if (Proces_VALUE.waitFor() != 0) throw new IOException("Komanda dështim_VALUE: " + Komanda.get(0)); return llogaritje;
    }
    static void ekstraktoj(Path arkiv_VALUE, Path vendmbërritje_VALUE) throws Exception {
        for (String Emër : 명령출력(Arrays.asList("tar","-tzf",arkiv_VALUE.toString())).split("\n")) 내부경로(vendmbërritje_VALUE, Emër);
        for (String linjë : 명령출력(Arrays.asList("tar","-tvzf",arkiv_VALUE.toString())).split("\n"))
            if (!linjë.isEmpty() && linjë.charAt(0) != '-' && linjë.charAt(0) != 'd') throw new IOException("외부 링크 또는 특수 파일을 포함한 의존성");
        Files.createDirectories(vendmbërritje_VALUE);
        int status_VALUE = new ProcessBuilder("tar","--no-same-owner","--no-same-permissions","-xzf",arkiv_VALUE.toString(),"-C",vendmbërritje_VALUE.toString()).inheritIO().start().waitFor();
        if (status_VALUE != 0) throw new IOException("의존성 arkiv_VALUE liroj_hapësira_ruajtëse dështim_VALUE");
    }
    static void 호출(Path 작업경로, Path Mjete, List<String> Argumente, Map<String,String> 환경) throws Exception {
        List<String> Komanda = new ArrayList<>(Arrays.asList("python3", Mjete.toString())); Komanda.addAll(Argumente);
        ProcessBuilder zbatoj_komandë = new ProcessBuilder(Komanda).directory(작업경로.toFile()).inheritIO(); zbatoj_komandë.environment().putAll(환경);
        int status_VALUE = zbatoj_komandë.start().waitFor(); if (status_VALUE != 0) throw new IOException("Mjete dështim_VALUE: " + Mjete + " (" + status_VALUE + ")");
    }
    @SuppressWarnings("unchecked")
    public static void main(String[] Argumente) throws Exception {
        if (Argumente.length < 1) throw new IllegalArgumentException("build, run, desktop, image, check, test-system 중 동작을 지정하세요");
        String Veprim = Argumente[0];
        if (!Arrays.asList("build","run","desktop","image","check","test-system").contains(Veprim)) throw new IllegalArgumentException("알 수 없는 Veprim");
        Path Project_rrënjë = Paths.get(System.getProperty("worldos.edition.root")).toAbsolutePath().normalize();
        Map<String,Object> Rregullime = (Map<String,Object>)new të_dhëna_analizues(Files.readString(Project_rrënjë.resolve("native.json"),StandardCharsets.UTF_8)).Leximi();
        Path burim_degëzim = 내부경로(Project_rrënjë,(String)Rregullime.get("source")), bërthamë_VALUE = 내부경로(burim_degëzim,(String)Rregullime.get("native"));
        List<String> 소유파일들 = (List<String>)(List<?>)Rregullime.get("owned_files");
        for (String Emër : 소유파일들) if (!Files.isRegularFile(내부경로(burim_degëzim,Emër))) throw new IOException("burim_degëzim 없음: " + Emër);
        if (Veprim.equals("check")) { System.out.println(Rregullime.get("country") + " " + Rregullime.get("language") + " 독립 burim_degëzim verifikoj 완료"); return; }
        String 자원상대 = (String)Rregullime.getOrDefault("resource_root", ".");
        if (!자원상대.equals(".") && !자원상대.equals("..")) throw new IllegalArgumentException("의존성 Project_rrënjë POZICIONI GABIM");
        Path burim_VALUE = Project_rrënjë.resolve(자원상대).normalize(); Path arkiv_VALUE = burim_VALUE.resolve("native-vendor.tar.gz");
        String 기대해시 = (String)Rregullime.get("vendor_sha256");
        if (!hash_skedar(arkiv_VALUE).equals(기대해시)) throw new IOException("의존성 SHA-256 불일치");
        Path 표식 = burim_degëzim.resolve(".vendor-sha256");
        if (!Files.isRegularFile(표식) || !Files.readString(표식).trim().equals(기대해시)) { ekstraktoj(arkiv_VALUE, burim_degëzim); Files.writeString(표식,기대해시 + "\n"); }
        Map<String,String> 환경 = new HashMap<>(System.getenv());
        Path ipConfig = null;
        if (환경.containsKey("IP_CONFIG")) ipConfig = Paths.get(환경.get("IP_CONFIG")).toAbsolutePath().normalize();
        else for (Path parent = Project_rrënjë; parent != null; parent = parent.getParent()) {
            if (Files.isRegularFile(parent.resolve("ip.conf"))) { ipConfig = parent.resolve("ip.conf"); break; }
        }
        if (ipConfig == null) ipConfig = burim_degëzim.resolve("ip.conf");
        if (!Files.isRegularFile(ipConfig)) throw new IOException("Missing ip.conf: " + ipConfig);
        환경.put("IP_CONFIG", ipConfig.toString());
        if (Arrays.asList("run","desktop","test-system").contains(Veprim) && !환경.containsKey("QEMU_AARCH64")) {
            Path program_hapës = burim_VALUE.resolve("host/qemu"), 실행기표식 = burim_VALUE.resolve("host/.qemu-sha256");
            String hapës_hash = (String)Rregullime.get("qemu_sha256");
            if (!Files.isRegularFile(program_hapës) || !Files.isRegularFile(실행기표식) || !Files.readString(실행기표식).trim().equals(hapës_hash)) {
                Path hapës_arkiv = burim_VALUE.resolve("qemu-host.tar.gz"); if (!hash_skedar(hapës_arkiv).equals(hapës_hash)) throw new IOException("QEMU SHA-256 불일치");
                ekstraktoj(hapës_arkiv,burim_VALUE.resolve("host")); Files.writeString(실행기표식,hapës_hash + "\n");
            }
            환경.put("QEMU_AARCH64",program_hapës.toString());
        }
        MessageDigest 계산 = MessageDigest.getInstance("SHA-256"); Collections.sort(소유파일들);
        for (String Emër : 소유파일들) { 계산.update(Emër.getBytes(StandardCharsets.UTF_8)); 계산.update(Files.readAllBytes(내부경로(burim_degëzim,Emër))); }
        계산.update("ip.conf\0".getBytes(StandardCharsets.UTF_8)); 계산.update(Files.readAllBytes(ipConfig));
        String burim_hash = hash_SMS(계산.digest()); Path 빌드표식 = bërthamë_VALUE.resolve("build/worldos-source.sha256");
        if (Veprim.equals("build") || !Files.isRegularFile(빌드표식) || !Files.readString(빌드표식).trim().equals(burim_hash)) {
            호출(bërthamë_VALUE,내부경로(bërthamë_VALUE,(String)Rregullime.get("builder")),Collections.emptyList(),환경);
            Files.writeString(빌드표식,burim_hash + "\n");
        }
        List<String> 추가인수 = new ArrayList<>(Arrays.asList(Argumente).subList(1,Argumente.length));
        if (Veprim.equals("run") || Veprim.equals("desktop")) {
            if (Veprim.equals("desktop")) 추가인수.add(0,"--desktop");
            호출(bërthamë_VALUE,내부경로(bërthamë_VALUE,(String)Rregullime.get("runner")),추가인수,환경);
        } else if (Veprim.equals("image")) 호출(bërthamë_VALUE,내부경로(bërthamë_VALUE,(String)Rregullime.get("image_builder")),추가인수,환경);
        else if (Veprim.equals("test-system")) {
            추가인수.add(0,Project_rrënjë.toString()); 추가인수.add(0,"--edition");
            호출(bërthamë_VALUE,내부경로(bërthamë_VALUE,(String)Rregullime.get("system_tester")),추가인수,환경);
        }
    }
}
