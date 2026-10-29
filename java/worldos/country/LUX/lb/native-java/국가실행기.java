// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.security.MessageDigest;
import java.util.*;

/** 독립 국가판의 의존성 검사·복원·Build_System·실행을 맡는 Host Java Tools. */
public final class 국가실행기 {
    static final class 자료해석기 {
        final String Quell; int positionéieren;
        자료해석기(String SMS) { Quell = SMS; }
        void 빈칸() { while (positionéieren < Quell.length() && Character.isWhitespace(Quell.charAt(positionéieren))) positionéieren++; }
        Object 읽기() {
            빈칸(); char Zeechen_VALUE = Quell.charAt(positionéieren++);
            if (Zeechen_VALUE == '{') {
                Map<String,Object> Mooss = new LinkedHashMap<>(); 빈칸();
                if (Quell.charAt(positionéieren) == '}') { positionéieren++; return Mooss; }
                while (true) {
                    String Numm = (String)읽기(); 빈칸(); if (Quell.charAt(positionéieren++) != ':') throw new IllegalArgumentException("Daten Trennzeechen_VALUE_d8ba4873 Feeler");
                    Mooss.put(Numm, 읽기()); 빈칸(); char Trennzeechen_VALUE_d8ba4873 = Quell.charAt(positionéieren++);
                    if (Trennzeechen_VALUE_d8ba4873 == '}') return Mooss; if (Trennzeechen_VALUE_d8ba4873 != ',') throw new IllegalArgumentException("Daten Trennzeechen_VALUE_d8ba4873 Feeler");
                }
            }
            if (Zeechen_VALUE == '[') {
                List<Object> Mooss = new ArrayList<>(); 빈칸();
                if (Quell.charAt(positionéieren) == ']') { positionéieren++; return Mooss; }
                while (true) {
                    Mooss.add(읽기()); 빈칸(); char Trennzeechen_VALUE_d8ba4873 = Quell.charAt(positionéieren++);
                    if (Trennzeechen_VALUE_d8ba4873 == ']') return Mooss; if (Trennzeechen_VALUE_d8ba4873 != ',') throw new IllegalArgumentException("Daten Trennzeechen_VALUE_d8ba4873 Feeler");
                }
            }
            if (Zeechen_VALUE == '"') {
                StringBuilder Mooss = new StringBuilder();
                while (true) {
                    char Weider_Element = Quell.charAt(positionéieren++); if (Weider_Element == '"') return Mooss.toString();
                    if (Weider_Element == '\\') {
                        Weider_Element = Quell.charAt(positionéieren++);
                        if (Weider_Element == 'u') { Mooss.append((char)Integer.parseInt(Quell.substring(positionéieren, positionéieren + 4),16)); positionéieren += 4; continue; }
                        if (Weider_Element == 'n') Weider_Element = '\n'; else if (Weider_Element == 'r') Weider_Element = '\r'; else if (Weider_Element == 't') Weider_Element = '\t';
                        else if (Weider_Element == 'b') Weider_Element = '\b'; else if (Weider_Element == 'f') Weider_Element = '\f';
                        else if (Weider_Element != '"' && Weider_Element != '\\' && Weider_Element != '/') throw new IllegalArgumentException("문자 이스케이프 Feeler");
                    }
                    Mooss.append(Weider_Element);
                }
            }
            int Laf = positionéieren - 1;
            while (positionéieren < Quell.length() && ",]} \t\r\n".indexOf(Quell.charAt(positionéieren)) < 0) positionéieren++;
            String VALUE = Quell.substring(Laf, positionéieren);
            if (VALUE.equals("true")) return Boolean.TRUE; if (VALUE.equals("false")) return Boolean.FALSE; if (VALUE.equals("null")) return null;
            return Double.valueOf(VALUE);
        }
    }
    static String Hash_Fichier(Path Wee) throws Exception {
        MessageDigest 계산 = MessageDigest.getInstance("SHA-256"); byte[] Daten = new byte[1024 * 1024];
        try (InputStream 입력 = Files.newInputStream(Wee)) { for (int Längt_VALUE; (Längt_VALUE = 입력.read(Daten)) >= 0;) 계산.update(Daten,0,Längt_VALUE); }
        return Hash_SMS(계산.digest());
    }
    static String Hash_SMS(byte[] Daten) {
        StringBuilder SMS = new StringBuilder(); for (byte VALUE : Daten) SMS.append(String.format(Locale.ROOT,"%02x",VALUE & 255)); return SMS.toString();
    }
    static Path 내부경로(Path projezéieren_Racinn, String Numm) {
        Path Mooss = projezéieren_Racinn.resolve(Numm).normalize();
        if (Numm.isEmpty() || Paths.get(Numm).isAbsolute() || !Mooss.startsWith(projezéieren_Racinn) || Numm.indexOf('\\') >= 0)
            throw new IllegalArgumentException("범위를 벗어난 Wee: " + Numm);
        for (Path 부분 : Paths.get(Numm)) if (부분.toString().equals("..")) throw new IllegalArgumentException("상위 Wee 금지: " + Numm);
        for (Path 현재 = Mooss; 현재 != null && 현재.startsWith(projezéieren_Racinn); 현재 = 현재.getParent())
            if (Files.isSymbolicLink(현재)) throw new IllegalArgumentException("의존성 경로의 링크 금지: " + Numm);
        return Mooss;
    }
    static String 명령출력(List<String> Befeel) throws Exception {
        Process Prozess_VALUE = new ProcessBuilder(Befeel).redirectError(ProcessBuilder.Redirect.INHERIT).start();
        String Mooss = new String(Prozess_VALUE.getInputStream().readAllBytes(),StandardCharsets.UTF_8);
        if (Prozess_VALUE.waitFor() != 0) throw new IOException("Befeel Feeler_VALUE: " + Befeel.get(0)); return Mooss;
    }
    static void erauszéien(Path Archiv_VALUE, Path Zil_VALUE) throws Exception {
        for (String Numm : 명령출력(Arrays.asList("tar","-tzf",Archiv_VALUE.toString())).split("\n")) 내부경로(Zil_VALUE, Numm);
        for (String Zeil : 명령출력(Arrays.asList("tar","-tvzf",Archiv_VALUE.toString())).split("\n"))
            if (!Zeil.isEmpty() && Zeil.charAt(0) != '-' && Zeil.charAt(0) != 'd') throw new IOException("외부 링크 또는 특수 파일을 포함한 의존성");
        Files.createDirectories(Zil_VALUE);
        int Status_VALUE = new ProcessBuilder("tar","--no-same-owner","--no-same-permissions","-xzf",Archiv_VALUE.toString(),"-C",Zil_VALUE.toString()).inheritIO().start().waitFor();
        if (Status_VALUE != 0) throw new IOException("의존성 Archiv_VALUE Versioun_Späicher Feeler_VALUE");
    }
    static void 호출(Path 작업경로, Path Tools, List<String> 인수, Map<String,String> 환경) throws Exception {
        List<String> Befeel = new ArrayList<>(Arrays.asList("python3", Tools.toString())); Befeel.addAll(인수);
        ProcessBuilder ausféieren_Befeel = new ProcessBuilder(Befeel).directory(작업경로.toFile()).inheritIO(); ausféieren_Befeel.environment().putAll(환경);
        int Status_VALUE = ausféieren_Befeel.start().waitFor(); if (Status_VALUE != 0) throw new IOException("Tools Feeler_VALUE: " + Tools + " (" + Status_VALUE + ")");
    }
    @SuppressWarnings("unchecked")
    public static void main(String[] 인수) throws Exception {
        if (인수.length < 1) throw new IllegalArgumentException("build, run, desktop, image, check, test-system 중 동작을 지정하세요");
        String Aktioun = 인수[0];
        if (!Arrays.asList("build","run","desktop","image","check","test-system").contains(Aktioun)) throw new IllegalArgumentException("알 수 없는 Aktioun");
        Path projezéieren_Racinn = Paths.get(System.getProperty("worldos.edition.root")).toAbsolutePath().normalize();
        Map<String,Object> Astellungen = (Map<String,Object>)new 자료해석기(Files.readString(projezéieren_Racinn.resolve("native.json"),StandardCharsets.UTF_8)).읽기();
        Path Quell_Bamstruktur = 내부경로(projezéieren_Racinn,(String)Astellungen.get("source")), Kernel_VALUE = 내부경로(Quell_Bamstruktur,(String)Astellungen.get("native"));
        List<String> 소유파일들 = (List<String>)(List<?>)Astellungen.get("owned_files");
        for (String Numm : 소유파일들) if (!Files.isRegularFile(내부경로(Quell_Bamstruktur,Numm))) throw new IOException("Quell_Bamstruktur 없음: " + Numm);
        if (Aktioun.equals("check")) { System.out.println(Astellungen.get("country") + " " + Astellungen.get("language") + " 독립 Quell_Bamstruktur verifizéieren 완료"); return; }
        String 자원상대 = (String)Astellungen.getOrDefault("resource_root", ".");
        if (!자원상대.equals(".") && !자원상대.equals("..")) throw new IllegalArgumentException("의존성 projezéieren_Racinn Wee Feeler");
        Path Ressource_VALUE = projezéieren_Racinn.resolve(자원상대).normalize(); Path Archiv_VALUE = Ressource_VALUE.resolve("native-vendor.tar.gz");
        String 기대해시 = (String)Astellungen.get("vendor_sha256");
        if (!Hash_Fichier(Archiv_VALUE).equals(기대해시)) throw new IOException("의존성 SHA-256 불일치");
        Path Markéierung_VALUE = Quell_Bamstruktur.resolve(".vendor-sha256");
        if (!Files.isRegularFile(Markéierung_VALUE) || !Files.readString(Markéierung_VALUE).trim().equals(기대해시)) { erauszéien(Archiv_VALUE, Quell_Bamstruktur); Files.writeString(Markéierung_VALUE,기대해시 + "\n"); }
        Map<String,String> 환경 = new HashMap<>(System.getenv());
        Path ipConfig = null;
        if (환경.containsKey("IP_CONFIG")) ipConfig = Paths.get(환경.get("IP_CONFIG")).toAbsolutePath().normalize();
        else for (Path parent = projezéieren_Racinn; parent != null; parent = parent.getParent()) {
            if (Files.isRegularFile(parent.resolve("ip.conf"))) { ipConfig = parent.resolve("ip.conf"); break; }
        }
        if (ipConfig == null) ipConfig = Quell_Bamstruktur.resolve("ip.conf");
        if (!Files.isRegularFile(ipConfig)) throw new IOException("Missing ip.conf: " + ipConfig);
        환경.put("IP_CONFIG", ipConfig.toString());
        if (Arrays.asList("run","desktop","test-system").contains(Aktioun) && !환경.containsKey("QEMU_AARCH64")) {
            Path App_App_Beräich = Ressource_VALUE.resolve("host/qemu"), App_Beräich_Markéierung = Ressource_VALUE.resolve("host/.qemu-sha256");
            String App_Beräich_Hash = (String)Astellungen.get("qemu_sha256");
            if (!Files.isRegularFile(App_App_Beräich) || !Files.isRegularFile(App_Beräich_Markéierung) || !Files.readString(App_Beräich_Markéierung).trim().equals(App_Beräich_Hash)) {
                Path App_Beräich_Archiv = Ressource_VALUE.resolve("qemu-host.tar.gz"); if (!Hash_Fichier(App_Beräich_Archiv).equals(App_Beräich_Hash)) throw new IOException("QEMU SHA-256 불일치");
                erauszéien(App_Beräich_Archiv,Ressource_VALUE.resolve("host")); Files.writeString(App_Beräich_Markéierung,App_Beräich_Hash + "\n");
            }
            환경.put("QEMU_AARCH64",App_App_Beräich.toString());
        }
        MessageDigest 계산 = MessageDigest.getInstance("SHA-256"); Collections.sort(소유파일들);
        for (String Numm : 소유파일들) { 계산.update(Numm.getBytes(StandardCharsets.UTF_8)); 계산.update(Files.readAllBytes(내부경로(Quell_Bamstruktur,Numm))); }
        계산.update("ip.conf\0".getBytes(StandardCharsets.UTF_8)); 계산.update(Files.readAllBytes(ipConfig));
        String Quell_Hash = Hash_SMS(계산.digest()); Path Build_Markéierung = Kernel_VALUE.resolve("build/worldos-source.sha256");
        if (Aktioun.equals("build") || !Files.isRegularFile(Build_Markéierung) || !Files.readString(Build_Markéierung).trim().equals(Quell_Hash)) {
            호출(Kernel_VALUE,내부경로(Kernel_VALUE,(String)Astellungen.get("builder")),Collections.emptyList(),환경);
            Files.writeString(Build_Markéierung,Quell_Hash + "\n");
        }
        List<String> 추가인수 = new ArrayList<>(Arrays.asList(인수).subList(1,인수.length));
        if (Aktioun.equals("run") || Aktioun.equals("desktop")) {
            if (Aktioun.equals("desktop")) 추가인수.add(0,"--desktop");
            호출(Kernel_VALUE,내부경로(Kernel_VALUE,(String)Astellungen.get("runner")),추가인수,환경);
        } else if (Aktioun.equals("image")) 호출(Kernel_VALUE,내부경로(Kernel_VALUE,(String)Astellungen.get("image_builder")),추가인수,환경);
        else if (Aktioun.equals("test-system")) {
            추가인수.add(0,projezéieren_Racinn.toString()); 추가인수.add(0,"--edition");
            호출(Kernel_VALUE,내부경로(Kernel_VALUE,(String)Astellungen.get("system_tester")),추가인수,환경);
        }
    }
}
