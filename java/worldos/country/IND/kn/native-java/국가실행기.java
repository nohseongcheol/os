// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.security.MessageDigest;
import java.util.*;

/** 독립 국가판의 의존성 검사·복원·ಬಿಲ್ಡ್_ಸಿಸ್ಟಂ·실행을 맡는 ಹೋಸ್ಟ್ Java ಪರಿಕರಗಳು. */
public final class 국가실행기 {
    static final class ಡೇಟಾ_ಪಾರ್ಸರ್ {
        final String ಮೂಲ; int ಸ್ಥಾನ;
        ಡೇಟಾ_ಪಾರ್ಸರ್(String ಪಠ್ಯ) { ಮೂಲ = ಪಠ್ಯ; }
        void 빈칸() { while (ಸ್ಥಾನ < ಮೂಲ.length() && Character.isWhitespace(ಮೂಲ.charAt(ಸ್ಥಾನ))) ಸ್ಥಾನ++; }
        Object ಓದು() {
            빈칸(); char ಅಕ್ಷರ_ಮೌಲ್ಯ = ಮೂಲ.charAt(ಸ್ಥಾನ++);
            if (ಅಕ್ಷರ_ಮೌಲ್ಯ == '{') {
                Map<String,Object> ಮಾಪನ = new LinkedHashMap<>(); 빈칸();
                if (ಮೂಲ.charAt(ಸ್ಥಾನ) == '}') { ಸ್ಥಾನ++; return ಮಾಪನ; }
                while (true) {
                    String ಹೆಸರು = (String)ಓದು(); 빈칸(); if (ಮೂಲ.charAt(ಸ್ಥಾನ++) != ':') throw new IllegalArgumentException("ಡೇಟಾ ಮಿತಿಸೂಚಕ_ಮೌಲ್ಯ ದೋಷ");
                    ಮಾಪನ.put(ಹೆಸರು, ಓದು()); 빈칸(); char ಮಿತಿಸೂಚಕ_ಮೌಲ್ಯ = ಮೂಲ.charAt(ಸ್ಥಾನ++);
                    if (ಮಿತಿಸೂಚಕ_ಮೌಲ್ಯ == '}') return ಮಾಪನ; if (ಮಿತಿಸೂಚಕ_ಮೌಲ್ಯ != ',') throw new IllegalArgumentException("ಡೇಟಾ ಮಿತಿಸೂಚಕ_ಮೌಲ್ಯ ದೋಷ");
                }
            }
            if (ಅಕ್ಷರ_ಮೌಲ್ಯ == '[') {
                List<Object> ಮಾಪನ = new ArrayList<>(); 빈칸();
                if (ಮೂಲ.charAt(ಸ್ಥಾನ) == ']') { ಸ್ಥಾನ++; return ಮಾಪನ; }
                while (true) {
                    ಮಾಪನ.add(ಓದು()); 빈칸(); char ಮಿತಿಸೂಚಕ_ಮೌಲ್ಯ = ಮೂಲ.charAt(ಸ್ಥಾನ++);
                    if (ಮಿತಿಸೂಚಕ_ಮೌಲ್ಯ == ']') return ಮಾಪನ; if (ಮಿತಿಸೂಚಕ_ಮೌಲ್ಯ != ',') throw new IllegalArgumentException("ಡೇಟಾ ಮಿತಿಸೂಚಕ_ಮೌಲ್ಯ ದೋಷ");
                }
            }
            if (ಅಕ್ಷರ_ಮೌಲ್ಯ == '"') {
                StringBuilder ಮಾಪನ = new StringBuilder();
                while (true) {
                    char ಮುಂದೆ_ಅಂಶ = ಮೂಲ.charAt(ಸ್ಥಾನ++); if (ಮುಂದೆ_ಅಂಶ == '"') return ಮಾಪನ.toString();
                    if (ಮುಂದೆ_ಅಂಶ == '\\') {
                        ಮುಂದೆ_ಅಂಶ = ಮೂಲ.charAt(ಸ್ಥಾನ++);
                        if (ಮುಂದೆ_ಅಂಶ == 'u') { ಮಾಪನ.append((char)Integer.parseInt(ಮೂಲ.substring(ಸ್ಥಾನ, ಸ್ಥಾನ + 4),16)); ಸ್ಥಾನ += 4; continue; }
                        if (ಮುಂದೆ_ಅಂಶ == 'n') ಮುಂದೆ_ಅಂಶ = '\n'; else if (ಮುಂದೆ_ಅಂಶ == 'r') ಮುಂದೆ_ಅಂಶ = '\r'; else if (ಮುಂದೆ_ಅಂಶ == 't') ಮುಂದೆ_ಅಂಶ = '\t';
                        else if (ಮುಂದೆ_ಅಂಶ == 'b') ಮುಂದೆ_ಅಂಶ = '\b'; else if (ಮುಂದೆ_ಅಂಶ == 'f') ಮುಂದೆ_ಅಂಶ = '\f';
                        else if (ಮುಂದೆ_ಅಂಶ != '"' && ಮುಂದೆ_ಅಂಶ != '\\' && ಮುಂದೆ_ಅಂಶ != '/') throw new IllegalArgumentException("문자 이스케이프 ದೋಷ");
                    }
                    ಮಾಪನ.append(ಮುಂದೆ_ಅಂಶ);
                }
            }
            int ಚಲಾಯಿಸು_2 = ಸ್ಥಾನ - 1;
            while (ಸ್ಥಾನ < ಮೂಲ.length() && ",]} \t\r\n".indexOf(ಮೂಲ.charAt(ಸ್ಥಾನ)) < 0) ಸ್ಥಾನ++;
            String ಮೌಲ್ಯ = ಮೂಲ.substring(ಚಲಾಯಿಸು_2, ಸ್ಥಾನ);
            if (ಮೌಲ್ಯ.equals("true")) return Boolean.TRUE; if (ಮೌಲ್ಯ.equals("false")) return Boolean.FALSE; if (ಮೌಲ್ಯ.equals("null")) return null;
            return Double.valueOf(ಮೌಲ್ಯ);
        }
    }
    static String ಹ್ಯಾಶ್_ಫೈಲ್(Path ಮಾರ್ಗ) throws Exception {
        MessageDigest 계산 = MessageDigest.getInstance("SHA-256"); byte[] ಡೇಟಾ = new byte[1024 * 1024];
        try (InputStream 입력 = Files.newInputStream(ಮಾರ್ಗ)) { for (int ಉದ್ದ_ಮೌಲ್ಯ; (ಉದ್ದ_ಮೌಲ್ಯ = 입력.read(ಡೇಟಾ)) >= 0;) 계산.update(ಡೇಟಾ,0,ಉದ್ದ_ಮೌಲ್ಯ); }
        return ಹ್ಯಾಶ್_ಪಠ್ಯ(계산.digest());
    }
    static String ಹ್ಯಾಶ್_ಪಠ್ಯ(byte[] ಡೇಟಾ) {
        StringBuilder ಪಠ್ಯ = new StringBuilder(); for (byte ಮೌಲ್ಯ : ಡೇಟಾ) ಪಠ್ಯ.append(String.format(Locale.ROOT,"%02x",ಮೌಲ್ಯ & 255)); return ಪಠ್ಯ.toString();
    }
    static Path 내부경로(Path ಬಿಂಬಿಸು_ಮೂಲ, String ಹೆಸರು) {
        Path ಮಾಪನ = ಬಿಂಬಿಸು_ಮೂಲ.resolve(ಹೆಸರು).normalize();
        if (ಹೆಸರು.isEmpty() || Paths.get(ಹೆಸರು).isAbsolute() || !ಮಾಪನ.startsWith(ಬಿಂಬಿಸು_ಮೂಲ) || ಹೆಸರು.indexOf('\\') >= 0)
            throw new IllegalArgumentException("범위를 벗어난 ಮಾರ್ಗ: " + ಹೆಸರು);
        for (Path 부분 : Paths.get(ಹೆಸರು)) if (부분.toString().equals("..")) throw new IllegalArgumentException("상위 ಮಾರ್ಗ 금지: " + ಹೆಸರು);
        for (Path 현재 = ಮಾಪನ; 현재 != null && 현재.startsWith(ಬಿಂಬಿಸು_ಮೂಲ); 현재 = 현재.getParent())
            if (Files.isSymbolicLink(현재)) throw new IllegalArgumentException("의존성 경로의 링크 금지: " + ಹೆಸರು);
        return ಮಾಪನ;
    }
    static String 명령출력(List<String> ಆಜ್ಞೆ) throws Exception {
        Process ಪ್ರಕ್ರಿಯೆ_ಮೌಲ್ಯ = new ProcessBuilder(ಆಜ್ಞೆ).redirectError(ProcessBuilder.Redirect.INHERIT).start();
        String ಮಾಪನ = new String(ಪ್ರಕ್ರಿಯೆ_ಮೌಲ್ಯ.getInputStream().readAllBytes(),StandardCharsets.UTF_8);
        if (ಪ್ರಕ್ರಿಯೆ_ಮೌಲ್ಯ.waitFor() != 0) throw new IOException("ಆಜ್ಞೆ ವೈಫಲ್ಯ_ಮೌಲ್ಯ: " + ಆಜ್ಞೆ.get(0)); return ಮಾಪನ;
    }
    static void ಬೇರೆ_ಮಾಡು(Path ಅರ್ಖೀವ್_ಮೌಲ್ಯ, Path ಗಮ್ಯಸ್ಥಾನ_ಮೌಲ್ಯ) throws Exception {
        for (String ಹೆಸರು : 명령출력(Arrays.asList("tar","-tzf",ಅರ್ಖೀವ್_ಮೌಲ್ಯ.toString())).split("\n")) 내부경로(ಗಮ್ಯಸ್ಥಾನ_ಮೌಲ್ಯ, ಹೆಸರು);
        for (String ಸಾಲು : 명령출력(Arrays.asList("tar","-tvzf",ಅರ್ಖೀವ್_ಮೌಲ್ಯ.toString())).split("\n"))
            if (!ಸಾಲು.isEmpty() && ಸಾಲು.charAt(0) != '-' && ಸಾಲು.charAt(0) != 'd') throw new IOException("외부 링크 또는 특수 파일을 포함한 의존성");
        Files.createDirectories(ಗಮ್ಯಸ್ಥಾನ_ಮೌಲ್ಯ);
        int ಸ್ಥಿತಿ_ಮೌಲ್ಯ = new ProcessBuilder("tar","--no-same-owner","--no-same-permissions","-xzf",ಅರ್ಖೀವ್_ಮೌಲ್ಯ.toString(),"-C",ಗಮ್ಯಸ್ಥಾನ_ಮೌಲ್ಯ.toString()).inheritIO().start().waitFor();
        if (ಸ್ಥಿತಿ_ಮೌಲ್ಯ != 0) throw new IOException("의존성 ಅರ್ಖೀವ್_ಮೌಲ್ಯ ಬಿಡುಗಡೆ_ಸಂಗ್ರಹ ವೈಫಲ್ಯ_ಮೌಲ್ಯ");
    }
    static void 호출(Path 작업경로, Path ಪರಿಕರಗಳು, List<String> 인수, Map<String,String> 환경) throws Exception {
        List<String> ಆಜ್ಞೆ = new ArrayList<>(Arrays.asList("python3", ಪರಿಕರಗಳು.toString())); ಆಜ್ಞೆ.addAll(인수);
        ProcessBuilder ಪೂರೈಸು_ಆದೇಶ = new ProcessBuilder(ಆಜ್ಞೆ).directory(작업경로.toFile()).inheritIO(); ಪೂರೈಸು_ಆದೇಶ.environment().putAll(환경);
        int ಸ್ಥಿತಿ_ಮೌಲ್ಯ = ಪೂರೈಸು_ಆದೇಶ.start().waitFor(); if (ಸ್ಥಿತಿ_ಮೌಲ್ಯ != 0) throw new IOException("ಪರಿಕರಗಳು ವೈಫಲ್ಯ_ಮೌಲ್ಯ: " + ಪರಿಕರಗಳು + " (" + ಸ್ಥಿತಿ_ಮೌಲ್ಯ + ")");
    }
    @SuppressWarnings("unchecked")
    public static void main(String[] 인수) throws Exception {
        if (인수.length < 1) throw new IllegalArgumentException("build, run, desktop, image, check, test-system 중 동작을 지정하세요");
        String ಹಕ್ರಿಯೆ = 인수[0];
        if (!Arrays.asList("build","run","desktop","image","check","test-system").contains(ಹಕ್ರಿಯೆ)) throw new IllegalArgumentException("알 수 없는 ಹಕ್ರಿಯೆ");
        Path ಬಿಂಬಿಸು_ಮೂಲ = Paths.get(System.getProperty("worldos.edition.root")).toAbsolutePath().normalize();
        Map<String,Object> ಸಿದ್ಧತೆಗಳು = (Map<String,Object>)new ಡೇಟಾ_ಪಾರ್ಸರ್(Files.readString(ಬಿಂಬಿಸು_ಮೂಲ.resolve("native.json"),StandardCharsets.UTF_8)).ಓದು();
        Path ಮೂಲ_ವೃಕ್ಷ = 내부경로(ಬಿಂಬಿಸು_ಮೂಲ,(String)ಸಿದ್ಧತೆಗಳು.get("source")), ಕರ್ನಲ್_ಮೌಲ್ಯ = 내부경로(ಮೂಲ_ವೃಕ್ಷ,(String)ಸಿದ್ಧತೆಗಳು.get("native"));
        List<String> 소유파일들 = (List<String>)(List<?>)ಸಿದ್ಧತೆಗಳು.get("owned_files");
        for (String ಹೆಸರು : 소유파일들) if (!Files.isRegularFile(내부경로(ಮೂಲ_ವೃಕ್ಷ,ಹೆಸರು))) throw new IOException("ಮೂಲ_ವೃಕ್ಷ 없음: " + ಹೆಸರು);
        if (ಹಕ್ರಿಯೆ.equals("check")) { System.out.println(ಸಿದ್ಧತೆಗಳು.get("country") + " " + ಸಿದ್ಧತೆಗಳು.get("language") + " 독립 ಮೂಲ_ವೃಕ್ಷ ಖಚಿತಪಡಿಸಿಕೊಳ್ಳು 완료"); return; }
        String 자원상대 = (String)ಸಿದ್ಧತೆಗಳು.getOrDefault("resource_root", ".");
        if (!자원상대.equals(".") && !자원상대.equals("..")) throw new IllegalArgumentException("의존성 ಬಿಂಬಿಸು_ಮೂಲ ಮಾರ್ಗ ದೋಷ");
        Path ಸಂಪನ್ಮೂಲ_ಮೌಲ್ಯ = ಬಿಂಬಿಸು_ಮೂಲ.resolve(자원상대).normalize(); Path ಅರ್ಖೀವ್_ಮೌಲ್ಯ = ಸಂಪನ್ಮೂಲ_ಮೌಲ್ಯ.resolve("native-vendor.tar.gz");
        String 기대해시 = (String)ಸಿದ್ಧತೆಗಳು.get("vendor_sha256");
        if (!ಹ್ಯಾಶ್_ಫೈಲ್(ಅರ್ಖೀವ್_ಮೌಲ್ಯ).equals(기대해시)) throw new IOException("의존성 SHA-256 불일치");
        Path 표식 = ಮೂಲ_ವೃಕ್ಷ.resolve(".vendor-sha256");
        if (!Files.isRegularFile(표식) || !Files.readString(표식).trim().equals(기대해시)) { ಬೇರೆ_ಮಾಡು(ಅರ್ಖೀವ್_ಮೌಲ್ಯ, ಮೂಲ_ವೃಕ್ಷ); Files.writeString(표식,기대해시 + "\n"); }
        Map<String,String> 환경 = new HashMap<>(System.getenv());
        Path ipConfig = null;
        if (환경.containsKey("IP_CONFIG")) ipConfig = Paths.get(환경.get("IP_CONFIG")).toAbsolutePath().normalize();
        else for (Path parent = ಬಿಂಬಿಸು_ಮೂಲ; parent != null; parent = parent.getParent()) {
            if (Files.isRegularFile(parent.resolve("ip.conf"))) { ipConfig = parent.resolve("ip.conf"); break; }
        }
        if (ipConfig == null) ipConfig = ಮೂಲ_ವೃಕ್ಷ.resolve("ip.conf");
        if (!Files.isRegularFile(ipConfig)) throw new IOException("Missing ip.conf: " + ipConfig);
        환경.put("IP_CONFIG", ipConfig.toString());
        if (Arrays.asList("run","desktop","test-system").contains(ಹಕ್ರಿಯೆ) && !환경.containsKey("QEMU_AARCH64")) {
            Path ಅಪ್ಲಿ_ಲಾಂಚರ್ = ಸಂಪನ್ಮೂಲ_ಮೌಲ್ಯ.resolve("host/qemu"), 실행기표식 = ಸಂಪನ್ಮೂಲ_ಮೌಲ್ಯ.resolve("host/.qemu-sha256");
            String ಲಾಂಚರ್_ಹ್ಯಾಶ್ = (String)ಸಿದ್ಧತೆಗಳು.get("qemu_sha256");
            if (!Files.isRegularFile(ಅಪ್ಲಿ_ಲಾಂಚರ್) || !Files.isRegularFile(실행기표식) || !Files.readString(실행기표식).trim().equals(ಲಾಂಚರ್_ಹ್ಯಾಶ್)) {
                Path ಲಾಂಚರ್_ಅರ್ಖೀವ್ = ಸಂಪನ್ಮೂಲ_ಮೌಲ್ಯ.resolve("qemu-host.tar.gz"); if (!ಹ್ಯಾಶ್_ಫೈಲ್(ಲಾಂಚರ್_ಅರ್ಖೀವ್).equals(ಲಾಂಚರ್_ಹ್ಯಾಶ್)) throw new IOException("QEMU SHA-256 불일치");
                ಬೇರೆ_ಮಾಡು(ಲಾಂಚರ್_ಅರ್ಖೀವ್,ಸಂಪನ್ಮೂಲ_ಮೌಲ್ಯ.resolve("host")); Files.writeString(실행기표식,ಲಾಂಚರ್_ಹ್ಯಾಶ್ + "\n");
            }
            환경.put("QEMU_AARCH64",ಅಪ್ಲಿ_ಲಾಂಚರ್.toString());
        }
        MessageDigest 계산 = MessageDigest.getInstance("SHA-256"); Collections.sort(소유파일들);
        for (String ಹೆಸರು : 소유파일들) { 계산.update(ಹೆಸರು.getBytes(StandardCharsets.UTF_8)); 계산.update(Files.readAllBytes(내부경로(ಮೂಲ_ವೃಕ್ಷ,ಹೆಸರು))); }
        계산.update("ip.conf\0".getBytes(StandardCharsets.UTF_8)); 계산.update(Files.readAllBytes(ipConfig));
        String ಮೂಲ_ಹ್ಯಾಶ್ = ಹ್ಯಾಶ್_ಪಠ್ಯ(계산.digest()); Path 빌드표식 = ಕರ್ನಲ್_ಮೌಲ್ಯ.resolve("build/worldos-source.sha256");
        if (ಹಕ್ರಿಯೆ.equals("build") || !Files.isRegularFile(빌드표식) || !Files.readString(빌드표식).trim().equals(ಮೂಲ_ಹ್ಯಾಶ್)) {
            호출(ಕರ್ನಲ್_ಮೌಲ್ಯ,내부경로(ಕರ್ನಲ್_ಮೌಲ್ಯ,(String)ಸಿದ್ಧತೆಗಳು.get("builder")),Collections.emptyList(),환경);
            Files.writeString(빌드표식,ಮೂಲ_ಹ್ಯಾಶ್ + "\n");
        }
        List<String> 추가인수 = new ArrayList<>(Arrays.asList(인수).subList(1,인수.length));
        if (ಹಕ್ರಿಯೆ.equals("run") || ಹಕ್ರಿಯೆ.equals("desktop")) {
            if (ಹಕ್ರಿಯೆ.equals("desktop")) 추가인수.add(0,"--desktop");
            호출(ಕರ್ನಲ್_ಮೌಲ್ಯ,내부경로(ಕರ್ನಲ್_ಮೌಲ್ಯ,(String)ಸಿದ್ಧತೆಗಳು.get("runner")),추가인수,환경);
        } else if (ಹಕ್ರಿಯೆ.equals("image")) 호출(ಕರ್ನಲ್_ಮೌಲ್ಯ,내부경로(ಕರ್ನಲ್_ಮೌಲ್ಯ,(String)ಸಿದ್ಧತೆಗಳು.get("image_builder")),추가인수,환경);
        else if (ಹಕ್ರಿಯೆ.equals("test-system")) {
            추가인수.add(0,ಬಿಂಬಿಸು_ಮೂಲ.toString()); 추가인수.add(0,"--edition");
            호출(ಕರ್ನಲ್_ಮೌಲ್ಯ,내부경로(ಕರ್ನಲ್_ಮೌಲ್ಯ,(String)ಸಿದ್ಧತೆಗಳು.get("system_tester")),추가인수,환경);
        }
    }
}
