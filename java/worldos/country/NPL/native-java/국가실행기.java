// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.security.MessageDigest;
import java.util.*;

/** 독립 국가판의 의존성 검사·복원·बनाउनुहोस्_प्रणाली·실행을 맡는 होस्ट Java उपकरणहरू. */
public final class 국가실행기 {
    static final class 자료해석기 {
        final String स्रोत; int स्थिति;
        자료해석기(String पाठ) { स्रोत = पाठ; }
        void 빈칸() { while (स्थिति < स्रोत.length() && Character.isWhitespace(स्रोत.charAt(स्थिति))) स्थिति++; }
        Object पढनुहोस्() {
            빈칸(); char वर्ण_मान = स्रोत.charAt(स्थिति++);
            if (वर्ण_मान == '{') {
                Map<String,Object> मापन = new LinkedHashMap<>(); 빈칸();
                if (स्रोत.charAt(स्थिति) == '}') { स्थिति++; return मापन; }
                while (true) {
                    String नाम = (String)पढनुहोस्(); 빈칸(); if (स्रोत.charAt(स्थिति++) != ':') throw new IllegalArgumentException("लगत सीमानिर्धारण_मान त्रुटि");
                    मापन.put(नाम, पढनुहोस्()); 빈칸(); char सीमानिर्धारण_मान = स्रोत.charAt(स्थिति++);
                    if (सीमानिर्धारण_मान == '}') return मापन; if (सीमानिर्धारण_मान != ',') throw new IllegalArgumentException("लगत सीमानिर्धारण_मान त्रुटि");
                }
            }
            if (वर्ण_मान == '[') {
                List<Object> मापन = new ArrayList<>(); 빈칸();
                if (स्रोत.charAt(स्थिति) == ']') { स्थिति++; return मापन; }
                while (true) {
                    मापन.add(पढनुहोस्()); 빈칸(); char सीमानिर्धारण_मान = स्रोत.charAt(स्थिति++);
                    if (सीमानिर्धारण_मान == ']') return मापन; if (सीमानिर्धारण_मान != ',') throw new IllegalArgumentException("लगत सीमानिर्धारण_मान त्रुटि");
                }
            }
            if (वर्ण_मान == '"') {
                StringBuilder मापन = new StringBuilder();
                while (true) {
                    char अर्को_वस्तु = स्रोत.charAt(स्थिति++); if (अर्को_वस्तु == '"') return मापन.toString();
                    if (अर्को_वस्तु == '\\') {
                        अर्को_वस्तु = स्रोत.charAt(स्थिति++);
                        if (अर्को_वस्तु == 'u') { मापन.append((char)Integer.parseInt(स्रोत.substring(स्थिति, स्थिति + 4),16)); स्थिति += 4; continue; }
                        if (अर्को_वस्तु == 'n') अर्को_वस्तु = '\n'; else if (अर्को_वस्तु == 'r') अर्को_वस्तु = '\r'; else if (अर्को_वस्तु == 't') अर्को_वस्तु = '\t';
                        else if (अर्को_वस्तु == 'b') अर्को_वस्तु = '\b'; else if (अर्को_वस्तु == 'f') अर्को_वस्तु = '\f';
                        else if (अर्को_वस्तु != '"' && अर्को_वस्तु != '\\' && अर्को_वस्तु != '/') throw new IllegalArgumentException("문자 이스케이프 त्रुटि");
                    }
                    मापन.append(अर्को_वस्तु);
                }
            }
            int चलाउनुहोस् = स्थिति - 1;
            while (स्थिति < स्रोत.length() && ",]} \t\r\n".indexOf(स्रोत.charAt(स्थिति)) < 0) स्थिति++;
            String मान = स्रोत.substring(चलाउनुहोस्, स्थिति);
            if (मान.equals("true")) return Boolean.TRUE; if (मान.equals("false")) return Boolean.FALSE; if (मान.equals("null")) return null;
            return Double.valueOf(मान);
        }
    }
    static String ह्यास_फाइल(Path मार्ग) throws Exception {
        MessageDigest 계산 = MessageDigest.getInstance("SHA-256"); byte[] लगत = new byte[1024 * 1024];
        try (InputStream 입력 = Files.newInputStream(मार्ग)) { for (int लम्बाइ_मान; (लम्बाइ_मान = 입력.read(लगत)) >= 0;) 계산.update(लगत,0,लम्बाइ_मान); }
        return ह्यास_पाठ(계산.digest());
    }
    static String ह्यास_पाठ(byte[] लगत) {
        StringBuilder पाठ = new StringBuilder(); for (byte मान : लगत) पाठ.append(String.format(Locale.ROOT,"%02x",मान & 255)); return पाठ.toString();
    }
    static Path 내부경로(Path परियोजना_रूट, String नाम) {
        Path मापन = परियोजना_रूट.resolve(नाम).normalize();
        if (नाम.isEmpty() || Paths.get(नाम).isAbsolute() || !मापन.startsWith(परियोजना_रूट) || नाम.indexOf('\\') >= 0)
            throw new IllegalArgumentException("범위를 벗어난 मार्ग: " + नाम);
        for (Path 부분 : Paths.get(नाम)) if (부분.toString().equals("..")) throw new IllegalArgumentException("상위 मार्ग 금지: " + नाम);
        for (Path 현재 = मापन; 현재 != null && 현재.startsWith(परियोजना_रूट); 현재 = 현재.getParent())
            if (Files.isSymbolicLink(현재)) throw new IllegalArgumentException("의존성 경로의 링크 금지: " + नाम);
        return मापन;
    }
    static String 명령출력(List<String> आदेश) throws Exception {
        Process प्रक्रिया_मान = new ProcessBuilder(आदेश).redirectError(ProcessBuilder.Redirect.INHERIT).start();
        String मापन = new String(प्रक्रिया_मान.getInputStream().readAllBytes(),StandardCharsets.UTF_8);
        if (प्रक्रिया_मान.waitFor() != 0) throw new IOException("आदेश विफल_मान: " + आदेश.get(0)); return मापन;
    }
    static void झिक्नुहोस्(Path सङ्ग्रह_मान, Path गन्तव्य_मान) throws Exception {
        for (String नाम : 명령출력(Arrays.asList("tar","-tzf",सङ्ग्रह_मान.toString())).split("\n")) 내부경로(गन्तव्य_मान, नाम);
        for (String रेखा : 명령출력(Arrays.asList("tar","-tvzf",सङ्ग्रह_मान.toString())).split("\n"))
            if (!रेखा.isEmpty() && रेखा.charAt(0) != '-' && रेखा.charAt(0) != 'd') throw new IOException("외부 링크 또는 특수 파일을 포함한 의존성");
        Files.createDirectories(गन्तव्य_मान);
        int स्थिति_मान = new ProcessBuilder("tar","--no-same-owner","--no-same-permissions","-xzf",सङ्ग्रह_मान.toString(),"-C",गन्तव्य_मान.toString()).inheritIO().start().waitFor();
        if (स्थिति_मान != 0) throw new IOException("의존성 सङ्ग्रह_मान जारी_भण्डारण विफल_मान");
    }
    static void 호출(Path 작업경로, Path उपकरणहरू, List<String> तर्क, Map<String,String> 환경) throws Exception {
        List<String> आदेश = new ArrayList<>(Arrays.asList("python3", उपकरणहरू.toString())); आदेश.addAll(तर्क);
        ProcessBuilder कार्यान्वयन_गर्नुहोस्_आदेश = new ProcessBuilder(आदेश).directory(작업경로.toFile()).inheritIO(); कार्यान्वयन_गर्नुहोस्_आदेश.environment().putAll(환경);
        int स्थिति_मान = कार्यान्वयन_गर्नुहोस्_आदेश.start().waitFor(); if (स्थिति_मान != 0) throw new IOException("उपकरणहरू विफल_मान: " + उपकरणहरू + " (" + स्थिति_मान + ")");
    }
    @SuppressWarnings("unchecked")
    public static void main(String[] तर्क) throws Exception {
        if (तर्क.length < 1) throw new IllegalArgumentException("build, run, desktop, image, check, test-system 중 동작을 지정하세요");
        String कार्य = तर्क[0];
        if (!Arrays.asList("build","run","desktop","image","check","test-system").contains(कार्य)) throw new IllegalArgumentException("알 수 없는 कार्य");
        Path परियोजना_रूट = Paths.get(System.getProperty("worldos.edition.root")).toAbsolutePath().normalize();
        Map<String,Object> सेटिङ = (Map<String,Object>)new 자료해석기(Files.readString(परियोजना_रूट.resolve("native.json"),StandardCharsets.UTF_8)).पढनुहोस्();
        Path स्रोत_वृक्ष = 내부경로(परियोजना_रूट,(String)सेटिङ.get("source")), कर्णेल_मान = 내부경로(स्रोत_वृक्ष,(String)सेटिङ.get("native"));
        List<String> 소유파일들 = (List<String>)(List<?>)सेटिङ.get("owned_files");
        for (String नाम : 소유파일들) if (!Files.isRegularFile(내부경로(स्रोत_वृक्ष,नाम))) throw new IOException("स्रोत_वृक्ष 없음: " + नाम);
        if (कार्य.equals("check")) { System.out.println(सेटिङ.get("country") + " " + सेटिङ.get("language") + " 독립 स्रोत_वृक्ष रुजू_गर्नुहोस् 완료"); return; }
        String 자원상대 = (String)सेटिङ.getOrDefault("resource_root", ".");
        if (!자원상대.equals(".") && !자원상대.equals("..")) throw new IllegalArgumentException("의존성 परियोजना_रूट मार्ग त्रुटि");
        Path स्रोत_मान = परियोजना_रूट.resolve(자원상대).normalize(); Path सङ्ग्रह_मान = स्रोत_मान.resolve("native-vendor.tar.gz");
        String 기대해시 = (String)सेटिङ.get("vendor_sha256");
        if (!ह्यास_फाइल(सङ्ग्रह_मान).equals(기대해시)) throw new IOException("의존성 SHA-256 불일치");
        Path 표식 = स्रोत_वृक्ष.resolve(".vendor-sha256");
        if (!Files.isRegularFile(표식) || !Files.readString(표식).trim().equals(기대해시)) { झिक्नुहोस्(सङ्ग्रह_मान, स्रोत_वृक्ष); Files.writeString(표식,기대해시 + "\n"); }
        Map<String,String> 환경 = new HashMap<>(System.getenv());
        Path ipConfig = null;
        if (환경.containsKey("IP_CONFIG")) ipConfig = Paths.get(환경.get("IP_CONFIG")).toAbsolutePath().normalize();
        else for (Path parent = परियोजना_रूट; parent != null; parent = parent.getParent()) {
            if (Files.isRegularFile(parent.resolve("ip.conf"))) { ipConfig = parent.resolve("ip.conf"); break; }
        }
        if (ipConfig == null) ipConfig = स्रोत_वृक्ष.resolve("ip.conf");
        if (!Files.isRegularFile(ipConfig)) throw new IOException("Missing ip.conf: " + ipConfig);
        환경.put("IP_CONFIG", ipConfig.toString());
        if (Arrays.asList("run","desktop","test-system").contains(कार्य) && !환경.containsKey("QEMU_AARCH64")) {
            Path अनुप्रयोग_कर्मचारी_अगुवा = स्रोत_मान.resolve("host/qemu"), 실행기표식 = स्रोत_मान.resolve("host/.qemu-sha256");
            String कर्मचारी_अगुवा_ह्यास = (String)सेटिङ.get("qemu_sha256");
            if (!Files.isRegularFile(अनुप्रयोग_कर्मचारी_अगुवा) || !Files.isRegularFile(실행기표식) || !Files.readString(실행기표식).trim().equals(कर्मचारी_अगुवा_ह्यास)) {
                Path कर्मचारी_अगुवा_सङ्ग्रह = स्रोत_मान.resolve("qemu-host.tar.gz"); if (!ह्यास_फाइल(कर्मचारी_अगुवा_सङ्ग्रह).equals(कर्मचारी_अगुवा_ह्यास)) throw new IOException("QEMU SHA-256 불일치");
                झिक्नुहोस्(कर्मचारी_अगुवा_सङ्ग्रह,स्रोत_मान.resolve("host")); Files.writeString(실행기표식,कर्मचारी_अगुवा_ह्यास + "\n");
            }
            환경.put("QEMU_AARCH64",अनुप्रयोग_कर्मचारी_अगुवा.toString());
        }
        MessageDigest 계산 = MessageDigest.getInstance("SHA-256"); Collections.sort(소유파일들);
        for (String नाम : 소유파일들) { 계산.update(नाम.getBytes(StandardCharsets.UTF_8)); 계산.update(Files.readAllBytes(내부경로(स्रोत_वृक्ष,नाम))); }
        계산.update("ip.conf\0".getBytes(StandardCharsets.UTF_8)); 계산.update(Files.readAllBytes(ipConfig));
        String स्रोत_ह्यास = ह्यास_पाठ(계산.digest()); Path 빌드표식 = कर्णेल_मान.resolve("build/worldos-source.sha256");
        if (कार्य.equals("build") || !Files.isRegularFile(빌드표식) || !Files.readString(빌드표식).trim().equals(स्रोत_ह्यास)) {
            호출(कर्णेल_मान,내부경로(कर्णेल_मान,(String)सेटिङ.get("builder")),Collections.emptyList(),환경);
            Files.writeString(빌드표식,स्रोत_ह्यास + "\n");
        }
        List<String> 추가인수 = new ArrayList<>(Arrays.asList(तर्क).subList(1,तर्क.length));
        if (कार्य.equals("run") || कार्य.equals("desktop")) {
            if (कार्य.equals("desktop")) 추가인수.add(0,"--desktop");
            호출(कर्णेल_मान,내부경로(कर्णेल_मान,(String)सेटिङ.get("runner")),추가인수,환경);
        } else if (कार्य.equals("image")) 호출(कर्णेल_मान,내부경로(कर्णेल_मान,(String)सेटिङ.get("image_builder")),추가인수,환경);
        else if (कार्य.equals("test-system")) {
            추가인수.add(0,परियोजना_रूट.toString()); 추가인수.add(0,"--edition");
            호출(कर्णेल_मान,내부경로(कर्णेल_मान,(String)सेटिङ.get("system_tester")),추가인수,환경);
        }
    }
}
