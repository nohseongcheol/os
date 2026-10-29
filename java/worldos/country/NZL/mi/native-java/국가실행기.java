// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.security.MessageDigest;
import java.util.*;

/** 독립 국가판의 의존성 검사·복원·hanga_pūnaha·실행을 맡는 taurima Java Ngā_Utauta. */
public final class 국가실행기 {
    static final class 자료해석기 {
        final String pūtake; int tūranga;
        자료해석기(String Ngā_kupu) { pūtake = Ngā_kupu; }
        void 빈칸() { while (tūranga < pūtake.length() && Character.isWhitespace(pūtake.charAt(tūranga))) tūranga++; }
        Object Pānuitia() {
            빈칸(); char pūāhua_uara = pūtake.charAt(tūranga++);
            if (pūāhua_uara == '{') {
                Map<String,Object> mēhua = new LinkedHashMap<>(); 빈칸();
                if (pūtake.charAt(tūranga) == '}') { tūranga++; return mēhua; }
                while (true) {
                    String Ingoa = (String)Pānuitia(); 빈칸(); if (pūtake.charAt(tūranga++) != ':') throw new IllegalArgumentException("raraunga pūwehe_uara Pōhēhē");
                    mēhua.put(Ingoa, Pānuitia()); 빈칸(); char pūwehe_uara = pūtake.charAt(tūranga++);
                    if (pūwehe_uara == '}') return mēhua; if (pūwehe_uara != ',') throw new IllegalArgumentException("raraunga pūwehe_uara Pōhēhē");
                }
            }
            if (pūāhua_uara == '[') {
                List<Object> mēhua = new ArrayList<>(); 빈칸();
                if (pūtake.charAt(tūranga) == ']') { tūranga++; return mēhua; }
                while (true) {
                    mēhua.add(Pānuitia()); 빈칸(); char pūwehe_uara = pūtake.charAt(tūranga++);
                    if (pūwehe_uara == ']') return mēhua; if (pūwehe_uara != ',') throw new IllegalArgumentException("raraunga pūwehe_uara Pōhēhē");
                }
            }
            if (pūāhua_uara == '"') {
                StringBuilder mēhua = new StringBuilder();
                while (true) {
                    char Panuku_tuemi = pūtake.charAt(tūranga++); if (Panuku_tuemi == '"') return mēhua.toString();
                    if (Panuku_tuemi == '\\') {
                        Panuku_tuemi = pūtake.charAt(tūranga++);
                        if (Panuku_tuemi == 'u') { mēhua.append((char)Integer.parseInt(pūtake.substring(tūranga, tūranga + 4),16)); tūranga += 4; continue; }
                        if (Panuku_tuemi == 'n') Panuku_tuemi = '\n'; else if (Panuku_tuemi == 'r') Panuku_tuemi = '\r'; else if (Panuku_tuemi == 't') Panuku_tuemi = '\t';
                        else if (Panuku_tuemi == 'b') Panuku_tuemi = '\b'; else if (Panuku_tuemi == 'f') Panuku_tuemi = '\f';
                        else if (Panuku_tuemi != '"' && Panuku_tuemi != '\\' && Panuku_tuemi != '/') throw new IllegalArgumentException("문자 이스케이프 Pōhēhē");
                    }
                    mēhua.append(Panuku_tuemi);
                }
            }
            int whakahaere = tūranga - 1;
            while (tūranga < pūtake.length() && ",]} \t\r\n".indexOf(pūtake.charAt(tūranga)) < 0) tūranga++;
            String uara = pūtake.substring(whakahaere, tūranga);
            if (uara.equals("true")) return Boolean.TRUE; if (uara.equals("false")) return Boolean.FALSE; if (uara.equals("null")) return null;
            return Double.valueOf(uara);
        }
    }
    static String hash_kōnae(Path ara) throws Exception {
        MessageDigest 계산 = MessageDigest.getInstance("SHA-256"); byte[] raraunga = new byte[1024 * 1024];
        try (InputStream 입력 = Files.newInputStream(ara)) { for (int roa_uara; (roa_uara = 입력.read(raraunga)) >= 0;) 계산.update(raraunga,0,roa_uara); }
        return hash_TEXT(계산.digest());
    }
    static String hash_TEXT(byte[] raraunga) {
        StringBuilder Ngā_kupu = new StringBuilder(); for (byte uara : raraunga) Ngā_kupu.append(String.format(Locale.ROOT,"%02x",uara & 255)); return Ngā_kupu.toString();
    }
    static Path 내부경로(Path whakaatu_pūtake, String Ingoa) {
        Path mēhua = whakaatu_pūtake.resolve(Ingoa).normalize();
        if (Ingoa.isEmpty() || Paths.get(Ingoa).isAbsolute() || !mēhua.startsWith(whakaatu_pūtake) || Ingoa.indexOf('\\') >= 0)
            throw new IllegalArgumentException("범위를 벗어난 ara: " + Ingoa);
        for (Path 부분 : Paths.get(Ingoa)) if (부분.toString().equals("..")) throw new IllegalArgumentException("상위 ara 금지: " + Ingoa);
        for (Path 현재 = mēhua; 현재 != null && 현재.startsWith(whakaatu_pūtake); 현재 = 현재.getParent())
            if (Files.isSymbolicLink(현재)) throw new IllegalArgumentException("의존성 경로의 링크 금지: " + Ingoa);
        return mēhua;
    }
    static String 명령출력(List<String> tono) throws Exception {
        Process Hātepe_uara = new ProcessBuilder(tono).redirectError(ProcessBuilder.Redirect.INHERIT).start();
        String mēhua = new String(Hātepe_uara.getInputStream().readAllBytes(),StandardCharsets.UTF_8);
        if (Hātepe_uara.waitFor() != 0) throw new IOException("tono rahunga_uara: " + tono.get(0)); return mēhua;
    }
    static void unu(Path Pūranga_uara, Path ūnga_uara) throws Exception {
        for (String Ingoa : 명령출력(Arrays.asList("tar","-tzf",Pūranga_uara.toString())).split("\n")) 내부경로(ūnga_uara, Ingoa);
        for (String hononga : 명령출력(Arrays.asList("tar","-tvzf",Pūranga_uara.toString())).split("\n"))
            if (!hononga.isEmpty() && hononga.charAt(0) != '-' && hononga.charAt(0) != 'd') throw new IOException("외부 링크 또는 특수 파일을 포함한 의존성");
        Files.createDirectories(ūnga_uara);
        int tūnga_uara = new ProcessBuilder("tar","--no-same-owner","--no-same-permissions","-xzf",Pūranga_uara.toString(),"-C",ūnga_uara.toString()).inheritIO().start().waitFor();
        if (tūnga_uara != 0) throw new IOException("의존성 Pūranga_uara tuku_Rokiroki rahunga_uara");
    }
    static void 호출(Path 작업경로, Path Ngā_Utauta, List<String> 인수, Map<String,String> 환경) throws Exception {
        List<String> tono = new ArrayList<>(Arrays.asList("python3", Ngā_Utauta.toString())); tono.addAll(인수);
        ProcessBuilder kawe_tono = new ProcessBuilder(tono).directory(작업경로.toFile()).inheritIO(); kawe_tono.environment().putAll(환경);
        int tūnga_uara = kawe_tono.start().waitFor(); if (tūnga_uara != 0) throw new IOException("Ngā_Utauta rahunga_uara: " + Ngā_Utauta + " (" + tūnga_uara + ")");
    }
    @SuppressWarnings("unchecked")
    public static void main(String[] 인수) throws Exception {
        if (인수.length < 1) throw new IllegalArgumentException("build, run, desktop, image, check, test-system 중 동작을 지정하세요");
        String hohenga = 인수[0];
        if (!Arrays.asList("build","run","desktop","image","check","test-system").contains(hohenga)) throw new IllegalArgumentException("알 수 없는 hohenga");
        Path whakaatu_pūtake = Paths.get(System.getProperty("worldos.edition.root")).toAbsolutePath().normalize();
        Map<String,Object> Ngā_Tautuhinga = (Map<String,Object>)new 자료해석기(Files.readString(whakaatu_pūtake.resolve("native.json"),StandardCharsets.UTF_8)).Pānuitia();
        Path pūtake_rākau = 내부경로(whakaatu_pūtake,(String)Ngā_Tautuhinga.get("source")), kākano_uara_0611a8a8 = 내부경로(pūtake_rākau,(String)Ngā_Tautuhinga.get("native"));
        List<String> 소유파일들 = (List<String>)(List<?>)Ngā_Tautuhinga.get("owned_files");
        for (String Ingoa : 소유파일들) if (!Files.isRegularFile(내부경로(pūtake_rākau,Ingoa))) throw new IOException("pūtake_rākau 없음: " + Ingoa);
        if (hohenga.equals("check")) { System.out.println(Ngā_Tautuhinga.get("country") + " " + Ngā_Tautuhinga.get("language") + " 독립 pūtake_rākau manatoko 완료"); return; }
        String 자원상대 = (String)Ngā_Tautuhinga.getOrDefault("resource_root", ".");
        if (!자원상대.equals(".") && !자원상대.equals("..")) throw new IllegalArgumentException("의존성 whakaatu_pūtake ara Pōhēhē");
        Path rauemi_uara = whakaatu_pūtake.resolve(자원상대).normalize(); Path Pūranga_uara = rauemi_uara.resolve("native-vendor.tar.gz");
        String 기대해시 = (String)Ngā_Tautuhinga.get("vendor_sha256");
        if (!hash_kōnae(Pūranga_uara).equals(기대해시)) throw new IOException("의존성 SHA-256 불일치");
        Path 표식 = pūtake_rākau.resolve(".vendor-sha256");
        if (!Files.isRegularFile(표식) || !Files.readString(표식).trim().equals(기대해시)) { unu(Pūranga_uara, pūtake_rākau); Files.writeString(표식,기대해시 + "\n"); }
        Map<String,String> 환경 = new HashMap<>(System.getenv());
        Path ipConfig = null;
        if (환경.containsKey("IP_CONFIG")) ipConfig = Paths.get(환경.get("IP_CONFIG")).toAbsolutePath().normalize();
        else for (Path parent = whakaatu_pūtake; parent != null; parent = parent.getParent()) {
            if (Files.isRegularFile(parent.resolve("ip.conf"))) { ipConfig = parent.resolve("ip.conf"); break; }
        }
        if (ipConfig == null) ipConfig = pūtake_rākau.resolve("ip.conf");
        if (!Files.isRegularFile(ipConfig)) throw new IOException("Missing ip.conf: " + ipConfig);
        환경.put("IP_CONFIG", ipConfig.toString());
        if (Arrays.asList("run","desktop","test-system").contains(hohenga) && !환경.containsKey("QEMU_AARCH64")) {
            Path kaupapa_pūwhiri_taupānga = rauemi_uara.resolve("host/qemu"), 실행기표식 = rauemi_uara.resolve("host/.qemu-sha256");
            String pūwhiri_taupānga_hash = (String)Ngā_Tautuhinga.get("qemu_sha256");
            if (!Files.isRegularFile(kaupapa_pūwhiri_taupānga) || !Files.isRegularFile(실행기표식) || !Files.readString(실행기표식).trim().equals(pūwhiri_taupānga_hash)) {
                Path pūwhiri_taupānga_Pūranga = rauemi_uara.resolve("qemu-host.tar.gz"); if (!hash_kōnae(pūwhiri_taupānga_Pūranga).equals(pūwhiri_taupānga_hash)) throw new IOException("QEMU SHA-256 불일치");
                unu(pūwhiri_taupānga_Pūranga,rauemi_uara.resolve("host")); Files.writeString(실행기표식,pūwhiri_taupānga_hash + "\n");
            }
            환경.put("QEMU_AARCH64",kaupapa_pūwhiri_taupānga.toString());
        }
        MessageDigest 계산 = MessageDigest.getInstance("SHA-256"); Collections.sort(소유파일들);
        for (String Ingoa : 소유파일들) { 계산.update(Ingoa.getBytes(StandardCharsets.UTF_8)); 계산.update(Files.readAllBytes(내부경로(pūtake_rākau,Ingoa))); }
        계산.update("ip.conf\0".getBytes(StandardCharsets.UTF_8)); 계산.update(Files.readAllBytes(ipConfig));
        String pūtake_hash = hash_TEXT(계산.digest()); Path 빌드표식 = kākano_uara_0611a8a8.resolve("build/worldos-source.sha256");
        if (hohenga.equals("build") || !Files.isRegularFile(빌드표식) || !Files.readString(빌드표식).trim().equals(pūtake_hash)) {
            호출(kākano_uara_0611a8a8,내부경로(kākano_uara_0611a8a8,(String)Ngā_Tautuhinga.get("builder")),Collections.emptyList(),환경);
            Files.writeString(빌드표식,pūtake_hash + "\n");
        }
        List<String> 추가인수 = new ArrayList<>(Arrays.asList(인수).subList(1,인수.length));
        if (hohenga.equals("run") || hohenga.equals("desktop")) {
            if (hohenga.equals("desktop")) 추가인수.add(0,"--desktop");
            호출(kākano_uara_0611a8a8,내부경로(kākano_uara_0611a8a8,(String)Ngā_Tautuhinga.get("runner")),추가인수,환경);
        } else if (hohenga.equals("image")) 호출(kākano_uara_0611a8a8,내부경로(kākano_uara_0611a8a8,(String)Ngā_Tautuhinga.get("image_builder")),추가인수,환경);
        else if (hohenga.equals("test-system")) {
            추가인수.add(0,whakaatu_pūtake.toString()); 추가인수.add(0,"--edition");
            호출(kākano_uara_0611a8a8,내부경로(kākano_uara_0611a8a8,(String)Ngā_Tautuhinga.get("system_tester")),추가인수,환경);
        }
    }
}
