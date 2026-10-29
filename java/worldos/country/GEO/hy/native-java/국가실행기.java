// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.security.MessageDigest;
import java.util.*;

/** 독립 국가판의 의존성 검사·복원·կառուցել_համակարգ·실행을 맡는 հոստ Java Գործիքներ. */
public final class 국가실행기 {
    static final class 자료해석기 {
        final String ԱՂԲՅՈՒՐ; int Դիրք;
        자료해석기(String Տեքստ) { ԱՂԲՅՈՒՐ = Տեքստ; }
        void 빈칸() { while (Դիրք < ԱՂԲՅՈՒՐ.length() && Character.isWhitespace(ԱՂԲՅՈՒՐ.charAt(Դիրք))) Դիրք++; }
        Object Ընթերցում() {
            빈칸(); char գրանշան_արժեք = ԱՂԲՅՈՒՐ.charAt(Դիրք++);
            if (գրանշան_արժեք == '{') {
                Map<String,Object> չափ = new LinkedHashMap<>(); 빈칸();
                if (ԱՂԲՅՈՒՐ.charAt(Դիրք) == '}') { Դիրք++; return չափ; }
                while (true) {
                    String Անուն = (String)Ընթերցում(); 빈칸(); if (ԱՂԲՅՈՒՐ.charAt(Դիրք++) != ':') throw new IllegalArgumentException("տվյալ սահմանանշիչ_արժեք Սխալ");
                    չափ.put(Անուն, Ընթերցում()); 빈칸(); char սահմանանշիչ_արժեք = ԱՂԲՅՈՒՐ.charAt(Դիրք++);
                    if (սահմանանշիչ_արժեք == '}') return չափ; if (սահմանանշիչ_արժեք != ',') throw new IllegalArgumentException("տվյալ սահմանանշիչ_արժեք Սխալ");
                }
            }
            if (գրանշան_արժեք == '[') {
                List<Object> չափ = new ArrayList<>(); 빈칸();
                if (ԱՂԲՅՈՒՐ.charAt(Դիրք) == ']') { Դիրք++; return չափ; }
                while (true) {
                    չափ.add(Ընթերցում()); 빈칸(); char սահմանանշիչ_արժեք = ԱՂԲՅՈՒՐ.charAt(Դիրք++);
                    if (սահմանանշիչ_արժեք == ']') return չափ; if (սահմանանշիչ_արժեք != ',') throw new IllegalArgumentException("տվյալ սահմանանշիչ_արժեք Սխալ");
                }
            }
            if (գրանշան_արժեք == '"') {
                StringBuilder չափ = new StringBuilder();
                while (true) {
                    char Հաջորդը_միավոր = ԱՂԲՅՈՒՐ.charAt(Դիրք++); if (Հաջորդը_միավոր == '"') return չափ.toString();
                    if (Հաջորդը_միավոր == '\\') {
                        Հաջորդը_միավոր = ԱՂԲՅՈՒՐ.charAt(Դիրք++);
                        if (Հաջորդը_միավոր == 'u') { չափ.append((char)Integer.parseInt(ԱՂԲՅՈՒՐ.substring(Դիրք, Դիրք + 4),16)); Դիրք += 4; continue; }
                        if (Հաջորդը_միավոր == 'n') Հաջորդը_միավոր = '\n'; else if (Հաջորդը_միավոր == 'r') Հաջորդը_միավոր = '\r'; else if (Հաջորդը_միավոր == 't') Հաջորդը_միավոր = '\t';
                        else if (Հաջորդը_միավոր == 'b') Հաջորդը_միավոր = '\b'; else if (Հաջորդը_միավոր == 'f') Հաջորդը_միավոր = '\f';
                        else if (Հաջորդը_միավոր != '"' && Հաջորդը_միավոր != '\\' && Հաջորդը_միավոր != '/') throw new IllegalArgumentException("문자 이스케이프 Սխալ");
                    }
                    չափ.append(Հաջորդը_միավոր);
                }
            }
            int Գործարկել = Դիրք - 1;
            while (Դիրք < ԱՂԲՅՈՒՐ.length() && ",]} \t\r\n".indexOf(ԱՂԲՅՈՒՐ.charAt(Դիրք)) < 0) Դիրք++;
            String արժեք = ԱՂԲՅՈՒՐ.substring(Գործարկել, Դիրք);
            if (արժեք.equals("true")) return Boolean.TRUE; if (արժեք.equals("false")) return Boolean.FALSE; if (արժեք.equals("null")) return null;
            return Double.valueOf(արժեք);
        }
    }
    static String պատահական_տվյալներ_նիշք(Path Ճանապարհ) throws Exception {
        MessageDigest 계산 = MessageDigest.getInstance("SHA-256"); byte[] տվյալ = new byte[1024 * 1024];
        try (InputStream 입력 = Files.newInputStream(Ճանապարհ)) { for (int տեւողություն_արժեք; (տեւողություն_արժեք = 입력.read(տվյալ)) >= 0;) 계산.update(տվյալ,0,տեւողություն_արժեք); }
        return պատահական_տվյալներ_Գրվածք(계산.digest());
    }
    static String պատահական_տվյալներ_Գրվածք(byte[] տվյալ) {
        StringBuilder Տեքստ = new StringBuilder(); for (byte արժեք : տվյալ) Տեքստ.append(String.format(Locale.ROOT,"%02x",արժեք & 255)); return Տեքստ.toString();
    }
    static Path 내부경로(Path արձակել_արմատ, String Անուն) {
        Path չափ = արձակել_արմատ.resolve(Անուն).normalize();
        if (Անուն.isEmpty() || Paths.get(Անուն).isAbsolute() || !չափ.startsWith(արձակել_արմատ) || Անուն.indexOf('\\') >= 0)
            throw new IllegalArgumentException("범위를 벗어난 Ճանապարհ: " + Անուն);
        for (Path 부분 : Paths.get(Անուն)) if (부분.toString().equals("..")) throw new IllegalArgumentException("상위 Ճանապարհ 금지: " + Անուն);
        for (Path 현재 = չափ; 현재 != null && 현재.startsWith(արձակել_արմատ); 현재 = 현재.getParent())
            if (Files.isSymbolicLink(현재)) throw new IllegalArgumentException("의존성 경로의 링크 금지: " + Անուն);
        return չափ;
    }
    static String 명령출력(List<String> Հրահանգ) throws Exception {
        Process Ընթացք_արժեք = new ProcessBuilder(Հրահանգ).redirectError(ProcessBuilder.Redirect.INHERIT).start();
        String չափ = new String(Ընթացք_արժեք.getInputStream().readAllBytes(),StandardCharsets.UTF_8);
        if (Ընթացք_արժեք.waitFor() != 0) throw new IOException("Հրահանգ ձախողում_արժեք: " + Հրահանգ.get(0)); return չափ;
    }
    static void արտահանել(Path Պահոց_արժեք, Path նպատակակետ_արժեք) throws Exception {
        for (String Անուն : 명령출력(Arrays.asList("tar","-tzf",Պահոց_արժեք.toString())).split("\n")) 내부경로(նպատակակետ_արժեք, Անուն);
        for (String կապ : 명령출력(Arrays.asList("tar","-tvzf",Պահոց_արժեք.toString())).split("\n"))
            if (!կապ.isEmpty() && կապ.charAt(0) != '-' && կապ.charAt(0) != 'd') throw new IOException("외부 링크 또는 특수 파일을 포함한 의존성");
        Files.createDirectories(նպատակակետ_արժեք);
        int վիճակ_արժեք = new ProcessBuilder("tar","--no-same-owner","--no-same-permissions","-xzf",Պահոց_արժեք.toString(),"-C",նպատակակետ_արժեք.toString()).inheritIO().start().waitFor();
        if (վիճակ_արժեք != 0) throw new IOException("의존성 Պահոց_արժեք արձակել_Պահեստ ձախողում_արժեք");
    }
    static void 호출(Path 작업경로, Path Գործիքներ, List<String> 인수, Map<String,String> 환경) throws Exception {
        List<String> Հրահանգ = new ArrayList<>(Arrays.asList("python3", Գործիքներ.toString())); Հրահանգ.addAll(인수);
        ProcessBuilder կատարել_հրաման = new ProcessBuilder(Հրահանգ).directory(작업경로.toFile()).inheritIO(); կատարել_հրաման.environment().putAll(환경);
        int վիճակ_արժեք = կատարել_հրաման.start().waitFor(); if (վիճակ_արժեք != 0) throw new IOException("Գործիքներ ձախողում_արժեք: " + Գործիքներ + " (" + վիճակ_արժեք + ")");
    }
    @SuppressWarnings("unchecked")
    public static void main(String[] 인수) throws Exception {
        if (인수.length < 1) throw new IllegalArgumentException("build, run, desktop, image, check, test-system 중 동작을 지정하세요");
        String Գործողություն = 인수[0];
        if (!Arrays.asList("build","run","desktop","image","check","test-system").contains(Գործողություն)) throw new IllegalArgumentException("알 수 없는 Գործողություն");
        Path արձակել_արմատ = Paths.get(System.getProperty("worldos.edition.root")).toAbsolutePath().normalize();
        Map<String,Object> Նախընտրանքներ = (Map<String,Object>)new 자료해석기(Files.readString(արձակել_արմատ.resolve("native.json"),StandardCharsets.UTF_8)).Ընթերցում();
        Path աղբյուր_ծառ = 내부경로(արձակել_արմատ,(String)Նախընտրանքներ.get("source")), միջուկ_արժեք = 내부경로(աղբյուր_ծառ,(String)Նախընտրանքներ.get("native"));
        List<String> 소유파일들 = (List<String>)(List<?>)Նախընտրանքներ.get("owned_files");
        for (String Անուն : 소유파일들) if (!Files.isRegularFile(내부경로(աղբյուր_ծառ,Անուն))) throw new IOException("աղբյուր_ծառ 없음: " + Անուն);
        if (Գործողություն.equals("check")) { System.out.println(Նախընտրանքներ.get("country") + " " + Նախընտրանքներ.get("language") + " 독립 աղբյուր_ծառ հաստատել 완료"); return; }
        String 자원상대 = (String)Նախընտրանքներ.getOrDefault("resource_root", ".");
        if (!자원상대.equals(".") && !자원상대.equals("..")) throw new IllegalArgumentException("의존성 արձակել_արմատ Ճանապարհ Սխալ");
        Path միջոց_արժեք = արձակել_արմատ.resolve(자원상대).normalize(); Path Պահոց_արժեք = միջոց_արժեք.resolve("native-vendor.tar.gz");
        String 기대해시 = (String)Նախընտրանքներ.get("vendor_sha256");
        if (!պատահական_տվյալներ_նիշք(Պահոց_արժեք).equals(기대해시)) throw new IOException("의존성 SHA-256 불일치");
        Path 표식 = աղբյուր_ծառ.resolve(".vendor-sha256");
        if (!Files.isRegularFile(표식) || !Files.readString(표식).trim().equals(기대해시)) { արտահանել(Պահոց_արժեք, աղբյուր_ծառ); Files.writeString(표식,기대해시 + "\n"); }
        Map<String,String> 환경 = new HashMap<>(System.getenv());
        Path ipConfig = null;
        if (환경.containsKey("IP_CONFIG")) ipConfig = Paths.get(환경.get("IP_CONFIG")).toAbsolutePath().normalize();
        else for (Path parent = արձակել_արմատ; parent != null; parent = parent.getParent()) {
            if (Files.isRegularFile(parent.resolve("ip.conf"))) { ipConfig = parent.resolve("ip.conf"); break; }
        }
        if (ipConfig == null) ipConfig = աղբյուր_ծառ.resolve("ip.conf");
        if (!Files.isRegularFile(ipConfig)) throw new IOException("Missing ip.conf: " + ipConfig);
        환경.put("IP_CONFIG", ipConfig.toString());
        if (Arrays.asList("run","desktop","test-system").contains(Գործողություն) && !환경.containsKey("QEMU_AARCH64")) {
            Path ծրագիր_թողարկիչ = միջոց_արժեք.resolve("host/qemu"), 실행기표식 = միջոց_արժեք.resolve("host/.qemu-sha256");
            String թողարկիչ_պատահական_տվյալներ = (String)Նախընտրանքներ.get("qemu_sha256");
            if (!Files.isRegularFile(ծրագիր_թողարկիչ) || !Files.isRegularFile(실행기표식) || !Files.readString(실행기표식).trim().equals(թողարկիչ_պատահական_տվյալներ)) {
                Path թողարկիչ_Պահոց = միջոց_արժեք.resolve("qemu-host.tar.gz"); if (!պատահական_տվյալներ_նիշք(թողարկիչ_Պահոց).equals(թողարկիչ_պատահական_տվյալներ)) throw new IOException("QEMU SHA-256 불일치");
                արտահանել(թողարկիչ_Պահոց,միջոց_արժեք.resolve("host")); Files.writeString(실행기표식,թողարկիչ_պատահական_տվյալներ + "\n");
            }
            환경.put("QEMU_AARCH64",ծրագիր_թողարկիչ.toString());
        }
        MessageDigest 계산 = MessageDigest.getInstance("SHA-256"); Collections.sort(소유파일들);
        for (String Անուն : 소유파일들) { 계산.update(Անուն.getBytes(StandardCharsets.UTF_8)); 계산.update(Files.readAllBytes(내부경로(աղբյուր_ծառ,Անուն))); }
        계산.update("ip.conf\0".getBytes(StandardCharsets.UTF_8)); 계산.update(Files.readAllBytes(ipConfig));
        String աղբյուր_պատահական_տվյալներ = պատահական_տվյալներ_Գրվածք(계산.digest()); Path 빌드표식 = միջուկ_արժեք.resolve("build/worldos-source.sha256");
        if (Գործողություն.equals("build") || !Files.isRegularFile(빌드표식) || !Files.readString(빌드표식).trim().equals(աղբյուր_պատահական_տվյալներ)) {
            호출(միջուկ_արժեք,내부경로(միջուկ_արժեք,(String)Նախընտրանքներ.get("builder")),Collections.emptyList(),환경);
            Files.writeString(빌드표식,աղբյուր_պատահական_տվյալներ + "\n");
        }
        List<String> 추가인수 = new ArrayList<>(Arrays.asList(인수).subList(1,인수.length));
        if (Գործողություն.equals("run") || Գործողություն.equals("desktop")) {
            if (Գործողություն.equals("desktop")) 추가인수.add(0,"--desktop");
            호출(միջուկ_արժեք,내부경로(միջուկ_արժեք,(String)Նախընտրանքներ.get("runner")),추가인수,환경);
        } else if (Գործողություն.equals("image")) 호출(միջուկ_արժեք,내부경로(միջուկ_արժեք,(String)Նախընտրանքներ.get("image_builder")),추가인수,환경);
        else if (Գործողություն.equals("test-system")) {
            추가인수.add(0,արձակել_արմատ.toString()); 추가인수.add(0,"--edition");
            호출(միջուկ_արժեք,내부경로(միջուկ_արժեք,(String)Նախընտրանքներ.get("system_tester")),추가인수,환경);
        }
    }
}
