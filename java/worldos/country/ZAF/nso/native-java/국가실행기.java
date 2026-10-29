// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.security.MessageDigest;
import java.util.*;

/** 독립 국가판의 의존성 검사·복원·aga_lenaneo·실행을 맡는 go_nea_ditirelo Java Ditholosi. */
public final class 국가실행기 {
    static final class 자료해석기 {
        final String mohlodi; int 위치;
        자료해석기(String Sengwalwa) { mohlodi = Sengwalwa; }
        void 빈칸() { while (위치 < mohlodi.length() && Character.isWhitespace(mohlodi.charAt(위치))) 위치++; }
        Object Bala() {
            빈칸(); char tlhaka_boleng = mohlodi.charAt(위치++);
            if (tlhaka_boleng == '{') {
                Map<String,Object> 결과 = new LinkedHashMap<>(); 빈칸();
                if (mohlodi.charAt(위치) == '}') { 위치++; return 결과; }
                while (true) {
                    String Leina = (String)Bala(); 빈칸(); if (mohlodi.charAt(위치++) != ':') throw new IllegalArgumentException("data searoganyi_boleng_d8ba4873 Phošo");
                    결과.put(Leina, Bala()); 빈칸(); char searoganyi_boleng_d8ba4873 = mohlodi.charAt(위치++);
                    if (searoganyi_boleng_d8ba4873 == '}') return 결과; if (searoganyi_boleng_d8ba4873 != ',') throw new IllegalArgumentException("data searoganyi_boleng_d8ba4873 Phošo");
                }
            }
            if (tlhaka_boleng == '[') {
                List<Object> 결과 = new ArrayList<>(); 빈칸();
                if (mohlodi.charAt(위치) == ']') { 위치++; return 결과; }
                while (true) {
                    결과.add(Bala()); 빈칸(); char searoganyi_boleng_d8ba4873 = mohlodi.charAt(위치++);
                    if (searoganyi_boleng_d8ba4873 == ']') return 결과; if (searoganyi_boleng_d8ba4873 != ',') throw new IllegalArgumentException("data searoganyi_boleng_d8ba4873 Phošo");
                }
            }
            if (tlhaka_boleng == '"') {
                StringBuilder 결과 = new StringBuilder();
                while (true) {
                    char 다음 = mohlodi.charAt(위치++); if (다음 == '"') return 결과.toString();
                    if (다음 == '\\') {
                        다음 = mohlodi.charAt(위치++);
                        if (다음 == 'u') { 결과.append((char)Integer.parseInt(mohlodi.substring(위치, 위치 + 4),16)); 위치 += 4; continue; }
                        if (다음 == 'n') 다음 = '\n'; else if (다음 == 'r') 다음 = '\r'; else if (다음 == 't') 다음 = '\t';
                        else if (다음 == 'b') 다음 = '\b'; else if (다음 == 'f') 다음 = '\f';
                        else if (다음 != '"' && 다음 != '\\' && 다음 != '/') throw new IllegalArgumentException("문자 이스케이프 Phošo");
                    }
                    결과.append(다음);
                }
            }
            int Diriša = 위치 - 1;
            while (위치 < mohlodi.length() && ",]} \t\r\n".indexOf(mohlodi.charAt(위치)) < 0) 위치++;
            String boleng = mohlodi.substring(Diriša, 위치);
            if (boleng.equals("true")) return Boolean.TRUE; if (boleng.equals("false")) return Boolean.FALSE; if (boleng.equals("null")) return null;
            return Double.valueOf(boleng);
        }
    }
    static String haše_faele(Path Tsejana) throws Exception {
        MessageDigest 계산 = MessageDigest.getInstance("SHA-256"); byte[] data = new byte[1024 * 1024];
        try (InputStream 입력 = Files.newInputStream(Tsejana)) { for (int botelele_boleng; (botelele_boleng = 입력.read(data)) >= 0;) 계산.update(data,0,botelele_boleng); }
        return haše_SMS(계산.digest());
    }
    static String haše_SMS(byte[] data) {
        StringBuilder Sengwalwa = new StringBuilder(); for (byte boleng : data) Sengwalwa.append(String.format(Locale.ROOT,"%02x",boleng & 255)); return Sengwalwa.toString();
    }
    static Path 내부경로(Path 기준, String Leina) {
        Path 결과 = 기준.resolve(Leina).normalize();
        if (Leina.isEmpty() || Paths.get(Leina).isAbsolute() || !결과.startsWith(기준) || Leina.indexOf('\\') >= 0)
            throw new IllegalArgumentException("범위를 벗어난 Tsejana: " + Leina);
        for (Path 부분 : Paths.get(Leina)) if (부분.toString().equals("..")) throw new IllegalArgumentException("상위 Tsejana 금지: " + Leina);
        for (Path 현재 = 결과; 현재 != null && 현재.startsWith(기준); 현재 = 현재.getParent())
            if (Files.isSymbolicLink(현재)) throw new IllegalArgumentException("의존성 경로의 링크 금지: " + Leina);
        return 결과;
    }
    static String 명령출력(List<String> Taelo) throws Exception {
        Process tiragalo_boleng = new ProcessBuilder(Taelo).redirectError(ProcessBuilder.Redirect.INHERIT).start();
        String 결과 = new String(tiragalo_boleng.getInputStream().readAllBytes(),StandardCharsets.UTF_8);
        if (tiragalo_boleng.waitFor() != 0) throw new IOException("Taelo go_palelwa_boleng: " + Taelo.get(0)); return 결과;
    }
    static void ntšha(Path Akhaebe_boleng, Path boyo_boleng) throws Exception {
        for (String Leina : 명령출력(Arrays.asList("tar","-tzf",Akhaebe_boleng.toString())).split("\n")) 내부경로(boyo_boleng, Leina);
        for (String mothaladi : 명령출력(Arrays.asList("tar","-tvzf",Akhaebe_boleng.toString())).split("\n"))
            if (!mothaladi.isEmpty() && mothaladi.charAt(0) != '-' && mothaladi.charAt(0) != 'd') throw new IOException("외부 링크 또는 특수 파일을 포함한 의존성");
        Files.createDirectories(boyo_boleng);
        int boemo_boleng = new ProcessBuilder("tar","--no-same-owner","--no-same-permissions","-xzf",Akhaebe_boleng.toString(),"-C",boyo_boleng.toString()).inheritIO().start().waitFor();
        if (boemo_boleng != 0) throw new IOException("의존성 Akhaebe_boleng lokolla_Bobolokelo go_palelwa_boleng");
    }
    static void 호출(Path 작업경로, Path Ditholosi, List<String> 인수, Map<String,String> 환경) throws Exception {
        List<String> Taelo = new ArrayList<>(Arrays.asList("python3", Ditholosi.toString())); Taelo.addAll(인수);
        ProcessBuilder phethagatša_taelo = new ProcessBuilder(Taelo).directory(작업경로.toFile()).inheritIO(); phethagatša_taelo.environment().putAll(환경);
        int boemo_boleng = phethagatša_taelo.start().waitFor(); if (boemo_boleng != 0) throw new IOException("Ditholosi go_palelwa_boleng: " + Ditholosi + " (" + boemo_boleng + ")");
    }
    @SuppressWarnings("unchecked")
    public static void main(String[] 인수) throws Exception {
        if (인수.length < 1) throw new IllegalArgumentException("build, run, desktop, image, check, test-system 중 동작을 지정하세요");
        String Mogato = 인수[0];
        if (!Arrays.asList("build","run","desktop","image","check","test-system").contains(Mogato)) throw new IllegalArgumentException("알 수 없는 Mogato");
        Path 기준 = Paths.get(System.getProperty("worldos.edition.root")).toAbsolutePath().normalize();
        Map<String,Object> Dipeakanyo = (Map<String,Object>)new 자료해석기(Files.readString(기준.resolve("native.json"),StandardCharsets.UTF_8)).Bala();
        Path mohlodi_mohlare = 내부경로(기준,(String)Dipeakanyo.get("source")), khenele_boleng = 내부경로(mohlodi_mohlare,(String)Dipeakanyo.get("native"));
        List<String> 소유파일들 = (List<String>)(List<?>)Dipeakanyo.get("owned_files");
        for (String Leina : 소유파일들) if (!Files.isRegularFile(내부경로(mohlodi_mohlare,Leina))) throw new IOException("mohlodi_mohlare 없음: " + Leina);
        if (Mogato.equals("check")) { System.out.println(Dipeakanyo.get("country") + " " + Dipeakanyo.get("language") + " 독립 mohlodi_mohlare kgonthiša 완료"); return; }
        String 자원상대 = (String)Dipeakanyo.getOrDefault("resource_root", ".");
        if (!자원상대.equals(".") && !자원상대.equals("..")) throw new IllegalArgumentException("의존성 기준 Tsejana Phošo");
        Path mothopo_boleng = 기준.resolve(자원상대).normalize(); Path Akhaebe_boleng = mothopo_boleng.resolve("native-vendor.tar.gz");
        String 기대해시 = (String)Dipeakanyo.get("vendor_sha256");
        if (!haše_faele(Akhaebe_boleng).equals(기대해시)) throw new IOException("의존성 SHA-256 불일치");
        Path 표식 = mohlodi_mohlare.resolve(".vendor-sha256");
        if (!Files.isRegularFile(표식) || !Files.readString(표식).trim().equals(기대해시)) { ntšha(Akhaebe_boleng, mohlodi_mohlare); Files.writeString(표식,기대해시 + "\n"); }
        Map<String,String> 환경 = new HashMap<>(System.getenv());
        Path ipConfig = null;
        if (환경.containsKey("IP_CONFIG")) ipConfig = Paths.get(환경.get("IP_CONFIG")).toAbsolutePath().normalize();
        else for (Path parent = 기준; parent != null; parent = parent.getParent()) {
            if (Files.isRegularFile(parent.resolve("ip.conf"))) { ipConfig = parent.resolve("ip.conf"); break; }
        }
        if (ipConfig == null) ipConfig = mohlodi_mohlare.resolve("ip.conf");
        if (!Files.isRegularFile(ipConfig)) throw new IOException("Missing ip.conf: " + ipConfig);
        환경.put("IP_CONFIG", ipConfig.toString());
        if (Arrays.asList("run","desktop","test-system").contains(Mogato) && !환경.containsKey("QEMU_AARCH64")) {
            Path tirišo_sethala_tirišo = mothopo_boleng.resolve("host/qemu"), 실행기표식 = mothopo_boleng.resolve("host/.qemu-sha256");
            String sethala_tirišo_haše = (String)Dipeakanyo.get("qemu_sha256");
            if (!Files.isRegularFile(tirišo_sethala_tirišo) || !Files.isRegularFile(실행기표식) || !Files.readString(실행기표식).trim().equals(sethala_tirišo_haše)) {
                Path sethala_tirišo_Akhaebe = mothopo_boleng.resolve("qemu-host.tar.gz"); if (!haše_faele(sethala_tirišo_Akhaebe).equals(sethala_tirišo_haše)) throw new IOException("QEMU SHA-256 불일치");
                ntšha(sethala_tirišo_Akhaebe,mothopo_boleng.resolve("host")); Files.writeString(실행기표식,sethala_tirišo_haše + "\n");
            }
            환경.put("QEMU_AARCH64",tirišo_sethala_tirišo.toString());
        }
        MessageDigest 계산 = MessageDigest.getInstance("SHA-256"); Collections.sort(소유파일들);
        for (String Leina : 소유파일들) { 계산.update(Leina.getBytes(StandardCharsets.UTF_8)); 계산.update(Files.readAllBytes(내부경로(mohlodi_mohlare,Leina))); }
        계산.update("ip.conf\0".getBytes(StandardCharsets.UTF_8)); 계산.update(Files.readAllBytes(ipConfig));
        String mohlodi_haše = haše_SMS(계산.digest()); Path 빌드표식 = khenele_boleng.resolve("build/worldos-source.sha256");
        if (Mogato.equals("build") || !Files.isRegularFile(빌드표식) || !Files.readString(빌드표식).trim().equals(mohlodi_haše)) {
            호출(khenele_boleng,내부경로(khenele_boleng,(String)Dipeakanyo.get("builder")),Collections.emptyList(),환경);
            Files.writeString(빌드표식,mohlodi_haše + "\n");
        }
        List<String> 추가인수 = new ArrayList<>(Arrays.asList(인수).subList(1,인수.length));
        if (Mogato.equals("run") || Mogato.equals("desktop")) {
            if (Mogato.equals("desktop")) 추가인수.add(0,"--desktop");
            호출(khenele_boleng,내부경로(khenele_boleng,(String)Dipeakanyo.get("runner")),추가인수,환경);
        } else if (Mogato.equals("image")) 호출(khenele_boleng,내부경로(khenele_boleng,(String)Dipeakanyo.get("image_builder")),추가인수,환경);
        else if (Mogato.equals("test-system")) {
            추가인수.add(0,기준.toString()); 추가인수.add(0,"--edition");
            호출(khenele_boleng,내부경로(khenele_boleng,(String)Dipeakanyo.get("system_tester")),추가인수,환경);
        }
    }
}
