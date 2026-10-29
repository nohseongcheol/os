// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.security.MessageDigest;
import java.util.*;

/** 독립 국가판의 의존성 검사·복원·ສ້າງ_ລະບົບ·실행을 맡는 ໂຮສ Java ເຄື່ອງມື. */
public final class 국가실행기 {
    static final class ຂໍ້ມູນ_ຕົວແຍກວິເຄາະ {
        final String ແຫຼ່ງທີ່ມາ; int ຈັດຕໍາແຫນ່ງ;
        ຂໍ້ມູນ_ຕົວແຍກວິເຄາະ(String ຂໍ້ຄວາມ) { ແຫຼ່ງທີ່ມາ = ຂໍ້ຄວາມ; }
        void 빈칸() { while (ຈັດຕໍາແຫນ່ງ < ແຫຼ່ງທີ່ມາ.length() && Character.isWhitespace(ແຫຼ່ງທີ່ມາ.charAt(ຈັດຕໍາແຫນ່ງ))) ຈັດຕໍາແຫນ່ງ++; }
        Object 읽기() {
            빈칸(); char ຕົວອັກສອນ_ຄ່າ = ແຫຼ່ງທີ່ມາ.charAt(ຈັດຕໍາແຫນ່ງ++);
            if (ຕົວອັກສອນ_ຄ່າ == '{') {
                Map<String,Object> ມາດຕະການ = new LinkedHashMap<>(); 빈칸();
                if (ແຫຼ່ງທີ່ມາ.charAt(ຈັດຕໍາແຫນ່ງ) == '}') { ຈັດຕໍາແຫນ່ງ++; return ມາດຕະການ; }
                while (true) {
                    String ຊື່ = (String)읽기(); 빈칸(); if (ແຫຼ່ງທີ່ມາ.charAt(ຈັດຕໍາແຫນ່ງ++) != ':') throw new IllegalArgumentException("ຂໍ້ມູນ ເຄື່ອງຫມາຍຂັ້ນ_ຄ່າ ຂໍ້ຜິດພາດ");
                    ມາດຕະການ.put(ຊື່, 읽기()); 빈칸(); char ເຄື່ອງຫມາຍຂັ້ນ_ຄ່າ = ແຫຼ່ງທີ່ມາ.charAt(ຈັດຕໍາແຫນ່ງ++);
                    if (ເຄື່ອງຫມາຍຂັ້ນ_ຄ່າ == '}') return ມາດຕະການ; if (ເຄື່ອງຫມາຍຂັ້ນ_ຄ່າ != ',') throw new IllegalArgumentException("ຂໍ້ມູນ ເຄື່ອງຫມາຍຂັ້ນ_ຄ່າ ຂໍ້ຜິດພາດ");
                }
            }
            if (ຕົວອັກສອນ_ຄ່າ == '[') {
                List<Object> ມາດຕະການ = new ArrayList<>(); 빈칸();
                if (ແຫຼ່ງທີ່ມາ.charAt(ຈັດຕໍາແຫນ່ງ) == ']') { ຈັດຕໍາແຫນ່ງ++; return ມາດຕະການ; }
                while (true) {
                    ມາດຕະການ.add(읽기()); 빈칸(); char ເຄື່ອງຫມາຍຂັ້ນ_ຄ່າ = ແຫຼ່ງທີ່ມາ.charAt(ຈັດຕໍາແຫນ່ງ++);
                    if (ເຄື່ອງຫມາຍຂັ້ນ_ຄ່າ == ']') return ມາດຕະການ; if (ເຄື່ອງຫມາຍຂັ້ນ_ຄ່າ != ',') throw new IllegalArgumentException("ຂໍ້ມູນ ເຄື່ອງຫມາຍຂັ້ນ_ຄ່າ ຂໍ້ຜິດພາດ");
                }
            }
            if (ຕົວອັກສອນ_ຄ່າ == '"') {
                StringBuilder ມາດຕະການ = new StringBuilder();
                while (true) {
                    char ຕໍ່ໄປ_ລາຍການ = ແຫຼ່ງທີ່ມາ.charAt(ຈັດຕໍາແຫນ່ງ++); if (ຕໍ່ໄປ_ລາຍການ == '"') return ມາດຕະການ.toString();
                    if (ຕໍ່ໄປ_ລາຍການ == '\\') {
                        ຕໍ່ໄປ_ລາຍການ = ແຫຼ່ງທີ່ມາ.charAt(ຈັດຕໍາແຫນ່ງ++);
                        if (ຕໍ່ໄປ_ລາຍການ == 'u') { ມາດຕະການ.append((char)Integer.parseInt(ແຫຼ່ງທີ່ມາ.substring(ຈັດຕໍາແຫນ່ງ, ຈັດຕໍາແຫນ່ງ + 4),16)); ຈັດຕໍາແຫນ່ງ += 4; continue; }
                        if (ຕໍ່ໄປ_ລາຍການ == 'n') ຕໍ່ໄປ_ລາຍການ = '\n'; else if (ຕໍ່ໄປ_ລາຍການ == 'r') ຕໍ່ໄປ_ລາຍການ = '\r'; else if (ຕໍ່ໄປ_ລາຍການ == 't') ຕໍ່ໄປ_ລາຍການ = '\t';
                        else if (ຕໍ່ໄປ_ລາຍການ == 'b') ຕໍ່ໄປ_ລາຍການ = '\b'; else if (ຕໍ່ໄປ_ລາຍການ == 'f') ຕໍ່ໄປ_ລາຍການ = '\f';
                        else if (ຕໍ່ໄປ_ລາຍການ != '"' && ຕໍ່ໄປ_ລາຍການ != '\\' && ຕໍ່ໄປ_ລາຍການ != '/') throw new IllegalArgumentException("문자 이스케이프 ຂໍ້ຜິດພາດ");
                    }
                    ມາດຕະການ.append(ຕໍ່ໄປ_ລາຍການ);
                }
            }
            int ແລ່ນ = ຈັດຕໍາແຫນ່ງ - 1;
            while (ຈັດຕໍາແຫນ່ງ < ແຫຼ່ງທີ່ມາ.length() && ",]} \t\r\n".indexOf(ແຫຼ່ງທີ່ມາ.charAt(ຈັດຕໍາແຫນ່ງ)) < 0) ຈັດຕໍາແຫນ່ງ++;
            String ຄ່າ = ແຫຼ່ງທີ່ມາ.substring(ແລ່ນ, ຈັດຕໍາແຫນ່ງ);
            if (ຄ່າ.equals("true")) return Boolean.TRUE; if (ຄ່າ.equals("false")) return Boolean.FALSE; if (ຄ່າ.equals("null")) return null;
            return Double.valueOf(ຄ່າ);
        }
    }
    static String ແຮຊ_ຟາຍ(Path ທາງໂຄຈອນ) throws Exception {
        MessageDigest 계산 = MessageDigest.getInstance("SHA-256"); byte[] ຂໍ້ມູນ = new byte[1024 * 1024];
        try (InputStream 입력 = Files.newInputStream(ທາງໂຄຈອນ)) { for (int ຄວາມຍາວ_ຄ່າ; (ຄວາມຍາວ_ຄ່າ = 입력.read(ຂໍ້ມູນ)) >= 0;) 계산.update(ຂໍ້ມູນ,0,ຄວາມຍາວ_ຄ່າ); }
        return ແຮຊ_ຂໍ້ຄວາມ(계산.digest());
    }
    static String ແຮຊ_ຂໍ້ຄວາມ(byte[] ຂໍ້ມູນ) {
        StringBuilder ຂໍ້ຄວາມ = new StringBuilder(); for (byte ຄ່າ : ຂໍ້ມູນ) ຂໍ້ຄວາມ.append(String.format(Locale.ROOT,"%02x",ຄ່າ & 255)); return ຂໍ້ຄວາມ.toString();
    }
    static Path 내부경로(Path ໂຄງ_ການ_ເລກຮາກ, String ຊື່) {
        Path ມາດຕະການ = ໂຄງ_ການ_ເລກຮາກ.resolve(ຊື່).normalize();
        if (ຊື່.isEmpty() || Paths.get(ຊື່).isAbsolute() || !ມາດຕະການ.startsWith(ໂຄງ_ການ_ເລກຮາກ) || ຊື່.indexOf('\\') >= 0)
            throw new IllegalArgumentException("범위를 벗어난 ທາງໂຄຈອນ: " + ຊື່);
        for (Path 부분 : Paths.get(ຊື່)) if (부분.toString().equals("..")) throw new IllegalArgumentException("상위 ທາງໂຄຈອນ 금지: " + ຊື່);
        for (Path 현재 = ມາດຕະການ; 현재 != null && 현재.startsWith(ໂຄງ_ການ_ເລກຮາກ); 현재 = 현재.getParent())
            if (Files.isSymbolicLink(현재)) throw new IllegalArgumentException("의존성 경로의 링크 금지: " + ຊື່);
        return ມາດຕະການ;
    }
    static String 명령출력(List<String> ຄໍາສັ່ງ_1f12b8e2) throws Exception {
        Process ຂະ_ບວນ_ການ_ຄ່າ = new ProcessBuilder(ຄໍາສັ່ງ_1f12b8e2).redirectError(ProcessBuilder.Redirect.INHERIT).start();
        String ມາດຕະການ = new String(ຂະ_ບວນ_ການ_ຄ່າ.getInputStream().readAllBytes(),StandardCharsets.UTF_8);
        if (ຂະ_ບວນ_ການ_ຄ່າ.waitFor() != 0) throw new IOException("ຄໍາສັ່ງ_1f12b8e2 ຫຼົ້ມເຫຼວ_ຄ່າ: " + ຄໍາສັ່ງ_1f12b8e2.get(0)); return ມາດຕະການ;
    }
    static void ແຕກໄຟລ໌(Path ການສໍາເນົາ_ຄ່າ, Path ປາຍທາງ_ຄ່າ) throws Exception {
        for (String ຊື່ : 명령출력(Arrays.asList("tar","-tzf",ການສໍາເນົາ_ຄ່າ.toString())).split("\n")) 내부경로(ປາຍທາງ_ຄ່າ, ຊື່);
        for (String ສາຍ : 명령출력(Arrays.asList("tar","-tvzf",ການສໍາເນົາ_ຄ່າ.toString())).split("\n"))
            if (!ສາຍ.isEmpty() && ສາຍ.charAt(0) != '-' && ສາຍ.charAt(0) != 'd') throw new IOException("외부 링크 또는 특수 파일을 포함한 의존성");
        Files.createDirectories(ປາຍທາງ_ຄ່າ);
        int ສະຖານະ_ຄ່າ = new ProcessBuilder("tar","--no-same-owner","--no-same-permissions","-xzf",ການສໍາເນົາ_ຄ່າ.toString(),"-C",ປາຍທາງ_ຄ່າ.toString()).inheritIO().start().waitFor();
        if (ສະຖານະ_ຄ່າ != 0) throw new IOException("의존성 ການສໍາເນົາ_ຄ່າ ເວີຊັນ_ບ່ອນເກັບຂໍ້ມູນ ຫຼົ້ມເຫຼວ_ຄ່າ");
    }
    static void 호출(Path 작업경로, Path ເຄື່ອງມື, List<String> 인수, Map<String,String> 환경) throws Exception {
        List<String> ຄໍາສັ່ງ_1f12b8e2 = new ArrayList<>(Arrays.asList("python3", ເຄື່ອງມື.toString())); ຄໍາສັ່ງ_1f12b8e2.addAll(인수);
        ProcessBuilder ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ = new ProcessBuilder(ຄໍາສັ່ງ_1f12b8e2).directory(작업경로.toFile()).inheritIO(); ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ.environment().putAll(환경);
        int ສະຖານະ_ຄ່າ = ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ.start().waitFor(); if (ສະຖານະ_ຄ່າ != 0) throw new IOException("ເຄື່ອງມື ຫຼົ້ມເຫຼວ_ຄ່າ: " + ເຄື່ອງມື + " (" + ສະຖານະ_ຄ່າ + ")");
    }
    @SuppressWarnings("unchecked")
    public static void main(String[] 인수) throws Exception {
        if (인수.length < 1) throw new IllegalArgumentException("build, run, desktop, image, check, test-system 중 동작을 지정하세요");
        String ຄໍາສັ່ງ = 인수[0];
        if (!Arrays.asList("build","run","desktop","image","check","test-system").contains(ຄໍາສັ່ງ)) throw new IllegalArgumentException("알 수 없는 ຄໍາສັ່ງ");
        Path ໂຄງ_ການ_ເລກຮາກ = Paths.get(System.getProperty("worldos.edition.root")).toAbsolutePath().normalize();
        Map<String,Object> ການຕັ້ງຄ່າ = (Map<String,Object>)new ຂໍ້ມູນ_ຕົວແຍກວິເຄາະ(Files.readString(ໂຄງ_ການ_ເລກຮາກ.resolve("native.json"),StandardCharsets.UTF_8)).읽기();
        Path ແຫຼ່ງທີ່ມາ_ຕົ້ນໄມ້ = 내부경로(ໂຄງ_ການ_ເລກຮາກ,(String)ການຕັ້ງຄ່າ.get("source")), ແກນກາງ_ຄ່າ = 내부경로(ແຫຼ່ງທີ່ມາ_ຕົ້ນໄມ້,(String)ການຕັ້ງຄ່າ.get("native"));
        List<String> 소유파일들 = (List<String>)(List<?>)ການຕັ້ງຄ່າ.get("owned_files");
        for (String ຊື່ : 소유파일들) if (!Files.isRegularFile(내부경로(ແຫຼ່ງທີ່ມາ_ຕົ້ນໄມ້,ຊື່))) throw new IOException("ແຫຼ່ງທີ່ມາ_ຕົ້ນໄມ້ 없음: " + ຊື່);
        if (ຄໍາສັ່ງ.equals("check")) { System.out.println(ການຕັ້ງຄ່າ.get("country") + " " + ການຕັ້ງຄ່າ.get("language") + " 독립 ແຫຼ່ງທີ່ມາ_ຕົ້ນໄມ້ 확인 완료"); return; }
        String 자원상대 = (String)ການຕັ້ງຄ່າ.getOrDefault("resource_root", ".");
        if (!자원상대.equals(".") && !자원상대.equals("..")) throw new IllegalArgumentException("의존성 ໂຄງ_ການ_ເລກຮາກ ທາງໂຄຈອນ ຂໍ້ຜິດພາດ");
        Path ແຫຼ່ງ_ຄ່າ = ໂຄງ_ການ_ເລກຮາກ.resolve(자원상대).normalize(); Path ການສໍາເນົາ_ຄ່າ = ແຫຼ່ງ_ຄ່າ.resolve("native-vendor.tar.gz");
        String 기대해시 = (String)ການຕັ້ງຄ່າ.get("vendor_sha256");
        if (!ແຮຊ_ຟາຍ(ການສໍາເນົາ_ຄ່າ).equals(기대해시)) throw new IOException("의존성 SHA-256 불일치");
        Path 표식 = ແຫຼ່ງທີ່ມາ_ຕົ້ນໄມ້.resolve(".vendor-sha256");
        if (!Files.isRegularFile(표식) || !Files.readString(표식).trim().equals(기대해시)) { ແຕກໄຟລ໌(ການສໍາເນົາ_ຄ່າ, ແຫຼ່ງທີ່ມາ_ຕົ້ນໄມ້); Files.writeString(표식,기대해시 + "\n"); }
        Map<String,String> 환경 = new HashMap<>(System.getenv());
        Path ipConfig = null;
        if (환경.containsKey("IP_CONFIG")) ipConfig = Paths.get(환경.get("IP_CONFIG")).toAbsolutePath().normalize();
        else for (Path parent = ໂຄງ_ການ_ເລກຮາກ; parent != null; parent = parent.getParent()) {
            if (Files.isRegularFile(parent.resolve("ip.conf"))) { ipConfig = parent.resolve("ip.conf"); break; }
        }
        if (ipConfig == null) ipConfig = ແຫຼ່ງທີ່ມາ_ຕົ້ນໄມ້.resolve("ip.conf");
        if (!Files.isRegularFile(ipConfig)) throw new IOException("Missing ip.conf: " + ipConfig);
        환경.put("IP_CONFIG", ipConfig.toString());
        if (Arrays.asList("run","desktop","test-system").contains(ຄໍາສັ່ງ) && !환경.containsKey("QEMU_AARCH64")) {
            Path ແອັບ_ຕົວເປີດໃຊ້ = ແຫຼ່ງ_ຄ່າ.resolve("host/qemu"), 실행기표식 = ແຫຼ່ງ_ຄ່າ.resolve("host/.qemu-sha256");
            String ຕົວເປີດໃຊ້_ແຮຊ = (String)ການຕັ້ງຄ່າ.get("qemu_sha256");
            if (!Files.isRegularFile(ແອັບ_ຕົວເປີດໃຊ້) || !Files.isRegularFile(실행기표식) || !Files.readString(실행기표식).trim().equals(ຕົວເປີດໃຊ້_ແຮຊ)) {
                Path ຕົວເປີດໃຊ້_ການສໍາເນົາ = ແຫຼ່ງ_ຄ່າ.resolve("qemu-host.tar.gz"); if (!ແຮຊ_ຟາຍ(ຕົວເປີດໃຊ້_ການສໍາເນົາ).equals(ຕົວເປີດໃຊ້_ແຮຊ)) throw new IOException("QEMU SHA-256 불일치");
                ແຕກໄຟລ໌(ຕົວເປີດໃຊ້_ການສໍາເນົາ,ແຫຼ່ງ_ຄ່າ.resolve("host")); Files.writeString(실행기표식,ຕົວເປີດໃຊ້_ແຮຊ + "\n");
            }
            환경.put("QEMU_AARCH64",ແອັບ_ຕົວເປີດໃຊ້.toString());
        }
        MessageDigest 계산 = MessageDigest.getInstance("SHA-256"); Collections.sort(소유파일들);
        for (String ຊື່ : 소유파일들) { 계산.update(ຊື່.getBytes(StandardCharsets.UTF_8)); 계산.update(Files.readAllBytes(내부경로(ແຫຼ່ງທີ່ມາ_ຕົ້ນໄມ້,ຊື່))); }
        계산.update("ip.conf\0".getBytes(StandardCharsets.UTF_8)); 계산.update(Files.readAllBytes(ipConfig));
        String ແຫຼ່ງທີ່ມາ_ແຮຊ = ແຮຊ_ຂໍ້ຄວາມ(계산.digest()); Path 빌드표식 = ແກນກາງ_ຄ່າ.resolve("build/worldos-source.sha256");
        if (ຄໍາສັ່ງ.equals("build") || !Files.isRegularFile(빌드표식) || !Files.readString(빌드표식).trim().equals(ແຫຼ່ງທີ່ມາ_ແຮຊ)) {
            호출(ແກນກາງ_ຄ່າ,내부경로(ແກນກາງ_ຄ່າ,(String)ການຕັ້ງຄ່າ.get("builder")),Collections.emptyList(),환경);
            Files.writeString(빌드표식,ແຫຼ່ງທີ່ມາ_ແຮຊ + "\n");
        }
        List<String> 추가인수 = new ArrayList<>(Arrays.asList(인수).subList(1,인수.length));
        if (ຄໍາສັ່ງ.equals("run") || ຄໍາສັ່ງ.equals("desktop")) {
            if (ຄໍາສັ່ງ.equals("desktop")) 추가인수.add(0,"--desktop");
            호출(ແກນກາງ_ຄ່າ,내부경로(ແກນກາງ_ຄ່າ,(String)ການຕັ້ງຄ່າ.get("runner")),추가인수,환경);
        } else if (ຄໍາສັ່ງ.equals("image")) 호출(ແກນກາງ_ຄ່າ,내부경로(ແກນກາງ_ຄ່າ,(String)ການຕັ້ງຄ່າ.get("image_builder")),추가인수,환경);
        else if (ຄໍາສັ່ງ.equals("test-system")) {
            추가인수.add(0,ໂຄງ_ການ_ເລກຮາກ.toString()); 추가인수.add(0,"--edition");
            호출(ແກນກາງ_ຄ່າ,내부경로(ແກນກາງ_ຄ່າ,(String)ການຕັ້ງຄ່າ.get("system_tester")),추가인수,환경);
        }
    }
}
