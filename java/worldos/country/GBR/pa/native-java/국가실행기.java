// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.security.MessageDigest;
import java.util.*;

/** 독립 국가판의 의존성 검사·복원·ਬਿਲਡ_ਪਰਬੰਧ·실행을 맡는 ਹੋਸਟ Java ਸਾਧਨ. */
public final class 국가실행기 {
    static final class 자료해석기 {
        final String ਸਰੋਤ; int ਸਥਿਤੀ;
        자료해석기(String ਟੈਕਸਟ) { ਸਰੋਤ = ਟੈਕਸਟ; }
        void 빈칸() { while (ਸਥਿਤੀ < ਸਰੋਤ.length() && Character.isWhitespace(ਸਰੋਤ.charAt(ਸਥਿਤੀ))) ਸਥਿਤੀ++; }
        Object ਪੜ੍ਹਨ() {
            빈칸(); char ਵਰਣ_ਕੀਮਤ = ਸਰੋਤ.charAt(ਸਥਿਤੀ++);
            if (ਵਰਣ_ਕੀਮਤ == '{') {
                Map<String,Object> ਮਾਪ = new LinkedHashMap<>(); 빈칸();
                if (ਸਰੋਤ.charAt(ਸਥਿਤੀ) == '}') { ਸਥਿਤੀ++; return ਮਾਪ; }
                while (true) {
                    String ਨਾਂ = (String)ਪੜ੍ਹਨ(); 빈칸(); if (ਸਰੋਤ.charAt(ਸਥਿਤੀ++) != ':') throw new IllegalArgumentException("ਸਮੱਗਰੀ ਅਸੀਮਤ_ਕੀਮਤ ਗਲਤੀ");
                    ਮਾਪ.put(ਨਾਂ, ਪੜ੍ਹਨ()); 빈칸(); char ਅਸੀਮਤ_ਕੀਮਤ = ਸਰੋਤ.charAt(ਸਥਿਤੀ++);
                    if (ਅਸੀਮਤ_ਕੀਮਤ == '}') return ਮਾਪ; if (ਅਸੀਮਤ_ਕੀਮਤ != ',') throw new IllegalArgumentException("ਸਮੱਗਰੀ ਅਸੀਮਤ_ਕੀਮਤ ਗਲਤੀ");
                }
            }
            if (ਵਰਣ_ਕੀਮਤ == '[') {
                List<Object> ਮਾਪ = new ArrayList<>(); 빈칸();
                if (ਸਰੋਤ.charAt(ਸਥਿਤੀ) == ']') { ਸਥਿਤੀ++; return ਮਾਪ; }
                while (true) {
                    ਮਾਪ.add(ਪੜ੍ਹਨ()); 빈칸(); char ਅਸੀਮਤ_ਕੀਮਤ = ਸਰੋਤ.charAt(ਸਥਿਤੀ++);
                    if (ਅਸੀਮਤ_ਕੀਮਤ == ']') return ਮਾਪ; if (ਅਸੀਮਤ_ਕੀਮਤ != ',') throw new IllegalArgumentException("ਸਮੱਗਰੀ ਅਸੀਮਤ_ਕੀਮਤ ਗਲਤੀ");
                }
            }
            if (ਵਰਣ_ਕੀਮਤ == '"') {
                StringBuilder ਮਾਪ = new StringBuilder();
                while (true) {
                    char ਅਗਲਾ_ਆਇਟਮ = ਸਰੋਤ.charAt(ਸਥਿਤੀ++); if (ਅਗਲਾ_ਆਇਟਮ == '"') return ਮਾਪ.toString();
                    if (ਅਗਲਾ_ਆਇਟਮ == '\\') {
                        ਅਗਲਾ_ਆਇਟਮ = ਸਰੋਤ.charAt(ਸਥਿਤੀ++);
                        if (ਅਗਲਾ_ਆਇਟਮ == 'u') { ਮਾਪ.append((char)Integer.parseInt(ਸਰੋਤ.substring(ਸਥਿਤੀ, ਸਥਿਤੀ + 4),16)); ਸਥਿਤੀ += 4; continue; }
                        if (ਅਗਲਾ_ਆਇਟਮ == 'n') ਅਗਲਾ_ਆਇਟਮ = '\n'; else if (ਅਗਲਾ_ਆਇਟਮ == 'r') ਅਗਲਾ_ਆਇਟਮ = '\r'; else if (ਅਗਲਾ_ਆਇਟਮ == 't') ਅਗਲਾ_ਆਇਟਮ = '\t';
                        else if (ਅਗਲਾ_ਆਇਟਮ == 'b') ਅਗਲਾ_ਆਇਟਮ = '\b'; else if (ਅਗਲਾ_ਆਇਟਮ == 'f') ਅਗਲਾ_ਆਇਟਮ = '\f';
                        else if (ਅਗਲਾ_ਆਇਟਮ != '"' && ਅਗਲਾ_ਆਇਟਮ != '\\' && ਅਗਲਾ_ਆਇਟਮ != '/') throw new IllegalArgumentException("문자 이스케이프 ਗਲਤੀ");
                    }
                    ਮਾਪ.append(ਅਗਲਾ_ਆਇਟਮ);
                }
            }
            int ਚਲਾਓ_2 = ਸਥਿਤੀ - 1;
            while (ਸਥਿਤੀ < ਸਰੋਤ.length() && ",]} \t\r\n".indexOf(ਸਰੋਤ.charAt(ਸਥਿਤੀ)) < 0) ਸਥਿਤੀ++;
            String ਕੀਮਤ = ਸਰੋਤ.substring(ਚਲਾਓ_2, ਸਥਿਤੀ);
            if (ਕੀਮਤ.equals("true")) return Boolean.TRUE; if (ਕੀਮਤ.equals("false")) return Boolean.FALSE; if (ਕੀਮਤ.equals("null")) return null;
            return Double.valueOf(ਕੀਮਤ);
        }
    }
    static String ਹੈਸ਼_ਲਿਖਤ_ਪੱਤਰ(Path ਮਾਰਗ) throws Exception {
        MessageDigest 계산 = MessageDigest.getInstance("SHA-256"); byte[] ਸਮੱਗਰੀ = new byte[1024 * 1024];
        try (InputStream 입력 = Files.newInputStream(ਮਾਰਗ)) { for (int ਲੰਬਾਈ_ਕੀਮਤ; (ਲੰਬਾਈ_ਕੀਮਤ = 입력.read(ਸਮੱਗਰੀ)) >= 0;) 계산.update(ਸਮੱਗਰੀ,0,ਲੰਬਾਈ_ਕੀਮਤ); }
        return ਹੈਸ਼_ਪਾਠ(계산.digest());
    }
    static String ਹੈਸ਼_ਪਾਠ(byte[] ਸਮੱਗਰੀ) {
        StringBuilder ਟੈਕਸਟ = new StringBuilder(); for (byte ਕੀਮਤ : ਸਮੱਗਰੀ) ਟੈਕਸਟ.append(String.format(Locale.ROOT,"%02x",ਕੀਮਤ & 255)); return ਟੈਕਸਟ.toString();
    }
    static Path 내부경로(Path ਪ੍ਰੋਜੈਕਟ_ਰੂਟ, String ਨਾਂ) {
        Path ਮਾਪ = ਪ੍ਰੋਜੈਕਟ_ਰੂਟ.resolve(ਨਾਂ).normalize();
        if (ਨਾਂ.isEmpty() || Paths.get(ਨਾਂ).isAbsolute() || !ਮਾਪ.startsWith(ਪ੍ਰੋਜੈਕਟ_ਰੂਟ) || ਨਾਂ.indexOf('\\') >= 0)
            throw new IllegalArgumentException("범위를 벗어난 ਮਾਰਗ: " + ਨਾਂ);
        for (Path 부분 : Paths.get(ਨਾਂ)) if (부분.toString().equals("..")) throw new IllegalArgumentException("상위 ਮਾਰਗ 금지: " + ਨਾਂ);
        for (Path 현재 = ਮਾਪ; 현재 != null && 현재.startsWith(ਪ੍ਰੋਜੈਕਟ_ਰੂਟ); 현재 = 현재.getParent())
            if (Files.isSymbolicLink(현재)) throw new IllegalArgumentException("의존성 경로의 링크 금지: " + ਨਾਂ);
        return ਮਾਪ;
    }
    static String 명령출력(List<String> ਕਮਾਂਡ) throws Exception {
        Process ਕਾਰਵਾਈ_ਕੀਮਤ = new ProcessBuilder(ਕਮਾਂਡ).redirectError(ProcessBuilder.Redirect.INHERIT).start();
        String ਮਾਪ = new String(ਕਾਰਵਾਈ_ਕੀਮਤ.getInputStream().readAllBytes(),StandardCharsets.UTF_8);
        if (ਕਾਰਵਾਈ_ਕੀਮਤ.waitFor() != 0) throw new IOException("ਕਮਾਂਡ ਅਸਫਲ_ਕੀਮਤ: " + ਕਮਾਂਡ.get(0)); return ਮਾਪ;
    }
    static void ਕੱਢੋ(Path ਸੰਗ੍ਰਹਿ_ਕੀਮਤ, Path ਮੰਜਿਲ_ਕੀਮਤ) throws Exception {
        for (String ਨਾਂ : 명령출력(Arrays.asList("tar","-tzf",ਸੰਗ੍ਰਹਿ_ਕੀਮਤ.toString())).split("\n")) 내부경로(ਮੰਜਿਲ_ਕੀਮਤ, ਨਾਂ);
        for (String ਲਾਈਨ : 명령출력(Arrays.asList("tar","-tvzf",ਸੰਗ੍ਰਹਿ_ਕੀਮਤ.toString())).split("\n"))
            if (!ਲਾਈਨ.isEmpty() && ਲਾਈਨ.charAt(0) != '-' && ਲਾਈਨ.charAt(0) != 'd') throw new IOException("외부 링크 또는 특수 파일을 포함한 의존성");
        Files.createDirectories(ਮੰਜਿਲ_ਕੀਮਤ);
        int ਸਥਿਤੀ_ਕੀਮਤ = new ProcessBuilder("tar","--no-same-owner","--no-same-permissions","-xzf",ਸੰਗ੍ਰਹਿ_ਕੀਮਤ.toString(),"-C",ਮੰਜਿਲ_ਕੀਮਤ.toString()).inheritIO().start().waitFor();
        if (ਸਥਿਤੀ_ਕੀਮਤ != 0) throw new IOException("의존성 ਸੰਗ੍ਰਹਿ_ਕੀਮਤ ਰਿਲੀਜ_ਸਟੋਰੇਜ ਅਸਫਲ_ਕੀਮਤ");
    }
    static void 호출(Path 작업경로, Path ਸਾਧਨ, List<String> ਆਰਗੂਮੈਂਟ, Map<String,String> 환경) throws Exception {
        List<String> ਕਮਾਂਡ = new ArrayList<>(Arrays.asList("python3", ਸਾਧਨ.toString())); ਕਮਾਂਡ.addAll(ਆਰਗੂਮੈਂਟ);
        ProcessBuilder ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼ = new ProcessBuilder(ਕਮਾਂਡ).directory(작업경로.toFile()).inheritIO(); ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼.environment().putAll(환경);
        int ਸਥਿਤੀ_ਕੀਮਤ = ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼.start().waitFor(); if (ਸਥਿਤੀ_ਕੀਮਤ != 0) throw new IOException("ਸਾਧਨ ਅਸਫਲ_ਕੀਮਤ: " + ਸਾਧਨ + " (" + ਸਥਿਤੀ_ਕੀਮਤ + ")");
    }
    @SuppressWarnings("unchecked")
    public static void main(String[] ਆਰਗੂਮੈਂਟ) throws Exception {
        if (ਆਰਗੂਮੈਂਟ.length < 1) throw new IllegalArgumentException("build, run, desktop, image, check, test-system 중 동작을 지정하세요");
        String ਐਕਸ਼ਨ = ਆਰਗੂਮੈਂਟ[0];
        if (!Arrays.asList("build","run","desktop","image","check","test-system").contains(ਐਕਸ਼ਨ)) throw new IllegalArgumentException("알 수 없는 ਐਕਸ਼ਨ");
        Path ਪ੍ਰੋਜੈਕਟ_ਰੂਟ = Paths.get(System.getProperty("worldos.edition.root")).toAbsolutePath().normalize();
        Map<String,Object> ਸੈਟਿੰਗ = (Map<String,Object>)new 자료해석기(Files.readString(ਪ੍ਰੋਜੈਕਟ_ਰੂਟ.resolve("native.json"),StandardCharsets.UTF_8)).ਪੜ੍ਹਨ();
        Path ਸਰੋਤ_ਟ੍ਰੀ = 내부경로(ਪ੍ਰੋਜੈਕਟ_ਰੂਟ,(String)ਸੈਟਿੰਗ.get("source")), ਪੱਕੇ_ਹੋਣਾ_ਕੀਮਤ = 내부경로(ਸਰੋਤ_ਟ੍ਰੀ,(String)ਸੈਟਿੰਗ.get("native"));
        List<String> 소유파일들 = (List<String>)(List<?>)ਸੈਟਿੰਗ.get("owned_files");
        for (String ਨਾਂ : 소유파일들) if (!Files.isRegularFile(내부경로(ਸਰੋਤ_ਟ੍ਰੀ,ਨਾਂ))) throw new IOException("ਸਰੋਤ_ਟ੍ਰੀ 없음: " + ਨਾਂ);
        if (ਐਕਸ਼ਨ.equals("check")) { System.out.println(ਸੈਟਿੰਗ.get("country") + " " + ਸੈਟਿੰਗ.get("language") + " 독립 ਸਰੋਤ_ਟ੍ਰੀ ਤਸਦੀਕ 완료"); return; }
        String 자원상대 = (String)ਸੈਟਿੰਗ.getOrDefault("resource_root", ".");
        if (!자원상대.equals(".") && !자원상대.equals("..")) throw new IllegalArgumentException("의존성 ਪ੍ਰੋਜੈਕਟ_ਰੂਟ ਮਾਰਗ ਗਲਤੀ");
        Path ਸੰਸਾਧਨ_ਕੀਮਤ = ਪ੍ਰੋਜੈਕਟ_ਰੂਟ.resolve(자원상대).normalize(); Path ਸੰਗ੍ਰਹਿ_ਕੀਮਤ = ਸੰਸਾਧਨ_ਕੀਮਤ.resolve("native-vendor.tar.gz");
        String 기대해시 = (String)ਸੈਟਿੰਗ.get("vendor_sha256");
        if (!ਹੈਸ਼_ਲਿਖਤ_ਪੱਤਰ(ਸੰਗ੍ਰਹਿ_ਕੀਮਤ).equals(기대해시)) throw new IOException("의존성 SHA-256 불일치");
        Path 표식 = ਸਰੋਤ_ਟ੍ਰੀ.resolve(".vendor-sha256");
        if (!Files.isRegularFile(표식) || !Files.readString(표식).trim().equals(기대해시)) { ਕੱਢੋ(ਸੰਗ੍ਰਹਿ_ਕੀਮਤ, ਸਰੋਤ_ਟ੍ਰੀ); Files.writeString(표식,기대해시 + "\n"); }
        Map<String,String> 환경 = new HashMap<>(System.getenv());
        Path ipConfig = null;
        if (환경.containsKey("IP_CONFIG")) ipConfig = Paths.get(환경.get("IP_CONFIG")).toAbsolutePath().normalize();
        else for (Path parent = ਪ੍ਰੋਜੈਕਟ_ਰੂਟ; parent != null; parent = parent.getParent()) {
            if (Files.isRegularFile(parent.resolve("ip.conf"))) { ipConfig = parent.resolve("ip.conf"); break; }
        }
        if (ipConfig == null) ipConfig = ਸਰੋਤ_ਟ੍ਰੀ.resolve("ip.conf");
        if (!Files.isRegularFile(ipConfig)) throw new IOException("Missing ip.conf: " + ipConfig);
        환경.put("IP_CONFIG", ipConfig.toString());
        if (Arrays.asList("run","desktop","test-system").contains(ਐਕਸ਼ਨ) && !환경.containsKey("QEMU_AARCH64")) {
            Path ਐਪਲੀਕੇਸ਼_ਐਪ_ਡ੍ਰਾਅਰ = ਸੰਸਾਧਨ_ਕੀਮਤ.resolve("host/qemu"), 실행기표식 = ਸੰਸਾਧਨ_ਕੀਮਤ.resolve("host/.qemu-sha256");
            String ਐਪ_ਡ੍ਰਾਅਰ_ਹੈਸ਼ = (String)ਸੈਟਿੰਗ.get("qemu_sha256");
            if (!Files.isRegularFile(ਐਪਲੀਕੇਸ਼_ਐਪ_ਡ੍ਰਾਅਰ) || !Files.isRegularFile(실행기표식) || !Files.readString(실행기표식).trim().equals(ਐਪ_ਡ੍ਰਾਅਰ_ਹੈਸ਼)) {
                Path ਐਪ_ਡ੍ਰਾਅਰ_ਸੰਗ੍ਰਹਿ = ਸੰਸਾਧਨ_ਕੀਮਤ.resolve("qemu-host.tar.gz"); if (!ਹੈਸ਼_ਲਿਖਤ_ਪੱਤਰ(ਐਪ_ਡ੍ਰਾਅਰ_ਸੰਗ੍ਰਹਿ).equals(ਐਪ_ਡ੍ਰਾਅਰ_ਹੈਸ਼)) throw new IOException("QEMU SHA-256 불일치");
                ਕੱਢੋ(ਐਪ_ਡ੍ਰਾਅਰ_ਸੰਗ੍ਰਹਿ,ਸੰਸਾਧਨ_ਕੀਮਤ.resolve("host")); Files.writeString(실행기표식,ਐਪ_ਡ੍ਰਾਅਰ_ਹੈਸ਼ + "\n");
            }
            환경.put("QEMU_AARCH64",ਐਪਲੀਕੇਸ਼_ਐਪ_ਡ੍ਰਾਅਰ.toString());
        }
        MessageDigest 계산 = MessageDigest.getInstance("SHA-256"); Collections.sort(소유파일들);
        for (String ਨਾਂ : 소유파일들) { 계산.update(ਨਾਂ.getBytes(StandardCharsets.UTF_8)); 계산.update(Files.readAllBytes(내부경로(ਸਰੋਤ_ਟ੍ਰੀ,ਨਾਂ))); }
        계산.update("ip.conf\0".getBytes(StandardCharsets.UTF_8)); 계산.update(Files.readAllBytes(ipConfig));
        String ਸਰੋਤ_ਹੈਸ਼ = ਹੈਸ਼_ਪਾਠ(계산.digest()); Path 빌드표식 = ਪੱਕੇ_ਹੋਣਾ_ਕੀਮਤ.resolve("build/worldos-source.sha256");
        if (ਐਕਸ਼ਨ.equals("build") || !Files.isRegularFile(빌드표식) || !Files.readString(빌드표식).trim().equals(ਸਰੋਤ_ਹੈਸ਼)) {
            호출(ਪੱਕੇ_ਹੋਣਾ_ਕੀਮਤ,내부경로(ਪੱਕੇ_ਹੋਣਾ_ਕੀਮਤ,(String)ਸੈਟਿੰਗ.get("builder")),Collections.emptyList(),환경);
            Files.writeString(빌드표식,ਸਰੋਤ_ਹੈਸ਼ + "\n");
        }
        List<String> 추가인수 = new ArrayList<>(Arrays.asList(ਆਰਗੂਮੈਂਟ).subList(1,ਆਰਗੂਮੈਂਟ.length));
        if (ਐਕਸ਼ਨ.equals("run") || ਐਕਸ਼ਨ.equals("desktop")) {
            if (ਐਕਸ਼ਨ.equals("desktop")) 추가인수.add(0,"--desktop");
            호출(ਪੱਕੇ_ਹੋਣਾ_ਕੀਮਤ,내부경로(ਪੱਕੇ_ਹੋਣਾ_ਕੀਮਤ,(String)ਸੈਟਿੰਗ.get("runner")),추가인수,환경);
        } else if (ਐਕਸ਼ਨ.equals("image")) 호출(ਪੱਕੇ_ਹੋਣਾ_ਕੀਮਤ,내부경로(ਪੱਕੇ_ਹੋਣਾ_ਕੀਮਤ,(String)ਸੈਟਿੰਗ.get("image_builder")),추가인수,환경);
        else if (ਐਕਸ਼ਨ.equals("test-system")) {
            추가인수.add(0,ਪ੍ਰੋਜੈਕਟ_ਰੂਟ.toString()); 추가인수.add(0,"--edition");
            호출(ਪੱਕੇ_ਹੋਣਾ_ਕੀਮਤ,내부경로(ਪੱਕੇ_ਹੋਣਾ_ਕੀਮਤ,(String)ਸੈਟਿੰਗ.get("system_tester")),추가인수,환경);
        }
    }
}
