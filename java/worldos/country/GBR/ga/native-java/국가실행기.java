// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.security.MessageDigest;
import java.util.*;

/** 독립 국가판의 의존성 검사·복원·tóg_córas·실행을 맡는 óstach Java Uirlisí. */
public final class 국가실행기 {
    static final class 자료해석기 {
        final String FOINSE; int suíomh;
        자료해석기(String Téacs) { FOINSE = Téacs; }
        void 빈칸() { while (suíomh < FOINSE.length() && Character.isWhitespace(FOINSE.charAt(suíomh))) suíomh++; }
        Object Léigh() {
            빈칸(); char carachtar_VALUE = FOINSE.charAt(suíomh++);
            if (carachtar_VALUE == '{') {
                Map<String,Object> tomhas = new LinkedHashMap<>(); 빈칸();
                if (FOINSE.charAt(suíomh) == '}') { suíomh++; return tomhas; }
                while (true) {
                    String Ainm = (String)Léigh(); 빈칸(); if (FOINSE.charAt(suíomh++) != ':') throw new IllegalArgumentException("sonraí teormharcóir_VALUE ERREÁID");
                    tomhas.put(Ainm, Léigh()); 빈칸(); char teormharcóir_VALUE = FOINSE.charAt(suíomh++);
                    if (teormharcóir_VALUE == '}') return tomhas; if (teormharcóir_VALUE != ',') throw new IllegalArgumentException("sonraí teormharcóir_VALUE ERREÁID");
                }
            }
            if (carachtar_VALUE == '[') {
                List<Object> tomhas = new ArrayList<>(); 빈칸();
                if (FOINSE.charAt(suíomh) == ']') { suíomh++; return tomhas; }
                while (true) {
                    tomhas.add(Léigh()); 빈칸(); char teormharcóir_VALUE = FOINSE.charAt(suíomh++);
                    if (teormharcóir_VALUE == ']') return tomhas; if (teormharcóir_VALUE != ',') throw new IllegalArgumentException("sonraí teormharcóir_VALUE ERREÁID");
                }
            }
            if (carachtar_VALUE == '"') {
                StringBuilder tomhas = new StringBuilder();
                while (true) {
                    char Ar_aghaidh_mír = FOINSE.charAt(suíomh++); if (Ar_aghaidh_mír == '"') return tomhas.toString();
                    if (Ar_aghaidh_mír == '\\') {
                        Ar_aghaidh_mír = FOINSE.charAt(suíomh++);
                        if (Ar_aghaidh_mír == 'u') { tomhas.append((char)Integer.parseInt(FOINSE.substring(suíomh, suíomh + 4),16)); suíomh += 4; continue; }
                        if (Ar_aghaidh_mír == 'n') Ar_aghaidh_mír = '\n'; else if (Ar_aghaidh_mír == 'r') Ar_aghaidh_mír = '\r'; else if (Ar_aghaidh_mír == 't') Ar_aghaidh_mír = '\t';
                        else if (Ar_aghaidh_mír == 'b') Ar_aghaidh_mír = '\b'; else if (Ar_aghaidh_mír == 'f') Ar_aghaidh_mír = '\f';
                        else if (Ar_aghaidh_mír != '"' && Ar_aghaidh_mír != '\\' && Ar_aghaidh_mír != '/') throw new IllegalArgumentException("문자 이스케이프 ERREÁID");
                    }
                    tomhas.append(Ar_aghaidh_mír);
                }
            }
            int Rith_2 = suíomh - 1;
            while (suíomh < FOINSE.length() && ",]} \t\r\n".indexOf(FOINSE.charAt(suíomh)) < 0) suíomh++;
            String VALUE = FOINSE.substring(Rith_2, suíomh);
            if (VALUE.equals("true")) return Boolean.TRUE; if (VALUE.equals("false")) return Boolean.FALSE; if (VALUE.equals("null")) return null;
            return Double.valueOf(VALUE);
        }
    }
    static String hais_comhad(Path CONAIR) throws Exception {
        MessageDigest 계산 = MessageDigest.getInstance("SHA-256"); byte[] sonraí = new byte[1024 * 1024];
        try (InputStream 입력 = Files.newInputStream(CONAIR)) { for (int fad_VALUE; (fad_VALUE = 입력.read(sonraí)) >= 0;) 계산.update(sonraí,0,fad_VALUE); }
        return hais_SMS(계산.digest());
    }
    static String hais_SMS(byte[] sonraí) {
        StringBuilder Téacs = new StringBuilder(); for (byte VALUE : sonraí) Téacs.append(String.format(Locale.ROOT,"%02x",VALUE & 255)); return Téacs.toString();
    }
    static Path 내부경로(Path teilgean_fréamh, String Ainm) {
        Path tomhas = teilgean_fréamh.resolve(Ainm).normalize();
        if (Ainm.isEmpty() || Paths.get(Ainm).isAbsolute() || !tomhas.startsWith(teilgean_fréamh) || Ainm.indexOf('\\') >= 0)
            throw new IllegalArgumentException("범위를 벗어난 CONAIR: " + Ainm);
        for (Path 부분 : Paths.get(Ainm)) if (부분.toString().equals("..")) throw new IllegalArgumentException("상위 CONAIR 금지: " + Ainm);
        for (Path 현재 = tomhas; 현재 != null && 현재.startsWith(teilgean_fréamh); 현재 = 현재.getParent())
            if (Files.isSymbolicLink(현재)) throw new IllegalArgumentException("의존성 경로의 링크 금지: " + Ainm);
        return tomhas;
    }
    static String 명령출력(List<String> Ordú) throws Exception {
        Process Próiseas_VALUE = new ProcessBuilder(Ordú).redirectError(ProcessBuilder.Redirect.INHERIT).start();
        String tomhas = new String(Próiseas_VALUE.getInputStream().readAllBytes(),StandardCharsets.UTF_8);
        if (Próiseas_VALUE.waitFor() != 0) throw new IOException("Ordú teip_VALUE: " + Ordú.get(0)); return tomhas;
    }
    static void bain_amach(Path Cartlann_VALUE, Path sprioc_VALUE) throws Exception {
        for (String Ainm : 명령출력(Arrays.asList("tar","-tzf",Cartlann_VALUE.toString())).split("\n")) 내부경로(sprioc_VALUE, Ainm);
        for (String Líne : 명령출력(Arrays.asList("tar","-tvzf",Cartlann_VALUE.toString())).split("\n"))
            if (!Líne.isEmpty() && Líne.charAt(0) != '-' && Líne.charAt(0) != 'd') throw new IOException("외부 링크 또는 특수 파일을 포함한 의존성");
        Files.createDirectories(sprioc_VALUE);
        int staid_VALUE = new ProcessBuilder("tar","--no-same-owner","--no-same-permissions","-xzf",Cartlann_VALUE.toString(),"-C",sprioc_VALUE.toString()).inheritIO().start().waitFor();
        if (staid_VALUE != 0) throw new IOException("의존성 Cartlann_VALUE leagan_Stóras teip_VALUE");
    }
    static void 호출(Path 작업경로, Path Uirlisí, List<String> Argóintí, Map<String,String> 환경) throws Exception {
        List<String> Ordú = new ArrayList<>(Arrays.asList("python3", Uirlisí.toString())); Ordú.addAll(Argóintí);
        ProcessBuilder Rith_ordú = new ProcessBuilder(Ordú).directory(작업경로.toFile()).inheritIO(); Rith_ordú.environment().putAll(환경);
        int staid_VALUE = Rith_ordú.start().waitFor(); if (staid_VALUE != 0) throw new IOException("Uirlisí teip_VALUE: " + Uirlisí + " (" + staid_VALUE + ")");
    }
    @SuppressWarnings("unchecked")
    public static void main(String[] Argóintí) throws Exception {
        if (Argóintí.length < 1) throw new IllegalArgumentException("build, run, desktop, image, check, test-system 중 동작을 지정하세요");
        String Gníomh = Argóintí[0];
        if (!Arrays.asList("build","run","desktop","image","check","test-system").contains(Gníomh)) throw new IllegalArgumentException("알 수 없는 Gníomh");
        Path teilgean_fréamh = Paths.get(System.getProperty("worldos.edition.root")).toAbsolutePath().normalize();
        Map<String,Object> Socruithe = (Map<String,Object>)new 자료해석기(Files.readString(teilgean_fréamh.resolve("native.json"),StandardCharsets.UTF_8)).Léigh();
        Path foinse_crann = 내부경로(teilgean_fréamh,(String)Socruithe.get("source")), eithne_VALUE = 내부경로(foinse_crann,(String)Socruithe.get("native"));
        List<String> 소유파일들 = (List<String>)(List<?>)Socruithe.get("owned_files");
        for (String Ainm : 소유파일들) if (!Files.isRegularFile(내부경로(foinse_crann,Ainm))) throw new IOException("foinse_crann 없음: " + Ainm);
        if (Gníomh.equals("check")) { System.out.println(Socruithe.get("country") + " " + Socruithe.get("language") + " 독립 foinse_crann fíoraigh 완료"); return; }
        String 자원상대 = (String)Socruithe.getOrDefault("resource_root", ".");
        if (!자원상대.equals(".") && !자원상대.equals("..")) throw new IllegalArgumentException("의존성 teilgean_fréamh CONAIR ERREÁID");
        Path acmhainn_VALUE = teilgean_fréamh.resolve(자원상대).normalize(); Path Cartlann_VALUE = acmhainn_VALUE.resolve("native-vendor.tar.gz");
        String 기대해시 = (String)Socruithe.get("vendor_sha256");
        if (!hais_comhad(Cartlann_VALUE).equals(기대해시)) throw new IOException("의존성 SHA-256 불일치");
        Path 표식 = foinse_crann.resolve(".vendor-sha256");
        if (!Files.isRegularFile(표식) || !Files.readString(표식).trim().equals(기대해시)) { bain_amach(Cartlann_VALUE, foinse_crann); Files.writeString(표식,기대해시 + "\n"); }
        Map<String,String> 환경 = new HashMap<>(System.getenv());
        Path ipConfig = null;
        if (환경.containsKey("IP_CONFIG")) ipConfig = Paths.get(환경.get("IP_CONFIG")).toAbsolutePath().normalize();
        else for (Path parent = teilgean_fréamh; parent != null; parent = parent.getParent()) {
            if (Files.isRegularFile(parent.resolve("ip.conf"))) { ipConfig = parent.resolve("ip.conf"); break; }
        }
        if (ipConfig == null) ipConfig = foinse_crann.resolve("ip.conf");
        if (!Files.isRegularFile(ipConfig)) throw new IOException("Missing ip.conf: " + ipConfig);
        환경.put("IP_CONFIG", ipConfig.toString());
        if (Arrays.asList("run","desktop","test-system").contains(Gníomh) && !환경.containsKey("QEMU_AARCH64")) {
            Path clár_tarraiceán_feidhmchlár = acmhainn_VALUE.resolve("host/qemu"), 실행기표식 = acmhainn_VALUE.resolve("host/.qemu-sha256");
            String tarraiceán_feidhmchlár_hais = (String)Socruithe.get("qemu_sha256");
            if (!Files.isRegularFile(clár_tarraiceán_feidhmchlár) || !Files.isRegularFile(실행기표식) || !Files.readString(실행기표식).trim().equals(tarraiceán_feidhmchlár_hais)) {
                Path tarraiceán_feidhmchlár_Cartlann = acmhainn_VALUE.resolve("qemu-host.tar.gz"); if (!hais_comhad(tarraiceán_feidhmchlár_Cartlann).equals(tarraiceán_feidhmchlár_hais)) throw new IOException("QEMU SHA-256 불일치");
                bain_amach(tarraiceán_feidhmchlár_Cartlann,acmhainn_VALUE.resolve("host")); Files.writeString(실행기표식,tarraiceán_feidhmchlár_hais + "\n");
            }
            환경.put("QEMU_AARCH64",clár_tarraiceán_feidhmchlár.toString());
        }
        MessageDigest 계산 = MessageDigest.getInstance("SHA-256"); Collections.sort(소유파일들);
        for (String Ainm : 소유파일들) { 계산.update(Ainm.getBytes(StandardCharsets.UTF_8)); 계산.update(Files.readAllBytes(내부경로(foinse_crann,Ainm))); }
        계산.update("ip.conf\0".getBytes(StandardCharsets.UTF_8)); 계산.update(Files.readAllBytes(ipConfig));
        String foinse_hais = hais_SMS(계산.digest()); Path 빌드표식 = eithne_VALUE.resolve("build/worldos-source.sha256");
        if (Gníomh.equals("build") || !Files.isRegularFile(빌드표식) || !Files.readString(빌드표식).trim().equals(foinse_hais)) {
            호출(eithne_VALUE,내부경로(eithne_VALUE,(String)Socruithe.get("builder")),Collections.emptyList(),환경);
            Files.writeString(빌드표식,foinse_hais + "\n");
        }
        List<String> 추가인수 = new ArrayList<>(Arrays.asList(Argóintí).subList(1,Argóintí.length));
        if (Gníomh.equals("run") || Gníomh.equals("desktop")) {
            if (Gníomh.equals("desktop")) 추가인수.add(0,"--desktop");
            호출(eithne_VALUE,내부경로(eithne_VALUE,(String)Socruithe.get("runner")),추가인수,환경);
        } else if (Gníomh.equals("image")) 호출(eithne_VALUE,내부경로(eithne_VALUE,(String)Socruithe.get("image_builder")),추가인수,환경);
        else if (Gníomh.equals("test-system")) {
            추가인수.add(0,teilgean_fréamh.toString()); 추가인수.add(0,"--edition");
            호출(eithne_VALUE,내부경로(eithne_VALUE,(String)Socruithe.get("system_tester")),추가인수,환경);
        }
    }
}
