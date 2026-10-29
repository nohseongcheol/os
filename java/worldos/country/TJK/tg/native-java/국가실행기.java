// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.security.MessageDigest;
import java.util.*;

/** 독립 국가판의 의존성 검사·복원·сохт_система·실행을 맡는 мизбон Java Абзорҳо. */
public final class 국가실행기 {
    static final class 자료해석기 {
        final String манбаъ; int 위치;
        자료해석기(String Матн) { манбаъ = Матн; }
        void 빈칸() { while (위치 < манбаъ.length() && Character.isWhitespace(манбаъ.charAt(위치))) 위치++; }
        Object Хондан() {
            빈칸(); char аломат_қимат_068c2631 = манбаъ.charAt(위치++);
            if (аломат_қимат_068c2631 == '{') {
                Map<String,Object> 결과 = new LinkedHashMap<>(); 빈칸();
                if (манбаъ.charAt(위치) == '}') { 위치++; return 결과; }
                while (true) {
                    String Ном = (String)Хондан(); 빈칸(); if (манбаъ.charAt(위치++) != ':') throw new IllegalArgumentException("иттилоот маҳдудкунанда_қимат Хато");
                    결과.put(Ном, Хондан()); 빈칸(); char маҳдудкунанда_қимат = манбаъ.charAt(위치++);
                    if (маҳдудкунанда_қимат == '}') return 결과; if (маҳдудкунанда_қимат != ',') throw new IllegalArgumentException("иттилоот маҳдудкунанда_қимат Хато");
                }
            }
            if (аломат_қимат_068c2631 == '[') {
                List<Object> 결과 = new ArrayList<>(); 빈칸();
                if (манбаъ.charAt(위치) == ']') { 위치++; return 결과; }
                while (true) {
                    결과.add(Хондан()); 빈칸(); char маҳдудкунанда_қимат = манбаъ.charAt(위치++);
                    if (маҳдудкунанда_қимат == ']') return 결과; if (маҳдудкунанда_қимат != ',') throw new IllegalArgumentException("иттилоот маҳдудкунанда_қимат Хато");
                }
            }
            if (аломат_қимат_068c2631 == '"') {
                StringBuilder 결과 = new StringBuilder();
                while (true) {
                    char 다음 = манбаъ.charAt(위치++); if (다음 == '"') return 결과.toString();
                    if (다음 == '\\') {
                        다음 = манбаъ.charAt(위치++);
                        if (다음 == 'u') { 결과.append((char)Integer.parseInt(манбаъ.substring(위치, 위치 + 4),16)); 위치 += 4; continue; }
                        if (다음 == 'n') 다음 = '\n'; else if (다음 == 'r') 다음 = '\r'; else if (다음 == 't') 다음 = '\t';
                        else if (다음 == 'b') 다음 = '\b'; else if (다음 == 'f') 다음 = '\f';
                        else if (다음 != '"' && 다음 != '\\' && 다음 != '/') throw new IllegalArgumentException("문자 이스케이프 Хато");
                    }
                    결과.append(다음);
                }
            }
            int порча = 위치 - 1;
            while (위치 < манбаъ.length() && ",]} \t\r\n".indexOf(манбаъ.charAt(위치)) < 0) 위치++;
            String қимат = манбаъ.substring(порча, 위치);
            if (қимат.equals("true")) return Boolean.TRUE; if (қимат.equals("false")) return Boolean.FALSE; if (қимат.equals("null")) return null;
            return Double.valueOf(қимат);
        }
    }
    static String ҳэш_файл(Path масир) throws Exception {
        MessageDigest 계산 = MessageDigest.getInstance("SHA-256"); byte[] иттилоот = new byte[1024 * 1024];
        try (InputStream 입력 = Files.newInputStream(масир)) { for (int дарозӣ_қимат; (дарозӣ_қимат = 입력.read(иттилоот)) >= 0;) 계산.update(иттилоот,0,дарозӣ_қимат); }
        return ҳэш_Матн(계산.digest());
    }
    static String ҳэш_Матн(byte[] иттилоот) {
        StringBuilder Матн = new StringBuilder(); for (byte қимат : иттилоот) Матн.append(String.format(Locale.ROOT,"%02x",қимат & 255)); return Матн.toString();
    }
    static Path 내부경로(Path 기준, String Ном) {
        Path 결과 = 기준.resolve(Ном).normalize();
        if (Ном.isEmpty() || Paths.get(Ном).isAbsolute() || !결과.startsWith(기준) || Ном.indexOf('\\') >= 0)
            throw new IllegalArgumentException("범위를 벗어난 масир: " + Ном);
        for (Path 부분 : Paths.get(Ном)) if (부분.toString().equals("..")) throw new IllegalArgumentException("상위 масир 금지: " + Ном);
        for (Path 현재 = 결과; 현재 != null && 현재.startsWith(기준); 현재 = 현재.getParent())
            if (Files.isSymbolicLink(현재)) throw new IllegalArgumentException("의존성 경로의 링크 금지: " + Ном);
        return 결과;
    }
    static String 명령출력(List<String> фармон) throws Exception {
        Process Раванд_қимат = new ProcessBuilder(фармон).redirectError(ProcessBuilder.Redirect.INHERIT).start();
        String 결과 = new String(Раванд_қимат.getInputStream().readAllBytes(),StandardCharsets.UTF_8);
        if (Раванд_қимат.waitFor() != 0) throw new IOException("фармон нокомӣ_қимат: " + фармон.get(0)); return 결과;
    }
    static void баровардан(Path Бойгонӣ_қимат, Path ҷои_таъинот_қимат) throws Exception {
        for (String Ном : 명령출력(Arrays.asList("tar","-tzf",Бойгонӣ_қимат.toString())).split("\n")) 내부경로(ҷои_таъинот_қимат, Ном);
        for (String хат : 명령출력(Arrays.asList("tar","-tvzf",Бойгонӣ_қимат.toString())).split("\n"))
            if (!хат.isEmpty() && хат.charAt(0) != '-' && хат.charAt(0) != 'd') throw new IOException("외부 링크 또는 특수 파일을 포함한 의존성");
        Files.createDirectories(ҷои_таъинот_қимат);
        int вазъият_қимат = new ProcessBuilder("tar","--no-same-owner","--no-same-permissions","-xzf",Бойгонӣ_қимат.toString(),"-C",ҷои_таъинот_қимат.toString()).inheritIO().start().waitFor();
        if (вазъият_қимат != 0) throw new IOException("의존성 Бойгонӣ_қимат нашр_Захирагоҳ нокомӣ_қимат");
    }
    static void 호출(Path 작업경로, Path Абзорҳо, List<String> 인수, Map<String,String> 환경) throws Exception {
        List<String> фармон = new ArrayList<>(Arrays.asList("python3", Абзорҳо.toString())); фармон.addAll(인수);
        ProcessBuilder иҷро_кардан_фармон = new ProcessBuilder(фармон).directory(작업경로.toFile()).inheritIO(); иҷро_кардан_фармон.environment().putAll(환경);
        int вазъият_қимат = иҷро_кардан_фармон.start().waitFor(); if (вазъият_қимат != 0) throw new IOException("Абзорҳо нокомӣ_қимат: " + Абзорҳо + " (" + вазъият_қимат + ")");
    }
    @SuppressWarnings("unchecked")
    public static void main(String[] 인수) throws Exception {
        if (인수.length < 1) throw new IllegalArgumentException("build, run, desktop, image, check, test-system 중 동작을 지정하세요");
        String Амал = 인수[0];
        if (!Arrays.asList("build","run","desktop","image","check","test-system").contains(Амал)) throw new IllegalArgumentException("알 수 없는 Амал");
        Path 기준 = Paths.get(System.getProperty("worldos.edition.root")).toAbsolutePath().normalize();
        Map<String,Object> Танзимот = (Map<String,Object>)new 자료해석기(Files.readString(기준.resolve("native.json"),StandardCharsets.UTF_8)).Хондан();
        Path манбаъ_дарахт = 내부경로(기준,(String)Танзимот.get("source")), ҳаста_қимат = 내부경로(манбаъ_дарахт,(String)Танзимот.get("native"));
        List<String> 소유파일들 = (List<String>)(List<?>)Танзимот.get("owned_files");
        for (String Ном : 소유파일들) if (!Files.isRegularFile(내부경로(манбаъ_дарахт,Ном))) throw new IOException("манбаъ_дарахт 없음: " + Ном);
        if (Амал.equals("check")) { System.out.println(Танзимот.get("country") + " " + Танзимот.get("language") + " 독립 манбаъ_дарахт тасдиқ_кардан 완료"); return; }
        String 자원상대 = (String)Танзимот.getOrDefault("resource_root", ".");
        if (!자원상대.equals(".") && !자원상대.equals("..")) throw new IllegalArgumentException("의존성 기준 масир Хато");
        Path захира_қимат = 기준.resolve(자원상대).normalize(); Path Бойгонӣ_қимат = захира_қимат.resolve("native-vendor.tar.gz");
        String 기대해시 = (String)Танзимот.get("vendor_sha256");
        if (!ҳэш_файл(Бойгонӣ_қимат).equals(기대해시)) throw new IOException("의존성 SHA-256 불일치");
        Path 표식 = манбаъ_дарахт.resolve(".vendor-sha256");
        if (!Files.isRegularFile(표식) || !Files.readString(표식).trim().equals(기대해시)) { баровардан(Бойгонӣ_қимат, манбаъ_дарахт); Files.writeString(표식,기대해시 + "\n"); }
        Map<String,String> 환경 = new HashMap<>(System.getenv());
        Path ipConfig = null;
        if (환경.containsKey("IP_CONFIG")) ipConfig = Paths.get(환경.get("IP_CONFIG")).toAbsolutePath().normalize();
        else for (Path parent = 기준; parent != null; parent = parent.getParent()) {
            if (Files.isRegularFile(parent.resolve("ip.conf"))) { ipConfig = parent.resolve("ip.conf"); break; }
        }
        if (ipConfig == null) ipConfig = манбаъ_дарахт.resolve("ip.conf");
        if (!Files.isRegularFile(ipConfig)) throw new IOException("Missing ip.conf: " + ipConfig);
        환경.put("IP_CONFIG", ipConfig.toString());
        if (Arrays.asList("run","desktop","test-system").contains(Амал) && !환경.containsKey("QEMU_AARCH64")) {
            Path барнома_панели_барномаҳо = захира_қимат.resolve("host/qemu"), 실행기표식 = захира_қимат.resolve("host/.qemu-sha256");
            String панели_барномаҳо_ҳэш = (String)Танзимот.get("qemu_sha256");
            if (!Files.isRegularFile(барнома_панели_барномаҳо) || !Files.isRegularFile(실행기표식) || !Files.readString(실행기표식).trim().equals(панели_барномаҳо_ҳэш)) {
                Path панели_барномаҳо_Бойгонӣ = захира_қимат.resolve("qemu-host.tar.gz"); if (!ҳэш_файл(панели_барномаҳо_Бойгонӣ).equals(панели_барномаҳо_ҳэш)) throw new IOException("QEMU SHA-256 불일치");
                баровардан(панели_барномаҳо_Бойгонӣ,захира_қимат.resolve("host")); Files.writeString(실행기표식,панели_барномаҳо_ҳэш + "\n");
            }
            환경.put("QEMU_AARCH64",барнома_панели_барномаҳо.toString());
        }
        MessageDigest 계산 = MessageDigest.getInstance("SHA-256"); Collections.sort(소유파일들);
        for (String Ном : 소유파일들) { 계산.update(Ном.getBytes(StandardCharsets.UTF_8)); 계산.update(Files.readAllBytes(내부경로(манбаъ_дарахт,Ном))); }
        계산.update("ip.conf\0".getBytes(StandardCharsets.UTF_8)); 계산.update(Files.readAllBytes(ipConfig));
        String манбаъ_ҳэш = ҳэш_Матн(계산.digest()); Path 빌드표식 = ҳаста_қимат.resolve("build/worldos-source.sha256");
        if (Амал.equals("build") || !Files.isRegularFile(빌드표식) || !Files.readString(빌드표식).trim().equals(манбаъ_ҳэш)) {
            호출(ҳаста_қимат,내부경로(ҳаста_қимат,(String)Танзимот.get("builder")),Collections.emptyList(),환경);
            Files.writeString(빌드표식,манбаъ_ҳэш + "\n");
        }
        List<String> 추가인수 = new ArrayList<>(Arrays.asList(인수).subList(1,인수.length));
        if (Амал.equals("run") || Амал.equals("desktop")) {
            if (Амал.equals("desktop")) 추가인수.add(0,"--desktop");
            호출(ҳаста_қимат,내부경로(ҳаста_қимат,(String)Танзимот.get("runner")),추가인수,환경);
        } else if (Амал.equals("image")) 호출(ҳаста_қимат,내부경로(ҳаста_қимат,(String)Танзимот.get("image_builder")),추가인수,환경);
        else if (Амал.equals("test-system")) {
            추가인수.add(0,기준.toString()); 추가인수.add(0,"--edition");
            호출(ҳаста_қимат,내부경로(ҳаста_қимат,(String)Танзимот.get("system_tester")),추가인수,환경);
        }
    }
}
