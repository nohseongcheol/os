// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.security.MessageDigest;
import java.util.*;

/** 독립 국가판의 의존성 검사·복원·दाळचे_प्रणाली·실행을 맡는 येजमान Java साधनां. */
public final class 국가실행기 {
    static final class 자료해석기 {
        final String स्त्रोत; int स्थिती;
        자료해석기(String SMS) { स्त्रोत = SMS; }
        void 빈칸() { while (स्थिती < स्त्रोत.length() && Character.isWhitespace(स्त्रोत.charAt(स्थिती))) स्थिती++; }
        Object 읽기() {
            빈칸(); char वर्ण_मोल = स्त्रोत.charAt(स्थिती++);
            if (वर्ण_मोल == '{') {
                Map<String,Object> मेजप = new LinkedHashMap<>(); 빈칸();
                if (स्त्रोत.charAt(स्थिती) == '}') { स्थिती++; return मेजप; }
                while (true) {
                    String नांव = (String)읽기(); 빈칸(); if (स्त्रोत.charAt(स्थिती++) != ':') throw new IllegalArgumentException("डेटा डिलिमिटर_मोल चूक");
                    मेजप.put(नांव, 읽기()); 빈칸(); char डिलिमिटर_मोल = स्त्रोत.charAt(स्थिती++);
                    if (डिलिमिटर_मोल == '}') return मेजप; if (डिलिमिटर_मोल != ',') throw new IllegalArgumentException("डेटा डिलिमिटर_मोल चूक");
                }
            }
            if (वर्ण_मोल == '[') {
                List<Object> मेजप = new ArrayList<>(); 빈칸();
                if (स्त्रोत.charAt(स्थिती) == ']') { स्थिती++; return मेजप; }
                while (true) {
                    मेजप.add(읽기()); 빈칸(); char डिलिमिटर_मोल = स्त्रोत.charAt(स्थिती++);
                    if (डिलिमिटर_मोल == ']') return मेजप; if (डिलिमिटर_मोल != ',') throw new IllegalArgumentException("डेटा डिलिमिटर_मोल चूक");
                }
            }
            if (वर्ण_मोल == '"') {
                StringBuilder मेजप = new StringBuilder();
                while (true) {
                    char फुडलें_आयटम = स्त्रोत.charAt(स्थिती++); if (फुडलें_आयटम == '"') return मेजप.toString();
                    if (फुडलें_आयटम == '\\') {
                        फुडलें_आयटम = स्त्रोत.charAt(स्थिती++);
                        if (फुडलें_आयटम == 'u') { मेजप.append((char)Integer.parseInt(स्त्रोत.substring(स्थिती, स्थिती + 4),16)); स्थिती += 4; continue; }
                        if (फुडलें_आयटम == 'n') फुडलें_आयटम = '\n'; else if (फुडलें_आयटम == 'r') फुडलें_आयटम = '\r'; else if (फुडलें_आयटम == 't') फुडलें_आयटम = '\t';
                        else if (फुडलें_आयटम == 'b') फुडलें_आयटम = '\b'; else if (फुडलें_आयटम == 'f') फुडलें_आयटम = '\f';
                        else if (फुडलें_आयटम != '"' && फुडलें_आयटम != '\\' && फुडलें_आयटम != '/') throw new IllegalArgumentException("문자 이스케이프 चूक");
                    }
                    मेजप.append(फुडलें_आयटम);
                }
            }
            int चलोवप = स्थिती - 1;
            while (स्थिती < स्त्रोत.length() && ",]} \t\r\n".indexOf(स्त्रोत.charAt(स्थिती)) < 0) स्थिती++;
            String मोल = स्त्रोत.substring(चलोवप, स्थिती);
            if (मोल.equals("true")) return Boolean.TRUE; if (मोल.equals("false")) return Boolean.FALSE; if (मोल.equals("null")) return null;
            return Double.valueOf(मोल);
        }
    }
    static String हॅश_फायल(Path पाथ) throws Exception {
        MessageDigest 계산 = MessageDigest.getInstance("SHA-256"); byte[] डेटा = new byte[1024 * 1024];
        try (InputStream 입력 = Files.newInputStream(पाथ)) { for (int लांबाय_मोल; (लांबाय_मोल = 입력.read(डेटा)) >= 0;) 계산.update(डेटा,0,लांबाय_मोल); }
        return हॅश_SMS(계산.digest());
    }
    static String हॅश_SMS(byte[] डेटा) {
        StringBuilder SMS = new StringBuilder(); for (byte मोल : डेटा) SMS.append(String.format(Locale.ROOT,"%02x",मोल & 255)); return SMS.toString();
    }
    static Path 내부경로(Path प्रॉजॅक्ट_रूट, String नांव) {
        Path मेजप = प्रॉजॅक्ट_रूट.resolve(नांव).normalize();
        if (नांव.isEmpty() || Paths.get(नांव).isAbsolute() || !मेजप.startsWith(प्रॉजॅक्ट_रूट) || नांव.indexOf('\\') >= 0)
            throw new IllegalArgumentException("범위를 벗어난 पाथ: " + नांव);
        for (Path 부분 : Paths.get(नांव)) if (부분.toString().equals("..")) throw new IllegalArgumentException("상위 पाथ 금지: " + नांव);
        for (Path 현재 = मेजप; 현재 != null && 현재.startsWith(प्रॉजॅक्ट_रूट); 현재 = 현재.getParent())
            if (Files.isSymbolicLink(현재)) throw new IllegalArgumentException("의존성 경로의 링크 금지: " + नांव);
        return मेजप;
    }
    static String 명령출력(List<String> आदेश) throws Exception {
        Process प्रक्रिया_मोल = new ProcessBuilder(आदेश).redirectError(ProcessBuilder.Redirect.INHERIT).start();
        String मेजप = new String(प्रक्रिया_मोल.getInputStream().readAllBytes(),StandardCharsets.UTF_8);
        if (प्रक्रिया_मोल.waitFor() != 0) throw new IOException("आदेश अपेस_मोल: " + आदेश.get(0)); return मेजप;
    }
    static void ओडप(Path संग्रह_मोल, Path नियुक्त_स्थान_मोल) throws Exception {
        for (String नांव : 명령출력(Arrays.asList("tar","-tzf",संग्रह_मोल.toString())).split("\n")) 내부경로(नियुक्त_स्थान_मोल, नांव);
        for (String रेग : 명령출력(Arrays.asList("tar","-tvzf",संग्रह_मोल.toString())).split("\n"))
            if (!रेग.isEmpty() && रेग.charAt(0) != '-' && रेग.charAt(0) != 'd') throw new IOException("외부 링크 또는 특수 파일을 포함한 의존성");
        Files.createDirectories(नियुक्त_स्थान_मोल);
        int स्थिती_मोल_e10195a1 = new ProcessBuilder("tar","--no-same-owner","--no-same-permissions","-xzf",संग्रह_मोल.toString(),"-C",नियुक्त_स्थान_मोल.toString()).inheritIO().start().waitFor();
        if (स्थिती_मोल_e10195a1 != 0) throw new IOException("의존성 संग्रह_मोल रिलीज_सांठवण अपेस_मोल");
    }
    static void 호출(Path 작업경로, Path साधनां, List<String> 인수, Map<String,String> 환경) throws Exception {
        List<String> आदेश = new ArrayList<>(Arrays.asList("python3", साधनां.toString())); आदेश.addAll(인수);
        ProcessBuilder पाळो_दिवचो_आदेश = new ProcessBuilder(आदेश).directory(작업경로.toFile()).inheritIO(); पाळो_दिवचो_आदेश.environment().putAll(환경);
        int स्थिती_मोल_e10195a1 = पाळो_दिवचो_आदेश.start().waitFor(); if (स्थिती_मोल_e10195a1 != 0) throw new IOException("साधनां अपेस_मोल: " + साधनां + " (" + स्थिती_मोल_e10195a1 + ")");
    }
    @SuppressWarnings("unchecked")
    public static void main(String[] 인수) throws Exception {
        if (인수.length < 1) throw new IllegalArgumentException("build, run, desktop, image, check, test-system 중 동작을 지정하세요");
        String कृती = 인수[0];
        if (!Arrays.asList("build","run","desktop","image","check","test-system").contains(कृती)) throw new IllegalArgumentException("알 수 없는 कृती");
        Path प्रॉजॅक्ट_रूट = Paths.get(System.getProperty("worldos.edition.root")).toAbsolutePath().normalize();
        Map<String,Object> मांडावळी = (Map<String,Object>)new 자료해석기(Files.readString(प्रॉजॅक्ट_रूट.resolve("native.json"),StandardCharsets.UTF_8)).읽기();
        Path स्त्रोत_ट्री = 내부경로(प्रॉजॅक्ट_रूट,(String)मांडावळी.get("source")), कर्नेल_मोल = 내부경로(स्त्रोत_ट्री,(String)मांडावळी.get("native"));
        List<String> 소유파일들 = (List<String>)(List<?>)मांडावळी.get("owned_files");
        for (String नांव : 소유파일들) if (!Files.isRegularFile(내부경로(स्त्रोत_ट्री,नांव))) throw new IOException("स्त्रोत_ट्री 없음: " + नांव);
        if (कृती.equals("check")) { System.out.println(मांडावळी.get("country") + " " + मांडावळी.get("language") + " 독립 स्त्रोत_ट्री पुनर्तपासणी_करची 완료"); return; }
        String 자원상대 = (String)मांडावळी.getOrDefault("resource_root", ".");
        if (!자원상대.equals(".") && !자원상대.equals("..")) throw new IllegalArgumentException("의존성 प्रॉजॅक्ट_रूट पाथ चूक");
        Path साधनसामुग्री_मोल = प्रॉजॅक्ट_रूट.resolve(자원상대).normalize(); Path संग्रह_मोल = साधनसामुग्री_मोल.resolve("native-vendor.tar.gz");
        String 기대해시 = (String)मांडावळी.get("vendor_sha256");
        if (!हॅश_फायल(संग्रह_मोल).equals(기대해시)) throw new IOException("의존성 SHA-256 불일치");
        Path 표식 = स्त्रोत_ट्री.resolve(".vendor-sha256");
        if (!Files.isRegularFile(표식) || !Files.readString(표식).trim().equals(기대해시)) { ओडप(संग्रह_मोल, स्त्रोत_ट्री); Files.writeString(표식,기대해시 + "\n"); }
        Map<String,String> 환경 = new HashMap<>(System.getenv());
        Path ipConfig = null;
        if (환경.containsKey("IP_CONFIG")) ipConfig = Paths.get(환경.get("IP_CONFIG")).toAbsolutePath().normalize();
        else for (Path parent = प्रॉजॅक्ट_रूट; parent != null; parent = parent.getParent()) {
            if (Files.isRegularFile(parent.resolve("ip.conf"))) { ipConfig = parent.resolve("ip.conf"); break; }
        }
        if (ipConfig == null) ipConfig = स्त्रोत_ट्री.resolve("ip.conf");
        if (!Files.isRegularFile(ipConfig)) throw new IOException("Missing ip.conf: " + ipConfig);
        환경.put("IP_CONFIG", ipConfig.toString());
        if (Arrays.asList("run","desktop","test-system").contains(कृती) && !환경.containsKey("QEMU_AARCH64")) {
            Path एप्लिकेशन_ऍप्लिकेशन_ड्रॉवर = साधनसामुग्री_मोल.resolve("host/qemu"), 실행기표식 = साधनसामुग्री_मोल.resolve("host/.qemu-sha256");
            String ऍप्लिकेशन_ड्रॉवर_हॅश = (String)मांडावळी.get("qemu_sha256");
            if (!Files.isRegularFile(एप्लिकेशन_ऍप्लिकेशन_ड्रॉवर) || !Files.isRegularFile(실행기표식) || !Files.readString(실행기표식).trim().equals(ऍप्लिकेशन_ड्रॉवर_हॅश)) {
                Path ऍप्लिकेशन_ड्रॉवर_संग्रह = साधनसामुग्री_मोल.resolve("qemu-host.tar.gz"); if (!हॅश_फायल(ऍप्लिकेशन_ड्रॉवर_संग्रह).equals(ऍप्लिकेशन_ड्रॉवर_हॅश)) throw new IOException("QEMU SHA-256 불일치");
                ओडप(ऍप्लिकेशन_ड्रॉवर_संग्रह,साधनसामुग्री_मोल.resolve("host")); Files.writeString(실행기표식,ऍप्लिकेशन_ड्रॉवर_हॅश + "\n");
            }
            환경.put("QEMU_AARCH64",एप्लिकेशन_ऍप्लिकेशन_ड्रॉवर.toString());
        }
        MessageDigest 계산 = MessageDigest.getInstance("SHA-256"); Collections.sort(소유파일들);
        for (String नांव : 소유파일들) { 계산.update(नांव.getBytes(StandardCharsets.UTF_8)); 계산.update(Files.readAllBytes(내부경로(स्त्रोत_ट्री,नांव))); }
        계산.update("ip.conf\0".getBytes(StandardCharsets.UTF_8)); 계산.update(Files.readAllBytes(ipConfig));
        String स्त्रोत_हॅश = हॅश_SMS(계산.digest()); Path 빌드표식 = कर्नेल_मोल.resolve("build/worldos-source.sha256");
        if (कृती.equals("build") || !Files.isRegularFile(빌드표식) || !Files.readString(빌드표식).trim().equals(स्त्रोत_हॅश)) {
            호출(कर्नेल_मोल,내부경로(कर्नेल_मोल,(String)मांडावळी.get("builder")),Collections.emptyList(),환경);
            Files.writeString(빌드표식,स्त्रोत_हॅश + "\n");
        }
        List<String> 추가인수 = new ArrayList<>(Arrays.asList(인수).subList(1,인수.length));
        if (कृती.equals("run") || कृती.equals("desktop")) {
            if (कृती.equals("desktop")) 추가인수.add(0,"--desktop");
            호출(कर्नेल_मोल,내부경로(कर्नेल_मोल,(String)मांडावळी.get("runner")),추가인수,환경);
        } else if (कृती.equals("image")) 호출(कर्नेल_मोल,내부경로(कर्नेल_मोल,(String)मांडावळी.get("image_builder")),추가인수,환경);
        else if (कृती.equals("test-system")) {
            추가인수.add(0,प्रॉजॅक्ट_रूट.toString()); 추가인수.add(0,"--edition");
            호출(कर्नेल_मोल,내부경로(कर्नेल_मोल,(String)मांडावळी.get("system_tester")),추가인수,환경);
        }
    }
}
