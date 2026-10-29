// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.security.MessageDigest;
import java.util.*;

/** 독립 국가판의 의존성 검사·복원·nashr_tizim·실행을 맡는 tashkilotchi Java Vositalar. */
public final class 국가실행기 {
    static final class ma_lumotlar_parser {
        final String manba; int Holati;
        ma_lumotlar_parser(String Matn) { manba = Matn; }
        void 빈칸() { while (Holati < manba.length() && Character.isWhitespace(manba.charAt(Holati))) Holati++; }
        Object Oʻqish() {
            빈칸(); char belgi_VALUE = manba.charAt(Holati++);
            if (belgi_VALUE == '{') {
                Map<String,Object> o_lchov = new LinkedHashMap<>(); 빈칸();
                if (manba.charAt(Holati) == '}') { Holati++; return o_lchov; }
                while (true) {
                    String Nomi = (String)Oʻqish(); 빈칸(); if (manba.charAt(Holati++) != ':') throw new IllegalArgumentException("ma_lumotlar ajratuvchi_VALUE Xato");
                    o_lchov.put(Nomi, Oʻqish()); 빈칸(); char ajratuvchi_VALUE = manba.charAt(Holati++);
                    if (ajratuvchi_VALUE == '}') return o_lchov; if (ajratuvchi_VALUE != ',') throw new IllegalArgumentException("ma_lumotlar ajratuvchi_VALUE Xato");
                }
            }
            if (belgi_VALUE == '[') {
                List<Object> o_lchov = new ArrayList<>(); 빈칸();
                if (manba.charAt(Holati) == ']') { Holati++; return o_lchov; }
                while (true) {
                    o_lchov.add(Oʻqish()); 빈칸(); char ajratuvchi_VALUE = manba.charAt(Holati++);
                    if (ajratuvchi_VALUE == ']') return o_lchov; if (ajratuvchi_VALUE != ',') throw new IllegalArgumentException("ma_lumotlar ajratuvchi_VALUE Xato");
                }
            }
            if (belgi_VALUE == '"') {
                StringBuilder o_lchov = new StringBuilder();
                while (true) {
                    char Keyingi_element = manba.charAt(Holati++); if (Keyingi_element == '"') return o_lchov.toString();
                    if (Keyingi_element == '\\') {
                        Keyingi_element = manba.charAt(Holati++);
                        if (Keyingi_element == 'u') { o_lchov.append((char)Integer.parseInt(manba.substring(Holati, Holati + 4),16)); Holati += 4; continue; }
                        if (Keyingi_element == 'n') Keyingi_element = '\n'; else if (Keyingi_element == 'r') Keyingi_element = '\r'; else if (Keyingi_element == 't') Keyingi_element = '\t';
                        else if (Keyingi_element == 'b') Keyingi_element = '\b'; else if (Keyingi_element == 'f') Keyingi_element = '\f';
                        else if (Keyingi_element != '"' && Keyingi_element != '\\' && Keyingi_element != '/') throw new IllegalArgumentException("문자 이스케이프 Xato");
                    }
                    o_lchov.append(Keyingi_element);
                }
            }
            int Bajarish = Holati - 1;
            while (Holati < manba.length() && ",]} \t\r\n".indexOf(manba.charAt(Holati)) < 0) Holati++;
            String VALUE = manba.substring(Bajarish, Holati);
            if (VALUE.equals("true")) return Boolean.TRUE; if (VALUE.equals("false")) return Boolean.FALSE; if (VALUE.equals("null")) return null;
            return Double.valueOf(VALUE);
        }
    }
    static String tasodifiy_ma_lumot_fayl(Path yo_l) throws Exception {
        MessageDigest 계산 = MessageDigest.getInstance("SHA-256"); byte[] ma_lumotlar = new byte[1024 * 1024];
        try (InputStream 입력 = Files.newInputStream(yo_l)) { for (int uzunlik_VALUE; (uzunlik_VALUE = 입력.read(ma_lumotlar)) >= 0;) 계산.update(ma_lumotlar,0,uzunlik_VALUE); }
        return tasodifiy_ma_lumot_SMS(계산.digest());
    }
    static String tasodifiy_ma_lumot_SMS(byte[] ma_lumotlar) {
        StringBuilder Matn = new StringBuilder(); for (byte VALUE : ma_lumotlar) Matn.append(String.format(Locale.ROOT,"%02x",VALUE & 255)); return Matn.toString();
    }
    static Path 내부경로(Path Project_ildiz, String Nomi) {
        Path o_lchov = Project_ildiz.resolve(Nomi).normalize();
        if (Nomi.isEmpty() || Paths.get(Nomi).isAbsolute() || !o_lchov.startsWith(Project_ildiz) || Nomi.indexOf('\\') >= 0)
            throw new IllegalArgumentException("범위를 벗어난 yo_l: " + Nomi);
        for (Path 부분 : Paths.get(Nomi)) if (부분.toString().equals("..")) throw new IllegalArgumentException("상위 yo_l 금지: " + Nomi);
        for (Path 현재 = o_lchov; 현재 != null && 현재.startsWith(Project_ildiz); 현재 = 현재.getParent())
            if (Files.isSymbolicLink(현재)) throw new IllegalArgumentException("의존성 경로의 링크 금지: " + Nomi);
        return o_lchov;
    }
    static String 명령출력(List<String> Buyruq) throws Exception {
        Process Jarayon_VALUE = new ProcessBuilder(Buyruq).redirectError(ProcessBuilder.Redirect.INHERIT).start();
        String o_lchov = new String(Jarayon_VALUE.getInputStream().readAllBytes(),StandardCharsets.UTF_8);
        if (Jarayon_VALUE.waitFor() != 0) throw new IOException("Buyruq to_xtab_qolish_VALUE: " + Buyruq.get(0)); return o_lchov;
    }
    static void chiqarib_olmoq(Path Arxiv_VALUE, Path ko_chirish_joyi_VALUE) throws Exception {
        for (String Nomi : 명령출력(Arrays.asList("tar","-tzf",Arxiv_VALUE.toString())).split("\n")) 내부경로(ko_chirish_joyi_VALUE, Nomi);
        for (String satr : 명령출력(Arrays.asList("tar","-tvzf",Arxiv_VALUE.toString())).split("\n"))
            if (!satr.isEmpty() && satr.charAt(0) != '-' && satr.charAt(0) != 'd') throw new IOException("외부 링크 또는 특수 파일을 포함한 의존성");
        Files.createDirectories(ko_chirish_joyi_VALUE);
        int holat_VALUE_e10195a1 = new ProcessBuilder("tar","--no-same-owner","--no-same-permissions","-xzf",Arxiv_VALUE.toString(),"-C",ko_chirish_joyi_VALUE.toString()).inheritIO().start().waitFor();
        if (holat_VALUE_e10195a1 != 0) throw new IOException("의존성 Arxiv_VALUE nashr_Xotira to_xtab_qolish_VALUE");
    }
    static void 호출(Path 작업경로, Path Vositalar, List<String> 인수, Map<String,String> 환경) throws Exception {
        List<String> Buyruq = new ArrayList<>(Arrays.asList("python3", Vositalar.toString())); Buyruq.addAll(인수);
        ProcessBuilder bajarmoq_buyruq = new ProcessBuilder(Buyruq).directory(작업경로.toFile()).inheritIO(); bajarmoq_buyruq.environment().putAll(환경);
        int holat_VALUE_e10195a1 = bajarmoq_buyruq.start().waitFor(); if (holat_VALUE_e10195a1 != 0) throw new IOException("Vositalar to_xtab_qolish_VALUE: " + Vositalar + " (" + holat_VALUE_e10195a1 + ")");
    }
    @SuppressWarnings("unchecked")
    public static void main(String[] 인수) throws Exception {
        if (인수.length < 1) throw new IllegalArgumentException("build, run, desktop, image, check, test-system 중 동작을 지정하세요");
        String Amal = 인수[0];
        if (!Arrays.asList("build","run","desktop","image","check","test-system").contains(Amal)) throw new IllegalArgumentException("알 수 없는 Amal");
        Path Project_ildiz = Paths.get(System.getProperty("worldos.edition.root")).toAbsolutePath().normalize();
        Map<String,Object> Moslamalar = (Map<String,Object>)new ma_lumotlar_parser(Files.readString(Project_ildiz.resolve("native.json"),StandardCharsets.UTF_8)).Oʻqish();
        Path manba_daraxt = 내부경로(Project_ildiz,(String)Moslamalar.get("source")), o_zak_VALUE = 내부경로(manba_daraxt,(String)Moslamalar.get("native"));
        List<String> 소유파일들 = (List<String>)(List<?>)Moslamalar.get("owned_files");
        for (String Nomi : 소유파일들) if (!Files.isRegularFile(내부경로(manba_daraxt,Nomi))) throw new IOException("manba_daraxt 없음: " + Nomi);
        if (Amal.equals("check")) { System.out.println(Moslamalar.get("country") + " " + Moslamalar.get("language") + " 독립 manba_daraxt tasdiqlamoq 완료"); return; }
        String 자원상대 = (String)Moslamalar.getOrDefault("resource_root", ".");
        if (!자원상대.equals(".") && !자원상대.equals("..")) throw new IllegalArgumentException("의존성 Project_ildiz yo_l Xato");
        Path resurs_VALUE = Project_ildiz.resolve(자원상대).normalize(); Path Arxiv_VALUE = resurs_VALUE.resolve("native-vendor.tar.gz");
        String 기대해시 = (String)Moslamalar.get("vendor_sha256");
        if (!tasodifiy_ma_lumot_fayl(Arxiv_VALUE).equals(기대해시)) throw new IOException("의존성 SHA-256 불일치");
        Path 표식 = manba_daraxt.resolve(".vendor-sha256");
        if (!Files.isRegularFile(표식) || !Files.readString(표식).trim().equals(기대해시)) { chiqarib_olmoq(Arxiv_VALUE, manba_daraxt); Files.writeString(표식,기대해시 + "\n"); }
        Map<String,String> 환경 = new HashMap<>(System.getenv());
        Path ipConfig = null;
        if (환경.containsKey("IP_CONFIG")) ipConfig = Paths.get(환경.get("IP_CONFIG")).toAbsolutePath().normalize();
        else for (Path parent = Project_ildiz; parent != null; parent = parent.getParent()) {
            if (Files.isRegularFile(parent.resolve("ip.conf"))) { ipConfig = parent.resolve("ip.conf"); break; }
        }
        if (ipConfig == null) ipConfig = manba_daraxt.resolve("ip.conf");
        if (!Files.isRegularFile(ipConfig)) throw new IOException("Missing ip.conf: " + ipConfig);
        환경.put("IP_CONFIG", ipConfig.toString());
        if (Arrays.asList("run","desktop","test-system").contains(Amal) && !환경.containsKey("QEMU_AARCH64")) {
            Path ilova_ilovalar_paneli = resurs_VALUE.resolve("host/qemu"), 실행기표식 = resurs_VALUE.resolve("host/.qemu-sha256");
            String ilovalar_paneli_tasodifiy_ma_lumot = (String)Moslamalar.get("qemu_sha256");
            if (!Files.isRegularFile(ilova_ilovalar_paneli) || !Files.isRegularFile(실행기표식) || !Files.readString(실행기표식).trim().equals(ilovalar_paneli_tasodifiy_ma_lumot)) {
                Path ilovalar_paneli_Arxiv = resurs_VALUE.resolve("qemu-host.tar.gz"); if (!tasodifiy_ma_lumot_fayl(ilovalar_paneli_Arxiv).equals(ilovalar_paneli_tasodifiy_ma_lumot)) throw new IOException("QEMU SHA-256 불일치");
                chiqarib_olmoq(ilovalar_paneli_Arxiv,resurs_VALUE.resolve("host")); Files.writeString(실행기표식,ilovalar_paneli_tasodifiy_ma_lumot + "\n");
            }
            환경.put("QEMU_AARCH64",ilova_ilovalar_paneli.toString());
        }
        MessageDigest 계산 = MessageDigest.getInstance("SHA-256"); Collections.sort(소유파일들);
        for (String Nomi : 소유파일들) { 계산.update(Nomi.getBytes(StandardCharsets.UTF_8)); 계산.update(Files.readAllBytes(내부경로(manba_daraxt,Nomi))); }
        계산.update("ip.conf\0".getBytes(StandardCharsets.UTF_8)); 계산.update(Files.readAllBytes(ipConfig));
        String manba_tasodifiy_ma_lumot = tasodifiy_ma_lumot_SMS(계산.digest()); Path 빌드표식 = o_zak_VALUE.resolve("build/worldos-source.sha256");
        if (Amal.equals("build") || !Files.isRegularFile(빌드표식) || !Files.readString(빌드표식).trim().equals(manba_tasodifiy_ma_lumot)) {
            호출(o_zak_VALUE,내부경로(o_zak_VALUE,(String)Moslamalar.get("builder")),Collections.emptyList(),환경);
            Files.writeString(빌드표식,manba_tasodifiy_ma_lumot + "\n");
        }
        List<String> 추가인수 = new ArrayList<>(Arrays.asList(인수).subList(1,인수.length));
        if (Amal.equals("run") || Amal.equals("desktop")) {
            if (Amal.equals("desktop")) 추가인수.add(0,"--desktop");
            호출(o_zak_VALUE,내부경로(o_zak_VALUE,(String)Moslamalar.get("runner")),추가인수,환경);
        } else if (Amal.equals("image")) 호출(o_zak_VALUE,내부경로(o_zak_VALUE,(String)Moslamalar.get("image_builder")),추가인수,환경);
        else if (Amal.equals("test-system")) {
            추가인수.add(0,Project_ildiz.toString()); 추가인수.add(0,"--edition");
            호출(o_zak_VALUE,내부경로(o_zak_VALUE,(String)Moslamalar.get("system_tester")),추가인수,환경);
        }
    }
}
