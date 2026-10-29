// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.security.MessageDigest;
import java.util.*;

/** 독립 국가판의 의존성 검사·복원·курам_тутум·실행을 맡는 кабылдоо Java Куралдар. */
public final class 국가실행기 {
    static final class 자료해석기 {
        final String Булак; int Турган_жери;
        자료해석기(String Текст) { Булак = Текст; }
        void 빈칸() { while (Турган_жери < Булак.length() && Character.isWhitespace(Булак.charAt(Турган_жери))) Турган_жери++; }
        Object Окуу() {
            빈칸(); char символ_маани_068c2631 = Булак.charAt(Турган_жери++);
            if (символ_маани_068c2631 == '{') {
                Map<String,Object> 결과 = new LinkedHashMap<>(); 빈칸();
                if (Булак.charAt(Турган_жери) == '}') { Турган_жери++; return 결과; }
                while (true) {
                    String Аты = (String)Окуу(); 빈칸(); if (Булак.charAt(Турган_жери++) != ':') throw new IllegalArgumentException("берилмелер бөлгүч_маани Ката");
                    결과.put(Аты, Окуу()); 빈칸(); char бөлгүч_маани = Булак.charAt(Турган_жери++);
                    if (бөлгүч_маани == '}') return 결과; if (бөлгүч_маани != ',') throw new IllegalArgumentException("берилмелер бөлгүч_маани Ката");
                }
            }
            if (символ_маани_068c2631 == '[') {
                List<Object> 결과 = new ArrayList<>(); 빈칸();
                if (Булак.charAt(Турган_жери) == ']') { Турган_жери++; return 결과; }
                while (true) {
                    결과.add(Окуу()); 빈칸(); char бөлгүч_маани = Булак.charAt(Турган_жери++);
                    if (бөлгүч_маани == ']') return 결과; if (бөлгүч_маани != ',') throw new IllegalArgumentException("берилмелер бөлгүч_маани Ката");
                }
            }
            if (символ_маани_068c2631 == '"') {
                StringBuilder 결과 = new StringBuilder();
                while (true) {
                    char 다음 = Булак.charAt(Турган_жери++); if (다음 == '"') return 결과.toString();
                    if (다음 == '\\') {
                        다음 = Булак.charAt(Турган_жери++);
                        if (다음 == 'u') { 결과.append((char)Integer.parseInt(Булак.substring(Турган_жери, Турган_жери + 4),16)); Турган_жери += 4; continue; }
                        if (다음 == 'n') 다음 = '\n'; else if (다음 == 'r') 다음 = '\r'; else if (다음 == 't') 다음 = '\t';
                        else if (다음 == 'b') 다음 = '\b'; else if (다음 == 'f') 다음 = '\f';
                        else if (다음 != '"' && 다음 != '\\' && 다음 != '/') throw new IllegalArgumentException("문자 이스케이프 Ката");
                    }
                    결과.append(다음);
                }
            }
            int Жүргүзүү = Турган_жери - 1;
            while (Турган_жери < Булак.length() && ",]} \t\r\n".indexOf(Булак.charAt(Турган_жери)) < 0) Турган_жери++;
            String маани = Булак.substring(Жүргүзүү, Турган_жери);
            if (маани.equals("true")) return Boolean.TRUE; if (маани.equals("false")) return Boolean.FALSE; if (маани.equals("null")) return null;
            return Double.valueOf(маани);
        }
    }
    static String хэш_файл(Path ЖОЛ) throws Exception {
        MessageDigest 계산 = MessageDigest.getInstance("SHA-256"); byte[] берилмелер = new byte[1024 * 1024];
        try (InputStream 입력 = Files.newInputStream(ЖОЛ)) { for (int узундук_маани; (узундук_маани = 입력.read(берилмелер)) >= 0;) 계산.update(берилмелер,0,узундук_маани); }
        return хэш_СМС(계산.digest());
    }
    static String хэш_СМС(byte[] берилмелер) {
        StringBuilder Текст = new StringBuilder(); for (byte маани : берилмелер) Текст.append(String.format(Locale.ROOT,"%02x",маани & 255)); return Текст.toString();
    }
    static Path 내부경로(Path 기준, String Аты) {
        Path 결과 = 기준.resolve(Аты).normalize();
        if (Аты.isEmpty() || Paths.get(Аты).isAbsolute() || !결과.startsWith(기준) || Аты.indexOf('\\') >= 0)
            throw new IllegalArgumentException("범위를 벗어난 ЖОЛ: " + Аты);
        for (Path 부분 : Paths.get(Аты)) if (부분.toString().equals("..")) throw new IllegalArgumentException("상위 ЖОЛ 금지: " + Аты);
        for (Path 현재 = 결과; 현재 != null && 현재.startsWith(기준); 현재 = 현재.getParent())
            if (Files.isSymbolicLink(현재)) throw new IllegalArgumentException("의존성 경로의 링크 금지: " + Аты);
        return 결과;
    }
    static String 명령출력(List<String> Команда) throws Exception {
        Process Процесс_маани = new ProcessBuilder(Команда).redirectError(ProcessBuilder.Redirect.INHERIT).start();
        String 결과 = new String(Процесс_маани.getInputStream().readAllBytes(),StandardCharsets.UTF_8);
        if (Процесс_маани.waitFor() != 0) throw new IOException("Команда натыйжасыз_маани: " + Команда.get(0)); return 결과;
    }
    static void чыгарып_алуу(Path Архив_маани, Path көздөө_жайы_маани) throws Exception {
        for (String Аты : 명령출력(Arrays.asList("tar","-tzf",Архив_маани.toString())).split("\n")) 내부경로(көздөө_жайы_маани, Аты);
        for (String сап : 명령출력(Arrays.asList("tar","-tvzf",Архив_маани.toString())).split("\n"))
            if (!сап.isEmpty() && сап.charAt(0) != '-' && сап.charAt(0) != 'd') throw new IOException("외부 링크 또는 특수 파일을 포함한 의존성");
        Files.createDirectories(көздөө_жайы_маани);
        int абал_маани = new ProcessBuilder("tar","--no-same-owner","--no-same-permissions","-xzf",Архив_маани.toString(),"-C",көздөө_жайы_маани.toString()).inheritIO().start().waitFor();
        if (абал_маани != 0) throw new IOException("의존성 Архив_маани чыгаруу_сактагыч натыйжасыз_маани");
    }
    static void 호출(Path 작업경로, Path Куралдар, List<String> 인수, Map<String,String> 환경) throws Exception {
        List<String> Команда = new ArrayList<>(Arrays.asList("python3", Куралдар.toString())); Команда.addAll(인수);
        ProcessBuilder аткаруу_буйрук = new ProcessBuilder(Команда).directory(작업경로.toFile()).inheritIO(); аткаруу_буйрук.environment().putAll(환경);
        int абал_маани = аткаруу_буйрук.start().waitFor(); if (абал_маани != 0) throw new IOException("Куралдар натыйжасыз_маани: " + Куралдар + " (" + абал_маани + ")");
    }
    @SuppressWarnings("unchecked")
    public static void main(String[] 인수) throws Exception {
        if (인수.length < 1) throw new IllegalArgumentException("build, run, desktop, image, check, test-system 중 동작을 지정하세요");
        String Аракети = 인수[0];
        if (!Arrays.asList("build","run","desktop","image","check","test-system").contains(Аракети)) throw new IllegalArgumentException("알 수 없는 Аракети");
        Path 기준 = Paths.get(System.getProperty("worldos.edition.root")).toAbsolutePath().normalize();
        Map<String,Object> Орнотуулар = (Map<String,Object>)new 자료해석기(Files.readString(기준.resolve("native.json"),StandardCharsets.UTF_8)).Окуу();
        Path башат_дарак = 내부경로(기준,(String)Орнотуулар.get("source")), өзөк_маани = 내부경로(башат_дарак,(String)Орнотуулар.get("native"));
        List<String> 소유파일들 = (List<String>)(List<?>)Орнотуулар.get("owned_files");
        for (String Аты : 소유파일들) if (!Files.isRegularFile(내부경로(башат_дарак,Аты))) throw new IOException("башат_дарак 없음: " + Аты);
        if (Аракети.equals("check")) { System.out.println(Орнотуулар.get("country") + " " + Орнотуулар.get("language") + " 독립 башат_дарак тууралыгын_аныктоо 완료"); return; }
        String 자원상대 = (String)Орнотуулар.getOrDefault("resource_root", ".");
        if (!자원상대.equals(".") && !자원상대.equals("..")) throw new IllegalArgumentException("의존성 기준 ЖОЛ Ката");
        Path ресурс_маани = 기준.resolve(자원상대).normalize(); Path Архив_маани = ресурс_маани.resolve("native-vendor.tar.gz");
        String 기대해시 = (String)Орнотуулар.get("vendor_sha256");
        if (!хэш_файл(Архив_маани).equals(기대해시)) throw new IOException("의존성 SHA-256 불일치");
        Path 표식 = башат_дарак.resolve(".vendor-sha256");
        if (!Files.isRegularFile(표식) || !Files.readString(표식).trim().equals(기대해시)) { чыгарып_алуу(Архив_маани, башат_дарак); Files.writeString(표식,기대해시 + "\n"); }
        Map<String,String> 환경 = new HashMap<>(System.getenv());
        Path ipConfig = null;
        if (환경.containsKey("IP_CONFIG")) ipConfig = Paths.get(환경.get("IP_CONFIG")).toAbsolutePath().normalize();
        else for (Path parent = 기준; parent != null; parent = parent.getParent()) {
            if (Files.isRegularFile(parent.resolve("ip.conf"))) { ipConfig = parent.resolve("ip.conf"); break; }
        }
        if (ipConfig == null) ipConfig = башат_дарак.resolve("ip.conf");
        if (!Files.isRegularFile(ipConfig)) throw new IOException("Missing ip.conf: " + ipConfig);
        환경.put("IP_CONFIG", ipConfig.toString());
        if (Arrays.asList("run","desktop","test-system").contains(Аракети) && !환경.containsKey("QEMU_AARCH64")) {
            Path програм_жаратма_тарткычы = ресурс_маани.resolve("host/qemu"), 실행기표식 = ресурс_маани.resolve("host/.qemu-sha256");
            String жаратма_тарткычы_хэш = (String)Орнотуулар.get("qemu_sha256");
            if (!Files.isRegularFile(програм_жаратма_тарткычы) || !Files.isRegularFile(실행기표식) || !Files.readString(실행기표식).trim().equals(жаратма_тарткычы_хэш)) {
                Path жаратма_тарткычы_Архив = ресурс_маани.resolve("qemu-host.tar.gz"); if (!хэш_файл(жаратма_тарткычы_Архив).equals(жаратма_тарткычы_хэш)) throw new IOException("QEMU SHA-256 불일치");
                чыгарып_алуу(жаратма_тарткычы_Архив,ресурс_маани.resolve("host")); Files.writeString(실행기표식,жаратма_тарткычы_хэш + "\n");
            }
            환경.put("QEMU_AARCH64",програм_жаратма_тарткычы.toString());
        }
        MessageDigest 계산 = MessageDigest.getInstance("SHA-256"); Collections.sort(소유파일들);
        for (String Аты : 소유파일들) { 계산.update(Аты.getBytes(StandardCharsets.UTF_8)); 계산.update(Files.readAllBytes(내부경로(башат_дарак,Аты))); }
        계산.update("ip.conf\0".getBytes(StandardCharsets.UTF_8)); 계산.update(Files.readAllBytes(ipConfig));
        String башат_хэш = хэш_СМС(계산.digest()); Path 빌드표식 = өзөк_маани.resolve("build/worldos-source.sha256");
        if (Аракети.equals("build") || !Files.isRegularFile(빌드표식) || !Files.readString(빌드표식).trim().equals(башат_хэш)) {
            호출(өзөк_маани,내부경로(өзөк_маани,(String)Орнотуулар.get("builder")),Collections.emptyList(),환경);
            Files.writeString(빌드표식,башат_хэш + "\n");
        }
        List<String> 추가인수 = new ArrayList<>(Arrays.asList(인수).subList(1,인수.length));
        if (Аракети.equals("run") || Аракети.equals("desktop")) {
            if (Аракети.equals("desktop")) 추가인수.add(0,"--desktop");
            호출(өзөк_маани,내부경로(өзөк_маани,(String)Орнотуулар.get("runner")),추가인수,환경);
        } else if (Аракети.equals("image")) 호출(өзөк_маани,내부경로(өзөк_маани,(String)Орнотуулар.get("image_builder")),추가인수,환경);
        else if (Аракети.equals("test-system")) {
            추가인수.add(0,기준.toString()); 추가인수.add(0,"--edition");
            호출(өзөк_маани,내부경로(өзөк_маани,(String)Орнотуулар.get("system_tester")),추가인수,환경);
        }
    }
}
