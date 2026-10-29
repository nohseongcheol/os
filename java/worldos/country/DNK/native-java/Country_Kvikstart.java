// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.security.MessageDigest;
import java.util.*;

/** 독립 국가판의 의존성 검사·복원·build_System·실행을 맡는 vært Java Værktøjer. */
public final class Country_Kvikstart {
    static final class data_parser {
        final String KILDE; int Placering;
        data_parser(String Tekst) { KILDE = Tekst; }
        void 빈칸() { while (Placering < KILDE.length() && Character.isWhitespace(KILDE.charAt(Placering))) Placering++; }
        Object Læse() {
            빈칸(); char tegn_VÆRDI = KILDE.charAt(Placering++);
            if (tegn_VÆRDI == '{') {
                Map<String,Object> KR = new LinkedHashMap<>(); 빈칸();
                if (KILDE.charAt(Placering) == '}') { Placering++; return KR; }
                while (true) {
                    String Navn = (String)Læse(); 빈칸(); if (KILDE.charAt(Placering++) != ':') throw new IllegalArgumentException("data afgrænser_VÆRDI fejl");
                    KR.put(Navn, Læse()); 빈칸(); char afgrænser_VÆRDI = KILDE.charAt(Placering++);
                    if (afgrænser_VÆRDI == '}') return KR; if (afgrænser_VÆRDI != ',') throw new IllegalArgumentException("data afgrænser_VÆRDI fejl");
                }
            }
            if (tegn_VÆRDI == '[') {
                List<Object> KR = new ArrayList<>(); 빈칸();
                if (KILDE.charAt(Placering) == ']') { Placering++; return KR; }
                while (true) {
                    KR.add(Læse()); 빈칸(); char afgrænser_VÆRDI = KILDE.charAt(Placering++);
                    if (afgrænser_VÆRDI == ']') return KR; if (afgrænser_VÆRDI != ',') throw new IllegalArgumentException("data afgrænser_VÆRDI fejl");
                }
            }
            if (tegn_VÆRDI == '"') {
                StringBuilder KR = new StringBuilder();
                while (true) {
                    char Næste_vare = KILDE.charAt(Placering++); if (Næste_vare == '"') return KR.toString();
                    if (Næste_vare == '\\') {
                        Næste_vare = KILDE.charAt(Placering++);
                        if (Næste_vare == 'u') { KR.append((char)Integer.parseInt(KILDE.substring(Placering, Placering + 4),16)); Placering += 4; continue; }
                        if (Næste_vare == 'n') Næste_vare = '\n'; else if (Næste_vare == 'r') Næste_vare = '\r'; else if (Næste_vare == 't') Næste_vare = '\t';
                        else if (Næste_vare == 'b') Næste_vare = '\b'; else if (Næste_vare == 'f') Næste_vare = '\f';
                        else if (Næste_vare != '"' && Næste_vare != '\\' && Næste_vare != '/') throw new IllegalArgumentException("문자 이스케이프 fejl");
                    }
                    KR.append(Næste_vare);
                }
            }
            int Kør_2 = Placering - 1;
            while (Placering < KILDE.length() && ",]} \t\r\n".indexOf(KILDE.charAt(Placering)) < 0) Placering++;
            String VÆRDI = KILDE.substring(Kør_2, Placering);
            if (VÆRDI.equals("true")) return Boolean.TRUE; if (VÆRDI.equals("false")) return Boolean.FALSE; if (VÆRDI.equals("null")) return null;
            return Double.valueOf(VÆRDI);
        }
    }
    static String hash_fil(Path Sti) throws Exception {
        MessageDigest 계산 = MessageDigest.getInstance("SHA-256"); byte[] data = new byte[1024 * 1024];
        try (InputStream input_VÆRDI = Files.newInputStream(Sti)) { for (int varighed_VÆRDI; (varighed_VÆRDI = input_VÆRDI.read(data)) >= 0;) 계산.update(data,0,varighed_VÆRDI); }
        return hash_sms(계산.digest());
    }
    static String hash_sms(byte[] data) {
        StringBuilder Tekst = new StringBuilder(); for (byte VÆRDI : data) Tekst.append(String.format(Locale.ROOT,"%02x",VÆRDI & 255)); return Tekst.toString();
    }
    static Path intern_sti(Path To_do_rod, String Navn) {
        Path KR = To_do_rod.resolve(Navn).normalize();
        if (Navn.isEmpty() || Paths.get(Navn).isAbsolute() || !KR.startsWith(To_do_rod) || Navn.indexOf('\\') >= 0)
            throw new IllegalArgumentException("범위를 벗어난 Sti: " + Navn);
        for (Path 부분 : Paths.get(Navn)) if (부분.toString().equals("..")) throw new IllegalArgumentException("상위 Sti 금지: " + Navn);
        for (Path aktuel_vare = KR; aktuel_vare != null && aktuel_vare.startsWith(To_do_rod); aktuel_vare = aktuel_vare.getParent())
            if (Files.isSymbolicLink(aktuel_vare)) throw new IllegalArgumentException("의존성 경로의 링크 금지: " + Navn);
        return KR;
    }
    static String kommando_produktoutput(List<String> Kommando) throws Exception {
        Process Proces_VÆRDI = new ProcessBuilder(Kommando).redirectError(ProcessBuilder.Redirect.INHERIT).start();
        String KR = new String(Proces_VÆRDI.getInputStream().readAllBytes(),StandardCharsets.UTF_8);
        if (Proces_VÆRDI.waitFor() != 0) throw new IOException("Kommando fejl_VÆRDI: " + Kommando.get(0)); return KR;
    }
    static void pakke_ud(Path Arkiv_VÆRDI, Path destination_VÆRDI) throws Exception {
        for (String Navn : kommando_produktoutput(Arrays.asList("tar","-tzf",Arkiv_VÆRDI.toString())).split("\n")) intern_sti(destination_VÆRDI, Navn);
        for (String Linje : kommando_produktoutput(Arrays.asList("tar","-tvzf",Arkiv_VÆRDI.toString())).split("\n"))
            if (!Linje.isEmpty() && Linje.charAt(0) != '-' && Linje.charAt(0) != 'd') throw new IOException("ekstern_VÆRDI 링크 또는 특수 파일을 포함한 의존성");
        Files.createDirectories(destination_VÆRDI);
        int status_VÆRDI = new ProcessBuilder("tar","--no-same-owner","--no-same-permissions","-xzf",Arkiv_VÆRDI.toString(),"-C",destination_VÆRDI.toString()).inheritIO().start().waitFor();
        if (status_VÆRDI != 0) throw new IOException("의존성 Arkiv_VÆRDI udgive_Lager fejl_VÆRDI");
    }
    static void 호출(Path 작업경로, Path Værktøjer, List<String> Argumenter, Map<String,String> miljø) throws Exception {
        List<String> Kommando = new ArrayList<>(Arrays.asList("python3", Værktøjer.toString())); Kommando.addAll(Argumenter);
        ProcessBuilder Udfør_kommando = new ProcessBuilder(Kommando).directory(작업경로.toFile()).inheritIO(); Udfør_kommando.environment().putAll(miljø);
        int status_VÆRDI = Udfør_kommando.start().waitFor(); if (status_VÆRDI != 0) throw new IOException("Værktøjer fejl_VÆRDI: " + Værktøjer + " (" + status_VÆRDI + ")");
    }
    @SuppressWarnings("unchecked")
    public static void main(String[] Argumenter) throws Exception {
        if (Argumenter.length < 1) throw new IllegalArgumentException("build, run, desktop, image, check, test-system 중 동작을 지정하세요");
        String Handling = Argumenter[0];
        if (!Arrays.asList("build","run","desktop","image","check","test-system").contains(Handling)) throw new IllegalArgumentException("알 tal 없는 Handling");
        Path To_do_rod = Paths.get(System.getProperty("worldos.edition.root")).toAbsolutePath().normalize();
        Map<String,Object> Indstillinger = (Map<String,Object>)new data_parser(Files.readString(To_do_rod.resolve("native.json"),StandardCharsets.UTF_8)).Læse();
        Path kilde_træ = intern_sti(To_do_rod,(String)Indstillinger.get("source")), kerne_VÆRDI = intern_sti(kilde_træ,(String)Indstillinger.get("native"));
        List<String> 소유파일들 = (List<String>)(List<?>)Indstillinger.get("owned_files");
        for (String Navn : 소유파일들) if (!Files.isRegularFile(intern_sti(kilde_træ,Navn))) throw new IOException("kilde_træ 없음: " + Navn);
        if (Handling.equals("check")) { System.out.println(Indstillinger.get("country") + " " + Indstillinger.get("language") + " 독립 kilde_træ bekræfte 완료"); return; }
        String ressource_relativ_sti = (String)Indstillinger.getOrDefault("resource_root", ".");
        if (!ressource_relativ_sti.equals(".") && !ressource_relativ_sti.equals("..")) throw new IllegalArgumentException("의존성 To_do_rod Sti fejl");
        Path ressource_VÆRDI = To_do_rod.resolve(ressource_relativ_sti).normalize(); Path Arkiv_VÆRDI = ressource_VÆRDI.resolve("native-vendor.tar.gz");
        String 기대해시 = (String)Indstillinger.get("vendor_sha256");
        if (!hash_fil(Arkiv_VÆRDI).equals(기대해시)) throw new IOException("의존성 SHA-256 불일치");
        Path mærke_VÆRDI = kilde_træ.resolve(".vendor-sha256");
        if (!Files.isRegularFile(mærke_VÆRDI) || !Files.readString(mærke_VÆRDI).trim().equals(기대해시)) { pakke_ud(Arkiv_VÆRDI, kilde_træ); Files.writeString(mærke_VÆRDI,기대해시 + "\n"); }
        Map<String,String> miljø = new HashMap<>(System.getenv());
        Path ipConfig = null;
        if (miljø.containsKey("IP_CONFIG")) ipConfig = Paths.get(miljø.get("IP_CONFIG")).toAbsolutePath().normalize();
        else for (Path parent = To_do_rod; parent != null; parent = parent.getParent()) {
            if (Files.isRegularFile(parent.resolve("ip.conf"))) { ipConfig = parent.resolve("ip.conf"); break; }
        }
        if (ipConfig == null) ipConfig = kilde_træ.resolve("ip.conf");
        if (!Files.isRegularFile(ipConfig)) throw new IOException("Missing ip.conf: " + ipConfig);
        miljø.put("IP_CONFIG", ipConfig.toString());
        if (Arrays.asList("run","desktop","test-system").contains(Handling) && !miljø.containsKey("QEMU_AARCH64")) {
            Path app_Kvikstart = ressource_VÆRDI.resolve("host/qemu"), Kvikstart_mærke = ressource_VÆRDI.resolve("host/.qemu-sha256");
            String Kvikstart_hash = (String)Indstillinger.get("qemu_sha256");
            if (!Files.isRegularFile(app_Kvikstart) || !Files.isRegularFile(Kvikstart_mærke) || !Files.readString(Kvikstart_mærke).trim().equals(Kvikstart_hash)) {
                Path Kvikstart_Arkiv = ressource_VÆRDI.resolve("qemu-host.tar.gz"); if (!hash_fil(Kvikstart_Arkiv).equals(Kvikstart_hash)) throw new IOException("QEMU SHA-256 불일치");
                pakke_ud(Kvikstart_Arkiv,ressource_VÆRDI.resolve("host")); Files.writeString(Kvikstart_mærke,Kvikstart_hash + "\n");
            }
            miljø.put("QEMU_AARCH64",app_Kvikstart.toString());
        }
        MessageDigest 계산 = MessageDigest.getInstance("SHA-256"); Collections.sort(소유파일들);
        for (String Navn : 소유파일들) { 계산.update(Navn.getBytes(StandardCharsets.UTF_8)); 계산.update(Files.readAllBytes(intern_sti(kilde_træ,Navn))); }
        계산.update("ip.conf\0".getBytes(StandardCharsets.UTF_8)); 계산.update(Files.readAllBytes(ipConfig));
        String kilde_hash = hash_sms(계산.digest()); Path build_mærke = kerne_VÆRDI.resolve("build/worldos-source.sha256");
        if (Handling.equals("build") || !Files.isRegularFile(build_mærke) || !Files.readString(build_mærke).trim().equals(kilde_hash)) {
            호출(kerne_VÆRDI,intern_sti(kerne_VÆRDI,(String)Indstillinger.get("builder")),Collections.emptyList(),miljø);
            Files.writeString(build_mærke,kilde_hash + "\n");
        }
        List<String> 추가인수 = new ArrayList<>(Arrays.asList(Argumenter).subList(1,Argumenter.length));
        if (Handling.equals("run") || Handling.equals("desktop")) {
            if (Handling.equals("desktop")) 추가인수.add(0,"--desktop");
            호출(kerne_VÆRDI,intern_sti(kerne_VÆRDI,(String)Indstillinger.get("runner")),추가인수,miljø);
        } else if (Handling.equals("image")) 호출(kerne_VÆRDI,intern_sti(kerne_VÆRDI,(String)Indstillinger.get("image_builder")),추가인수,miljø);
        else if (Handling.equals("test-system")) {
            추가인수.add(0,To_do_rod.toString()); 추가인수.add(0,"--edition");
            호출(kerne_VÆRDI,intern_sti(kerne_VÆRDI,(String)Indstillinger.get("system_tester")),추가인수,miljø);
        }
    }
}
