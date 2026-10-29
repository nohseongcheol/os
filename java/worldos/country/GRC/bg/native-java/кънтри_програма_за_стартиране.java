// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.security.MessageDigest;
import java.util.*;

/** 독립 국가판의 의존성 검사·복원·компилация_система·실행을 맡는 хост Java Инструменти. */
public final class кънтри_програма_за_стартиране {
    static final class данни_анализатор {
        final String ИЗТОЧНИК; int Позиция;
        данни_анализатор(String Текст) { ИЗТОЧНИК = Текст; }
        void 빈칸() { while (Позиция < ИЗТОЧНИК.length() && Character.isWhitespace(ИЗТОЧНИК.charAt(Позиция))) Позиция++; }
        Object Четене() {
            빈칸(); char знак_стойност = ИЗТОЧНИК.charAt(Позиция++);
            if (знак_стойност == '{') {
                Map<String,Object> РЕЗУЛТАТ = new LinkedHashMap<>(); 빈칸();
                if (ИЗТОЧНИК.charAt(Позиция) == '}') { Позиция++; return РЕЗУЛТАТ; }
                while (true) {
                    String Име = (String)Четене(); 빈칸(); if (ИЗТОЧНИК.charAt(Позиция++) != ':') throw new IllegalArgumentException("данни разделител_стойност_d8ba4873 ГРЕШКА");
                    РЕЗУЛТАТ.put(Име, Четене()); 빈칸(); char разделител_стойност_d8ba4873 = ИЗТОЧНИК.charAt(Позиция++);
                    if (разделител_стойност_d8ba4873 == '}') return РЕЗУЛТАТ; if (разделител_стойност_d8ba4873 != ',') throw new IllegalArgumentException("данни разделител_стойност_d8ba4873 ГРЕШКА");
                }
            }
            if (знак_стойност == '[') {
                List<Object> РЕЗУЛТАТ = new ArrayList<>(); 빈칸();
                if (ИЗТОЧНИК.charAt(Позиция) == ']') { Позиция++; return РЕЗУЛТАТ; }
                while (true) {
                    РЕЗУЛТАТ.add(Четене()); 빈칸(); char разделител_стойност_d8ba4873 = ИЗТОЧНИК.charAt(Позиция++);
                    if (разделител_стойност_d8ba4873 == ']') return РЕЗУЛТАТ; if (разделител_стойност_d8ba4873 != ',') throw new IllegalArgumentException("данни разделител_стойност_d8ba4873 ГРЕШКА");
                }
            }
            if (знак_стойност == '"') {
                StringBuilder РЕЗУЛТАТ = new StringBuilder();
                while (true) {
                    char Следваща_артикул = ИЗТОЧНИК.charAt(Позиция++); if (Следваща_артикул == '"') return РЕЗУЛТАТ.toString();
                    if (Следваща_артикул == '\\') {
                        Следваща_артикул = ИЗТОЧНИК.charAt(Позиция++);
                        if (Следваща_артикул == 'u') { РЕЗУЛТАТ.append((char)Integer.parseInt(ИЗТОЧНИК.substring(Позиция, Позиция + 4),16)); Позиция += 4; continue; }
                        if (Следваща_артикул == 'n') Следваща_артикул = '\n'; else if (Следваща_артикул == 'r') Следваща_артикул = '\r'; else if (Следваща_артикул == 't') Следваща_артикул = '\t';
                        else if (Следваща_артикул == 'b') Следваща_артикул = '\b'; else if (Следваща_артикул == 'f') Следваща_артикул = '\f';
                        else if (Следваща_артикул != '"' && Следваща_артикул != '\\' && Следваща_артикул != '/') throw new IllegalArgumentException("문자 이스케이프 ГРЕШКА");
                    }
                    РЕЗУЛТАТ.append(Следваща_артикул);
                }
            }
            int Стартиране = Позиция - 1;
            while (Позиция < ИЗТОЧНИК.length() && ",]} \t\r\n".indexOf(ИЗТОЧНИК.charAt(Позиция)) < 0) Позиция++;
            String стойност = ИЗТОЧНИК.substring(Стартиране, Позиция);
            if (стойност.equals("true")) return Boolean.TRUE; if (стойност.equals("false")) return Boolean.FALSE; if (стойност.equals("null")) return null;
            return Double.valueOf(стойност);
        }
    }
    static String хеширане_Файл(Path ПЪТ) throws Exception {
        MessageDigest 계산 = MessageDigest.getInstance("SHA-256"); byte[] данни = new byte[1024 * 1024];
        try (InputStream 입력 = Files.newInputStream(ПЪТ)) { for (int 길이; (길이 = 입력.read(данни)) >= 0;) 계산.update(данни,0,길이); }
        return хеширане_Текст(계산.digest());
    }
    static String хеширане_Текст(byte[] данни) {
        StringBuilder Текст = new StringBuilder(); for (byte стойност : данни) Текст.append(String.format(Locale.ROOT,"%02x",стойност & 255)); return Текст.toString();
    }
    static Path вътрешен_път(Path проект_корен, String Име) {
        Path РЕЗУЛТАТ = проект_корен.resolve(Име).normalize();
        if (Име.isEmpty() || Paths.get(Име).isAbsolute() || !РЕЗУЛТАТ.startsWith(проект_корен) || Име.indexOf('\\') >= 0)
            throw new IllegalArgumentException("범위를 벗어난 ПЪТ: " + Име);
        for (Path 부분 : Paths.get(Име)) if (부분.toString().equals("..")) throw new IllegalArgumentException("상위 ПЪТ 금지: " + Име);
        for (Path в_срок_артикул = РЕЗУЛТАТ; в_срок_артикул != null && в_срок_артикул.startsWith(проект_корен); в_срок_артикул = в_срок_артикул.getParent())
            if (Files.isSymbolicLink(в_срок_артикул)) throw new IllegalArgumentException("의존성 경로의 링크 금지: " + Име);
        return РЕЗУЛТАТ;
    }
    static String 명령출력(List<String> Команда) throws Exception {
        Process Процес_стойност = new ProcessBuilder(Команда).redirectError(ProcessBuilder.Redirect.INHERIT).start();
        String РЕЗУЛТАТ = new String(Процес_стойност.getInputStream().readAllBytes(),StandardCharsets.UTF_8);
        if (Процес_стойност.waitFor() != 0) throw new IOException("Команда отказ_стойност: " + Команда.get(0)); return РЕЗУЛТАТ;
    }
    static void извличам(Path Архив_стойност, Path местоназначение_стойност) throws Exception {
        for (String Име : 명령출력(Arrays.asList("tar","-tzf",Архив_стойност.toString())).split("\n")) вътрешен_път(местоназначение_стойност, Име);
        for (String ред : 명령출력(Arrays.asList("tar","-tvzf",Архив_стойност.toString())).split("\n"))
            if (!ред.isEmpty() && ред.charAt(0) != '-' && ред.charAt(0) != 'd') throw new IOException("външен_стойност 링크 또는 특수 파일을 포함한 의존성");
        Files.createDirectories(местоназначение_стойност);
        int Състояние_стойност = new ProcessBuilder("tar","--no-same-owner","--no-same-permissions","-xzf",Архив_стойност.toString(),"-C",местоназначение_стойност.toString()).inheritIO().start().waitFor();
        if (Състояние_стойност != 0) throw new IOException("의존성 Архив_стойност издание_Памет отказ_стойност");
    }
    static void 호출(Path 작업경로, Path Инструменти, List<String> Параметри, Map<String,String> 환경) throws Exception {
        List<String> Команда = new ArrayList<>(Arrays.asList("python3", Инструменти.toString())); Команда.addAll(Параметри);
        ProcessBuilder изпълнявам_команда = new ProcessBuilder(Команда).directory(작업경로.toFile()).inheritIO(); изпълнявам_команда.environment().putAll(환경);
        int Състояние_стойност = изпълнявам_команда.start().waitFor(); if (Състояние_стойност != 0) throw new IOException("Инструменти отказ_стойност: " + Инструменти + " (" + Състояние_стойност + ")");
    }
    @SuppressWarnings("unchecked")
    public static void main(String[] Параметри) throws Exception {
        if (Параметри.length < 1) throw new IllegalArgumentException("build, run, desktop, image, check, test-system 중 동작을 지정하세요");
        String Операция = Параметри[0];
        if (!Arrays.asList("build","run","desktop","image","check","test-system").contains(Операция)) throw new IllegalArgumentException("알 수 없는 Операция");
        Path проект_корен = Paths.get(System.getProperty("worldos.edition.root")).toAbsolutePath().normalize();
        Map<String,Object> Настройки = (Map<String,Object>)new данни_анализатор(Files.readString(проект_корен.resolve("native.json"),StandardCharsets.UTF_8)).Четене();
        Path източник_дърво = вътрешен_път(проект_корен,(String)Настройки.get("source")), ядро_стойност = вътрешен_път(източник_дърво,(String)Настройки.get("native"));
        List<String> 소유파일들 = (List<String>)(List<?>)Настройки.get("owned_files");
        for (String Име : 소유파일들) if (!Files.isRegularFile(вътрешен_път(източник_дърво,Име))) throw new IOException("източник_дърво 없음: " + Име);
        if (Операция.equals("check")) { System.out.println(Настройки.get("country") + " " + Настройки.get("language") + " 독립 източник_дърво проверявам 완료"); return; }
        String ресурс_относителен_път = (String)Настройки.getOrDefault("resource_root", ".");
        if (!ресурс_относителен_път.equals(".") && !ресурс_относителен_път.equals("..")) throw new IllegalArgumentException("의존성 проект_корен ПЪТ ГРЕШКА");
        Path ресурс_стойност = проект_корен.resolve(ресурс_относителен_път).normalize(); Path Архив_стойност = ресурс_стойност.resolve("native-vendor.tar.gz");
        String 기대해시 = (String)Настройки.get("vendor_sha256");
        if (!хеширане_Файл(Архив_стойност).equals(기대해시)) throw new IOException("의존성 SHA-256 불일치");
        Path маркер_стойност = източник_дърво.resolve(".vendor-sha256");
        if (!Files.isRegularFile(маркер_стойност) || !Files.readString(маркер_стойност).trim().equals(기대해시)) { извличам(Архив_стойност, източник_дърво); Files.writeString(маркер_стойност,기대해시 + "\n"); }
        Map<String,String> 환경 = new HashMap<>(System.getenv());
        Path ipConfig = null;
        if (환경.containsKey("IP_CONFIG")) ipConfig = Paths.get(환경.get("IP_CONFIG")).toAbsolutePath().normalize();
        else for (Path parent = проект_корен; parent != null; parent = parent.getParent()) {
            if (Files.isRegularFile(parent.resolve("ip.conf"))) { ipConfig = parent.resolve("ip.conf"); break; }
        }
        if (ipConfig == null) ipConfig = източник_дърво.resolve("ip.conf");
        if (!Files.isRegularFile(ipConfig)) throw new IOException("Missing ip.conf: " + ipConfig);
        환경.put("IP_CONFIG", ipConfig.toString());
        if (Arrays.asList("run","desktop","test-system").contains(Операция) && !환경.containsKey("QEMU_AARCH64")) {
            Path програма_програма_за_стартиране = ресурс_стойност.resolve("host/qemu"), програма_за_стартиране_маркер = ресурс_стойност.resolve("host/.qemu-sha256");
            String програма_за_стартиране_хеширане = (String)Настройки.get("qemu_sha256");
            if (!Files.isRegularFile(програма_програма_за_стартиране) || !Files.isRegularFile(програма_за_стартиране_маркер) || !Files.readString(програма_за_стартиране_маркер).trim().equals(програма_за_стартиране_хеширане)) {
                Path програма_за_стартиране_Архив = ресурс_стойност.resolve("qemu-host.tar.gz"); if (!хеширане_Файл(програма_за_стартиране_Архив).equals(програма_за_стартиране_хеширане)) throw new IOException("QEMU SHA-256 불일치");
                извличам(програма_за_стартиране_Архив,ресурс_стойност.resolve("host")); Files.writeString(програма_за_стартиране_маркер,програма_за_стартиране_хеширане + "\n");
            }
            환경.put("QEMU_AARCH64",програма_програма_за_стартиране.toString());
        }
        MessageDigest 계산 = MessageDigest.getInstance("SHA-256"); Collections.sort(소유파일들);
        for (String Име : 소유파일들) { 계산.update(Име.getBytes(StandardCharsets.UTF_8)); 계산.update(Files.readAllBytes(вътрешен_път(източник_дърво,Име))); }
        계산.update("ip.conf\0".getBytes(StandardCharsets.UTF_8)); 계산.update(Files.readAllBytes(ipConfig));
        String източник_хеширане = хеширане_Текст(계산.digest()); Path компилация_маркер = ядро_стойност.resolve("build/worldos-source.sha256");
        if (Операция.equals("build") || !Files.isRegularFile(компилация_маркер) || !Files.readString(компилация_маркер).trim().equals(източник_хеширане)) {
            호출(ядро_стойност,вътрешен_път(ядро_стойност,(String)Настройки.get("builder")),Collections.emptyList(),환경);
            Files.writeString(компилация_маркер,източник_хеширане + "\n");
        }
        List<String> 추가인수 = new ArrayList<>(Arrays.asList(Параметри).subList(1,Параметри.length));
        if (Операция.equals("run") || Операция.equals("desktop")) {
            if (Операция.equals("desktop")) 추가인수.add(0,"--desktop");
            호출(ядро_стойност,вътрешен_път(ядро_стойност,(String)Настройки.get("runner")),추가인수,환경);
        } else if (Операция.equals("image")) 호출(ядро_стойност,вътрешен_път(ядро_стойност,(String)Настройки.get("image_builder")),추가인수,환경);
        else if (Операция.equals("test-system")) {
            추가인수.add(0,проект_корен.toString()); 추가인수.add(0,"--edition");
            호출(ядро_стойност,вътрешен_път(ядро_стойност,(String)Настройки.get("system_tester")),추가인수,환경);
        }
    }
}
