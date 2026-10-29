// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.security.MessageDigest;
import java.util.*;

/** 독립 국가판의 의존성 검사·복원·сборка·실행을 맡는 узел Java инструменты. */
public final class ЗапускСтраны {
    static final class данные_анализатор {
        final String исходныйКод; int позиция;
        данные_анализатор(String текст) { исходныйКод = текст; }
        void 빈칸() { while (позиция < исходныйКод.length() && Character.isWhitespace(исходныйКод.charAt(позиция))) позиция++; }
        Object Чтение() {
            빈칸(); char знак_ЗНАЧЕН = исходныйКод.charAt(позиция++);
            if (знак_ЗНАЧЕН == '{') {
                Map<String,Object> результат = new LinkedHashMap<>(); 빈칸();
                if (исходныйКод.charAt(позиция) == '}') { позиция++; return результат; }
                while (true) {
                    String Название = (String)Чтение(); 빈칸(); if (исходныйКод.charAt(позиция++) != ':') throw new IllegalArgumentException("данные разделитель_ЗНАЧЕН_d8ba4873 ошибка");
                    результат.put(Название, Чтение()); 빈칸(); char разделитель_ЗНАЧЕН_d8ba4873 = исходныйКод.charAt(позиция++);
                    if (разделитель_ЗНАЧЕН_d8ba4873 == '}') return результат; if (разделитель_ЗНАЧЕН_d8ba4873 != ',') throw new IllegalArgumentException("данные разделитель_ЗНАЧЕН_d8ba4873 ошибка");
                }
            }
            if (знак_ЗНАЧЕН == '[') {
                List<Object> результат = new ArrayList<>(); 빈칸();
                if (исходныйКод.charAt(позиция) == ']') { позиция++; return результат; }
                while (true) {
                    результат.add(Чтение()); 빈칸(); char разделитель_ЗНАЧЕН_d8ba4873 = исходныйКод.charAt(позиция++);
                    if (разделитель_ЗНАЧЕН_d8ba4873 == ']') return результат; if (разделитель_ЗНАЧЕН_d8ba4873 != ',') throw new IllegalArgumentException("данные разделитель_ЗНАЧЕН_d8ba4873 ошибка");
                }
            }
            if (знак_ЗНАЧЕН == '"') {
                StringBuilder результат = new StringBuilder();
                while (true) {
                    char Далее_товар = исходныйКод.charAt(позиция++); if (Далее_товар == '"') return результат.toString();
                    if (Далее_товар == '\\') {
                        Далее_товар = исходныйКод.charAt(позиция++);
                        if (Далее_товар == 'u') { результат.append((char)Integer.parseInt(исходныйКод.substring(позиция, позиция + 4),16)); позиция += 4; continue; }
                        if (Далее_товар == 'n') Далее_товар = '\n'; else if (Далее_товар == 'r') Далее_товар = '\r'; else if (Далее_товар == 't') Далее_товар = '\t';
                        else if (Далее_товар == 'b') Далее_товар = '\b'; else if (Далее_товар == 'f') Далее_товар = '\f';
                        else if (Далее_товар != '"' && Далее_товар != '\\' && Далее_товар != '/') throw new IllegalArgumentException("문자 이스케이프 ошибка");
                    }
                    результат.append(Далее_товар);
                }
            }
            int запустить = позиция - 1;
            while (позиция < исходныйКод.length() && ",]} \t\r\n".indexOf(исходныйКод.charAt(позиция)) < 0) позиция++;
            String ЗНАЧЕН = исходныйКод.substring(запустить, позиция);
            if (ЗНАЧЕН.equals("true")) return Boolean.TRUE; if (ЗНАЧЕН.equals("false")) return Boolean.FALSE; if (ЗНАЧЕН.equals("null")) return null;
            return Double.valueOf(ЗНАЧЕН);
        }
    }
    static String хэш_файл(Path путь) throws Exception {
        MessageDigest 계산 = MessageDigest.getInstance("SHA-256"); byte[] данные = new byte[1024 * 1024];
        try (InputStream входные_данные_ЗНАЧЕН = Files.newInputStream(путь)) { for (int длина_ЗНАЧЕН; (длина_ЗНАЧЕН = входные_данные_ЗНАЧЕН.read(данные)) >= 0;) 계산.update(данные,0,длина_ЗНАЧЕН); }
        return хэш_SMS(계산.digest());
    }
    static String хэш_SMS(byte[] данные) {
        StringBuilder текст = new StringBuilder(); for (byte ЗНАЧЕН : данные) текст.append(String.format(Locale.ROOT,"%02x",ЗНАЧЕН & 255)); return текст.toString();
    }
    static Path внутренний_путь(Path задача_корень, String Название) {
        Path результат = задача_корень.resolve(Название).normalize();
        if (Название.isEmpty() || Paths.get(Название).isAbsolute() || !результат.startsWith(задача_корень) || Название.indexOf('\\') >= 0)
            throw new IllegalArgumentException("범위를 벗어난 путь: " + Название);
        for (Path 부분 : Paths.get(Название)) if (부분.toString().equals("..")) throw new IllegalArgumentException("상위 путь 금지: " + Название);
        for (Path текущий_товар = результат; текущий_товар != null && текущий_товар.startsWith(задача_корень); текущий_товар = текущий_товар.getParent())
            if (Files.isSymbolicLink(текущий_товар)) throw new IllegalArgumentException("의존성 경로의 링크 금지: " + Название);
        return результат;
    }
    static String 명령출력(List<String> команда) throws Exception {
        Process Процесс_ЗНАЧЕН = new ProcessBuilder(команда).redirectError(ProcessBuilder.Redirect.INHERIT).start();
        String результат = new String(Процесс_ЗНАЧЕН.getInputStream().readAllBytes(),StandardCharsets.UTF_8);
        if (Процесс_ЗНАЧЕН.waitFor() != 0) throw new IOException("команда сбой_ЗНАЧЕН: " + команда.get(0)); return результат;
    }
    static void извлечь(Path Архив_ЗНАЧЕН, Path цель_ЗНАЧЕН) throws Exception {
        for (String Название : 명령출력(Arrays.asList("tar","-tzf",Архив_ЗНАЧЕН.toString())).split("\n")) внутренний_путь(цель_ЗНАЧЕН, Название);
        for (String строка_ввода : 명령출력(Arrays.asList("tar","-tvzf",Архив_ЗНАЧЕН.toString())).split("\n"))
            if (!строка_ввода.isEmpty() && строка_ввода.charAt(0) != '-' && строка_ввода.charAt(0) != 'd') throw new IOException("внешний_ЗНАЧЕН 링크 또는 특수 파일을 포함한 의존성");
        Files.createDirectories(цель_ЗНАЧЕН);
        int Состояние_ЗНАЧЕН = new ProcessBuilder("tar","--no-same-owner","--no-same-permissions","-xzf",Архив_ЗНАЧЕН.toString(),"-C",цель_ЗНАЧЕН.toString()).inheritIO().start().waitFor();
        if (Состояние_ЗНАЧЕН != 0) throw new IOException("의존성 Архив_ЗНАЧЕН выпуск_Память_293182ec сбой_ЗНАЧЕН");
    }
    static void 호출(Path 작업경로, Path инструменты, List<String> аргументы, Map<String,String> среда) throws Exception {
        List<String> команда = new ArrayList<>(Arrays.asList("python3", инструменты.toString())); команда.addAll(аргументы);
        ProcessBuilder 실행 = new ProcessBuilder(команда).directory(작업경로.toFile()).inheritIO(); 실행.environment().putAll(среда);
        int Состояние_ЗНАЧЕН = 실행.start().waitFor(); if (Состояние_ЗНАЧЕН != 0) throw new IOException("инструменты сбой_ЗНАЧЕН: " + инструменты + " (" + Состояние_ЗНАЧЕН + ")");
    }
    @SuppressWarnings("unchecked")
    public static void main(String[] аргументы) throws Exception {
        if (аргументы.length < 1) throw new IllegalArgumentException("build, run, desktop, image, check, test-system 중 동작을 지정하세요");
        String Действие = аргументы[0];
        if (!Arrays.asList("build","run","desktop","image","check","test-system").contains(Действие)) throw new IllegalArgumentException("알 수 없는 Действие");
        Path задача_корень = Paths.get(System.getProperty("worldos.edition.root")).toAbsolutePath().normalize();
        Map<String,Object> Настройки = (Map<String,Object>)new данные_анализатор(Files.readString(задача_корень.resolve("native.json"),StandardCharsets.UTF_8)).Чтение();
        Path источник_дерево = внутренний_путь(задача_корень,(String)Настройки.get("source")), ядро_ЗНАЧЕН = внутренний_путь(источник_дерево,(String)Настройки.get("native"));
        List<String> 소유파일들 = (List<String>)(List<?>)Настройки.get("owned_files");
        for (String Название : 소유파일들) if (!Files.isRegularFile(внутренний_путь(источник_дерево,Название))) throw new IOException("источник_дерево 없음: " + Название);
        if (Действие.equals("check")) { System.out.println(Настройки.get("country") + " " + Настройки.get("language") + " 독립 источник_дерево проверять 완료"); return; }
        String ресурс_относительный_путь = (String)Настройки.getOrDefault("resource_root", ".");
        if (!ресурс_относительный_путь.equals(".") && !ресурс_относительный_путь.equals("..")) throw new IllegalArgumentException("의존성 задача_корень путь ошибка");
        Path ресурс_ЗНАЧЕН = задача_корень.resolve(ресурс_относительный_путь).normalize(); Path Архив_ЗНАЧЕН = ресурс_ЗНАЧЕН.resolve("native-vendor.tar.gz");
        String 기대해시 = (String)Настройки.get("vendor_sha256");
        if (!хэш_файл(Архив_ЗНАЧЕН).equals(기대해시)) throw new IOException("의존성 SHA-256 불일치");
        Path метка_ЗНАЧЕН = источник_дерево.resolve(".vendor-sha256");
        if (!Files.isRegularFile(метка_ЗНАЧЕН) || !Files.readString(метка_ЗНАЧЕН).trim().equals(기대해시)) { извлечь(Архив_ЗНАЧЕН, источник_дерево); Files.writeString(метка_ЗНАЧЕН,기대해시 + "\n"); }
        Map<String,String> среда = new HashMap<>(System.getenv());
        Path ipConfig = null;
        if (среда.containsKey("IP_CONFIG")) ipConfig = Paths.get(среда.get("IP_CONFIG")).toAbsolutePath().normalize();
        else for (Path parent = задача_корень; parent != null; parent = parent.getParent()) {
            if (Files.isRegularFile(parent.resolve("ip.conf"))) { ipConfig = parent.resolve("ip.conf"); break; }
        }
        if (ipConfig == null) ipConfig = источник_дерево.resolve("ip.conf");
        if (!Files.isRegularFile(ipConfig)) throw new IOException("Missing ip.conf: " + ipConfig);
        среда.put("IP_CONFIG", ipConfig.toString());
        if (Arrays.asList("run","desktop","test-system").contains(Действие) && !среда.containsKey("QEMU_AARCH64")) {
            Path программа_Launcher = ресурс_ЗНАЧЕН.resolve("host/qemu"), Launcher_метка = ресурс_ЗНАЧЕН.resolve("host/.qemu-sha256");
            String Launcher_хэш = (String)Настройки.get("qemu_sha256");
            if (!Files.isRegularFile(программа_Launcher) || !Files.isRegularFile(Launcher_метка) || !Files.readString(Launcher_метка).trim().equals(Launcher_хэш)) {
                Path Launcher_Архив = ресурс_ЗНАЧЕН.resolve("qemu-host.tar.gz"); if (!хэш_файл(Launcher_Архив).equals(Launcher_хэш)) throw new IOException("QEMU SHA-256 불일치");
                извлечь(Launcher_Архив,ресурс_ЗНАЧЕН.resolve("host")); Files.writeString(Launcher_метка,Launcher_хэш + "\n");
            }
            среда.put("QEMU_AARCH64",программа_Launcher.toString());
        }
        MessageDigest 계산 = MessageDigest.getInstance("SHA-256"); Collections.sort(소유파일들);
        for (String Название : 소유파일들) { 계산.update(Название.getBytes(StandardCharsets.UTF_8)); 계산.update(Files.readAllBytes(внутренний_путь(источник_дерево,Название))); }
        계산.update("ip.conf\0".getBytes(StandardCharsets.UTF_8)); 계산.update(Files.readAllBytes(ipConfig));
        String источник_хэш = хэш_SMS(계산.digest()); Path BLD_метка = ядро_ЗНАЧЕН.resolve("build/worldos-source.sha256");
        if (Действие.equals("build") || !Files.isRegularFile(BLD_метка) || !Files.readString(BLD_метка).trim().equals(источник_хэш)) {
            호출(ядро_ЗНАЧЕН,внутренний_путь(ядро_ЗНАЧЕН,(String)Настройки.get("builder")),Collections.emptyList(),среда);
            Files.writeString(BLD_метка,источник_хэш + "\n");
        }
        List<String> 추가인수 = new ArrayList<>(Arrays.asList(аргументы).subList(1,аргументы.length));
        if (Действие.equals("run") || Действие.equals("desktop")) {
            if (Действие.equals("desktop")) 추가인수.add(0,"--desktop");
            호출(ядро_ЗНАЧЕН,внутренний_путь(ядро_ЗНАЧЕН,(String)Настройки.get("runner")),추가인수,среда);
        } else if (Действие.equals("image")) 호출(ядро_ЗНАЧЕН,внутренний_путь(ядро_ЗНАЧЕН,(String)Настройки.get("image_builder")),추가인수,среда);
        else if (Действие.equals("test-system")) {
            추가인수.add(0,задача_корень.toString()); 추가인수.add(0,"--edition");
            호출(ядро_ЗНАЧЕН,внутренний_путь(ядро_ЗНАЧЕН,(String)Настройки.get("system_tester")),추가인수,среда);
        }
    }
}
