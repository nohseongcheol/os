// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.security.MessageDigest;
import java.util.*;

/** 독립 국가판의 의존성 검사·복원·зборка_сістэма·실행을 맡는 вузел Java Інструменты. */
public final class 국가실행기 {
    static final class дадзеныя_аналізатар {
        final String КРЫНІЦА; int Пазіцыя;
        дадзеныя_аналізатар(String Тэкст) { КРЫНІЦА = Тэкст; }
        void 빈칸() { while (Пазіцыя < КРЫНІЦА.length() && Character.isWhitespace(КРЫНІЦА.charAt(Пазіцыя))) Пазіцыя++; }
        Object Чытанне() {
            빈칸(); char сімвал_значэнне_068c2631 = КРЫНІЦА.charAt(Пазіцыя++);
            if (сімвал_значэнне_068c2631 == '{') {
                Map<String,Object> 결과 = new LinkedHashMap<>(); 빈칸();
                if (КРЫНІЦА.charAt(Пазіцыя) == '}') { Пазіцыя++; return 결과; }
                while (true) {
                    String Назва = (String)Чытанне(); 빈칸(); if (КРЫНІЦА.charAt(Пазіцыя++) != ':') throw new IllegalArgumentException("дадзеныя раздзяляльнік_значэнне_d8ba4873 ПАМЫЛКА");
                    결과.put(Назва, Чытанне()); 빈칸(); char раздзяляльнік_значэнне_d8ba4873 = КРЫНІЦА.charAt(Пазіцыя++);
                    if (раздзяляльнік_значэнне_d8ba4873 == '}') return 결과; if (раздзяляльнік_значэнне_d8ba4873 != ',') throw new IllegalArgumentException("дадзеныя раздзяляльнік_значэнне_d8ba4873 ПАМЫЛКА");
                }
            }
            if (сімвал_значэнне_068c2631 == '[') {
                List<Object> 결과 = new ArrayList<>(); 빈칸();
                if (КРЫНІЦА.charAt(Пазіцыя) == ']') { Пазіцыя++; return 결과; }
                while (true) {
                    결과.add(Чытанне()); 빈칸(); char раздзяляльнік_значэнне_d8ba4873 = КРЫНІЦА.charAt(Пазіцыя++);
                    if (раздзяляльнік_значэнне_d8ba4873 == ']') return 결과; if (раздзяляльнік_значэнне_d8ba4873 != ',') throw new IllegalArgumentException("дадзеныя раздзяляльнік_значэнне_d8ba4873 ПАМЫЛКА");
                }
            }
            if (сімвал_значэнне_068c2631 == '"') {
                StringBuilder 결과 = new StringBuilder();
                while (true) {
                    char 다음 = КРЫНІЦА.charAt(Пазіцыя++); if (다음 == '"') return 결과.toString();
                    if (다음 == '\\') {
                        다음 = КРЫНІЦА.charAt(Пазіцыя++);
                        if (다음 == 'u') { 결과.append((char)Integer.parseInt(КРЫНІЦА.substring(Пазіцыя, Пазіцыя + 4),16)); Пазіцыя += 4; continue; }
                        if (다음 == 'n') 다음 = '\n'; else if (다음 == 'r') 다음 = '\r'; else if (다음 == 't') 다음 = '\t';
                        else if (다음 == 'b') 다음 = '\b'; else if (다음 == 'f') 다음 = '\f';
                        else if (다음 != '"' && 다음 != '\\' && 다음 != '/') throw new IllegalArgumentException("문자 이스케이프 ПАМЫЛКА");
                    }
                    결과.append(다음);
                }
            }
            int Выканаць = Пазіцыя - 1;
            while (Пазіцыя < КРЫНІЦА.length() && ",]} \t\r\n".indexOf(КРЫНІЦА.charAt(Пазіцыя)) < 0) Пазіцыя++;
            String значэнне = КРЫНІЦА.substring(Выканаць, Пазіцыя);
            if (значэнне.equals("true")) return Boolean.TRUE; if (значэнне.equals("false")) return Boolean.FALSE; if (значэнне.equals("null")) return null;
            return Double.valueOf(значэнне);
        }
    }
    static String хэш_файл(Path ШЛЯХ) throws Exception {
        MessageDigest 계산 = MessageDigest.getInstance("SHA-256"); byte[] дадзеныя = new byte[1024 * 1024];
        try (InputStream 입력 = Files.newInputStream(ШЛЯХ)) { for (int даўжыня_значэнне; (даўжыня_значэнне = 입력.read(дадзеныя)) >= 0;) 계산.update(дадзеныя,0,даўжыня_значэнне); }
        return хэш_Тэкст(계산.digest());
    }
    static String хэш_Тэкст(byte[] дадзеныя) {
        StringBuilder Тэкст = new StringBuilder(); for (byte значэнне : дадзеныя) Тэкст.append(String.format(Locale.ROOT,"%02x",значэнне & 255)); return Тэкст.toString();
    }
    static Path 내부경로(Path 기준, String Назва) {
        Path 결과 = 기준.resolve(Назва).normalize();
        if (Назва.isEmpty() || Paths.get(Назва).isAbsolute() || !결과.startsWith(기준) || Назва.indexOf('\\') >= 0)
            throw new IllegalArgumentException("범위를 벗어난 ШЛЯХ: " + Назва);
        for (Path 부분 : Paths.get(Назва)) if (부분.toString().equals("..")) throw new IllegalArgumentException("상위 ШЛЯХ 금지: " + Назва);
        for (Path 현재 = 결과; 현재 != null && 현재.startsWith(기준); 현재 = 현재.getParent())
            if (Files.isSymbolicLink(현재)) throw new IllegalArgumentException("의존성 경로의 링크 금지: " + Назва);
        return 결과;
    }
    static String 명령출력(List<String> Загад) throws Exception {
        Process Працэс_значэнне = new ProcessBuilder(Загад).redirectError(ProcessBuilder.Redirect.INHERIT).start();
        String 결과 = new String(Працэс_значэнне.getInputStream().readAllBytes(),StandardCharsets.UTF_8);
        if (Працэс_значэнне.waitFor() != 0) throw new IOException("Загад няўдача_значэнне: " + Загад.get(0)); return 결과;
    }
    static void выняць(Path Архіў_значэнне, Path прызначэнне_значэнне_a0fbc067) throws Exception {
        for (String Назва : 명령출력(Arrays.asList("tar","-tzf",Архіў_значэнне.toString())).split("\n")) 내부경로(прызначэнне_значэнне_a0fbc067, Назва);
        for (String лінія : 명령출력(Arrays.asList("tar","-tvzf",Архіў_значэнне.toString())).split("\n"))
            if (!лінія.isEmpty() && лінія.charAt(0) != '-' && лінія.charAt(0) != 'd') throw new IOException("외부 링크 또는 특수 파일을 포함한 의존성");
        Files.createDirectories(прызначэнне_значэнне_a0fbc067);
        int стан_значэнне = new ProcessBuilder("tar","--no-same-owner","--no-same-permissions","-xzf",Архіў_значэнне.toString(),"-C",прызначэнне_значэнне_a0fbc067.toString()).inheritIO().start().waitFor();
        if (стан_значэнне != 0) throw new IOException("의존성 Архіў_значэнне выпуск_Сховішча няўдача_значэнне");
    }
    static void 호출(Path 작업경로, Path Інструменты, List<String> 인수, Map<String,String> 환경) throws Exception {
        List<String> Загад = new ArrayList<>(Arrays.asList("python3", Інструменты.toString())); Загад.addAll(인수);
        ProcessBuilder выканаць_каманда = new ProcessBuilder(Загад).directory(작업경로.toFile()).inheritIO(); выканаць_каманда.environment().putAll(환경);
        int стан_значэнне = выканаць_каманда.start().waitFor(); if (стан_значэнне != 0) throw new IOException("Інструменты няўдача_значэнне: " + Інструменты + " (" + стан_значэнне + ")");
    }
    @SuppressWarnings("unchecked")
    public static void main(String[] 인수) throws Exception {
        if (인수.length < 1) throw new IllegalArgumentException("build, run, desktop, image, check, test-system 중 동작을 지정하세요");
        String Дзеянне = 인수[0];
        if (!Arrays.asList("build","run","desktop","image","check","test-system").contains(Дзеянне)) throw new IllegalArgumentException("알 수 없는 Дзеянне");
        Path 기준 = Paths.get(System.getProperty("worldos.edition.root")).toAbsolutePath().normalize();
        Map<String,Object> Усталёўкі = (Map<String,Object>)new дадзеныя_аналізатар(Files.readString(기준.resolve("native.json"),StandardCharsets.UTF_8)).Чытанне();
        Path крыніца_дрэва = 내부경로(기준,(String)Усталёўкі.get("source")), ядро_значэнне = 내부경로(крыніца_дрэва,(String)Усталёўкі.get("native"));
        List<String> 소유파일들 = (List<String>)(List<?>)Усталёўкі.get("owned_files");
        for (String Назва : 소유파일들) if (!Files.isRegularFile(내부경로(крыніца_дрэва,Назва))) throw new IOException("крыніца_дрэва 없음: " + Назва);
        if (Дзеянне.equals("check")) { System.out.println(Усталёўкі.get("country") + " " + Усталёўкі.get("language") + " 독립 крыніца_дрэва праверыць 완료"); return; }
        String 자원상대 = (String)Усталёўкі.getOrDefault("resource_root", ".");
        if (!자원상대.equals(".") && !자원상대.equals("..")) throw new IllegalArgumentException("의존성 기준 ШЛЯХ ПАМЫЛКА");
        Path рэсурс_значэнне = 기준.resolve(자원상대).normalize(); Path Архіў_значэнне = рэсурс_значэнне.resolve("native-vendor.tar.gz");
        String 기대해시 = (String)Усталёўкі.get("vendor_sha256");
        if (!хэш_файл(Архіў_значэнне).equals(기대해시)) throw new IOException("의존성 SHA-256 불일치");
        Path 표식 = крыніца_дрэва.resolve(".vendor-sha256");
        if (!Files.isRegularFile(표식) || !Files.readString(표식).trim().equals(기대해시)) { выняць(Архіў_значэнне, крыніца_дрэва); Files.writeString(표식,기대해시 + "\n"); }
        Map<String,String> 환경 = new HashMap<>(System.getenv());
        Path ipConfig = null;
        if (환경.containsKey("IP_CONFIG")) ipConfig = Paths.get(환경.get("IP_CONFIG")).toAbsolutePath().normalize();
        else for (Path parent = 기준; parent != null; parent = parent.getParent()) {
            if (Files.isRegularFile(parent.resolve("ip.conf"))) { ipConfig = parent.resolve("ip.conf"); break; }
        }
        if (ipConfig == null) ipConfig = крыніца_дрэва.resolve("ip.conf");
        if (!Files.isRegularFile(ipConfig)) throw new IOException("Missing ip.conf: " + ipConfig);
        환경.put("IP_CONFIG", ipConfig.toString());
        if (Arrays.asList("run","desktop","test-system").contains(Дзеянне) && !환경.containsKey("QEMU_AARCH64")) {
            Path праграма_выклік_праграм = рэсурс_значэнне.resolve("host/qemu"), 실행기표식 = рэсурс_значэнне.resolve("host/.qemu-sha256");
            String выклік_праграм_хэш = (String)Усталёўкі.get("qemu_sha256");
            if (!Files.isRegularFile(праграма_выклік_праграм) || !Files.isRegularFile(실행기표식) || !Files.readString(실행기표식).trim().equals(выклік_праграм_хэш)) {
                Path выклік_праграм_Архіў = рэсурс_значэнне.resolve("qemu-host.tar.gz"); if (!хэш_файл(выклік_праграм_Архіў).equals(выклік_праграм_хэш)) throw new IOException("QEMU SHA-256 불일치");
                выняць(выклік_праграм_Архіў,рэсурс_значэнне.resolve("host")); Files.writeString(실행기표식,выклік_праграм_хэш + "\n");
            }
            환경.put("QEMU_AARCH64",праграма_выклік_праграм.toString());
        }
        MessageDigest 계산 = MessageDigest.getInstance("SHA-256"); Collections.sort(소유파일들);
        for (String Назва : 소유파일들) { 계산.update(Назва.getBytes(StandardCharsets.UTF_8)); 계산.update(Files.readAllBytes(내부경로(крыніца_дрэва,Назва))); }
        계산.update("ip.conf\0".getBytes(StandardCharsets.UTF_8)); 계산.update(Files.readAllBytes(ipConfig));
        String крыніца_хэш = хэш_Тэкст(계산.digest()); Path 빌드표식 = ядро_значэнне.resolve("build/worldos-source.sha256");
        if (Дзеянне.equals("build") || !Files.isRegularFile(빌드표식) || !Files.readString(빌드표식).trim().equals(крыніца_хэш)) {
            호출(ядро_значэнне,내부경로(ядро_значэнне,(String)Усталёўкі.get("builder")),Collections.emptyList(),환경);
            Files.writeString(빌드표식,крыніца_хэш + "\n");
        }
        List<String> 추가인수 = new ArrayList<>(Arrays.asList(인수).subList(1,인수.length));
        if (Дзеянне.equals("run") || Дзеянне.equals("desktop")) {
            if (Дзеянне.equals("desktop")) 추가인수.add(0,"--desktop");
            호출(ядро_значэнне,내부경로(ядро_значэнне,(String)Усталёўкі.get("runner")),추가인수,환경);
        } else if (Дзеянне.equals("image")) 호출(ядро_значэнне,내부경로(ядро_значэнне,(String)Усталёўкі.get("image_builder")),추가인수,환경);
        else if (Дзеянне.equals("test-system")) {
            추가인수.add(0,기준.toString()); 추가인수.add(0,"--edition");
            호출(ядро_значэнне,내부경로(ядро_значэнне,(String)Усталёўкі.get("system_tester")),추가인수,환경);
        }
    }
}
