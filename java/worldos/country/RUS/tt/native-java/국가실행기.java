// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.security.MessageDigest;
import java.util.*;

/** 독립 국가판의 의존성 검사·복원·төзү_система·실행을 맡는 хост Java Кораллар. */
public final class 국가실행기 {
    static final class 자료해석기 {
        final String чыганак; int урнаштыру;
        자료해석기(String Mäten) { чыганак = Mäten; }
        void 빈칸() { while (урнаштыру < чыганак.length() && Character.isWhitespace(чыганак.charAt(урнаштыру))) урнаштыру++; }
        Object 읽기() {
            빈칸(); char символ_VALUE_068c2631 = чыганак.charAt(урнаштыру++);
            if (символ_VALUE_068c2631 == '{') {
                Map<String,Object> үлчәм = new LinkedHashMap<>(); 빈칸();
                if (чыганак.charAt(урнаштыру) == '}') { урнаштыру++; return үлчәм; }
                while (true) {
                    String исем = (String)읽기(); 빈칸(); if (чыганак.charAt(урнаштыру++) != ':') throw new IllegalArgumentException("мәгълүмат аергыч_VALUE_d8ba4873 Хата");
                    үлчәм.put(исем, 읽기()); 빈칸(); char аергыч_VALUE_d8ba4873 = чыганак.charAt(урнаштыру++);
                    if (аергыч_VALUE_d8ba4873 == '}') return үлчәм; if (аергыч_VALUE_d8ba4873 != ',') throw new IllegalArgumentException("мәгълүмат аергыч_VALUE_d8ba4873 Хата");
                }
            }
            if (символ_VALUE_068c2631 == '[') {
                List<Object> үлчәм = new ArrayList<>(); 빈칸();
                if (чыганак.charAt(урнаштыру) == ']') { урнаштыру++; return үлчәм; }
                while (true) {
                    үлчәм.add(읽기()); 빈칸(); char аергыч_VALUE_d8ba4873 = чыганак.charAt(урнаштыру++);
                    if (аергыч_VALUE_d8ba4873 == ']') return үлчәм; if (аергыч_VALUE_d8ba4873 != ',') throw new IllegalArgumentException("мәгълүмат аергыч_VALUE_d8ba4873 Хата");
                }
            }
            if (символ_VALUE_068c2631 == '"') {
                StringBuilder үлчәм = new StringBuilder();
                while (true) {
                    char Киләсе_элемент = чыганак.charAt(урнаштыру++); if (Киләсе_элемент == '"') return үлчәм.toString();
                    if (Киләсе_элемент == '\\') {
                        Киләсе_элемент = чыганак.charAt(урнаштыру++);
                        if (Киләсе_элемент == 'u') { үлчәм.append((char)Integer.parseInt(чыганак.substring(урнаштыру, урнаштыру + 4),16)); урнаштыру += 4; continue; }
                        if (Киләсе_элемент == 'n') Киләсе_элемент = '\n'; else if (Киләсе_элемент == 'r') Киләсе_элемент = '\r'; else if (Киләсе_элемент == 't') Киләсе_элемент = '\t';
                        else if (Киләсе_элемент == 'b') Киләсе_элемент = '\b'; else if (Киләсе_элемент == 'f') Киләсе_элемент = '\f';
                        else if (Киләсе_элемент != '"' && Киләсе_элемент != '\\' && Киләсе_элемент != '/') throw new IllegalArgumentException("문자 이스케이프 Хата");
                    }
                    үлчәм.append(Киләсе_элемент);
                }
            }
            int эшләтү = урнаштыру - 1;
            while (урнаштыру < чыганак.length() && ",]} \t\r\n".indexOf(чыганак.charAt(урнаштыру)) < 0) урнаштыру++;
            String VALUE = чыганак.substring(эшләтү, урнаштыру);
            if (VALUE.equals("true")) return Boolean.TRUE; if (VALUE.equals("false")) return Boolean.FALSE; if (VALUE.equals("null")) return null;
            return Double.valueOf(VALUE);
        }
    }
    static String Хәш_файл(Path Yul) throws Exception {
        MessageDigest 계산 = MessageDigest.getInstance("SHA-256"); byte[] мәгълүмат = new byte[1024 * 1024];
        try (InputStream 입력 = Files.newInputStream(Yul)) { for (int озынлык_VALUE; (озынлык_VALUE = 입력.read(мәгълүмат)) >= 0;) 계산.update(мәгълүмат,0,озынлык_VALUE); }
        return Хәш_СМС(계산.digest());
    }
    static String Хәш_СМС(byte[] мәгълүмат) {
        StringBuilder Mäten = new StringBuilder(); for (byte VALUE : мәгълүмат) Mäten.append(String.format(Locale.ROOT,"%02x",VALUE & 255)); return Mäten.toString();
    }
    static Path 내부경로(Path экранга_җибәрү_тамыр, String исем) {
        Path үлчәм = экранга_җибәрү_тамыр.resolve(исем).normalize();
        if (исем.isEmpty() || Paths.get(исем).isAbsolute() || !үлчәм.startsWith(экранга_җибәрү_тамыр) || исем.indexOf('\\') >= 0)
            throw new IllegalArgumentException("범위를 벗어난 Yul: " + исем);
        for (Path 부분 : Paths.get(исем)) if (부분.toString().equals("..")) throw new IllegalArgumentException("상위 Yul 금지: " + исем);
        for (Path 현재 = үлчәм; 현재 != null && 현재.startsWith(экранга_җибәрү_тамыр); 현재 = 현재.getParent())
            if (Files.isSymbolicLink(현재)) throw new IllegalArgumentException("의존성 경로의 링크 금지: " + исем);
        return үлчәм;
    }
    static String 명령출력(List<String> команда) throws Exception {
        Process Процесс_VALUE = new ProcessBuilder(команда).redirectError(ProcessBuilder.Redirect.INHERIT).start();
        String үлчәм = new String(Процесс_VALUE.getInputStream().readAllBytes(),StandardCharsets.UTF_8);
        if (Процесс_VALUE.waitFor() != 0) throw new IOException("команда эштән_туктау_VALUE: " + команда.get(0)); return үлчәм;
    }
    static void чыгарту(Path Архив_VALUE, Path күчерү_урыны_VALUE) throws Exception {
        for (String исем : 명령출력(Arrays.asList("tar","-tzf",Архив_VALUE.toString())).split("\n")) 내부경로(күчерү_урыны_VALUE, исем);
        for (String юл : 명령출력(Arrays.asList("tar","-tvzf",Архив_VALUE.toString())).split("\n"))
            if (!юл.isEmpty() && юл.charAt(0) != '-' && юл.charAt(0) != 'd') throw new IOException("외부 링크 또는 특수 파일을 포함한 의존성");
        Files.createDirectories(күчерү_урыны_VALUE);
        int халәт_VALUE = new ProcessBuilder("tar","--no-same-owner","--no-same-permissions","-xzf",Архив_VALUE.toString(),"-C",күчерү_урыны_VALUE.toString()).inheritIO().start().waitFor();
        if (халәт_VALUE != 0) throw new IOException("의존성 Архив_VALUE Чыгарылыш_Саклагыч эштән_туктау_VALUE");
    }
    static void 호출(Path 작업경로, Path Кораллар, List<String> 인수, Map<String,String> 환경) throws Exception {
        List<String> команда = new ArrayList<>(Arrays.asList("python3", Кораллар.toString())); команда.addAll(인수);
        ProcessBuilder үтәргә_команда = new ProcessBuilder(команда).directory(작업경로.toFile()).inheritIO(); үтәргә_команда.environment().putAll(환경);
        int халәт_VALUE = үтәргә_команда.start().waitFor(); if (халәт_VALUE != 0) throw new IOException("Кораллар эштән_туктау_VALUE: " + Кораллар + " (" + халәт_VALUE + ")");
    }
    @SuppressWarnings("unchecked")
    public static void main(String[] 인수) throws Exception {
        if (인수.length < 1) throw new IllegalArgumentException("build, run, desktop, image, check, test-system 중 동작을 지정하세요");
        String Гамәл = 인수[0];
        if (!Arrays.asList("build","run","desktop","image","check","test-system").contains(Гамәл)) throw new IllegalArgumentException("알 수 없는 Гамәл");
        Path экранга_җибәрү_тамыр = Paths.get(System.getProperty("worldos.edition.root")).toAbsolutePath().normalize();
        Map<String,Object> Caylaw = (Map<String,Object>)new 자료해석기(Files.readString(экранга_җибәрү_тамыр.resolve("native.json"),StandardCharsets.UTF_8)).읽기();
        Path чыганак_агач = 내부경로(экранга_җибәрү_тамыр,(String)Caylaw.get("source")), төш_VALUE = 내부경로(чыганак_агач,(String)Caylaw.get("native"));
        List<String> 소유파일들 = (List<String>)(List<?>)Caylaw.get("owned_files");
        for (String исем : 소유파일들) if (!Files.isRegularFile(내부경로(чыганак_агач,исем))) throw new IOException("чыганак_агач 없음: " + исем);
        if (Гамәл.equals("check")) { System.out.println(Caylaw.get("country") + " " + Caylaw.get("language") + " 독립 чыганак_агач раслау 완료"); return; }
        String 자원상대 = (String)Caylaw.getOrDefault("resource_root", ".");
        if (!자원상대.equals(".") && !자원상대.equals("..")) throw new IllegalArgumentException("의존성 экранга_җибәрү_тамыр Yul Хата");
        Path ресурс_VALUE = экранга_җибәрү_тамыр.resolve(자원상대).normalize(); Path Архив_VALUE = ресурс_VALUE.resolve("native-vendor.tar.gz");
        String 기대해시 = (String)Caylaw.get("vendor_sha256");
        if (!Хәш_файл(Архив_VALUE).equals(기대해시)) throw new IOException("의존성 SHA-256 불일치");
        Path 표식 = чыганак_агач.resolve(".vendor-sha256");
        if (!Files.isRegularFile(표식) || !Files.readString(표식).trim().equals(기대해시)) { чыгарту(Архив_VALUE, чыганак_агач); Files.writeString(표식,기대해시 + "\n"); }
        Map<String,String> 환경 = new HashMap<>(System.getenv());
        Path ipConfig = null;
        if (환경.containsKey("IP_CONFIG")) ipConfig = Paths.get(환경.get("IP_CONFIG")).toAbsolutePath().normalize();
        else for (Path parent = экранга_җибәрү_тамыр; parent != null; parent = parent.getParent()) {
            if (Files.isRegularFile(parent.resolve("ip.conf"))) { ipConfig = parent.resolve("ip.conf"); break; }
        }
        if (ipConfig == null) ipConfig = чыганак_агач.resolve("ip.conf");
        if (!Files.isRegularFile(ipConfig)) throw new IOException("Missing ip.conf: " + ipConfig);
        환경.put("IP_CONFIG", ipConfig.toString());
        if (Arrays.asList("run","desktop","test-system").contains(Гамәл) && !환경.containsKey("QEMU_AARCH64")) {
            Path кушымта_хезмәткәр = ресурс_VALUE.resolve("host/qemu"), 실행기표식 = ресурс_VALUE.resolve("host/.qemu-sha256");
            String хезмәткәр_Хәш = (String)Caylaw.get("qemu_sha256");
            if (!Files.isRegularFile(кушымта_хезмәткәр) || !Files.isRegularFile(실행기표식) || !Files.readString(실행기표식).trim().equals(хезмәткәр_Хәш)) {
                Path хезмәткәр_Архив = ресурс_VALUE.resolve("qemu-host.tar.gz"); if (!Хәш_файл(хезмәткәр_Архив).equals(хезмәткәр_Хәш)) throw new IOException("QEMU SHA-256 불일치");
                чыгарту(хезмәткәр_Архив,ресурс_VALUE.resolve("host")); Files.writeString(실행기표식,хезмәткәр_Хәш + "\n");
            }
            환경.put("QEMU_AARCH64",кушымта_хезмәткәр.toString());
        }
        MessageDigest 계산 = MessageDigest.getInstance("SHA-256"); Collections.sort(소유파일들);
        for (String исем : 소유파일들) { 계산.update(исем.getBytes(StandardCharsets.UTF_8)); 계산.update(Files.readAllBytes(내부경로(чыганак_агач,исем))); }
        계산.update("ip.conf\0".getBytes(StandardCharsets.UTF_8)); 계산.update(Files.readAllBytes(ipConfig));
        String чыганак_Хәш = Хәш_СМС(계산.digest()); Path 빌드표식 = төш_VALUE.resolve("build/worldos-source.sha256");
        if (Гамәл.equals("build") || !Files.isRegularFile(빌드표식) || !Files.readString(빌드표식).trim().equals(чыганак_Хәш)) {
            호출(төш_VALUE,내부경로(төш_VALUE,(String)Caylaw.get("builder")),Collections.emptyList(),환경);
            Files.writeString(빌드표식,чыганак_Хәш + "\n");
        }
        List<String> 추가인수 = new ArrayList<>(Arrays.asList(인수).subList(1,인수.length));
        if (Гамәл.equals("run") || Гамәл.equals("desktop")) {
            if (Гамәл.equals("desktop")) 추가인수.add(0,"--desktop");
            호출(төш_VALUE,내부경로(төш_VALUE,(String)Caylaw.get("runner")),추가인수,환경);
        } else if (Гамәл.equals("image")) 호출(төш_VALUE,내부경로(төш_VALUE,(String)Caylaw.get("image_builder")),추가인수,환경);
        else if (Гамәл.equals("test-system")) {
            추가인수.add(0,экранга_җибәрү_тамыр.toString()); 추가인수.add(0,"--edition");
            호출(төш_VALUE,내부경로(төш_VALUE,(String)Caylaw.get("system_tester")),추가인수,환경);
        }
    }
}
