// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.security.MessageDigest;
import java.util.*;

/** 독립 국가판의 의존성 검사·복원·градити_систем·실행을 맡는 хост Java Алатке. */
public final class 국가실행기 {
    static final class подаци_анализатор {
        final String ИЗВОР; int Положај;
        подаци_анализатор(String Текст) { ИЗВОР = Текст; }
        void 빈칸() { while (Положај < ИЗВОР.length() && Character.isWhitespace(ИЗВОР.charAt(Положај))) Положај++; }
        Object Чита() {
            빈칸(); char знак_вриједност = ИЗВОР.charAt(Положај++);
            if (знак_вриједност == '{') {
                Map<String,Object> ИСХОД = new LinkedHashMap<>(); 빈칸();
                if (ИЗВОР.charAt(Положај) == '}') { Положај++; return ИСХОД; }
                while (true) {
                    String Назив = (String)Чита(); 빈칸(); if (ИЗВОР.charAt(Положај++) != ':') throw new IllegalArgumentException("подаци граничник_вриједност ГРЕШКА");
                    ИСХОД.put(Назив, Чита()); 빈칸(); char граничник_вриједност = ИЗВОР.charAt(Положај++);
                    if (граничник_вриједност == '}') return ИСХОД; if (граничник_вриједност != ',') throw new IllegalArgumentException("подаци граничник_вриједност ГРЕШКА");
                }
            }
            if (знак_вриједност == '[') {
                List<Object> ИСХОД = new ArrayList<>(); 빈칸();
                if (ИЗВОР.charAt(Положај) == ']') { Положај++; return ИСХОД; }
                while (true) {
                    ИСХОД.add(Чита()); 빈칸(); char граничник_вриједност = ИЗВОР.charAt(Положај++);
                    if (граничник_вриједност == ']') return ИСХОД; if (граничник_вриједност != ',') throw new IllegalArgumentException("подаци граничник_вриједност ГРЕШКА");
                }
            }
            if (знак_вриједност == '"') {
                StringBuilder ИСХОД = new StringBuilder();
                while (true) {
                    char Даље_ставка = ИЗВОР.charAt(Положај++); if (Даље_ставка == '"') return ИСХОД.toString();
                    if (Даље_ставка == '\\') {
                        Даље_ставка = ИЗВОР.charAt(Положај++);
                        if (Даље_ставка == 'u') { ИСХОД.append((char)Integer.parseInt(ИЗВОР.substring(Положај, Положај + 4),16)); Положај += 4; continue; }
                        if (Даље_ставка == 'n') Даље_ставка = '\n'; else if (Даље_ставка == 'r') Даље_ставка = '\r'; else if (Даље_ставка == 't') Даље_ставка = '\t';
                        else if (Даље_ставка == 'b') Даље_ставка = '\b'; else if (Даље_ставка == 'f') Даље_ставка = '\f';
                        else if (Даље_ставка != '"' && Даље_ставка != '\\' && Даље_ставка != '/') throw new IllegalArgumentException("문자 이스케이프 ГРЕШКА");
                    }
                    ИСХОД.append(Даље_ставка);
                }
            }
            int Покрени = Положај - 1;
            while (Положај < ИЗВОР.length() && ",]} \t\r\n".indexOf(ИЗВОР.charAt(Положај)) < 0) Положај++;
            String вриједност = ИЗВОР.substring(Покрени, Положај);
            if (вриједност.equals("true")) return Boolean.TRUE; if (вриједност.equals("false")) return Boolean.FALSE; if (вриједност.equals("null")) return null;
            return Double.valueOf(вриједност);
        }
    }
    static String хеш_фајл(Path ПУТАЊА) throws Exception {
        MessageDigest 계산 = MessageDigest.getInstance("SHA-256"); byte[] подаци = new byte[1024 * 1024];
        try (InputStream 입력 = Files.newInputStream(ПУТАЊА)) { for (int дужина_вриједност; (дужина_вриједност = 입력.read(подаци)) >= 0;) 계산.update(подаци,0,дужина_вриједност); }
        return хеш_Текст(계산.digest());
    }
    static String хеш_Текст(byte[] подаци) {
        StringBuilder Текст = new StringBuilder(); for (byte вриједност : подаци) Текст.append(String.format(Locale.ROOT,"%02x",вриједност & 255)); return Текст.toString();
    }
    static Path 내부경로(Path пројектовати_корен, String Назив) {
        Path ИСХОД = пројектовати_корен.resolve(Назив).normalize();
        if (Назив.isEmpty() || Paths.get(Назив).isAbsolute() || !ИСХОД.startsWith(пројектовати_корен) || Назив.indexOf('\\') >= 0)
            throw new IllegalArgumentException("범위를 벗어난 ПУТАЊА: " + Назив);
        for (Path 부분 : Paths.get(Назив)) if (부분.toString().equals("..")) throw new IllegalArgumentException("상위 ПУТАЊА 금지: " + Назив);
        for (Path актуелно_ставка = ИСХОД; актуелно_ставка != null && актуелно_ставка.startsWith(пројектовати_корен); актуелно_ставка = актуелно_ставка.getParent())
            if (Files.isSymbolicLink(актуелно_ставка)) throw new IllegalArgumentException("의존성 경로의 링크 금지: " + Назив);
        return ИСХОД;
    }
    static String 명령출력(List<String> Наредба) throws Exception {
        Process Процес_вриједност = new ProcessBuilder(Наредба).redirectError(ProcessBuilder.Redirect.INHERIT).start();
        String ИСХОД = new String(Процес_вриједност.getInputStream().readAllBytes(),StandardCharsets.UTF_8);
        if (Процес_вриједност.waitFor() != 0) throw new IOException("Наредба неуспјех_вриједност: " + Наредба.get(0)); return ИСХОД;
    }
    static void издвојити(Path Архива_вриједност, Path одредиште_вриједност) throws Exception {
        for (String Назив : 명령출력(Arrays.asList("tar","-tzf",Архива_вриједност.toString())).split("\n")) 내부경로(одредиште_вриједност, Назив);
        for (String Ред : 명령출력(Arrays.asList("tar","-tvzf",Архива_вриједност.toString())).split("\n"))
            if (!Ред.isEmpty() && Ред.charAt(0) != '-' && Ред.charAt(0) != 'd') throw new IOException("екстерни_вриједност 링크 또는 특수 파일을 포함한 의존성");
        Files.createDirectories(одредиште_вриједност);
        int стање_вриједност = new ProcessBuilder("tar","--no-same-owner","--no-same-permissions","-xzf",Архива_вриједност.toString(),"-C",одредиште_вриједност.toString()).inheritIO().start().waitFor();
        if (стање_вриједност != 0) throw new IOException("의존성 Архива_вриједност издање_похрана неуспјех_вриједност");
    }
    static void 호출(Path 작업경로, Path Алатке, List<String> Аргументи, Map<String,String> радно_окружење) throws Exception {
        List<String> Наредба = new ArrayList<>(Arrays.asList("python3", Алатке.toString())); Наредба.addAll(Аргументи);
        ProcessBuilder Изврши_команда = new ProcessBuilder(Наредба).directory(작업경로.toFile()).inheritIO(); Изврши_команда.environment().putAll(радно_окружење);
        int стање_вриједност = Изврши_команда.start().waitFor(); if (стање_вриједност != 0) throw new IOException("Алатке неуспјех_вриједност: " + Алатке + " (" + стање_вриједност + ")");
    }
    @SuppressWarnings("unchecked")
    public static void main(String[] Аргументи) throws Exception {
        if (Аргументи.length < 1) throw new IllegalArgumentException("build, run, desktop, image, check, test-system 중 동작을 지정하세요");
        String радња = Аргументи[0];
        if (!Arrays.asList("build","run","desktop","image","check","test-system").contains(радња)) throw new IllegalArgumentException("알 수 없는 радња");
        Path пројектовати_корен = Paths.get(System.getProperty("worldos.edition.root")).toAbsolutePath().normalize();
        Map<String,Object> Поставке = (Map<String,Object>)new подаци_анализатор(Files.readString(пројектовати_корен.resolve("native.json"),StandardCharsets.UTF_8)).Чита();
        Path извор_стабло = 내부경로(пројектовати_корен,(String)Поставке.get("source")), језгро_вриједност = 내부경로(извор_стабло,(String)Поставке.get("native"));
        List<String> 소유파일들 = (List<String>)(List<?>)Поставке.get("owned_files");
        for (String Назив : 소유파일들) if (!Files.isRegularFile(내부경로(извор_стабло,Назив))) throw new IOException("извор_стабло 없음: " + Назив);
        if (радња.equals("check")) { System.out.println(Поставке.get("country") + " " + Поставке.get("language") + " 독립 извор_стабло потврдити 완료"); return; }
        String 자원상대 = (String)Поставке.getOrDefault("resource_root", ".");
        if (!자원상대.equals(".") && !자원상대.equals("..")) throw new IllegalArgumentException("의존성 пројектовати_корен ПУТАЊА ГРЕШКА");
        Path ресурс_вриједност = пројектовати_корен.resolve(자원상대).normalize(); Path Архива_вриједност = ресурс_вриједност.resolve("native-vendor.tar.gz");
        String 기대해시 = (String)Поставке.get("vendor_sha256");
        if (!хеш_фајл(Архива_вриједност).equals(기대해시)) throw new IOException("의존성 SHA-256 불일치");
        Path 표식 = извор_стабло.resolve(".vendor-sha256");
        if (!Files.isRegularFile(표식) || !Files.readString(표식).trim().equals(기대해시)) { издвојити(Архива_вриједност, извор_стабло); Files.writeString(표식,기대해시 + "\n"); }
        Map<String,String> радно_окружење = new HashMap<>(System.getenv());
        Path ipConfig = null;
        if (радно_окружење.containsKey("IP_CONFIG")) ipConfig = Paths.get(радно_окружење.get("IP_CONFIG")).toAbsolutePath().normalize();
        else for (Path parent = пројектовати_корен; parent != null; parent = parent.getParent()) {
            if (Files.isRegularFile(parent.resolve("ip.conf"))) { ipConfig = parent.resolve("ip.conf"); break; }
        }
        if (ipConfig == null) ipConfig = извор_стабло.resolve("ip.conf");
        if (!Files.isRegularFile(ipConfig)) throw new IOException("Missing ip.conf: " + ipConfig);
        радно_окружење.put("IP_CONFIG", ipConfig.toString());
        if (Arrays.asList("run","desktop","test-system").contains(радња) && !радно_окружење.containsKey("QEMU_AARCH64")) {
            Path програм_покретач = ресурс_вриједност.resolve("host/qemu"), 실행기표식 = ресурс_вриједност.resolve("host/.qemu-sha256");
            String покретач_хеш = (String)Поставке.get("qemu_sha256");
            if (!Files.isRegularFile(програм_покретач) || !Files.isRegularFile(실행기표식) || !Files.readString(실행기표식).trim().equals(покретач_хеш)) {
                Path покретач_Архива = ресурс_вриједност.resolve("qemu-host.tar.gz"); if (!хеш_фајл(покретач_Архива).equals(покретач_хеш)) throw new IOException("QEMU SHA-256 불일치");
                издвојити(покретач_Архива,ресурс_вриједност.resolve("host")); Files.writeString(실행기표식,покретач_хеш + "\n");
            }
            радно_окружење.put("QEMU_AARCH64",програм_покретач.toString());
        }
        MessageDigest 계산 = MessageDigest.getInstance("SHA-256"); Collections.sort(소유파일들);
        for (String Назив : 소유파일들) { 계산.update(Назив.getBytes(StandardCharsets.UTF_8)); 계산.update(Files.readAllBytes(내부경로(извор_стабло,Назив))); }
        계산.update("ip.conf\0".getBytes(StandardCharsets.UTF_8)); 계산.update(Files.readAllBytes(ipConfig));
        String извор_хеш = хеш_Текст(계산.digest()); Path 빌드표식 = језгро_вриједност.resolve("build/worldos-source.sha256");
        if (радња.equals("build") || !Files.isRegularFile(빌드표식) || !Files.readString(빌드표식).trim().equals(извор_хеш)) {
            호출(језгро_вриједност,내부경로(језгро_вриједност,(String)Поставке.get("builder")),Collections.emptyList(),радно_окружење);
            Files.writeString(빌드표식,извор_хеш + "\n");
        }
        List<String> 추가인수 = new ArrayList<>(Arrays.asList(Аргументи).subList(1,Аргументи.length));
        if (радња.equals("run") || радња.equals("desktop")) {
            if (радња.equals("desktop")) 추가인수.add(0,"--desktop");
            호출(језгро_вриједност,내부경로(језгро_вриједност,(String)Поставке.get("runner")),추가인수,радно_окружење);
        } else if (радња.equals("image")) 호출(језгро_вриједност,내부경로(језгро_вриједност,(String)Поставке.get("image_builder")),추가인수,радно_окружење);
        else if (радња.equals("test-system")) {
            추가인수.add(0,пројектовати_корен.toString()); 추가인수.add(0,"--edition");
            호출(језгро_вриједност,내부경로(језгро_вриједност,(String)Поставке.get("system_tester")),추가인수,радно_окружење);
        }
    }
}
