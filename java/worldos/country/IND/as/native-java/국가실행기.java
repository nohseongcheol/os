// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.security.MessageDigest;
import java.util.*;

/** 독립 국가판의 의존성 검사·복원·বিল্ড_ছিষ্টেম·실행을 맡는 হ_ষ্ট Java সঁজুলিসমূহ. */
public final class 국가실행기 {
    static final class 자료해석기 {
        final String উৎস; int অৱস্থান;
        자료해석기(String টেক্সট) { উৎস = টেক্সট; }
        void 빈칸() { while (অৱস্থান < উৎস.length() && Character.isWhitespace(উৎস.charAt(অৱস্থান))) অৱস্থান++; }
        Object পড়া() {
            빈칸(); char বৰ্ণ_মান = উৎস.charAt(অৱস্থান++);
            if (বৰ্ণ_মান == '{') {
                Map<String,Object> পৰিমাপ = new LinkedHashMap<>(); 빈칸();
                if (উৎস.charAt(অৱস্থান) == '}') { অৱস্থান++; return পৰিমাপ; }
                while (true) {
                    String নাম = (String)পড়া(); 빈칸(); if (উৎস.charAt(অৱস্থান++) != ':') throw new IllegalArgumentException("ডাটা সীমানিৰ্দ্ধাৰক_মান ত্ৰুটি");
                    পৰিমাপ.put(নাম, পড়া()); 빈칸(); char সীমানিৰ্দ্ধাৰক_মান = উৎস.charAt(অৱস্থান++);
                    if (সীমানিৰ্দ্ধাৰক_মান == '}') return পৰিমাপ; if (সীমানিৰ্দ্ধাৰক_মান != ',') throw new IllegalArgumentException("ডাটা সীমানিৰ্দ্ধাৰক_মান ত্ৰুটি");
                }
            }
            if (বৰ্ণ_মান == '[') {
                List<Object> পৰিমাপ = new ArrayList<>(); 빈칸();
                if (উৎস.charAt(অৱস্থান) == ']') { অৱস্থান++; return পৰিমাপ; }
                while (true) {
                    পৰিমাপ.add(পড়া()); 빈칸(); char সীমানিৰ্দ্ধাৰক_মান = উৎস.charAt(অৱস্থান++);
                    if (সীমানিৰ্দ্ধাৰক_মান == ']') return পৰিমাপ; if (সীমানিৰ্দ্ধাৰক_মান != ',') throw new IllegalArgumentException("ডাটা সীমানিৰ্দ্ধাৰক_মান ত্ৰুটি");
                }
            }
            if (বৰ্ণ_মান == '"') {
                StringBuilder পৰিমাপ = new StringBuilder();
                while (true) {
                    char পৰৱৰ্তী_আইটেম = উৎস.charAt(অৱস্থান++); if (পৰৱৰ্তী_আইটেম == '"') return পৰিমাপ.toString();
                    if (পৰৱৰ্তী_আইটেম == '\\') {
                        পৰৱৰ্তী_আইটেম = উৎস.charAt(অৱস্থান++);
                        if (পৰৱৰ্তী_আইটেম == 'u') { পৰিমাপ.append((char)Integer.parseInt(উৎস.substring(অৱস্থান, অৱস্থান + 4),16)); অৱস্থান += 4; continue; }
                        if (পৰৱৰ্তী_আইটেম == 'n') পৰৱৰ্তী_আইটেম = '\n'; else if (পৰৱৰ্তী_আইটেম == 'r') পৰৱৰ্তী_আইটেম = '\r'; else if (পৰৱৰ্তী_আইটেম == 't') পৰৱৰ্তী_আইটেম = '\t';
                        else if (পৰৱৰ্তী_আইটেম == 'b') পৰৱৰ্তী_আইটেম = '\b'; else if (পৰৱৰ্তী_আইটেম == 'f') পৰৱৰ্তী_আইটেম = '\f';
                        else if (পৰৱৰ্তী_আইটেম != '"' && পৰৱৰ্তী_আইটেম != '\\' && পৰৱৰ্তী_আইটেম != '/') throw new IllegalArgumentException("문자 이스케이프 ত্ৰুটি");
                    }
                    পৰিমাপ.append(পৰৱৰ্তী_আইটেম);
                }
            }
            int সঞ্চালন = অৱস্থান - 1;
            while (অৱস্থান < উৎস.length() && ",]} \t\r\n".indexOf(উৎস.charAt(অৱস্থান)) < 0) অৱস্থান++;
            String মান = উৎস.substring(সঞ্চালন, অৱস্থান);
            if (মান.equals("true")) return Boolean.TRUE; if (মান.equals("false")) return Boolean.FALSE; if (মান.equals("null")) return null;
            return Double.valueOf(মান);
        }
    }
    static String হেচ_ফাইল(Path পথ) throws Exception {
        MessageDigest 계산 = MessageDigest.getInstance("SHA-256"); byte[] ডাটা = new byte[1024 * 1024];
        try (InputStream 입력 = Files.newInputStream(পথ)) { for (int দৈর্ঘ্য_মান; (দৈর্ঘ্য_মান = 입력.read(ডাটা)) >= 0;) 계산.update(ডাটা,0,দৈর্ঘ্য_মান); }
        return হেচ_পাঠ(계산.digest());
    }
    static String হেচ_পাঠ(byte[] ডাটা) {
        StringBuilder টেক্সট = new StringBuilder(); for (byte মান : ডাটা) টেক্সট.append(String.format(Locale.ROOT,"%02x",মান & 255)); return টেক্সট.toString();
    }
    static Path 내부경로(Path 기준, String নাম) {
        Path পৰিমাপ = 기준.resolve(নাম).normalize();
        if (নাম.isEmpty() || Paths.get(নাম).isAbsolute() || !পৰিমাপ.startsWith(기준) || নাম.indexOf('\\') >= 0)
            throw new IllegalArgumentException("범위를 벗어난 পথ: " + নাম);
        for (Path 부분 : Paths.get(নাম)) if (부분.toString().equals("..")) throw new IllegalArgumentException("상위 পথ 금지: " + নাম);
        for (Path 현재 = পৰিমাপ; 현재 != null && 현재.startsWith(기준); 현재 = 현재.getParent())
            if (Files.isSymbolicLink(현재)) throw new IllegalArgumentException("의존성 경로의 링크 금지: " + নাম);
        return পৰিমাপ;
    }
    static String 명령출력(List<String> কমান্ড) throws Exception {
        Process প্ৰক্ৰিয়া_মান = new ProcessBuilder(কমান্ড).redirectError(ProcessBuilder.Redirect.INHERIT).start();
        String পৰিমাপ = new String(প্ৰক্ৰিয়া_মান.getInputStream().readAllBytes(),StandardCharsets.UTF_8);
        if (প্ৰক্ৰিয়া_মান.waitFor() != 0) throw new IOException("কমান্ড বিফলতা_মান: " + কমান্ড.get(0)); return পৰিমাপ;
    }
    static void এক্সট্ৰেক্ট_কৰক(Path অভিলেখাগাৰ_মান, Path গন্তব্য_স্থান_মান) throws Exception {
        for (String নাম : 명령출력(Arrays.asList("tar","-tzf",অভিলেখাগাৰ_মান.toString())).split("\n")) 내부경로(গন্তব্য_স্থান_মান, নাম);
        for (String লাইন : 명령출력(Arrays.asList("tar","-tvzf",অভিলেখাগাৰ_মান.toString())).split("\n"))
            if (!লাইন.isEmpty() && লাইন.charAt(0) != '-' && লাইন.charAt(0) != 'd') throw new IOException("외부 링크 또는 특수 파일을 포함한 의존성");
        Files.createDirectories(গন্তব্য_স্থান_মান);
        int অৱস্থা_মান = new ProcessBuilder("tar","--no-same-owner","--no-same-permissions","-xzf",অভিলেখাগাৰ_মান.toString(),"-C",গন্তব্য_স্থান_মান.toString()).inheritIO().start().waitFor();
        if (অৱস্থা_মান != 0) throw new IOException("의존성 অভিলেখাগাৰ_মান ৰিলিজ_ষ্ট_ৰেজ বিফলতা_মান");
    }
    static void 호출(Path 작업경로, Path সঁজুলিসমূহ, List<String> 인수, Map<String,String> 환경) throws Exception {
        List<String> কমান্ড = new ArrayList<>(Arrays.asList("python3", সঁজুলিসমূহ.toString())); কমান্ড.addAll(인수);
        ProcessBuilder নিষ্পাদন_আদেশ = new ProcessBuilder(কমান্ড).directory(작업경로.toFile()).inheritIO(); নিষ্পাদন_আদেশ.environment().putAll(환경);
        int অৱস্থা_মান = নিষ্পাদন_আদেশ.start().waitFor(); if (অৱস্থা_মান != 0) throw new IOException("সঁজুলিসমূহ বিফলতা_মান: " + সঁজুলিসমূহ + " (" + অৱস্থা_মান + ")");
    }
    @SuppressWarnings("unchecked")
    public static void main(String[] 인수) throws Exception {
        if (인수.length < 1) throw new IllegalArgumentException("build, run, desktop, image, check, test-system 중 동작을 지정하세요");
        String কাৰ্য্য = 인수[0];
        if (!Arrays.asList("build","run","desktop","image","check","test-system").contains(কাৰ্য্য)) throw new IllegalArgumentException("알 수 없는 কাৰ্য্য");
        Path 기준 = Paths.get(System.getProperty("worldos.edition.root")).toAbsolutePath().normalize();
        Map<String,Object> বৈশিষ্ট্য = (Map<String,Object>)new 자료해석기(Files.readString(기준.resolve("native.json"),StandardCharsets.UTF_8)).পড়া();
        Path উৎস_ট্ৰি = 내부경로(기준,(String)বৈশিষ্ট্য.get("source")), কাৰ্ণেল_মান = 내부경로(উৎস_ট্ৰি,(String)বৈশিষ্ট্য.get("native"));
        List<String> 소유파일들 = (List<String>)(List<?>)বৈশিষ্ট্য.get("owned_files");
        for (String নাম : 소유파일들) if (!Files.isRegularFile(내부경로(উৎস_ট্ৰি,নাম))) throw new IOException("উৎস_ট্ৰি 없음: " + নাম);
        if (কাৰ্য্য.equals("check")) { System.out.println(বৈশিষ্ট্য.get("country") + " " + বৈশিষ্ট্য.get("language") + " 독립 উৎস_ট্ৰি প্ৰমাণিত_কৰক 완료"); return; }
        String 자원상대 = (String)বৈশিষ্ট্য.getOrDefault("resource_root", ".");
        if (!자원상대.equals(".") && !자원상대.equals("..")) throw new IllegalArgumentException("의존성 기준 পথ ত্ৰুটি");
        Path সম্পদ_মান = 기준.resolve(자원상대).normalize(); Path অভিলেখাগাৰ_মান = সম্পদ_মান.resolve("native-vendor.tar.gz");
        String 기대해시 = (String)বৈশিষ্ট্য.get("vendor_sha256");
        if (!হেচ_ফাইল(অভিলেখাগাৰ_মান).equals(기대해시)) throw new IOException("의존성 SHA-256 불일치");
        Path 표식 = উৎস_ট্ৰি.resolve(".vendor-sha256");
        if (!Files.isRegularFile(표식) || !Files.readString(표식).trim().equals(기대해시)) { এক্সট্ৰেক্ট_কৰক(অভিলেখাগাৰ_মান, উৎস_ট্ৰি); Files.writeString(표식,기대해시 + "\n"); }
        Map<String,String> 환경 = new HashMap<>(System.getenv());
        Path ipConfig = null;
        if (환경.containsKey("IP_CONFIG")) ipConfig = Paths.get(환경.get("IP_CONFIG")).toAbsolutePath().normalize();
        else for (Path parent = 기준; parent != null; parent = parent.getParent()) {
            if (Files.isRegularFile(parent.resolve("ip.conf"))) { ipConfig = parent.resolve("ip.conf"); break; }
        }
        if (ipConfig == null) ipConfig = উৎস_ট্ৰি.resolve("ip.conf");
        if (!Files.isRegularFile(ipConfig)) throw new IOException("Missing ip.conf: " + ipConfig);
        환경.put("IP_CONFIG", ipConfig.toString());
        if (Arrays.asList("run","desktop","test-system").contains(কাৰ্য্য) && !환경.containsKey("QEMU_AARCH64")) {
            Path এপ্প্_এপ্প্_ড্ৰৱাৰ = সম্পদ_মান.resolve("host/qemu"), 실행기표식 = সম্পদ_মান.resolve("host/.qemu-sha256");
            String এপ্প্_ড্ৰৱাৰ_হেচ = (String)বৈশিষ্ট্য.get("qemu_sha256");
            if (!Files.isRegularFile(এপ্প্_এপ্প্_ড্ৰৱাৰ) || !Files.isRegularFile(실행기표식) || !Files.readString(실행기표식).trim().equals(এপ্প্_ড্ৰৱাৰ_হেচ)) {
                Path এপ্প্_ড্ৰৱাৰ_অভিলেখাগাৰ = সম্পদ_মান.resolve("qemu-host.tar.gz"); if (!হেচ_ফাইল(এপ্প্_ড্ৰৱাৰ_অভিলেখাগাৰ).equals(এপ্প্_ড্ৰৱাৰ_হেচ)) throw new IOException("QEMU SHA-256 불일치");
                এক্সট্ৰেক্ট_কৰক(এপ্প্_ড্ৰৱাৰ_অভিলেখাগাৰ,সম্পদ_মান.resolve("host")); Files.writeString(실행기표식,এপ্প্_ড্ৰৱাৰ_হেচ + "\n");
            }
            환경.put("QEMU_AARCH64",এপ্প্_এপ্প্_ড্ৰৱাৰ.toString());
        }
        MessageDigest 계산 = MessageDigest.getInstance("SHA-256"); Collections.sort(소유파일들);
        for (String নাম : 소유파일들) { 계산.update(নাম.getBytes(StandardCharsets.UTF_8)); 계산.update(Files.readAllBytes(내부경로(উৎস_ট্ৰি,নাম))); }
        계산.update("ip.conf\0".getBytes(StandardCharsets.UTF_8)); 계산.update(Files.readAllBytes(ipConfig));
        String উৎস_হেচ = হেচ_পাঠ(계산.digest()); Path 빌드표식 = কাৰ্ণেল_মান.resolve("build/worldos-source.sha256");
        if (কাৰ্য্য.equals("build") || !Files.isRegularFile(빌드표식) || !Files.readString(빌드표식).trim().equals(উৎস_হেচ)) {
            호출(কাৰ্ণেল_মান,내부경로(কাৰ্ণেল_মান,(String)বৈশিষ্ট্য.get("builder")),Collections.emptyList(),환경);
            Files.writeString(빌드표식,উৎস_হেচ + "\n");
        }
        List<String> 추가인수 = new ArrayList<>(Arrays.asList(인수).subList(1,인수.length));
        if (কাৰ্য্য.equals("run") || কাৰ্য্য.equals("desktop")) {
            if (কাৰ্য্য.equals("desktop")) 추가인수.add(0,"--desktop");
            호출(কাৰ্ণেল_মান,내부경로(কাৰ্ণেল_মান,(String)বৈশিষ্ট্য.get("runner")),추가인수,환경);
        } else if (কাৰ্য্য.equals("image")) 호출(কাৰ্ণেল_মান,내부경로(কাৰ্ণেল_মান,(String)বৈশিষ্ট্য.get("image_builder")),추가인수,환경);
        else if (কাৰ্য্য.equals("test-system")) {
            추가인수.add(0,기준.toString()); 추가인수.add(0,"--edition");
            호출(কাৰ্ণেল_মান,내부경로(কাৰ্ণেল_মান,(String)বৈশিষ্ট্য.get("system_tester")),추가인수,환경);
        }
    }
}
