// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.security.MessageDigest;
import java.util.*;

/** 독립 국가판의 의존성 검사·복원·kääntää_Järjestelmä·실행을 맡는 isäntä Java työkalut. */
public final class country_sovellusvalikko {
    static final class data_jäsennin {
        final String lähdetiedosto; int paikka;
        data_jäsennin(String teksti) { lähdetiedosto = teksti; }
        void 빈칸() { while (paikka < lähdetiedosto.length() && Character.isWhitespace(lähdetiedosto.charAt(paikka))) paikka++; }
        Object Luku() {
            빈칸(); char merkki_ARVO = lähdetiedosto.charAt(paikka++);
            if (merkki_ARVO == '{') {
                Map<String,Object> TULOS = new LinkedHashMap<>(); 빈칸();
                if (lähdetiedosto.charAt(paikka) == '}') { paikka++; return TULOS; }
                while (true) {
                    String Nimi = (String)Luku(); 빈칸(); if (lähdetiedosto.charAt(paikka++) != ':') throw new IllegalArgumentException("data erotin_ARVO_d8ba4873 VIRHE");
                    TULOS.put(Nimi, Luku()); 빈칸(); char erotin_ARVO_d8ba4873 = lähdetiedosto.charAt(paikka++);
                    if (erotin_ARVO_d8ba4873 == '}') return TULOS; if (erotin_ARVO_d8ba4873 != ',') throw new IllegalArgumentException("data erotin_ARVO_d8ba4873 VIRHE");
                }
            }
            if (merkki_ARVO == '[') {
                List<Object> TULOS = new ArrayList<>(); 빈칸();
                if (lähdetiedosto.charAt(paikka) == ']') { paikka++; return TULOS; }
                while (true) {
                    TULOS.add(Luku()); 빈칸(); char erotin_ARVO_d8ba4873 = lähdetiedosto.charAt(paikka++);
                    if (erotin_ARVO_d8ba4873 == ']') return TULOS; if (erotin_ARVO_d8ba4873 != ',') throw new IllegalArgumentException("data erotin_ARVO_d8ba4873 VIRHE");
                }
            }
            if (merkki_ARVO == '"') {
                StringBuilder TULOS = new StringBuilder();
                while (true) {
                    char Seuraava_kohde = lähdetiedosto.charAt(paikka++); if (Seuraava_kohde == '"') return TULOS.toString();
                    if (Seuraava_kohde == '\\') {
                        Seuraava_kohde = lähdetiedosto.charAt(paikka++);
                        if (Seuraava_kohde == 'u') { TULOS.append((char)Integer.parseInt(lähdetiedosto.substring(paikka, paikka + 4),16)); paikka += 4; continue; }
                        if (Seuraava_kohde == 'n') Seuraava_kohde = '\n'; else if (Seuraava_kohde == 'r') Seuraava_kohde = '\r'; else if (Seuraava_kohde == 't') Seuraava_kohde = '\t';
                        else if (Seuraava_kohde == 'b') Seuraava_kohde = '\b'; else if (Seuraava_kohde == 'f') Seuraava_kohde = '\f';
                        else if (Seuraava_kohde != '"' && Seuraava_kohde != '\\' && Seuraava_kohde != '/') throw new IllegalArgumentException("문자 이스케이프 VIRHE");
                    }
                    TULOS.append(Seuraava_kohde);
                }
            }
            int Suorita_2 = paikka - 1;
            while (paikka < lähdetiedosto.length() && ",]} \t\r\n".indexOf(lähdetiedosto.charAt(paikka)) < 0) paikka++;
            String ARVO = lähdetiedosto.substring(Suorita_2, paikka);
            if (ARVO.equals("true")) return Boolean.TRUE; if (ARVO.equals("false")) return Boolean.FALSE; if (ARVO.equals("null")) return null;
            return Double.valueOf(ARVO);
        }
    }
    static String hajautusarvo_Tiedosto(Path polku_2) throws Exception {
        MessageDigest 계산 = MessageDigest.getInstance("SHA-256"); byte[] data = new byte[1024 * 1024];
        try (InputStream syöte_ARVO = Files.newInputStream(polku_2)) { for (int kesto_ARVO; (kesto_ARVO = syöte_ARVO.read(data)) >= 0;) 계산.update(data,0,kesto_ARVO); }
        return hajautusarvo_SMS(계산.digest());
    }
    static String hajautusarvo_SMS(byte[] data) {
        StringBuilder teksti = new StringBuilder(); for (byte ARVO : data) teksti.append(String.format(Locale.ROOT,"%02x",ARVO & 255)); return teksti.toString();
    }
    static Path sisäinen_polku(Path aloite_juuri, String Nimi) {
        Path TULOS = aloite_juuri.resolve(Nimi).normalize();
        if (Nimi.isEmpty() || Paths.get(Nimi).isAbsolute() || !TULOS.startsWith(aloite_juuri) || Nimi.indexOf('\\') >= 0)
            throw new IllegalArgumentException("범위를 벗어난 polku_2: " + Nimi);
        for (Path 부분 : Paths.get(Nimi)) if (부분.toString().equals("..")) throw new IllegalArgumentException("상위 polku_2 금지: " + Nimi);
        for (Path nykyinen_kohde = TULOS; nykyinen_kohde != null && nykyinen_kohde.startsWith(aloite_juuri); nykyinen_kohde = nykyinen_kohde.getParent())
            if (Files.isSymbolicLink(nykyinen_kohde)) throw new IllegalArgumentException("의존성 경로의 링크 금지: " + Nimi);
        return TULOS;
    }
    static String komento_tulos(List<String> komento) throws Exception {
        Process prosessi_ARVO = new ProcessBuilder(komento).redirectError(ProcessBuilder.Redirect.INHERIT).start();
        String TULOS = new String(prosessi_ARVO.getInputStream().readAllBytes(),StandardCharsets.UTF_8);
        if (prosessi_ARVO.waitFor() != 0) throw new IOException("komento virhe_ARVO: " + komento.get(0)); return TULOS;
    }
    static void purkaa(Path Arkisto_ARVO, Path kohde_ARVO) throws Exception {
        for (String Nimi : komento_tulos(Arrays.asList("tar","-tzf",Arkisto_ARVO.toString())).split("\n")) sisäinen_polku(kohde_ARVO, Nimi);
        for (String syöterivi : komento_tulos(Arrays.asList("tar","-tvzf",Arkisto_ARVO.toString())).split("\n"))
            if (!syöterivi.isEmpty() && syöterivi.charAt(0) != '-' && syöterivi.charAt(0) != 'd') throw new IOException("ulkoinen_ARVO 링크 또는 특수 파일을 포함한 의존성");
        Files.createDirectories(kohde_ARVO);
        int Tila_ARVO = new ProcessBuilder("tar","--no-same-owner","--no-same-permissions","-xzf",Arkisto_ARVO.toString(),"-C",kohde_ARVO.toString()).inheritIO().start().waitFor();
        if (Tila_ARVO != 0) throw new IOException("의존성 Arkisto_ARVO julkaista_Tallennus virhe_ARVO");
    }
    static void 호출(Path 작업경로, Path työkalut, List<String> argumentit, Map<String,String> ympäristö) throws Exception {
        List<String> komento = new ArrayList<>(Arrays.asList("python3", työkalut.toString())); komento.addAll(argumentit);
        ProcessBuilder Suorita_komento = new ProcessBuilder(komento).directory(작업경로.toFile()).inheritIO(); Suorita_komento.environment().putAll(ympäristö);
        int Tila_ARVO = Suorita_komento.start().waitFor(); if (Tila_ARVO != 0) throw new IOException("työkalut virhe_ARVO: " + työkalut + " (" + Tila_ARVO + ")");
    }
    @SuppressWarnings("unchecked")
    public static void main(String[] argumentit) throws Exception {
        if (argumentit.length < 1) throw new IllegalArgumentException("build, run, desktop, image, check, test-system 중 동작을 지정하세요");
        String Toiminto = argumentit[0];
        if (!Arrays.asList("build","run","desktop","image","check","test-system").contains(Toiminto)) throw new IllegalArgumentException("알 numero 없는 Toiminto");
        Path aloite_juuri = Paths.get(System.getProperty("worldos.edition.root")).toAbsolutePath().normalize();
        Map<String,Object> Asetukset = (Map<String,Object>)new data_jäsennin(Files.readString(aloite_juuri.resolve("native.json"),StandardCharsets.UTF_8)).Luku();
        Path lähde_puu = sisäinen_polku(aloite_juuri,(String)Asetukset.get("source")), ydin_ARVO = sisäinen_polku(lähde_puu,(String)Asetukset.get("native"));
        List<String> 소유파일들 = (List<String>)(List<?>)Asetukset.get("owned_files");
        for (String Nimi : 소유파일들) if (!Files.isRegularFile(sisäinen_polku(lähde_puu,Nimi))) throw new IOException("lähde_puu 없음: " + Nimi);
        if (Toiminto.equals("check")) { System.out.println(Asetukset.get("country") + " " + Asetukset.get("language") + " 독립 lähde_puu tarkistaa 완료"); return; }
        String resurssi_suhteellinen_polku = (String)Asetukset.getOrDefault("resource_root", ".");
        if (!resurssi_suhteellinen_polku.equals(".") && !resurssi_suhteellinen_polku.equals("..")) throw new IllegalArgumentException("의존성 aloite_juuri polku_2 VIRHE");
        Path resurssi_ARVO = aloite_juuri.resolve(resurssi_suhteellinen_polku).normalize(); Path Arkisto_ARVO = resurssi_ARVO.resolve("native-vendor.tar.gz");
        String 기대해시 = (String)Asetukset.get("vendor_sha256");
        if (!hajautusarvo_Tiedosto(Arkisto_ARVO).equals(기대해시)) throw new IOException("의존성 SHA-256 불일치");
        Path merkintä_ARVO = lähde_puu.resolve(".vendor-sha256");
        if (!Files.isRegularFile(merkintä_ARVO) || !Files.readString(merkintä_ARVO).trim().equals(기대해시)) { purkaa(Arkisto_ARVO, lähde_puu); Files.writeString(merkintä_ARVO,기대해시 + "\n"); }
        Map<String,String> ympäristö = new HashMap<>(System.getenv());
        Path ipConfig = null;
        if (ympäristö.containsKey("IP_CONFIG")) ipConfig = Paths.get(ympäristö.get("IP_CONFIG")).toAbsolutePath().normalize();
        else for (Path parent = aloite_juuri; parent != null; parent = parent.getParent()) {
            if (Files.isRegularFile(parent.resolve("ip.conf"))) { ipConfig = parent.resolve("ip.conf"); break; }
        }
        if (ipConfig == null) ipConfig = lähde_puu.resolve("ip.conf");
        if (!Files.isRegularFile(ipConfig)) throw new IOException("Missing ip.conf: " + ipConfig);
        ympäristö.put("IP_CONFIG", ipConfig.toString());
        if (Arrays.asList("run","desktop","test-system").contains(Toiminto) && !ympäristö.containsKey("QEMU_AARCH64")) {
            Path ohjelma_sovellusvalikko = resurssi_ARVO.resolve("host/qemu"), sovellusvalikko_merkintä = resurssi_ARVO.resolve("host/.qemu-sha256");
            String sovellusvalikko_hajautusarvo = (String)Asetukset.get("qemu_sha256");
            if (!Files.isRegularFile(ohjelma_sovellusvalikko) || !Files.isRegularFile(sovellusvalikko_merkintä) || !Files.readString(sovellusvalikko_merkintä).trim().equals(sovellusvalikko_hajautusarvo)) {
                Path sovellusvalikko_Arkisto = resurssi_ARVO.resolve("qemu-host.tar.gz"); if (!hajautusarvo_Tiedosto(sovellusvalikko_Arkisto).equals(sovellusvalikko_hajautusarvo)) throw new IOException("QEMU SHA-256 불일치");
                purkaa(sovellusvalikko_Arkisto,resurssi_ARVO.resolve("host")); Files.writeString(sovellusvalikko_merkintä,sovellusvalikko_hajautusarvo + "\n");
            }
            ympäristö.put("QEMU_AARCH64",ohjelma_sovellusvalikko.toString());
        }
        MessageDigest 계산 = MessageDigest.getInstance("SHA-256"); Collections.sort(소유파일들);
        for (String Nimi : 소유파일들) { 계산.update(Nimi.getBytes(StandardCharsets.UTF_8)); 계산.update(Files.readAllBytes(sisäinen_polku(lähde_puu,Nimi))); }
        계산.update("ip.conf\0".getBytes(StandardCharsets.UTF_8)); 계산.update(Files.readAllBytes(ipConfig));
        String lähde_hajautusarvo = hajautusarvo_SMS(계산.digest()); Path kääntää_merkintä = ydin_ARVO.resolve("build/worldos-source.sha256");
        if (Toiminto.equals("build") || !Files.isRegularFile(kääntää_merkintä) || !Files.readString(kääntää_merkintä).trim().equals(lähde_hajautusarvo)) {
            호출(ydin_ARVO,sisäinen_polku(ydin_ARVO,(String)Asetukset.get("builder")),Collections.emptyList(),ympäristö);
            Files.writeString(kääntää_merkintä,lähde_hajautusarvo + "\n");
        }
        List<String> 추가인수 = new ArrayList<>(Arrays.asList(argumentit).subList(1,argumentit.length));
        if (Toiminto.equals("run") || Toiminto.equals("desktop")) {
            if (Toiminto.equals("desktop")) 추가인수.add(0,"--desktop");
            호출(ydin_ARVO,sisäinen_polku(ydin_ARVO,(String)Asetukset.get("runner")),추가인수,ympäristö);
        } else if (Toiminto.equals("image")) 호출(ydin_ARVO,sisäinen_polku(ydin_ARVO,(String)Asetukset.get("image_builder")),추가인수,ympäristö);
        else if (Toiminto.equals("test-system")) {
            추가인수.add(0,aloite_juuri.toString()); 추가인수.add(0,"--edition");
            호출(ydin_ARVO,sisäinen_polku(ydin_ARVO,(String)Asetukset.get("system_tester")),추가인수,ympäristö);
        }
    }
}
