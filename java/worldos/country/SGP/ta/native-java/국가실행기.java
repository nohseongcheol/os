// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.security.MessageDigest;
import java.util.*;

/** 독립 국가판의 의존성 검사·복원·தொகு_முறைமை·실행을 맡는 ஓம்பு Java கருவிகள். */
public final class 국가실행기 {
    static final class தரவு_பார்சர் {
        final String மூலக்_கோப்பு; int இடம்;
        தரவு_பார்சர்(String உரை) { மூலக்_கோப்பு = உரை; }
        void 빈칸() { while (இடம் < மூலக்_கோப்பு.length() && Character.isWhitespace(மூலக்_கோப்பு.charAt(இடம்))) இடம்++; }
        Object படி() {
            빈칸(); char எழுத்துக்குறி_மதிப்பு = மூலக்_கோப்பு.charAt(இடம்++);
            if (எழுத்துக்குறி_மதிப்பு == '{') {
                Map<String,Object> அளவிடக்கூடியது = new LinkedHashMap<>(); 빈칸();
                if (மூலக்_கோப்பு.charAt(இடம்) == '}') { இடம்++; return அளவிடக்கூடியது; }
                while (true) {
                    String பெயர் = (String)படி(); 빈칸(); if (மூலக்_கோப்பு.charAt(இடம்++) != ':') throw new IllegalArgumentException("தரவு வரம்புக்குறி_மதிப்பு பிழை");
                    அளவிடக்கூடியது.put(பெயர், படி()); 빈칸(); char வரம்புக்குறி_மதிப்பு = மூலக்_கோப்பு.charAt(இடம்++);
                    if (வரம்புக்குறி_மதிப்பு == '}') return அளவிடக்கூடியது; if (வரம்புக்குறி_மதிப்பு != ',') throw new IllegalArgumentException("தரவு வரம்புக்குறி_மதிப்பு பிழை");
                }
            }
            if (எழுத்துக்குறி_மதிப்பு == '[') {
                List<Object> அளவிடக்கூடியது = new ArrayList<>(); 빈칸();
                if (மூலக்_கோப்பு.charAt(இடம்) == ']') { இடம்++; return அளவிடக்கூடியது; }
                while (true) {
                    அளவிடக்கூடியது.add(படி()); 빈칸(); char வரம்புக்குறி_மதிப்பு = மூலக்_கோப்பு.charAt(இடம்++);
                    if (வரம்புக்குறி_மதிப்பு == ']') return அளவிடக்கூடியது; if (வரம்புக்குறி_மதிப்பு != ',') throw new IllegalArgumentException("தரவு வரம்புக்குறி_மதிப்பு பிழை");
                }
            }
            if (எழுத்துக்குறி_மதிப்பு == '"') {
                StringBuilder அளவிடக்கூடியது = new StringBuilder();
                while (true) {
                    char அடுத்து_உருப்படி = மூலக்_கோப்பு.charAt(இடம்++); if (அடுத்து_உருப்படி == '"') return அளவிடக்கூடியது.toString();
                    if (அடுத்து_உருப்படி == '\\') {
                        அடுத்து_உருப்படி = மூலக்_கோப்பு.charAt(இடம்++);
                        if (அடுத்து_உருப்படி == 'u') { அளவிடக்கூடியது.append((char)Integer.parseInt(மூலக்_கோப்பு.substring(இடம், இடம் + 4),16)); இடம் += 4; continue; }
                        if (அடுத்து_உருப்படி == 'n') அடுத்து_உருப்படி = '\n'; else if (அடுத்து_உருப்படி == 'r') அடுத்து_உருப்படி = '\r'; else if (அடுத்து_உருப்படி == 't') அடுத்து_உருப்படி = '\t';
                        else if (அடுத்து_உருப்படி == 'b') அடுத்து_உருப்படி = '\b'; else if (அடுத்து_உருப்படி == 'f') அடுத்து_உருப்படி = '\f';
                        else if (அடுத்து_உருப்படி != '"' && அடுத்து_உருப்படி != '\\' && அடுத்து_உருப்படி != '/') throw new IllegalArgumentException("문자 이스케이프 பிழை");
                    }
                    அளவிடக்கூடியது.append(அடுத்து_உருப்படி);
                }
            }
            int செயல்படுத்துக = இடம் - 1;
            while (இடம் < மூலக்_கோப்பு.length() && ",]} \t\r\n".indexOf(மூலக்_கோப்பு.charAt(இடம்)) < 0) இடம்++;
            String மதிப்பு = மூலக்_கோப்பு.substring(செயல்படுத்துக, இடம்);
            if (மதிப்பு.equals("true")) return Boolean.TRUE; if (மதிப்பு.equals("false")) return Boolean.FALSE; if (மதிப்பு.equals("null")) return null;
            return Double.valueOf(மதிப்பு);
        }
    }
    static String ஹாஷ்_கோப்பு(Path பாதை_2) throws Exception {
        MessageDigest 계산 = MessageDigest.getInstance("SHA-256"); byte[] தரவு = new byte[1024 * 1024];
        try (InputStream 입력 = Files.newInputStream(பாதை_2)) { for (int நீளம்_மதிப்பு; (நீளம்_மதிப்பு = 입력.read(தரவு)) >= 0;) 계산.update(தரவு,0,நீளம்_மதிப்பு); }
        return ஹாஷ்_உரை(계산.digest());
    }
    static String ஹாஷ்_உரை(byte[] தரவு) {
        StringBuilder உரை = new StringBuilder(); for (byte மதிப்பு : தரவு) உரை.append(String.format(Locale.ROOT,"%02x",மதிப்பு & 255)); return உரை.toString();
    }
    static Path 내부경로(Path திட்டப்பணி_மூலம், String பெயர்) {
        Path அளவிடக்கூடியது = திட்டப்பணி_மூலம்.resolve(பெயர்).normalize();
        if (பெயர்.isEmpty() || Paths.get(பெயர்).isAbsolute() || !அளவிடக்கூடியது.startsWith(திட்டப்பணி_மூலம்) || பெயர்.indexOf('\\') >= 0)
            throw new IllegalArgumentException("범위를 벗어난 பாதை_2: " + பெயர்);
        for (Path 부분 : Paths.get(பெயர்)) if (부분.toString().equals("..")) throw new IllegalArgumentException("상위 பாதை_2 금지: " + பெயர்);
        for (Path 현재 = அளவிடக்கூடியது; 현재 != null && 현재.startsWith(திட்டப்பணி_மூலம்); 현재 = 현재.getParent())
            if (Files.isSymbolicLink(현재)) throw new IllegalArgumentException("의존성 경로의 링크 금지: " + பெயர்);
        return அளவிடக்கூடியது;
    }
    static String 명령출력(List<String> கட்டளை) throws Exception {
        Process செயலகம்_மதிப்பு = new ProcessBuilder(கட்டளை).redirectError(ProcessBuilder.Redirect.INHERIT).start();
        String அளவிடக்கூடியது = new String(செயலகம்_மதிப்பு.getInputStream().readAllBytes(),StandardCharsets.UTF_8);
        if (செயலகம்_மதிப்பு.waitFor() != 0) throw new IOException("கட்டளை செயலிழப்பு_மதிப்பு: " + கட்டளை.get(0)); return அளவிடக்கூடியது;
    }
    static void பிரித்தெடு(Path காப்பகம்_மதிப்பு, Path இலக்கு_மதிப்பு) throws Exception {
        for (String பெயர் : 명령출력(Arrays.asList("tar","-tzf",காப்பகம்_மதிப்பு.toString())).split("\n")) 내부경로(இலக்கு_மதிப்பு, பெயர்);
        for (String உள்ளீட்டு_வரி : 명령출력(Arrays.asList("tar","-tvzf",காப்பகம்_மதிப்பு.toString())).split("\n"))
            if (!உள்ளீட்டு_வரி.isEmpty() && உள்ளீட்டு_வரி.charAt(0) != '-' && உள்ளீட்டு_வரி.charAt(0) != 'd') throw new IOException("외부 링크 또는 특수 파일을 포함한 의존성");
        Files.createDirectories(இலக்கு_மதிப்பு);
        int நிலை_மதிப்பு_e10195a1 = new ProcessBuilder("tar","--no-same-owner","--no-same-permissions","-xzf",காப்பகம்_மதிப்பு.toString(),"-C",இலக்கு_மதிப்பு.toString()).inheritIO().start().waitFor();
        if (நிலை_மதிப்பு_e10195a1 != 0) throw new IOException("의존성 காப்பகம்_மதிப்பு அனுப்பு_சேமிப்பகம் செயலிழப்பு_மதிப்பு");
    }
    static void 호출(Path 작업경로, Path கருவிகள், List<String> செயலுருபுகள், Map<String,String> 환경) throws Exception {
        List<String> கட்டளை = new ArrayList<>(Arrays.asList("python3", கருவிகள்.toString())); கட்டளை.addAll(செயலுருபுகள்);
        ProcessBuilder இயக்கு_கட்டளை = new ProcessBuilder(கட்டளை).directory(작업경로.toFile()).inheritIO(); இயக்கு_கட்டளை.environment().putAll(환경);
        int நிலை_மதிப்பு_e10195a1 = இயக்கு_கட்டளை.start().waitFor(); if (நிலை_மதிப்பு_e10195a1 != 0) throw new IOException("கருவிகள் செயலிழப்பு_மதிப்பு: " + கருவிகள் + " (" + நிலை_மதிப்பு_e10195a1 + ")");
    }
    @SuppressWarnings("unchecked")
    public static void main(String[] செயலுருபுகள்) throws Exception {
        if (செயலுருபுகள்.length < 1) throw new IllegalArgumentException("build, run, desktop, image, check, test-system 중 동작을 지정하세요");
        String செயல் = செயலுருபுகள்[0];
        if (!Arrays.asList("build","run","desktop","image","check","test-system").contains(செயல்)) throw new IllegalArgumentException("알 수 없는 செயல்");
        Path திட்டப்பணி_மூலம் = Paths.get(System.getProperty("worldos.edition.root")).toAbsolutePath().normalize();
        Map<String,Object> அமைப்புகள் = (Map<String,Object>)new தரவு_பார்சர்(Files.readString(திட்டப்பணி_மூலம்.resolve("native.json"),StandardCharsets.UTF_8)).படி();
        Path மூலம்_மரம் = 내부경로(திட்டப்பணி_மூலம்,(String)அமைப்புகள்.get("source")), கரு_மதிப்பு = 내부경로(மூலம்_மரம்,(String)அமைப்புகள்.get("native"));
        List<String> 소유파일들 = (List<String>)(List<?>)அமைப்புகள்.get("owned_files");
        for (String பெயர் : 소유파일들) if (!Files.isRegularFile(내부경로(மூலம்_மரம்,பெயர்))) throw new IOException("மூலம்_மரம் 없음: " + பெயர்);
        if (செயல்.equals("check")) { System.out.println(அமைப்புகள்.get("country") + " " + அமைப்புகள்.get("language") + " 독립 மூலம்_மரம் சரிபார் 완료"); return; }
        String வளம்_தொடர்புடைய_பாதை = (String)அமைப்புகள்.getOrDefault("resource_root", ".");
        if (!வளம்_தொடர்புடைய_பாதை.equals(".") && !வளம்_தொடர்புடைய_பாதை.equals("..")) throw new IllegalArgumentException("의존성 திட்டப்பணி_மூலம் பாதை_2 பிழை");
        Path வளம்_மதிப்பு = திட்டப்பணி_மூலம்.resolve(வளம்_தொடர்புடைய_பாதை).normalize(); Path காப்பகம்_மதிப்பு = வளம்_மதிப்பு.resolve("native-vendor.tar.gz");
        String 기대해시 = (String)அமைப்புகள்.get("vendor_sha256");
        if (!ஹாஷ்_கோப்பு(காப்பகம்_மதிப்பு).equals(기대해시)) throw new IOException("의존성 SHA-256 불일치");
        Path 표식 = மூலம்_மரம்.resolve(".vendor-sha256");
        if (!Files.isRegularFile(표식) || !Files.readString(표식).trim().equals(기대해시)) { பிரித்தெடு(காப்பகம்_மதிப்பு, மூலம்_மரம்); Files.writeString(표식,기대해시 + "\n"); }
        Map<String,String> 환경 = new HashMap<>(System.getenv());
        Path ipConfig = null;
        if (환경.containsKey("IP_CONFIG")) ipConfig = Paths.get(환경.get("IP_CONFIG")).toAbsolutePath().normalize();
        else for (Path parent = திட்டப்பணி_மூலம்; parent != null; parent = parent.getParent()) {
            if (Files.isRegularFile(parent.resolve("ip.conf"))) { ipConfig = parent.resolve("ip.conf"); break; }
        }
        if (ipConfig == null) ipConfig = மூலம்_மரம்.resolve("ip.conf");
        if (!Files.isRegularFile(ipConfig)) throw new IOException("Missing ip.conf: " + ipConfig);
        환경.put("IP_CONFIG", ipConfig.toString());
        if (Arrays.asList("run","desktop","test-system").contains(செயல்) && !환경.containsKey("QEMU_AARCH64")) {
            Path நிரல்_துவக்குநர் = வளம்_மதிப்பு.resolve("host/qemu"), 실행기표식 = வளம்_மதிப்பு.resolve("host/.qemu-sha256");
            String துவக்குநர்_ஹாஷ் = (String)அமைப்புகள்.get("qemu_sha256");
            if (!Files.isRegularFile(நிரல்_துவக்குநர்) || !Files.isRegularFile(실행기표식) || !Files.readString(실행기표식).trim().equals(துவக்குநர்_ஹாஷ்)) {
                Path துவக்குநர்_காப்பகம் = வளம்_மதிப்பு.resolve("qemu-host.tar.gz"); if (!ஹாஷ்_கோப்பு(துவக்குநர்_காப்பகம்).equals(துவக்குநர்_ஹாஷ்)) throw new IOException("QEMU SHA-256 불일치");
                பிரித்தெடு(துவக்குநர்_காப்பகம்,வளம்_மதிப்பு.resolve("host")); Files.writeString(실행기표식,துவக்குநர்_ஹாஷ் + "\n");
            }
            환경.put("QEMU_AARCH64",நிரல்_துவக்குநர்.toString());
        }
        MessageDigest 계산 = MessageDigest.getInstance("SHA-256"); Collections.sort(소유파일들);
        for (String பெயர் : 소유파일들) { 계산.update(பெயர்.getBytes(StandardCharsets.UTF_8)); 계산.update(Files.readAllBytes(내부경로(மூலம்_மரம்,பெயர்))); }
        계산.update("ip.conf\0".getBytes(StandardCharsets.UTF_8)); 계산.update(Files.readAllBytes(ipConfig));
        String மூலம்_ஹாஷ் = ஹாஷ்_உரை(계산.digest()); Path 빌드표식 = கரு_மதிப்பு.resolve("build/worldos-source.sha256");
        if (செயல்.equals("build") || !Files.isRegularFile(빌드표식) || !Files.readString(빌드표식).trim().equals(மூலம்_ஹாஷ்)) {
            호출(கரு_மதிப்பு,내부경로(கரு_மதிப்பு,(String)அமைப்புகள்.get("builder")),Collections.emptyList(),환경);
            Files.writeString(빌드표식,மூலம்_ஹாஷ் + "\n");
        }
        List<String> 추가인수 = new ArrayList<>(Arrays.asList(செயலுருபுகள்).subList(1,செயலுருபுகள்.length));
        if (செயல்.equals("run") || செயல்.equals("desktop")) {
            if (செயல்.equals("desktop")) 추가인수.add(0,"--desktop");
            호출(கரு_மதிப்பு,내부경로(கரு_மதிப்பு,(String)அமைப்புகள்.get("runner")),추가인수,환경);
        } else if (செயல்.equals("image")) 호출(கரு_மதிப்பு,내부경로(கரு_மதிப்பு,(String)அமைப்புகள்.get("image_builder")),추가인수,환경);
        else if (செயல்.equals("test-system")) {
            추가인수.add(0,திட்டப்பணி_மூலம்.toString()); 추가인수.add(0,"--edition");
            호출(கரு_மதிப்பு,내부경로(கரு_மதிப்பு,(String)அமைப்புகள்.get("system_tester")),추가인수,환경);
        }
    }
}
