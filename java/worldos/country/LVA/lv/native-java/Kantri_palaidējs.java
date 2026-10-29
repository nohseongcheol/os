// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.security.MessageDigest;
import java.util.*;

/** 독립 국가판의 의존성 검사·복원·būvējums_sistēma·실행을 맡는 viesot Java Rīki. */
public final class Kantri_palaidējs {
    static final class dati_parsētājs {
        final String AVOTS; int Novietojums;
        dati_parsētājs(String Teksts) { AVOTS = Teksts; }
        void 빈칸() { while (Novietojums < AVOTS.length() && Character.isWhitespace(AVOTS.charAt(Novietojums))) Novietojums++; }
        Object Lasīt() {
            빈칸(); char rakstzīme_VALUE = AVOTS.charAt(Novietojums++);
            if (rakstzīme_VALUE == '{') {
                Map<String,Object> mērs = new LinkedHashMap<>(); 빈칸();
                if (AVOTS.charAt(Novietojums) == '}') { Novietojums++; return mērs; }
                while (true) {
                    String Nosaukums = (String)Lasīt(); 빈칸(); if (AVOTS.charAt(Novietojums++) != ':') throw new IllegalArgumentException("dati norobežotājs_VALUE Kļūda");
                    mērs.put(Nosaukums, Lasīt()); 빈칸(); char norobežotājs_VALUE = AVOTS.charAt(Novietojums++);
                    if (norobežotājs_VALUE == '}') return mērs; if (norobežotājs_VALUE != ',') throw new IllegalArgumentException("dati norobežotājs_VALUE Kļūda");
                }
            }
            if (rakstzīme_VALUE == '[') {
                List<Object> mērs = new ArrayList<>(); 빈칸();
                if (AVOTS.charAt(Novietojums) == ']') { Novietojums++; return mērs; }
                while (true) {
                    mērs.add(Lasīt()); 빈칸(); char norobežotājs_VALUE = AVOTS.charAt(Novietojums++);
                    if (norobežotājs_VALUE == ']') return mērs; if (norobežotājs_VALUE != ',') throw new IllegalArgumentException("dati norobežotājs_VALUE Kļūda");
                }
            }
            if (rakstzīme_VALUE == '"') {
                StringBuilder mērs = new StringBuilder();
                while (true) {
                    char Tālāk_krājums = AVOTS.charAt(Novietojums++); if (Tālāk_krājums == '"') return mērs.toString();
                    if (Tālāk_krājums == '\\') {
                        Tālāk_krājums = AVOTS.charAt(Novietojums++);
                        if (Tālāk_krājums == 'u') { mērs.append((char)Integer.parseInt(AVOTS.substring(Novietojums, Novietojums + 4),16)); Novietojums += 4; continue; }
                        if (Tālāk_krājums == 'n') Tālāk_krājums = '\n'; else if (Tālāk_krājums == 'r') Tālāk_krājums = '\r'; else if (Tālāk_krājums == 't') Tālāk_krājums = '\t';
                        else if (Tālāk_krājums == 'b') Tālāk_krājums = '\b'; else if (Tālāk_krājums == 'f') Tālāk_krājums = '\f';
                        else if (Tālāk_krājums != '"' && Tālāk_krājums != '\\' && Tālāk_krājums != '/') throw new IllegalArgumentException("문자 이스케이프 Kļūda");
                    }
                    mērs.append(Tālāk_krājums);
                }
            }
            int Palaist = Novietojums - 1;
            while (Novietojums < AVOTS.length() && ",]} \t\r\n".indexOf(AVOTS.charAt(Novietojums)) < 0) Novietojums++;
            String VALUE = AVOTS.substring(Palaist, Novietojums);
            if (VALUE.equals("true")) return Boolean.TRUE; if (VALUE.equals("false")) return Boolean.FALSE; if (VALUE.equals("null")) return null;
            return Double.valueOf(VALUE);
        }
    }
    static String jaukšana_Fails(Path CEĻŠ) throws Exception {
        MessageDigest 계산 = MessageDigest.getInstance("SHA-256"); byte[] dati = new byte[1024 * 1024];
        try (InputStream 입력 = Files.newInputStream(CEĻŠ)) { for (int 길이; (길이 = 입력.read(dati)) >= 0;) 계산.update(dati,0,길이); }
        return jaukšana_SMS(계산.digest());
    }
    static String jaukšana_SMS(byte[] dati) {
        StringBuilder Teksts = new StringBuilder(); for (byte VALUE : dati) Teksts.append(String.format(Locale.ROOT,"%02x",VALUE & 255)); return Teksts.toString();
    }
    static Path iekšējs_ceļš(Path Project_sakne, String Nosaukums) {
        Path mērs = Project_sakne.resolve(Nosaukums).normalize();
        if (Nosaukums.isEmpty() || Paths.get(Nosaukums).isAbsolute() || !mērs.startsWith(Project_sakne) || Nosaukums.indexOf('\\') >= 0)
            throw new IllegalArgumentException("범위를 벗어난 CEĻŠ: " + Nosaukums);
        for (Path 부분 : Paths.get(Nosaukums)) if (부분.toString().equals("..")) throw new IllegalArgumentException("상위 CEĻŠ 금지: " + Nosaukums);
        for (Path pašreizējais_krājums = mērs; pašreizējais_krājums != null && pašreizējais_krājums.startsWith(Project_sakne); pašreizējais_krājums = pašreizējais_krājums.getParent())
            if (Files.isSymbolicLink(pašreizējais_krājums)) throw new IllegalArgumentException("의존성 경로의 링크 금지: " + Nosaukums);
        return mērs;
    }
    static String komanda_ražojums(List<String> Komanda) throws Exception {
        Process Process_VALUE = new ProcessBuilder(Komanda).redirectError(ProcessBuilder.Redirect.INHERIT).start();
        String mērs = new String(Process_VALUE.getInputStream().readAllBytes(),StandardCharsets.UTF_8);
        if (Process_VALUE.waitFor() != 0) throw new IOException("Komanda kļūme_VALUE: " + Komanda.get(0)); return mērs;
    }
    static void izvilkt(Path Arhīvs_VALUE, Path mērķis_VALUE) throws Exception {
        for (String Nosaukums : komanda_ražojums(Arrays.asList("tar","-tzf",Arhīvs_VALUE.toString())).split("\n")) iekšējs_ceļš(mērķis_VALUE, Nosaukums);
        for (String Līniju : komanda_ražojums(Arrays.asList("tar","-tvzf",Arhīvs_VALUE.toString())).split("\n"))
            if (!Līniju.isEmpty() && Līniju.charAt(0) != '-' && Līniju.charAt(0) != 'd') throw new IOException("ārējs_VALUE 링크 또는 특수 파일을 포함한 의존성");
        Files.createDirectories(mērķis_VALUE);
        int Statuss_VALUE = new ProcessBuilder("tar","--no-same-owner","--no-same-permissions","-xzf",Arhīvs_VALUE.toString(),"-C",mērķis_VALUE.toString()).inheritIO().start().waitFor();
        if (Statuss_VALUE != 0) throw new IOException("의존성 Arhīvs_VALUE izlaist_Krātuve kļūme_VALUE");
    }
    static void 호출(Path 작업경로, Path Rīki, List<String> Parametri, Map<String,String> 환경) throws Exception {
        List<String> Komanda = new ArrayList<>(Arrays.asList("python3", Rīki.toString())); Komanda.addAll(Parametri);
        ProcessBuilder Izpildīt_komanda = new ProcessBuilder(Komanda).directory(작업경로.toFile()).inheritIO(); Izpildīt_komanda.environment().putAll(환경);
        int Statuss_VALUE = Izpildīt_komanda.start().waitFor(); if (Statuss_VALUE != 0) throw new IOException("Rīki kļūme_VALUE: " + Rīki + " (" + Statuss_VALUE + ")");
    }
    @SuppressWarnings("unchecked")
    public static void main(String[] Parametri) throws Exception {
        if (Parametri.length < 1) throw new IllegalArgumentException("build, run, desktop, image, check, test-system 중 동작을 지정하세요");
        String Darbība = Parametri[0];
        if (!Arrays.asList("build","run","desktop","image","check","test-system").contains(Darbība)) throw new IllegalArgumentException("알 numurs 없는 Darbība");
        Path Project_sakne = Paths.get(System.getProperty("worldos.edition.root")).toAbsolutePath().normalize();
        Map<String,Object> Uzstādījumi = (Map<String,Object>)new dati_parsētājs(Files.readString(Project_sakne.resolve("native.json"),StandardCharsets.UTF_8)).Lasīt();
        Path avots_koks = iekšējs_ceļš(Project_sakne,(String)Uzstādījumi.get("source")), kodols_VALUE = iekšējs_ceļš(avots_koks,(String)Uzstādījumi.get("native"));
        List<String> 소유파일들 = (List<String>)(List<?>)Uzstādījumi.get("owned_files");
        for (String Nosaukums : 소유파일들) if (!Files.isRegularFile(iekšējs_ceļš(avots_koks,Nosaukums))) throw new IOException("avots_koks 없음: " + Nosaukums);
        if (Darbība.equals("check")) { System.out.println(Uzstādījumi.get("country") + " " + Uzstādījumi.get("language") + " 독립 avots_koks verificēt 완료"); return; }
        String resurss_relatīvais_ceļš = (String)Uzstādījumi.getOrDefault("resource_root", ".");
        if (!resurss_relatīvais_ceļš.equals(".") && !resurss_relatīvais_ceļš.equals("..")) throw new IllegalArgumentException("의존성 Project_sakne CEĻŠ Kļūda");
        Path resurss_VALUE = Project_sakne.resolve(resurss_relatīvais_ceļš).normalize(); Path Arhīvs_VALUE = resurss_VALUE.resolve("native-vendor.tar.gz");
        String 기대해시 = (String)Uzstādījumi.get("vendor_sha256");
        if (!jaukšana_Fails(Arhīvs_VALUE).equals(기대해시)) throw new IOException("의존성 SHA-256 불일치");
        Path marķieris_VALUE = avots_koks.resolve(".vendor-sha256");
        if (!Files.isRegularFile(marķieris_VALUE) || !Files.readString(marķieris_VALUE).trim().equals(기대해시)) { izvilkt(Arhīvs_VALUE, avots_koks); Files.writeString(marķieris_VALUE,기대해시 + "\n"); }
        Map<String,String> 환경 = new HashMap<>(System.getenv());
        Path ipConfig = null;
        if (환경.containsKey("IP_CONFIG")) ipConfig = Paths.get(환경.get("IP_CONFIG")).toAbsolutePath().normalize();
        else for (Path parent = Project_sakne; parent != null; parent = parent.getParent()) {
            if (Files.isRegularFile(parent.resolve("ip.conf"))) { ipConfig = parent.resolve("ip.conf"); break; }
        }
        if (ipConfig == null) ipConfig = avots_koks.resolve("ip.conf");
        if (!Files.isRegularFile(ipConfig)) throw new IOException("Missing ip.conf: " + ipConfig);
        환경.put("IP_CONFIG", ipConfig.toString());
        if (Arrays.asList("run","desktop","test-system").contains(Darbība) && !환경.containsKey("QEMU_AARCH64")) {
            Path programma_palaidējs = resurss_VALUE.resolve("host/qemu"), palaidējs_marķieris = resurss_VALUE.resolve("host/.qemu-sha256");
            String palaidējs_jaukšana = (String)Uzstādījumi.get("qemu_sha256");
            if (!Files.isRegularFile(programma_palaidējs) || !Files.isRegularFile(palaidējs_marķieris) || !Files.readString(palaidējs_marķieris).trim().equals(palaidējs_jaukšana)) {
                Path palaidējs_Arhīvs = resurss_VALUE.resolve("qemu-host.tar.gz"); if (!jaukšana_Fails(palaidējs_Arhīvs).equals(palaidējs_jaukšana)) throw new IOException("QEMU SHA-256 불일치");
                izvilkt(palaidējs_Arhīvs,resurss_VALUE.resolve("host")); Files.writeString(palaidējs_marķieris,palaidējs_jaukšana + "\n");
            }
            환경.put("QEMU_AARCH64",programma_palaidējs.toString());
        }
        MessageDigest 계산 = MessageDigest.getInstance("SHA-256"); Collections.sort(소유파일들);
        for (String Nosaukums : 소유파일들) { 계산.update(Nosaukums.getBytes(StandardCharsets.UTF_8)); 계산.update(Files.readAllBytes(iekšējs_ceļš(avots_koks,Nosaukums))); }
        계산.update("ip.conf\0".getBytes(StandardCharsets.UTF_8)); 계산.update(Files.readAllBytes(ipConfig));
        String avots_jaukšana = jaukšana_SMS(계산.digest()); Path būvējums_marķieris = kodols_VALUE.resolve("build/worldos-source.sha256");
        if (Darbība.equals("build") || !Files.isRegularFile(būvējums_marķieris) || !Files.readString(būvējums_marķieris).trim().equals(avots_jaukšana)) {
            호출(kodols_VALUE,iekšējs_ceļš(kodols_VALUE,(String)Uzstādījumi.get("builder")),Collections.emptyList(),환경);
            Files.writeString(būvējums_marķieris,avots_jaukšana + "\n");
        }
        List<String> 추가인수 = new ArrayList<>(Arrays.asList(Parametri).subList(1,Parametri.length));
        if (Darbība.equals("run") || Darbība.equals("desktop")) {
            if (Darbība.equals("desktop")) 추가인수.add(0,"--desktop");
            호출(kodols_VALUE,iekšējs_ceļš(kodols_VALUE,(String)Uzstādījumi.get("runner")),추가인수,환경);
        } else if (Darbība.equals("image")) 호출(kodols_VALUE,iekšējs_ceļš(kodols_VALUE,(String)Uzstādījumi.get("image_builder")),추가인수,환경);
        else if (Darbība.equals("test-system")) {
            추가인수.add(0,Project_sakne.toString()); 추가인수.add(0,"--edition");
            호출(kodols_VALUE,iekšējs_ceļš(kodols_VALUE,(String)Uzstādījumi.get("system_tester")),추가인수,환경);
        }
    }
}
