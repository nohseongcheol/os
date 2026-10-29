// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.security.MessageDigest;
import java.util.*;

/** 독립 국가판의 의존성 검사·복원·wue_sistèm·실행을 맡는 usu Java Ngwaọrụ. */
public final class 국가실행기 {
    static final class 자료해석기 {
        final String ebensìbịa; int 위치;
        자료해석기(String SMS) { ebensìbịa = SMS; }
        void 빈칸() { while (위치 < ebensìbịa.length() && Character.isWhitespace(ebensìbịa.charAt(위치))) 위치++; }
        Object Wepụta_ọzi() {
            빈칸(); char mkpụrụedemede_valuu = ebensìbịa.charAt(위치++);
            if (mkpụrụedemede_valuu == '{') {
                Map<String,Object> 결과 = new LinkedHashMap<>(); 빈칸();
                if (ebensìbịa.charAt(위치) == '}') { 위치++; return 결과; }
                while (true) {
                    String Aha = (String)Wepụta_ọzi(); 빈칸(); if (ebensìbịa.charAt(위치++) != ':') throw new IllegalArgumentException("datà nzinjedebe_valuu mmejọ");
                    결과.put(Aha, Wepụta_ọzi()); 빈칸(); char nzinjedebe_valuu = ebensìbịa.charAt(위치++);
                    if (nzinjedebe_valuu == '}') return 결과; if (nzinjedebe_valuu != ',') throw new IllegalArgumentException("datà nzinjedebe_valuu mmejọ");
                }
            }
            if (mkpụrụedemede_valuu == '[') {
                List<Object> 결과 = new ArrayList<>(); 빈칸();
                if (ebensìbịa.charAt(위치) == ']') { 위치++; return 결과; }
                while (true) {
                    결과.add(Wepụta_ọzi()); 빈칸(); char nzinjedebe_valuu = ebensìbịa.charAt(위치++);
                    if (nzinjedebe_valuu == ']') return 결과; if (nzinjedebe_valuu != ',') throw new IllegalArgumentException("datà nzinjedebe_valuu mmejọ");
                }
            }
            if (mkpụrụedemede_valuu == '"') {
                StringBuilder 결과 = new StringBuilder();
                while (true) {
                    char 다음 = ebensìbịa.charAt(위치++); if (다음 == '"') return 결과.toString();
                    if (다음 == '\\') {
                        다음 = ebensìbịa.charAt(위치++);
                        if (다음 == 'u') { 결과.append((char)Integer.parseInt(ebensìbịa.substring(위치, 위치 + 4),16)); 위치 += 4; continue; }
                        if (다음 == 'n') 다음 = '\n'; else if (다음 == 'r') 다음 = '\r'; else if (다음 == 't') 다음 = '\t';
                        else if (다음 == 'b') 다음 = '\b'; else if (다음 == 'f') 다음 = '\f';
                        else if (다음 != '"' && 다음 != '\\' && 다음 != '/') throw new IllegalArgumentException("문자 이스케이프 mmejọ");
                    }
                    결과.append(다음);
                }
            }
            int Bido = 위치 - 1;
            while (위치 < ebensìbịa.length() && ",]} \t\r\n".indexOf(ebensìbịa.charAt(위치)) < 0) 위치++;
            String valuu = ebensìbịa.substring(Bido, 위치);
            if (valuu.equals("true")) return Boolean.TRUE; if (valuu.equals("false")) return Boolean.FALSE; if (valuu.equals("null")) return null;
            return Double.valueOf(valuu);
        }
    }
    static String di_ike_ọbọakwụkwọ(Path ụzọ_ozi) throws Exception {
        MessageDigest 계산 = MessageDigest.getInstance("SHA-256"); byte[] datà = new byte[1024 * 1024];
        try (InputStream 입력 = Files.newInputStream(ụzọ_ozi)) { for (int ogologo_valuu; (ogologo_valuu = 입력.read(datà)) >= 0;) 계산.update(datà,0,ogologo_valuu); }
        return di_ike_SMS(계산.digest());
    }
    static String di_ike_SMS(byte[] datà) {
        StringBuilder SMS = new StringBuilder(); for (byte valuu : datà) SMS.append(String.format(Locale.ROOT,"%02x",valuu & 255)); return SMS.toString();
    }
    static Path 내부경로(Path 기준, String Aha) {
        Path 결과 = 기준.resolve(Aha).normalize();
        if (Aha.isEmpty() || Paths.get(Aha).isAbsolute() || !결과.startsWith(기준) || Aha.indexOf('\\') >= 0)
            throw new IllegalArgumentException("범위를 벗어난 ụzọ_ozi: " + Aha);
        for (Path 부분 : Paths.get(Aha)) if (부분.toString().equals("..")) throw new IllegalArgumentException("상위 ụzọ_ozi 금지: " + Aha);
        for (Path 현재 = 결과; 현재 != null && 현재.startsWith(기준); 현재 = 현재.getParent())
            if (Files.isSymbolicLink(현재)) throw new IllegalArgumentException("의존성 경로의 링크 금지: " + Aha);
        return 결과;
    }
    static String 명령출력(List<String> Ntiiwu) throws Exception {
        Process ùsòrò_valuu_6712bde7 = new ProcessBuilder(Ntiiwu).redirectError(ProcessBuilder.Redirect.INHERIT).start();
        String 결과 = new String(ùsòrò_valuu_6712bde7.getInputStream().readAllBytes(),StandardCharsets.UTF_8);
        if (ùsòrò_valuu_6712bde7.waitFor() != 0) throw new IOException("Ntiiwu ọdịdà_valuu: " + Ntiiwu.get(0)); return 결과;
    }
    static void mwepụta(Path ọkpụ_valuu, Path ebemwèga_valuu) throws Exception {
        for (String Aha : 명령출력(Arrays.asList("tar","-tzf",ọkpụ_valuu.toString())).split("\n")) 내부경로(ebemwèga_valuu, Aha);
        for (String ahịrī : 명령출력(Arrays.asList("tar","-tvzf",ọkpụ_valuu.toString())).split("\n"))
            if (!ahịrī.isEmpty() && ahịrī.charAt(0) != '-' && ahịrī.charAt(0) != 'd') throw new IOException("외부 링크 또는 특수 파일을 포함한 의존성");
        Files.createDirectories(ebemwèga_valuu);
        int ọnọdụ_valuu = new ProcessBuilder("tar","--no-same-owner","--no-same-permissions","-xzf",ọkpụ_valuu.toString(),"-C",ebemwèga_valuu.toString()).inheritIO().start().waitFor();
        if (ọnọdụ_valuu != 0) throw new IOException("의존성 ọkpụ_valuu bupute_Nchekwa ọdịdà_valuu");
    }
    static void 호출(Path 작업경로, Path Ngwaọrụ, List<String> 인수, Map<String,String> 환경) throws Exception {
        List<String> Ntiiwu = new ArrayList<>(Arrays.asList("python3", Ngwaọrụ.toString())); Ntiiwu.addAll(인수);
        ProcessBuilder mee_nnyemiwu = new ProcessBuilder(Ntiiwu).directory(작업경로.toFile()).inheritIO(); mee_nnyemiwu.environment().putAll(환경);
        int ọnọdụ_valuu = mee_nnyemiwu.start().waitFor(); if (ọnọdụ_valuu != 0) throw new IOException("Ngwaọrụ ọdịdà_valuu: " + Ngwaọrụ + " (" + ọnọdụ_valuu + ")");
    }
    @SuppressWarnings("unchecked")
    public static void main(String[] 인수) throws Exception {
        if (인수.length < 1) throw new IllegalArgumentException("build, run, desktop, image, check, test-system 중 동작을 지정하세요");
        String mmèm = 인수[0];
        if (!Arrays.asList("build","run","desktop","image","check","test-system").contains(mmèm)) throw new IllegalArgumentException("알 수 없는 mmèm");
        Path 기준 = Paths.get(System.getProperty("worldos.edition.root")).toAbsolutePath().normalize();
        Map<String,Object> Mwube = (Map<String,Object>)new 자료해석기(Files.readString(기준.resolve("native.json"),StandardCharsets.UTF_8)).Wepụta_ọzi();
        Path ebensìbịa_èsèrèsè_osisi = 내부경로(기준,(String)Mwube.get("source")), mkpụrụobī_kọmpùta_valuu = 내부경로(ebensìbịa_èsèrèsè_osisi,(String)Mwube.get("native"));
        List<String> 소유파일들 = (List<String>)(List<?>)Mwube.get("owned_files");
        for (String Aha : 소유파일들) if (!Files.isRegularFile(내부경로(ebensìbịa_èsèrèsè_osisi,Aha))) throw new IOException("ebensìbịa_èsèrèsè_osisi 없음: " + Aha);
        if (mmèm.equals("check")) { System.out.println(Mwube.get("country") + " " + Mwube.get("language") + " 독립 ebensìbịa_èsèrèsè_osisi nkwàdo_eziokwū 완료"); return; }
        String 자원상대 = (String)Mwube.getOrDefault("resource_root", ".");
        if (!자원상대.equals(".") && !자원상대.equals("..")) throw new IllegalArgumentException("의존성 기준 ụzọ_ozi mmejọ");
        Path njìàrụọrụ_valuu = 기준.resolve(자원상대).normalize(); Path ọkpụ_valuu = njìàrụọrụ_valuu.resolve("native-vendor.tar.gz");
        String 기대해시 = (String)Mwube.get("vendor_sha256");
        if (!di_ike_ọbọakwụkwọ(ọkpụ_valuu).equals(기대해시)) throw new IOException("의존성 SHA-256 불일치");
        Path 표식 = ebensìbịa_èsèrèsè_osisi.resolve(".vendor-sha256");
        if (!Files.isRegularFile(표식) || !Files.readString(표식).trim().equals(기대해시)) { mwepụta(ọkpụ_valuu, ebensìbịa_èsèrèsè_osisi); Files.writeString(표식,기대해시 + "\n"); }
        Map<String,String> 환경 = new HashMap<>(System.getenv());
        Path ipConfig = null;
        if (환경.containsKey("IP_CONFIG")) ipConfig = Paths.get(환경.get("IP_CONFIG")).toAbsolutePath().normalize();
        else for (Path parent = 기준; parent != null; parent = parent.getParent()) {
            if (Files.isRegularFile(parent.resolve("ip.conf"))) { ipConfig = parent.resolve("ip.conf"); break; }
        }
        if (ipConfig == null) ipConfig = ebensìbịa_èsèrèsè_osisi.resolve("ip.conf");
        if (!Files.isRegularFile(ipConfig)) throw new IOException("Missing ip.conf: " + ipConfig);
        환경.put("IP_CONFIG", ipConfig.toString());
        if (Arrays.asList("run","desktop","test-system").contains(mmèm) && !환경.containsKey("QEMU_AARCH64")) {
            Path app_ihengosi_ndi_app = njìàrụọrụ_valuu.resolve("host/qemu"), 실행기표식 = njìàrụọrụ_valuu.resolve("host/.qemu-sha256");
            String ihengosi_ndi_app_di_ike = (String)Mwube.get("qemu_sha256");
            if (!Files.isRegularFile(app_ihengosi_ndi_app) || !Files.isRegularFile(실행기표식) || !Files.readString(실행기표식).trim().equals(ihengosi_ndi_app_di_ike)) {
                Path ihengosi_ndi_app_ọkpụ = njìàrụọrụ_valuu.resolve("qemu-host.tar.gz"); if (!di_ike_ọbọakwụkwọ(ihengosi_ndi_app_ọkpụ).equals(ihengosi_ndi_app_di_ike)) throw new IOException("QEMU SHA-256 불일치");
                mwepụta(ihengosi_ndi_app_ọkpụ,njìàrụọrụ_valuu.resolve("host")); Files.writeString(실행기표식,ihengosi_ndi_app_di_ike + "\n");
            }
            환경.put("QEMU_AARCH64",app_ihengosi_ndi_app.toString());
        }
        MessageDigest 계산 = MessageDigest.getInstance("SHA-256"); Collections.sort(소유파일들);
        for (String Aha : 소유파일들) { 계산.update(Aha.getBytes(StandardCharsets.UTF_8)); 계산.update(Files.readAllBytes(내부경로(ebensìbịa_èsèrèsè_osisi,Aha))); }
        계산.update("ip.conf\0".getBytes(StandardCharsets.UTF_8)); 계산.update(Files.readAllBytes(ipConfig));
        String ebensìbịa_di_ike = di_ike_SMS(계산.digest()); Path 빌드표식 = mkpụrụobī_kọmpùta_valuu.resolve("build/worldos-source.sha256");
        if (mmèm.equals("build") || !Files.isRegularFile(빌드표식) || !Files.readString(빌드표식).trim().equals(ebensìbịa_di_ike)) {
            호출(mkpụrụobī_kọmpùta_valuu,내부경로(mkpụrụobī_kọmpùta_valuu,(String)Mwube.get("builder")),Collections.emptyList(),환경);
            Files.writeString(빌드표식,ebensìbịa_di_ike + "\n");
        }
        List<String> 추가인수 = new ArrayList<>(Arrays.asList(인수).subList(1,인수.length));
        if (mmèm.equals("run") || mmèm.equals("desktop")) {
            if (mmèm.equals("desktop")) 추가인수.add(0,"--desktop");
            호출(mkpụrụobī_kọmpùta_valuu,내부경로(mkpụrụobī_kọmpùta_valuu,(String)Mwube.get("runner")),추가인수,환경);
        } else if (mmèm.equals("image")) 호출(mkpụrụobī_kọmpùta_valuu,내부경로(mkpụrụobī_kọmpùta_valuu,(String)Mwube.get("image_builder")),추가인수,환경);
        else if (mmèm.equals("test-system")) {
            추가인수.add(0,기준.toString()); 추가인수.add(0,"--edition");
            호출(mkpụrụobī_kọmpùta_valuu,내부경로(mkpụrụobī_kọmpùta_valuu,(String)Mwube.get("system_tester")),추가인수,환경);
        }
    }
}
