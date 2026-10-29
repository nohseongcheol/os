// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.security.MessageDigest;
import java.util.*;

/** 독립 국가판의 의존성 검사·복원·دروستکراو_سیستم·실행을 맡는 جێدەر Java ئامرازەکان. */
public final class 국가실행기 {
    static final class 자료해석기 {
        final String ژێدەر; int 위치;
        자료해석기(String دەق) { ژێدەر = دەق; }
        void 빈칸() { while (위치 < ژێدەر.length() && Character.isWhitespace(ژێدەر.charAt(위치))) 위치++; }
        Object 읽기() {
            빈칸(); char نووسە_نرخ = ژێدەر.charAt(위치++);
            if (نووسە_نرخ == '{') {
                Map<String,Object> 결과 = new LinkedHashMap<>(); 빈칸();
                if (ژێدەر.charAt(위치) == '}') { 위치++; return 결과; }
                while (true) {
                    String ناو = (String)읽기(); 빈칸(); if (ژێدەر.charAt(위치++) != ':') throw new IllegalArgumentException("دەیتا دێلیمیتەر_نرخ هەڵە");
                    결과.put(ناو, 읽기()); 빈칸(); char دێلیمیتەر_نرخ = ژێدەر.charAt(위치++);
                    if (دێلیمیتەر_نرخ == '}') return 결과; if (دێلیمیتەر_نرخ != ',') throw new IllegalArgumentException("دەیتا دێلیمیتەر_نرخ هەڵە");
                }
            }
            if (نووسە_نرخ == '[') {
                List<Object> 결과 = new ArrayList<>(); 빈칸();
                if (ژێدەر.charAt(위치) == ']') { 위치++; return 결과; }
                while (true) {
                    결과.add(읽기()); 빈칸(); char دێلیمیتەر_نرخ = ژێدەر.charAt(위치++);
                    if (دێلیمیتەر_نرخ == ']') return 결과; if (دێلیمیتەر_نرخ != ',') throw new IllegalArgumentException("دەیتا دێلیمیتەر_نرخ هەڵە");
                }
            }
            if (نووسە_نرخ == '"') {
                StringBuilder 결과 = new StringBuilder();
                while (true) {
                    char 다음 = ژێدەر.charAt(위치++); if (다음 == '"') return 결과.toString();
                    if (다음 == '\\') {
                        다음 = ژێدەر.charAt(위치++);
                        if (다음 == 'u') { 결과.append((char)Integer.parseInt(ژێدەر.substring(위치, 위치 + 4),16)); 위치 += 4; continue; }
                        if (다음 == 'n') 다음 = '\n'; else if (다음 == 'r') 다음 = '\r'; else if (다음 == 't') 다음 = '\t';
                        else if (다음 == 'b') 다음 = '\b'; else if (다음 == 'f') 다음 = '\f';
                        else if (다음 != '"' && 다음 != '\\' && 다음 != '/') throw new IllegalArgumentException("문자 이스케이프 هەڵە");
                    }
                    결과.append(다음);
                }
            }
            int ڕادان = 위치 - 1;
            while (위치 < ژێدەر.length() && ",]} \t\r\n".indexOf(ژێدەر.charAt(위치)) < 0) 위치++;
            String نرخ = ژێدەر.substring(ڕادان, 위치);
            if (نرخ.equals("true")) return Boolean.TRUE; if (نرخ.equals("false")) return Boolean.FALSE; if (نرخ.equals("null")) return null;
            return Double.valueOf(نرخ);
        }
    }
    static String دەرەنجام_فایل(Path گوزەر) throws Exception {
        MessageDigest 계산 = MessageDigest.getInstance("SHA-256"); byte[] دەیتا = new byte[1024 * 1024];
        try (InputStream 입력 = Files.newInputStream(گوزەر)) { for (int درێژی_نرخ; (درێژی_نرخ = 입력.read(دەیتا)) >= 0;) 계산.update(دەیتا,0,درێژی_نرخ); }
        return دەرەنجام_دەق(계산.digest());
    }
    static String دەرەنجام_دەق(byte[] دەیتا) {
        StringBuilder دەق = new StringBuilder(); for (byte نرخ : دەیتا) دەق.append(String.format(Locale.ROOT,"%02x",نرخ & 255)); return دەق.toString();
    }
    static Path 내부경로(Path 기준, String ناو) {
        Path 결과 = 기준.resolve(ناو).normalize();
        if (ناو.isEmpty() || Paths.get(ناو).isAbsolute() || !결과.startsWith(기준) || ناو.indexOf('\\') >= 0)
            throw new IllegalArgumentException("범위를 벗어난 گوزەر: " + ناو);
        for (Path 부분 : Paths.get(ناو)) if (부분.toString().equals("..")) throw new IllegalArgumentException("상위 گوزەر 금지: " + ناو);
        for (Path 현재 = 결과; 현재 != null && 현재.startsWith(기준); 현재 = 현재.getParent())
            if (Files.isSymbolicLink(현재)) throw new IllegalArgumentException("의존성 경로의 링크 금지: " + ناو);
        return 결과;
    }
    static String 명령출력(List<String> فەرمان) throws Exception {
        Process پرۆسە_نرخ = new ProcessBuilder(فەرمان).redirectError(ProcessBuilder.Redirect.INHERIT).start();
        String 결과 = new String(پرۆسە_نرخ.getInputStream().readAllBytes(),StandardCharsets.UTF_8);
        if (پرۆسە_نرخ.waitFor() != 0) throw new IOException("فەرمان شکستهێنان_نرخ: " + فەرمان.get(0)); return 결과;
    }
    static void دەرهێنان(Path ئەرشیف_نرخ, Path جێمەبەست_نرخ) throws Exception {
        for (String ناو : 명령출력(Arrays.asList("tar","-tzf",ئەرشیف_نرخ.toString())).split("\n")) 내부경로(جێمەبەست_نرخ, ناو);
        for (String دێڕ : 명령출력(Arrays.asList("tar","-tvzf",ئەرشیف_نرخ.toString())).split("\n"))
            if (!دێڕ.isEmpty() && دێڕ.charAt(0) != '-' && دێڕ.charAt(0) != 'd') throw new IOException("외부 링크 또는 특수 파일을 포함한 의존성");
        Files.createDirectories(جێمەبەست_نرخ);
        int دۆخ_نرخ = new ProcessBuilder("tar","--no-same-owner","--no-same-permissions","-xzf",ئەرشیف_نرخ.toString(),"-C",جێمەبەست_نرخ.toString()).inheritIO().start().waitFor();
        if (دۆخ_نرخ != 0) throw new IOException("의존성 ئەرشیف_نرخ وەشان_هەمارگە شکستهێنان_نرخ");
    }
    static void 호출(Path 작업경로, Path ئامرازەکان, List<String> 인수, Map<String,String> 환경) throws Exception {
        List<String> فەرمان = new ArrayList<>(Arrays.asList("python3", ئامرازەکان.toString())); فەرمان.addAll(인수);
        ProcessBuilder جێبەجێکردن_فەرمان = new ProcessBuilder(فەرمان).directory(작업경로.toFile()).inheritIO(); جێبەجێکردن_فەرمان.environment().putAll(환경);
        int دۆخ_نرخ = جێبەجێکردن_فەرمان.start().waitFor(); if (دۆخ_نرخ != 0) throw new IOException("ئامرازەکان شکستهێنان_نرخ: " + ئامرازەکان + " (" + دۆخ_نرخ + ")");
    }
    @SuppressWarnings("unchecked")
    public static void main(String[] 인수) throws Exception {
        if (인수.length < 1) throw new IllegalArgumentException("build, run, desktop, image, check, test-system 중 동작을 지정하세요");
        String ئاکشن = 인수[0];
        if (!Arrays.asList("build","run","desktop","image","check","test-system").contains(ئاکشن)) throw new IllegalArgumentException("알 수 없는 ئاکشن");
        Path 기준 = Paths.get(System.getProperty("worldos.edition.root")).toAbsolutePath().normalize();
        Map<String,Object> ڕێكبەندەكان = (Map<String,Object>)new 자료해석기(Files.readString(기준.resolve("native.json"),StandardCharsets.UTF_8)).읽기();
        Path ژێدەر_دار = 내부경로(기준,(String)ڕێكبەندەكان.get("source")), کوورەک_نرخ = 내부경로(ژێدەر_دار,(String)ڕێكبەندەكان.get("native"));
        List<String> 소유파일들 = (List<String>)(List<?>)ڕێكبەندەكان.get("owned_files");
        for (String ناو : 소유파일들) if (!Files.isRegularFile(내부경로(ژێدەر_دار,ناو))) throw new IOException("ژێدەر_دار 없음: " + ناو);
        if (ئاکشن.equals("check")) { System.out.println(ڕێكبەندەكان.get("country") + " " + ڕێكبەندەكان.get("language") + " 독립 ژێدەر_دار سەلماندن 완료"); return; }
        String 자원상대 = (String)ڕێكبەندەكان.getOrDefault("resource_root", ".");
        if (!자원상대.equals(".") && !자원상대.equals("..")) throw new IllegalArgumentException("의존성 기준 گوزەر هەڵە");
        Path ژێدەر_نرخ = 기준.resolve(자원상대).normalize(); Path ئەرشیف_نرخ = ژێدەر_نرخ.resolve("native-vendor.tar.gz");
        String 기대해시 = (String)ڕێكبەندەكان.get("vendor_sha256");
        if (!دەرەنجام_فایل(ئەرشیف_نرخ).equals(기대해시)) throw new IOException("의존성 SHA-256 불일치");
        Path 표식 = ژێدەر_دار.resolve(".vendor-sha256");
        if (!Files.isRegularFile(표식) || !Files.readString(표식).trim().equals(기대해시)) { دەرهێنان(ئەرشیف_نرخ, ژێدەر_دار); Files.writeString(표식,기대해시 + "\n"); }
        Map<String,String> 환경 = new HashMap<>(System.getenv());
        Path ipConfig = null;
        if (환경.containsKey("IP_CONFIG")) ipConfig = Paths.get(환경.get("IP_CONFIG")).toAbsolutePath().normalize();
        else for (Path parent = 기준; parent != null; parent = parent.getParent()) {
            if (Files.isRegularFile(parent.resolve("ip.conf"))) { ipConfig = parent.resolve("ip.conf"); break; }
        }
        if (ipConfig == null) ipConfig = ژێدەر_دار.resolve("ip.conf");
        if (!Files.isRegularFile(ipConfig)) throw new IOException("Missing ip.conf: " + ipConfig);
        환경.put("IP_CONFIG", ipConfig.toString());
        if (Arrays.asList("run","desktop","test-system").contains(ئاکشن) && !환경.containsKey("QEMU_AARCH64")) {
            Path بەرنامە_ئەندامی_ستاف = ژێدەر_نرخ.resolve("host/qemu"), 실행기표식 = ژێدەر_نرخ.resolve("host/.qemu-sha256");
            String ئەندامی_ستاف_دەرەنجام = (String)ڕێكبەندەكان.get("qemu_sha256");
            if (!Files.isRegularFile(بەرنامە_ئەندامی_ستاف) || !Files.isRegularFile(실행기표식) || !Files.readString(실행기표식).trim().equals(ئەندامی_ستاف_دەرەنجام)) {
                Path ئەندامی_ستاف_ئەرشیف = ژێدەر_نرخ.resolve("qemu-host.tar.gz"); if (!دەرەنجام_فایل(ئەندامی_ستاف_ئەرشیف).equals(ئەندامی_ستاف_دەرەنجام)) throw new IOException("QEMU SHA-256 불일치");
                دەرهێنان(ئەندامی_ستاف_ئەرشیف,ژێدەر_نرخ.resolve("host")); Files.writeString(실행기표식,ئەندامی_ستاف_دەرەنجام + "\n");
            }
            환경.put("QEMU_AARCH64",بەرنامە_ئەندامی_ستاف.toString());
        }
        MessageDigest 계산 = MessageDigest.getInstance("SHA-256"); Collections.sort(소유파일들);
        for (String ناو : 소유파일들) { 계산.update(ناو.getBytes(StandardCharsets.UTF_8)); 계산.update(Files.readAllBytes(내부경로(ژێدەر_دار,ناو))); }
        계산.update("ip.conf\0".getBytes(StandardCharsets.UTF_8)); 계산.update(Files.readAllBytes(ipConfig));
        String ژێدەر_دەرەنجام = دەرەنجام_دەق(계산.digest()); Path 빌드표식 = کوورەک_نرخ.resolve("build/worldos-source.sha256");
        if (ئاکشن.equals("build") || !Files.isRegularFile(빌드표식) || !Files.readString(빌드표식).trim().equals(ژێدەر_دەرەنجام)) {
            호출(کوورەک_نرخ,내부경로(کوورەک_نرخ,(String)ڕێكبەندەكان.get("builder")),Collections.emptyList(),환경);
            Files.writeString(빌드표식,ژێدەر_دەرەنجام + "\n");
        }
        List<String> 추가인수 = new ArrayList<>(Arrays.asList(인수).subList(1,인수.length));
        if (ئاکشن.equals("run") || ئاکشن.equals("desktop")) {
            if (ئاکشن.equals("desktop")) 추가인수.add(0,"--desktop");
            호출(کوورەک_نرخ,내부경로(کوورەک_نرخ,(String)ڕێكبەندەكان.get("runner")),추가인수,환경);
        } else if (ئاکشن.equals("image")) 호출(کوورەک_نرخ,내부경로(کوورەک_نرخ,(String)ڕێكبەندەكان.get("image_builder")),추가인수,환경);
        else if (ئاکشن.equals("test-system")) {
            추가인수.add(0,기준.toString()); 추가인수.add(0,"--edition");
            호출(کوورەک_نرخ,내부경로(کوورەک_نرخ,(String)ڕێكبەندەكان.get("system_tester")),추가인수,환경);
        }
    }
}
