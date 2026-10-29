// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.security.MessageDigest;
import java.util.*;

/** 독립 국가판의 의존성 검사·복원·generare_sistem·실행을 맡는 gazdă Java Instrumente. */
public final class Country_ecrane_de_lansare {
    static final class date_parser {
        final String SURSĂ; int Poziție;
        date_parser(String SMS) { SURSĂ = SMS; }
        void 빈칸() { while (Poziție < SURSĂ.length() && Character.isWhitespace(SURSĂ.charAt(Poziție))) Poziție++; }
        Object Citire() {
            빈칸(); char caracter_VALUE = SURSĂ.charAt(Poziție++);
            if (caracter_VALUE == '{') {
                Map<String,Object> KR = new LinkedHashMap<>(); 빈칸();
                if (SURSĂ.charAt(Poziție) == '}') { Poziție++; return KR; }
                while (true) {
                    String Nume = (String)Citire(); 빈칸(); if (SURSĂ.charAt(Poziție++) != ':') throw new IllegalArgumentException("date delimitator_VALUE eroare");
                    KR.put(Nume, Citire()); 빈칸(); char delimitator_VALUE = SURSĂ.charAt(Poziție++);
                    if (delimitator_VALUE == '}') return KR; if (delimitator_VALUE != ',') throw new IllegalArgumentException("date delimitator_VALUE eroare");
                }
            }
            if (caracter_VALUE == '[') {
                List<Object> KR = new ArrayList<>(); 빈칸();
                if (SURSĂ.charAt(Poziție) == ']') { Poziție++; return KR; }
                while (true) {
                    KR.add(Citire()); 빈칸(); char delimitator_VALUE = SURSĂ.charAt(Poziție++);
                    if (delimitator_VALUE == ']') return KR; if (delimitator_VALUE != ',') throw new IllegalArgumentException("date delimitator_VALUE eroare");
                }
            }
            if (caracter_VALUE == '"') {
                StringBuilder KR = new StringBuilder();
                while (true) {
                    char Următorul_element = SURSĂ.charAt(Poziție++); if (Următorul_element == '"') return KR.toString();
                    if (Următorul_element == '\\') {
                        Următorul_element = SURSĂ.charAt(Poziție++);
                        if (Următorul_element == 'u') { KR.append((char)Integer.parseInt(SURSĂ.substring(Poziție, Poziție + 4),16)); Poziție += 4; continue; }
                        if (Următorul_element == 'n') Următorul_element = '\n'; else if (Următorul_element == 'r') Următorul_element = '\r'; else if (Următorul_element == 't') Următorul_element = '\t';
                        else if (Următorul_element == 'b') Următorul_element = '\b'; else if (Următorul_element == 'f') Următorul_element = '\f';
                        else if (Următorul_element != '"' && Următorul_element != '\\' && Următorul_element != '/') throw new IllegalArgumentException("문자 이스케이프 eroare");
                    }
                    KR.append(Următorul_element);
                }
            }
            int Pornește = Poziție - 1;
            while (Poziție < SURSĂ.length() && ",]} \t\r\n".indexOf(SURSĂ.charAt(Poziție)) < 0) Poziție++;
            String VALUE = SURSĂ.substring(Pornește, Poziție);
            if (VALUE.equals("true")) return Boolean.TRUE; if (VALUE.equals("false")) return Boolean.FALSE; if (VALUE.equals("null")) return null;
            return Double.valueOf(VALUE);
        }
    }
    static String cod_hash_Fișier(Path Cale) throws Exception {
        MessageDigest 계산 = MessageDigest.getInstance("SHA-256"); byte[] date = new byte[1024 * 1024];
        try (InputStream 입력 = Files.newInputStream(Cale)) { for (int lungime_VALUE; (lungime_VALUE = 입력.read(date)) >= 0;) 계산.update(date,0,lungime_VALUE); }
        return cod_hash_SMS(계산.digest());
    }
    static String cod_hash_SMS(byte[] date) {
        StringBuilder SMS = new StringBuilder(); for (byte VALUE : date) SMS.append(String.format(Locale.ROOT,"%02x",VALUE & 255)); return SMS.toString();
    }
    static Path intern_cale(Path Project_rădăcină, String Nume) {
        Path KR = Project_rădăcină.resolve(Nume).normalize();
        if (Nume.isEmpty() || Paths.get(Nume).isAbsolute() || !KR.startsWith(Project_rădăcină) || Nume.indexOf('\\') >= 0)
            throw new IllegalArgumentException("범위를 벗어난 Cale: " + Nume);
        for (Path 부분 : Paths.get(Nume)) if (부분.toString().equals("..")) throw new IllegalArgumentException("상위 Cale 금지: " + Nume);
        for (Path curent_element = KR; curent_element != null && curent_element.startsWith(Project_rădăcină); curent_element = curent_element.getParent())
            if (Files.isSymbolicLink(curent_element)) throw new IllegalArgumentException("의존성 경로의 링크 금지: " + Nume);
        return KR;
    }
    static String 명령출력(List<String> Comandă) throws Exception {
        Process Proces_VALUE = new ProcessBuilder(Comandă).redirectError(ProcessBuilder.Redirect.INHERIT).start();
        String KR = new String(Proces_VALUE.getInputStream().readAllBytes(),StandardCharsets.UTF_8);
        if (Proces_VALUE.waitFor() != 0) throw new IOException("Comandă eroare_VALUE: " + Comandă.get(0)); return KR;
    }
    static void extrage(Path Arhivă_VALUE, Path destinație_VALUE) throws Exception {
        for (String Nume : 명령출력(Arrays.asList("tar","-tzf",Arhivă_VALUE.toString())).split("\n")) intern_cale(destinație_VALUE, Nume);
        for (String Linie : 명령출력(Arrays.asList("tar","-tvzf",Arhivă_VALUE.toString())).split("\n"))
            if (!Linie.isEmpty() && Linie.charAt(0) != '-' && Linie.charAt(0) != 'd') throw new IOException("extern_VALUE 링크 또는 특수 파일을 포함한 의존성");
        Files.createDirectories(destinație_VALUE);
        int Stare_VALUE = new ProcessBuilder("tar","--no-same-owner","--no-same-permissions","-xzf",Arhivă_VALUE.toString(),"-C",destinație_VALUE.toString()).inheritIO().start().waitFor();
        if (Stare_VALUE != 0) throw new IOException("의존성 Arhivă_VALUE lansa_Stocare eroare_VALUE");
    }
    static void 호출(Path 작업경로, Path Instrumente, List<String> Argumente, Map<String,String> 환경) throws Exception {
        List<String> Comandă = new ArrayList<>(Arrays.asList("python3", Instrumente.toString())); Comandă.addAll(Argumente);
        ProcessBuilder executa_comandă = new ProcessBuilder(Comandă).directory(작업경로.toFile()).inheritIO(); executa_comandă.environment().putAll(환경);
        int Stare_VALUE = executa_comandă.start().waitFor(); if (Stare_VALUE != 0) throw new IOException("Instrumente eroare_VALUE: " + Instrumente + " (" + Stare_VALUE + ")");
    }
    @SuppressWarnings("unchecked")
    public static void main(String[] Argumente) throws Exception {
        if (Argumente.length < 1) throw new IllegalArgumentException("build, run, desktop, image, check, test-system 중 동작을 지정하세요");
        String Acțiuni = Argumente[0];
        if (!Arrays.asList("build","run","desktop","image","check","test-system").contains(Acțiuni)) throw new IllegalArgumentException("알 수 없는 Acțiuni");
        Path Project_rădăcină = Paths.get(System.getProperty("worldos.edition.root")).toAbsolutePath().normalize();
        Map<String,Object> Setări = (Map<String,Object>)new date_parser(Files.readString(Project_rădăcină.resolve("native.json"),StandardCharsets.UTF_8)).Citire();
        Path sursă_arborescență = intern_cale(Project_rădăcină,(String)Setări.get("source")), nucleu_VALUE = intern_cale(sursă_arborescență,(String)Setări.get("native"));
        List<String> 소유파일들 = (List<String>)(List<?>)Setări.get("owned_files");
        for (String Nume : 소유파일들) if (!Files.isRegularFile(intern_cale(sursă_arborescență,Nume))) throw new IOException("sursă_arborescență 없음: " + Nume);
        if (Acțiuni.equals("check")) { System.out.println(Setări.get("country") + " " + Setări.get("language") + " 독립 sursă_arborescență verifica 완료"); return; }
        String resursă_cale_relativă = (String)Setări.getOrDefault("resource_root", ".");
        if (!resursă_cale_relativă.equals(".") && !resursă_cale_relativă.equals("..")) throw new IllegalArgumentException("의존성 Project_rădăcină Cale eroare");
        Path resursă_VALUE = Project_rădăcină.resolve(resursă_cale_relativă).normalize(); Path Arhivă_VALUE = resursă_VALUE.resolve("native-vendor.tar.gz");
        String 기대해시 = (String)Setări.get("vendor_sha256");
        if (!cod_hash_Fișier(Arhivă_VALUE).equals(기대해시)) throw new IOException("의존성 SHA-256 불일치");
        Path marcaj_VALUE = sursă_arborescență.resolve(".vendor-sha256");
        if (!Files.isRegularFile(marcaj_VALUE) || !Files.readString(marcaj_VALUE).trim().equals(기대해시)) { extrage(Arhivă_VALUE, sursă_arborescență); Files.writeString(marcaj_VALUE,기대해시 + "\n"); }
        Map<String,String> 환경 = new HashMap<>(System.getenv());
        Path ipConfig = null;
        if (환경.containsKey("IP_CONFIG")) ipConfig = Paths.get(환경.get("IP_CONFIG")).toAbsolutePath().normalize();
        else for (Path parent = Project_rădăcină; parent != null; parent = parent.getParent()) {
            if (Files.isRegularFile(parent.resolve("ip.conf"))) { ipConfig = parent.resolve("ip.conf"); break; }
        }
        if (ipConfig == null) ipConfig = sursă_arborescență.resolve("ip.conf");
        if (!Files.isRegularFile(ipConfig)) throw new IOException("Missing ip.conf: " + ipConfig);
        환경.put("IP_CONFIG", ipConfig.toString());
        if (Arrays.asList("run","desktop","test-system").contains(Acțiuni) && !환경.containsKey("QEMU_AARCH64")) {
            Path program_ecrane_de_lansare = resursă_VALUE.resolve("host/qemu"), ecrane_de_lansare_marcaj = resursă_VALUE.resolve("host/.qemu-sha256");
            String ecrane_de_lansare_cod_hash = (String)Setări.get("qemu_sha256");
            if (!Files.isRegularFile(program_ecrane_de_lansare) || !Files.isRegularFile(ecrane_de_lansare_marcaj) || !Files.readString(ecrane_de_lansare_marcaj).trim().equals(ecrane_de_lansare_cod_hash)) {
                Path ecrane_de_lansare_Arhivă = resursă_VALUE.resolve("qemu-host.tar.gz"); if (!cod_hash_Fișier(ecrane_de_lansare_Arhivă).equals(ecrane_de_lansare_cod_hash)) throw new IOException("QEMU SHA-256 불일치");
                extrage(ecrane_de_lansare_Arhivă,resursă_VALUE.resolve("host")); Files.writeString(ecrane_de_lansare_marcaj,ecrane_de_lansare_cod_hash + "\n");
            }
            환경.put("QEMU_AARCH64",program_ecrane_de_lansare.toString());
        }
        MessageDigest 계산 = MessageDigest.getInstance("SHA-256"); Collections.sort(소유파일들);
        for (String Nume : 소유파일들) { 계산.update(Nume.getBytes(StandardCharsets.UTF_8)); 계산.update(Files.readAllBytes(intern_cale(sursă_arborescență,Nume))); }
        계산.update("ip.conf\0".getBytes(StandardCharsets.UTF_8)); 계산.update(Files.readAllBytes(ipConfig));
        String sursă_cod_hash = cod_hash_SMS(계산.digest()); Path generare_marcaj = nucleu_VALUE.resolve("build/worldos-source.sha256");
        if (Acțiuni.equals("build") || !Files.isRegularFile(generare_marcaj) || !Files.readString(generare_marcaj).trim().equals(sursă_cod_hash)) {
            호출(nucleu_VALUE,intern_cale(nucleu_VALUE,(String)Setări.get("builder")),Collections.emptyList(),환경);
            Files.writeString(generare_marcaj,sursă_cod_hash + "\n");
        }
        List<String> 추가인수 = new ArrayList<>(Arrays.asList(Argumente).subList(1,Argumente.length));
        if (Acțiuni.equals("run") || Acțiuni.equals("desktop")) {
            if (Acțiuni.equals("desktop")) 추가인수.add(0,"--desktop");
            호출(nucleu_VALUE,intern_cale(nucleu_VALUE,(String)Setări.get("runner")),추가인수,환경);
        } else if (Acțiuni.equals("image")) 호출(nucleu_VALUE,intern_cale(nucleu_VALUE,(String)Setări.get("image_builder")),추가인수,환경);
        else if (Acțiuni.equals("test-system")) {
            추가인수.add(0,Project_rădăcină.toString()); 추가인수.add(0,"--edition");
            호출(nucleu_VALUE,intern_cale(nucleu_VALUE,(String)Setări.get("system_tester")),추가인수,환경);
        }
    }
}
