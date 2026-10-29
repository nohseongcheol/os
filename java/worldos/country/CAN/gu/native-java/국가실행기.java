// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.security.MessageDigest;
import java.util.*;

/** 독립 국가판의 의존성 검사·복원·બિલ્ડ_સિસ્ટમ·실행을 맡는 હોસ્ટ Java ઉપકરણો. */
public final class 국가실행기 {
    static final class 자료해석기 {
        final String સ્રોત; int સ્થાન;
        자료해석기(String લખાણ) { સ્રોત = લખાણ; }
        void 빈칸() { while (સ્થાન < સ્રોત.length() && Character.isWhitespace(સ્રોત.charAt(સ્થાન))) સ્થાન++; }
        Object વાંચો() {
            빈칸(); char વર્ણ_મૂલ્ય = સ્રોત.charAt(સ્થાન++);
            if (વર્ણ_મૂલ્ય == '{') {
                Map<String,Object> પરિમાણ = new LinkedHashMap<>(); 빈칸();
                if (સ્રોત.charAt(સ્થાન) == '}') { સ્થાન++; return પરિમાણ; }
                while (true) {
                    String નામ = (String)વાંચો(); 빈칸(); if (સ્રોત.charAt(સ્થાન++) != ':') throw new IllegalArgumentException("ડેટા સીમાનિર્ધારક_મૂલ્ય ભૂલ");
                    પરિમાણ.put(નામ, વાંચો()); 빈칸(); char સીમાનિર્ધારક_મૂલ્ય = સ્રોત.charAt(સ્થાન++);
                    if (સીમાનિર્ધારક_મૂલ્ય == '}') return પરિમાણ; if (સીમાનિર્ધારક_મૂલ્ય != ',') throw new IllegalArgumentException("ડેટા સીમાનિર્ધારક_મૂલ્ય ભૂલ");
                }
            }
            if (વર્ણ_મૂલ્ય == '[') {
                List<Object> પરિમાણ = new ArrayList<>(); 빈칸();
                if (સ્રોત.charAt(સ્થાન) == ']') { સ્થાન++; return પરિમાણ; }
                while (true) {
                    પરિમાણ.add(વાંચો()); 빈칸(); char સીમાનિર્ધારક_મૂલ્ય = સ્રોત.charAt(સ્થાન++);
                    if (સીમાનિર્ધારક_મૂલ્ય == ']') return પરિમાણ; if (સીમાનિર્ધારક_મૂલ્ય != ',') throw new IllegalArgumentException("ડેટા સીમાનિર્ધારક_મૂલ્ય ભૂલ");
                }
            }
            if (વર્ણ_મૂલ્ય == '"') {
                StringBuilder પરિમાણ = new StringBuilder();
                while (true) {
                    char આગલું_આઇટમ = સ્રોત.charAt(સ્થાન++); if (આગલું_આઇટમ == '"') return પરિમાણ.toString();
                    if (આગલું_આઇટમ == '\\') {
                        આગલું_આઇટમ = સ્રોત.charAt(સ્થાન++);
                        if (આગલું_આઇટમ == 'u') { પરિમાણ.append((char)Integer.parseInt(સ્રોત.substring(સ્થાન, સ્થાન + 4),16)); સ્થાન += 4; continue; }
                        if (આગલું_આઇટમ == 'n') આગલું_આઇટમ = '\n'; else if (આગલું_આઇટમ == 'r') આગલું_આઇટમ = '\r'; else if (આગલું_આઇટમ == 't') આગલું_આઇટમ = '\t';
                        else if (આગલું_આઇટમ == 'b') આગલું_આઇટમ = '\b'; else if (આગલું_આઇટમ == 'f') આગલું_આઇટમ = '\f';
                        else if (આગલું_આઇટમ != '"' && આગલું_આઇટમ != '\\' && આગલું_આઇટમ != '/') throw new IllegalArgumentException("문자 이스케이프 ભૂલ");
                    }
                    પરિમાણ.append(આગલું_આઇટમ);
                }
            }
            int ચલાવો_2 = સ્થાન - 1;
            while (સ્થાન < સ્રોત.length() && ",]} \t\r\n".indexOf(સ્રોત.charAt(સ્થાન)) < 0) સ્થાન++;
            String મૂલ્ય = સ્રોત.substring(ચલાવો_2, સ્થાન);
            if (મૂલ્ય.equals("true")) return Boolean.TRUE; if (મૂલ્ય.equals("false")) return Boolean.FALSE; if (મૂલ્ય.equals("null")) return null;
            return Double.valueOf(મૂલ્ય);
        }
    }
    static String હૅશ_ફાઇલ(Path પથ) throws Exception {
        MessageDigest 계산 = MessageDigest.getInstance("SHA-256"); byte[] ડેટા = new byte[1024 * 1024];
        try (InputStream 입력 = Files.newInputStream(પથ)) { for (int લંબાઈ_મૂલ્ય; (લંબાઈ_મૂલ્ય = 입력.read(ડેટા)) >= 0;) 계산.update(ડેટા,0,લંબાઈ_મૂલ્ય); }
        return હૅશ_પાઠ(계산.digest());
    }
    static String હૅશ_પાઠ(byte[] ડેટા) {
        StringBuilder લખાણ = new StringBuilder(); for (byte મૂલ્ય : ડેટા) લખાણ.append(String.format(Locale.ROOT,"%02x",મૂલ્ય & 255)); return લખાણ.toString();
    }
    static Path 내부경로(Path પ્રોજેક્ટ_રૂટ, String નામ) {
        Path પરિમાણ = પ્રોજેક્ટ_રૂટ.resolve(નામ).normalize();
        if (નામ.isEmpty() || Paths.get(નામ).isAbsolute() || !પરિમાણ.startsWith(પ્રોજેક્ટ_રૂટ) || નામ.indexOf('\\') >= 0)
            throw new IllegalArgumentException("범위를 벗어난 પથ: " + નામ);
        for (Path 부분 : Paths.get(નામ)) if (부분.toString().equals("..")) throw new IllegalArgumentException("상위 પથ 금지: " + નામ);
        for (Path 현재 = પરિમાણ; 현재 != null && 현재.startsWith(પ્રોજેક્ટ_રૂટ); 현재 = 현재.getParent())
            if (Files.isSymbolicLink(현재)) throw new IllegalArgumentException("의존성 경로의 링크 금지: " + નામ);
        return પરિમાણ;
    }
    static String 명령출력(List<String> આદેશ) throws Exception {
        Process પ્રક્રિયા_મૂલ્ય = new ProcessBuilder(આદેશ).redirectError(ProcessBuilder.Redirect.INHERIT).start();
        String પરિમાણ = new String(પ્રક્રિયા_મૂલ્ય.getInputStream().readAllBytes(),StandardCharsets.UTF_8);
        if (પ્રક્રિયા_મૂલ્ય.waitFor() != 0) throw new IOException("આદેશ નિષ્ફળતા_મૂલ્ય: " + આદેશ.get(0)); return પરિમાણ;
    }
    static void બહાર_કાઢો(Path સંગ્રહ_મૂલ્ય, Path ગંતવ્ય_મૂલ્ય) throws Exception {
        for (String નામ : 명령출력(Arrays.asList("tar","-tzf",સંગ્રહ_મૂલ્ય.toString())).split("\n")) 내부경로(ગંતવ્ય_મૂલ્ય, નામ);
        for (String લાઇન : 명령출력(Arrays.asList("tar","-tvzf",સંગ્રહ_મૂલ્ય.toString())).split("\n"))
            if (!લાઇન.isEmpty() && લાઇન.charAt(0) != '-' && લાઇન.charAt(0) != 'd') throw new IOException("외부 링크 또는 특수 파일을 포함한 의존성");
        Files.createDirectories(ગંતવ્ય_મૂલ્ય);
        int સ્થિતિ_મૂલ્ય_e10195a1 = new ProcessBuilder("tar","--no-same-owner","--no-same-permissions","-xzf",સંગ્રહ_મૂલ્ય.toString(),"-C",ગંતવ્ય_મૂલ્ય.toString()).inheritIO().start().waitFor();
        if (સ્થિતિ_મૂલ્ય_e10195a1 != 0) throw new IOException("의존성 સંગ્રહ_મૂલ્ય રિલીઝ_સંગ્રહ નિષ્ફળતા_મૂલ્ય");
    }
    static void 호출(Path 작업경로, Path ઉપકરણો, List<String> દલીલો, Map<String,String> 환경) throws Exception {
        List<String> આદેશ = new ArrayList<>(Arrays.asList("python3", ઉપકરણો.toString())); આદેશ.addAll(દલીલો);
        ProcessBuilder અમલ_કરો_આદેશ = new ProcessBuilder(આદેશ).directory(작업경로.toFile()).inheritIO(); અમલ_કરો_આદેશ.environment().putAll(환경);
        int સ્થિતિ_મૂલ્ય_e10195a1 = અમલ_કરો_આદેશ.start().waitFor(); if (સ્થિતિ_મૂલ્ય_e10195a1 != 0) throw new IOException("ઉપકરણો નિષ્ફળતા_મૂલ્ય: " + ઉપકરણો + " (" + સ્થિતિ_મૂલ્ય_e10195a1 + ")");
    }
    @SuppressWarnings("unchecked")
    public static void main(String[] દલીલો) throws Exception {
        if (દલીલો.length < 1) throw new IllegalArgumentException("build, run, desktop, image, check, test-system 중 동작을 지정하세요");
        String ક્રિયા = દલીલો[0];
        if (!Arrays.asList("build","run","desktop","image","check","test-system").contains(ક્રિયા)) throw new IllegalArgumentException("알 수 없는 ક્રિયા");
        Path પ્રોજેક્ટ_રૂટ = Paths.get(System.getProperty("worldos.edition.root")).toAbsolutePath().normalize();
        Map<String,Object> સુયોજના = (Map<String,Object>)new 자료해석기(Files.readString(પ્રોજેક્ટ_રૂટ.resolve("native.json"),StandardCharsets.UTF_8)).વાંચો();
        Path સ્રોત_ટ્રી = 내부경로(પ્રોજેક્ટ_રૂટ,(String)સુયોજના.get("source")), કર્નેલ_મૂલ્ય = 내부경로(સ્રોત_ટ્રી,(String)સુયોજના.get("native"));
        List<String> 소유파일들 = (List<String>)(List<?>)સુયોજના.get("owned_files");
        for (String નામ : 소유파일들) if (!Files.isRegularFile(내부경로(સ્રોત_ટ્રી,નામ))) throw new IOException("સ્રોત_ટ્રી 없음: " + નામ);
        if (ક્રિયા.equals("check")) { System.out.println(સુયોજના.get("country") + " " + સુયોજના.get("language") + " 독립 સ્રોત_ટ્રી ચકાસવું 완료"); return; }
        String 자원상대 = (String)સુયોજના.getOrDefault("resource_root", ".");
        if (!자원상대.equals(".") && !자원상대.equals("..")) throw new IllegalArgumentException("의존성 પ્રોજેક્ટ_રૂટ પથ ભૂલ");
        Path સાધન_મૂલ્ય = પ્રોજેક્ટ_રૂટ.resolve(자원상대).normalize(); Path સંગ્રહ_મૂલ્ય = સાધન_મૂલ્ય.resolve("native-vendor.tar.gz");
        String 기대해시 = (String)સુયોજના.get("vendor_sha256");
        if (!હૅશ_ફાઇલ(સંગ્રહ_મૂલ્ય).equals(기대해시)) throw new IOException("의존성 SHA-256 불일치");
        Path 표식 = સ્રોત_ટ્રી.resolve(".vendor-sha256");
        if (!Files.isRegularFile(표식) || !Files.readString(표식).trim().equals(기대해시)) { બહાર_કાઢો(સંગ્રહ_મૂલ્ય, સ્રોત_ટ્રી); Files.writeString(표식,기대해시 + "\n"); }
        Map<String,String> 환경 = new HashMap<>(System.getenv());
        Path ipConfig = null;
        if (환경.containsKey("IP_CONFIG")) ipConfig = Paths.get(환경.get("IP_CONFIG")).toAbsolutePath().normalize();
        else for (Path parent = પ્રોજેક્ટ_રૂટ; parent != null; parent = parent.getParent()) {
            if (Files.isRegularFile(parent.resolve("ip.conf"))) { ipConfig = parent.resolve("ip.conf"); break; }
        }
        if (ipConfig == null) ipConfig = સ્રોત_ટ્રી.resolve("ip.conf");
        if (!Files.isRegularFile(ipConfig)) throw new IOException("Missing ip.conf: " + ipConfig);
        환경.put("IP_CONFIG", ipConfig.toString());
        if (Arrays.asList("run","desktop","test-system").contains(ક્રિયા) && !환경.containsKey("QEMU_AARCH64")) {
            Path એપ્લિકેશન_લૉન્ચર = સાધન_મૂલ્ય.resolve("host/qemu"), 실행기표식 = સાધન_મૂલ્ય.resolve("host/.qemu-sha256");
            String લૉન્ચર_હૅશ = (String)સુયોજના.get("qemu_sha256");
            if (!Files.isRegularFile(એપ્લિકેશન_લૉન્ચર) || !Files.isRegularFile(실행기표식) || !Files.readString(실행기표식).trim().equals(લૉન્ચર_હૅશ)) {
                Path લૉન્ચર_સંગ્રહ = સાધન_મૂલ્ય.resolve("qemu-host.tar.gz"); if (!હૅશ_ફાઇલ(લૉન્ચર_સંગ્રહ).equals(લૉન્ચર_હૅશ)) throw new IOException("QEMU SHA-256 불일치");
                બહાર_કાઢો(લૉન્ચર_સંગ્રહ,સાધન_મૂલ્ય.resolve("host")); Files.writeString(실행기표식,લૉન્ચર_હૅશ + "\n");
            }
            환경.put("QEMU_AARCH64",એપ્લિકેશન_લૉન્ચર.toString());
        }
        MessageDigest 계산 = MessageDigest.getInstance("SHA-256"); Collections.sort(소유파일들);
        for (String નામ : 소유파일들) { 계산.update(નામ.getBytes(StandardCharsets.UTF_8)); 계산.update(Files.readAllBytes(내부경로(સ્રોત_ટ્રી,નામ))); }
        계산.update("ip.conf\0".getBytes(StandardCharsets.UTF_8)); 계산.update(Files.readAllBytes(ipConfig));
        String સ્રોત_હૅશ = હૅશ_પાઠ(계산.digest()); Path 빌드표식 = કર્નેલ_મૂલ્ય.resolve("build/worldos-source.sha256");
        if (ક્રિયા.equals("build") || !Files.isRegularFile(빌드표식) || !Files.readString(빌드표식).trim().equals(સ્રોત_હૅશ)) {
            호출(કર્નેલ_મૂલ્ય,내부경로(કર્નેલ_મૂલ્ય,(String)સુયોજના.get("builder")),Collections.emptyList(),환경);
            Files.writeString(빌드표식,સ્રોત_હૅશ + "\n");
        }
        List<String> 추가인수 = new ArrayList<>(Arrays.asList(દલીલો).subList(1,દલીલો.length));
        if (ક્રિયા.equals("run") || ક્રિયા.equals("desktop")) {
            if (ક્રિયા.equals("desktop")) 추가인수.add(0,"--desktop");
            호출(કર્નેલ_મૂલ્ય,내부경로(કર્નેલ_મૂલ્ય,(String)સુયોજના.get("runner")),추가인수,환경);
        } else if (ક્રિયા.equals("image")) 호출(કર્નેલ_મૂલ્ય,내부경로(કર્નેલ_મૂલ્ય,(String)સુયોજના.get("image_builder")),추가인수,환경);
        else if (ક્રિયા.equals("test-system")) {
            추가인수.add(0,પ્રોજેક્ટ_રૂટ.toString()); 추가인수.add(0,"--edition");
            호출(કર્નેલ_મૂલ્ય,내부경로(કર્નેલ_મૂલ્ય,(String)સુયોજના.get("system_tester")),추가인수,환경);
        }
    }
}
