// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.security.MessageDigest;
import java.util.*;

/** 독립 국가판의 의존성 검사·복원·épít_Rendszer·실행을 맡는 gazda Java Eszközök. */
public final class Country_indító {
    static final class adat_elemző {
        final String FORRÁS; int Pozíció;
        adat_elemző(String Szöveg) { FORRÁS = Szöveg; }
        void 빈칸() { while (Pozíció < FORRÁS.length() && Character.isWhitespace(FORRÁS.charAt(Pozíció))) Pozíció++; }
        Object Olvasás() {
            빈칸(); char karakter_ÉRTÉK = FORRÁS.charAt(Pozíció++);
            if (karakter_ÉRTÉK == '{') {
                Map<String,Object> KR = new LinkedHashMap<>(); 빈칸();
                if (FORRÁS.charAt(Pozíció) == '}') { Pozíció++; return KR; }
                while (true) {
                    String Név = (String)Olvasás(); 빈칸(); if (FORRÁS.charAt(Pozíció++) != ':') throw new IllegalArgumentException("adat elválasztó_karakter_ÉRTÉK HIBA");
                    KR.put(Név, Olvasás()); 빈칸(); char elválasztó_karakter_ÉRTÉK = FORRÁS.charAt(Pozíció++);
                    if (elválasztó_karakter_ÉRTÉK == '}') return KR; if (elválasztó_karakter_ÉRTÉK != ',') throw new IllegalArgumentException("adat elválasztó_karakter_ÉRTÉK HIBA");
                }
            }
            if (karakter_ÉRTÉK == '[') {
                List<Object> KR = new ArrayList<>(); 빈칸();
                if (FORRÁS.charAt(Pozíció) == ']') { Pozíció++; return KR; }
                while (true) {
                    KR.add(Olvasás()); 빈칸(); char elválasztó_karakter_ÉRTÉK = FORRÁS.charAt(Pozíció++);
                    if (elválasztó_karakter_ÉRTÉK == ']') return KR; if (elválasztó_karakter_ÉRTÉK != ',') throw new IllegalArgumentException("adat elválasztó_karakter_ÉRTÉK HIBA");
                }
            }
            if (karakter_ÉRTÉK == '"') {
                StringBuilder KR = new StringBuilder();
                while (true) {
                    char Tovább_cikk = FORRÁS.charAt(Pozíció++); if (Tovább_cikk == '"') return KR.toString();
                    if (Tovább_cikk == '\\') {
                        Tovább_cikk = FORRÁS.charAt(Pozíció++);
                        if (Tovább_cikk == 'u') { KR.append((char)Integer.parseInt(FORRÁS.substring(Pozíció, Pozíció + 4),16)); Pozíció += 4; continue; }
                        if (Tovább_cikk == 'n') Tovább_cikk = '\n'; else if (Tovább_cikk == 'r') Tovább_cikk = '\r'; else if (Tovább_cikk == 't') Tovább_cikk = '\t';
                        else if (Tovább_cikk == 'b') Tovább_cikk = '\b'; else if (Tovább_cikk == 'f') Tovább_cikk = '\f';
                        else if (Tovább_cikk != '"' && Tovább_cikk != '\\' && Tovább_cikk != '/') throw new IllegalArgumentException("문자 이스케이프 HIBA");
                    }
                    KR.append(Tovább_cikk);
                }
            }
            int Futtatás = Pozíció - 1;
            while (Pozíció < FORRÁS.length() && ",]} \t\r\n".indexOf(FORRÁS.charAt(Pozíció)) < 0) Pozíció++;
            String ÉRTÉK = FORRÁS.substring(Futtatás, Pozíció);
            if (ÉRTÉK.equals("true")) return Boolean.TRUE; if (ÉRTÉK.equals("false")) return Boolean.FALSE; if (ÉRTÉK.equals("null")) return null;
            return Double.valueOf(ÉRTÉK);
        }
    }
    static String kivonat_Fájl(Path ÚTVONAL) throws Exception {
        MessageDigest 계산 = MessageDigest.getInstance("SHA-256"); byte[] adat = new byte[1024 * 1024];
        try (InputStream bevitel_ÉRTÉK = Files.newInputStream(ÚTVONAL)) { for (int hossz_ÉRTÉK; (hossz_ÉRTÉK = bevitel_ÉRTÉK.read(adat)) >= 0;) 계산.update(adat,0,hossz_ÉRTÉK); }
        return kivonat_SMS(계산.digest());
    }
    static String kivonat_SMS(byte[] adat) {
        StringBuilder Szöveg = new StringBuilder(); for (byte ÉRTÉK : adat) Szöveg.append(String.format(Locale.ROOT,"%02x",ÉRTÉK & 255)); return Szöveg.toString();
    }
    static Path belső_útvonal(Path teendő_gyök, String Név) {
        Path KR = teendő_gyök.resolve(Név).normalize();
        if (Név.isEmpty() || Paths.get(Név).isAbsolute() || !KR.startsWith(teendő_gyök) || Név.indexOf('\\') >= 0)
            throw new IllegalArgumentException("범위를 벗어난 ÚTVONAL: " + Név);
        for (Path 부분 : Paths.get(Név)) if (부분.toString().equals("..")) throw new IllegalArgumentException("상위 ÚTVONAL 금지: " + Név);
        for (Path aktuális_cikk = KR; aktuális_cikk != null && aktuális_cikk.startsWith(teendő_gyök); aktuális_cikk = aktuális_cikk.getParent())
            if (Files.isSymbolicLink(aktuális_cikk)) throw new IllegalArgumentException("의존성 경로의 링크 금지: " + Név);
        return KR;
    }
    static String parancs_kimenet(List<String> Parancs) throws Exception {
        Process folyamat_ÉRTÉK = new ProcessBuilder(Parancs).redirectError(ProcessBuilder.Redirect.INHERIT).start();
        String KR = new String(folyamat_ÉRTÉK.getInputStream().readAllBytes(),StandardCharsets.UTF_8);
        if (folyamat_ÉRTÉK.waitFor() != 0) throw new IOException("Parancs hiba_ÉRTÉK: " + Parancs.get(0)); return KR;
    }
    static void kivon(Path archív_ÉRTÉK, Path cél_ÉRTÉK) throws Exception {
        for (String Név : parancs_kimenet(Arrays.asList("tar","-tzf",archív_ÉRTÉK.toString())).split("\n")) belső_útvonal(cél_ÉRTÉK, Név);
        for (String Vonal : parancs_kimenet(Arrays.asList("tar","-tvzf",archív_ÉRTÉK.toString())).split("\n"))
            if (!Vonal.isEmpty() && Vonal.charAt(0) != '-' && Vonal.charAt(0) != 'd') throw new IOException("külső_ÉRTÉK 링크 또는 특수 파일을 포함한 의존성");
        Files.createDirectories(cél_ÉRTÉK);
        int Állapot_ÉRTÉK = new ProcessBuilder("tar","--no-same-owner","--no-same-permissions","-xzf",archív_ÉRTÉK.toString(),"-C",cél_ÉRTÉK.toString()).inheritIO().start().waitFor();
        if (Állapot_ÉRTÉK != 0) throw new IOException("의존성 archív_ÉRTÉK kiad_tár hiba_ÉRTÉK");
    }
    static void 호출(Path 작업경로, Path Eszközök, List<String> Argumentumok, Map<String,String> környezet_5d36e09c) throws Exception {
        List<String> Parancs = new ArrayList<>(Arrays.asList("python3", Eszközök.toString())); Parancs.addAll(Argumentumok);
        ProcessBuilder végrehajt_parancs = new ProcessBuilder(Parancs).directory(작업경로.toFile()).inheritIO(); végrehajt_parancs.environment().putAll(környezet_5d36e09c);
        int Állapot_ÉRTÉK = végrehajt_parancs.start().waitFor(); if (Állapot_ÉRTÉK != 0) throw new IOException("Eszközök hiba_ÉRTÉK: " + Eszközök + " (" + Állapot_ÉRTÉK + ")");
    }
    @SuppressWarnings("unchecked")
    public static void main(String[] Argumentumok) throws Exception {
        if (Argumentumok.length < 1) throw new IllegalArgumentException("build, run, desktop, image, check, test-system 중 동작을 지정하세요");
        String Művelet = Argumentumok[0];
        if (!Arrays.asList("build","run","desktop","image","check","test-system").contains(Művelet)) throw new IllegalArgumentException("알 szám 없는 Művelet");
        Path teendő_gyök = Paths.get(System.getProperty("worldos.edition.root")).toAbsolutePath().normalize();
        Map<String,Object> Beállítások = (Map<String,Object>)new adat_elemző(Files.readString(teendő_gyök.resolve("native.json"),StandardCharsets.UTF_8)).Olvasás();
        Path forrás_fa = belső_útvonal(teendő_gyök,(String)Beállítások.get("source")), kernel_ÉRTÉK = belső_útvonal(forrás_fa,(String)Beállítások.get("native"));
        List<String> 소유파일들 = (List<String>)(List<?>)Beállítások.get("owned_files");
        for (String Név : 소유파일들) if (!Files.isRegularFile(belső_útvonal(forrás_fa,Név))) throw new IOException("forrás_fa 없음: " + Név);
        if (Művelet.equals("check")) { System.out.println(Beállítások.get("country") + " " + Beállítások.get("language") + " 독립 forrás_fa igazol 완료"); return; }
        String erőforrás_relatív_elérési_út = (String)Beállítások.getOrDefault("resource_root", ".");
        if (!erőforrás_relatív_elérési_út.equals(".") && !erőforrás_relatív_elérési_út.equals("..")) throw new IllegalArgumentException("의존성 teendő_gyök ÚTVONAL HIBA");
        Path erőforrás_ÉRTÉK = teendő_gyök.resolve(erőforrás_relatív_elérési_út).normalize(); Path archív_ÉRTÉK = erőforrás_ÉRTÉK.resolve("native-vendor.tar.gz");
        String 기대해시 = (String)Beállítások.get("vendor_sha256");
        if (!kivonat_Fájl(archív_ÉRTÉK).equals(기대해시)) throw new IOException("의존성 SHA-256 불일치");
        Path jelölő_ÉRTÉK = forrás_fa.resolve(".vendor-sha256");
        if (!Files.isRegularFile(jelölő_ÉRTÉK) || !Files.readString(jelölő_ÉRTÉK).trim().equals(기대해시)) { kivon(archív_ÉRTÉK, forrás_fa); Files.writeString(jelölő_ÉRTÉK,기대해시 + "\n"); }
        Map<String,String> környezet_5d36e09c = new HashMap<>(System.getenv());
        Path ipConfig = null;
        if (környezet_5d36e09c.containsKey("IP_CONFIG")) ipConfig = Paths.get(környezet_5d36e09c.get("IP_CONFIG")).toAbsolutePath().normalize();
        else for (Path parent = teendő_gyök; parent != null; parent = parent.getParent()) {
            if (Files.isRegularFile(parent.resolve("ip.conf"))) { ipConfig = parent.resolve("ip.conf"); break; }
        }
        if (ipConfig == null) ipConfig = forrás_fa.resolve("ip.conf");
        if (!Files.isRegularFile(ipConfig)) throw new IOException("Missing ip.conf: " + ipConfig);
        környezet_5d36e09c.put("IP_CONFIG", ipConfig.toString());
        if (Arrays.asList("run","desktop","test-system").contains(Művelet) && !környezet_5d36e09c.containsKey("QEMU_AARCH64")) {
            Path app_indító = erőforrás_ÉRTÉK.resolve("host/qemu"), indító_jelölő = erőforrás_ÉRTÉK.resolve("host/.qemu-sha256");
            String indító_kivonat = (String)Beállítások.get("qemu_sha256");
            if (!Files.isRegularFile(app_indító) || !Files.isRegularFile(indító_jelölő) || !Files.readString(indító_jelölő).trim().equals(indító_kivonat)) {
                Path indító_archív = erőforrás_ÉRTÉK.resolve("qemu-host.tar.gz"); if (!kivonat_Fájl(indító_archív).equals(indító_kivonat)) throw new IOException("QEMU SHA-256 불일치");
                kivon(indító_archív,erőforrás_ÉRTÉK.resolve("host")); Files.writeString(indító_jelölő,indító_kivonat + "\n");
            }
            környezet_5d36e09c.put("QEMU_AARCH64",app_indító.toString());
        }
        MessageDigest 계산 = MessageDigest.getInstance("SHA-256"); Collections.sort(소유파일들);
        for (String Név : 소유파일들) { 계산.update(Név.getBytes(StandardCharsets.UTF_8)); 계산.update(Files.readAllBytes(belső_útvonal(forrás_fa,Név))); }
        계산.update("ip.conf\0".getBytes(StandardCharsets.UTF_8)); 계산.update(Files.readAllBytes(ipConfig));
        String forrás_kivonat = kivonat_SMS(계산.digest()); Path épít_jelölő = kernel_ÉRTÉK.resolve("build/worldos-source.sha256");
        if (Művelet.equals("build") || !Files.isRegularFile(épít_jelölő) || !Files.readString(épít_jelölő).trim().equals(forrás_kivonat)) {
            호출(kernel_ÉRTÉK,belső_útvonal(kernel_ÉRTÉK,(String)Beállítások.get("builder")),Collections.emptyList(),környezet_5d36e09c);
            Files.writeString(épít_jelölő,forrás_kivonat + "\n");
        }
        List<String> 추가인수 = new ArrayList<>(Arrays.asList(Argumentumok).subList(1,Argumentumok.length));
        if (Művelet.equals("run") || Művelet.equals("desktop")) {
            if (Művelet.equals("desktop")) 추가인수.add(0,"--desktop");
            호출(kernel_ÉRTÉK,belső_útvonal(kernel_ÉRTÉK,(String)Beállítások.get("runner")),추가인수,környezet_5d36e09c);
        } else if (Művelet.equals("image")) 호출(kernel_ÉRTÉK,belső_útvonal(kernel_ÉRTÉK,(String)Beállítások.get("image_builder")),추가인수,környezet_5d36e09c);
        else if (Művelet.equals("test-system")) {
            추가인수.add(0,teendő_gyök.toString()); 추가인수.add(0,"--edition");
            호출(kernel_ÉRTÉK,belső_útvonal(kernel_ÉRTÉK,(String)Beállítások.get("system_tester")),추가인수,környezet_5d36e09c);
        }
    }
}
