// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.security.MessageDigest;
import java.util.*;

/** 독립 국가판의 의존성 검사·복원·ህነጽ_ስርዓት·실행을 맡는 አዐንግድ Java መሳርሒታት. */
public final class 국가실행기 {
    static final class 자료해석기 {
        final String ምንጪ; int 위치;
        자료해석기(String ጽሑፍ) { ምንጪ = ጽሑፍ; }
        void 빈칸() { while (위치 < ምንጪ.length() && Character.isWhitespace(ምንጪ.charAt(위치))) 위치++; }
        Object 읽기() {
            빈칸(); char ፊደል_ዋጋ = ምንጪ.charAt(위치++);
            if (ፊደል_ዋጋ == '{') {
                Map<String,Object> 결과 = new LinkedHashMap<>(); 빈칸();
                if (ምንጪ.charAt(위치) == '}') { 위치++; return 결과; }
                while (true) {
                    String ሽም = (String)읽기(); 빈칸(); if (ምንጪ.charAt(위치++) != ':') throw new IllegalArgumentException("ሓበሬታ ደራቲ_ዋጋ ጌጋ");
                    결과.put(ሽም, 읽기()); 빈칸(); char ደራቲ_ዋጋ = ምንጪ.charAt(위치++);
                    if (ደራቲ_ዋጋ == '}') return 결과; if (ደራቲ_ዋጋ != ',') throw new IllegalArgumentException("ሓበሬታ ደራቲ_ዋጋ ጌጋ");
                }
            }
            if (ፊደል_ዋጋ == '[') {
                List<Object> 결과 = new ArrayList<>(); 빈칸();
                if (ምንጪ.charAt(위치) == ']') { 위치++; return 결과; }
                while (true) {
                    결과.add(읽기()); 빈칸(); char ደራቲ_ዋጋ = ምንጪ.charAt(위치++);
                    if (ደራቲ_ዋጋ == ']') return 결과; if (ደራቲ_ዋጋ != ',') throw new IllegalArgumentException("ሓበሬታ ደራቲ_ዋጋ ጌጋ");
                }
            }
            if (ፊደል_ዋጋ == '"') {
                StringBuilder 결과 = new StringBuilder();
                while (true) {
                    char 다음 = ምንጪ.charAt(위치++); if (다음 == '"') return 결과.toString();
                    if (다음 == '\\') {
                        다음 = ምንጪ.charAt(위치++);
                        if (다음 == 'u') { 결과.append((char)Integer.parseInt(ምንጪ.substring(위치, 위치 + 4),16)); 위치 += 4; continue; }
                        if (다음 == 'n') 다음 = '\n'; else if (다음 == 'r') 다음 = '\r'; else if (다음 == 't') 다음 = '\t';
                        else if (다음 == 'b') 다음 = '\b'; else if (다음 == 'f') 다음 = '\f';
                        else if (다음 != '"' && 다음 != '\\' && 다음 != '/') throw new IllegalArgumentException("문자 이스케이프 ጌጋ");
                    }
                    결과.append(다음);
                }
            }
            int ኣኺድ = 위치 - 1;
            while (위치 < ምንጪ.length() && ",]} \t\r\n".indexOf(ምንጪ.charAt(위치)) < 0) 위치++;
            String ዋጋ = ምንጪ.substring(ኣኺድ, 위치);
            if (ዋጋ.equals("true")) return Boolean.TRUE; if (ዋጋ.equals("false")) return Boolean.FALSE; if (ዋጋ.equals("null")) return null;
            return Double.valueOf(ዋጋ);
        }
    }
    static String 해시(Path መገዲ) throws Exception {
        MessageDigest 계산 = MessageDigest.getInstance("SHA-256"); byte[] ሓበሬታ = new byte[1024 * 1024];
        try (InputStream 입력 = Files.newInputStream(መገዲ)) { for (int ንውሓት_ዋጋ; (ንውሓት_ዋጋ = 입력.read(ሓበሬታ)) >= 0;) 계산.update(ሓበሬታ,0,ንውሓት_ዋጋ); }
        return 해시글(계산.digest());
    }
    static String 해시글(byte[] ሓበሬታ) {
        StringBuilder ጽሑፍ = new StringBuilder(); for (byte ዋጋ : ሓበሬታ) ጽሑፍ.append(String.format(Locale.ROOT,"%02x",ዋጋ & 255)); return ጽሑፍ.toString();
    }
    static Path 내부경로(Path 기준, String ሽም) {
        Path 결과 = 기준.resolve(ሽም).normalize();
        if (ሽም.isEmpty() || Paths.get(ሽም).isAbsolute() || !결과.startsWith(기준) || ሽም.indexOf('\\') >= 0)
            throw new IllegalArgumentException("범위를 벗어난 መገዲ: " + ሽም);
        for (Path 부분 : Paths.get(ሽም)) if (부분.toString().equals("..")) throw new IllegalArgumentException("상위 መገዲ 금지: " + ሽም);
        for (Path 현재 = 결과; 현재 != null && 현재.startsWith(기준); 현재 = 현재.getParent())
            if (Files.isSymbolicLink(현재)) throw new IllegalArgumentException("의존성 경로의 링크 금지: " + ሽም);
        return 결과;
    }
    static String 명령출력(List<String> ትእዛዝ) throws Exception {
        Process መስርሕ_ዋጋ = new ProcessBuilder(ትእዛዝ).redirectError(ProcessBuilder.Redirect.INHERIT).start();
        String 결과 = new String(መስርሕ_ዋጋ.getInputStream().readAllBytes(),StandardCharsets.UTF_8);
        if (መስርሕ_ዋጋ.waitFor() != 0) throw new IOException("ትእዛዝ ፍሽለት_ዋጋ: " + ትእዛዝ.get(0)); return 결과;
    }
    static void ካብ_ማህደር_አውጽዕ(Path ሰንድ_ዋጋ, Path መዓልቦ_ዋጋ) throws Exception {
        for (String ሽም : 명령출력(Arrays.asList("tar","-tzf",ሰንድ_ዋጋ.toString())).split("\n")) 내부경로(መዓልቦ_ዋጋ, ሽም);
        for (String መስመር : 명령출력(Arrays.asList("tar","-tvzf",ሰንድ_ዋጋ.toString())).split("\n"))
            if (!መስመር.isEmpty() && መስመር.charAt(0) != '-' && መስመር.charAt(0) != 'd') throw new IOException("외부 링크 또는 특수 파일을 포함한 의존성");
        Files.createDirectories(መዓልቦ_ዋጋ);
        int ደረጃ_ዋጋ = new ProcessBuilder("tar","--no-same-owner","--no-same-permissions","-xzf",ሰንድ_ዋጋ.toString(),"-C",መዓልቦ_ዋጋ.toString()).inheritIO().start().waitFor();
        if (ደረጃ_ዋጋ != 0) throw new IOException("의존성 ሰንድ_ዋጋ ፍታሕ_መኽዘን ፍሽለት_ዋጋ");
    }
    static void 호출(Path 작업경로, Path መሳርሒታት, List<String> 인수, Map<String,String> 환경) throws Exception {
        List<String> ትእዛዝ = new ArrayList<>(Arrays.asList("python3", መሳርሒታት.toString())); ትእዛዝ.addAll(인수);
        ProcessBuilder ተግብር_ትእዛዝ = new ProcessBuilder(ትእዛዝ).directory(작업경로.toFile()).inheritIO(); ተግብር_ትእዛዝ.environment().putAll(환경);
        int ደረጃ_ዋጋ = ተግብር_ትእዛዝ.start().waitFor(); if (ደረጃ_ዋጋ != 0) throw new IOException("መሳርሒታት ፍሽለት_ዋጋ: " + መሳርሒታት + " (" + ደረጃ_ዋጋ + ")");
    }
    @SuppressWarnings("unchecked")
    public static void main(String[] 인수) throws Exception {
        if (인수.length < 1) throw new IllegalArgumentException("build, run, desktop, image, check, test-system 중 동작을 지정하세요");
        String ስጉምቲ = 인수[0];
        if (!Arrays.asList("build","run","desktop","image","check","test-system").contains(ስጉምቲ)) throw new IllegalArgumentException("알 수 없는 ስጉምቲ");
        Path 기준 = Paths.get(System.getProperty("worldos.edition.root")).toAbsolutePath().normalize();
        Map<String,Object> ኣቀማምጣታት = (Map<String,Object>)new 자료해석기(Files.readString(기준.resolve("native.json"),StandardCharsets.UTF_8)).읽기();
        Path ምንጪ_ገረብ = 내부경로(기준,(String)ኣቀማምጣታት.get("source")), ፍረ_ዋጋ = 내부경로(ምንጪ_ገረብ,(String)ኣቀማምጣታት.get("native"));
        List<String> 소유파일들 = (List<String>)(List<?>)ኣቀማምጣታት.get("owned_files");
        for (String ሽም : 소유파일들) if (!Files.isRegularFile(내부경로(ምንጪ_ገረብ,ሽም))) throw new IOException("ምንጪ_ገረብ 없음: " + ሽም);
        if (ስጉምቲ.equals("check")) { System.out.println(ኣቀማምጣታት.get("country") + " " + ኣቀማምጣታት.get("language") + " 독립 ምንጪ_ገረብ ኣረጋግጽ 완료"); return; }
        String 자원상대 = (String)ኣቀማምጣታት.getOrDefault("resource_root", ".");
        if (!자원상대.equals(".") && !자원상대.equals("..")) throw new IllegalArgumentException("의존성 기준 መገዲ ጌጋ");
        Path ሃብቲ_ዋጋ = 기준.resolve(자원상대).normalize(); Path ሰንድ_ዋጋ = ሃብቲ_ዋጋ.resolve("native-vendor.tar.gz");
        String 기대해시 = (String)ኣቀማምጣታት.get("vendor_sha256");
        if (!해시(ሰንድ_ዋጋ).equals(기대해시)) throw new IOException("의존성 SHA-256 불일치");
        Path 표식 = ምንጪ_ገረብ.resolve(".vendor-sha256");
        if (!Files.isRegularFile(표식) || !Files.readString(표식).trim().equals(기대해시)) { ካብ_ማህደር_አውጽዕ(ሰንድ_ዋጋ, ምንጪ_ገረብ); Files.writeString(표식,기대해시 + "\n"); }
        Map<String,String> 환경 = new HashMap<>(System.getenv());
        Path ipConfig = null;
        if (환경.containsKey("IP_CONFIG")) ipConfig = Paths.get(환경.get("IP_CONFIG")).toAbsolutePath().normalize();
        else for (Path parent = 기준; parent != null; parent = parent.getParent()) {
            if (Files.isRegularFile(parent.resolve("ip.conf"))) { ipConfig = parent.resolve("ip.conf"); break; }
        }
        if (ipConfig == null) ipConfig = ምንጪ_ገረብ.resolve("ip.conf");
        if (!Files.isRegularFile(ipConfig)) throw new IOException("Missing ip.conf: " + ipConfig);
        환경.put("IP_CONFIG", ipConfig.toString());
        if (Arrays.asList("run","desktop","test-system").contains(ስጉምቲ) && !환경.containsKey("QEMU_AARCH64")) {
            Path መተግበሪ_ተመዛዚ_መተግበሪ = ሃብቲ_ዋጋ.resolve("host/qemu"), 실행기표식 = ሃብቲ_ዋጋ.resolve("host/.qemu-sha256");
            String 실행기해시 = (String)ኣቀማምጣታት.get("qemu_sha256");
            if (!Files.isRegularFile(መተግበሪ_ተመዛዚ_መተግበሪ) || !Files.isRegularFile(실행기표식) || !Files.readString(실행기표식).trim().equals(실행기해시)) {
                Path ተመዛዚ_መተግበሪ_ሰንድ = ሃብቲ_ዋጋ.resolve("qemu-host.tar.gz"); if (!해시(ተመዛዚ_መተግበሪ_ሰንድ).equals(실행기해시)) throw new IOException("QEMU SHA-256 불일치");
                ካብ_ማህደር_አውጽዕ(ተመዛዚ_መተግበሪ_ሰንድ,ሃብቲ_ዋጋ.resolve("host")); Files.writeString(실행기표식,실행기해시 + "\n");
            }
            환경.put("QEMU_AARCH64",መተግበሪ_ተመዛዚ_መተግበሪ.toString());
        }
        MessageDigest 계산 = MessageDigest.getInstance("SHA-256"); Collections.sort(소유파일들);
        for (String ሽም : 소유파일들) { 계산.update(ሽም.getBytes(StandardCharsets.UTF_8)); 계산.update(Files.readAllBytes(내부경로(ምንጪ_ገረብ,ሽም))); }
        계산.update("ip.conf\0".getBytes(StandardCharsets.UTF_8)); 계산.update(Files.readAllBytes(ipConfig));
        String 소스해시 = 해시글(계산.digest()); Path 빌드표식 = ፍረ_ዋጋ.resolve("build/worldos-source.sha256");
        if (ስጉምቲ.equals("build") || !Files.isRegularFile(빌드표식) || !Files.readString(빌드표식).trim().equals(소스해시)) {
            호출(ፍረ_ዋጋ,내부경로(ፍረ_ዋጋ,(String)ኣቀማምጣታት.get("builder")),Collections.emptyList(),환경);
            Files.writeString(빌드표식,소스해시 + "\n");
        }
        List<String> 추가인수 = new ArrayList<>(Arrays.asList(인수).subList(1,인수.length));
        if (ስጉምቲ.equals("run") || ስጉምቲ.equals("desktop")) {
            if (ስጉምቲ.equals("desktop")) 추가인수.add(0,"--desktop");
            호출(ፍረ_ዋጋ,내부경로(ፍረ_ዋጋ,(String)ኣቀማምጣታት.get("runner")),추가인수,환경);
        } else if (ስጉምቲ.equals("image")) 호출(ፍረ_ዋጋ,내부경로(ፍረ_ዋጋ,(String)ኣቀማምጣታት.get("image_builder")),추가인수,환경);
        else if (ስጉምቲ.equals("test-system")) {
            추가인수.add(0,기준.toString()); 추가인수.add(0,"--edition");
            호출(ፍረ_ዋጋ,내부경로(ፍረ_ዋጋ,(String)ኣቀማምጣታት.get("system_tester")),추가인수,환경);
        }
    }
}
