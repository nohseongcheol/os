// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.security.MessageDigest;
import java.util.*;

/** 독립 국가판의 의존성 검사·복원·బిల్డ్_సిస్టం·실행을 맡는 హోస్ట్ Java ఉపకరణాలు. */
public final class 국가실행기 {
    static final class డేటా_పార్సర్ {
        final String వనరు; int స్థానము;
        డేటా_పార్సర్(String పాఠ్యము) { వనరు = పాఠ్యము; }
        void 빈칸() { while (స్థానము < వనరు.length() && Character.isWhitespace(వనరు.charAt(స్థానము))) స్థానము++; }
        Object చదువు() {
            빈칸(); char అక్షరం_మూల్యం = వనరు.charAt(స్థానము++);
            if (అక్షరం_మూల్యం == '{') {
                Map<String,Object> ప్రమాణం = new LinkedHashMap<>(); 빈칸();
                if (వనరు.charAt(స్థానము) == '}') { స్థానము++; return ప్రమాణం; }
                while (true) {
                    String పేరు = (String)చదువు(); 빈칸(); if (వనరు.charAt(స్థానము++) != ':') throw new IllegalArgumentException("డేటా డెలీమీటర్_మూల్యం దోషం");
                    ప్రమాణం.put(పేరు, చదువు()); 빈칸(); char డెలీమీటర్_మూల్యం = వనరు.charAt(స్థానము++);
                    if (డెలీమీటర్_మూల్యం == '}') return ప్రమాణం; if (డెలీమీటర్_మూల్యం != ',') throw new IllegalArgumentException("డేటా డెలీమీటర్_మూల్యం దోషం");
                }
            }
            if (అక్షరం_మూల్యం == '[') {
                List<Object> ప్రమాణం = new ArrayList<>(); 빈칸();
                if (వనరు.charAt(స్థానము) == ']') { స్థానము++; return ప్రమాణం; }
                while (true) {
                    ప్రమాణం.add(చదువు()); 빈칸(); char డెలీమీటర్_మూల్యం = వనరు.charAt(స్థానము++);
                    if (డెలీమీటర్_మూల్యం == ']') return ప్రమాణం; if (డెలీమీటర్_మూల్యం != ',') throw new IllegalArgumentException("డేటా డెలీమీటర్_మూల్యం దోషం");
                }
            }
            if (అక్షరం_మూల్యం == '"') {
                StringBuilder ప్రమాణం = new StringBuilder();
                while (true) {
                    char తదుపరి_అంశం = వనరు.charAt(స్థానము++); if (తదుపరి_అంశం == '"') return ప్రమాణం.toString();
                    if (తదుపరి_అంశం == '\\') {
                        తదుపరి_అంశం = వనరు.charAt(స్థానము++);
                        if (తదుపరి_అంశం == 'u') { ప్రమాణం.append((char)Integer.parseInt(వనరు.substring(స్థానము, స్థానము + 4),16)); స్థానము += 4; continue; }
                        if (తదుపరి_అంశం == 'n') తదుపరి_అంశం = '\n'; else if (తదుపరి_అంశం == 'r') తదుపరి_అంశం = '\r'; else if (తదుపరి_అంశం == 't') తదుపరి_అంశం = '\t';
                        else if (తదుపరి_అంశం == 'b') తదుపరి_అంశం = '\b'; else if (తదుపరి_అంశం == 'f') తదుపరి_అంశం = '\f';
                        else if (తదుపరి_అంశం != '"' && తదుపరి_అంశం != '\\' && తదుపరి_అంశం != '/') throw new IllegalArgumentException("문자 이스케이프 దోషం");
                    }
                    ప్రమాణం.append(తదుపరి_అంశం);
                }
            }
            int నడుపుము = స్థానము - 1;
            while (స్థానము < వనరు.length() && ",]} \t\r\n".indexOf(వనరు.charAt(స్థానము)) < 0) స్థానము++;
            String మూల్యం = వనరు.substring(నడుపుము, స్థానము);
            if (మూల్యం.equals("true")) return Boolean.TRUE; if (మూల్యం.equals("false")) return Boolean.FALSE; if (మూల్యం.equals("null")) return null;
            return Double.valueOf(మూల్యం);
        }
    }
    static String హాష్_ఫైలు(Path పాత్) throws Exception {
        MessageDigest 계산 = MessageDigest.getInstance("SHA-256"); byte[] డేటా = new byte[1024 * 1024];
        try (InputStream 입력 = Files.newInputStream(పాత్)) { for (int పొడవు_మూల్యం; (పొడవు_మూల్యం = 입력.read(డేటా)) >= 0;) 계산.update(డేటా,0,పొడవు_మూల్యం); }
        return హాష్_పాఠం(계산.digest());
    }
    static String హాష్_పాఠం(byte[] డేటా) {
        StringBuilder పాఠ్యము = new StringBuilder(); for (byte మూల్యం : డేటా) పాఠ్యము.append(String.format(Locale.ROOT,"%02x",మూల్యం & 255)); return పాఠ్యము.toString();
    }
    static Path 내부경로(Path ప్రొజెక్ట్_మూలం, String పేరు) {
        Path ప్రమాణం = ప్రొజెక్ట్_మూలం.resolve(పేరు).normalize();
        if (పేరు.isEmpty() || Paths.get(పేరు).isAbsolute() || !ప్రమాణం.startsWith(ప్రొజెక్ట్_మూలం) || పేరు.indexOf('\\') >= 0)
            throw new IllegalArgumentException("범위를 벗어난 పాత్: " + పేరు);
        for (Path 부분 : Paths.get(పేరు)) if (부분.toString().equals("..")) throw new IllegalArgumentException("상위 పాత్ 금지: " + పేరు);
        for (Path 현재 = ప్రమాణం; 현재 != null && 현재.startsWith(ప్రొజెక్ట్_మూలం); 현재 = 현재.getParent())
            if (Files.isSymbolicLink(현재)) throw new IllegalArgumentException("의존성 경로의 링크 금지: " + పేరు);
        return ప్రమాణం;
    }
    static String 명령출력(List<String> ఆదేశము) throws Exception {
        Process విధానం_మూల్యం = new ProcessBuilder(ఆదేశము).redirectError(ProcessBuilder.Redirect.INHERIT).start();
        String ప్రమాణం = new String(విధానం_మూల్యం.getInputStream().readAllBytes(),StandardCharsets.UTF_8);
        if (విధానం_మూల్యం.waitFor() != 0) throw new IOException("ఆదేశము వైఫల్యం_మూల్యం: " + ఆదేశము.get(0)); return ప్రమాణం;
    }
    static void ఉద్ధరణ(Path ఆర్కైవ్_మూల్యం, Path గమ్యం_మూల్యం) throws Exception {
        for (String పేరు : 명령출력(Arrays.asList("tar","-tzf",ఆర్కైవ్_మూల్యం.toString())).split("\n")) 내부경로(గమ్యం_మూల్యం, పేరు);
        for (String పంక్తి : 명령출력(Arrays.asList("tar","-tvzf",ఆర్కైవ్_మూల్యం.toString())).split("\n"))
            if (!పంక్తి.isEmpty() && పంక్తి.charAt(0) != '-' && పంక్తి.charAt(0) != 'd') throw new IOException("외부 링크 또는 특수 파일을 포함한 의존성");
        Files.createDirectories(గమ్యం_మూల్యం);
        int స్థితి_మూల్యం = new ProcessBuilder("tar","--no-same-owner","--no-same-permissions","-xzf",ఆర్కైవ్_మూల్యం.toString(),"-C",గమ్యం_మూల్యం.toString()).inheritIO().start().waitFor();
        if (స్థితి_మూల్యం != 0) throw new IOException("의존성 ఆర్కైవ్_మూల్యం విడుదల_నిల్వ వైఫల్యం_మూల్యం");
    }
    static void 호출(Path 작업경로, Path ఉపకరణాలు, List<String> 인수, Map<String,String> 환경) throws Exception {
        List<String> ఆదేశము = new ArrayList<>(Arrays.asList("python3", ఉపకరణాలు.toString())); ఆదేశము.addAll(인수);
        ProcessBuilder అమలు_చేయి_ఆదేశం = new ProcessBuilder(ఆదేశము).directory(작업경로.toFile()).inheritIO(); అమలు_చేయి_ఆదేశం.environment().putAll(환경);
        int స్థితి_మూల్యం = అమలు_చేయి_ఆదేశం.start().waitFor(); if (స్థితి_మూల్యం != 0) throw new IOException("ఉపకరణాలు వైఫల్యం_మూల్యం: " + ఉపకరణాలు + " (" + స్థితి_మూల్యం + ")");
    }
    @SuppressWarnings("unchecked")
    public static void main(String[] 인수) throws Exception {
        if (인수.length < 1) throw new IllegalArgumentException("build, run, desktop, image, check, test-system 중 동작을 지정하세요");
        String చర్య = 인수[0];
        if (!Arrays.asList("build","run","desktop","image","check","test-system").contains(చర్య)) throw new IllegalArgumentException("알 수 없는 చర్య");
        Path ప్రొజెక్ట్_మూలం = Paths.get(System.getProperty("worldos.edition.root")).toAbsolutePath().normalize();
        Map<String,Object> అమరికలు = (Map<String,Object>)new డేటా_పార్సర్(Files.readString(ప్రొజెక్ట్_మూలం.resolve("native.json"),StandardCharsets.UTF_8)).చదువు();
        Path మూలం_వృక్షాకృతి = 내부경로(ప్రొజెక్ట్_మూలం,(String)అమరికలు.get("source")), కెర్నల్_మూల్యం = 내부경로(మూలం_వృక్షాకృతి,(String)అమరికలు.get("native"));
        List<String> 소유파일들 = (List<String>)(List<?>)అమరికలు.get("owned_files");
        for (String పేరు : 소유파일들) if (!Files.isRegularFile(내부경로(మూలం_వృక్షాకృతి,పేరు))) throw new IOException("మూలం_వృక్షాకృతి 없음: " + పేరు);
        if (చర్య.equals("check")) { System.out.println(అమరికలు.get("country") + " " + అమరికలు.get("language") + " 독립 మూలం_వృక్షాకృతి సరిచూడు 완료"); return; }
        String 자원상대 = (String)అమరికలు.getOrDefault("resource_root", ".");
        if (!자원상대.equals(".") && !자원상대.equals("..")) throw new IllegalArgumentException("의존성 ప్రొజెక్ట్_మూలం పాత్ దోషం");
        Path వనరు_మూల్యం = ప్రొజెక్ట్_మూలం.resolve(자원상대).normalize(); Path ఆర్కైవ్_మూల్యం = వనరు_మూల్యం.resolve("native-vendor.tar.gz");
        String 기대해시 = (String)అమరికలు.get("vendor_sha256");
        if (!హాష్_ఫైలు(ఆర్కైవ్_మూల్యం).equals(기대해시)) throw new IOException("의존성 SHA-256 불일치");
        Path 표식 = మూలం_వృక్షాకృతి.resolve(".vendor-sha256");
        if (!Files.isRegularFile(표식) || !Files.readString(표식).trim().equals(기대해시)) { ఉద్ధరణ(ఆర్కైవ్_మూల్యం, మూలం_వృక్షాకృతి); Files.writeString(표식,기대해시 + "\n"); }
        Map<String,String> 환경 = new HashMap<>(System.getenv());
        Path ipConfig = null;
        if (환경.containsKey("IP_CONFIG")) ipConfig = Paths.get(환경.get("IP_CONFIG")).toAbsolutePath().normalize();
        else for (Path parent = ప్రొజెక్ట్_మూలం; parent != null; parent = parent.getParent()) {
            if (Files.isRegularFile(parent.resolve("ip.conf"))) { ipConfig = parent.resolve("ip.conf"); break; }
        }
        if (ipConfig == null) ipConfig = మూలం_వృక్షాకృతి.resolve("ip.conf");
        if (!Files.isRegularFile(ipConfig)) throw new IOException("Missing ip.conf: " + ipConfig);
        환경.put("IP_CONFIG", ipConfig.toString());
        if (Arrays.asList("run","desktop","test-system").contains(చర్య) && !환경.containsKey("QEMU_AARCH64")) {
            Path అనువర్తనం_లాంచర్ = వనరు_మూల్యం.resolve("host/qemu"), 실행기표식 = వనరు_మూల్యం.resolve("host/.qemu-sha256");
            String లాంచర్_హాష్ = (String)అమరికలు.get("qemu_sha256");
            if (!Files.isRegularFile(అనువర్తనం_లాంచర్) || !Files.isRegularFile(실행기표식) || !Files.readString(실행기표식).trim().equals(లాంచర్_హాష్)) {
                Path లాంచర్_ఆర్కైవ్ = వనరు_మూల్యం.resolve("qemu-host.tar.gz"); if (!హాష్_ఫైలు(లాంచర్_ఆర్కైవ్).equals(లాంచర్_హాష్)) throw new IOException("QEMU SHA-256 불일치");
                ఉద్ధరణ(లాంచర్_ఆర్కైవ్,వనరు_మూల్యం.resolve("host")); Files.writeString(실행기표식,లాంచర్_హాష్ + "\n");
            }
            환경.put("QEMU_AARCH64",అనువర్తనం_లాంచర్.toString());
        }
        MessageDigest 계산 = MessageDigest.getInstance("SHA-256"); Collections.sort(소유파일들);
        for (String పేరు : 소유파일들) { 계산.update(పేరు.getBytes(StandardCharsets.UTF_8)); 계산.update(Files.readAllBytes(내부경로(మూలం_వృక్షాకృతి,పేరు))); }
        계산.update("ip.conf\0".getBytes(StandardCharsets.UTF_8)); 계산.update(Files.readAllBytes(ipConfig));
        String మూలం_హాష్ = హాష్_పాఠం(계산.digest()); Path 빌드표식 = కెర్నల్_మూల్యం.resolve("build/worldos-source.sha256");
        if (చర్య.equals("build") || !Files.isRegularFile(빌드표식) || !Files.readString(빌드표식).trim().equals(మూలం_హాష్)) {
            호출(కెర్నల్_మూల్యం,내부경로(కెర్నల్_మూల్యం,(String)అమరికలు.get("builder")),Collections.emptyList(),환경);
            Files.writeString(빌드표식,మూలం_హాష్ + "\n");
        }
        List<String> 추가인수 = new ArrayList<>(Arrays.asList(인수).subList(1,인수.length));
        if (చర్య.equals("run") || చర్య.equals("desktop")) {
            if (చర్య.equals("desktop")) 추가인수.add(0,"--desktop");
            호출(కెర్నల్_మూల్యం,내부경로(కెర్నల్_మూల్యం,(String)అమరికలు.get("runner")),추가인수,환경);
        } else if (చర్య.equals("image")) 호출(కెర్నల్_మూల్యం,내부경로(కెర్నల్_మూల్యం,(String)అమరికలు.get("image_builder")),추가인수,환경);
        else if (చర్య.equals("test-system")) {
            추가인수.add(0,ప్రొజెక్ట్_మూలం.toString()); 추가인수.add(0,"--edition");
            호출(కెర్నల్_మూల్యం,내부경로(కెర్నల్_మూల్యం,(String)అమరికలు.get("system_tester")),추가인수,환경);
        }
    }
}
