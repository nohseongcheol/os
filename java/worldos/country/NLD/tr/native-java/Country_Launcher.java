// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.security.MessageDigest;
import java.util.*;

/** 독립 국가판의 의존성 검사·복원·oluştur·실행을 맡는 konak Java araçlar. */
public final class Country_Launcher {
    static final class veri_ayrıştırıcı {
        final String kaynakKod; int konum;
        veri_ayrıştırıcı(String metin) { kaynakKod = metin; }
        void 빈칸() { while (konum < kaynakKod.length() && Character.isWhitespace(kaynakKod.charAt(konum))) konum++; }
        Object Okuma() {
            빈칸(); char karakter_değer = kaynakKod.charAt(konum++);
            if (karakter_değer == '{') {
                Map<String,Object> sonuç = new LinkedHashMap<>(); 빈칸();
                if (kaynakKod.charAt(konum) == '}') { konum++; return sonuç; }
                while (true) {
                    String İsim = (String)Okuma(); 빈칸(); if (kaynakKod.charAt(konum++) != ':') throw new IllegalArgumentException("veri sınırlayıcı_değer hata");
                    sonuç.put(İsim, Okuma()); 빈칸(); char sınırlayıcı_değer = kaynakKod.charAt(konum++);
                    if (sınırlayıcı_değer == '}') return sonuç; if (sınırlayıcı_değer != ',') throw new IllegalArgumentException("veri sınırlayıcı_değer hata");
                }
            }
            if (karakter_değer == '[') {
                List<Object> sonuç = new ArrayList<>(); 빈칸();
                if (kaynakKod.charAt(konum) == ']') { konum++; return sonuç; }
                while (true) {
                    sonuç.add(Okuma()); 빈칸(); char sınırlayıcı_değer = kaynakKod.charAt(konum++);
                    if (sınırlayıcı_değer == ']') return sonuç; if (sınırlayıcı_değer != ',') throw new IllegalArgumentException("veri sınırlayıcı_değer hata");
                }
            }
            if (karakter_değer == '"') {
                StringBuilder sonuç = new StringBuilder();
                while (true) {
                    char Sonraki_öğe = kaynakKod.charAt(konum++); if (Sonraki_öğe == '"') return sonuç.toString();
                    if (Sonraki_öğe == '\\') {
                        Sonraki_öğe = kaynakKod.charAt(konum++);
                        if (Sonraki_öğe == 'u') { sonuç.append((char)Integer.parseInt(kaynakKod.substring(konum, konum + 4),16)); konum += 4; continue; }
                        if (Sonraki_öğe == 'n') Sonraki_öğe = '\n'; else if (Sonraki_öğe == 'r') Sonraki_öğe = '\r'; else if (Sonraki_öğe == 't') Sonraki_öğe = '\t';
                        else if (Sonraki_öğe == 'b') Sonraki_öğe = '\b'; else if (Sonraki_öğe == 'f') Sonraki_öğe = '\f';
                        else if (Sonraki_öğe != '"' && Sonraki_öğe != '\\' && Sonraki_öğe != '/') throw new IllegalArgumentException("문자 이스케이프 hata");
                    }
                    sonuç.append(Sonraki_öğe);
                }
            }
            int çalıştır = konum - 1;
            while (konum < kaynakKod.length() && ",]} \t\r\n".indexOf(kaynakKod.charAt(konum)) < 0) konum++;
            String değer = kaynakKod.substring(çalıştır, konum);
            if (değer.equals("true")) return Boolean.TRUE; if (değer.equals("false")) return Boolean.FALSE; if (değer.equals("null")) return null;
            return Double.valueOf(değer);
        }
    }
    static String özet_Dosya(Path yol) throws Exception {
        MessageDigest 계산 = MessageDigest.getInstance("SHA-256"); byte[] veri = new byte[1024 * 1024];
        try (InputStream artış_değer = Files.newInputStream(yol)) { for (int süre_değer; (süre_değer = artış_değer.read(veri)) >= 0;) 계산.update(veri,0,süre_değer); }
        return özet_SMS(계산.digest());
    }
    static String özet_SMS(byte[] veri) {
        StringBuilder metin = new StringBuilder(); for (byte değer : veri) metin.append(String.format(Locale.ROOT,"%02x",değer & 255)); return metin.toString();
    }
    static Path iç_yol(Path işlem_kök, String İsim) {
        Path sonuç = işlem_kök.resolve(İsim).normalize();
        if (İsim.isEmpty() || Paths.get(İsim).isAbsolute() || !sonuç.startsWith(işlem_kök) || İsim.indexOf('\\') >= 0)
            throw new IllegalArgumentException("범위를 벗어난 yol: " + İsim);
        for (Path 부분 : Paths.get(İsim)) if (부분.toString().equals("..")) throw new IllegalArgumentException("상위 yol 금지: " + İsim);
        for (Path geçerli_öğe = sonuç; geçerli_öğe != null && geçerli_öğe.startsWith(işlem_kök); geçerli_öğe = geçerli_öğe.getParent())
            if (Files.isSymbolicLink(geçerli_öğe)) throw new IllegalArgumentException("의존성 경로의 링크 금지: " + İsim);
        return sonuç;
    }
    static String komut_çıktı(List<String> komut) throws Exception {
        Process işlem_değer = new ProcessBuilder(komut).redirectError(ProcessBuilder.Redirect.INHERIT).start();
        String sonuç = new String(işlem_değer.getInputStream().readAllBytes(),StandardCharsets.UTF_8);
        if (işlem_değer.waitFor() != 0) throw new IOException("komut hata_değer: " + komut.get(0)); return sonuç;
    }
    static void ayıklamak(Path Arşiv_değer, Path hedef_değer) throws Exception {
        for (String İsim : komut_çıktı(Arrays.asList("tar","-tzf",Arşiv_değer.toString())).split("\n")) iç_yol(hedef_değer, İsim);
        for (String girdi_satırı : komut_çıktı(Arrays.asList("tar","-tvzf",Arşiv_değer.toString())).split("\n"))
            if (!girdi_satırı.isEmpty() && girdi_satırı.charAt(0) != '-' && girdi_satırı.charAt(0) != 'd') throw new IOException("dış_değer 링크 또는 특수 파일을 포함한 의존성");
        Files.createDirectories(hedef_değer);
        int Durum_değer = new ProcessBuilder("tar","--no-same-owner","--no-same-permissions","-xzf",Arşiv_değer.toString(),"-C",hedef_değer.toString()).inheritIO().start().waitFor();
        if (Durum_değer != 0) throw new IOException("의존성 Arşiv_değer sürüm_Depolama hata_değer");
    }
    static void 호출(Path 작업경로, Path araçlar, List<String> bağımsız_değişkenler, Map<String,String> ortam) throws Exception {
        List<String> komut = new ArrayList<>(Arrays.asList("python3", araçlar.toString())); komut.addAll(bağımsız_değişkenler);
        ProcessBuilder yürütmek_komut = new ProcessBuilder(komut).directory(작업경로.toFile()).inheritIO(); yürütmek_komut.environment().putAll(ortam);
        int Durum_değer = yürütmek_komut.start().waitFor(); if (Durum_değer != 0) throw new IOException("araçlar hata_değer: " + araçlar + " (" + Durum_değer + ")");
    }
    @SuppressWarnings("unchecked")
    public static void main(String[] bağımsız_değişkenler) throws Exception {
        if (bağımsız_değişkenler.length < 1) throw new IllegalArgumentException("build, run, desktop, image, check, test-system 중 동작을 지정하세요");
        String Eylem = bağımsız_değişkenler[0];
        if (!Arrays.asList("build","run","desktop","image","check","test-system").contains(Eylem)) throw new IllegalArgumentException("알 수 없는 Eylem");
        Path işlem_kök = Paths.get(System.getProperty("worldos.edition.root")).toAbsolutePath().normalize();
        Map<String,Object> Ayarlar = (Map<String,Object>)new veri_ayrıştırıcı(Files.readString(işlem_kök.resolve("native.json"),StandardCharsets.UTF_8)).Okuma();
        Path kaynak_ağaç = iç_yol(işlem_kök,(String)Ayarlar.get("source")), çekirdek_değer = iç_yol(kaynak_ağaç,(String)Ayarlar.get("native"));
        List<String> 소유파일들 = (List<String>)(List<?>)Ayarlar.get("owned_files");
        for (String İsim : 소유파일들) if (!Files.isRegularFile(iç_yol(kaynak_ağaç,İsim))) throw new IOException("kaynak_ağaç 없음: " + İsim);
        if (Eylem.equals("check")) { System.out.println(Ayarlar.get("country") + " " + Ayarlar.get("language") + " 독립 kaynak_ağaç doğrulamak 완료"); return; }
        String kaynak_göreli_yol = (String)Ayarlar.getOrDefault("resource_root", ".");
        if (!kaynak_göreli_yol.equals(".") && !kaynak_göreli_yol.equals("..")) throw new IllegalArgumentException("의존성 işlem_kök yol hata");
        Path kaynak_değer = işlem_kök.resolve(kaynak_göreli_yol).normalize(); Path Arşiv_değer = kaynak_değer.resolve("native-vendor.tar.gz");
        String 기대해시 = (String)Ayarlar.get("vendor_sha256");
        if (!özet_Dosya(Arşiv_değer).equals(기대해시)) throw new IOException("의존성 SHA-256 불일치");
        Path işaret_değer = kaynak_ağaç.resolve(".vendor-sha256");
        if (!Files.isRegularFile(işaret_değer) || !Files.readString(işaret_değer).trim().equals(기대해시)) { ayıklamak(Arşiv_değer, kaynak_ağaç); Files.writeString(işaret_değer,기대해시 + "\n"); }
        Map<String,String> ortam = new HashMap<>(System.getenv());
        Path ipConfig = null;
        if (ortam.containsKey("IP_CONFIG")) ipConfig = Paths.get(ortam.get("IP_CONFIG")).toAbsolutePath().normalize();
        else for (Path parent = işlem_kök; parent != null; parent = parent.getParent()) {
            if (Files.isRegularFile(parent.resolve("ip.conf"))) { ipConfig = parent.resolve("ip.conf"); break; }
        }
        if (ipConfig == null) ipConfig = kaynak_ağaç.resolve("ip.conf");
        if (!Files.isRegularFile(ipConfig)) throw new IOException("Missing ip.conf: " + ipConfig);
        ortam.put("IP_CONFIG", ipConfig.toString());
        if (Arrays.asList("run","desktop","test-system").contains(Eylem) && !ortam.containsKey("QEMU_AARCH64")) {
            Path program_Launcher = kaynak_değer.resolve("host/qemu"), Launcher_işaret = kaynak_değer.resolve("host/.qemu-sha256");
            String Launcher_özet = (String)Ayarlar.get("qemu_sha256");
            if (!Files.isRegularFile(program_Launcher) || !Files.isRegularFile(Launcher_işaret) || !Files.readString(Launcher_işaret).trim().equals(Launcher_özet)) {
                Path Launcher_Arşiv = kaynak_değer.resolve("qemu-host.tar.gz"); if (!özet_Dosya(Launcher_Arşiv).equals(Launcher_özet)) throw new IOException("QEMU SHA-256 불일치");
                ayıklamak(Launcher_Arşiv,kaynak_değer.resolve("host")); Files.writeString(Launcher_işaret,Launcher_özet + "\n");
            }
            ortam.put("QEMU_AARCH64",program_Launcher.toString());
        }
        MessageDigest 계산 = MessageDigest.getInstance("SHA-256"); Collections.sort(소유파일들);
        for (String İsim : 소유파일들) { 계산.update(İsim.getBytes(StandardCharsets.UTF_8)); 계산.update(Files.readAllBytes(iç_yol(kaynak_ağaç,İsim))); }
        계산.update("ip.conf\0".getBytes(StandardCharsets.UTF_8)); 계산.update(Files.readAllBytes(ipConfig));
        String kaynak_özet = özet_SMS(계산.digest()); Path BLD_işaret = çekirdek_değer.resolve("build/worldos-source.sha256");
        if (Eylem.equals("build") || !Files.isRegularFile(BLD_işaret) || !Files.readString(BLD_işaret).trim().equals(kaynak_özet)) {
            호출(çekirdek_değer,iç_yol(çekirdek_değer,(String)Ayarlar.get("builder")),Collections.emptyList(),ortam);
            Files.writeString(BLD_işaret,kaynak_özet + "\n");
        }
        List<String> 추가인수 = new ArrayList<>(Arrays.asList(bağımsız_değişkenler).subList(1,bağımsız_değişkenler.length));
        if (Eylem.equals("run") || Eylem.equals("desktop")) {
            if (Eylem.equals("desktop")) 추가인수.add(0,"--desktop");
            호출(çekirdek_değer,iç_yol(çekirdek_değer,(String)Ayarlar.get("runner")),추가인수,ortam);
        } else if (Eylem.equals("image")) 호출(çekirdek_değer,iç_yol(çekirdek_değer,(String)Ayarlar.get("image_builder")),추가인수,ortam);
        else if (Eylem.equals("test-system")) {
            추가인수.add(0,işlem_kök.toString()); 추가인수.add(0,"--edition");
            호출(çekirdek_değer,iç_yol(çekirdek_değer,(String)Ayarlar.get("system_tester")),추가인수,ortam);
        }
    }
}
