// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.security.MessageDigest;
import java.util.*;

/** 독립 국가판의 의존성 검사·복원·ግንብ_ስርዓት·실행을 맡는 አዘጋጅ_b78e430d Java መሳሪያዎች. */
public final class 국가실행기 {
    static final class ውሂብ_አግልሎ_ማስቀመጥ {
        final String ምንጭ; int አካባቢ;
        ውሂብ_አግልሎ_ማስቀመጥ(String ጽሁፍ) { ምንጭ = ጽሁፍ; }
        void 빈칸() { while (አካባቢ < ምንጭ.length() && Character.isWhitespace(ምንጭ.charAt(አካባቢ))) አካባቢ++; }
        Object ማንበቢያ() {
            빈칸(); char ቁምፊ_እሴት = ምንጭ.charAt(አካባቢ++);
            if (ቁምፊ_እሴት == '{') {
                Map<String,Object> ልኬት = new LinkedHashMap<>(); 빈칸();
                if (ምንጭ.charAt(አካባቢ) == '}') { አካባቢ++; return ልኬት; }
                while (true) {
                    String ስም = (String)ማንበቢያ(); 빈칸(); if (ምንጭ.charAt(አካባቢ++) != ':') throw new IllegalArgumentException("ውሂብ ገዳቢ_እሴት ስህተት");
                    ልኬት.put(ስም, ማንበቢያ()); 빈칸(); char ገዳቢ_እሴት = ምንጭ.charAt(አካባቢ++);
                    if (ገዳቢ_እሴት == '}') return ልኬት; if (ገዳቢ_እሴት != ',') throw new IllegalArgumentException("ውሂብ ገዳቢ_እሴት ስህተት");
                }
            }
            if (ቁምፊ_እሴት == '[') {
                List<Object> ልኬት = new ArrayList<>(); 빈칸();
                if (ምንጭ.charAt(አካባቢ) == ']') { አካባቢ++; return ልኬት; }
                while (true) {
                    ልኬት.add(ማንበቢያ()); 빈칸(); char ገዳቢ_እሴት = ምንጭ.charAt(አካባቢ++);
                    if (ገዳቢ_እሴት == ']') return ልኬት; if (ገዳቢ_እሴት != ',') throw new IllegalArgumentException("ውሂብ ገዳቢ_እሴት ስህተት");
                }
            }
            if (ቁምፊ_እሴት == '"') {
                StringBuilder ልኬት = new StringBuilder();
                while (true) {
                    char ቀጣይ_ንጥል_ነገር = ምንጭ.charAt(አካባቢ++); if (ቀጣይ_ንጥል_ነገር == '"') return ልኬት.toString();
                    if (ቀጣይ_ንጥል_ነገር == '\\') {
                        ቀጣይ_ንጥል_ነገር = ምንጭ.charAt(አካባቢ++);
                        if (ቀጣይ_ንጥል_ነገር == 'u') { ልኬት.append((char)Integer.parseInt(ምንጭ.substring(አካባቢ, አካባቢ + 4),16)); አካባቢ += 4; continue; }
                        if (ቀጣይ_ንጥል_ነገር == 'n') ቀጣይ_ንጥል_ነገር = '\n'; else if (ቀጣይ_ንጥል_ነገር == 'r') ቀጣይ_ንጥል_ነገር = '\r'; else if (ቀጣይ_ንጥል_ነገር == 't') ቀጣይ_ንጥል_ነገር = '\t';
                        else if (ቀጣይ_ንጥል_ነገር == 'b') ቀጣይ_ንጥል_ነገር = '\b'; else if (ቀጣይ_ንጥል_ነገር == 'f') ቀጣይ_ንጥል_ነገር = '\f';
                        else if (ቀጣይ_ንጥል_ነገር != '"' && ቀጣይ_ንጥል_ነገር != '\\' && ቀጣይ_ንጥል_ነገር != '/') throw new IllegalArgumentException("문자 이스케이프 ስህተት");
                    }
                    ልኬት.append(ቀጣይ_ንጥል_ነገር);
                }
            }
            int ማስኬጃ = አካባቢ - 1;
            while (አካባቢ < ምንጭ.length() && ",]} \t\r\n".indexOf(ምንጭ.charAt(አካባቢ)) < 0) አካባቢ++;
            String እሴት = ምንጭ.substring(ማስኬጃ, አካባቢ);
            if (እሴት.equals("true")) return Boolean.TRUE; if (እሴት.equals("false")) return Boolean.FALSE; if (እሴት.equals("null")) return null;
            return Double.valueOf(እሴት);
        }
    }
    static String ሃሽ_ፋይል(Path መተላለፊያ) throws Exception {
        MessageDigest 계산 = MessageDigest.getInstance("SHA-256"); byte[] ውሂብ = new byte[1024 * 1024];
        try (InputStream 입력 = Files.newInputStream(መተላለፊያ)) { for (int ርዝመት_እሴት; (ርዝመት_እሴት = 입력.read(ውሂብ)) >= 0;) 계산.update(ውሂብ,0,ርዝመት_እሴት); }
        return ሃሽ_ጽሁፍ(계산.digest());
    }
    static String ሃሽ_ጽሁፍ(byte[] ውሂብ) {
        StringBuilder ጽሁፍ = new StringBuilder(); for (byte እሴት : ውሂብ) ጽሁፍ.append(String.format(Locale.ROOT,"%02x",እሴት & 255)); return ጽሁፍ.toString();
    }
    static Path 내부경로(Path አሳይ_ስር, String ስም) {
        Path ልኬት = አሳይ_ስር.resolve(ስም).normalize();
        if (ስም.isEmpty() || Paths.get(ስም).isAbsolute() || !ልኬት.startsWith(አሳይ_ስር) || ስም.indexOf('\\') >= 0)
            throw new IllegalArgumentException("범위를 벗어난 መተላለፊያ: " + ስም);
        for (Path 부분 : Paths.get(ስም)) if (부분.toString().equals("..")) throw new IllegalArgumentException("상위 መተላለፊያ 금지: " + ስም);
        for (Path 현재 = ልኬት; 현재 != null && 현재.startsWith(አሳይ_ስር); 현재 = 현재.getParent())
            if (Files.isSymbolicLink(현재)) throw new IllegalArgumentException("의존성 경로의 링크 금지: " + ስም);
        return ልኬት;
    }
    static String 명령출력(List<String> ትእዛዝ) throws Exception {
        Process ሂደት_እሴት = new ProcessBuilder(ትእዛዝ).redirectError(ProcessBuilder.Redirect.INHERIT).start();
        String ልኬት = new String(ሂደት_እሴት.getInputStream().readAllBytes(),StandardCharsets.UTF_8);
        if (ሂደት_እሴት.waitFor() != 0) throw new IOException("ትእዛዝ ተስኖት_እሴት: " + ትእዛዝ.get(0)); return ልኬት;
    }
    static void ማውጣት(Path ከዝን_እሴት, Path መድረሻ_እሴት) throws Exception {
        for (String ስም : 명령출력(Arrays.asList("tar","-tzf",ከዝን_እሴት.toString())).split("\n")) 내부경로(መድረሻ_እሴት, ስም);
        for (String መስመር : 명령출력(Arrays.asList("tar","-tvzf",ከዝን_እሴት.toString())).split("\n"))
            if (!መስመር.isEmpty() && መስመር.charAt(0) != '-' && መስመር.charAt(0) != 'd') throw new IOException("외부 링크 또는 특수 파일을 포함한 의존성");
        Files.createDirectories(መድረሻ_እሴት);
        int ዞን_እሴት = new ProcessBuilder("tar","--no-same-owner","--no-same-permissions","-xzf",ከዝን_እሴት.toString(),"-C",መድረሻ_እሴት.toString()).inheritIO().start().waitFor();
        if (ዞን_እሴት != 0) throw new IOException("의존성 ከዝን_እሴት ልቀቅ_ማከማቻ ተስኖት_እሴት");
    }
    static void 호출(Path 작업경로, Path መሳሪያዎች, List<String> 인수, Map<String,String> 환경) throws Exception {
        List<String> ትእዛዝ = new ArrayList<>(Arrays.asList("python3", መሳሪያዎች.toString())); ትእዛዝ.addAll(인수);
        ProcessBuilder ፈጽም_ትእዛዝ = new ProcessBuilder(ትእዛዝ).directory(작업경로.toFile()).inheritIO(); ፈጽም_ትእዛዝ.environment().putAll(환경);
        int ዞን_እሴት = ፈጽም_ትእዛዝ.start().waitFor(); if (ዞን_እሴት != 0) throw new IOException("መሳሪያዎች ተስኖት_እሴት: " + መሳሪያዎች + " (" + ዞን_እሴት + ")");
    }
    @SuppressWarnings("unchecked")
    public static void main(String[] 인수) throws Exception {
        if (인수.length < 1) throw new IllegalArgumentException("build, run, desktop, image, check, test-system 중 동작을 지정하세요");
        String ተግባር = 인수[0];
        if (!Arrays.asList("build","run","desktop","image","check","test-system").contains(ተግባር)) throw new IllegalArgumentException("알 수 없는 ተግባር");
        Path አሳይ_ስር = Paths.get(System.getProperty("worldos.edition.root")).toAbsolutePath().normalize();
        Map<String,Object> ማሰናጃዎች = (Map<String,Object>)new ውሂብ_አግልሎ_ማስቀመጥ(Files.readString(አሳይ_ስር.resolve("native.json"),StandardCharsets.UTF_8)).ማንበቢያ();
        Path ምንጭ_ዛፍ = 내부경로(አሳይ_ስር,(String)ማሰናጃዎች.get("source")), ዓንኳር_እሴት = 내부경로(ምንጭ_ዛፍ,(String)ማሰናጃዎች.get("native"));
        List<String> 소유파일들 = (List<String>)(List<?>)ማሰናጃዎች.get("owned_files");
        for (String ስም : 소유파일들) if (!Files.isRegularFile(내부경로(ምንጭ_ዛፍ,ስም))) throw new IOException("ምንጭ_ዛፍ 없음: " + ስም);
        if (ተግባር.equals("check")) { System.out.println(ማሰናጃዎች.get("country") + " " + ማሰናጃዎች.get("language") + " 독립 ምንጭ_ዛፍ አረጋግጥ 완료"); return; }
        String 자원상대 = (String)ማሰናጃዎች.getOrDefault("resource_root", ".");
        if (!자원상대.equals(".") && !자원상대.equals("..")) throw new IllegalArgumentException("의존성 አሳይ_ስር መተላለፊያ ስህተት");
        Path ሃብት_እሴት = አሳይ_ስር.resolve(자원상대).normalize(); Path ከዝን_እሴት = ሃብት_እሴት.resolve("native-vendor.tar.gz");
        String 기대해시 = (String)ማሰናጃዎች.get("vendor_sha256");
        if (!ሃሽ_ፋይል(ከዝን_እሴት).equals(기대해시)) throw new IOException("의존성 SHA-256 불일치");
        Path 표식 = ምንጭ_ዛፍ.resolve(".vendor-sha256");
        if (!Files.isRegularFile(표식) || !Files.readString(표식).trim().equals(기대해시)) { ማውጣት(ከዝን_እሴት, ምንጭ_ዛፍ); Files.writeString(표식,기대해시 + "\n"); }
        Map<String,String> 환경 = new HashMap<>(System.getenv());
        Path ipConfig = null;
        if (환경.containsKey("IP_CONFIG")) ipConfig = Paths.get(환경.get("IP_CONFIG")).toAbsolutePath().normalize();
        else for (Path parent = አሳይ_ስር; parent != null; parent = parent.getParent()) {
            if (Files.isRegularFile(parent.resolve("ip.conf"))) { ipConfig = parent.resolve("ip.conf"); break; }
        }
        if (ipConfig == null) ipConfig = ምንጭ_ዛፍ.resolve("ip.conf");
        if (!Files.isRegularFile(ipConfig)) throw new IOException("Missing ip.conf: " + ipConfig);
        환경.put("IP_CONFIG", ipConfig.toString());
        if (Arrays.asList("run","desktop","test-system").contains(ተግባር) && !환경.containsKey("QEMU_AARCH64")) {
            Path ፕሮግራም_የመተግበሪያ_መሳቢያ = ሃብት_እሴት.resolve("host/qemu"), 실행기표식 = ሃብት_እሴት.resolve("host/.qemu-sha256");
            String የመተግበሪያ_መሳቢያ_ሃሽ = (String)ማሰናጃዎች.get("qemu_sha256");
            if (!Files.isRegularFile(ፕሮግራም_የመተግበሪያ_መሳቢያ) || !Files.isRegularFile(실행기표식) || !Files.readString(실행기표식).trim().equals(የመተግበሪያ_መሳቢያ_ሃሽ)) {
                Path የመተግበሪያ_መሳቢያ_ከዝን = ሃብት_እሴት.resolve("qemu-host.tar.gz"); if (!ሃሽ_ፋይል(የመተግበሪያ_መሳቢያ_ከዝን).equals(የመተግበሪያ_መሳቢያ_ሃሽ)) throw new IOException("QEMU SHA-256 불일치");
                ማውጣት(የመተግበሪያ_መሳቢያ_ከዝን,ሃብት_እሴት.resolve("host")); Files.writeString(실행기표식,የመተግበሪያ_መሳቢያ_ሃሽ + "\n");
            }
            환경.put("QEMU_AARCH64",ፕሮግራም_የመተግበሪያ_መሳቢያ.toString());
        }
        MessageDigest 계산 = MessageDigest.getInstance("SHA-256"); Collections.sort(소유파일들);
        for (String ስም : 소유파일들) { 계산.update(ስም.getBytes(StandardCharsets.UTF_8)); 계산.update(Files.readAllBytes(내부경로(ምንጭ_ዛፍ,ስም))); }
        계산.update("ip.conf\0".getBytes(StandardCharsets.UTF_8)); 계산.update(Files.readAllBytes(ipConfig));
        String ምንጭ_ሃሽ = ሃሽ_ጽሁፍ(계산.digest()); Path 빌드표식 = ዓንኳር_እሴት.resolve("build/worldos-source.sha256");
        if (ተግባር.equals("build") || !Files.isRegularFile(빌드표식) || !Files.readString(빌드표식).trim().equals(ምንጭ_ሃሽ)) {
            호출(ዓንኳር_እሴት,내부경로(ዓንኳር_እሴት,(String)ማሰናጃዎች.get("builder")),Collections.emptyList(),환경);
            Files.writeString(빌드표식,ምንጭ_ሃሽ + "\n");
        }
        List<String> 추가인수 = new ArrayList<>(Arrays.asList(인수).subList(1,인수.length));
        if (ተግባር.equals("run") || ተግባር.equals("desktop")) {
            if (ተግባር.equals("desktop")) 추가인수.add(0,"--desktop");
            호출(ዓንኳር_እሴት,내부경로(ዓንኳር_እሴት,(String)ማሰናጃዎች.get("runner")),추가인수,환경);
        } else if (ተግባር.equals("image")) 호출(ዓንኳር_እሴት,내부경로(ዓንኳር_እሴት,(String)ማሰናጃዎች.get("image_builder")),추가인수,환경);
        else if (ተግባር.equals("test-system")) {
            추가인수.add(0,አሳይ_ስር.toString()); 추가인수.add(0,"--edition");
            호출(ዓንኳር_እሴት,내부경로(ዓንኳር_እሴት,(String)ማሰናጃዎች.get("system_tester")),추가인수,환경);
        }
    }
}
