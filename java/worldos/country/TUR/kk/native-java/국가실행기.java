// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.security.MessageDigest;
import java.util.*;

/** 독립 국가판의 의존성 검사·복원·құрастыру_жүйе·실행을 맡는 орналастыру Java Құралдар. */
public final class 국가실행기 {
    static final class деректер_талдау_құралы {
        final String Неден; int Орны;
        деректер_талдау_құралы(String Мәтін) { Неден = Мәтін; }
        void 빈칸() { while (Орны < Неден.length() && Character.isWhitespace(Неден.charAt(Орны))) Орны++; }
        Object Оқу() {
            빈칸(); char таңба_мән = Неден.charAt(Орны++);
            if (таңба_мән == '{') {
                Map<String,Object> НӘТИЖЕ = new LinkedHashMap<>(); 빈칸();
                if (Неден.charAt(Орны) == '}') { Орны++; return НӘТИЖЕ; }
                while (true) {
                    String Аты = (String)Оқу(); 빈칸(); if (Неден.charAt(Орны++) != ':') throw new IllegalArgumentException("деректер бөлгіш_мән Қате");
                    НӘТИЖЕ.put(Аты, Оқу()); 빈칸(); char бөлгіш_мән = Неден.charAt(Орны++);
                    if (бөлгіш_мән == '}') return НӘТИЖЕ; if (бөлгіш_мән != ',') throw new IllegalArgumentException("деректер бөлгіш_мән Қате");
                }
            }
            if (таңба_мән == '[') {
                List<Object> НӘТИЖЕ = new ArrayList<>(); 빈칸();
                if (Неден.charAt(Орны) == ']') { Орны++; return НӘТИЖЕ; }
                while (true) {
                    НӘТИЖЕ.add(Оқу()); 빈칸(); char бөлгіш_мән = Неден.charAt(Орны++);
                    if (бөлгіш_мән == ']') return НӘТИЖЕ; if (бөлгіш_мән != ',') throw new IllegalArgumentException("деректер бөлгіш_мән Қате");
                }
            }
            if (таңба_мән == '"') {
                StringBuilder НӘТИЖЕ = new StringBuilder();
                while (true) {
                    char Келесі_элемент = Неден.charAt(Орны++); if (Келесі_элемент == '"') return НӘТИЖЕ.toString();
                    if (Келесі_элемент == '\\') {
                        Келесі_элемент = Неден.charAt(Орны++);
                        if (Келесі_элемент == 'u') { НӘТИЖЕ.append((char)Integer.parseInt(Неден.substring(Орны, Орны + 4),16)); Орны += 4; continue; }
                        if (Келесі_элемент == 'n') Келесі_элемент = '\n'; else if (Келесі_элемент == 'r') Келесі_элемент = '\r'; else if (Келесі_элемент == 't') Келесі_элемент = '\t';
                        else if (Келесі_элемент == 'b') Келесі_элемент = '\b'; else if (Келесі_элемент == 'f') Келесі_элемент = '\f';
                        else if (Келесі_элемент != '"' && Келесі_элемент != '\\' && Келесі_элемент != '/') throw new IllegalArgumentException("문자 이스케이프 Қате");
                    }
                    НӘТИЖЕ.append(Келесі_элемент);
                }
            }
            int Орындау_2 = Орны - 1;
            while (Орны < Неден.length() && ",]} \t\r\n".indexOf(Неден.charAt(Орны)) < 0) Орны++;
            String мән = Неден.substring(Орындау_2, Орны);
            if (мән.equals("true")) return Boolean.TRUE; if (мән.equals("false")) return Boolean.FALSE; if (мән.equals("null")) return null;
            return Double.valueOf(мән);
        }
    }
    static String хэш_файл(Path Жол_2) throws Exception {
        MessageDigest 계산 = MessageDigest.getInstance("SHA-256"); byte[] деректер = new byte[1024 * 1024];
        try (InputStream 입력 = Files.newInputStream(Жол_2)) { for (int ұзындық_мән; (ұзындық_мән = 입력.read(деректер)) >= 0;) 계산.update(деректер,0,ұзындық_мән); }
        return хэш_Мәтін(계산.digest());
    }
    static String хэш_Мәтін(byte[] деректер) {
        StringBuilder Мәтін = new StringBuilder(); for (byte мән : деректер) Мәтін.append(String.format(Locale.ROOT,"%02x",мән & 255)); return Мәтін.toString();
    }
    static Path 내부경로(Path жоба_түбір, String Аты) {
        Path НӘТИЖЕ = жоба_түбір.resolve(Аты).normalize();
        if (Аты.isEmpty() || Paths.get(Аты).isAbsolute() || !НӘТИЖЕ.startsWith(жоба_түбір) || Аты.indexOf('\\') >= 0)
            throw new IllegalArgumentException("범위를 벗어난 Жол_2: " + Аты);
        for (Path 부분 : Paths.get(Аты)) if (부분.toString().equals("..")) throw new IllegalArgumentException("상위 Жол_2 금지: " + Аты);
        for (Path ток_элемент = НӘТИЖЕ; ток_элемент != null && ток_элемент.startsWith(жоба_түбір); ток_элемент = ток_элемент.getParent())
            if (Files.isSymbolicLink(ток_элемент)) throw new IllegalArgumentException("의존성 경로의 링크 금지: " + Аты);
        return НӘТИЖЕ;
    }
    static String 명령출력(List<String> Команда) throws Exception {
        Process Процесс_мән = new ProcessBuilder(Команда).redirectError(ProcessBuilder.Redirect.INHERIT).start();
        String НӘТИЖЕ = new String(Процесс_мән.getInputStream().readAllBytes(),StandardCharsets.UTF_8);
        if (Процесс_мән.waitFor() != 0) throw new IOException("Команда қате_мән: " + Команда.get(0)); return НӘТИЖЕ;
    }
    static void шығарып_алу(Path Мұрағат_мән, Path тағайындау_мән) throws Exception {
        for (String Аты : 명령출력(Arrays.asList("tar","-tzf",Мұрағат_мән.toString())).split("\n")) 내부경로(тағайындау_мән, Аты);
        for (String Жол : 명령출력(Arrays.asList("tar","-tvzf",Мұрағат_мән.toString())).split("\n"))
            if (!Жол.isEmpty() && Жол.charAt(0) != '-' && Жол.charAt(0) != 'd') throw new IOException("сыртқы_мән 링크 또는 특수 파일을 포함한 의존성");
        Files.createDirectories(тағайындау_мән);
        int күй_мән = new ProcessBuilder("tar","--no-same-owner","--no-same-permissions","-xzf",Мұрағат_мән.toString(),"-C",тағайындау_мән.toString()).inheritIO().start().waitFor();
        if (күй_мән != 0) throw new IOException("의존성 Мұрағат_мән шығарылым_Жад қате_мән");
    }
    static void 호출(Path 작업경로, Path Құралдар, List<String> Аргументтер, Map<String,String> 환경) throws Exception {
        List<String> Команда = new ArrayList<>(Arrays.asList("python3", Құралдар.toString())); Команда.addAll(Аргументтер);
        ProcessBuilder орындау_пәрмен = new ProcessBuilder(Команда).directory(작업경로.toFile()).inheritIO(); орындау_пәрмен.environment().putAll(환경);
        int күй_мән = орындау_пәрмен.start().waitFor(); if (күй_мән != 0) throw new IOException("Құралдар қате_мән: " + Құралдар + " (" + күй_мән + ")");
    }
    @SuppressWarnings("unchecked")
    public static void main(String[] Аргументтер) throws Exception {
        if (Аргументтер.length < 1) throw new IllegalArgumentException("build, run, desktop, image, check, test-system 중 동작을 지정하세요");
        String Әрекет = Аргументтер[0];
        if (!Arrays.asList("build","run","desktop","image","check","test-system").contains(Әрекет)) throw new IllegalArgumentException("알 수 없는 Әрекет");
        Path жоба_түбір = Paths.get(System.getProperty("worldos.edition.root")).toAbsolutePath().normalize();
        Map<String,Object> Баптаулар = (Map<String,Object>)new деректер_талдау_құралы(Files.readString(жоба_түбір.resolve("native.json"),StandardCharsets.UTF_8)).Оқу();
        Path көз_дарақ = 내부경로(жоба_түбір,(String)Баптаулар.get("source")), ядро_мән = 내부경로(көз_дарақ,(String)Баптаулар.get("native"));
        List<String> 소유파일들 = (List<String>)(List<?>)Баптаулар.get("owned_files");
        for (String Аты : 소유파일들) if (!Files.isRegularFile(내부경로(көз_дарақ,Аты))) throw new IOException("көз_дарақ 없음: " + Аты);
        if (Әрекет.equals("check")) { System.out.println(Баптаулар.get("country") + " " + Баптаулар.get("language") + " 독립 көз_дарақ тексеру 완료"); return; }
        String 자원상대 = (String)Баптаулар.getOrDefault("resource_root", ".");
        if (!자원상대.equals(".") && !자원상대.equals("..")) throw new IllegalArgumentException("의존성 жоба_түбір Жол_2 Қате");
        Path ресурс_мән = жоба_түбір.resolve(자원상대).normalize(); Path Мұрағат_мән = ресурс_мән.resolve("native-vendor.tar.gz");
        String 기대해시 = (String)Баптаулар.get("vendor_sha256");
        if (!хэш_файл(Мұрағат_мән).equals(기대해시)) throw new IOException("의존성 SHA-256 불일치");
        Path 표식 = көз_дарақ.resolve(".vendor-sha256");
        if (!Files.isRegularFile(표식) || !Files.readString(표식).trim().equals(기대해시)) { шығарып_алу(Мұрағат_мән, көз_дарақ); Files.writeString(표식,기대해시 + "\n"); }
        Map<String,String> 환경 = new HashMap<>(System.getenv());
        Path ipConfig = null;
        if (환경.containsKey("IP_CONFIG")) ipConfig = Paths.get(환경.get("IP_CONFIG")).toAbsolutePath().normalize();
        else for (Path parent = жоба_түбір; parent != null; parent = parent.getParent()) {
            if (Files.isRegularFile(parent.resolve("ip.conf"))) { ipConfig = parent.resolve("ip.conf"); break; }
        }
        if (ipConfig == null) ipConfig = көз_дарақ.resolve("ip.conf");
        if (!Files.isRegularFile(ipConfig)) throw new IOException("Missing ip.conf: " + ipConfig);
        환경.put("IP_CONFIG", ipConfig.toString());
        if (Arrays.asList("run","desktop","test-system").contains(Әрекет) && !환경.containsKey("QEMU_AARCH64")) {
            Path бағдарлама_іске_қосу_құралы = ресурс_мән.resolve("host/qemu"), 실행기표식 = ресурс_мән.resolve("host/.qemu-sha256");
            String іске_қосу_құралы_хэш = (String)Баптаулар.get("qemu_sha256");
            if (!Files.isRegularFile(бағдарлама_іске_қосу_құралы) || !Files.isRegularFile(실행기표식) || !Files.readString(실행기표식).trim().equals(іске_қосу_құралы_хэш)) {
                Path іске_қосу_құралы_Мұрағат = ресурс_мән.resolve("qemu-host.tar.gz"); if (!хэш_файл(іске_қосу_құралы_Мұрағат).equals(іске_қосу_құралы_хэш)) throw new IOException("QEMU SHA-256 불일치");
                шығарып_алу(іске_қосу_құралы_Мұрағат,ресурс_мән.resolve("host")); Files.writeString(실행기표식,іске_қосу_құралы_хэш + "\n");
            }
            환경.put("QEMU_AARCH64",бағдарлама_іске_қосу_құралы.toString());
        }
        MessageDigest 계산 = MessageDigest.getInstance("SHA-256"); Collections.sort(소유파일들);
        for (String Аты : 소유파일들) { 계산.update(Аты.getBytes(StandardCharsets.UTF_8)); 계산.update(Files.readAllBytes(내부경로(көз_дарақ,Аты))); }
        계산.update("ip.conf\0".getBytes(StandardCharsets.UTF_8)); 계산.update(Files.readAllBytes(ipConfig));
        String көз_хэш = хэш_Мәтін(계산.digest()); Path 빌드표식 = ядро_мән.resolve("build/worldos-source.sha256");
        if (Әрекет.equals("build") || !Files.isRegularFile(빌드표식) || !Files.readString(빌드표식).trim().equals(көз_хэш)) {
            호출(ядро_мән,내부경로(ядро_мән,(String)Баптаулар.get("builder")),Collections.emptyList(),환경);
            Files.writeString(빌드표식,көз_хэш + "\n");
        }
        List<String> 추가인수 = new ArrayList<>(Arrays.asList(Аргументтер).subList(1,Аргументтер.length));
        if (Әрекет.equals("run") || Әрекет.equals("desktop")) {
            if (Әрекет.equals("desktop")) 추가인수.add(0,"--desktop");
            호출(ядро_мән,내부경로(ядро_мән,(String)Баптаулар.get("runner")),추가인수,환경);
        } else if (Әрекет.equals("image")) 호출(ядро_мән,내부경로(ядро_мән,(String)Баптаулар.get("image_builder")),추가인수,환경);
        else if (Әрекет.equals("test-system")) {
            추가인수.add(0,жоба_түбір.toString()); 추가인수.add(0,"--edition");
            호출(ядро_мән,내부경로(ядро_мән,(String)Баптаулар.get("system_tester")),추가인수,환경);
        }
    }
}
