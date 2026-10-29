// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.security.MessageDigest;
import java.util.*;

/** 독립 국가판의 의존성 검사·복원·хувилбар_систем·실행을 맡는 хост Java Хэрэгслүүд. */
public final class 국가실행기 {
    static final class 자료해석기 {
        final String ЭХ; int 위치;
        자료해석기(String Бичвэр) { ЭХ = Бичвэр; }
        void 빈칸() { while (위치 < ЭХ.length() && Character.isWhitespace(ЭХ.charAt(위치))) 위치++; }
        Object Унших() {
            빈칸(); char тэмдэгт_утга = ЭХ.charAt(위치++);
            if (тэмдэгт_утга == '{') {
                Map<String,Object> 결과 = new LinkedHashMap<>(); 빈칸();
                if (ЭХ.charAt(위치) == '}') { 위치++; return 결과; }
                while (true) {
                    String Нэр = (String)Унших(); 빈칸(); if (ЭХ.charAt(위치++) != ':') throw new IllegalArgumentException("өгөгдөл тусгаарлах_тэмдэгт_утга Алдаа");
                    결과.put(Нэр, Унших()); 빈칸(); char тусгаарлах_тэмдэгт_утга = ЭХ.charAt(위치++);
                    if (тусгаарлах_тэмдэгт_утга == '}') return 결과; if (тусгаарлах_тэмдэгт_утга != ',') throw new IllegalArgumentException("өгөгдөл тусгаарлах_тэмдэгт_утга Алдаа");
                }
            }
            if (тэмдэгт_утга == '[') {
                List<Object> 결과 = new ArrayList<>(); 빈칸();
                if (ЭХ.charAt(위치) == ']') { 위치++; return 결과; }
                while (true) {
                    결과.add(Унших()); 빈칸(); char тусгаарлах_тэмдэгт_утга = ЭХ.charAt(위치++);
                    if (тусгаарлах_тэмдэгт_утга == ']') return 결과; if (тусгаарлах_тэмдэгт_утга != ',') throw new IllegalArgumentException("өгөгдөл тусгаарлах_тэмдэгт_утга Алдаа");
                }
            }
            if (тэмдэгт_утга == '"') {
                StringBuilder 결과 = new StringBuilder();
                while (true) {
                    char 다음 = ЭХ.charAt(위치++); if (다음 == '"') return 결과.toString();
                    if (다음 == '\\') {
                        다음 = ЭХ.charAt(위치++);
                        if (다음 == 'u') { 결과.append((char)Integer.parseInt(ЭХ.substring(위치, 위치 + 4),16)); 위치 += 4; continue; }
                        if (다음 == 'n') 다음 = '\n'; else if (다음 == 'r') 다음 = '\r'; else if (다음 == 't') 다음 = '\t';
                        else if (다음 == 'b') 다음 = '\b'; else if (다음 == 'f') 다음 = '\f';
                        else if (다음 != '"' && 다음 != '\\' && 다음 != '/') throw new IllegalArgumentException("문자 이스케이프 Алдаа");
                    }
                    결과.append(다음);
                }
            }
            int Ажиллуулах = 위치 - 1;
            while (위치 < ЭХ.length() && ",]} \t\r\n".indexOf(ЭХ.charAt(위치)) < 0) 위치++;
            String утга = ЭХ.substring(Ажиллуулах, 위치);
            if (утга.equals("true")) return Boolean.TRUE; if (утга.equals("false")) return Boolean.FALSE; if (утга.equals("null")) return null;
            return Double.valueOf(утга);
        }
    }
    static String Оруулсан_мэдээллийг_өөрчлөх_хэрэгсэл_файл(Path ЗАМ) throws Exception {
        MessageDigest 계산 = MessageDigest.getInstance("SHA-256"); byte[] өгөгдөл = new byte[1024 * 1024];
        try (InputStream 입력 = Files.newInputStream(ЗАМ)) { for (int урт_утга; (урт_утга = 입력.read(өгөгдөл)) >= 0;) 계산.update(өгөгдөл,0,урт_утга); }
        return Оруулсан_мэдээллийг_өөрчлөх_хэрэгсэл_Бичвэр(계산.digest());
    }
    static String Оруулсан_мэдээллийг_өөрчлөх_хэрэгсэл_Бичвэр(byte[] өгөгдөл) {
        StringBuilder Бичвэр = new StringBuilder(); for (byte утга : өгөгдөл) Бичвэр.append(String.format(Locale.ROOT,"%02x",утга & 255)); return Бичвэр.toString();
    }
    static Path 내부경로(Path 기준, String Нэр) {
        Path 결과 = 기준.resolve(Нэр).normalize();
        if (Нэр.isEmpty() || Paths.get(Нэр).isAbsolute() || !결과.startsWith(기준) || Нэр.indexOf('\\') >= 0)
            throw new IllegalArgumentException("범위를 벗어난 ЗАМ: " + Нэр);
        for (Path 부분 : Paths.get(Нэр)) if (부분.toString().equals("..")) throw new IllegalArgumentException("상위 ЗАМ 금지: " + Нэр);
        for (Path 현재 = 결과; 현재 != null && 현재.startsWith(기준); 현재 = 현재.getParent())
            if (Files.isSymbolicLink(현재)) throw new IllegalArgumentException("의존성 경로의 링크 금지: " + Нэр);
        return 결과;
    }
    static String 명령출력(List<String> Тушаал) throws Exception {
        Process үйл_явц_утга = new ProcessBuilder(Тушаал).redirectError(ProcessBuilder.Redirect.INHERIT).start();
        String 결과 = new String(үйл_явц_утга.getInputStream().readAllBytes(),StandardCharsets.UTF_8);
        if (үйл_явц_утга.waitFor() != 0) throw new IOException("Тушаал гэмтэл_утга: " + Тушаал.get(0)); return 결과;
    }
    static void задлах(Path Архив_утга, Path товлосон_газар_утга) throws Exception {
        for (String Нэр : 명령출력(Arrays.asList("tar","-tzf",Архив_утга.toString())).split("\n")) 내부경로(товлосон_газар_утга, Нэр);
        for (String Шугам : 명령출력(Arrays.asList("tar","-tvzf",Архив_утга.toString())).split("\n"))
            if (!Шугам.isEmpty() && Шугам.charAt(0) != '-' && Шугам.charAt(0) != 'd') throw new IOException("외부 링크 또는 특수 파일을 포함한 의존성");
        Files.createDirectories(товлосон_газар_утга);
        int төлөв_утга = new ProcessBuilder("tar","--no-same-owner","--no-same-permissions","-xzf",Архив_утга.toString(),"-C",товлосон_газар_утга.toString()).inheritIO().start().waitFor();
        if (төлөв_утга != 0) throw new IOException("의존성 Архив_утга гарц_Санах_ой гэмтэл_утга");
    }
    static void 호출(Path 작업경로, Path Хэрэгслүүд, List<String> 인수, Map<String,String> 환경) throws Exception {
        List<String> Тушаал = new ArrayList<>(Arrays.asList("python3", Хэрэгслүүд.toString())); Тушаал.addAll(인수);
        ProcessBuilder Гүйцэтгэх_команд = new ProcessBuilder(Тушаал).directory(작업경로.toFile()).inheritIO(); Гүйцэтгэх_команд.environment().putAll(환경);
        int төлөв_утга = Гүйцэтгэх_команд.start().waitFor(); if (төлөв_утга != 0) throw new IOException("Хэрэгслүүд гэмтэл_утга: " + Хэрэгслүүд + " (" + төлөв_утга + ")");
    }
    @SuppressWarnings("unchecked")
    public static void main(String[] 인수) throws Exception {
        if (인수.length < 1) throw new IllegalArgumentException("build, run, desktop, image, check, test-system 중 동작을 지정하세요");
        String Үйлдэл = 인수[0];
        if (!Arrays.asList("build","run","desktop","image","check","test-system").contains(Үйлдэл)) throw new IllegalArgumentException("알 수 없는 Үйлдэл");
        Path 기준 = Paths.get(System.getProperty("worldos.edition.root")).toAbsolutePath().normalize();
        Map<String,Object> Тохиргоо = (Map<String,Object>)new 자료해석기(Files.readString(기준.resolve("native.json"),StandardCharsets.UTF_8)).Унших();
        Path эх_мод = 내부경로(기준,(String)Тохиргоо.get("source")), кернел_утга = 내부경로(эх_мод,(String)Тохиргоо.get("native"));
        List<String> 소유파일들 = (List<String>)(List<?>)Тохиргоо.get("owned_files");
        for (String Нэр : 소유파일들) if (!Files.isRegularFile(내부경로(эх_мод,Нэр))) throw new IOException("эх_мод 없음: " + Нэр);
        if (Үйлдэл.equals("check")) { System.out.println(Тохиргоо.get("country") + " " + Тохиргоо.get("language") + " 독립 эх_мод шалгах 완료"); return; }
        String 자원상대 = (String)Тохиргоо.getOrDefault("resource_root", ".");
        if (!자원상대.equals(".") && !자원상대.equals("..")) throw new IllegalArgumentException("의존성 기준 ЗАМ Алдаа");
        Path хэрэгсэл_утга = 기준.resolve(자원상대).normalize(); Path Архив_утга = хэрэгсэл_утга.resolve("native-vendor.tar.gz");
        String 기대해시 = (String)Тохиргоо.get("vendor_sha256");
        if (!Оруулсан_мэдээллийг_өөрчлөх_хэрэгсэл_файл(Архив_утга).equals(기대해시)) throw new IOException("의존성 SHA-256 불일치");
        Path 표식 = эх_мод.resolve(".vendor-sha256");
        if (!Files.isRegularFile(표식) || !Files.readString(표식).trim().equals(기대해시)) { задлах(Архив_утга, эх_мод); Files.writeString(표식,기대해시 + "\n"); }
        Map<String,String> 환경 = new HashMap<>(System.getenv());
        Path ipConfig = null;
        if (환경.containsKey("IP_CONFIG")) ipConfig = Paths.get(환경.get("IP_CONFIG")).toAbsolutePath().normalize();
        else for (Path parent = 기준; parent != null; parent = parent.getParent()) {
            if (Files.isRegularFile(parent.resolve("ip.conf"))) { ipConfig = parent.resolve("ip.conf"); break; }
        }
        if (ipConfig == null) ipConfig = эх_мод.resolve("ip.conf");
        if (!Files.isRegularFile(ipConfig)) throw new IOException("Missing ip.conf: " + ipConfig);
        환경.put("IP_CONFIG", ipConfig.toString());
        if (Arrays.asList("run","desktop","test-system").contains(Үйлдэл) && !환경.containsKey("QEMU_AARCH64")) {
            Path програм_гишүүн = хэрэгсэл_утга.resolve("host/qemu"), 실행기표식 = хэрэгсэл_утга.resolve("host/.qemu-sha256");
            String гишүүн_Оруулсан_мэдээллийг_өөрчлөх_хэрэгсэл = (String)Тохиргоо.get("qemu_sha256");
            if (!Files.isRegularFile(програм_гишүүн) || !Files.isRegularFile(실행기표식) || !Files.readString(실행기표식).trim().equals(гишүүн_Оруулсан_мэдээллийг_өөрчлөх_хэрэгсэл)) {
                Path гишүүн_Архив = хэрэгсэл_утга.resolve("qemu-host.tar.gz"); if (!Оруулсан_мэдээллийг_өөрчлөх_хэрэгсэл_файл(гишүүн_Архив).equals(гишүүн_Оруулсан_мэдээллийг_өөрчлөх_хэрэгсэл)) throw new IOException("QEMU SHA-256 불일치");
                задлах(гишүүн_Архив,хэрэгсэл_утга.resolve("host")); Files.writeString(실행기표식,гишүүн_Оруулсан_мэдээллийг_өөрчлөх_хэрэгсэл + "\n");
            }
            환경.put("QEMU_AARCH64",програм_гишүүн.toString());
        }
        MessageDigest 계산 = MessageDigest.getInstance("SHA-256"); Collections.sort(소유파일들);
        for (String Нэр : 소유파일들) { 계산.update(Нэр.getBytes(StandardCharsets.UTF_8)); 계산.update(Files.readAllBytes(내부경로(эх_мод,Нэр))); }
        계산.update("ip.conf\0".getBytes(StandardCharsets.UTF_8)); 계산.update(Files.readAllBytes(ipConfig));
        String эх_Оруулсан_мэдээллийг_өөрчлөх_хэрэгсэл = Оруулсан_мэдээллийг_өөрчлөх_хэрэгсэл_Бичвэр(계산.digest()); Path 빌드표식 = кернел_утга.resolve("build/worldos-source.sha256");
        if (Үйлдэл.equals("build") || !Files.isRegularFile(빌드표식) || !Files.readString(빌드표식).trim().equals(эх_Оруулсан_мэдээллийг_өөрчлөх_хэрэгсэл)) {
            호출(кернел_утга,내부경로(кернел_утга,(String)Тохиргоо.get("builder")),Collections.emptyList(),환경);
            Files.writeString(빌드표식,эх_Оруулсан_мэдээллийг_өөрчлөх_хэрэгсэл + "\n");
        }
        List<String> 추가인수 = new ArrayList<>(Arrays.asList(인수).subList(1,인수.length));
        if (Үйлдэл.equals("run") || Үйлдэл.equals("desktop")) {
            if (Үйлдэл.equals("desktop")) 추가인수.add(0,"--desktop");
            호출(кернел_утга,내부경로(кернел_утга,(String)Тохиргоо.get("runner")),추가인수,환경);
        } else if (Үйлдэл.equals("image")) 호출(кернел_утга,내부경로(кернел_утга,(String)Тохиргоо.get("image_builder")),추가인수,환경);
        else if (Үйлдэл.equals("test-system")) {
            추가인수.add(0,기준.toString()); 추가인수.add(0,"--edition");
            호출(кернел_утга,내부경로(кернел_утга,(String)Тохиргоо.get("system_tester")),추가인수,환경);
        }
    }
}
