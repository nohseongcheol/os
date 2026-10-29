// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.security.MessageDigest;
import java.util.*;

/** 독립 국가판의 의존성 검사·복원·version_System·실행을 맡는 värd Java verktyg. */
public final class Country_Startbild {
    static final class data_parser {
        final String källfil; int position;
        data_parser(String text) { källfil = text; }
        void 빈칸() { while (position < källfil.length() && Character.isWhitespace(källfil.charAt(position))) position++; }
        Object Läs() {
            빈칸(); char tecken_värde = källfil.charAt(position++);
            if (tecken_värde == '{') {
                Map<String,Object> RESULTAT = new LinkedHashMap<>(); 빈칸();
                if (källfil.charAt(position) == '}') { position++; return RESULTAT; }
                while (true) {
                    String Namn = (String)Läs(); 빈칸(); if (källfil.charAt(position++) != ':') throw new IllegalArgumentException("data avgränsare_värde_d8ba4873 fel");
                    RESULTAT.put(Namn, Läs()); 빈칸(); char avgränsare_värde_d8ba4873 = källfil.charAt(position++);
                    if (avgränsare_värde_d8ba4873 == '}') return RESULTAT; if (avgränsare_värde_d8ba4873 != ',') throw new IllegalArgumentException("data avgränsare_värde_d8ba4873 fel");
                }
            }
            if (tecken_värde == '[') {
                List<Object> RESULTAT = new ArrayList<>(); 빈칸();
                if (källfil.charAt(position) == ']') { position++; return RESULTAT; }
                while (true) {
                    RESULTAT.add(Läs()); 빈칸(); char avgränsare_värde_d8ba4873 = källfil.charAt(position++);
                    if (avgränsare_värde_d8ba4873 == ']') return RESULTAT; if (avgränsare_värde_d8ba4873 != ',') throw new IllegalArgumentException("data avgränsare_värde_d8ba4873 fel");
                }
            }
            if (tecken_värde == '"') {
                StringBuilder RESULTAT = new StringBuilder();
                while (true) {
                    char Nästa_objekt = källfil.charAt(position++); if (Nästa_objekt == '"') return RESULTAT.toString();
                    if (Nästa_objekt == '\\') {
                        Nästa_objekt = källfil.charAt(position++);
                        if (Nästa_objekt == 'u') { RESULTAT.append((char)Integer.parseInt(källfil.substring(position, position + 4),16)); position += 4; continue; }
                        if (Nästa_objekt == 'n') Nästa_objekt = '\n'; else if (Nästa_objekt == 'r') Nästa_objekt = '\r'; else if (Nästa_objekt == 't') Nästa_objekt = '\t';
                        else if (Nästa_objekt == 'b') Nästa_objekt = '\b'; else if (Nästa_objekt == 'f') Nästa_objekt = '\f';
                        else if (Nästa_objekt != '"' && Nästa_objekt != '\\' && Nästa_objekt != '/') throw new IllegalArgumentException("문자 이스케이프 fel");
                    }
                    RESULTAT.append(Nästa_objekt);
                }
            }
            int Kör = position - 1;
            while (position < källfil.length() && ",]} \t\r\n".indexOf(källfil.charAt(position)) < 0) position++;
            String värde = källfil.substring(Kör, position);
            if (värde.equals("true")) return Boolean.TRUE; if (värde.equals("false")) return Boolean.FALSE; if (värde.equals("null")) return null;
            return Double.valueOf(värde);
        }
    }
    static String hash_fil(Path sökväg_2) throws Exception {
        MessageDigest 계산 = MessageDigest.getInstance("SHA-256"); byte[] data = new byte[1024 * 1024];
        try (InputStream indata_värde = Files.newInputStream(sökväg_2)) { for (int längd_värde; (längd_värde = indata_värde.read(data)) >= 0;) 계산.update(data,0,längd_värde); }
        return hash_SMS(계산.digest());
    }
    static String hash_SMS(byte[] data) {
        StringBuilder text = new StringBuilder(); for (byte värde : data) text.append(String.format(Locale.ROOT,"%02x",värde & 255)); return text.toString();
    }
    static Path intern_väg(Path åtgärd_rot, String Namn) {
        Path RESULTAT = åtgärd_rot.resolve(Namn).normalize();
        if (Namn.isEmpty() || Paths.get(Namn).isAbsolute() || !RESULTAT.startsWith(åtgärd_rot) || Namn.indexOf('\\') >= 0)
            throw new IllegalArgumentException("범위를 벗어난 sökväg_2: " + Namn);
        for (Path 부분 : Paths.get(Namn)) if (부분.toString().equals("..")) throw new IllegalArgumentException("상위 sökväg_2 금지: " + Namn);
        for (Path aktuellt_objekt = RESULTAT; aktuellt_objekt != null && aktuellt_objekt.startsWith(åtgärd_rot); aktuellt_objekt = aktuellt_objekt.getParent())
            if (Files.isSymbolicLink(aktuellt_objekt)) throw new IllegalArgumentException("의존성 경로의 링크 금지: " + Namn);
        return RESULTAT;
    }
    static String kommando_utleverans(List<String> kommando) throws Exception {
        Process Process_värde = new ProcessBuilder(kommando).redirectError(ProcessBuilder.Redirect.INHERIT).start();
        String RESULTAT = new String(Process_värde.getInputStream().readAllBytes(),StandardCharsets.UTF_8);
        if (Process_värde.waitFor() != 0) throw new IOException("kommando fel_värde: " + kommando.get(0)); return RESULTAT;
    }
    static void extrahera(Path Arkiv_värde, Path mål_värde) throws Exception {
        for (String Namn : kommando_utleverans(Arrays.asList("tar","-tzf",Arkiv_värde.toString())).split("\n")) intern_väg(mål_värde, Namn);
        for (String inmatningsrad : kommando_utleverans(Arrays.asList("tar","-tvzf",Arkiv_värde.toString())).split("\n"))
            if (!inmatningsrad.isEmpty() && inmatningsrad.charAt(0) != '-' && inmatningsrad.charAt(0) != 'd') throw new IOException("extern_värde 링크 또는 특수 파일을 포함한 의존성");
        Files.createDirectories(mål_värde);
        int status_värde = new ProcessBuilder("tar","--no-same-owner","--no-same-permissions","-xzf",Arkiv_värde.toString(),"-C",mål_värde.toString()).inheritIO().start().waitFor();
        if (status_värde != 0) throw new IOException("의존성 Arkiv_värde släppa_minne fel_värde");
    }
    static void 호출(Path 작업경로, Path verktyg, List<String> argument, Map<String,String> miljö) throws Exception {
        List<String> kommando = new ArrayList<>(Arrays.asList("python3", verktyg.toString())); kommando.addAll(argument);
        ProcessBuilder köra_kommando = new ProcessBuilder(kommando).directory(작업경로.toFile()).inheritIO(); köra_kommando.environment().putAll(miljö);
        int status_värde = köra_kommando.start().waitFor(); if (status_värde != 0) throw new IOException("verktyg fel_värde: " + verktyg + " (" + status_värde + ")");
    }
    @SuppressWarnings("unchecked")
    public static void main(String[] argument) throws Exception {
        if (argument.length < 1) throw new IllegalArgumentException("build, run, desktop, image, check, test-system 중 동작을 지정하세요");
        String Åtgärd = argument[0];
        if (!Arrays.asList("build","run","desktop","image","check","test-system").contains(Åtgärd)) throw new IllegalArgumentException("알 nummer 없는 Åtgärd");
        Path åtgärd_rot = Paths.get(System.getProperty("worldos.edition.root")).toAbsolutePath().normalize();
        Map<String,Object> Inställningar = (Map<String,Object>)new data_parser(Files.readString(åtgärd_rot.resolve("native.json"),StandardCharsets.UTF_8)).Läs();
        Path källa_träd = intern_väg(åtgärd_rot,(String)Inställningar.get("source")), kärna_värde = intern_väg(källa_träd,(String)Inställningar.get("native"));
        List<String> 소유파일들 = (List<String>)(List<?>)Inställningar.get("owned_files");
        for (String Namn : 소유파일들) if (!Files.isRegularFile(intern_väg(källa_träd,Namn))) throw new IOException("källa_träd 없음: " + Namn);
        if (Åtgärd.equals("check")) { System.out.println(Inställningar.get("country") + " " + Inställningar.get("language") + " 독립 källa_träd verifiera 완료"); return; }
        String resurs_relativ_sökväg = (String)Inställningar.getOrDefault("resource_root", ".");
        if (!resurs_relativ_sökväg.equals(".") && !resurs_relativ_sökväg.equals("..")) throw new IllegalArgumentException("의존성 åtgärd_rot sökväg_2 fel");
        Path resurs_värde = åtgärd_rot.resolve(resurs_relativ_sökväg).normalize(); Path Arkiv_värde = resurs_värde.resolve("native-vendor.tar.gz");
        String 기대해시 = (String)Inställningar.get("vendor_sha256");
        if (!hash_fil(Arkiv_värde).equals(기대해시)) throw new IOException("의존성 SHA-256 불일치");
        Path markör_värde = källa_träd.resolve(".vendor-sha256");
        if (!Files.isRegularFile(markör_värde) || !Files.readString(markör_värde).trim().equals(기대해시)) { extrahera(Arkiv_värde, källa_träd); Files.writeString(markör_värde,기대해시 + "\n"); }
        Map<String,String> miljö = new HashMap<>(System.getenv());
        Path ipConfig = null;
        if (miljö.containsKey("IP_CONFIG")) ipConfig = Paths.get(miljö.get("IP_CONFIG")).toAbsolutePath().normalize();
        else for (Path parent = åtgärd_rot; parent != null; parent = parent.getParent()) {
            if (Files.isRegularFile(parent.resolve("ip.conf"))) { ipConfig = parent.resolve("ip.conf"); break; }
        }
        if (ipConfig == null) ipConfig = källa_träd.resolve("ip.conf");
        if (!Files.isRegularFile(ipConfig)) throw new IOException("Missing ip.conf: " + ipConfig);
        miljö.put("IP_CONFIG", ipConfig.toString());
        if (Arrays.asList("run","desktop","test-system").contains(Åtgärd) && !miljö.containsKey("QEMU_AARCH64")) {
            Path app_Startbild = resurs_värde.resolve("host/qemu"), Startbild_markör = resurs_värde.resolve("host/.qemu-sha256");
            String Startbild_hash = (String)Inställningar.get("qemu_sha256");
            if (!Files.isRegularFile(app_Startbild) || !Files.isRegularFile(Startbild_markör) || !Files.readString(Startbild_markör).trim().equals(Startbild_hash)) {
                Path Startbild_Arkiv = resurs_värde.resolve("qemu-host.tar.gz"); if (!hash_fil(Startbild_Arkiv).equals(Startbild_hash)) throw new IOException("QEMU SHA-256 불일치");
                extrahera(Startbild_Arkiv,resurs_värde.resolve("host")); Files.writeString(Startbild_markör,Startbild_hash + "\n");
            }
            miljö.put("QEMU_AARCH64",app_Startbild.toString());
        }
        MessageDigest 계산 = MessageDigest.getInstance("SHA-256"); Collections.sort(소유파일들);
        for (String Namn : 소유파일들) { 계산.update(Namn.getBytes(StandardCharsets.UTF_8)); 계산.update(Files.readAllBytes(intern_väg(källa_träd,Namn))); }
        계산.update("ip.conf\0".getBytes(StandardCharsets.UTF_8)); 계산.update(Files.readAllBytes(ipConfig));
        String källa_hash = hash_SMS(계산.digest()); Path version_markör = kärna_värde.resolve("build/worldos-source.sha256");
        if (Åtgärd.equals("build") || !Files.isRegularFile(version_markör) || !Files.readString(version_markör).trim().equals(källa_hash)) {
            호출(kärna_värde,intern_väg(kärna_värde,(String)Inställningar.get("builder")),Collections.emptyList(),miljö);
            Files.writeString(version_markör,källa_hash + "\n");
        }
        List<String> 추가인수 = new ArrayList<>(Arrays.asList(argument).subList(1,argument.length));
        if (Åtgärd.equals("run") || Åtgärd.equals("desktop")) {
            if (Åtgärd.equals("desktop")) 추가인수.add(0,"--desktop");
            호출(kärna_värde,intern_väg(kärna_värde,(String)Inställningar.get("runner")),추가인수,miljö);
        } else if (Åtgärd.equals("image")) 호출(kärna_värde,intern_väg(kärna_värde,(String)Inställningar.get("image_builder")),추가인수,miljö);
        else if (Åtgärd.equals("test-system")) {
            추가인수.add(0,åtgärd_rot.toString()); 추가인수.add(0,"--edition");
            호출(kärna_värde,intern_väg(kärna_värde,(String)Inställningar.get("system_tester")),추가인수,miljö);
        }
    }
}
