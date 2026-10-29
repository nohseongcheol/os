// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.security.MessageDigest;
import java.util.*;

/** 독립 국가판의 의존성 검사·복원·ចងក្រង_ប្រព័ន្ធ·실행을 맡는 ហូស Java ឧបករណ៍. */
public final class 국가실행기 {
    static final class ទិន្នន័យ_មុខងារ_ញែក {
        final String ប្រភព; int កំណត់ទីតាំង;
        ទិន្នន័យ_មុខងារ_ញែក(String អត្ថបទ) { ប្រភព = អត្ថបទ; }
        void 빈칸() { while (កំណត់ទីតាំង < ប្រភព.length() && Character.isWhitespace(ប្រភព.charAt(កំណត់ទីតាំង))) កំណត់ទីតាំង++; }
        Object អាន() {
            빈칸(); char តួអក្សរ_តំលៃ = ប្រភព.charAt(កំណត់ទីតាំង++);
            if (តួអក្សរ_តំលៃ == '{') {
                Map<String,Object> ការវាស់វែង = new LinkedHashMap<>(); 빈칸();
                if (ប្រភព.charAt(កំណត់ទីតាំង) == '}') { កំណត់ទីតាំង++; return ការវាស់វែង; }
                while (true) {
                    String ឈ្មោះ = (String)អាន(); 빈칸(); if (ប្រភព.charAt(កំណត់ទីតាំង++) != ':') throw new IllegalArgumentException("ទិន្នន័យ សញ្ញាកំណត់ប្លុក_តំលៃ កំហុស");
                    ការវាស់វែង.put(ឈ្មោះ, អាន()); 빈칸(); char សញ្ញាកំណត់ប្លុក_តំលៃ = ប្រភព.charAt(កំណត់ទីតាំង++);
                    if (សញ្ញាកំណត់ប្លុក_តំលៃ == '}') return ការវាស់វែង; if (សញ្ញាកំណត់ប្លុក_តំលៃ != ',') throw new IllegalArgumentException("ទិន្នន័យ សញ្ញាកំណត់ប្លុក_តំលៃ កំហុស");
                }
            }
            if (តួអក្សរ_តំលៃ == '[') {
                List<Object> ការវាស់វែង = new ArrayList<>(); 빈칸();
                if (ប្រភព.charAt(កំណត់ទីតាំង) == ']') { កំណត់ទីតាំង++; return ការវាស់វែង; }
                while (true) {
                    ការវាស់វែង.add(អាន()); 빈칸(); char សញ្ញាកំណត់ប្លុក_តំលៃ = ប្រភព.charAt(កំណត់ទីតាំង++);
                    if (សញ្ញាកំណត់ប្លុក_តំលៃ == ']') return ការវាស់វែង; if (សញ្ញាកំណត់ប្លុក_តំលៃ != ',') throw new IllegalArgumentException("ទិន្នន័យ សញ្ញាកំណត់ប្លុក_តំលៃ កំហុស");
                }
            }
            if (តួអក្សរ_តំលៃ == '"') {
                StringBuilder ការវាស់វែង = new StringBuilder();
                while (true) {
                    char បន្ទាប់_ធាតុ = ប្រភព.charAt(កំណត់ទីតាំង++); if (បន្ទាប់_ធាតុ == '"') return ការវាស់វែង.toString();
                    if (បន្ទាប់_ធាតុ == '\\') {
                        បន្ទាប់_ធាតុ = ប្រភព.charAt(កំណត់ទីតាំង++);
                        if (បន្ទាប់_ធាតុ == 'u') { ការវាស់វែង.append((char)Integer.parseInt(ប្រភព.substring(កំណត់ទីតាំង, កំណត់ទីតាំង + 4),16)); កំណត់ទីតាំង += 4; continue; }
                        if (បន្ទាប់_ធាតុ == 'n') បន្ទាប់_ធាតុ = '\n'; else if (បន្ទាប់_ធាតុ == 'r') បន្ទាប់_ធាតុ = '\r'; else if (បន្ទាប់_ធាតុ == 't') បន្ទាប់_ធាតុ = '\t';
                        else if (បន្ទាប់_ធាតុ == 'b') បន្ទាប់_ធាតុ = '\b'; else if (បន្ទាប់_ធាតុ == 'f') បន្ទាប់_ធាតុ = '\f';
                        else if (បន្ទាប់_ធាតុ != '"' && បន្ទាប់_ធាតុ != '\\' && បន្ទាប់_ធាតុ != '/') throw new IllegalArgumentException("문자 이스케이프 កំហុស");
                    }
                    ការវាស់វែង.append(បន្ទាប់_ធាតុ);
                }
            }
            int រត់ = កំណត់ទីតាំង - 1;
            while (កំណត់ទីតាំង < ប្រភព.length() && ",]} \t\r\n".indexOf(ប្រភព.charAt(កំណត់ទីតាំង)) < 0) កំណត់ទីតាំង++;
            String តំលៃ = ប្រភព.substring(រត់, កំណត់ទីតាំង);
            if (តំលៃ.equals("true")) return Boolean.TRUE; if (តំលៃ.equals("false")) return Boolean.FALSE; if (តំលៃ.equals("null")) return null;
            return Double.valueOf(តំលៃ);
        }
    }
    static String ហាស_ឯកសារ(Path ផ្លូវ) throws Exception {
        MessageDigest 계산 = MessageDigest.getInstance("SHA-256"); byte[] ទិន្នន័យ = new byte[1024 * 1024];
        try (InputStream 입력 = Files.newInputStream(ផ្លូវ)) { for (int ប្រវែង_តំលៃ; (ប្រវែង_តំលៃ = 입력.read(ទិន្នន័យ)) >= 0;) 계산.update(ទិន្នន័យ,0,ប្រវែង_តំលៃ); }
        return ហាស_អត្ថបទ(계산.digest());
    }
    static String ហាស_អត្ថបទ(byte[] ទិន្នន័យ) {
        StringBuilder អត្ថបទ = new StringBuilder(); for (byte តំលៃ : ទិន្នន័យ) អត្ថបទ.append(String.format(Locale.ROOT,"%02x",តំលៃ & 255)); return អត្ថបទ.toString();
    }
    static Path 내부경로(Path បញ្ចាំង_ឬស, String ឈ្មោះ) {
        Path ការវាស់វែង = បញ្ចាំង_ឬស.resolve(ឈ្មោះ).normalize();
        if (ឈ្មោះ.isEmpty() || Paths.get(ឈ្មោះ).isAbsolute() || !ការវាស់វែង.startsWith(បញ្ចាំង_ឬស) || ឈ្មោះ.indexOf('\\') >= 0)
            throw new IllegalArgumentException("범위를 벗어난 ផ្លូវ: " + ឈ្មោះ);
        for (Path 부분 : Paths.get(ឈ្មោះ)) if (부분.toString().equals("..")) throw new IllegalArgumentException("상위 ផ្លូវ 금지: " + ឈ្មោះ);
        for (Path 현재 = ការវាស់វែង; 현재 != null && 현재.startsWith(បញ្ចាំង_ឬស); 현재 = 현재.getParent())
            if (Files.isSymbolicLink(현재)) throw new IllegalArgumentException("의존성 경로의 링크 금지: " + ឈ្មោះ);
        return ការវាស់វែង;
    }
    static String 명령출력(List<String> ពាក្យ_បញ្ជា) throws Exception {
        Process ដំណើរការ_តំលៃ = new ProcessBuilder(ពាក្យ_បញ្ជា).redirectError(ProcessBuilder.Redirect.INHERIT).start();
        String ការវាស់វែង = new String(ដំណើរការ_តំលៃ.getInputStream().readAllBytes(),StandardCharsets.UTF_8);
        if (ដំណើរការ_តំលៃ.waitFor() != 0) throw new IOException("ពាក្យ_បញ្ជា បរាជ័យ_តំលៃ: " + ពាក្យ_បញ្ជា.get(0)); return ការវាស់វែង;
    }
    static void ទាញចេញ(Path ប័ណ្ណសារ_តំលៃ, Path ទិសដៅ_តំលៃ) throws Exception {
        for (String ឈ្មោះ : 명령출력(Arrays.asList("tar","-tzf",ប័ណ្ណសារ_តំលៃ.toString())).split("\n")) 내부경로(ទិសដៅ_តំលៃ, ឈ្មោះ);
        for (String បន្ទាត់ : 명령출력(Arrays.asList("tar","-tvzf",ប័ណ្ណសារ_តំលៃ.toString())).split("\n"))
            if (!បន្ទាត់.isEmpty() && បន្ទាត់.charAt(0) != '-' && បន្ទាត់.charAt(0) != 'd') throw new IOException("외부 링크 또는 특수 파일을 포함한 의존성");
        Files.createDirectories(ទិសដៅ_តំលៃ);
        int ភាព_តំលៃ = new ProcessBuilder("tar","--no-same-owner","--no-same-permissions","-xzf",ប័ណ្ណសារ_តំលៃ.toString(),"-C",ទិសដៅ_តំលៃ.toString()).inheritIO().start().waitFor();
        if (ភាព_តំលៃ != 0) throw new IOException("의존성 ប័ណ្ណសារ_តំលៃ លែង_ការផ្ទុក បរាជ័យ_តំលៃ");
    }
    static void 호출(Path 작업경로, Path ឧបករណ៍, List<String> អាគុយម៉ង់, Map<String,String> 환경) throws Exception {
        List<String> ពាក្យ_បញ្ជា = new ArrayList<>(Arrays.asList("python3", ឧបករណ៍.toString())); ពាក្យ_បញ្ជា.addAll(អាគុយម៉ង់);
        ProcessBuilder អនុវត្ត_ពាក្យបញ្ជា = new ProcessBuilder(ពាក្យ_បញ្ជា).directory(작업경로.toFile()).inheritIO(); អនុវត្ត_ពាក្យបញ្ជា.environment().putAll(환경);
        int ភាព_តំលៃ = អនុវត្ត_ពាក្យបញ្ជា.start().waitFor(); if (ភាព_តំលៃ != 0) throw new IOException("ឧបករណ៍ បរាជ័យ_តំលៃ: " + ឧបករណ៍ + " (" + ភាព_តំលៃ + ")");
    }
    @SuppressWarnings("unchecked")
    public static void main(String[] អាគុយម៉ង់) throws Exception {
        if (អាគុយម៉ង់.length < 1) throw new IllegalArgumentException("build, run, desktop, image, check, test-system 중 동작을 지정하세요");
        String អំពើ = អាគុយម៉ង់[0];
        if (!Arrays.asList("build","run","desktop","image","check","test-system").contains(អំពើ)) throw new IllegalArgumentException("알 수 없는 អំពើ");
        Path បញ្ចាំង_ឬស = Paths.get(System.getProperty("worldos.edition.root")).toAbsolutePath().normalize();
        Map<String,Object> ការកំណត់ = (Map<String,Object>)new ទិន្នន័យ_មុខងារ_ញែក(Files.readString(បញ្ចាំង_ឬស.resolve("native.json"),StandardCharsets.UTF_8)).អាន();
        Path ប្រភព_មែកធាង = 내부경로(បញ្ចាំង_ឬស,(String)ការកំណត់.get("source")), ខឺណេល_តំលៃ = 내부경로(ប្រភព_មែកធាង,(String)ការកំណត់.get("native"));
        List<String> 소유파일들 = (List<String>)(List<?>)ការកំណត់.get("owned_files");
        for (String ឈ្មោះ : 소유파일들) if (!Files.isRegularFile(내부경로(ប្រភព_មែកធាង,ឈ្មោះ))) throw new IOException("ប្រភព_មែកធាង 없음: " + ឈ្មោះ);
        if (អំពើ.equals("check")) { System.out.println(ការកំណត់.get("country") + " " + ការកំណត់.get("language") + " 독립 ប្រភព_មែកធាង ផ្ទៀងផ្ទាត់ 완료"); return; }
        String 자원상대 = (String)ការកំណត់.getOrDefault("resource_root", ".");
        if (!자원상대.equals(".") && !자원상대.equals("..")) throw new IllegalArgumentException("의존성 បញ្ចាំង_ឬស ផ្លូវ កំហុស");
        Path ធនធាន_តំលៃ = បញ្ចាំង_ឬស.resolve(자원상대).normalize(); Path ប័ណ្ណសារ_តំលៃ = ធនធាន_តំលៃ.resolve("native-vendor.tar.gz");
        String 기대해시 = (String)ការកំណត់.get("vendor_sha256");
        if (!ហាស_ឯកសារ(ប័ណ្ណសារ_តំលៃ).equals(기대해시)) throw new IOException("의존성 SHA-256 불일치");
        Path 표식 = ប្រភព_មែកធាង.resolve(".vendor-sha256");
        if (!Files.isRegularFile(표식) || !Files.readString(표식).trim().equals(기대해시)) { ទាញចេញ(ប័ណ្ណសារ_តំលៃ, ប្រភព_មែកធាង); Files.writeString(표식,기대해시 + "\n"); }
        Map<String,String> 환경 = new HashMap<>(System.getenv());
        Path ipConfig = null;
        if (환경.containsKey("IP_CONFIG")) ipConfig = Paths.get(환경.get("IP_CONFIG")).toAbsolutePath().normalize();
        else for (Path parent = បញ្ចាំង_ឬស; parent != null; parent = parent.getParent()) {
            if (Files.isRegularFile(parent.resolve("ip.conf"))) { ipConfig = parent.resolve("ip.conf"); break; }
        }
        if (ipConfig == null) ipConfig = ប្រភព_មែកធាង.resolve("ip.conf");
        if (!Files.isRegularFile(ipConfig)) throw new IOException("Missing ip.conf: " + ipConfig);
        환경.put("IP_CONFIG", ipConfig.toString());
        if (Arrays.asList("run","desktop","test-system").contains(អំពើ) && !환경.containsKey("QEMU_AARCH64")) {
            Path កម្មវិធី_ថត_កម្មវិធី = ធនធាន_តំលៃ.resolve("host/qemu"), 실행기표식 = ធនធាន_តំលៃ.resolve("host/.qemu-sha256");
            String ថត_កម្មវិធី_ហាស = (String)ការកំណត់.get("qemu_sha256");
            if (!Files.isRegularFile(កម្មវិធី_ថត_កម្មវិធី) || !Files.isRegularFile(실행기표식) || !Files.readString(실행기표식).trim().equals(ថត_កម្មវិធី_ហាស)) {
                Path ថត_កម្មវិធី_ប័ណ្ណសារ = ធនធាន_តំលៃ.resolve("qemu-host.tar.gz"); if (!ហាស_ឯកសារ(ថត_កម្មវិធី_ប័ណ្ណសារ).equals(ថត_កម្មវិធី_ហាស)) throw new IOException("QEMU SHA-256 불일치");
                ទាញចេញ(ថត_កម្មវិធី_ប័ណ្ណសារ,ធនធាន_តំលៃ.resolve("host")); Files.writeString(실행기표식,ថត_កម្មវិធី_ហាស + "\n");
            }
            환경.put("QEMU_AARCH64",កម្មវិធី_ថត_កម្មវិធី.toString());
        }
        MessageDigest 계산 = MessageDigest.getInstance("SHA-256"); Collections.sort(소유파일들);
        for (String ឈ្មោះ : 소유파일들) { 계산.update(ឈ្មោះ.getBytes(StandardCharsets.UTF_8)); 계산.update(Files.readAllBytes(내부경로(ប្រភព_មែកធាង,ឈ្មោះ))); }
        계산.update("ip.conf\0".getBytes(StandardCharsets.UTF_8)); 계산.update(Files.readAllBytes(ipConfig));
        String ប្រភព_ហាស = ហាស_អត្ថបទ(계산.digest()); Path 빌드표식 = ខឺណេល_តំលៃ.resolve("build/worldos-source.sha256");
        if (អំពើ.equals("build") || !Files.isRegularFile(빌드표식) || !Files.readString(빌드표식).trim().equals(ប្រភព_ហាស)) {
            호출(ខឺណេល_តំលៃ,내부경로(ខឺណេល_តំលៃ,(String)ការកំណត់.get("builder")),Collections.emptyList(),환경);
            Files.writeString(빌드표식,ប្រភព_ហាស + "\n");
        }
        List<String> 추가인수 = new ArrayList<>(Arrays.asList(អាគុយម៉ង់).subList(1,អាគុយម៉ង់.length));
        if (អំពើ.equals("run") || អំពើ.equals("desktop")) {
            if (អំពើ.equals("desktop")) 추가인수.add(0,"--desktop");
            호출(ខឺណេល_តំលៃ,내부경로(ខឺណេល_តំលៃ,(String)ការកំណត់.get("runner")),추가인수,환경);
        } else if (អំពើ.equals("image")) 호출(ខឺណេល_តំលៃ,내부경로(ខឺណេល_តំលៃ,(String)ការកំណត់.get("image_builder")),추가인수,환경);
        else if (អំពើ.equals("test-system")) {
            추가인수.add(0,បញ្ចាំង_ឬស.toString()); 추가인수.add(0,"--edition");
            호출(ខឺណេល_តំលៃ,내부경로(ខឺណេល_តំលៃ,(String)ការកំណត់.get("system_tester")),추가인수,환경);
        }
    }
}
