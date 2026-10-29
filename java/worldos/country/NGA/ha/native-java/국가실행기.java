// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.security.MessageDigest;
import java.util.*;

/** 독립 국가판의 의존성 검사·복원·Gina_na_ura·실행을 맡는 sauka Java Kaya. */
public final class 국가실행기 {
    static final class Tarin_bayani_tatsar_manhaja {
        final String tushe; int 위치;
        Tarin_bayani_tatsar_manhaja(String SMS) { tushe = SMS; }
        void 빈칸() { while (위치 < tushe.length() && Character.isWhitespace(tushe.charAt(위치))) 위치++; }
        Object Yi_Karatu() {
            빈칸(); char Harafi_Daraja = tushe.charAt(위치++);
            if (Harafi_Daraja == '{') {
                Map<String,Object> 결과 = new LinkedHashMap<>(); 빈칸();
                if (tushe.charAt(위치) == '}') { 위치++; return 결과; }
                while (true) {
                    String Suna = (String)Yi_Karatu(); 빈칸(); if (tushe.charAt(위치++) != ':') throw new IllegalArgumentException("Tarin_bayani Haruffan_rabawa_Daraja Kuskure");
                    결과.put(Suna, Yi_Karatu()); 빈칸(); char Haruffan_rabawa_Daraja = tushe.charAt(위치++);
                    if (Haruffan_rabawa_Daraja == '}') return 결과; if (Haruffan_rabawa_Daraja != ',') throw new IllegalArgumentException("Tarin_bayani Haruffan_rabawa_Daraja Kuskure");
                }
            }
            if (Harafi_Daraja == '[') {
                List<Object> 결과 = new ArrayList<>(); 빈칸();
                if (tushe.charAt(위치) == ']') { 위치++; return 결과; }
                while (true) {
                    결과.add(Yi_Karatu()); 빈칸(); char Haruffan_rabawa_Daraja = tushe.charAt(위치++);
                    if (Haruffan_rabawa_Daraja == ']') return 결과; if (Haruffan_rabawa_Daraja != ',') throw new IllegalArgumentException("Tarin_bayani Haruffan_rabawa_Daraja Kuskure");
                }
            }
            if (Harafi_Daraja == '"') {
                StringBuilder 결과 = new StringBuilder();
                while (true) {
                    char 다음 = tushe.charAt(위치++); if (다음 == '"') return 결과.toString();
                    if (다음 == '\\') {
                        다음 = tushe.charAt(위치++);
                        if (다음 == 'u') { 결과.append((char)Integer.parseInt(tushe.substring(위치, 위치 + 4),16)); 위치 += 4; continue; }
                        if (다음 == 'n') 다음 = '\n'; else if (다음 == 'r') 다음 = '\r'; else if (다음 == 't') 다음 = '\t';
                        else if (다음 == 'b') 다음 = '\b'; else if (다음 == 'f') 다음 = '\f';
                        else if (다음 != '"' && 다음 != '\\' && 다음 != '/') throw new IllegalArgumentException("문자 이스케이프 Kuskure");
                    }
                    결과.append(다음);
                }
            }
            int Tafiyar_da = 위치 - 1;
            while (위치 < tushe.length() && ",]} \t\r\n".indexOf(tushe.charAt(위치)) < 0) 위치++;
            String Daraja = tushe.substring(Tafiyar_da, 위치);
            if (Daraja.equals("true")) return Boolean.TRUE; if (Daraja.equals("false")) return Boolean.FALSE; if (Daraja.equals("null")) return null;
            return Double.valueOf(Daraja);
        }
    }
    static String hash_Fayil(Path Hanyar_shiga) throws Exception {
        MessageDigest 계산 = MessageDigest.getInstance("SHA-256"); byte[] Tarin_bayani = new byte[1024 * 1024];
        try (InputStream 입력 = Files.newInputStream(Hanyar_shiga)) { for (int Tsawo_Daraja; (Tsawo_Daraja = 입력.read(Tarin_bayani)) >= 0;) 계산.update(Tarin_bayani,0,Tsawo_Daraja); }
        return hash_SMS(계산.digest());
    }
    static String hash_SMS(byte[] Tarin_bayani) {
        StringBuilder SMS = new StringBuilder(); for (byte Daraja : Tarin_bayani) SMS.append(String.format(Locale.ROOT,"%02x",Daraja & 255)); return SMS.toString();
    }
    static Path 내부경로(Path 기준, String Suna) {
        Path 결과 = 기준.resolve(Suna).normalize();
        if (Suna.isEmpty() || Paths.get(Suna).isAbsolute() || !결과.startsWith(기준) || Suna.indexOf('\\') >= 0)
            throw new IllegalArgumentException("범위를 벗어난 Hanyar_shiga: " + Suna);
        for (Path 부분 : Paths.get(Suna)) if (부분.toString().equals("..")) throw new IllegalArgumentException("상위 Hanyar_shiga 금지: " + Suna);
        for (Path 현재 = 결과; 현재 != null && 현재.startsWith(기준); 현재 = 현재.getParent())
            if (Files.isSymbolicLink(현재)) throw new IllegalArgumentException("의존성 경로의 링크 금지: " + Suna);
        return 결과;
    }
    static String 명령출력(List<String> Umarni) throws Exception {
        Process haryar_aikin_na_ura_Daraja = new ProcessBuilder(Umarni).redirectError(ProcessBuilder.Redirect.INHERIT).start();
        String 결과 = new String(haryar_aikin_na_ura_Daraja.getInputStream().readAllBytes(),StandardCharsets.UTF_8);
        if (haryar_aikin_na_ura_Daraja.waitFor() != 0) throw new IOException("Umarni Kasa_aiki_Daraja: " + Umarni.get(0)); return 결과;
    }
    static void tsamo(Path Rumbun_ajiya_Daraja, Path Zangon_ƙarshe_Daraja) throws Exception {
        for (String Suna : 명령출력(Arrays.asList("tar","-tzf",Rumbun_ajiya_Daraja.toString())).split("\n")) 내부경로(Zangon_ƙarshe_Daraja, Suna);
        for (String Layi : 명령출력(Arrays.asList("tar","-tvzf",Rumbun_ajiya_Daraja.toString())).split("\n"))
            if (!Layi.isEmpty() && Layi.charAt(0) != '-' && Layi.charAt(0) != 'd') throw new IOException("외부 링크 또는 특수 파일을 포함한 의존성");
        Files.createDirectories(Zangon_ƙarshe_Daraja);
        int Matsayi_Daraja = new ProcessBuilder("tar","--no-same-owner","--no-same-permissions","-xzf",Rumbun_ajiya_Daraja.toString(),"-C",Zangon_ƙarshe_Daraja.toString()).inheritIO().start().waitFor();
        if (Matsayi_Daraja != 0) throw new IOException("의존성 Rumbun_ajiya_Daraja saka_Wurin_adana Kasa_aiki_Daraja");
    }
    static void 호출(Path 작업경로, Path Kaya, List<String> 인수, Map<String,String> 환경) throws Exception {
        List<String> Umarni = new ArrayList<>(Arrays.asList("python3", Kaya.toString())); Umarni.addAll(인수);
        ProcessBuilder gudanar_Umarni = new ProcessBuilder(Umarni).directory(작업경로.toFile()).inheritIO(); gudanar_Umarni.environment().putAll(환경);
        int Matsayi_Daraja = gudanar_Umarni.start().waitFor(); if (Matsayi_Daraja != 0) throw new IOException("Kaya Kasa_aiki_Daraja: " + Kaya + " (" + Matsayi_Daraja + ")");
    }
    @SuppressWarnings("unchecked")
    public static void main(String[] 인수) throws Exception {
        if (인수.length < 1) throw new IllegalArgumentException("build, run, desktop, image, check, test-system 중 동작을 지정하세요");
        String Aiki = 인수[0];
        if (!Arrays.asList("build","run","desktop","image","check","test-system").contains(Aiki)) throw new IllegalArgumentException("알 수 없는 Aiki");
        Path 기준 = Paths.get(System.getProperty("worldos.edition.root")).toAbsolutePath().normalize();
        Map<String,Object> Saituna = (Map<String,Object>)new Tarin_bayani_tatsar_manhaja(Files.readString(기준.resolve("native.json"),StandardCharsets.UTF_8)).Yi_Karatu();
        Path tushe_Li_irabin_tarin_bayanai = 내부경로(기준,(String)Saituna.get("source")), Kwara_Daraja = 내부경로(tushe_Li_irabin_tarin_bayanai,(String)Saituna.get("native"));
        List<String> 소유파일들 = (List<String>)(List<?>)Saituna.get("owned_files");
        for (String Suna : 소유파일들) if (!Files.isRegularFile(내부경로(tushe_Li_irabin_tarin_bayanai,Suna))) throw new IOException("tushe_Li_irabin_tarin_bayanai 없음: " + Suna);
        if (Aiki.equals("check")) { System.out.println(Saituna.get("country") + " " + Saituna.get("language") + " 독립 tushe_Li_irabin_tarin_bayanai Tabbatar_da 완료"); return; }
        String 자원상대 = (String)Saituna.getOrDefault("resource_root", ".");
        if (!자원상대.equals(".") && !자원상대.equals("..")) throw new IllegalArgumentException("의존성 기준 Hanyar_shiga Kuskure");
        Path albarkatu_Daraja = 기준.resolve(자원상대).normalize(); Path Rumbun_ajiya_Daraja = albarkatu_Daraja.resolve("native-vendor.tar.gz");
        String 기대해시 = (String)Saituna.get("vendor_sha256");
        if (!hash_Fayil(Rumbun_ajiya_Daraja).equals(기대해시)) throw new IOException("의존성 SHA-256 불일치");
        Path 표식 = tushe_Li_irabin_tarin_bayanai.resolve(".vendor-sha256");
        if (!Files.isRegularFile(표식) || !Files.readString(표식).trim().equals(기대해시)) { tsamo(Rumbun_ajiya_Daraja, tushe_Li_irabin_tarin_bayanai); Files.writeString(표식,기대해시 + "\n"); }
        Map<String,String> 환경 = new HashMap<>(System.getenv());
        Path ipConfig = null;
        if (환경.containsKey("IP_CONFIG")) ipConfig = Paths.get(환경.get("IP_CONFIG")).toAbsolutePath().normalize();
        else for (Path parent = 기준; parent != null; parent = parent.getParent()) {
            if (Files.isRegularFile(parent.resolve("ip.conf"))) { ipConfig = parent.resolve("ip.conf"); break; }
        }
        if (ipConfig == null) ipConfig = tushe_Li_irabin_tarin_bayanai.resolve("ip.conf");
        if (!Files.isRegularFile(ipConfig)) throw new IOException("Missing ip.conf: " + ipConfig);
        환경.put("IP_CONFIG", ipConfig.toString());
        if (Arrays.asList("run","desktop","test-system").contains(Aiki) && !환경.containsKey("QEMU_AARCH64")) {
            Path Shiri_Mai_Fara_Ka_ida = albarkatu_Daraja.resolve("host/qemu"), 실행기표식 = albarkatu_Daraja.resolve("host/.qemu-sha256");
            String Mai_Fara_Ka_ida_hash = (String)Saituna.get("qemu_sha256");
            if (!Files.isRegularFile(Shiri_Mai_Fara_Ka_ida) || !Files.isRegularFile(실행기표식) || !Files.readString(실행기표식).trim().equals(Mai_Fara_Ka_ida_hash)) {
                Path Mai_Fara_Ka_ida_Rumbun_ajiya = albarkatu_Daraja.resolve("qemu-host.tar.gz"); if (!hash_Fayil(Mai_Fara_Ka_ida_Rumbun_ajiya).equals(Mai_Fara_Ka_ida_hash)) throw new IOException("QEMU SHA-256 불일치");
                tsamo(Mai_Fara_Ka_ida_Rumbun_ajiya,albarkatu_Daraja.resolve("host")); Files.writeString(실행기표식,Mai_Fara_Ka_ida_hash + "\n");
            }
            환경.put("QEMU_AARCH64",Shiri_Mai_Fara_Ka_ida.toString());
        }
        MessageDigest 계산 = MessageDigest.getInstance("SHA-256"); Collections.sort(소유파일들);
        for (String Suna : 소유파일들) { 계산.update(Suna.getBytes(StandardCharsets.UTF_8)); 계산.update(Files.readAllBytes(내부경로(tushe_Li_irabin_tarin_bayanai,Suna))); }
        계산.update("ip.conf\0".getBytes(StandardCharsets.UTF_8)); 계산.update(Files.readAllBytes(ipConfig));
        String tushe_hash = hash_SMS(계산.digest()); Path 빌드표식 = Kwara_Daraja.resolve("build/worldos-source.sha256");
        if (Aiki.equals("build") || !Files.isRegularFile(빌드표식) || !Files.readString(빌드표식).trim().equals(tushe_hash)) {
            호출(Kwara_Daraja,내부경로(Kwara_Daraja,(String)Saituna.get("builder")),Collections.emptyList(),환경);
            Files.writeString(빌드표식,tushe_hash + "\n");
        }
        List<String> 추가인수 = new ArrayList<>(Arrays.asList(인수).subList(1,인수.length));
        if (Aiki.equals("run") || Aiki.equals("desktop")) {
            if (Aiki.equals("desktop")) 추가인수.add(0,"--desktop");
            호출(Kwara_Daraja,내부경로(Kwara_Daraja,(String)Saituna.get("runner")),추가인수,환경);
        } else if (Aiki.equals("image")) 호출(Kwara_Daraja,내부경로(Kwara_Daraja,(String)Saituna.get("image_builder")),추가인수,환경);
        else if (Aiki.equals("test-system")) {
            추가인수.add(0,기준.toString()); 추가인수.add(0,"--edition");
            호출(Kwara_Daraja,내부경로(Kwara_Daraja,(String)Saituna.get("system_tester")),추가인수,환경);
        }
    }
}
