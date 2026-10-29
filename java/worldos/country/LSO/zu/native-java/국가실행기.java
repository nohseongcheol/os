// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.security.MessageDigest;
import java.util.*;

/** 독립 국가판의 의존성 검사·복원·akha_isistimu·실행을 맡는 singatha Java Amathuluzi. */
public final class 국가실행기 {
    static final class 자료해석기 {
        final String umthombo; int 위치;
        자료해석기(String Itekisi) { umthombo = Itekisi; }
        void 빈칸() { while (위치 < umthombo.length() && Character.isWhitespace(umthombo.charAt(위치))) 위치++; }
        Object Funda() {
            빈칸(); char uhlamvusimo_inani = umthombo.charAt(위치++);
            if (uhlamvusimo_inani == '{') {
                Map<String,Object> 결과 = new LinkedHashMap<>(); 빈칸();
                if (umthombo.charAt(위치) == '}') { 위치++; return 결과; }
                while (true) {
                    String Igama = (String)Funda(); 빈칸(); if (umthombo.charAt(위치++) != ':') throw new IllegalArgumentException("imininingwane okunqandayo_inani Iphutha");
                    결과.put(Igama, Funda()); 빈칸(); char okunqandayo_inani = umthombo.charAt(위치++);
                    if (okunqandayo_inani == '}') return 결과; if (okunqandayo_inani != ',') throw new IllegalArgumentException("imininingwane okunqandayo_inani Iphutha");
                }
            }
            if (uhlamvusimo_inani == '[') {
                List<Object> 결과 = new ArrayList<>(); 빈칸();
                if (umthombo.charAt(위치) == ']') { 위치++; return 결과; }
                while (true) {
                    결과.add(Funda()); 빈칸(); char okunqandayo_inani = umthombo.charAt(위치++);
                    if (okunqandayo_inani == ']') return 결과; if (okunqandayo_inani != ',') throw new IllegalArgumentException("imininingwane okunqandayo_inani Iphutha");
                }
            }
            if (uhlamvusimo_inani == '"') {
                StringBuilder 결과 = new StringBuilder();
                while (true) {
                    char 다음 = umthombo.charAt(위치++); if (다음 == '"') return 결과.toString();
                    if (다음 == '\\') {
                        다음 = umthombo.charAt(위치++);
                        if (다음 == 'u') { 결과.append((char)Integer.parseInt(umthombo.substring(위치, 위치 + 4),16)); 위치 += 4; continue; }
                        if (다음 == 'n') 다음 = '\n'; else if (다음 == 'r') 다음 = '\r'; else if (다음 == 't') 다음 = '\t';
                        else if (다음 == 'b') 다음 = '\b'; else if (다음 == 'f') 다음 = '\f';
                        else if (다음 != '"' && 다음 != '\\' && 다음 != '/') throw new IllegalArgumentException("문자 이스케이프 Iphutha");
                    }
                    결과.append(다음);
                }
            }
            int Sebenzisa = 위치 - 1;
            while (위치 < umthombo.length() && ",]} \t\r\n".indexOf(umthombo.charAt(위치)) < 0) 위치++;
            String inani = umthombo.substring(Sebenzisa, 위치);
            if (inani.equals("true")) return Boolean.TRUE; if (inani.equals("false")) return Boolean.FALSE; if (inani.equals("null")) return null;
            return Double.valueOf(inani);
        }
    }
    static String i_hash_ifayela(Path Indlela_2) throws Exception {
        MessageDigest 계산 = MessageDigest.getInstance("SHA-256"); byte[] imininingwane = new byte[1024 * 1024];
        try (InputStream 입력 = Files.newInputStream(Indlela_2)) { for (int ubude_inani; (ubude_inani = 입력.read(imininingwane)) >= 0;) 계산.update(imininingwane,0,ubude_inani); }
        return i_hash_I_SMS(계산.digest());
    }
    static String i_hash_I_SMS(byte[] imininingwane) {
        StringBuilder Itekisi = new StringBuilder(); for (byte inani : imininingwane) Itekisi.append(String.format(Locale.ROOT,"%02x",inani & 255)); return Itekisi.toString();
    }
    static Path 내부경로(Path 기준, String Igama) {
        Path 결과 = 기준.resolve(Igama).normalize();
        if (Igama.isEmpty() || Paths.get(Igama).isAbsolute() || !결과.startsWith(기준) || Igama.indexOf('\\') >= 0)
            throw new IllegalArgumentException("범위를 벗어난 Indlela_2: " + Igama);
        for (Path 부분 : Paths.get(Igama)) if (부분.toString().equals("..")) throw new IllegalArgumentException("상위 Indlela_2 금지: " + Igama);
        for (Path 현재 = 결과; 현재 != null && 현재.startsWith(기준); 현재 = 현재.getParent())
            if (Files.isSymbolicLink(현재)) throw new IllegalArgumentException("의존성 경로의 링크 금지: " + Igama);
        return 결과;
    }
    static String 명령출력(List<String> Umlayelo) throws Exception {
        Process Inqubo_inani = new ProcessBuilder(Umlayelo).redirectError(ProcessBuilder.Redirect.INHERIT).start();
        String 결과 = new String(Inqubo_inani.getInputStream().readAllBytes(),StandardCharsets.UTF_8);
        if (Inqubo_inani.waitFor() != 0) throw new IOException("Umlayelo ukwehluleka_inani: " + Umlayelo.get(0)); return 결과;
    }
    static void monyula(Path londoloza_inani, Path isikhumulo_inani) throws Exception {
        for (String Igama : 명령출력(Arrays.asList("tar","-tzf",londoloza_inani.toString())).split("\n")) 내부경로(isikhumulo_inani, Igama);
        for (String umugqa : 명령출력(Arrays.asList("tar","-tvzf",londoloza_inani.toString())).split("\n"))
            if (!umugqa.isEmpty() && umugqa.charAt(0) != '-' && umugqa.charAt(0) != 'd') throw new IOException("외부 링크 또는 특수 파일을 포함한 의존성");
        Files.createDirectories(isikhumulo_inani);
        int isimo_inani = new ProcessBuilder("tar","--no-same-owner","--no-same-permissions","-xzf",londoloza_inani.toString(),"-C",isikhumulo_inani.toString()).inheritIO().start().waitFor();
        if (isimo_inani != 0) throw new IOException("의존성 londoloza_inani khulula_Indawo_yokugcina ukwehluleka_inani");
    }
    static void 호출(Path 작업경로, Path Amathuluzi, List<String> 인수, Map<String,String> 환경) throws Exception {
        List<String> Umlayelo = new ArrayList<>(Arrays.asList("python3", Amathuluzi.toString())); Umlayelo.addAll(인수);
        ProcessBuilder yenza_umyalo = new ProcessBuilder(Umlayelo).directory(작업경로.toFile()).inheritIO(); yenza_umyalo.environment().putAll(환경);
        int isimo_inani = yenza_umyalo.start().waitFor(); if (isimo_inani != 0) throw new IOException("Amathuluzi ukwehluleka_inani: " + Amathuluzi + " (" + isimo_inani + ")");
    }
    @SuppressWarnings("unchecked")
    public static void main(String[] 인수) throws Exception {
        if (인수.length < 1) throw new IllegalArgumentException("build, run, desktop, image, check, test-system 중 동작을 지정하세요");
        String Isenzo = 인수[0];
        if (!Arrays.asList("build","run","desktop","image","check","test-system").contains(Isenzo)) throw new IllegalArgumentException("알 수 없는 Isenzo");
        Path 기준 = Paths.get(System.getProperty("worldos.edition.root")).toAbsolutePath().normalize();
        Map<String,Object> Izinhlelo = (Map<String,Object>)new 자료해석기(Files.readString(기준.resolve("native.json"),StandardCharsets.UTF_8)).Funda();
        Path umthombo_isihlahla = 내부경로(기준,(String)Izinhlelo.get("source")), ikhenela_inani = 내부경로(umthombo_isihlahla,(String)Izinhlelo.get("native"));
        List<String> 소유파일들 = (List<String>)(List<?>)Izinhlelo.get("owned_files");
        for (String Igama : 소유파일들) if (!Files.isRegularFile(내부경로(umthombo_isihlahla,Igama))) throw new IOException("umthombo_isihlahla 없음: " + Igama);
        if (Isenzo.equals("check")) { System.out.println(Izinhlelo.get("country") + " " + Izinhlelo.get("language") + " 독립 umthombo_isihlahla qiniseka 완료"); return; }
        String 자원상대 = (String)Izinhlelo.getOrDefault("resource_root", ".");
        if (!자원상대.equals(".") && !자원상대.equals("..")) throw new IllegalArgumentException("의존성 기준 Indlela_2 Iphutha");
        Path insiza_inani = 기준.resolve(자원상대).normalize(); Path londoloza_inani = insiza_inani.resolve("native-vendor.tar.gz");
        String 기대해시 = (String)Izinhlelo.get("vendor_sha256");
        if (!i_hash_ifayela(londoloza_inani).equals(기대해시)) throw new IOException("의존성 SHA-256 불일치");
        Path 표식 = umthombo_isihlahla.resolve(".vendor-sha256");
        if (!Files.isRegularFile(표식) || !Files.readString(표식).trim().equals(기대해시)) { monyula(londoloza_inani, umthombo_isihlahla); Files.writeString(표식,기대해시 + "\n"); }
        Map<String,String> 환경 = new HashMap<>(System.getenv());
        Path ipConfig = null;
        if (환경.containsKey("IP_CONFIG")) ipConfig = Paths.get(환경.get("IP_CONFIG")).toAbsolutePath().normalize();
        else for (Path parent = 기준; parent != null; parent = parent.getParent()) {
            if (Files.isRegularFile(parent.resolve("ip.conf"))) { ipConfig = parent.resolve("ip.conf"); break; }
        }
        if (ipConfig == null) ipConfig = umthombo_isihlahla.resolve("ip.conf");
        if (!Files.isRegularFile(ipConfig)) throw new IOException("Missing ip.conf: " + ipConfig);
        환경.put("IP_CONFIG", ipConfig.toString());
        if (Arrays.asList("run","desktop","test-system").contains(Isenzo) && !환경.containsKey("QEMU_AARCH64")) {
            Path i_app_ikhabethe_le_app = insiza_inani.resolve("host/qemu"), 실행기표식 = insiza_inani.resolve("host/.qemu-sha256");
            String ikhabethe_le_app_i_hash = (String)Izinhlelo.get("qemu_sha256");
            if (!Files.isRegularFile(i_app_ikhabethe_le_app) || !Files.isRegularFile(실행기표식) || !Files.readString(실행기표식).trim().equals(ikhabethe_le_app_i_hash)) {
                Path ikhabethe_le_app_londoloza = insiza_inani.resolve("qemu-host.tar.gz"); if (!i_hash_ifayela(ikhabethe_le_app_londoloza).equals(ikhabethe_le_app_i_hash)) throw new IOException("QEMU SHA-256 불일치");
                monyula(ikhabethe_le_app_londoloza,insiza_inani.resolve("host")); Files.writeString(실행기표식,ikhabethe_le_app_i_hash + "\n");
            }
            환경.put("QEMU_AARCH64",i_app_ikhabethe_le_app.toString());
        }
        MessageDigest 계산 = MessageDigest.getInstance("SHA-256"); Collections.sort(소유파일들);
        for (String Igama : 소유파일들) { 계산.update(Igama.getBytes(StandardCharsets.UTF_8)); 계산.update(Files.readAllBytes(내부경로(umthombo_isihlahla,Igama))); }
        계산.update("ip.conf\0".getBytes(StandardCharsets.UTF_8)); 계산.update(Files.readAllBytes(ipConfig));
        String umthombo_i_hash = i_hash_I_SMS(계산.digest()); Path 빌드표식 = ikhenela_inani.resolve("build/worldos-source.sha256");
        if (Isenzo.equals("build") || !Files.isRegularFile(빌드표식) || !Files.readString(빌드표식).trim().equals(umthombo_i_hash)) {
            호출(ikhenela_inani,내부경로(ikhenela_inani,(String)Izinhlelo.get("builder")),Collections.emptyList(),환경);
            Files.writeString(빌드표식,umthombo_i_hash + "\n");
        }
        List<String> 추가인수 = new ArrayList<>(Arrays.asList(인수).subList(1,인수.length));
        if (Isenzo.equals("run") || Isenzo.equals("desktop")) {
            if (Isenzo.equals("desktop")) 추가인수.add(0,"--desktop");
            호출(ikhenela_inani,내부경로(ikhenela_inani,(String)Izinhlelo.get("runner")),추가인수,환경);
        } else if (Isenzo.equals("image")) 호출(ikhenela_inani,내부경로(ikhenela_inani,(String)Izinhlelo.get("image_builder")),추가인수,환경);
        else if (Isenzo.equals("test-system")) {
            추가인수.add(0,기준.toString()); 추가인수.add(0,"--edition");
            호출(ikhenela_inani,내부경로(ikhenela_inani,(String)Izinhlelo.get("system_tester")),추가인수,환경);
        }
    }
}
