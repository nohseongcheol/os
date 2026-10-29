// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.security.MessageDigest;
import java.util.*;

/** 독립 국가판의 의존성 검사·복원·बिल्ड_सिस्टम·실행을 맡는 आयोजक Java उपकरण. */
public final class देशप्रवर्तक {
    static final class डेटा_पार्सर {
        final String स्रोत; int स्थान;
        डेटा_पार्सर(String पाठ) { स्रोत = पाठ; }
        void 빈칸() { while (स्थान < स्रोत.length() && Character.isWhitespace(स्रोत.charAt(स्थान))) स्थान++; }
        Object पढ़ें() {
            빈칸(); char कैरेक्टर_मान = स्रोत.charAt(स्थान++);
            if (कैरेक्टर_मान == '{') {
                Map<String,Object> परिणाम = new LinkedHashMap<>(); 빈칸();
                if (स्रोत.charAt(स्थान) == '}') { स्थान++; return परिणाम; }
                while (true) {
                    String नाम = (String)पढ़ें(); 빈칸(); if (स्रोत.charAt(स्थान++) != ':') throw new IllegalArgumentException("आँकड़े डिलिमिटर_मान त्रुटि");
                    परिणाम.put(नाम, पढ़ें()); 빈칸(); char डिलिमिटर_मान = स्रोत.charAt(स्थान++);
                    if (डिलिमिटर_मान == '}') return परिणाम; if (डिलिमिटर_मान != ',') throw new IllegalArgumentException("आँकड़े डिलिमिटर_मान त्रुटि");
                }
            }
            if (कैरेक्टर_मान == '[') {
                List<Object> परिणाम = new ArrayList<>(); 빈칸();
                if (स्रोत.charAt(स्थान) == ']') { स्थान++; return परिणाम; }
                while (true) {
                    परिणाम.add(पढ़ें()); 빈칸(); char डिलिमिटर_मान = स्रोत.charAt(स्थान++);
                    if (डिलिमिटर_मान == ']') return परिणाम; if (डिलिमिटर_मान != ',') throw new IllegalArgumentException("आँकड़े डिलिमिटर_मान त्रुटि");
                }
            }
            if (कैरेक्टर_मान == '"') {
                StringBuilder परिणाम = new StringBuilder();
                while (true) {
                    char अगला_आइटम = स्रोत.charAt(स्थान++); if (अगला_आइटम == '"') return परिणाम.toString();
                    if (अगला_आइटम == '\\') {
                        अगला_आइटम = स्रोत.charAt(स्थान++);
                        if (अगला_आइटम == 'u') { परिणाम.append((char)Integer.parseInt(स्रोत.substring(स्थान, स्थान + 4),16)); स्थान += 4; continue; }
                        if (अगला_आइटम == 'n') अगला_आइटम = '\n'; else if (अगला_आइटम == 'r') अगला_आइटम = '\r'; else if (अगला_आइटम == 't') अगला_आइटम = '\t';
                        else if (अगला_आइटम == 'b') अगला_आइटम = '\b'; else if (अगला_आइटम == 'f') अगला_आइटम = '\f';
                        else if (अगला_आइटम != '"' && अगला_आइटम != '\\' && अगला_आइटम != '/') throw new IllegalArgumentException("문자 이스케이프 त्रुटि");
                    }
                    परिणाम.append(अगला_आइटम);
                }
            }
            int चलाएँ = स्थान - 1;
            while (स्थान < स्रोत.length() && ",]} \t\r\n".indexOf(स्रोत.charAt(स्थान)) < 0) स्थान++;
            String मान = स्रोत.substring(चलाएँ, स्थान);
            if (मान.equals("true")) return Boolean.TRUE; if (मान.equals("false")) return Boolean.FALSE; if (मान.equals("null")) return null;
            return Double.valueOf(मान);
        }
    }
    static String हैश_फ़ाइल(Path पथ) throws Exception {
        MessageDigest 계산 = MessageDigest.getInstance("SHA-256"); byte[] आँकड़े = new byte[1024 * 1024];
        try (InputStream 입력 = Files.newInputStream(पथ)) { for (int 길이; (길이 = 입력.read(आँकड़े)) >= 0;) 계산.update(आँकड़े,0,길이); }
        return हैश_पाठ(계산.digest());
    }
    static String हैश_पाठ(byte[] आँकड़े) {
        StringBuilder पाठ = new StringBuilder(); for (byte मान : आँकड़े) पाठ.append(String.format(Locale.ROOT,"%02x",मान & 255)); return पाठ.toString();
    }
    static Path 내부경로(Path प्रोजेक्ट_करें_मूल, String नाम) {
        Path परिणाम = प्रोजेक्ट_करें_मूल.resolve(नाम).normalize();
        if (नाम.isEmpty() || Paths.get(नाम).isAbsolute() || !परिणाम.startsWith(प्रोजेक्ट_करें_मूल) || नाम.indexOf('\\') >= 0)
            throw new IllegalArgumentException("범위를 벗어난 पथ: " + नाम);
        for (Path 부분 : Paths.get(नाम)) if (부분.toString().equals("..")) throw new IllegalArgumentException("상위 पथ 금지: " + नाम);
        for (Path अद्यतित_आइटम = परिणाम; अद्यतित_आइटम != null && अद्यतित_आइटम.startsWith(प्रोजेक्ट_करें_मूल); अद्यतित_आइटम = अद्यतित_आइटम.getParent())
            if (Files.isSymbolicLink(अद्यतित_आइटम)) throw new IllegalArgumentException("의존성 경로의 링크 금지: " + नाम);
        return परिणाम;
    }
    static String 명령출력(List<String> आदेश) throws Exception {
        Process प्रक्रिया_मान = new ProcessBuilder(आदेश).redirectError(ProcessBuilder.Redirect.INHERIT).start();
        String परिणाम = new String(प्रक्रिया_मान.getInputStream().readAllBytes(),StandardCharsets.UTF_8);
        if (प्रक्रिया_मान.waitFor() != 0) throw new IOException("आदेश विफलता_मान: " + आदेश.get(0)); return परिणाम;
    }
    static void निकालें(Path संग्रह_मान, Path गंतव्य_मान) throws Exception {
        for (String नाम : 명령출력(Arrays.asList("tar","-tzf",संग्रह_मान.toString())).split("\n")) 내부경로(गंतव्य_मान, नाम);
        for (String पंक्ति : 명령출력(Arrays.asList("tar","-tvzf",संग्रह_मान.toString())).split("\n"))
            if (!पंक्ति.isEmpty() && पंक्ति.charAt(0) != '-' && पंक्ति.charAt(0) != 'd') throw new IOException("बाहरी_मान 링크 또는 특수 파일을 포함한 의존성");
        Files.createDirectories(गंतव्य_मान);
        int अवस्था_मान = new ProcessBuilder("tar","--no-same-owner","--no-same-permissions","-xzf",संग्रह_मान.toString(),"-C",गंतव्य_मान.toString()).inheritIO().start().waitFor();
        if (अवस्था_मान != 0) throw new IOException("의존성 संग्रह_मान रिलीज़_संग्रहण विफलता_मान");
    }
    static void 호출(Path 작업경로, Path उपकरण, List<String> तर्क, Map<String,String> 환경) throws Exception {
        List<String> आदेश = new ArrayList<>(Arrays.asList("python3", उपकरण.toString())); आदेश.addAll(तर्क);
        ProcessBuilder निष्पादित_करें_आदेश = new ProcessBuilder(आदेश).directory(작업경로.toFile()).inheritIO(); निष्पादित_करें_आदेश.environment().putAll(환경);
        int अवस्था_मान = निष्पादित_करें_आदेश.start().waitFor(); if (अवस्था_मान != 0) throw new IOException("उपकरण विफलता_मान: " + उपकरण + " (" + अवस्था_मान + ")");
    }
    @SuppressWarnings("unchecked")
    public static void main(String[] तर्क) throws Exception {
        if (तर्क.length < 1) throw new IllegalArgumentException("build, run, desktop, image, check, test-system 중 동작을 지정하세요");
        String क्रिया = तर्क[0];
        if (!Arrays.asList("build","run","desktop","image","check","test-system").contains(क्रिया)) throw new IllegalArgumentException("알 수 없는 क्रिया");
        Path प्रोजेक्ट_करें_मूल = Paths.get(System.getProperty("worldos.edition.root")).toAbsolutePath().normalize();
        Map<String,Object> विन्यास = (Map<String,Object>)new डेटा_पार्सर(Files.readString(प्रोजेक्ट_करें_मूल.resolve("native.json"),StandardCharsets.UTF_8)).पढ़ें();
        Path स्रोत_ट्री = 내부경로(प्रोजेक्ट_करें_मूल,(String)विन्यास.get("source")), कर्नेल_मान = 내부경로(स्रोत_ट्री,(String)विन्यास.get("native"));
        List<String> 소유파일들 = (List<String>)(List<?>)विन्यास.get("owned_files");
        for (String नाम : 소유파일들) if (!Files.isRegularFile(내부경로(स्रोत_ट्री,नाम))) throw new IOException("स्रोत_ट्री 없음: " + नाम);
        if (क्रिया.equals("check")) { System.out.println(विन्यास.get("country") + " " + विन्यास.get("language") + " 독립 स्रोत_ट्री सत्यापित_करें 완료"); return; }
        String संसाधन_संबंधित_पथ = (String)विन्यास.getOrDefault("resource_root", ".");
        if (!संसाधन_संबंधित_पथ.equals(".") && !संसाधन_संबंधित_पथ.equals("..")) throw new IllegalArgumentException("의존성 प्रोजेक्ट_करें_मूल पथ त्रुटि");
        Path संसाधन_मान = प्रोजेक्ट_करें_मूल.resolve(संसाधन_संबंधित_पथ).normalize(); Path संग्रह_मान = संसाधन_मान.resolve("native-vendor.tar.gz");
        String 기대해시 = (String)विन्यास.get("vendor_sha256");
        if (!हैश_फ़ाइल(संग्रह_मान).equals(기대해시)) throw new IOException("의존성 SHA-256 불일치");
        Path मार्कर_मान = स्रोत_ट्री.resolve(".vendor-sha256");
        if (!Files.isRegularFile(मार्कर_मान) || !Files.readString(मार्कर_मान).trim().equals(기대해시)) { निकालें(संग्रह_मान, स्रोत_ट्री); Files.writeString(मार्कर_मान,기대해시 + "\n"); }
        Map<String,String> 환경 = new HashMap<>(System.getenv());
        Path ipConfig = null;
        if (환경.containsKey("IP_CONFIG")) ipConfig = Paths.get(환경.get("IP_CONFIG")).toAbsolutePath().normalize();
        else for (Path parent = प्रोजेक्ट_करें_मूल; parent != null; parent = parent.getParent()) {
            if (Files.isRegularFile(parent.resolve("ip.conf"))) { ipConfig = parent.resolve("ip.conf"); break; }
        }
        if (ipConfig == null) ipConfig = स्रोत_ट्री.resolve("ip.conf");
        if (!Files.isRegularFile(ipConfig)) throw new IOException("Missing ip.conf: " + ipConfig);
        환경.put("IP_CONFIG", ipConfig.toString());
        if (Arrays.asList("run","desktop","test-system").contains(क्रिया) && !환경.containsKey("QEMU_AARCH64")) {
            Path ऐप_लॉन्चर = संसाधन_मान.resolve("host/qemu"), लॉन्चर_मार्कर = संसाधन_मान.resolve("host/.qemu-sha256");
            String लॉन्चर_हैश = (String)विन्यास.get("qemu_sha256");
            if (!Files.isRegularFile(ऐप_लॉन्चर) || !Files.isRegularFile(लॉन्चर_मार्कर) || !Files.readString(लॉन्चर_मार्कर).trim().equals(लॉन्चर_हैश)) {
                Path लॉन्चर_संग्रह = संसाधन_मान.resolve("qemu-host.tar.gz"); if (!हैश_फ़ाइल(लॉन्चर_संग्रह).equals(लॉन्चर_हैश)) throw new IOException("QEMU SHA-256 불일치");
                निकालें(लॉन्चर_संग्रह,संसाधन_मान.resolve("host")); Files.writeString(लॉन्चर_मार्कर,लॉन्चर_हैश + "\n");
            }
            환경.put("QEMU_AARCH64",ऐप_लॉन्चर.toString());
        }
        MessageDigest 계산 = MessageDigest.getInstance("SHA-256"); Collections.sort(소유파일들);
        for (String नाम : 소유파일들) { 계산.update(नाम.getBytes(StandardCharsets.UTF_8)); 계산.update(Files.readAllBytes(내부경로(स्रोत_ट्री,नाम))); }
        계산.update("ip.conf\0".getBytes(StandardCharsets.UTF_8)); 계산.update(Files.readAllBytes(ipConfig));
        String स्रोत_हैश = हैश_पाठ(계산.digest()); Path बिल्ड_मार्कर = कर्नेल_मान.resolve("build/worldos-source.sha256");
        if (क्रिया.equals("build") || !Files.isRegularFile(बिल्ड_मार्कर) || !Files.readString(बिल्ड_मार्कर).trim().equals(स्रोत_हैश)) {
            호출(कर्नेल_मान,내부경로(कर्नेल_मान,(String)विन्यास.get("builder")),Collections.emptyList(),환경);
            Files.writeString(बिल्ड_मार्कर,स्रोत_हैश + "\n");
        }
        List<String> 추가인수 = new ArrayList<>(Arrays.asList(तर्क).subList(1,तर्क.length));
        if (क्रिया.equals("run") || क्रिया.equals("desktop")) {
            if (क्रिया.equals("desktop")) 추가인수.add(0,"--desktop");
            호출(कर्नेल_मान,내부경로(कर्नेल_मान,(String)विन्यास.get("runner")),추가인수,환경);
        } else if (क्रिया.equals("image")) 호출(कर्नेल_मान,내부경로(कर्नेल_मान,(String)विन्यास.get("image_builder")),추가인수,환경);
        else if (क्रिया.equals("test-system")) {
            추가인수.add(0,प्रोजेक्ट_करें_मूल.toString()); 추가인수.add(0,"--edition");
            호출(कर्नेल_मान,내부경로(कर्नेल_मान,(String)विन्यास.get("system_tester")),추가인수,환경);
        }
    }
}
