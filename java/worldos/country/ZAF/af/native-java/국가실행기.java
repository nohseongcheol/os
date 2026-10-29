// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.security.MessageDigest;
import java.util.*;

/** 독립 국가판의 의존성 검사·복원·bou_stelsel·실행을 맡는 hou Java Nutsmiddels. */
public final class 국가실행기 {
    static final class data_ontleder {
        final String Bron; int Posisie;
        data_ontleder(String Teks) { Bron = Teks; }
        void 빈칸() { while (Posisie < Bron.length() && Character.isWhitespace(Bron.charAt(Posisie))) Posisie++; }
        Object Lees() {
            빈칸(); char karakter_VALUE = Bron.charAt(Posisie++);
            if (karakter_VALUE == '{') {
                Map<String,Object> maatreël = new LinkedHashMap<>(); 빈칸();
                if (Bron.charAt(Posisie) == '}') { Posisie++; return maatreël; }
                while (true) {
                    String Naam = (String)Lees(); 빈칸(); if (Bron.charAt(Posisie++) != ':') throw new IllegalArgumentException("data skeier_VALUE Fout");
                    maatreël.put(Naam, Lees()); 빈칸(); char skeier_VALUE = Bron.charAt(Posisie++);
                    if (skeier_VALUE == '}') return maatreël; if (skeier_VALUE != ',') throw new IllegalArgumentException("data skeier_VALUE Fout");
                }
            }
            if (karakter_VALUE == '[') {
                List<Object> maatreël = new ArrayList<>(); 빈칸();
                if (Bron.charAt(Posisie) == ']') { Posisie++; return maatreël; }
                while (true) {
                    maatreël.add(Lees()); 빈칸(); char skeier_VALUE = Bron.charAt(Posisie++);
                    if (skeier_VALUE == ']') return maatreël; if (skeier_VALUE != ',') throw new IllegalArgumentException("data skeier_VALUE Fout");
                }
            }
            if (karakter_VALUE == '"') {
                StringBuilder maatreël = new StringBuilder();
                while (true) {
                    char Volgende_item = Bron.charAt(Posisie++); if (Volgende_item == '"') return maatreël.toString();
                    if (Volgende_item == '\\') {
                        Volgende_item = Bron.charAt(Posisie++);
                        if (Volgende_item == 'u') { maatreël.append((char)Integer.parseInt(Bron.substring(Posisie, Posisie + 4),16)); Posisie += 4; continue; }
                        if (Volgende_item == 'n') Volgende_item = '\n'; else if (Volgende_item == 'r') Volgende_item = '\r'; else if (Volgende_item == 't') Volgende_item = '\t';
                        else if (Volgende_item == 'b') Volgende_item = '\b'; else if (Volgende_item == 'f') Volgende_item = '\f';
                        else if (Volgende_item != '"' && Volgende_item != '\\' && Volgende_item != '/') throw new IllegalArgumentException("문자 이스케이프 Fout");
                    }
                    maatreël.append(Volgende_item);
                }
            }
            int Loop = Posisie - 1;
            while (Posisie < Bron.length() && ",]} \t\r\n".indexOf(Bron.charAt(Posisie)) < 0) Posisie++;
            String VALUE = Bron.substring(Loop, Posisie);
            if (VALUE.equals("true")) return Boolean.TRUE; if (VALUE.equals("false")) return Boolean.FALSE; if (VALUE.equals("null")) return null;
            return Double.valueOf(VALUE);
        }
    }
    static String huts_lêer(Path Pad) throws Exception {
        MessageDigest 계산 = MessageDigest.getInstance("SHA-256"); byte[] data = new byte[1024 * 1024];
        try (InputStream 입력 = Files.newInputStream(Pad)) { for (int lengte_VALUE; (lengte_VALUE = 입력.read(data)) >= 0;) 계산.update(data,0,lengte_VALUE); }
        return huts_SMS(계산.digest());
    }
    static String huts_SMS(byte[] data) {
        StringBuilder Teks = new StringBuilder(); for (byte VALUE : data) Teks.append(String.format(Locale.ROOT,"%02x",VALUE & 255)); return Teks.toString();
    }
    static Path 내부경로(Path Project_wortel, String Naam) {
        Path maatreël = Project_wortel.resolve(Naam).normalize();
        if (Naam.isEmpty() || Paths.get(Naam).isAbsolute() || !maatreël.startsWith(Project_wortel) || Naam.indexOf('\\') >= 0)
            throw new IllegalArgumentException("범위를 벗어난 Pad: " + Naam);
        for (Path 부분 : Paths.get(Naam)) if (부분.toString().equals("..")) throw new IllegalArgumentException("상위 Pad 금지: " + Naam);
        for (Path 현재 = maatreël; 현재 != null && 현재.startsWith(Project_wortel); 현재 = 현재.getParent())
            if (Files.isSymbolicLink(현재)) throw new IllegalArgumentException("의존성 경로의 링크 금지: " + Naam);
        return maatreël;
    }
    static String 명령출력(List<String> Opdrag) throws Exception {
        Process Proses_VALUE = new ProcessBuilder(Opdrag).redirectError(ProcessBuilder.Redirect.INHERIT).start();
        String maatreël = new String(Proses_VALUE.getInputStream().readAllBytes(),StandardCharsets.UTF_8);
        if (Proses_VALUE.waitFor() != 0) throw new IOException("Opdrag faling_VALUE: " + Opdrag.get(0)); return maatreël;
    }
    static void ekstraheer(Path Argief_VALUE, Path bestemming_VALUE) throws Exception {
        for (String Naam : 명령출력(Arrays.asList("tar","-tzf",Argief_VALUE.toString())).split("\n")) 내부경로(bestemming_VALUE, Naam);
        for (String lyn : 명령출력(Arrays.asList("tar","-tvzf",Argief_VALUE.toString())).split("\n"))
            if (!lyn.isEmpty() && lyn.charAt(0) != '-' && lyn.charAt(0) != 'd') throw new IOException("외부 링크 또는 특수 파일을 포함한 의존성");
        Files.createDirectories(bestemming_VALUE);
        int stand_VALUE = new ProcessBuilder("tar","--no-same-owner","--no-same-permissions","-xzf",Argief_VALUE.toString(),"-C",bestemming_VALUE.toString()).inheritIO().start().waitFor();
        if (stand_VALUE != 0) throw new IOException("의존성 Argief_VALUE stel_vry_Berging faling_VALUE");
    }
    static void 호출(Path 작업경로, Path Nutsmiddels, List<String> 인수, Map<String,String> 환경) throws Exception {
        List<String> Opdrag = new ArrayList<>(Arrays.asList("python3", Nutsmiddels.toString())); Opdrag.addAll(인수);
        ProcessBuilder uitvoer_bevel = new ProcessBuilder(Opdrag).directory(작업경로.toFile()).inheritIO(); uitvoer_bevel.environment().putAll(환경);
        int stand_VALUE = uitvoer_bevel.start().waitFor(); if (stand_VALUE != 0) throw new IOException("Nutsmiddels faling_VALUE: " + Nutsmiddels + " (" + stand_VALUE + ")");
    }
    @SuppressWarnings("unchecked")
    public static void main(String[] 인수) throws Exception {
        if (인수.length < 1) throw new IllegalArgumentException("build, run, desktop, image, check, test-system 중 동작을 지정하세요");
        String Aksie = 인수[0];
        if (!Arrays.asList("build","run","desktop","image","check","test-system").contains(Aksie)) throw new IllegalArgumentException("알 수 없는 Aksie");
        Path Project_wortel = Paths.get(System.getProperty("worldos.edition.root")).toAbsolutePath().normalize();
        Map<String,Object> Instellings = (Map<String,Object>)new data_ontleder(Files.readString(Project_wortel.resolve("native.json"),StandardCharsets.UTF_8)).Lees();
        Path bron_boom = 내부경로(Project_wortel,(String)Instellings.get("source")), kern_VALUE = 내부경로(bron_boom,(String)Instellings.get("native"));
        List<String> 소유파일들 = (List<String>)(List<?>)Instellings.get("owned_files");
        for (String Naam : 소유파일들) if (!Files.isRegularFile(내부경로(bron_boom,Naam))) throw new IOException("bron_boom 없음: " + Naam);
        if (Aksie.equals("check")) { System.out.println(Instellings.get("country") + " " + Instellings.get("language") + " 독립 bron_boom verifieer 완료"); return; }
        String 자원상대 = (String)Instellings.getOrDefault("resource_root", ".");
        if (!자원상대.equals(".") && !자원상대.equals("..")) throw new IllegalArgumentException("의존성 Project_wortel Pad Fout");
        Path hulpbron_VALUE = Project_wortel.resolve(자원상대).normalize(); Path Argief_VALUE = hulpbron_VALUE.resolve("native-vendor.tar.gz");
        String 기대해시 = (String)Instellings.get("vendor_sha256");
        if (!huts_lêer(Argief_VALUE).equals(기대해시)) throw new IOException("의존성 SHA-256 불일치");
        Path 표식 = bron_boom.resolve(".vendor-sha256");
        if (!Files.isRegularFile(표식) || !Files.readString(표식).trim().equals(기대해시)) { ekstraheer(Argief_VALUE, bron_boom); Files.writeString(표식,기대해시 + "\n"); }
        Map<String,String> 환경 = new HashMap<>(System.getenv());
        Path ipConfig = null;
        if (환경.containsKey("IP_CONFIG")) ipConfig = Paths.get(환경.get("IP_CONFIG")).toAbsolutePath().normalize();
        else for (Path parent = Project_wortel; parent != null; parent = parent.getParent()) {
            if (Files.isRegularFile(parent.resolve("ip.conf"))) { ipConfig = parent.resolve("ip.conf"); break; }
        }
        if (ipConfig == null) ipConfig = bron_boom.resolve("ip.conf");
        if (!Files.isRegularFile(ipConfig)) throw new IOException("Missing ip.conf: " + ipConfig);
        환경.put("IP_CONFIG", ipConfig.toString());
        if (Arrays.asList("run","desktop","test-system").contains(Aksie) && !환경.containsKey("QEMU_AARCH64")) {
            Path program_oopmaker = hulpbron_VALUE.resolve("host/qemu"), 실행기표식 = hulpbron_VALUE.resolve("host/.qemu-sha256");
            String oopmaker_huts = (String)Instellings.get("qemu_sha256");
            if (!Files.isRegularFile(program_oopmaker) || !Files.isRegularFile(실행기표식) || !Files.readString(실행기표식).trim().equals(oopmaker_huts)) {
                Path oopmaker_Argief = hulpbron_VALUE.resolve("qemu-host.tar.gz"); if (!huts_lêer(oopmaker_Argief).equals(oopmaker_huts)) throw new IOException("QEMU SHA-256 불일치");
                ekstraheer(oopmaker_Argief,hulpbron_VALUE.resolve("host")); Files.writeString(실행기표식,oopmaker_huts + "\n");
            }
            환경.put("QEMU_AARCH64",program_oopmaker.toString());
        }
        MessageDigest 계산 = MessageDigest.getInstance("SHA-256"); Collections.sort(소유파일들);
        for (String Naam : 소유파일들) { 계산.update(Naam.getBytes(StandardCharsets.UTF_8)); 계산.update(Files.readAllBytes(내부경로(bron_boom,Naam))); }
        계산.update("ip.conf\0".getBytes(StandardCharsets.UTF_8)); 계산.update(Files.readAllBytes(ipConfig));
        String bron_huts = huts_SMS(계산.digest()); Path 빌드표식 = kern_VALUE.resolve("build/worldos-source.sha256");
        if (Aksie.equals("build") || !Files.isRegularFile(빌드표식) || !Files.readString(빌드표식).trim().equals(bron_huts)) {
            호출(kern_VALUE,내부경로(kern_VALUE,(String)Instellings.get("builder")),Collections.emptyList(),환경);
            Files.writeString(빌드표식,bron_huts + "\n");
        }
        List<String> 추가인수 = new ArrayList<>(Arrays.asList(인수).subList(1,인수.length));
        if (Aksie.equals("run") || Aksie.equals("desktop")) {
            if (Aksie.equals("desktop")) 추가인수.add(0,"--desktop");
            호출(kern_VALUE,내부경로(kern_VALUE,(String)Instellings.get("runner")),추가인수,환경);
        } else if (Aksie.equals("image")) 호출(kern_VALUE,내부경로(kern_VALUE,(String)Instellings.get("image_builder")),추가인수,환경);
        else if (Aksie.equals("test-system")) {
            추가인수.add(0,Project_wortel.toString()); 추가인수.add(0,"--edition");
            호출(kern_VALUE,내부경로(kern_VALUE,(String)Instellings.get("system_tester")),추가인수,환경);
        }
    }
}
