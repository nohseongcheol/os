// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.security.MessageDigest;
import java.util.*;

/** 독립 국가판의 의존성 검사·복원·গঠন_সিস্টেম·실행을 맡는 হোস্ট Java সরঞ্জামগুলি. */
public final class 국가실행기 {
    static final class ডাটা_পার্সার {
        final String উৎস_নথি; int অবস্থান;
        ডাটা_পার্সার(String পাঠ) { উৎস_নথি = পাঠ; }
        void 빈칸() { while (অবস্থান < উৎস_নথি.length() && Character.isWhitespace(উৎস_নথি.charAt(অবস্থান))) অবস্থান++; }
        Object পড়া() {
            빈칸(); char অক্ষর_মান = উৎস_নথি.charAt(অবস্থান++);
            if (অক্ষর_মান == '{') {
                Map<String,Object> পরিমাপ = new LinkedHashMap<>(); 빈칸();
                if (উৎস_নথি.charAt(অবস্থান) == '}') { অবস্থান++; return পরিমাপ; }
                while (true) {
                    String নাম = (String)পড়া(); 빈칸(); if (উৎস_নথি.charAt(অবস্থান++) != ':') throw new IllegalArgumentException("ডাটা সীমানির্ধারক_মান ত্রুটি");
                    পরিমাপ.put(নাম, পড়া()); 빈칸(); char সীমানির্ধারক_মান = উৎস_নথি.charAt(অবস্থান++);
                    if (সীমানির্ধারক_মান == '}') return পরিমাপ; if (সীমানির্ধারক_মান != ',') throw new IllegalArgumentException("ডাটা সীমানির্ধারক_মান ত্রুটি");
                }
            }
            if (অক্ষর_মান == '[') {
                List<Object> পরিমাপ = new ArrayList<>(); 빈칸();
                if (উৎস_নথি.charAt(অবস্থান) == ']') { অবস্থান++; return পরিমাপ; }
                while (true) {
                    পরিমাপ.add(পড়া()); 빈칸(); char সীমানির্ধারক_মান = উৎস_নথি.charAt(অবস্থান++);
                    if (সীমানির্ধারক_মান == ']') return পরিমাপ; if (সীমানির্ধারক_মান != ',') throw new IllegalArgumentException("ডাটা সীমানির্ধারক_মান ত্রুটি");
                }
            }
            if (অক্ষর_মান == '"') {
                StringBuilder পরিমাপ = new StringBuilder();
                while (true) {
                    char পরবর্তী_দফা = উৎস_নথি.charAt(অবস্থান++); if (পরবর্তী_দফা == '"') return পরিমাপ.toString();
                    if (পরবর্তী_দফা == '\\') {
                        পরবর্তী_দফা = উৎস_নথি.charAt(অবস্থান++);
                        if (পরবর্তী_দফা == 'u') { পরিমাপ.append((char)Integer.parseInt(উৎস_নথি.substring(অবস্থান, অবস্থান + 4),16)); অবস্থান += 4; continue; }
                        if (পরবর্তী_দফা == 'n') পরবর্তী_দফা = '\n'; else if (পরবর্তী_দফা == 'r') পরবর্তী_দফা = '\r'; else if (পরবর্তী_দফা == 't') পরবর্তী_দফা = '\t';
                        else if (পরবর্তী_দফা == 'b') পরবর্তী_দফা = '\b'; else if (পরবর্তী_দফা == 'f') পরবর্তী_দফা = '\f';
                        else if (পরবর্তী_দফা != '"' && পরবর্তী_দফা != '\\' && পরবর্তী_দফা != '/') throw new IllegalArgumentException("문자 이스케이프 ত্রুটি");
                    }
                    পরিমাপ.append(পরবর্তী_দফা);
                }
            }
            int চালনা = অবস্থান - 1;
            while (অবস্থান < উৎস_নথি.length() && ",]} \t\r\n".indexOf(উৎস_নথি.charAt(অবস্থান)) < 0) অবস্থান++;
            String মান = উৎস_নথি.substring(চালনা, অবস্থান);
            if (মান.equals("true")) return Boolean.TRUE; if (মান.equals("false")) return Boolean.FALSE; if (মান.equals("null")) return null;
            return Double.valueOf(মান);
        }
    }
    static String হ্যাশ_ফাইল(Path পথ_2) throws Exception {
        MessageDigest 계산 = MessageDigest.getInstance("SHA-256"); byte[] ডাটা = new byte[1024 * 1024];
        try (InputStream 입력 = Files.newInputStream(পথ_2)) { for (int দৈর্ঘ্য_মান; (দৈর্ঘ্য_মান = 입력.read(ডাটা)) >= 0;) 계산.update(ডাটা,0,দৈর্ঘ্য_মান); }
        return হ্যাশ_পাঠ(계산.digest());
    }
    static String হ্যাশ_পাঠ(byte[] ডাটা) {
        StringBuilder পাঠ = new StringBuilder(); for (byte মান : ডাটা) পাঠ.append(String.format(Locale.ROOT,"%02x",মান & 255)); return পাঠ.toString();
    }
    static Path 내부경로(Path প্রকল্প_মূল, String নাম) {
        Path পরিমাপ = প্রকল্প_মূল.resolve(নাম).normalize();
        if (নাম.isEmpty() || Paths.get(নাম).isAbsolute() || !পরিমাপ.startsWith(প্রকল্প_মূল) || নাম.indexOf('\\') >= 0)
            throw new IllegalArgumentException("범위를 벗어난 পথ_2: " + নাম);
        for (Path 부분 : Paths.get(নাম)) if (부분.toString().equals("..")) throw new IllegalArgumentException("상위 পথ_2 금지: " + নাম);
        for (Path 현재 = পরিমাপ; 현재 != null && 현재.startsWith(প্রকল্প_মূল); 현재 = 현재.getParent())
            if (Files.isSymbolicLink(현재)) throw new IllegalArgumentException("의존성 경로의 링크 금지: " + নাম);
        return পরিমাপ;
    }
    static String 명령출력(List<String> আদেশ) throws Exception {
        Process প্রসেসর_মান = new ProcessBuilder(আদেশ).redirectError(ProcessBuilder.Redirect.INHERIT).start();
        String পরিমাপ = new String(প্রসেসর_মান.getInputStream().readAllBytes(),StandardCharsets.UTF_8);
        if (প্রসেসর_মান.waitFor() != 0) throw new IOException("আদেশ বিফলতা_মান: " + আদেশ.get(0)); return পরিমাপ;
    }
    static void এক্সট্রাক্ট(Path সংগ্রহ_করা_মান, Path গন্তব্য_মান) throws Exception {
        for (String নাম : 명령출력(Arrays.asList("tar","-tzf",সংগ্রহ_করা_মান.toString())).split("\n")) 내부경로(গন্তব্য_মান, নাম);
        for (String নিবেশের_পঙ্_ক্তি : 명령출력(Arrays.asList("tar","-tvzf",সংগ্রহ_করা_মান.toString())).split("\n"))
            if (!নিবেশের_পঙ্_ক্তি.isEmpty() && নিবেশের_পঙ্_ক্তি.charAt(0) != '-' && নিবেশের_পঙ্_ক্তি.charAt(0) != 'd') throw new IOException("외부 링크 또는 특수 파일을 포함한 의존성");
        Files.createDirectories(গন্তব্য_মান);
        int অবস্হা_মান = new ProcessBuilder("tar","--no-same-owner","--no-same-permissions","-xzf",সংগ্রহ_করা_মান.toString(),"-C",গন্তব্য_মান.toString()).inheritIO().start().waitFor();
        if (অবস্হা_মান != 0) throw new IOException("의존성 সংগ্রহ_করা_মান রিলিজ_স্টোরেজ বিফলতা_মান");
    }
    static void 호출(Path 작업경로, Path সরঞ্জামগুলি, List<String> আর্গুমেন্ট_তালিকা, Map<String,String> 환경) throws Exception {
        List<String> আদেশ = new ArrayList<>(Arrays.asList("python3", সরঞ্জামগুলি.toString())); আদেশ.addAll(আর্গুমেন্ট_তালিকা);
        ProcessBuilder কার্যকর_করুন_আদেশ = new ProcessBuilder(আদেশ).directory(작업경로.toFile()).inheritIO(); কার্যকর_করুন_আদেশ.environment().putAll(환경);
        int অবস্হা_মান = কার্যকর_করুন_আদেশ.start().waitFor(); if (অবস্হা_মান != 0) throw new IOException("সরঞ্জামগুলি বিফলতা_মান: " + সরঞ্জামগুলি + " (" + অবস্হা_মান + ")");
    }
    @SuppressWarnings("unchecked")
    public static void main(String[] আর্গুমেন্ট_তালিকা) throws Exception {
        if (আর্গুমেন্ট_তালিকা.length < 1) throw new IllegalArgumentException("build, run, desktop, image, check, test-system 중 동작을 지정하세요");
        String কাজ = আর্গুমেন্ট_তালিকা[0];
        if (!Arrays.asList("build","run","desktop","image","check","test-system").contains(কাজ)) throw new IllegalArgumentException("알 수 없는 কাজ");
        Path প্রকল্প_মূল = Paths.get(System.getProperty("worldos.edition.root")).toAbsolutePath().normalize();
        Map<String,Object> সেটিংস = (Map<String,Object>)new ডাটা_পার্সার(Files.readString(প্রকল্প_মূল.resolve("native.json"),StandardCharsets.UTF_8)).পড়া();
        Path উত্স_ট্রী = 내부경로(প্রকল্প_মূল,(String)সেটিংস.get("source")), কারনেল_মান = 내부경로(উত্স_ট্রী,(String)সেটিংস.get("native"));
        List<String> 소유파일들 = (List<String>)(List<?>)সেটিংস.get("owned_files");
        for (String নাম : 소유파일들) if (!Files.isRegularFile(내부경로(উত্স_ট্রী,নাম))) throw new IOException("উত্স_ট্রী 없음: " + নাম);
        if (কাজ.equals("check")) { System.out.println(সেটিংস.get("country") + " " + সেটিংস.get("language") + " 독립 উত্স_ট্রী যাচাই_করা 완료"); return; }
        String 자원상대 = (String)সেটিংস.getOrDefault("resource_root", ".");
        if (!자원상대.equals(".") && !자원상대.equals("..")) throw new IllegalArgumentException("의존성 প্রকল্প_মূল পথ_2 ত্রুটি");
        Path রিসোর্স_মান = প্রকল্প_মূল.resolve(자원상대).normalize(); Path সংগ্রহ_করা_মান = রিসোর্স_মান.resolve("native-vendor.tar.gz");
        String 기대해시 = (String)সেটিংস.get("vendor_sha256");
        if (!হ্যাশ_ফাইল(সংগ্রহ_করা_মান).equals(기대해시)) throw new IOException("의존성 SHA-256 불일치");
        Path 표식 = উত্স_ট্রী.resolve(".vendor-sha256");
        if (!Files.isRegularFile(표식) || !Files.readString(표식).trim().equals(기대해시)) { এক্সট্রাক্ট(সংগ্রহ_করা_মান, উত্স_ট্রী); Files.writeString(표식,기대해시 + "\n"); }
        Map<String,String> 환경 = new HashMap<>(System.getenv());
        Path ipConfig = null;
        if (환경.containsKey("IP_CONFIG")) ipConfig = Paths.get(환경.get("IP_CONFIG")).toAbsolutePath().normalize();
        else for (Path parent = প্রকল্প_মূল; parent != null; parent = parent.getParent()) {
            if (Files.isRegularFile(parent.resolve("ip.conf"))) { ipConfig = parent.resolve("ip.conf"); break; }
        }
        if (ipConfig == null) ipConfig = উত্স_ট্রী.resolve("ip.conf");
        if (!Files.isRegularFile(ipConfig)) throw new IOException("Missing ip.conf: " + ipConfig);
        환경.put("IP_CONFIG", ipConfig.toString());
        if (Arrays.asList("run","desktop","test-system").contains(কাজ) && !환경.containsKey("QEMU_AARCH64")) {
            Path অ্যাপ_অ্যাপ_লঞ্চার = রিসোর্স_মান.resolve("host/qemu"), 실행기표식 = রিসোর্স_মান.resolve("host/.qemu-sha256");
            String অ্যাপ_লঞ্চার_হ্যাশ = (String)সেটিংস.get("qemu_sha256");
            if (!Files.isRegularFile(অ্যাপ_অ্যাপ_লঞ্চার) || !Files.isRegularFile(실행기표식) || !Files.readString(실행기표식).trim().equals(অ্যাপ_লঞ্চার_হ্যাশ)) {
                Path অ্যাপ_লঞ্চার_সংগ্রহ_করা = রিসোর্স_মান.resolve("qemu-host.tar.gz"); if (!হ্যাশ_ফাইল(অ্যাপ_লঞ্চার_সংগ্রহ_করা).equals(অ্যাপ_লঞ্চার_হ্যাশ)) throw new IOException("QEMU SHA-256 불일치");
                এক্সট্রাক্ট(অ্যাপ_লঞ্চার_সংগ্রহ_করা,রিসোর্স_মান.resolve("host")); Files.writeString(실행기표식,অ্যাপ_লঞ্চার_হ্যাশ + "\n");
            }
            환경.put("QEMU_AARCH64",অ্যাপ_অ্যাপ_লঞ্চার.toString());
        }
        MessageDigest 계산 = MessageDigest.getInstance("SHA-256"); Collections.sort(소유파일들);
        for (String নাম : 소유파일들) { 계산.update(নাম.getBytes(StandardCharsets.UTF_8)); 계산.update(Files.readAllBytes(내부경로(উত্স_ট্রী,নাম))); }
        계산.update("ip.conf\0".getBytes(StandardCharsets.UTF_8)); 계산.update(Files.readAllBytes(ipConfig));
        String উত্স_হ্যাশ = হ্যাশ_পাঠ(계산.digest()); Path 빌드표식 = কারনেল_মান.resolve("build/worldos-source.sha256");
        if (কাজ.equals("build") || !Files.isRegularFile(빌드표식) || !Files.readString(빌드표식).trim().equals(উত্স_হ্যাশ)) {
            호출(কারনেল_মান,내부경로(কারনেল_মান,(String)সেটিংস.get("builder")),Collections.emptyList(),환경);
            Files.writeString(빌드표식,উত্স_হ্যাশ + "\n");
        }
        List<String> 추가인수 = new ArrayList<>(Arrays.asList(আর্গুমেন্ট_তালিকা).subList(1,আর্গুমেন্ট_তালিকা.length));
        if (কাজ.equals("run") || কাজ.equals("desktop")) {
            if (কাজ.equals("desktop")) 추가인수.add(0,"--desktop");
            호출(কারনেল_মান,내부경로(কারনেল_মান,(String)সেটিংস.get("runner")),추가인수,환경);
        } else if (কাজ.equals("image")) 호출(কারনেল_মান,내부경로(কারনেল_মান,(String)সেটিংস.get("image_builder")),추가인수,환경);
        else if (কাজ.equals("test-system")) {
            추가인수.add(0,প্রকল্প_মূল.toString()); 추가인수.add(0,"--edition");
            호출(কারনেল_মান,내부경로(কারনেল_মান,(String)সেটিংস.get("system_tester")),추가인수,환경);
        }
    }
}
