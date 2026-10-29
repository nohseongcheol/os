// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.security.MessageDigest;
import java.util.*;

/** 독립 국가판의 의존성 검사·복원·kompiliuoti_sistema·실행을 맡는 organizuoti Java Įrankiai. */
public final class Kantri_programų_skydelis {
    static final class duomenys_analizatorius {
        final String ŠALTINIS; int Pozicija;
        duomenys_analizatorius(String Tekstas) { ŠALTINIS = Tekstas; }
        void 빈칸() { while (Pozicija < ŠALTINIS.length() && Character.isWhitespace(ŠALTINIS.charAt(Pozicija))) Pozicija++; }
        Object Skaitymas() {
            빈칸(); char simbolis_VALUE_068c2631 = ŠALTINIS.charAt(Pozicija++);
            if (simbolis_VALUE_068c2631 == '{') {
                Map<String,Object> REZULTATAS = new LinkedHashMap<>(); 빈칸();
                if (ŠALTINIS.charAt(Pozicija) == '}') { Pozicija++; return REZULTATAS; }
                while (true) {
                    String Pavadinimas_2 = (String)Skaitymas(); 빈칸(); if (ŠALTINIS.charAt(Pozicija++) != ':') throw new IllegalArgumentException("duomenys skyriklis_VALUE_d8ba4873 KLAIDA");
                    REZULTATAS.put(Pavadinimas_2, Skaitymas()); 빈칸(); char skyriklis_VALUE_d8ba4873 = ŠALTINIS.charAt(Pozicija++);
                    if (skyriklis_VALUE_d8ba4873 == '}') return REZULTATAS; if (skyriklis_VALUE_d8ba4873 != ',') throw new IllegalArgumentException("duomenys skyriklis_VALUE_d8ba4873 KLAIDA");
                }
            }
            if (simbolis_VALUE_068c2631 == '[') {
                List<Object> REZULTATAS = new ArrayList<>(); 빈칸();
                if (ŠALTINIS.charAt(Pozicija) == ']') { Pozicija++; return REZULTATAS; }
                while (true) {
                    REZULTATAS.add(Skaitymas()); 빈칸(); char skyriklis_VALUE_d8ba4873 = ŠALTINIS.charAt(Pozicija++);
                    if (skyriklis_VALUE_d8ba4873 == ']') return REZULTATAS; if (skyriklis_VALUE_d8ba4873 != ',') throw new IllegalArgumentException("duomenys skyriklis_VALUE_d8ba4873 KLAIDA");
                }
            }
            if (simbolis_VALUE_068c2631 == '"') {
                StringBuilder REZULTATAS = new StringBuilder();
                while (true) {
                    char toliau_prekė = ŠALTINIS.charAt(Pozicija++); if (toliau_prekė == '"') return REZULTATAS.toString();
                    if (toliau_prekė == '\\') {
                        toliau_prekė = ŠALTINIS.charAt(Pozicija++);
                        if (toliau_prekė == 'u') { REZULTATAS.append((char)Integer.parseInt(ŠALTINIS.substring(Pozicija, Pozicija + 4),16)); Pozicija += 4; continue; }
                        if (toliau_prekė == 'n') toliau_prekė = '\n'; else if (toliau_prekė == 'r') toliau_prekė = '\r'; else if (toliau_prekė == 't') toliau_prekė = '\t';
                        else if (toliau_prekė == 'b') toliau_prekė = '\b'; else if (toliau_prekė == 'f') toliau_prekė = '\f';
                        else if (toliau_prekė != '"' && toliau_prekė != '\\' && toliau_prekė != '/') throw new IllegalArgumentException("문자 이스케이프 KLAIDA");
                    }
                    REZULTATAS.append(toliau_prekė);
                }
            }
            int Paleisti = Pozicija - 1;
            while (Pozicija < ŠALTINIS.length() && ",]} \t\r\n".indexOf(ŠALTINIS.charAt(Pozicija)) < 0) Pozicija++;
            String VALUE = ŠALTINIS.substring(Paleisti, Pozicija);
            if (VALUE.equals("true")) return Boolean.TRUE; if (VALUE.equals("false")) return Boolean.FALSE; if (VALUE.equals("null")) return null;
            return Double.valueOf(VALUE);
        }
    }
    static String maiša_Failas(Path KELIAS) throws Exception {
        MessageDigest 계산 = MessageDigest.getInstance("SHA-256"); byte[] duomenys = new byte[1024 * 1024];
        try (InputStream 입력 = Files.newInputStream(KELIAS)) { for (int 길이; (길이 = 입력.read(duomenys)) >= 0;) 계산.update(duomenys,0,길이); }
        return maiša_SMS(계산.digest());
    }
    static String maiša_SMS(byte[] duomenys) {
        StringBuilder Tekstas = new StringBuilder(); for (byte VALUE : duomenys) Tekstas.append(String.format(Locale.ROOT,"%02x",VALUE & 255)); return Tekstas.toString();
    }
    static Path vidinis_kelias(Path Project_šaknis, String Pavadinimas_2) {
        Path REZULTATAS = Project_šaknis.resolve(Pavadinimas_2).normalize();
        if (Pavadinimas_2.isEmpty() || Paths.get(Pavadinimas_2).isAbsolute() || !REZULTATAS.startsWith(Project_šaknis) || Pavadinimas_2.indexOf('\\') >= 0)
            throw new IllegalArgumentException("범위를 벗어난 KELIAS: " + Pavadinimas_2);
        for (Path 부분 : Paths.get(Pavadinimas_2)) if (부분.toString().equals("..")) throw new IllegalArgumentException("상위 KELIAS 금지: " + Pavadinimas_2);
        for (Path dabartinis_prekė = REZULTATAS; dabartinis_prekė != null && dabartinis_prekė.startsWith(Project_šaknis); dabartinis_prekė = dabartinis_prekė.getParent())
            if (Files.isSymbolicLink(dabartinis_prekė)) throw new IllegalArgumentException("의존성 경로의 링크 금지: " + Pavadinimas_2);
        return REZULTATAS;
    }
    static String komanda_išeiga(List<String> Komanda) throws Exception {
        Process Procesas_VALUE = new ProcessBuilder(Komanda).redirectError(ProcessBuilder.Redirect.INHERIT).start();
        String REZULTATAS = new String(Procesas_VALUE.getInputStream().readAllBytes(),StandardCharsets.UTF_8);
        if (Procesas_VALUE.waitFor() != 0) throw new IOException("Komanda triktis_VALUE: " + Komanda.get(0)); return REZULTATAS;
    }
    static void išskleisti(Path Archyvas_VALUE, Path vieta_VALUE) throws Exception {
        for (String Pavadinimas_2 : komanda_išeiga(Arrays.asList("tar","-tzf",Archyvas_VALUE.toString())).split("\n")) vidinis_kelias(vieta_VALUE, Pavadinimas_2);
        for (String Eilutė : komanda_išeiga(Arrays.asList("tar","-tvzf",Archyvas_VALUE.toString())).split("\n"))
            if (!Eilutė.isEmpty() && Eilutė.charAt(0) != '-' && Eilutė.charAt(0) != 'd') throw new IOException("išorinis_VALUE 링크 또는 특수 파일을 포함한 의존성");
        Files.createDirectories(vieta_VALUE);
        int Būsena_VALUE = new ProcessBuilder("tar","--no-same-owner","--no-same-permissions","-xzf",Archyvas_VALUE.toString(),"-C",vieta_VALUE.toString()).inheritIO().start().waitFor();
        if (Būsena_VALUE != 0) throw new IOException("의존성 Archyvas_VALUE išleisti_Saugykla triktis_VALUE");
    }
    static void 호출(Path 작업경로, Path Įrankiai, List<String> Argumentai, Map<String,String> 환경) throws Exception {
        List<String> Komanda = new ArrayList<>(Arrays.asList("python3", Įrankiai.toString())); Komanda.addAll(Argumentai);
        ProcessBuilder Vykdyti_komanda = new ProcessBuilder(Komanda).directory(작업경로.toFile()).inheritIO(); Vykdyti_komanda.environment().putAll(환경);
        int Būsena_VALUE = Vykdyti_komanda.start().waitFor(); if (Būsena_VALUE != 0) throw new IOException("Įrankiai triktis_VALUE: " + Įrankiai + " (" + Būsena_VALUE + ")");
    }
    @SuppressWarnings("unchecked")
    public static void main(String[] Argumentai) throws Exception {
        if (Argumentai.length < 1) throw new IllegalArgumentException("build, run, desktop, image, check, test-system 중 동작을 지정하세요");
        String Veiksmas = Argumentai[0];
        if (!Arrays.asList("build","run","desktop","image","check","test-system").contains(Veiksmas)) throw new IllegalArgumentException("알 numeris 없는 Veiksmas");
        Path Project_šaknis = Paths.get(System.getProperty("worldos.edition.root")).toAbsolutePath().normalize();
        Map<String,Object> Nustatymai = (Map<String,Object>)new duomenys_analizatorius(Files.readString(Project_šaknis.resolve("native.json"),StandardCharsets.UTF_8)).Skaitymas();
        Path šaltinis_medis = vidinis_kelias(Project_šaknis,(String)Nustatymai.get("source")), branduolys_VALUE = vidinis_kelias(šaltinis_medis,(String)Nustatymai.get("native"));
        List<String> 소유파일들 = (List<String>)(List<?>)Nustatymai.get("owned_files");
        for (String Pavadinimas_2 : 소유파일들) if (!Files.isRegularFile(vidinis_kelias(šaltinis_medis,Pavadinimas_2))) throw new IOException("šaltinis_medis 없음: " + Pavadinimas_2);
        if (Veiksmas.equals("check")) { System.out.println(Nustatymai.get("country") + " " + Nustatymai.get("language") + " 독립 šaltinis_medis patvirtinti 완료"); return; }
        String ištekliai_santykinis_kelias = (String)Nustatymai.getOrDefault("resource_root", ".");
        if (!ištekliai_santykinis_kelias.equals(".") && !ištekliai_santykinis_kelias.equals("..")) throw new IllegalArgumentException("의존성 Project_šaknis KELIAS KLAIDA");
        Path ištekliai_VALUE = Project_šaknis.resolve(ištekliai_santykinis_kelias).normalize(); Path Archyvas_VALUE = ištekliai_VALUE.resolve("native-vendor.tar.gz");
        String 기대해시 = (String)Nustatymai.get("vendor_sha256");
        if (!maiša_Failas(Archyvas_VALUE).equals(기대해시)) throw new IOException("의존성 SHA-256 불일치");
        Path žymeklis_VALUE = šaltinis_medis.resolve(".vendor-sha256");
        if (!Files.isRegularFile(žymeklis_VALUE) || !Files.readString(žymeklis_VALUE).trim().equals(기대해시)) { išskleisti(Archyvas_VALUE, šaltinis_medis); Files.writeString(žymeklis_VALUE,기대해시 + "\n"); }
        Map<String,String> 환경 = new HashMap<>(System.getenv());
        Path ipConfig = null;
        if (환경.containsKey("IP_CONFIG")) ipConfig = Paths.get(환경.get("IP_CONFIG")).toAbsolutePath().normalize();
        else for (Path parent = Project_šaknis; parent != null; parent = parent.getParent()) {
            if (Files.isRegularFile(parent.resolve("ip.conf"))) { ipConfig = parent.resolve("ip.conf"); break; }
        }
        if (ipConfig == null) ipConfig = šaltinis_medis.resolve("ip.conf");
        if (!Files.isRegularFile(ipConfig)) throw new IOException("Missing ip.conf: " + ipConfig);
        환경.put("IP_CONFIG", ipConfig.toString());
        if (Arrays.asList("run","desktop","test-system").contains(Veiksmas) && !환경.containsKey("QEMU_AARCH64")) {
            Path programa_programų_skydelis = ištekliai_VALUE.resolve("host/qemu"), programų_skydelis_žymeklis = ištekliai_VALUE.resolve("host/.qemu-sha256");
            String programų_skydelis_maiša = (String)Nustatymai.get("qemu_sha256");
            if (!Files.isRegularFile(programa_programų_skydelis) || !Files.isRegularFile(programų_skydelis_žymeklis) || !Files.readString(programų_skydelis_žymeklis).trim().equals(programų_skydelis_maiša)) {
                Path programų_skydelis_Archyvas = ištekliai_VALUE.resolve("qemu-host.tar.gz"); if (!maiša_Failas(programų_skydelis_Archyvas).equals(programų_skydelis_maiša)) throw new IOException("QEMU SHA-256 불일치");
                išskleisti(programų_skydelis_Archyvas,ištekliai_VALUE.resolve("host")); Files.writeString(programų_skydelis_žymeklis,programų_skydelis_maiša + "\n");
            }
            환경.put("QEMU_AARCH64",programa_programų_skydelis.toString());
        }
        MessageDigest 계산 = MessageDigest.getInstance("SHA-256"); Collections.sort(소유파일들);
        for (String Pavadinimas_2 : 소유파일들) { 계산.update(Pavadinimas_2.getBytes(StandardCharsets.UTF_8)); 계산.update(Files.readAllBytes(vidinis_kelias(šaltinis_medis,Pavadinimas_2))); }
        계산.update("ip.conf\0".getBytes(StandardCharsets.UTF_8)); 계산.update(Files.readAllBytes(ipConfig));
        String šaltinis_maiša = maiša_SMS(계산.digest()); Path kompiliuoti_žymeklis = branduolys_VALUE.resolve("build/worldos-source.sha256");
        if (Veiksmas.equals("build") || !Files.isRegularFile(kompiliuoti_žymeklis) || !Files.readString(kompiliuoti_žymeklis).trim().equals(šaltinis_maiša)) {
            호출(branduolys_VALUE,vidinis_kelias(branduolys_VALUE,(String)Nustatymai.get("builder")),Collections.emptyList(),환경);
            Files.writeString(kompiliuoti_žymeklis,šaltinis_maiša + "\n");
        }
        List<String> 추가인수 = new ArrayList<>(Arrays.asList(Argumentai).subList(1,Argumentai.length));
        if (Veiksmas.equals("run") || Veiksmas.equals("desktop")) {
            if (Veiksmas.equals("desktop")) 추가인수.add(0,"--desktop");
            호출(branduolys_VALUE,vidinis_kelias(branduolys_VALUE,(String)Nustatymai.get("runner")),추가인수,환경);
        } else if (Veiksmas.equals("image")) 호출(branduolys_VALUE,vidinis_kelias(branduolys_VALUE,(String)Nustatymai.get("image_builder")),추가인수,환경);
        else if (Veiksmas.equals("test-system")) {
            추가인수.add(0,Project_šaknis.toString()); 추가인수.add(0,"--edition");
            호출(branduolys_VALUE,vidinis_kelias(branduolys_VALUE,(String)Nustatymai.get("system_tester")),추가인수,환경);
        }
    }
}
