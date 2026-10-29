// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.security.MessageDigest;
import java.util.*;

/** 독립 국가판의 의존성 검사·복원·yakha_inkqubo·실행을 맡는 umsingathi Java Izixhobo. */
public final class 국가실행기 {
    static final class 자료해석기 {
        final String UMTHOMBO; int 위치;
        자료해석기(String Umbhalo) { UMTHOMBO = Umbhalo; }
        void 빈칸() { while (위치 < UMTHOMBO.length() && Character.isWhitespace(UMTHOMBO.charAt(위치))) 위치++; }
        Object Funda() {
            빈칸(); char ikharakhtha_ixabiso = UMTHOMBO.charAt(위치++);
            if (ikharakhtha_ixabiso == '{') {
                Map<String,Object> 결과 = new LinkedHashMap<>(); 빈칸();
                if (UMTHOMBO.charAt(위치) == '}') { 위치++; return 결과; }
                while (true) {
                    String Igama = (String)Funda(); 빈칸(); if (UMTHOMBO.charAt(위치++) != ':') throw new IllegalArgumentException("iingcombolo isinqandi_esimiselweyo_ixabiso Impazamo");
                    결과.put(Igama, Funda()); 빈칸(); char isinqandi_esimiselweyo_ixabiso = UMTHOMBO.charAt(위치++);
                    if (isinqandi_esimiselweyo_ixabiso == '}') return 결과; if (isinqandi_esimiselweyo_ixabiso != ',') throw new IllegalArgumentException("iingcombolo isinqandi_esimiselweyo_ixabiso Impazamo");
                }
            }
            if (ikharakhtha_ixabiso == '[') {
                List<Object> 결과 = new ArrayList<>(); 빈칸();
                if (UMTHOMBO.charAt(위치) == ']') { 위치++; return 결과; }
                while (true) {
                    결과.add(Funda()); 빈칸(); char isinqandi_esimiselweyo_ixabiso = UMTHOMBO.charAt(위치++);
                    if (isinqandi_esimiselweyo_ixabiso == ']') return 결과; if (isinqandi_esimiselweyo_ixabiso != ',') throw new IllegalArgumentException("iingcombolo isinqandi_esimiselweyo_ixabiso Impazamo");
                }
            }
            if (ikharakhtha_ixabiso == '"') {
                StringBuilder 결과 = new StringBuilder();
                while (true) {
                    char 다음 = UMTHOMBO.charAt(위치++); if (다음 == '"') return 결과.toString();
                    if (다음 == '\\') {
                        다음 = UMTHOMBO.charAt(위치++);
                        if (다음 == 'u') { 결과.append((char)Integer.parseInt(UMTHOMBO.substring(위치, 위치 + 4),16)); 위치 += 4; continue; }
                        if (다음 == 'n') 다음 = '\n'; else if (다음 == 'r') 다음 = '\r'; else if (다음 == 't') 다음 = '\t';
                        else if (다음 == 'b') 다음 = '\b'; else if (다음 == 'f') 다음 = '\f';
                        else if (다음 != '"' && 다음 != '\\' && 다음 != '/') throw new IllegalArgumentException("문자 이스케이프 Impazamo");
                    }
                    결과.append(다음);
                }
            }
            int Phumeza = 위치 - 1;
            while (위치 < UMTHOMBO.length() && ",]} \t\r\n".indexOf(UMTHOMBO.charAt(위치)) < 0) 위치++;
            String ixabiso = UMTHOMBO.substring(Phumeza, 위치);
            if (ixabiso.equals("true")) return Boolean.TRUE; if (ixabiso.equals("false")) return Boolean.FALSE; if (ixabiso.equals("null")) return null;
            return Double.valueOf(ixabiso);
        }
    }
    static String i_hash_ifayile(Path INDLELA) throws Exception {
        MessageDigest 계산 = MessageDigest.getInstance("SHA-256"); byte[] iingcombolo = new byte[1024 * 1024];
        try (InputStream 입력 = Files.newInputStream(INDLELA)) { for (int ubude_ixabiso; (ubude_ixabiso = 입력.read(iingcombolo)) >= 0;) 계산.update(iingcombolo,0,ubude_ixabiso); }
        return i_hash_I_SMS(계산.digest());
    }
    static String i_hash_I_SMS(byte[] iingcombolo) {
        StringBuilder Umbhalo = new StringBuilder(); for (byte ixabiso : iingcombolo) Umbhalo.append(String.format(Locale.ROOT,"%02x",ixabiso & 255)); return Umbhalo.toString();
    }
    static Path 내부경로(Path 기준, String Igama) {
        Path 결과 = 기준.resolve(Igama).normalize();
        if (Igama.isEmpty() || Paths.get(Igama).isAbsolute() || !결과.startsWith(기준) || Igama.indexOf('\\') >= 0)
            throw new IllegalArgumentException("범위를 벗어난 INDLELA: " + Igama);
        for (Path 부분 : Paths.get(Igama)) if (부분.toString().equals("..")) throw new IllegalArgumentException("상위 INDLELA 금지: " + Igama);
        for (Path 현재 = 결과; 현재 != null && 현재.startsWith(기준); 현재 = 현재.getParent())
            if (Files.isSymbolicLink(현재)) throw new IllegalArgumentException("의존성 경로의 링크 금지: " + Igama);
        return 결과;
    }
    static String 명령출력(List<String> Umyalelo) throws Exception {
        Process Inkqubo_ixabiso = new ProcessBuilder(Umyalelo).redirectError(ProcessBuilder.Redirect.INHERIT).start();
        String 결과 = new String(Inkqubo_ixabiso.getInputStream().readAllBytes(),StandardCharsets.UTF_8);
        if (Inkqubo_ixabiso.waitFor() != 0) throw new IOException("Umyalelo ukungaphumeleli_ixabiso: " + Umyalelo.get(0)); return 결과;
    }
    static void isicatshulwa(Path Uvimba_ixabiso, Path indawo_ekuyiwa_kuyo_ixabiso) throws Exception {
        for (String Igama : 명령출력(Arrays.asList("tar","-tzf",Uvimba_ixabiso.toString())).split("\n")) 내부경로(indawo_ekuyiwa_kuyo_ixabiso, Igama);
        for (String umgca : 명령출력(Arrays.asList("tar","-tvzf",Uvimba_ixabiso.toString())).split("\n"))
            if (!umgca.isEmpty() && umgca.charAt(0) != '-' && umgca.charAt(0) != 'd') throw new IOException("외부 링크 또는 특수 파일을 포함한 의존성");
        Files.createDirectories(indawo_ekuyiwa_kuyo_ixabiso);
        int imo_ixabiso = new ProcessBuilder("tar","--no-same-owner","--no-same-permissions","-xzf",Uvimba_ixabiso.toString(),"-C",indawo_ekuyiwa_kuyo_ixabiso.toString()).inheritIO().start().waitFor();
        if (imo_ixabiso != 0) throw new IOException("의존성 Uvimba_ixabiso vulela_Ugcino ukungaphumeleli_ixabiso");
    }
    static void 호출(Path 작업경로, Path Izixhobo, List<String> 인수, Map<String,String> 환경) throws Exception {
        List<String> Umyalelo = new ArrayList<>(Arrays.asList("python3", Izixhobo.toString())); Umyalelo.addAll(인수);
        ProcessBuilder ukwenza_umyalelo = new ProcessBuilder(Umyalelo).directory(작업경로.toFile()).inheritIO(); ukwenza_umyalelo.environment().putAll(환경);
        int imo_ixabiso = ukwenza_umyalelo.start().waitFor(); if (imo_ixabiso != 0) throw new IOException("Izixhobo ukungaphumeleli_ixabiso: " + Izixhobo + " (" + imo_ixabiso + ")");
    }
    @SuppressWarnings("unchecked")
    public static void main(String[] 인수) throws Exception {
        if (인수.length < 1) throw new IllegalArgumentException("build, run, desktop, image, check, test-system 중 동작을 지정하세요");
        String Intshukumo = 인수[0];
        if (!Arrays.asList("build","run","desktop","image","check","test-system").contains(Intshukumo)) throw new IllegalArgumentException("알 수 없는 Intshukumo");
        Path 기준 = Paths.get(System.getProperty("worldos.edition.root")).toAbsolutePath().normalize();
        Map<String,Object> Imimiselo = (Map<String,Object>)new 자료해석기(Files.readString(기준.resolve("native.json"),StandardCharsets.UTF_8)).Funda();
        Path umthombo_umthi = 내부경로(기준,(String)Imimiselo.get("source")), ikheneli_ixabiso = 내부경로(umthombo_umthi,(String)Imimiselo.get("native"));
        List<String> 소유파일들 = (List<String>)(List<?>)Imimiselo.get("owned_files");
        for (String Igama : 소유파일들) if (!Files.isRegularFile(내부경로(umthombo_umthi,Igama))) throw new IOException("umthombo_umthi 없음: " + Igama);
        if (Intshukumo.equals("check")) { System.out.println(Imimiselo.get("country") + " " + Imimiselo.get("language") + " 독립 umthombo_umthi ngqinisisa 완료"); return; }
        String 자원상대 = (String)Imimiselo.getOrDefault("resource_root", ".");
        if (!자원상대.equals(".") && !자원상대.equals("..")) throw new IllegalArgumentException("의존성 기준 INDLELA Impazamo");
        Path isixhobo_sekhompyutha_ixabiso = 기준.resolve(자원상대).normalize(); Path Uvimba_ixabiso = isixhobo_sekhompyutha_ixabiso.resolve("native-vendor.tar.gz");
        String 기대해시 = (String)Imimiselo.get("vendor_sha256");
        if (!i_hash_ifayile(Uvimba_ixabiso).equals(기대해시)) throw new IOException("의존성 SHA-256 불일치");
        Path 표식 = umthombo_umthi.resolve(".vendor-sha256");
        if (!Files.isRegularFile(표식) || !Files.readString(표식).trim().equals(기대해시)) { isicatshulwa(Uvimba_ixabiso, umthombo_umthi); Files.writeString(표식,기대해시 + "\n"); }
        Map<String,String> 환경 = new HashMap<>(System.getenv());
        Path ipConfig = null;
        if (환경.containsKey("IP_CONFIG")) ipConfig = Paths.get(환경.get("IP_CONFIG")).toAbsolutePath().normalize();
        else for (Path parent = 기준; parent != null; parent = parent.getParent()) {
            if (Files.isRegularFile(parent.resolve("ip.conf"))) { ipConfig = parent.resolve("ip.conf"); break; }
        }
        if (ipConfig == null) ipConfig = umthombo_umthi.resolve("ip.conf");
        if (!Files.isRegularFile(ipConfig)) throw new IOException("Missing ip.conf: " + ipConfig);
        환경.put("IP_CONFIG", ipConfig.toString());
        if (Arrays.asList("run","desktop","test-system").contains(Intshukumo) && !환경.containsKey("QEMU_AARCH64")) {
            Path inkqubo_idrowa_yosetyenziso = isixhobo_sekhompyutha_ixabiso.resolve("host/qemu"), 실행기표식 = isixhobo_sekhompyutha_ixabiso.resolve("host/.qemu-sha256");
            String idrowa_yosetyenziso_i_hash = (String)Imimiselo.get("qemu_sha256");
            if (!Files.isRegularFile(inkqubo_idrowa_yosetyenziso) || !Files.isRegularFile(실행기표식) || !Files.readString(실행기표식).trim().equals(idrowa_yosetyenziso_i_hash)) {
                Path idrowa_yosetyenziso_Uvimba = isixhobo_sekhompyutha_ixabiso.resolve("qemu-host.tar.gz"); if (!i_hash_ifayile(idrowa_yosetyenziso_Uvimba).equals(idrowa_yosetyenziso_i_hash)) throw new IOException("QEMU SHA-256 불일치");
                isicatshulwa(idrowa_yosetyenziso_Uvimba,isixhobo_sekhompyutha_ixabiso.resolve("host")); Files.writeString(실행기표식,idrowa_yosetyenziso_i_hash + "\n");
            }
            환경.put("QEMU_AARCH64",inkqubo_idrowa_yosetyenziso.toString());
        }
        MessageDigest 계산 = MessageDigest.getInstance("SHA-256"); Collections.sort(소유파일들);
        for (String Igama : 소유파일들) { 계산.update(Igama.getBytes(StandardCharsets.UTF_8)); 계산.update(Files.readAllBytes(내부경로(umthombo_umthi,Igama))); }
        계산.update("ip.conf\0".getBytes(StandardCharsets.UTF_8)); 계산.update(Files.readAllBytes(ipConfig));
        String umthombo_i_hash = i_hash_I_SMS(계산.digest()); Path 빌드표식 = ikheneli_ixabiso.resolve("build/worldos-source.sha256");
        if (Intshukumo.equals("build") || !Files.isRegularFile(빌드표식) || !Files.readString(빌드표식).trim().equals(umthombo_i_hash)) {
            호출(ikheneli_ixabiso,내부경로(ikheneli_ixabiso,(String)Imimiselo.get("builder")),Collections.emptyList(),환경);
            Files.writeString(빌드표식,umthombo_i_hash + "\n");
        }
        List<String> 추가인수 = new ArrayList<>(Arrays.asList(인수).subList(1,인수.length));
        if (Intshukumo.equals("run") || Intshukumo.equals("desktop")) {
            if (Intshukumo.equals("desktop")) 추가인수.add(0,"--desktop");
            호출(ikheneli_ixabiso,내부경로(ikheneli_ixabiso,(String)Imimiselo.get("runner")),추가인수,환경);
        } else if (Intshukumo.equals("image")) 호출(ikheneli_ixabiso,내부경로(ikheneli_ixabiso,(String)Imimiselo.get("image_builder")),추가인수,환경);
        else if (Intshukumo.equals("test-system")) {
            추가인수.add(0,기준.toString()); 추가인수.add(0,"--edition");
            호출(ikheneli_ixabiso,내부경로(ikheneli_ixabiso,(String)Imimiselo.get("system_tester")),추가인수,환경);
        }
    }
}
