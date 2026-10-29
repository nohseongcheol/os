// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.security.MessageDigest;
import java.util.*;

/** 독립 국가판의 의존성 검사·복원·tog_siostam·실행을 맡는 òstair Java innealan. */
public final class 국가실행기 {
    static final class 자료해석기 {
        final String tùs; int suidhich;
        자료해석기(String SMS) { tùs = SMS; }
        void 빈칸() { while (suidhich < tùs.length() && Character.isWhitespace(tùs.charAt(suidhich))) suidhich++; }
        Object 읽기() {
            빈칸(); char caractar_VALUE = tùs.charAt(suidhich++);
            if (caractar_VALUE == '{') {
                Map<String,Object> tomhas = new LinkedHashMap<>(); 빈칸();
                if (tùs.charAt(suidhich) == '}') { suidhich++; return tomhas; }
                while (true) {
                    String Ainm = (String)읽기(); 빈칸(); if (tùs.charAt(suidhich++) != ':') throw new IllegalArgumentException("dàta comharra_crìche_VALUE Mearachd");
                    tomhas.put(Ainm, 읽기()); 빈칸(); char comharra_crìche_VALUE = tùs.charAt(suidhich++);
                    if (comharra_crìche_VALUE == '}') return tomhas; if (comharra_crìche_VALUE != ',') throw new IllegalArgumentException("dàta comharra_crìche_VALUE Mearachd");
                }
            }
            if (caractar_VALUE == '[') {
                List<Object> tomhas = new ArrayList<>(); 빈칸();
                if (tùs.charAt(suidhich) == ']') { suidhich++; return tomhas; }
                while (true) {
                    tomhas.add(읽기()); 빈칸(); char comharra_crìche_VALUE = tùs.charAt(suidhich++);
                    if (comharra_crìche_VALUE == ']') return tomhas; if (comharra_crìche_VALUE != ',') throw new IllegalArgumentException("dàta comharra_crìche_VALUE Mearachd");
                }
            }
            if (caractar_VALUE == '"') {
                StringBuilder tomhas = new StringBuilder();
                while (true) {
                    char air_adhart_nì = tùs.charAt(suidhich++); if (air_adhart_nì == '"') return tomhas.toString();
                    if (air_adhart_nì == '\\') {
                        air_adhart_nì = tùs.charAt(suidhich++);
                        if (air_adhart_nì == 'u') { tomhas.append((char)Integer.parseInt(tùs.substring(suidhich, suidhich + 4),16)); suidhich += 4; continue; }
                        if (air_adhart_nì == 'n') air_adhart_nì = '\n'; else if (air_adhart_nì == 'r') air_adhart_nì = '\r'; else if (air_adhart_nì == 't') air_adhart_nì = '\t';
                        else if (air_adhart_nì == 'b') air_adhart_nì = '\b'; else if (air_adhart_nì == 'f') air_adhart_nì = '\f';
                        else if (air_adhart_nì != '"' && air_adhart_nì != '\\' && air_adhart_nì != '/') throw new IllegalArgumentException("문자 이스케이프 Mearachd");
                    }
                    tomhas.append(air_adhart_nì);
                }
            }
            int ruith = suidhich - 1;
            while (suidhich < tùs.length() && ",]} \t\r\n".indexOf(tùs.charAt(suidhich)) < 0) suidhich++;
            String VALUE = tùs.substring(ruith, suidhich);
            if (VALUE.equals("true")) return Boolean.TRUE; if (VALUE.equals("false")) return Boolean.FALSE; if (VALUE.equals("null")) return null;
            return Double.valueOf(VALUE);
        }
    }
    static String hais_faidhle(Path Slighe) throws Exception {
        MessageDigest 계산 = MessageDigest.getInstance("SHA-256"); byte[] dàta = new byte[1024 * 1024];
        try (InputStream 입력 = Files.newInputStream(Slighe)) { for (int faid_VALUE; (faid_VALUE = 입력.read(dàta)) >= 0;) 계산.update(dàta,0,faid_VALUE); }
        return hais_SMS(계산.digest());
    }
    static String hais_SMS(byte[] dàta) {
        StringBuilder SMS = new StringBuilder(); for (byte VALUE : dàta) SMS.append(String.format(Locale.ROOT,"%02x",VALUE & 255)); return SMS.toString();
    }
    static Path 내부경로(Path tilg_freumh, String Ainm) {
        Path tomhas = tilg_freumh.resolve(Ainm).normalize();
        if (Ainm.isEmpty() || Paths.get(Ainm).isAbsolute() || !tomhas.startsWith(tilg_freumh) || Ainm.indexOf('\\') >= 0)
            throw new IllegalArgumentException("범위를 벗어난 Slighe: " + Ainm);
        for (Path 부분 : Paths.get(Ainm)) if (부분.toString().equals("..")) throw new IllegalArgumentException("상위 Slighe 금지: " + Ainm);
        for (Path 현재 = tomhas; 현재 != null && 현재.startsWith(tilg_freumh); 현재 = 현재.getParent())
            if (Files.isSymbolicLink(현재)) throw new IllegalArgumentException("의존성 경로의 링크 금지: " + Ainm);
        return tomhas;
    }
    static String 명령출력(List<String> àithne) throws Exception {
        Process Pròiseas_VALUE = new ProcessBuilder(àithne).redirectError(ProcessBuilder.Redirect.INHERIT).start();
        String tomhas = new String(Pròiseas_VALUE.getInputStream().readAllBytes(),StandardCharsets.UTF_8);
        if (Pròiseas_VALUE.waitFor() != 0) throw new IOException("àithne fàilligeadh_VALUE: " + àithne.get(0)); return tomhas;
    }
    static void às_tharraing(Path taisg_VALUE, Path ceann_uidhe_VALUE) throws Exception {
        for (String Ainm : 명령출력(Arrays.asList("tar","-tzf",taisg_VALUE.toString())).split("\n")) 내부경로(ceann_uidhe_VALUE, Ainm);
        for (String loidhne : 명령출력(Arrays.asList("tar","-tvzf",taisg_VALUE.toString())).split("\n"))
            if (!loidhne.isEmpty() && loidhne.charAt(0) != '-' && loidhne.charAt(0) != 'd') throw new IOException("외부 링크 또는 특수 파일을 포함한 의존성");
        Files.createDirectories(ceann_uidhe_VALUE);
        int cor_VALUE = new ProcessBuilder("tar","--no-same-owner","--no-same-permissions","-xzf",taisg_VALUE.toString(),"-C",ceann_uidhe_VALUE.toString()).inheritIO().start().waitFor();
        if (cor_VALUE != 0) throw new IOException("의존성 taisg_VALUE sgaoileadh_stòras fàilligeadh_VALUE");
    }
    static void 호출(Path 작업경로, Path innealan, List<String> 인수, Map<String,String> 환경) throws Exception {
        List<String> àithne = new ArrayList<>(Arrays.asList("python3", innealan.toString())); àithne.addAll(인수);
        ProcessBuilder gnìomhaich_àithne = new ProcessBuilder(àithne).directory(작업경로.toFile()).inheritIO(); gnìomhaich_àithne.environment().putAll(환경);
        int cor_VALUE = gnìomhaich_àithne.start().waitFor(); if (cor_VALUE != 0) throw new IOException("innealan fàilligeadh_VALUE: " + innealan + " (" + cor_VALUE + ")");
    }
    @SuppressWarnings("unchecked")
    public static void main(String[] 인수) throws Exception {
        if (인수.length < 1) throw new IllegalArgumentException("build, run, desktop, image, check, test-system 중 동작을 지정하세요");
        String Gnìomh = 인수[0];
        if (!Arrays.asList("build","run","desktop","image","check","test-system").contains(Gnìomh)) throw new IllegalArgumentException("알 수 없는 Gnìomh");
        Path tilg_freumh = Paths.get(System.getProperty("worldos.edition.root")).toAbsolutePath().normalize();
        Map<String,Object> roghainnean = (Map<String,Object>)new 자료해석기(Files.readString(tilg_freumh.resolve("native.json"),StandardCharsets.UTF_8)).읽기();
        Path tùs_craobh = 내부경로(tilg_freumh,(String)roghainnean.get("source")), eitean_VALUE = 내부경로(tùs_craobh,(String)roghainnean.get("native"));
        List<String> 소유파일들 = (List<String>)(List<?>)roghainnean.get("owned_files");
        for (String Ainm : 소유파일들) if (!Files.isRegularFile(내부경로(tùs_craobh,Ainm))) throw new IOException("tùs_craobh 없음: " + Ainm);
        if (Gnìomh.equals("check")) { System.out.println(roghainnean.get("country") + " " + roghainnean.get("language") + " 독립 tùs_craobh dearbh 완료"); return; }
        String 자원상대 = (String)roghainnean.getOrDefault("resource_root", ".");
        if (!자원상대.equals(".") && !자원상대.equals("..")) throw new IllegalArgumentException("의존성 tilg_freumh Slighe Mearachd");
        Path goireas_VALUE = tilg_freumh.resolve(자원상대).normalize(); Path taisg_VALUE = goireas_VALUE.resolve("native-vendor.tar.gz");
        String 기대해시 = (String)roghainnean.get("vendor_sha256");
        if (!hais_faidhle(taisg_VALUE).equals(기대해시)) throw new IOException("의존성 SHA-256 불일치");
        Path 표식 = tùs_craobh.resolve(".vendor-sha256");
        if (!Files.isRegularFile(표식) || !Files.readString(표식).trim().equals(기대해시)) { às_tharraing(taisg_VALUE, tùs_craobh); Files.writeString(표식,기대해시 + "\n"); }
        Map<String,String> 환경 = new HashMap<>(System.getenv());
        Path ipConfig = null;
        if (환경.containsKey("IP_CONFIG")) ipConfig = Paths.get(환경.get("IP_CONFIG")).toAbsolutePath().normalize();
        else for (Path parent = tilg_freumh; parent != null; parent = parent.getParent()) {
            if (Files.isRegularFile(parent.resolve("ip.conf"))) { ipConfig = parent.resolve("ip.conf"); break; }
        }
        if (ipConfig == null) ipConfig = tùs_craobh.resolve("ip.conf");
        if (!Files.isRegularFile(ipConfig)) throw new IOException("Missing ip.conf: " + ipConfig);
        환경.put("IP_CONFIG", ipConfig.toString());
        if (Arrays.asList("run","desktop","test-system").contains(Gnìomh) && !환경.containsKey("QEMU_AARCH64")) {
            Path ap_drathair_nan_aplacaid = goireas_VALUE.resolve("host/qemu"), 실행기표식 = goireas_VALUE.resolve("host/.qemu-sha256");
            String drathair_nan_aplacaid_hais = (String)roghainnean.get("qemu_sha256");
            if (!Files.isRegularFile(ap_drathair_nan_aplacaid) || !Files.isRegularFile(실행기표식) || !Files.readString(실행기표식).trim().equals(drathair_nan_aplacaid_hais)) {
                Path drathair_nan_aplacaid_taisg = goireas_VALUE.resolve("qemu-host.tar.gz"); if (!hais_faidhle(drathair_nan_aplacaid_taisg).equals(drathair_nan_aplacaid_hais)) throw new IOException("QEMU SHA-256 불일치");
                às_tharraing(drathair_nan_aplacaid_taisg,goireas_VALUE.resolve("host")); Files.writeString(실행기표식,drathair_nan_aplacaid_hais + "\n");
            }
            환경.put("QEMU_AARCH64",ap_drathair_nan_aplacaid.toString());
        }
        MessageDigest 계산 = MessageDigest.getInstance("SHA-256"); Collections.sort(소유파일들);
        for (String Ainm : 소유파일들) { 계산.update(Ainm.getBytes(StandardCharsets.UTF_8)); 계산.update(Files.readAllBytes(내부경로(tùs_craobh,Ainm))); }
        계산.update("ip.conf\0".getBytes(StandardCharsets.UTF_8)); 계산.update(Files.readAllBytes(ipConfig));
        String tùs_hais = hais_SMS(계산.digest()); Path 빌드표식 = eitean_VALUE.resolve("build/worldos-source.sha256");
        if (Gnìomh.equals("build") || !Files.isRegularFile(빌드표식) || !Files.readString(빌드표식).trim().equals(tùs_hais)) {
            호출(eitean_VALUE,내부경로(eitean_VALUE,(String)roghainnean.get("builder")),Collections.emptyList(),환경);
            Files.writeString(빌드표식,tùs_hais + "\n");
        }
        List<String> 추가인수 = new ArrayList<>(Arrays.asList(인수).subList(1,인수.length));
        if (Gnìomh.equals("run") || Gnìomh.equals("desktop")) {
            if (Gnìomh.equals("desktop")) 추가인수.add(0,"--desktop");
            호출(eitean_VALUE,내부경로(eitean_VALUE,(String)roghainnean.get("runner")),추가인수,환경);
        } else if (Gnìomh.equals("image")) 호출(eitean_VALUE,내부경로(eitean_VALUE,(String)roghainnean.get("image_builder")),추가인수,환경);
        else if (Gnìomh.equals("test-system")) {
            추가인수.add(0,tilg_freumh.toString()); 추가인수.add(0,"--edition");
            호출(eitean_VALUE,내부경로(eitean_VALUE,(String)roghainnean.get("system_tester")),추가인수,환경);
        }
    }
}
