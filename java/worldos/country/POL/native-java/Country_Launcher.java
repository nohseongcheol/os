// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.security.MessageDigest;
import java.util.*;

/** 독립 국가판의 의존성 검사·복원·BLD_System·실행을 맡는 host Java narzędzia. */
public final class Country_Launcher {
    static final class dane_parser {
        final String plik_źródłowy; int pozycja;
        dane_parser(String tekst) { plik_źródłowy = tekst; }
        void 빈칸() { while (pozycja < plik_źródłowy.length() && Character.isWhitespace(plik_źródłowy.charAt(pozycja))) pozycja++; }
        Object Odczyt() {
            빈칸(); char znak_WARTOŚĆ = plik_źródłowy.charAt(pozycja++);
            if (znak_WARTOŚĆ == '{') {
                Map<String,Object> WYNIK = new LinkedHashMap<>(); 빈칸();
                if (plik_źródłowy.charAt(pozycja) == '}') { pozycja++; return WYNIK; }
                while (true) {
                    String Nazwa = (String)Odczyt(); 빈칸(); if (plik_źródłowy.charAt(pozycja++) != ':') throw new IllegalArgumentException("dane ogranicznik_WARTOŚĆ błąd");
                    WYNIK.put(Nazwa, Odczyt()); 빈칸(); char ogranicznik_WARTOŚĆ = plik_źródłowy.charAt(pozycja++);
                    if (ogranicznik_WARTOŚĆ == '}') return WYNIK; if (ogranicznik_WARTOŚĆ != ',') throw new IllegalArgumentException("dane ogranicznik_WARTOŚĆ błąd");
                }
            }
            if (znak_WARTOŚĆ == '[') {
                List<Object> WYNIK = new ArrayList<>(); 빈칸();
                if (plik_źródłowy.charAt(pozycja) == ']') { pozycja++; return WYNIK; }
                while (true) {
                    WYNIK.add(Odczyt()); 빈칸(); char ogranicznik_WARTOŚĆ = plik_źródłowy.charAt(pozycja++);
                    if (ogranicznik_WARTOŚĆ == ']') return WYNIK; if (ogranicznik_WARTOŚĆ != ',') throw new IllegalArgumentException("dane ogranicznik_WARTOŚĆ błąd");
                }
            }
            if (znak_WARTOŚĆ == '"') {
                StringBuilder WYNIK = new StringBuilder();
                while (true) {
                    char Dalej_towar = plik_źródłowy.charAt(pozycja++); if (Dalej_towar == '"') return WYNIK.toString();
                    if (Dalej_towar == '\\') {
                        Dalej_towar = plik_źródłowy.charAt(pozycja++);
                        if (Dalej_towar == 'u') { WYNIK.append((char)Integer.parseInt(plik_źródłowy.substring(pozycja, pozycja + 4),16)); pozycja += 4; continue; }
                        if (Dalej_towar == 'n') Dalej_towar = '\n'; else if (Dalej_towar == 'r') Dalej_towar = '\r'; else if (Dalej_towar == 't') Dalej_towar = '\t';
                        else if (Dalej_towar == 'b') Dalej_towar = '\b'; else if (Dalej_towar == 'f') Dalej_towar = '\f';
                        else if (Dalej_towar != '"' && Dalej_towar != '\\' && Dalej_towar != '/') throw new IllegalArgumentException("문자 이스케이프 błąd");
                    }
                    WYNIK.append(Dalej_towar);
                }
            }
            int Uruchom_2 = pozycja - 1;
            while (pozycja < plik_źródłowy.length() && ",]} \t\r\n".indexOf(plik_źródłowy.charAt(pozycja)) < 0) pozycja++;
            String WARTOŚĆ = plik_źródłowy.substring(Uruchom_2, pozycja);
            if (WARTOŚĆ.equals("true")) return Boolean.TRUE; if (WARTOŚĆ.equals("false")) return Boolean.FALSE; if (WARTOŚĆ.equals("null")) return null;
            return Double.valueOf(WARTOŚĆ);
        }
    }
    static String skrót_Plik(Path ścieżka_2) throws Exception {
        MessageDigest 계산 = MessageDigest.getInstance("SHA-256"); byte[] dane = new byte[1024 * 1024];
        try (InputStream wejście_WARTOŚĆ = Files.newInputStream(ścieżka_2)) { for (int długość_WARTOŚĆ; (długość_WARTOŚĆ = wejście_WARTOŚĆ.read(dane)) >= 0;) 계산.update(dane,0,długość_WARTOŚĆ); }
        return skrót_SMS(계산.digest());
    }
    static String skrót_SMS(byte[] dane) {
        StringBuilder tekst = new StringBuilder(); for (byte WARTOŚĆ : dane) tekst.append(String.format(Locale.ROOT,"%02x",WARTOŚĆ & 255)); return tekst.toString();
    }
    static Path wewnętrzny_ścieżka(Path Project_korzeń, String Nazwa) {
        Path WYNIK = Project_korzeń.resolve(Nazwa).normalize();
        if (Nazwa.isEmpty() || Paths.get(Nazwa).isAbsolute() || !WYNIK.startsWith(Project_korzeń) || Nazwa.indexOf('\\') >= 0)
            throw new IllegalArgumentException("범위를 벗어난 ścieżka_2: " + Nazwa);
        for (Path 부분 : Paths.get(Nazwa)) if (부분.toString().equals("..")) throw new IllegalArgumentException("상위 ścieżka_2 금지: " + Nazwa);
        for (Path bieżący_towar = WYNIK; bieżący_towar != null && bieżący_towar.startsWith(Project_korzeń); bieżący_towar = bieżący_towar.getParent())
            if (Files.isSymbolicLink(bieżący_towar)) throw new IllegalArgumentException("의존성 경로의 링크 금지: " + Nazwa);
        return WYNIK;
    }
    static String polecenie_produkt_wyjściowy(List<String> polecenie) throws Exception {
        Process Proces_WARTOŚĆ = new ProcessBuilder(polecenie).redirectError(ProcessBuilder.Redirect.INHERIT).start();
        String WYNIK = new String(Proces_WARTOŚĆ.getInputStream().readAllBytes(),StandardCharsets.UTF_8);
        if (Proces_WARTOŚĆ.waitFor() != 0) throw new IOException("polecenie awaria_WARTOŚĆ: " + polecenie.get(0)); return WYNIK;
    }
    static void wyodrębnić(Path Archiwum_WARTOŚĆ, Path cel_WARTOŚĆ) throws Exception {
        for (String Nazwa : polecenie_produkt_wyjściowy(Arrays.asList("tar","-tzf",Archiwum_WARTOŚĆ.toString())).split("\n")) wewnętrzny_ścieżka(cel_WARTOŚĆ, Nazwa);
        for (String wiersz_wejścia : polecenie_produkt_wyjściowy(Arrays.asList("tar","-tvzf",Archiwum_WARTOŚĆ.toString())).split("\n"))
            if (!wiersz_wejścia.isEmpty() && wiersz_wejścia.charAt(0) != '-' && wiersz_wejścia.charAt(0) != 'd') throw new IOException("zewnętrzny_WARTOŚĆ 링크 또는 특수 파일을 포함한 의존성");
        Files.createDirectories(cel_WARTOŚĆ);
        int Stan_WARTOŚĆ = new ProcessBuilder("tar","--no-same-owner","--no-same-permissions","-xzf",Archiwum_WARTOŚĆ.toString(),"-C",cel_WARTOŚĆ.toString()).inheritIO().start().waitFor();
        if (Stan_WARTOŚĆ != 0) throw new IOException("의존성 Archiwum_WARTOŚĆ wersja_Pamięć awaria_WARTOŚĆ");
    }
    static void 호출(Path 작업경로, Path narzędzia, List<String> argumenty, Map<String,String> środowisko) throws Exception {
        List<String> polecenie = new ArrayList<>(Arrays.asList("python3", narzędzia.toString())); polecenie.addAll(argumenty);
        ProcessBuilder Wykonaj_polecenie = new ProcessBuilder(polecenie).directory(작업경로.toFile()).inheritIO(); Wykonaj_polecenie.environment().putAll(środowisko);
        int Stan_WARTOŚĆ = Wykonaj_polecenie.start().waitFor(); if (Stan_WARTOŚĆ != 0) throw new IOException("narzędzia awaria_WARTOŚĆ: " + narzędzia + " (" + Stan_WARTOŚĆ + ")");
    }
    @SuppressWarnings("unchecked")
    public static void main(String[] argumenty) throws Exception {
        if (argumenty.length < 1) throw new IllegalArgumentException("build, run, desktop, image, check, test-system 중 동작을 지정하세요");
        String Akcja = argumenty[0];
        if (!Arrays.asList("build","run","desktop","image","check","test-system").contains(Akcja)) throw new IllegalArgumentException("알 identyfikator 없는 Akcja");
        Path Project_korzeń = Paths.get(System.getProperty("worldos.edition.root")).toAbsolutePath().normalize();
        Map<String,Object> Ustawienia = (Map<String,Object>)new dane_parser(Files.readString(Project_korzeń.resolve("native.json"),StandardCharsets.UTF_8)).Odczyt();
        Path źródło_drzewo = wewnętrzny_ścieżka(Project_korzeń,(String)Ustawienia.get("source")), jądro_WARTOŚĆ = wewnętrzny_ścieżka(źródło_drzewo,(String)Ustawienia.get("native"));
        List<String> 소유파일들 = (List<String>)(List<?>)Ustawienia.get("owned_files");
        for (String Nazwa : 소유파일들) if (!Files.isRegularFile(wewnętrzny_ścieżka(źródło_drzewo,Nazwa))) throw new IOException("źródło_drzewo 없음: " + Nazwa);
        if (Akcja.equals("check")) { System.out.println(Ustawienia.get("country") + " " + Ustawienia.get("language") + " 독립 źródło_drzewo 확인 완료"); return; }
        String zasób_ścieżka_względna = (String)Ustawienia.getOrDefault("resource_root", ".");
        if (!zasób_ścieżka_względna.equals(".") && !zasób_ścieżka_względna.equals("..")) throw new IllegalArgumentException("의존성 Project_korzeń ścieżka_2 błąd");
        Path zasób_WARTOŚĆ = Project_korzeń.resolve(zasób_ścieżka_względna).normalize(); Path Archiwum_WARTOŚĆ = zasób_WARTOŚĆ.resolve("native-vendor.tar.gz");
        String 기대해시 = (String)Ustawienia.get("vendor_sha256");
        if (!skrót_Plik(Archiwum_WARTOŚĆ).equals(기대해시)) throw new IOException("의존성 SHA-256 불일치");
        Path pisak_WARTOŚĆ = źródło_drzewo.resolve(".vendor-sha256");
        if (!Files.isRegularFile(pisak_WARTOŚĆ) || !Files.readString(pisak_WARTOŚĆ).trim().equals(기대해시)) { wyodrębnić(Archiwum_WARTOŚĆ, źródło_drzewo); Files.writeString(pisak_WARTOŚĆ,기대해시 + "\n"); }
        Map<String,String> środowisko = new HashMap<>(System.getenv());
        Path ipConfig = null;
        if (środowisko.containsKey("IP_CONFIG")) ipConfig = Paths.get(środowisko.get("IP_CONFIG")).toAbsolutePath().normalize();
        else for (Path parent = Project_korzeń; parent != null; parent = parent.getParent()) {
            if (Files.isRegularFile(parent.resolve("ip.conf"))) { ipConfig = parent.resolve("ip.conf"); break; }
        }
        if (ipConfig == null) ipConfig = źródło_drzewo.resolve("ip.conf");
        if (!Files.isRegularFile(ipConfig)) throw new IOException("Missing ip.conf: " + ipConfig);
        środowisko.put("IP_CONFIG", ipConfig.toString());
        if (Arrays.asList("run","desktop","test-system").contains(Akcja) && !środowisko.containsKey("QEMU_AARCH64")) {
            Path program_Launcher = zasób_WARTOŚĆ.resolve("host/qemu"), Launcher_pisak = zasób_WARTOŚĆ.resolve("host/.qemu-sha256");
            String Launcher_skrót = (String)Ustawienia.get("qemu_sha256");
            if (!Files.isRegularFile(program_Launcher) || !Files.isRegularFile(Launcher_pisak) || !Files.readString(Launcher_pisak).trim().equals(Launcher_skrót)) {
                Path Launcher_Archiwum = zasób_WARTOŚĆ.resolve("qemu-host.tar.gz"); if (!skrót_Plik(Launcher_Archiwum).equals(Launcher_skrót)) throw new IOException("QEMU SHA-256 불일치");
                wyodrębnić(Launcher_Archiwum,zasób_WARTOŚĆ.resolve("host")); Files.writeString(Launcher_pisak,Launcher_skrót + "\n");
            }
            środowisko.put("QEMU_AARCH64",program_Launcher.toString());
        }
        MessageDigest 계산 = MessageDigest.getInstance("SHA-256"); Collections.sort(소유파일들);
        for (String Nazwa : 소유파일들) { 계산.update(Nazwa.getBytes(StandardCharsets.UTF_8)); 계산.update(Files.readAllBytes(wewnętrzny_ścieżka(źródło_drzewo,Nazwa))); }
        계산.update("ip.conf\0".getBytes(StandardCharsets.UTF_8)); 계산.update(Files.readAllBytes(ipConfig));
        String źródło_skrót = skrót_SMS(계산.digest()); Path BLD_pisak = jądro_WARTOŚĆ.resolve("build/worldos-source.sha256");
        if (Akcja.equals("build") || !Files.isRegularFile(BLD_pisak) || !Files.readString(BLD_pisak).trim().equals(źródło_skrót)) {
            호출(jądro_WARTOŚĆ,wewnętrzny_ścieżka(jądro_WARTOŚĆ,(String)Ustawienia.get("builder")),Collections.emptyList(),środowisko);
            Files.writeString(BLD_pisak,źródło_skrót + "\n");
        }
        List<String> 추가인수 = new ArrayList<>(Arrays.asList(argumenty).subList(1,argumenty.length));
        if (Akcja.equals("run") || Akcja.equals("desktop")) {
            if (Akcja.equals("desktop")) 추가인수.add(0,"--desktop");
            호출(jądro_WARTOŚĆ,wewnętrzny_ścieżka(jądro_WARTOŚĆ,(String)Ustawienia.get("runner")),추가인수,środowisko);
        } else if (Akcja.equals("image")) 호출(jądro_WARTOŚĆ,wewnętrzny_ścieżka(jądro_WARTOŚĆ,(String)Ustawienia.get("image_builder")),추가인수,środowisko);
        else if (Akcja.equals("test-system")) {
            추가인수.add(0,Project_korzeń.toString()); 추가인수.add(0,"--edition");
            호출(jądro_WARTOŚĆ,wewnętrzny_ścieżka(jądro_WARTOŚĆ,(String)Ustawienia.get("system_tester")),추가인수,środowisko);
        }
    }
}
