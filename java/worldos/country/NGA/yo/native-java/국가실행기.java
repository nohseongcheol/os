// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.security.MessageDigest;
import java.util.*;

/** 독립 국가판의 의존성 검사·복원·àtòpọ̀_ètò·실행을 맡는 olùpèsè Java Àwọn_irinṣẹ́. */
public final class 국가실행기 {
    static final class 자료해석기 {
        final String orísun; int 위치;
        자료해석기(String SMS) { orísun = SMS; }
        void 빈칸() { while (위치 < orísun.length() && Character.isWhitespace(orísun.charAt(위치))) 위치++; }
        Object Kàá() {
            빈칸(); char ẹyọ_ọ̀rọ̀_iye = orísun.charAt(위치++);
            if (ẹyọ_ọ̀rọ̀_iye == '{') {
                Map<String,Object> 결과 = new LinkedHashMap<>(); 빈칸();
                if (orísun.charAt(위치) == '}') { 위치++; return 결과; }
                while (true) {
                    String Orúkọ = (String)Kàá(); 빈칸(); if (orísun.charAt(위치++) != ':') throw new IllegalArgumentException("détà àmí_ìdá_iye àṣìṣe");
                    결과.put(Orúkọ, Kàá()); 빈칸(); char àmí_ìdá_iye = orísun.charAt(위치++);
                    if (àmí_ìdá_iye == '}') return 결과; if (àmí_ìdá_iye != ',') throw new IllegalArgumentException("détà àmí_ìdá_iye àṣìṣe");
                }
            }
            if (ẹyọ_ọ̀rọ̀_iye == '[') {
                List<Object> 결과 = new ArrayList<>(); 빈칸();
                if (orísun.charAt(위치) == ']') { 위치++; return 결과; }
                while (true) {
                    결과.add(Kàá()); 빈칸(); char àmí_ìdá_iye = orísun.charAt(위치++);
                    if (àmí_ìdá_iye == ']') return 결과; if (àmí_ìdá_iye != ',') throw new IllegalArgumentException("détà àmí_ìdá_iye àṣìṣe");
                }
            }
            if (ẹyọ_ọ̀rọ̀_iye == '"') {
                StringBuilder 결과 = new StringBuilder();
                while (true) {
                    char 다음 = orísun.charAt(위치++); if (다음 == '"') return 결과.toString();
                    if (다음 == '\\') {
                        다음 = orísun.charAt(위치++);
                        if (다음 == 'u') { 결과.append((char)Integer.parseInt(orísun.substring(위치, 위치 + 4),16)); 위치 += 4; continue; }
                        if (다음 == 'n') 다음 = '\n'; else if (다음 == 'r') 다음 = '\r'; else if (다음 == 't') 다음 = '\t';
                        else if (다음 == 'b') 다음 = '\b'; else if (다음 == 'f') 다음 = '\f';
                        else if (다음 != '"' && 다음 != '\\' && 다음 != '/') throw new IllegalArgumentException("문자 이스케이프 àṣìṣe");
                    }
                    결과.append(다음);
                }
            }
            int Rọ́ọ̀nù = 위치 - 1;
            while (위치 < orísun.length() && ",]} \t\r\n".indexOf(orísun.charAt(위치)) < 0) 위치++;
            String iye = orísun.substring(Rọ́ọ̀nù, 위치);
            if (iye.equals("true")) return Boolean.TRUE; if (iye.equals("false")) return Boolean.FALSE; if (iye.equals("null")) return null;
            return Double.valueOf(iye);
        }
    }
    static String burú_fáìlì(Path ọ̀nà) throws Exception {
        MessageDigest 계산 = MessageDigest.getInstance("SHA-256"); byte[] détà = new byte[1024 * 1024];
        try (InputStream 입력 = Files.newInputStream(ọ̀nà)) { for (int gígùn_iye; (gígùn_iye = 입력.read(détà)) >= 0;) 계산.update(détà,0,gígùn_iye); }
        return burú_SMS(계산.digest());
    }
    static String burú_SMS(byte[] détà) {
        StringBuilder SMS = new StringBuilder(); for (byte iye : détà) SMS.append(String.format(Locale.ROOT,"%02x",iye & 255)); return SMS.toString();
    }
    static Path 내부경로(Path 기준, String Orúkọ) {
        Path 결과 = 기준.resolve(Orúkọ).normalize();
        if (Orúkọ.isEmpty() || Paths.get(Orúkọ).isAbsolute() || !결과.startsWith(기준) || Orúkọ.indexOf('\\') >= 0)
            throw new IllegalArgumentException("범위를 벗어난 ọ̀nà: " + Orúkọ);
        for (Path 부분 : Paths.get(Orúkọ)) if (부분.toString().equals("..")) throw new IllegalArgumentException("상위 ọ̀nà 금지: " + Orúkọ);
        for (Path 현재 = 결과; 현재 != null && 현재.startsWith(기준); 현재 = 현재.getParent())
            if (Files.isSymbolicLink(현재)) throw new IllegalArgumentException("의존성 경로의 링크 금지: " + Orúkọ);
        return 결과;
    }
    static String 명령출력(List<String> Àṣẹ) throws Exception {
        Process Ìlànà_iye = new ProcessBuilder(Àṣẹ).redirectError(ProcessBuilder.Redirect.INHERIT).start();
        String 결과 = new String(Ìlànà_iye.getInputStream().readAllBytes(),StandardCharsets.UTF_8);
        if (Ìlànà_iye.waitFor() != 0) throw new IOException("Àṣẹ ìkùnà_iye: " + Àṣẹ.get(0)); return 결과;
    }
    static void fà_yọ(Path Ìpamọ_ọlọ́jọ́pípẹ́_iye, Path èbúté_iye) throws Exception {
        for (String Orúkọ : 명령출력(Arrays.asList("tar","-tzf",Ìpamọ_ọlọ́jọ́pípẹ́_iye.toString())).split("\n")) 내부경로(èbúté_iye, Orúkọ);
        for (String ìlà : 명령출력(Arrays.asList("tar","-tvzf",Ìpamọ_ọlọ́jọ́pípẹ́_iye.toString())).split("\n"))
            if (!ìlà.isEmpty() && ìlà.charAt(0) != '-' && ìlà.charAt(0) != 'd') throw new IOException("외부 링크 또는 특수 파일을 포함한 의존성");
        Files.createDirectories(èbúté_iye);
        int ipò_iye = new ProcessBuilder("tar","--no-same-owner","--no-same-permissions","-xzf",Ìpamọ_ọlọ́jọ́pípẹ́_iye.toString(),"-C",èbúté_iye.toString()).inheritIO().start().waitFor();
        if (ipò_iye != 0) throw new IOException("의존성 Ìpamọ_ọlọ́jọ́pípẹ́_iye dápadà_Ibi_ìpamọ́ ìkùnà_iye");
    }
    static void 호출(Path 작업경로, Path Àwọn_irinṣẹ́, List<String> 인수, Map<String,String> 환경) throws Exception {
        List<String> Àṣẹ = new ArrayList<>(Arrays.asList("python3", Àwọn_irinṣẹ́.toString())); Àṣẹ.addAll(인수);
        ProcessBuilder ṣiṣẹ́_àṣẹ = new ProcessBuilder(Àṣẹ).directory(작업경로.toFile()).inheritIO(); ṣiṣẹ́_àṣẹ.environment().putAll(환경);
        int ipò_iye = ṣiṣẹ́_àṣẹ.start().waitFor(); if (ipò_iye != 0) throw new IOException("Àwọn_irinṣẹ́ ìkùnà_iye: " + Àwọn_irinṣẹ́ + " (" + ipò_iye + ")");
    }
    @SuppressWarnings("unchecked")
    public static void main(String[] 인수) throws Exception {
        if (인수.length < 1) throw new IllegalArgumentException("build, run, desktop, image, check, test-system 중 동작을 지정하세요");
        String ìṣe = 인수[0];
        if (!Arrays.asList("build","run","desktop","image","check","test-system").contains(ìṣe)) throw new IllegalArgumentException("알 수 없는 ìṣe");
        Path 기준 = Paths.get(System.getProperty("worldos.edition.root")).toAbsolutePath().normalize();
        Map<String,Object> Àwọn_ààtò = (Map<String,Object>)new 자료해석기(Files.readString(기준.resolve("native.json"),StandardCharsets.UTF_8)).Kàá();
        Path orísun_ètò_afigijúwe = 내부경로(기준,(String)Àwọn_ààtò.get("source")), kánẹ́ẹ̀lì_iye = 내부경로(orísun_ètò_afigijúwe,(String)Àwọn_ààtò.get("native"));
        List<String> 소유파일들 = (List<String>)(List<?>)Àwọn_ààtò.get("owned_files");
        for (String Orúkọ : 소유파일들) if (!Files.isRegularFile(내부경로(orísun_ètò_afigijúwe,Orúkọ))) throw new IOException("orísun_ètò_afigijúwe 없음: " + Orúkọ);
        if (ìṣe.equals("check")) { System.out.println(Àwọn_ààtò.get("country") + " " + Àwọn_ààtò.get("language") + " 독립 orísun_ètò_afigijúwe ridájú 완료"); return; }
        String 자원상대 = (String)Àwọn_ààtò.getOrDefault("resource_root", ".");
        if (!자원상대.equals(".") && !자원상대.equals("..")) throw new IllegalArgumentException("의존성 기준 ọ̀nà àṣìṣe");
        Path ohun_àmúlò_iye = 기준.resolve(자원상대).normalize(); Path Ìpamọ_ọlọ́jọ́pípẹ́_iye = ohun_àmúlò_iye.resolve("native-vendor.tar.gz");
        String 기대해시 = (String)Àwọn_ààtò.get("vendor_sha256");
        if (!burú_fáìlì(Ìpamọ_ọlọ́jọ́pípẹ́_iye).equals(기대해시)) throw new IOException("의존성 SHA-256 불일치");
        Path 표식 = orísun_ètò_afigijúwe.resolve(".vendor-sha256");
        if (!Files.isRegularFile(표식) || !Files.readString(표식).trim().equals(기대해시)) { fà_yọ(Ìpamọ_ọlọ́jọ́pípẹ́_iye, orísun_ètò_afigijúwe); Files.writeString(표식,기대해시 + "\n"); }
        Map<String,String> 환경 = new HashMap<>(System.getenv());
        Path ipConfig = null;
        if (환경.containsKey("IP_CONFIG")) ipConfig = Paths.get(환경.get("IP_CONFIG")).toAbsolutePath().normalize();
        else for (Path parent = 기준; parent != null; parent = parent.getParent()) {
            if (Files.isRegularFile(parent.resolve("ip.conf"))) { ipConfig = parent.resolve("ip.conf"); break; }
        }
        if (ipConfig == null) ipConfig = orísun_ètò_afigijúwe.resolve("ip.conf");
        if (!Files.isRegularFile(ipConfig)) throw new IOException("Missing ip.conf: " + ipConfig);
        환경.put("IP_CONFIG", ipConfig.toString());
        if (Arrays.asList("run","desktop","test-system").contains(ìṣe) && !환경.containsKey("QEMU_AARCH64")) {
            Path àtòjọ_ètò_aṣàfilọ́lẹ̀ = ohun_àmúlò_iye.resolve("host/qemu"), 실행기표식 = ohun_àmúlò_iye.resolve("host/.qemu-sha256");
            String aṣàfilọ́lẹ̀_burú = (String)Àwọn_ààtò.get("qemu_sha256");
            if (!Files.isRegularFile(àtòjọ_ètò_aṣàfilọ́lẹ̀) || !Files.isRegularFile(실행기표식) || !Files.readString(실행기표식).trim().equals(aṣàfilọ́lẹ̀_burú)) {
                Path aṣàfilọ́lẹ̀_Ìpamọ_ọlọ́jọ́pípẹ́ = ohun_àmúlò_iye.resolve("qemu-host.tar.gz"); if (!burú_fáìlì(aṣàfilọ́lẹ̀_Ìpamọ_ọlọ́jọ́pípẹ́).equals(aṣàfilọ́lẹ̀_burú)) throw new IOException("QEMU SHA-256 불일치");
                fà_yọ(aṣàfilọ́lẹ̀_Ìpamọ_ọlọ́jọ́pípẹ́,ohun_àmúlò_iye.resolve("host")); Files.writeString(실행기표식,aṣàfilọ́lẹ̀_burú + "\n");
            }
            환경.put("QEMU_AARCH64",àtòjọ_ètò_aṣàfilọ́lẹ̀.toString());
        }
        MessageDigest 계산 = MessageDigest.getInstance("SHA-256"); Collections.sort(소유파일들);
        for (String Orúkọ : 소유파일들) { 계산.update(Orúkọ.getBytes(StandardCharsets.UTF_8)); 계산.update(Files.readAllBytes(내부경로(orísun_ètò_afigijúwe,Orúkọ))); }
        계산.update("ip.conf\0".getBytes(StandardCharsets.UTF_8)); 계산.update(Files.readAllBytes(ipConfig));
        String orísun_burú = burú_SMS(계산.digest()); Path 빌드표식 = kánẹ́ẹ̀lì_iye.resolve("build/worldos-source.sha256");
        if (ìṣe.equals("build") || !Files.isRegularFile(빌드표식) || !Files.readString(빌드표식).trim().equals(orísun_burú)) {
            호출(kánẹ́ẹ̀lì_iye,내부경로(kánẹ́ẹ̀lì_iye,(String)Àwọn_ààtò.get("builder")),Collections.emptyList(),환경);
            Files.writeString(빌드표식,orísun_burú + "\n");
        }
        List<String> 추가인수 = new ArrayList<>(Arrays.asList(인수).subList(1,인수.length));
        if (ìṣe.equals("run") || ìṣe.equals("desktop")) {
            if (ìṣe.equals("desktop")) 추가인수.add(0,"--desktop");
            호출(kánẹ́ẹ̀lì_iye,내부경로(kánẹ́ẹ̀lì_iye,(String)Àwọn_ààtò.get("runner")),추가인수,환경);
        } else if (ìṣe.equals("image")) 호출(kánẹ́ẹ̀lì_iye,내부경로(kánẹ́ẹ̀lì_iye,(String)Àwọn_ààtò.get("image_builder")),추가인수,환경);
        else if (ìṣe.equals("test-system")) {
            추가인수.add(0,기준.toString()); 추가인수.add(0,"--edition");
            호출(kánẹ́ẹ̀lì_iye,내부경로(kánẹ́ẹ̀lì_iye,(String)Àwọn_ààtò.get("system_tester")),추가인수,환경);
        }
    }
}
