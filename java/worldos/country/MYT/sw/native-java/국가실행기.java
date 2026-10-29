// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.security.MessageDigest;
import java.util.*;

/** 독립 국가판의 의존성 검사·복원·jenga_mfumo·실행을 맡는 mwenyeji Java Zana. */
public final class 국가실행기 {
    static final class data_kichanganuzi {
        final String chanzo; int 위치;
        data_kichanganuzi(String SMS) { chanzo = SMS; }
        void 빈칸() { while (위치 < chanzo.length() && Character.isWhitespace(chanzo.charAt(위치))) 위치++; }
        Object 읽기() {
            빈칸(); char kibambo_thamani = chanzo.charAt(위치++);
            if (kibambo_thamani == '{') {
                Map<String,Object> 결과 = new LinkedHashMap<>(); 빈칸();
                if (chanzo.charAt(위치) == '}') { 위치++; return 결과; }
                while (true) {
                    String Jina = (String)읽기(); 빈칸(); if (chanzo.charAt(위치++) != ':') throw new IllegalArgumentException("data kitenganishi_thamani_d8ba4873 kosa");
                    결과.put(Jina, 읽기()); 빈칸(); char kitenganishi_thamani_d8ba4873 = chanzo.charAt(위치++);
                    if (kitenganishi_thamani_d8ba4873 == '}') return 결과; if (kitenganishi_thamani_d8ba4873 != ',') throw new IllegalArgumentException("data kitenganishi_thamani_d8ba4873 kosa");
                }
            }
            if (kibambo_thamani == '[') {
                List<Object> 결과 = new ArrayList<>(); 빈칸();
                if (chanzo.charAt(위치) == ']') { 위치++; return 결과; }
                while (true) {
                    결과.add(읽기()); 빈칸(); char kitenganishi_thamani_d8ba4873 = chanzo.charAt(위치++);
                    if (kitenganishi_thamani_d8ba4873 == ']') return 결과; if (kitenganishi_thamani_d8ba4873 != ',') throw new IllegalArgumentException("data kitenganishi_thamani_d8ba4873 kosa");
                }
            }
            if (kibambo_thamani == '"') {
                StringBuilder 결과 = new StringBuilder();
                while (true) {
                    char 다음 = chanzo.charAt(위치++); if (다음 == '"') return 결과.toString();
                    if (다음 == '\\') {
                        다음 = chanzo.charAt(위치++);
                        if (다음 == 'u') { 결과.append((char)Integer.parseInt(chanzo.substring(위치, 위치 + 4),16)); 위치 += 4; continue; }
                        if (다음 == 'n') 다음 = '\n'; else if (다음 == 'r') 다음 = '\r'; else if (다음 == 't') 다음 = '\t';
                        else if (다음 == 'b') 다음 = '\b'; else if (다음 == 'f') 다음 = '\f';
                        else if (다음 != '"' && 다음 != '\\' && 다음 != '/') throw new IllegalArgumentException("문자 이스케이프 kosa");
                    }
                    결과.append(다음);
                }
            }
            int endesha = 위치 - 1;
            while (위치 < chanzo.length() && ",]} \t\r\n".indexOf(chanzo.charAt(위치)) < 0) 위치++;
            String thamani = chanzo.substring(endesha, 위치);
            if (thamani.equals("true")) return Boolean.TRUE; if (thamani.equals("false")) return Boolean.FALSE; if (thamani.equals("null")) return null;
            return Double.valueOf(thamani);
        }
    }
    static String kali_faili(Path njia) throws Exception {
        MessageDigest 계산 = MessageDigest.getInstance("SHA-256"); byte[] data = new byte[1024 * 1024];
        try (InputStream 입력 = Files.newInputStream(njia)) { for (int urefu_thamani; (urefu_thamani = 입력.read(data)) >= 0;) 계산.update(data,0,urefu_thamani); }
        return kali_SMS(계산.digest());
    }
    static String kali_SMS(byte[] data) {
        StringBuilder SMS = new StringBuilder(); for (byte thamani : data) SMS.append(String.format(Locale.ROOT,"%02x",thamani & 255)); return SMS.toString();
    }
    static Path 내부경로(Path 기준, String Jina) {
        Path 결과 = 기준.resolve(Jina).normalize();
        if (Jina.isEmpty() || Paths.get(Jina).isAbsolute() || !결과.startsWith(기준) || Jina.indexOf('\\') >= 0)
            throw new IllegalArgumentException("범위를 벗어난 njia: " + Jina);
        for (Path 부분 : Paths.get(Jina)) if (부분.toString().equals("..")) throw new IllegalArgumentException("상위 njia 금지: " + Jina);
        for (Path 현재 = 결과; 현재 != null && 현재.startsWith(기준); 현재 = 현재.getParent())
            if (Files.isSymbolicLink(현재)) throw new IllegalArgumentException("의존성 경로의 링크 금지: " + Jina);
        return 결과;
    }
    static String 명령출력(List<String> amri) throws Exception {
        Process Mchakato_thamani = new ProcessBuilder(amri).redirectError(ProcessBuilder.Redirect.INHERIT).start();
        String 결과 = new String(Mchakato_thamani.getInputStream().readAllBytes(),StandardCharsets.UTF_8);
        if (Mchakato_thamani.waitFor() != 0) throw new IOException("amri kushindwa_thamani: " + amri.get(0)); return 결과;
    }
    static void opoa(Path Hifadhi_thamani, Path fikio_thamani) throws Exception {
        for (String Jina : 명령출력(Arrays.asList("tar","-tzf",Hifadhi_thamani.toString())).split("\n")) 내부경로(fikio_thamani, Jina);
        for (String laini : 명령출력(Arrays.asList("tar","-tvzf",Hifadhi_thamani.toString())).split("\n"))
            if (!laini.isEmpty() && laini.charAt(0) != '-' && laini.charAt(0) != 'd') throw new IOException("외부 링크 또는 특수 파일을 포함한 의존성");
        Files.createDirectories(fikio_thamani);
        int hali_thamani = new ProcessBuilder("tar","--no-same-owner","--no-same-permissions","-xzf",Hifadhi_thamani.toString(),"-C",fikio_thamani.toString()).inheritIO().start().waitFor();
        if (hali_thamani != 0) throw new IOException("의존성 Hifadhi_thamani toleo_Hifadhi kushindwa_thamani");
    }
    static void 호출(Path 작업경로, Path Zana, List<String> 인수, Map<String,String> 환경) throws Exception {
        List<String> amri = new ArrayList<>(Arrays.asList("python3", Zana.toString())); amri.addAll(인수);
        ProcessBuilder tekeleza_amri = new ProcessBuilder(amri).directory(작업경로.toFile()).inheritIO(); tekeleza_amri.environment().putAll(환경);
        int hali_thamani = tekeleza_amri.start().waitFor(); if (hali_thamani != 0) throw new IOException("Zana kushindwa_thamani: " + Zana + " (" + hali_thamani + ")");
    }
    @SuppressWarnings("unchecked")
    public static void main(String[] 인수) throws Exception {
        if (인수.length < 1) throw new IllegalArgumentException("build, run, desktop, image, check, test-system 중 동작을 지정하세요");
        String Kitendo = 인수[0];
        if (!Arrays.asList("build","run","desktop","image","check","test-system").contains(Kitendo)) throw new IllegalArgumentException("알 수 없는 Kitendo");
        Path 기준 = Paths.get(System.getProperty("worldos.edition.root")).toAbsolutePath().normalize();
        Map<String,Object> Mipangilio = (Map<String,Object>)new data_kichanganuzi(Files.readString(기준.resolve("native.json"),StandardCharsets.UTF_8)).읽기();
        Path chanzo_mti = 내부경로(기준,(String)Mipangilio.get("source")), kiini_thamani_0611a8a8 = 내부경로(chanzo_mti,(String)Mipangilio.get("native"));
        List<String> 소유파일들 = (List<String>)(List<?>)Mipangilio.get("owned_files");
        for (String Jina : 소유파일들) if (!Files.isRegularFile(내부경로(chanzo_mti,Jina))) throw new IOException("chanzo_mti 없음: " + Jina);
        if (Kitendo.equals("check")) { System.out.println(Mipangilio.get("country") + " " + Mipangilio.get("language") + " 독립 chanzo_mti thibitisha 완료"); return; }
        String 자원상대 = (String)Mipangilio.getOrDefault("resource_root", ".");
        if (!자원상대.equals(".") && !자원상대.equals("..")) throw new IllegalArgumentException("의존성 기준 njia kosa");
        Path rasilimali_thamani = 기준.resolve(자원상대).normalize(); Path Hifadhi_thamani = rasilimali_thamani.resolve("native-vendor.tar.gz");
        String 기대해시 = (String)Mipangilio.get("vendor_sha256");
        if (!kali_faili(Hifadhi_thamani).equals(기대해시)) throw new IOException("의존성 SHA-256 불일치");
        Path 표식 = chanzo_mti.resolve(".vendor-sha256");
        if (!Files.isRegularFile(표식) || !Files.readString(표식).trim().equals(기대해시)) { opoa(Hifadhi_thamani, chanzo_mti); Files.writeString(표식,기대해시 + "\n"); }
        Map<String,String> 환경 = new HashMap<>(System.getenv());
        Path ipConfig = null;
        if (환경.containsKey("IP_CONFIG")) ipConfig = Paths.get(환경.get("IP_CONFIG")).toAbsolutePath().normalize();
        else for (Path parent = 기준; parent != null; parent = parent.getParent()) {
            if (Files.isRegularFile(parent.resolve("ip.conf"))) { ipConfig = parent.resolve("ip.conf"); break; }
        }
        if (ipConfig == null) ipConfig = chanzo_mti.resolve("ip.conf");
        if (!Files.isRegularFile(ipConfig)) throw new IOException("Missing ip.conf: " + ipConfig);
        환경.put("IP_CONFIG", ipConfig.toString());
        if (Arrays.asList("run","desktop","test-system").contains(Kitendo) && !환경.containsKey("QEMU_AARCH64")) {
            Path programu_droo_ya_programu = rasilimali_thamani.resolve("host/qemu"), 실행기표식 = rasilimali_thamani.resolve("host/.qemu-sha256");
            String droo_ya_programu_kali = (String)Mipangilio.get("qemu_sha256");
            if (!Files.isRegularFile(programu_droo_ya_programu) || !Files.isRegularFile(실행기표식) || !Files.readString(실행기표식).trim().equals(droo_ya_programu_kali)) {
                Path droo_ya_programu_Hifadhi = rasilimali_thamani.resolve("qemu-host.tar.gz"); if (!kali_faili(droo_ya_programu_Hifadhi).equals(droo_ya_programu_kali)) throw new IOException("QEMU SHA-256 불일치");
                opoa(droo_ya_programu_Hifadhi,rasilimali_thamani.resolve("host")); Files.writeString(실행기표식,droo_ya_programu_kali + "\n");
            }
            환경.put("QEMU_AARCH64",programu_droo_ya_programu.toString());
        }
        MessageDigest 계산 = MessageDigest.getInstance("SHA-256"); Collections.sort(소유파일들);
        for (String Jina : 소유파일들) { 계산.update(Jina.getBytes(StandardCharsets.UTF_8)); 계산.update(Files.readAllBytes(내부경로(chanzo_mti,Jina))); }
        계산.update("ip.conf\0".getBytes(StandardCharsets.UTF_8)); 계산.update(Files.readAllBytes(ipConfig));
        String chanzo_kali = kali_SMS(계산.digest()); Path 빌드표식 = kiini_thamani_0611a8a8.resolve("build/worldos-source.sha256");
        if (Kitendo.equals("build") || !Files.isRegularFile(빌드표식) || !Files.readString(빌드표식).trim().equals(chanzo_kali)) {
            호출(kiini_thamani_0611a8a8,내부경로(kiini_thamani_0611a8a8,(String)Mipangilio.get("builder")),Collections.emptyList(),환경);
            Files.writeString(빌드표식,chanzo_kali + "\n");
        }
        List<String> 추가인수 = new ArrayList<>(Arrays.asList(인수).subList(1,인수.length));
        if (Kitendo.equals("run") || Kitendo.equals("desktop")) {
            if (Kitendo.equals("desktop")) 추가인수.add(0,"--desktop");
            호출(kiini_thamani_0611a8a8,내부경로(kiini_thamani_0611a8a8,(String)Mipangilio.get("runner")),추가인수,환경);
        } else if (Kitendo.equals("image")) 호출(kiini_thamani_0611a8a8,내부경로(kiini_thamani_0611a8a8,(String)Mipangilio.get("image_builder")),추가인수,환경);
        else if (Kitendo.equals("test-system")) {
            추가인수.add(0,기준.toString()); 추가인수.add(0,"--edition");
            호출(kiini_thamani_0611a8a8,내부경로(kiini_thamani_0611a8a8,(String)Mipangilio.get("system_tester")),추가인수,환경);
        }
    }
}
