// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.security.MessageDigest;
import java.util.*;

/** 독립 국가판의 의존성 검사·복원·bena_sistema·실행을 맡는 host Java Għodod. */
public final class 국가실행기 {
    static final class 자료해석기 {
        final String sors; int pożizzjoni;
        자료해석기(String SMS) { sors = SMS; }
        void 빈칸() { while (pożizzjoni < sors.length() && Character.isWhitespace(sors.charAt(pożizzjoni))) pożizzjoni++; }
        Object 읽기() {
            빈칸(); char karattru_VALUE = sors.charAt(pożizzjoni++);
            if (karattru_VALUE == '{') {
                Map<String,Object> miżura = new LinkedHashMap<>(); 빈칸();
                if (sors.charAt(pożizzjoni) == '}') { pożizzjoni++; return miżura; }
                while (true) {
                    String isem = (String)읽기(); 빈칸(); if (sors.charAt(pożizzjoni++) != ':') throw new IllegalArgumentException("data delimitatur_VALUE żball");
                    miżura.put(isem, 읽기()); 빈칸(); char delimitatur_VALUE = sors.charAt(pożizzjoni++);
                    if (delimitatur_VALUE == '}') return miżura; if (delimitatur_VALUE != ',') throw new IllegalArgumentException("data delimitatur_VALUE żball");
                }
            }
            if (karattru_VALUE == '[') {
                List<Object> miżura = new ArrayList<>(); 빈칸();
                if (sors.charAt(pożizzjoni) == ']') { pożizzjoni++; return miżura; }
                while (true) {
                    miżura.add(읽기()); 빈칸(); char delimitatur_VALUE = sors.charAt(pożizzjoni++);
                    if (delimitatur_VALUE == ']') return miżura; if (delimitatur_VALUE != ',') throw new IllegalArgumentException("data delimitatur_VALUE żball");
                }
            }
            if (karattru_VALUE == '"') {
                StringBuilder miżura = new StringBuilder();
                while (true) {
                    char Li_Jmiss_element = sors.charAt(pożizzjoni++); if (Li_Jmiss_element == '"') return miżura.toString();
                    if (Li_Jmiss_element == '\\') {
                        Li_Jmiss_element = sors.charAt(pożizzjoni++);
                        if (Li_Jmiss_element == 'u') { miżura.append((char)Integer.parseInt(sors.substring(pożizzjoni, pożizzjoni + 4),16)); pożizzjoni += 4; continue; }
                        if (Li_Jmiss_element == 'n') Li_Jmiss_element = '\n'; else if (Li_Jmiss_element == 'r') Li_Jmiss_element = '\r'; else if (Li_Jmiss_element == 't') Li_Jmiss_element = '\t';
                        else if (Li_Jmiss_element == 'b') Li_Jmiss_element = '\b'; else if (Li_Jmiss_element == 'f') Li_Jmiss_element = '\f';
                        else if (Li_Jmiss_element != '"' && Li_Jmiss_element != '\\' && Li_Jmiss_element != '/') throw new IllegalArgumentException("문자 이스케이프 żball");
                    }
                    miżura.append(Li_Jmiss_element);
                }
            }
            int serje = pożizzjoni - 1;
            while (pożizzjoni < sors.length() && ",]} \t\r\n".indexOf(sors.charAt(pożizzjoni)) < 0) pożizzjoni++;
            String VALUE = sors.substring(serje, pożizzjoni);
            if (VALUE.equals("true")) return Boolean.TRUE; if (VALUE.equals("false")) return Boolean.FALSE; if (VALUE.equals("null")) return null;
            return Double.valueOf(VALUE);
        }
    }
    static String hash_fajl(Path mogħdija) throws Exception {
        MessageDigest 계산 = MessageDigest.getInstance("SHA-256"); byte[] data = new byte[1024 * 1024];
        try (InputStream 입력 = Files.newInputStream(mogħdija)) { for (int tul_VALUE; (tul_VALUE = 입력.read(data)) >= 0;) 계산.update(data,0,tul_VALUE); }
        return hash_SMS(계산.digest());
    }
    static String hash_SMS(byte[] data) {
        StringBuilder SMS = new StringBuilder(); for (byte VALUE : data) SMS.append(String.format(Locale.ROOT,"%02x",VALUE & 255)); return SMS.toString();
    }
    static Path 내부경로(Path pprojetta_għerq, String isem) {
        Path miżura = pprojetta_għerq.resolve(isem).normalize();
        if (isem.isEmpty() || Paths.get(isem).isAbsolute() || !miżura.startsWith(pprojetta_għerq) || isem.indexOf('\\') >= 0)
            throw new IllegalArgumentException("범위를 벗어난 mogħdija: " + isem);
        for (Path 부분 : Paths.get(isem)) if (부분.toString().equals("..")) throw new IllegalArgumentException("상위 mogħdija 금지: " + isem);
        for (Path 현재 = miżura; 현재 != null && 현재.startsWith(pprojetta_għerq); 현재 = 현재.getParent())
            if (Files.isSymbolicLink(현재)) throw new IllegalArgumentException("의존성 경로의 링크 금지: " + isem);
        return miżura;
    }
    static String 명령출력(List<String> kmand) throws Exception {
        Process Proċess_VALUE = new ProcessBuilder(kmand).redirectError(ProcessBuilder.Redirect.INHERIT).start();
        String miżura = new String(Proċess_VALUE.getInputStream().readAllBytes(),StandardCharsets.UTF_8);
        if (Proċess_VALUE.waitFor() != 0) throw new IOException("kmand żball_VALUE: " + kmand.get(0)); return miżura;
    }
    static void estratta(Path Arkivju_VALUE, Path destinazzjoni_VALUE) throws Exception {
        for (String isem : 명령출력(Arrays.asList("tar","-tzf",Arkivju_VALUE.toString())).split("\n")) 내부경로(destinazzjoni_VALUE, isem);
        for (String linja : 명령출력(Arrays.asList("tar","-tvzf",Arkivju_VALUE.toString())).split("\n"))
            if (!linja.isEmpty() && linja.charAt(0) != '-' && linja.charAt(0) != 'd') throw new IOException("외부 링크 또는 특수 파일을 포함한 의존성");
        Files.createDirectories(destinazzjoni_VALUE);
        int stat_VALUE = new ProcessBuilder("tar","--no-same-owner","--no-same-permissions","-xzf",Arkivju_VALUE.toString(),"-C",destinazzjoni_VALUE.toString()).inheritIO().start().waitFor();
        if (stat_VALUE != 0) throw new IOException("의존성 Arkivju_VALUE mexxi_Ħażna żball_VALUE");
    }
    static void 호출(Path 작업경로, Path Għodod, List<String> 인수, Map<String,String> 환경) throws Exception {
        List<String> kmand = new ArrayList<>(Arrays.asList("python3", Għodod.toString())); kmand.addAll(인수);
        ProcessBuilder eżegwixxa_kmand = new ProcessBuilder(kmand).directory(작업경로.toFile()).inheritIO(); eżegwixxa_kmand.environment().putAll(환경);
        int stat_VALUE = eżegwixxa_kmand.start().waitFor(); if (stat_VALUE != 0) throw new IOException("Għodod żball_VALUE: " + Għodod + " (" + stat_VALUE + ")");
    }
    @SuppressWarnings("unchecked")
    public static void main(String[] 인수) throws Exception {
        if (인수.length < 1) throw new IllegalArgumentException("build, run, desktop, image, check, test-system 중 동작을 지정하세요");
        String azzjoni = 인수[0];
        if (!Arrays.asList("build","run","desktop","image","check","test-system").contains(azzjoni)) throw new IllegalArgumentException("알 수 없는 azzjoni");
        Path pprojetta_għerq = Paths.get(System.getProperty("worldos.edition.root")).toAbsolutePath().normalize();
        Map<String,Object> Settings = (Map<String,Object>)new 자료해석기(Files.readString(pprojetta_għerq.resolve("native.json"),StandardCharsets.UTF_8)).읽기();
        Path sors_siġra = 내부경로(pprojetta_għerq,(String)Settings.get("source")), kernel_VALUE = 내부경로(sors_siġra,(String)Settings.get("native"));
        List<String> 소유파일들 = (List<String>)(List<?>)Settings.get("owned_files");
        for (String isem : 소유파일들) if (!Files.isRegularFile(내부경로(sors_siġra,isem))) throw new IOException("sors_siġra 없음: " + isem);
        if (azzjoni.equals("check")) { System.out.println(Settings.get("country") + " " + Settings.get("language") + " 독립 sors_siġra vverifika 완료"); return; }
        String 자원상대 = (String)Settings.getOrDefault("resource_root", ".");
        if (!자원상대.equals(".") && !자원상대.equals("..")) throw new IllegalArgumentException("의존성 pprojetta_għerq mogħdija żball");
        Path riżorsa_VALUE = pprojetta_għerq.resolve(자원상대).normalize(); Path Arkivju_VALUE = riżorsa_VALUE.resolve("native-vendor.tar.gz");
        String 기대해시 = (String)Settings.get("vendor_sha256");
        if (!hash_fajl(Arkivju_VALUE).equals(기대해시)) throw new IOException("의존성 SHA-256 불일치");
        Path 표식 = sors_siġra.resolve(".vendor-sha256");
        if (!Files.isRegularFile(표식) || !Files.readString(표식).trim().equals(기대해시)) { estratta(Arkivju_VALUE, sors_siġra); Files.writeString(표식,기대해시 + "\n"); }
        Map<String,String> 환경 = new HashMap<>(System.getenv());
        Path ipConfig = null;
        if (환경.containsKey("IP_CONFIG")) ipConfig = Paths.get(환경.get("IP_CONFIG")).toAbsolutePath().normalize();
        else for (Path parent = pprojetta_għerq; parent != null; parent = parent.getParent()) {
            if (Files.isRegularFile(parent.resolve("ip.conf"))) { ipConfig = parent.resolve("ip.conf"); break; }
        }
        if (ipConfig == null) ipConfig = sors_siġra.resolve("ip.conf");
        if (!Files.isRegularFile(ipConfig)) throw new IOException("Missing ip.conf: " + ipConfig);
        환경.put("IP_CONFIG", ipConfig.toString());
        if (Arrays.asList("run","desktop","test-system").contains(azzjoni) && !환경.containsKey("QEMU_AARCH64")) {
            Path programm_ġabra_ta_apps = riżorsa_VALUE.resolve("host/qemu"), 실행기표식 = riżorsa_VALUE.resolve("host/.qemu-sha256");
            String ġabra_ta_apps_hash = (String)Settings.get("qemu_sha256");
            if (!Files.isRegularFile(programm_ġabra_ta_apps) || !Files.isRegularFile(실행기표식) || !Files.readString(실행기표식).trim().equals(ġabra_ta_apps_hash)) {
                Path ġabra_ta_apps_Arkivju = riżorsa_VALUE.resolve("qemu-host.tar.gz"); if (!hash_fajl(ġabra_ta_apps_Arkivju).equals(ġabra_ta_apps_hash)) throw new IOException("QEMU SHA-256 불일치");
                estratta(ġabra_ta_apps_Arkivju,riżorsa_VALUE.resolve("host")); Files.writeString(실행기표식,ġabra_ta_apps_hash + "\n");
            }
            환경.put("QEMU_AARCH64",programm_ġabra_ta_apps.toString());
        }
        MessageDigest 계산 = MessageDigest.getInstance("SHA-256"); Collections.sort(소유파일들);
        for (String isem : 소유파일들) { 계산.update(isem.getBytes(StandardCharsets.UTF_8)); 계산.update(Files.readAllBytes(내부경로(sors_siġra,isem))); }
        계산.update("ip.conf\0".getBytes(StandardCharsets.UTF_8)); 계산.update(Files.readAllBytes(ipConfig));
        String sors_hash = hash_SMS(계산.digest()); Path 빌드표식 = kernel_VALUE.resolve("build/worldos-source.sha256");
        if (azzjoni.equals("build") || !Files.isRegularFile(빌드표식) || !Files.readString(빌드표식).trim().equals(sors_hash)) {
            호출(kernel_VALUE,내부경로(kernel_VALUE,(String)Settings.get("builder")),Collections.emptyList(),환경);
            Files.writeString(빌드표식,sors_hash + "\n");
        }
        List<String> 추가인수 = new ArrayList<>(Arrays.asList(인수).subList(1,인수.length));
        if (azzjoni.equals("run") || azzjoni.equals("desktop")) {
            if (azzjoni.equals("desktop")) 추가인수.add(0,"--desktop");
            호출(kernel_VALUE,내부경로(kernel_VALUE,(String)Settings.get("runner")),추가인수,환경);
        } else if (azzjoni.equals("image")) 호출(kernel_VALUE,내부경로(kernel_VALUE,(String)Settings.get("image_builder")),추가인수,환경);
        else if (azzjoni.equals("test-system")) {
            추가인수.add(0,pprojetta_għerq.toString()); 추가인수.add(0,"--edition");
            호출(kernel_VALUE,내부경로(kernel_VALUE,(String)Settings.get("system_tester")),추가인수,환경);
        }
    }
}
