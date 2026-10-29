// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.security.MessageDigest;
import java.util.*;

/** 독립 국가판의 의존성 검사·복원·აწყობა_სისტემა·실행을 맡는 მასპინძელი Java ხელსაწყოები. */
public final class 국가실행기 {
    static final class 자료해석기 {
        final String წყარო; int პოზიცია;
        자료해석기(String ტექსტი) { წყარო = ტექსტი; }
        void 빈칸() { while (პოზიცია < წყარო.length() && Character.isWhitespace(წყარო.charAt(პოზიცია))) პოზიცია++; }
        Object კითხვა() {
            빈칸(); char სიმბოლო_მნიშვნელობა_068c2631 = წყარო.charAt(პოზიცია++);
            if (სიმბოლო_მნიშვნელობა_068c2631 == '{') {
                Map<String,Object> გაზომვა = new LinkedHashMap<>(); 빈칸();
                if (წყარო.charAt(პოზიცია) == '}') { პოზიცია++; return გაზომვა; }
                while (true) {
                    String სახელი = (String)კითხვა(); 빈칸(); if (წყარო.charAt(პოზიცია++) != ':') throw new IllegalArgumentException("მონაცემები გამყოფი_მნიშვნელობა_d8ba4873 შეცდომა");
                    გაზომვა.put(სახელი, კითხვა()); 빈칸(); char გამყოფი_მნიშვნელობა_d8ba4873 = წყარო.charAt(პოზიცია++);
                    if (გამყოფი_მნიშვნელობა_d8ba4873 == '}') return გაზომვა; if (გამყოფი_მნიშვნელობა_d8ba4873 != ',') throw new IllegalArgumentException("მონაცემები გამყოფი_მნიშვნელობა_d8ba4873 შეცდომა");
                }
            }
            if (სიმბოლო_მნიშვნელობა_068c2631 == '[') {
                List<Object> გაზომვა = new ArrayList<>(); 빈칸();
                if (წყარო.charAt(პოზიცია) == ']') { პოზიცია++; return გაზომვა; }
                while (true) {
                    გაზომვა.add(კითხვა()); 빈칸(); char გამყოფი_მნიშვნელობა_d8ba4873 = წყარო.charAt(პოზიცია++);
                    if (გამყოფი_მნიშვნელობა_d8ba4873 == ']') return გაზომვა; if (გამყოფი_მნიშვნელობა_d8ba4873 != ',') throw new IllegalArgumentException("მონაცემები გამყოფი_მნიშვნელობა_d8ba4873 შეცდომა");
                }
            }
            if (სიმბოლო_მნიშვნელობა_068c2631 == '"') {
                StringBuilder გაზომვა = new StringBuilder();
                while (true) {
                    char შემდეგი_ელემენტი = წყარო.charAt(პოზიცია++); if (შემდეგი_ელემენტი == '"') return გაზომვა.toString();
                    if (შემდეგი_ელემენტი == '\\') {
                        შემდეგი_ელემენტი = წყარო.charAt(პოზიცია++);
                        if (შემდეგი_ელემენტი == 'u') { გაზომვა.append((char)Integer.parseInt(წყარო.substring(პოზიცია, პოზიცია + 4),16)); პოზიცია += 4; continue; }
                        if (შემდეგი_ელემენტი == 'n') შემდეგი_ელემენტი = '\n'; else if (შემდეგი_ელემენტი == 'r') შემდეგი_ელემენტი = '\r'; else if (შემდეგი_ელემენტი == 't') შემდეგი_ელემენტი = '\t';
                        else if (შემდეგი_ელემენტი == 'b') შემდეგი_ელემენტი = '\b'; else if (შემდეგი_ელემენტი == 'f') შემდეგი_ელემენტი = '\f';
                        else if (შემდეგი_ელემენტი != '"' && შემდეგი_ელემენტი != '\\' && შემდეგი_ელემენტი != '/') throw new IllegalArgumentException("문자 이스케이프 შეცდომა");
                    }
                    გაზომვა.append(შემდეგი_ელემენტი);
                }
            }
            int გაშვება = პოზიცია - 1;
            while (პოზიცია < წყარო.length() && ",]} \t\r\n".indexOf(წყარო.charAt(პოზიცია)) < 0) პოზიცია++;
            String მნიშვნელობა = წყარო.substring(გაშვება, პოზიცია);
            if (მნიშვნელობა.equals("true")) return Boolean.TRUE; if (მნიშვნელობა.equals("false")) return Boolean.FALSE; if (მნიშვნელობა.equals("null")) return null;
            return Double.valueOf(მნიშვნელობა);
        }
    }
    static String ჰეში_ფაილი(Path გეზი) throws Exception {
        MessageDigest 계산 = MessageDigest.getInstance("SHA-256"); byte[] მონაცემები = new byte[1024 * 1024];
        try (InputStream 입력 = Files.newInputStream(გეზი)) { for (int სიგრძე_მნიშვნელობა; (სიგრძე_მნიშვნელობა = 입력.read(მონაცემები)) >= 0;) 계산.update(მონაცემები,0,სიგრძე_მნიშვნელობა); }
        return ჰეში_ტექსტი(계산.digest());
    }
    static String ჰეში_ტექსტი(byte[] მონაცემები) {
        StringBuilder ტექსტი = new StringBuilder(); for (byte მნიშვნელობა : მონაცემები) ტექსტი.append(String.format(Locale.ROOT,"%02x",მნიშვნელობა & 255)); return ტექსტი.toString();
    }
    static Path 내부경로(Path პროეცირება_ფესვი, String სახელი) {
        Path გაზომვა = პროეცირება_ფესვი.resolve(სახელი).normalize();
        if (სახელი.isEmpty() || Paths.get(სახელი).isAbsolute() || !გაზომვა.startsWith(პროეცირება_ფესვი) || სახელი.indexOf('\\') >= 0)
            throw new IllegalArgumentException("범위를 벗어난 გეზი: " + სახელი);
        for (Path 부분 : Paths.get(სახელი)) if (부분.toString().equals("..")) throw new IllegalArgumentException("상위 გეზი 금지: " + სახელი);
        for (Path 현재 = გაზომვა; 현재 != null && 현재.startsWith(პროეცირება_ფესვი); 현재 = 현재.getParent())
            if (Files.isSymbolicLink(현재)) throw new IllegalArgumentException("의존성 경로의 링크 금지: " + სახელი);
        return გაზომვა;
    }
    static String 명령출력(List<String> ბრძანება) throws Exception {
        Process პროცესი_მნიშვნელობა = new ProcessBuilder(ბრძანება).redirectError(ProcessBuilder.Redirect.INHERIT).start();
        String გაზომვა = new String(პროცესი_მნიშვნელობა.getInputStream().readAllBytes(),StandardCharsets.UTF_8);
        if (პროცესი_მნიშვნელობა.waitFor() != 0) throw new IOException("ბრძანება მარცხი_მნიშვნელობა: " + ბრძანება.get(0)); return გაზომვა;
    }
    static void ამოღება(Path არქივი_მნიშვნელობა, Path მიმართულება_მნიშვნელობა) throws Exception {
        for (String სახელი : 명령출력(Arrays.asList("tar","-tzf",არქივი_მნიშვნელობა.toString())).split("\n")) 내부경로(მიმართულება_მნიშვნელობა, სახელი);
        for (String ხაზი : 명령출력(Arrays.asList("tar","-tvzf",არქივი_მნიშვნელობა.toString())).split("\n"))
            if (!ხაზი.isEmpty() && ხაზი.charAt(0) != '-' && ხაზი.charAt(0) != 'd') throw new IOException("외부 링크 또는 특수 파일을 포함한 의존성");
        Files.createDirectories(მიმართულება_მნიშვნელობა);
        int სტატუსი_მნიშვნელობა = new ProcessBuilder("tar","--no-same-owner","--no-same-permissions","-xzf",არქივი_მნიშვნელობა.toString(),"-C",მიმართულება_მნიშვნელობა.toString()).inheritIO().start().waitFor();
        if (სტატუსი_მნიშვნელობა != 0) throw new IOException("의존성 არქივი_მნიშვნელობა რელიზი_საცავი მარცხი_მნიშვნელობა");
    }
    static void 호출(Path 작업경로, Path ხელსაწყოები, List<String> 인수, Map<String,String> 환경) throws Exception {
        List<String> ბრძანება = new ArrayList<>(Arrays.asList("python3", ხელსაწყოები.toString())); ბრძანება.addAll(인수);
        ProcessBuilder შესრულება_ბრძანება = new ProcessBuilder(ბრძანება).directory(작업경로.toFile()).inheritIO(); შესრულება_ბრძანება.environment().putAll(환경);
        int სტატუსი_მნიშვნელობა = შესრულება_ბრძანება.start().waitFor(); if (სტატუსი_მნიშვნელობა != 0) throw new IOException("ხელსაწყოები მარცხი_მნიშვნელობა: " + ხელსაწყოები + " (" + სტატუსი_მნიშვნელობა + ")");
    }
    @SuppressWarnings("unchecked")
    public static void main(String[] 인수) throws Exception {
        if (인수.length < 1) throw new IllegalArgumentException("build, run, desktop, image, check, test-system 중 동작을 지정하세요");
        String ქმედება = 인수[0];
        if (!Arrays.asList("build","run","desktop","image","check","test-system").contains(ქმედება)) throw new IllegalArgumentException("알 수 없는 ქმედება");
        Path პროეცირება_ფესვი = Paths.get(System.getProperty("worldos.edition.root")).toAbsolutePath().normalize();
        Map<String,Object> პარამეტრები = (Map<String,Object>)new 자료해석기(Files.readString(პროეცირება_ფესვი.resolve("native.json"),StandardCharsets.UTF_8)).კითხვა();
        Path წყარო_ხე = 내부경로(პროეცირება_ფესვი,(String)პარამეტრები.get("source")), ბირთვი_მნიშვნელობა = 내부경로(წყარო_ხე,(String)პარამეტრები.get("native"));
        List<String> 소유파일들 = (List<String>)(List<?>)პარამეტრები.get("owned_files");
        for (String სახელი : 소유파일들) if (!Files.isRegularFile(내부경로(წყარო_ხე,სახელი))) throw new IOException("წყარო_ხე 없음: " + სახელი);
        if (ქმედება.equals("check")) { System.out.println(პარამეტრები.get("country") + " " + პარამეტრები.get("language") + " 독립 წყარო_ხე გადამოწმება 완료"); return; }
        String 자원상대 = (String)პარამეტრები.getOrDefault("resource_root", ".");
        if (!자원상대.equals(".") && !자원상대.equals("..")) throw new IllegalArgumentException("의존성 პროეცირება_ფესვი გეზი შეცდომა");
        Path რესურსი_მნიშვნელობა = პროეცირება_ფესვი.resolve(자원상대).normalize(); Path არქივი_მნიშვნელობა = რესურსი_მნიშვნელობა.resolve("native-vendor.tar.gz");
        String 기대해시 = (String)პარამეტრები.get("vendor_sha256");
        if (!ჰეში_ფაილი(არქივი_მნიშვნელობა).equals(기대해시)) throw new IOException("의존성 SHA-256 불일치");
        Path 표식 = წყარო_ხე.resolve(".vendor-sha256");
        if (!Files.isRegularFile(표식) || !Files.readString(표식).trim().equals(기대해시)) { ამოღება(არქივი_მნიშვნელობა, წყარო_ხე); Files.writeString(표식,기대해시 + "\n"); }
        Map<String,String> 환경 = new HashMap<>(System.getenv());
        Path ipConfig = null;
        if (환경.containsKey("IP_CONFIG")) ipConfig = Paths.get(환경.get("IP_CONFIG")).toAbsolutePath().normalize();
        else for (Path parent = პროეცირება_ფესვი; parent != null; parent = parent.getParent()) {
            if (Files.isRegularFile(parent.resolve("ip.conf"))) { ipConfig = parent.resolve("ip.conf"); break; }
        }
        if (ipConfig == null) ipConfig = წყარო_ხე.resolve("ip.conf");
        if (!Files.isRegularFile(ipConfig)) throw new IOException("Missing ip.conf: " + ipConfig);
        환경.put("IP_CONFIG", ipConfig.toString());
        if (Arrays.asList("run","desktop","test-system").contains(ქმედება) && !환경.containsKey("QEMU_AARCH64")) {
            Path აპი_გამშვები = რესურსი_მნიშვნელობა.resolve("host/qemu"), 실행기표식 = რესურსი_მნიშვნელობა.resolve("host/.qemu-sha256");
            String გამშვები_ჰეში = (String)პარამეტრები.get("qemu_sha256");
            if (!Files.isRegularFile(აპი_გამშვები) || !Files.isRegularFile(실행기표식) || !Files.readString(실행기표식).trim().equals(გამშვები_ჰეში)) {
                Path გამშვები_არქივი = რესურსი_მნიშვნელობა.resolve("qemu-host.tar.gz"); if (!ჰეში_ფაილი(გამშვები_არქივი).equals(გამშვები_ჰეში)) throw new IOException("QEMU SHA-256 불일치");
                ამოღება(გამშვები_არქივი,რესურსი_მნიშვნელობა.resolve("host")); Files.writeString(실행기표식,გამშვები_ჰეში + "\n");
            }
            환경.put("QEMU_AARCH64",აპი_გამშვები.toString());
        }
        MessageDigest 계산 = MessageDigest.getInstance("SHA-256"); Collections.sort(소유파일들);
        for (String სახელი : 소유파일들) { 계산.update(სახელი.getBytes(StandardCharsets.UTF_8)); 계산.update(Files.readAllBytes(내부경로(წყარო_ხე,სახელი))); }
        계산.update("ip.conf\0".getBytes(StandardCharsets.UTF_8)); 계산.update(Files.readAllBytes(ipConfig));
        String წყარო_ჰეში = ჰეში_ტექსტი(계산.digest()); Path 빌드표식 = ბირთვი_მნიშვნელობა.resolve("build/worldos-source.sha256");
        if (ქმედება.equals("build") || !Files.isRegularFile(빌드표식) || !Files.readString(빌드표식).trim().equals(წყარო_ჰეში)) {
            호출(ბირთვი_მნიშვნელობა,내부경로(ბირთვი_მნიშვნელობა,(String)პარამეტრები.get("builder")),Collections.emptyList(),환경);
            Files.writeString(빌드표식,წყარო_ჰეში + "\n");
        }
        List<String> 추가인수 = new ArrayList<>(Arrays.asList(인수).subList(1,인수.length));
        if (ქმედება.equals("run") || ქმედება.equals("desktop")) {
            if (ქმედება.equals("desktop")) 추가인수.add(0,"--desktop");
            호출(ბირთვი_მნიშვნელობა,내부경로(ბირთვი_მნიშვნელობა,(String)პარამეტრები.get("runner")),추가인수,환경);
        } else if (ქმედება.equals("image")) 호출(ბირთვი_მნიშვნელობა,내부경로(ბირთვი_მნიშვნელობა,(String)პარამეტრები.get("image_builder")),추가인수,환경);
        else if (ქმედება.equals("test-system")) {
            추가인수.add(0,პროეცირება_ფესვი.toString()); 추가인수.add(0,"--edition");
            호출(ბირთვი_მნიშვნელობა,내부경로(ბირთვი_მნიშვნელობა,(String)პარამეტრები.get("system_tester")),추가인수,환경);
        }
    }
}
