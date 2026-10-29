// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.security.MessageDigest;
import java.util.*;

/** 독립 국가판의 의존성 검사·복원·верзија_систем·실행을 맡는 вдоми Java Алатки. */
public final class 국가실행기 {
    static final class податоци_анализатор {
        final String ИЗВОР; int Позиција;
        податоци_анализатор(String Текст) { ИЗВОР = Текст; }
        void 빈칸() { while (Позиција < ИЗВОР.length() && Character.isWhitespace(ИЗВОР.charAt(Позиција))) Позиција++; }
        Object Читај() {
            빈칸(); char знак_VALUE = ИЗВОР.charAt(Позиција++);
            if (знак_VALUE == '{') {
                Map<String,Object> мерка = new LinkedHashMap<>(); 빈칸();
                if (ИЗВОР.charAt(Позиција) == '}') { Позиција++; return мерка; }
                while (true) {
                    String Име = (String)Читај(); 빈칸(); if (ИЗВОР.charAt(Позиција++) != ':') throw new IllegalArgumentException("податоци разделник_VALUE_d8ba4873 ГРЕШКА");
                    мерка.put(Име, Читај()); 빈칸(); char разделник_VALUE_d8ba4873 = ИЗВОР.charAt(Позиција++);
                    if (разделник_VALUE_d8ba4873 == '}') return мерка; if (разделник_VALUE_d8ba4873 != ',') throw new IllegalArgumentException("податоци разделник_VALUE_d8ba4873 ГРЕШКА");
                }
            }
            if (знак_VALUE == '[') {
                List<Object> мерка = new ArrayList<>(); 빈칸();
                if (ИЗВОР.charAt(Позиција) == ']') { Позиција++; return мерка; }
                while (true) {
                    мерка.add(Читај()); 빈칸(); char разделник_VALUE_d8ba4873 = ИЗВОР.charAt(Позиција++);
                    if (разделник_VALUE_d8ba4873 == ']') return мерка; if (разделник_VALUE_d8ba4873 != ',') throw new IllegalArgumentException("податоци разделник_VALUE_d8ba4873 ГРЕШКА");
                }
            }
            if (знак_VALUE == '"') {
                StringBuilder мерка = new StringBuilder();
                while (true) {
                    char Следно_ставка = ИЗВОР.charAt(Позиција++); if (Следно_ставка == '"') return мерка.toString();
                    if (Следно_ставка == '\\') {
                        Следно_ставка = ИЗВОР.charAt(Позиција++);
                        if (Следно_ставка == 'u') { мерка.append((char)Integer.parseInt(ИЗВОР.substring(Позиција, Позиција + 4),16)); Позиција += 4; continue; }
                        if (Следно_ставка == 'n') Следно_ставка = '\n'; else if (Следно_ставка == 'r') Следно_ставка = '\r'; else if (Следно_ставка == 't') Следно_ставка = '\t';
                        else if (Следно_ставка == 'b') Следно_ставка = '\b'; else if (Следно_ставка == 'f') Следно_ставка = '\f';
                        else if (Следно_ставка != '"' && Следно_ставка != '\\' && Следно_ставка != '/') throw new IllegalArgumentException("문자 이스케이프 ГРЕШКА");
                    }
                    мерка.append(Следно_ставка);
                }
            }
            int Изврши_2 = Позиција - 1;
            while (Позиција < ИЗВОР.length() && ",]} \t\r\n".indexOf(ИЗВОР.charAt(Позиција)) < 0) Позиција++;
            String VALUE = ИЗВОР.substring(Изврши_2, Позиција);
            if (VALUE.equals("true")) return Boolean.TRUE; if (VALUE.equals("false")) return Boolean.FALSE; if (VALUE.equals("null")) return null;
            return Double.valueOf(VALUE);
        }
    }
    static String хаш_датотека(Path ПАТЕКА) throws Exception {
        MessageDigest 계산 = MessageDigest.getInstance("SHA-256"); byte[] податоци = new byte[1024 * 1024];
        try (InputStream 입력 = Files.newInputStream(ПАТЕКА)) { for (int должина_VALUE; (должина_VALUE = 입력.read(податоци)) >= 0;) 계산.update(податоци,0,должина_VALUE); }
        return хаш_СМС(계산.digest());
    }
    static String хаш_СМС(byte[] податоци) {
        StringBuilder Текст = new StringBuilder(); for (byte VALUE : податоци) Текст.append(String.format(Locale.ROOT,"%02x",VALUE & 255)); return Текст.toString();
    }
    static Path 내부경로(Path Project_корен, String Име) {
        Path мерка = Project_корен.resolve(Име).normalize();
        if (Име.isEmpty() || Paths.get(Име).isAbsolute() || !мерка.startsWith(Project_корен) || Име.indexOf('\\') >= 0)
            throw new IllegalArgumentException("범위를 벗어난 ПАТЕКА: " + Име);
        for (Path 부분 : Paths.get(Име)) if (부분.toString().equals("..")) throw new IllegalArgumentException("상위 ПАТЕКА 금지: " + Име);
        for (Path 현재 = мерка; 현재 != null && 현재.startsWith(Project_корен); 현재 = 현재.getParent())
            if (Files.isSymbolicLink(현재)) throw new IllegalArgumentException("의존성 경로의 링크 금지: " + Име);
        return мерка;
    }
    static String 명령출력(List<String> Команда) throws Exception {
        Process Процес_VALUE = new ProcessBuilder(Команда).redirectError(ProcessBuilder.Redirect.INHERIT).start();
        String мерка = new String(Процес_VALUE.getInputStream().readAllBytes(),StandardCharsets.UTF_8);
        if (Процес_VALUE.waitFor() != 0) throw new IOException("Команда неуспех_VALUE: " + Команда.get(0)); return мерка;
    }
    static void извлекува(Path Архива_VALUE, Path одредиште_VALUE) throws Exception {
        for (String Име : 명령출력(Arrays.asList("tar","-tzf",Архива_VALUE.toString())).split("\n")) 내부경로(одредиште_VALUE, Име);
        for (String ред : 명령출력(Arrays.asList("tar","-tvzf",Архива_VALUE.toString())).split("\n"))
            if (!ред.isEmpty() && ред.charAt(0) != '-' && ред.charAt(0) != 'd') throw new IOException("외부 링크 또는 특수 파일을 포함한 의존성");
        Files.createDirectories(одредиште_VALUE);
        int статус_VALUE = new ProcessBuilder("tar","--no-same-owner","--no-same-permissions","-xzf",Архива_VALUE.toString(),"-C",одредиште_VALUE.toString()).inheritIO().start().waitFor();
        if (статус_VALUE != 0) throw new IOException("의존성 Архива_VALUE издание_Склад неуспех_VALUE");
    }
    static void 호출(Path 작업경로, Path Алатки, List<String> Аргументи, Map<String,String> 환경) throws Exception {
        List<String> Команда = new ArrayList<>(Arrays.asList("python3", Алатки.toString())); Команда.addAll(Аргументи);
        ProcessBuilder Изврши_наредба = new ProcessBuilder(Команда).directory(작업경로.toFile()).inheritIO(); Изврши_наредба.environment().putAll(환경);
        int статус_VALUE = Изврши_наредба.start().waitFor(); if (статус_VALUE != 0) throw new IOException("Алатки неуспех_VALUE: " + Алатки + " (" + статус_VALUE + ")");
    }
    @SuppressWarnings("unchecked")
    public static void main(String[] Аргументи) throws Exception {
        if (Аргументи.length < 1) throw new IllegalArgumentException("build, run, desktop, image, check, test-system 중 동작을 지정하세요");
        String Дејство = Аргументи[0];
        if (!Arrays.asList("build","run","desktop","image","check","test-system").contains(Дејство)) throw new IllegalArgumentException("알 수 없는 Дејство");
        Path Project_корен = Paths.get(System.getProperty("worldos.edition.root")).toAbsolutePath().normalize();
        Map<String,Object> Подесувања = (Map<String,Object>)new податоци_анализатор(Files.readString(Project_корен.resolve("native.json"),StandardCharsets.UTF_8)).Читај();
        Path извор_дрво = 내부경로(Project_корен,(String)Подесувања.get("source")), јадро_VALUE = 내부경로(извор_дрво,(String)Подесувања.get("native"));
        List<String> 소유파일들 = (List<String>)(List<?>)Подесувања.get("owned_files");
        for (String Име : 소유파일들) if (!Files.isRegularFile(내부경로(извор_дрво,Име))) throw new IOException("извор_дрво 없음: " + Име);
        if (Дејство.equals("check")) { System.out.println(Подесувања.get("country") + " " + Подесувања.get("language") + " 독립 извор_дрво провери 완료"); return; }
        String 자원상대 = (String)Подесувања.getOrDefault("resource_root", ".");
        if (!자원상대.equals(".") && !자원상대.equals("..")) throw new IllegalArgumentException("의존성 Project_корен ПАТЕКА ГРЕШКА");
        Path извор_VALUE = Project_корен.resolve(자원상대).normalize(); Path Архива_VALUE = извор_VALUE.resolve("native-vendor.tar.gz");
        String 기대해시 = (String)Подесувања.get("vendor_sha256");
        if (!хаш_датотека(Архива_VALUE).equals(기대해시)) throw new IOException("의존성 SHA-256 불일치");
        Path 표식 = извор_дрво.resolve(".vendor-sha256");
        if (!Files.isRegularFile(표식) || !Files.readString(표식).trim().equals(기대해시)) { извлекува(Архива_VALUE, извор_дрво); Files.writeString(표식,기대해시 + "\n"); }
        Map<String,String> 환경 = new HashMap<>(System.getenv());
        Path ipConfig = null;
        if (환경.containsKey("IP_CONFIG")) ipConfig = Paths.get(환경.get("IP_CONFIG")).toAbsolutePath().normalize();
        else for (Path parent = Project_корен; parent != null; parent = parent.getParent()) {
            if (Files.isRegularFile(parent.resolve("ip.conf"))) { ipConfig = parent.resolve("ip.conf"); break; }
        }
        if (ipConfig == null) ipConfig = извор_дрво.resolve("ip.conf");
        if (!Files.isRegularFile(ipConfig)) throw new IOException("Missing ip.conf: " + ipConfig);
        환경.put("IP_CONFIG", ipConfig.toString());
        if (Arrays.asList("run","desktop","test-system").contains(Дејство) && !환경.containsKey("QEMU_AARCH64")) {
            Path програма_стартувач = извор_VALUE.resolve("host/qemu"), 실행기표식 = извор_VALUE.resolve("host/.qemu-sha256");
            String стартувач_хаш = (String)Подесувања.get("qemu_sha256");
            if (!Files.isRegularFile(програма_стартувач) || !Files.isRegularFile(실행기표식) || !Files.readString(실행기표식).trim().equals(стартувач_хаш)) {
                Path стартувач_Архива = извор_VALUE.resolve("qemu-host.tar.gz"); if (!хаш_датотека(стартувач_Архива).equals(стартувач_хаш)) throw new IOException("QEMU SHA-256 불일치");
                извлекува(стартувач_Архива,извор_VALUE.resolve("host")); Files.writeString(실행기표식,стартувач_хаш + "\n");
            }
            환경.put("QEMU_AARCH64",програма_стартувач.toString());
        }
        MessageDigest 계산 = MessageDigest.getInstance("SHA-256"); Collections.sort(소유파일들);
        for (String Име : 소유파일들) { 계산.update(Име.getBytes(StandardCharsets.UTF_8)); 계산.update(Files.readAllBytes(내부경로(извор_дрво,Име))); }
        계산.update("ip.conf\0".getBytes(StandardCharsets.UTF_8)); 계산.update(Files.readAllBytes(ipConfig));
        String извор_хаш = хаш_СМС(계산.digest()); Path 빌드표식 = јадро_VALUE.resolve("build/worldos-source.sha256");
        if (Дејство.equals("build") || !Files.isRegularFile(빌드표식) || !Files.readString(빌드표식).trim().equals(извор_хаш)) {
            호출(јадро_VALUE,내부경로(јадро_VALUE,(String)Подесувања.get("builder")),Collections.emptyList(),환경);
            Files.writeString(빌드표식,извор_хаш + "\n");
        }
        List<String> 추가인수 = new ArrayList<>(Arrays.asList(Аргументи).subList(1,Аргументи.length));
        if (Дејство.equals("run") || Дејство.equals("desktop")) {
            if (Дејство.equals("desktop")) 추가인수.add(0,"--desktop");
            호출(јадро_VALUE,내부경로(јадро_VALUE,(String)Подесувања.get("runner")),추가인수,환경);
        } else if (Дејство.equals("image")) 호출(јадро_VALUE,내부경로(јадро_VALUE,(String)Подесувања.get("image_builder")),추가인수,환경);
        else if (Дејство.equals("test-system")) {
            추가인수.add(0,Project_корен.toString()); 추가인수.add(0,"--edition");
            호출(јадро_VALUE,내부경로(јадро_VALUE,(String)Подесувања.get("system_tester")),추가인수,환경);
        }
    }
}
