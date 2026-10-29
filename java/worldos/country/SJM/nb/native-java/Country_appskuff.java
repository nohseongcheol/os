// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.security.MessageDigest;
import java.util.*;

/** 독립 국가판의 의존성 검사·복원·bygg_System·실행을 맡는 vert Java Verktøy. */
public final class Country_appskuff {
    static final class data_parser {
        final String KILDE; int Posisjon;
        data_parser(String Tekst) { KILDE = Tekst; }
        void 빈칸() { while (Posisjon < KILDE.length() && Character.isWhitespace(KILDE.charAt(Posisjon))) Posisjon++; }
        Object Les() {
            빈칸(); char tegn_VERDI = KILDE.charAt(Posisjon++);
            if (tegn_VERDI == '{') {
                Map<String,Object> KR = new LinkedHashMap<>(); 빈칸();
                if (KILDE.charAt(Posisjon) == '}') { Posisjon++; return KR; }
                while (true) {
                    String Navn = (String)Les(); 빈칸(); if (KILDE.charAt(Posisjon++) != ':') throw new IllegalArgumentException("data skilletegn_VERDI feil");
                    KR.put(Navn, Les()); 빈칸(); char skilletegn_VERDI = KILDE.charAt(Posisjon++);
                    if (skilletegn_VERDI == '}') return KR; if (skilletegn_VERDI != ',') throw new IllegalArgumentException("data skilletegn_VERDI feil");
                }
            }
            if (tegn_VERDI == '[') {
                List<Object> KR = new ArrayList<>(); 빈칸();
                if (KILDE.charAt(Posisjon) == ']') { Posisjon++; return KR; }
                while (true) {
                    KR.add(Les()); 빈칸(); char skilletegn_VERDI = KILDE.charAt(Posisjon++);
                    if (skilletegn_VERDI == ']') return KR; if (skilletegn_VERDI != ',') throw new IllegalArgumentException("data skilletegn_VERDI feil");
                }
            }
            if (tegn_VERDI == '"') {
                StringBuilder KR = new StringBuilder();
                while (true) {
                    char Neste_vare = KILDE.charAt(Posisjon++); if (Neste_vare == '"') return KR.toString();
                    if (Neste_vare == '\\') {
                        Neste_vare = KILDE.charAt(Posisjon++);
                        if (Neste_vare == 'u') { KR.append((char)Integer.parseInt(KILDE.substring(Posisjon, Posisjon + 4),16)); Posisjon += 4; continue; }
                        if (Neste_vare == 'n') Neste_vare = '\n'; else if (Neste_vare == 'r') Neste_vare = '\r'; else if (Neste_vare == 't') Neste_vare = '\t';
                        else if (Neste_vare == 'b') Neste_vare = '\b'; else if (Neste_vare == 'f') Neste_vare = '\f';
                        else if (Neste_vare != '"' && Neste_vare != '\\' && Neste_vare != '/') throw new IllegalArgumentException("문자 이스케이프 feil");
                    }
                    KR.append(Neste_vare);
                }
            }
            int Kjør_2 = Posisjon - 1;
            while (Posisjon < KILDE.length() && ",]} \t\r\n".indexOf(KILDE.charAt(Posisjon)) < 0) Posisjon++;
            String VERDI = KILDE.substring(Kjør_2, Posisjon);
            if (VERDI.equals("true")) return Boolean.TRUE; if (VERDI.equals("false")) return Boolean.FALSE; if (VERDI.equals("null")) return null;
            return Double.valueOf(VERDI);
        }
    }
    static String hash_Fil(Path Sti) throws Exception {
        MessageDigest 계산 = MessageDigest.getInstance("SHA-256"); byte[] data = new byte[1024 * 1024];
        try (InputStream inndata_VERDI = Files.newInputStream(Sti)) { for (int lengde_VERDI; (lengde_VERDI = inndata_VERDI.read(data)) >= 0;) 계산.update(data,0,lengde_VERDI); }
        return hash_SMS(계산.digest());
    }
    static String hash_SMS(byte[] data) {
        StringBuilder Tekst = new StringBuilder(); for (byte VERDI : data) Tekst.append(String.format(Locale.ROOT,"%02x",VERDI & 255)); return Tekst.toString();
    }
    static Path intern_bane(Path speile_rot, String Navn) {
        Path KR = speile_rot.resolve(Navn).normalize();
        if (Navn.isEmpty() || Paths.get(Navn).isAbsolute() || !KR.startsWith(speile_rot) || Navn.indexOf('\\') >= 0)
            throw new IllegalArgumentException("범위를 벗어난 Sti: " + Navn);
        for (Path 부분 : Paths.get(Navn)) if (부분.toString().equals("..")) throw new IllegalArgumentException("상위 Sti 금지: " + Navn);
        for (Path betalt_vare = KR; betalt_vare != null && betalt_vare.startsWith(speile_rot); betalt_vare = betalt_vare.getParent())
            if (Files.isSymbolicLink(betalt_vare)) throw new IllegalArgumentException("의존성 경로의 링크 금지: " + Navn);
        return KR;
    }
    static String kommando_produksjon(List<String> Kommando) throws Exception {
        Process Prosess_VERDI = new ProcessBuilder(Kommando).redirectError(ProcessBuilder.Redirect.INHERIT).start();
        String KR = new String(Prosess_VERDI.getInputStream().readAllBytes(),StandardCharsets.UTF_8);
        if (Prosess_VERDI.waitFor() != 0) throw new IOException("Kommando feil_VERDI: " + Kommando.get(0)); return KR;
    }
    static void pakke_ut(Path Arkiv_VERDI, Path mål_VERDI) throws Exception {
        for (String Navn : kommando_produksjon(Arrays.asList("tar","-tzf",Arkiv_VERDI.toString())).split("\n")) intern_bane(mål_VERDI, Navn);
        for (String Linje : kommando_produksjon(Arrays.asList("tar","-tvzf",Arkiv_VERDI.toString())).split("\n"))
            if (!Linje.isEmpty() && Linje.charAt(0) != '-' && Linje.charAt(0) != 'd') throw new IOException("ekstern_VERDI 링크 또는 특수 파일을 포함한 의존성");
        Files.createDirectories(mål_VERDI);
        int status_VERDI = new ProcessBuilder("tar","--no-same-owner","--no-same-permissions","-xzf",Arkiv_VERDI.toString(),"-C",mål_VERDI.toString()).inheritIO().start().waitFor();
        if (status_VERDI != 0) throw new IOException("의존성 Arkiv_VERDI frigi_lager feil_VERDI");
    }
    static void 호출(Path 작업경로, Path Verktøy, List<String> Argumenter, Map<String,String> miljø) throws Exception {
        List<String> Kommando = new ArrayList<>(Arrays.asList("python3", Verktøy.toString())); Kommando.addAll(Argumenter);
        ProcessBuilder Utfør_kommando = new ProcessBuilder(Kommando).directory(작업경로.toFile()).inheritIO(); Utfør_kommando.environment().putAll(miljø);
        int status_VERDI = Utfør_kommando.start().waitFor(); if (status_VERDI != 0) throw new IOException("Verktøy feil_VERDI: " + Verktøy + " (" + status_VERDI + ")");
    }
    @SuppressWarnings("unchecked")
    public static void main(String[] Argumenter) throws Exception {
        if (Argumenter.length < 1) throw new IllegalArgumentException("build, run, desktop, image, check, test-system 중 동작을 지정하세요");
        String Handling = Argumenter[0];
        if (!Arrays.asList("build","run","desktop","image","check","test-system").contains(Handling)) throw new IllegalArgumentException("알 nummer 없는 Handling");
        Path speile_rot = Paths.get(System.getProperty("worldos.edition.root")).toAbsolutePath().normalize();
        Map<String,Object> Innstillinger = (Map<String,Object>)new data_parser(Files.readString(speile_rot.resolve("native.json"),StandardCharsets.UTF_8)).Les();
        Path kilde_tre = intern_bane(speile_rot,(String)Innstillinger.get("source")), kjerne_VERDI = intern_bane(kilde_tre,(String)Innstillinger.get("native"));
        List<String> 소유파일들 = (List<String>)(List<?>)Innstillinger.get("owned_files");
        for (String Navn : 소유파일들) if (!Files.isRegularFile(intern_bane(kilde_tre,Navn))) throw new IOException("kilde_tre 없음: " + Navn);
        if (Handling.equals("check")) { System.out.println(Innstillinger.get("country") + " " + Innstillinger.get("language") + " 독립 kilde_tre bekrefte 완료"); return; }
        String ressurs_relativ_bane = (String)Innstillinger.getOrDefault("resource_root", ".");
        if (!ressurs_relativ_bane.equals(".") && !ressurs_relativ_bane.equals("..")) throw new IllegalArgumentException("의존성 speile_rot Sti feil");
        Path ressurs_VERDI = speile_rot.resolve(ressurs_relativ_bane).normalize(); Path Arkiv_VERDI = ressurs_VERDI.resolve("native-vendor.tar.gz");
        String 기대해시 = (String)Innstillinger.get("vendor_sha256");
        if (!hash_Fil(Arkiv_VERDI).equals(기대해시)) throw new IOException("의존성 SHA-256 불일치");
        Path tusj_VERDI = kilde_tre.resolve(".vendor-sha256");
        if (!Files.isRegularFile(tusj_VERDI) || !Files.readString(tusj_VERDI).trim().equals(기대해시)) { pakke_ut(Arkiv_VERDI, kilde_tre); Files.writeString(tusj_VERDI,기대해시 + "\n"); }
        Map<String,String> miljø = new HashMap<>(System.getenv());
        Path ipConfig = null;
        if (miljø.containsKey("IP_CONFIG")) ipConfig = Paths.get(miljø.get("IP_CONFIG")).toAbsolutePath().normalize();
        else for (Path parent = speile_rot; parent != null; parent = parent.getParent()) {
            if (Files.isRegularFile(parent.resolve("ip.conf"))) { ipConfig = parent.resolve("ip.conf"); break; }
        }
        if (ipConfig == null) ipConfig = kilde_tre.resolve("ip.conf");
        if (!Files.isRegularFile(ipConfig)) throw new IOException("Missing ip.conf: " + ipConfig);
        miljø.put("IP_CONFIG", ipConfig.toString());
        if (Arrays.asList("run","desktop","test-system").contains(Handling) && !miljø.containsKey("QEMU_AARCH64")) {
            Path app_appskuff = ressurs_VERDI.resolve("host/qemu"), appskuff_tusj = ressurs_VERDI.resolve("host/.qemu-sha256");
            String appskuff_hash = (String)Innstillinger.get("qemu_sha256");
            if (!Files.isRegularFile(app_appskuff) || !Files.isRegularFile(appskuff_tusj) || !Files.readString(appskuff_tusj).trim().equals(appskuff_hash)) {
                Path appskuff_Arkiv = ressurs_VERDI.resolve("qemu-host.tar.gz"); if (!hash_Fil(appskuff_Arkiv).equals(appskuff_hash)) throw new IOException("QEMU SHA-256 불일치");
                pakke_ut(appskuff_Arkiv,ressurs_VERDI.resolve("host")); Files.writeString(appskuff_tusj,appskuff_hash + "\n");
            }
            miljø.put("QEMU_AARCH64",app_appskuff.toString());
        }
        MessageDigest 계산 = MessageDigest.getInstance("SHA-256"); Collections.sort(소유파일들);
        for (String Navn : 소유파일들) { 계산.update(Navn.getBytes(StandardCharsets.UTF_8)); 계산.update(Files.readAllBytes(intern_bane(kilde_tre,Navn))); }
        계산.update("ip.conf\0".getBytes(StandardCharsets.UTF_8)); 계산.update(Files.readAllBytes(ipConfig));
        String kilde_hash = hash_SMS(계산.digest()); Path bygg_tusj = kjerne_VERDI.resolve("build/worldos-source.sha256");
        if (Handling.equals("build") || !Files.isRegularFile(bygg_tusj) || !Files.readString(bygg_tusj).trim().equals(kilde_hash)) {
            호출(kjerne_VERDI,intern_bane(kjerne_VERDI,(String)Innstillinger.get("builder")),Collections.emptyList(),miljø);
            Files.writeString(bygg_tusj,kilde_hash + "\n");
        }
        List<String> 추가인수 = new ArrayList<>(Arrays.asList(Argumenter).subList(1,Argumenter.length));
        if (Handling.equals("run") || Handling.equals("desktop")) {
            if (Handling.equals("desktop")) 추가인수.add(0,"--desktop");
            호출(kjerne_VERDI,intern_bane(kjerne_VERDI,(String)Innstillinger.get("runner")),추가인수,miljø);
        } else if (Handling.equals("image")) 호출(kjerne_VERDI,intern_bane(kjerne_VERDI,(String)Innstillinger.get("image_builder")),추가인수,miljø);
        else if (Handling.equals("test-system")) {
            추가인수.add(0,speile_rot.toString()); 추가인수.add(0,"--edition");
            호출(kjerne_VERDI,intern_bane(kjerne_VERDI,(String)Innstillinger.get("system_tester")),추가인수,miljø);
        }
    }
}
