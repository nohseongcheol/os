// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.security.MessageDigest;
import java.util.*;

/** 독립 국가판의 의존성 검사·복원·สร้าง·실행을 맡는 โฮสต์ Java เครื่องมือ. */
public final class คันทรี_ลิ้นชักแอป {
    static final class ข้อมูล_ตัวแยกวิเคราะห์ {
        final String รหัสต้นฉบับ; int ตําแหน่ง;
        ข้อมูล_ตัวแยกวิเคราะห์(String ข้อความ) { รหัสต้นฉบับ = ข้อความ; }
        void 빈칸() { while (ตําแหน่ง < รหัสต้นฉบับ.length() && Character.isWhitespace(รหัสต้นฉบับ.charAt(ตําแหน่ง))) ตําแหน่ง++; }
        Object อ่าน() {
            빈칸(); char อักขระ_ค่า = รหัสต้นฉบับ.charAt(ตําแหน่ง++);
            if (อักขระ_ค่า == '{') {
                Map<String,Object> ผลลัพธ์ = new LinkedHashMap<>(); 빈칸();
                if (รหัสต้นฉบับ.charAt(ตําแหน่ง) == '}') { ตําแหน่ง++; return ผลลัพธ์; }
                while (true) {
                    String ชื่อ = (String)อ่าน(); 빈칸(); if (รหัสต้นฉบับ.charAt(ตําแหน่ง++) != ':') throw new IllegalArgumentException("ข้อมูล ตัวคั่น_ค่า ข้อผิดพลาด");
                    ผลลัพธ์.put(ชื่อ, อ่าน()); 빈칸(); char ตัวคั่น_ค่า = รหัสต้นฉบับ.charAt(ตําแหน่ง++);
                    if (ตัวคั่น_ค่า == '}') return ผลลัพธ์; if (ตัวคั่น_ค่า != ',') throw new IllegalArgumentException("ข้อมูล ตัวคั่น_ค่า ข้อผิดพลาด");
                }
            }
            if (อักขระ_ค่า == '[') {
                List<Object> ผลลัพธ์ = new ArrayList<>(); 빈칸();
                if (รหัสต้นฉบับ.charAt(ตําแหน่ง) == ']') { ตําแหน่ง++; return ผลลัพธ์; }
                while (true) {
                    ผลลัพธ์.add(อ่าน()); 빈칸(); char ตัวคั่น_ค่า = รหัสต้นฉบับ.charAt(ตําแหน่ง++);
                    if (ตัวคั่น_ค่า == ']') return ผลลัพธ์; if (ตัวคั่น_ค่า != ',') throw new IllegalArgumentException("ข้อมูล ตัวคั่น_ค่า ข้อผิดพลาด");
                }
            }
            if (อักขระ_ค่า == '"') {
                StringBuilder ผลลัพธ์ = new StringBuilder();
                while (true) {
                    char ถัดไป_รายการ = รหัสต้นฉบับ.charAt(ตําแหน่ง++); if (ถัดไป_รายการ == '"') return ผลลัพธ์.toString();
                    if (ถัดไป_รายการ == '\\') {
                        ถัดไป_รายการ = รหัสต้นฉบับ.charAt(ตําแหน่ง++);
                        if (ถัดไป_รายการ == 'u') { ผลลัพธ์.append((char)Integer.parseInt(รหัสต้นฉบับ.substring(ตําแหน่ง, ตําแหน่ง + 4),16)); ตําแหน่ง += 4; continue; }
                        if (ถัดไป_รายการ == 'n') ถัดไป_รายการ = '\n'; else if (ถัดไป_รายการ == 'r') ถัดไป_รายการ = '\r'; else if (ถัดไป_รายการ == 't') ถัดไป_รายการ = '\t';
                        else if (ถัดไป_รายการ == 'b') ถัดไป_รายการ = '\b'; else if (ถัดไป_รายการ == 'f') ถัดไป_รายการ = '\f';
                        else if (ถัดไป_รายการ != '"' && ถัดไป_รายการ != '\\' && ถัดไป_รายการ != '/') throw new IllegalArgumentException("문자 이스케이프 ข้อผิดพลาด");
                    }
                    ผลลัพธ์.append(ถัดไป_รายการ);
                }
            }
            int เรียกใช้งาน = ตําแหน่ง - 1;
            while (ตําแหน่ง < รหัสต้นฉบับ.length() && ",]} \t\r\n".indexOf(รหัสต้นฉบับ.charAt(ตําแหน่ง)) < 0) ตําแหน่ง++;
            String ค่า = รหัสต้นฉบับ.substring(เรียกใช้งาน, ตําแหน่ง);
            if (ค่า.equals("true")) return Boolean.TRUE; if (ค่า.equals("false")) return Boolean.FALSE; if (ค่า.equals("null")) return null;
            return Double.valueOf(ค่า);
        }
    }
    static String แฮช_แฟ้ม(Path เส้นทาง) throws Exception {
        MessageDigest 계산 = MessageDigest.getInstance("SHA-256"); byte[] ข้อมูล = new byte[1024 * 1024];
        try (InputStream 입력 = Files.newInputStream(เส้นทาง)) { for (int 길이; (길이 = 입력.read(ข้อมูล)) >= 0;) 계산.update(ข้อมูล,0,길이); }
        return แฮช_ข้อความ(계산.digest());
    }
    static String แฮช_ข้อความ(byte[] ข้อมูล) {
        StringBuilder ข้อความ = new StringBuilder(); for (byte ค่า : ข้อมูล) ข้อความ.append(String.format(Locale.ROOT,"%02x",ค่า & 255)); return ข้อความ.toString();
    }
    static Path ภายใน_พาธ(Path แสดง_ราก, String ชื่อ) {
        Path ผลลัพธ์ = แสดง_ราก.resolve(ชื่อ).normalize();
        if (ชื่อ.isEmpty() || Paths.get(ชื่อ).isAbsolute() || !ผลลัพธ์.startsWith(แสดง_ราก) || ชื่อ.indexOf('\\') >= 0)
            throw new IllegalArgumentException("범위를 벗어난 เส้นทาง: " + ชื่อ);
        for (Path 부분 : Paths.get(ชื่อ)) if (부분.toString().equals("..")) throw new IllegalArgumentException("상위 เส้นทาง 금지: " + ชื่อ);
        for (Path ปัจจุบัน_รายการ = ผลลัพธ์; ปัจจุบัน_รายการ != null && ปัจจุบัน_รายการ.startsWith(แสดง_ราก); ปัจจุบัน_รายการ = ปัจจุบัน_รายการ.getParent())
            if (Files.isSymbolicLink(ปัจจุบัน_รายการ)) throw new IllegalArgumentException("의존성 경로의 링크 금지: " + ชื่อ);
        return ผลลัพธ์;
    }
    static String คําสั่ง_ผลผลิต(List<String> คําสั่ง) throws Exception {
        Process กระบวนการ_ค่า = new ProcessBuilder(คําสั่ง).redirectError(ProcessBuilder.Redirect.INHERIT).start();
        String ผลลัพธ์ = new String(กระบวนการ_ค่า.getInputStream().readAllBytes(),StandardCharsets.UTF_8);
        if (กระบวนการ_ค่า.waitFor() != 0) throw new IOException("คําสั่ง ความล้มเหลว_ค่า: " + คําสั่ง.get(0)); return ผลลัพธ์;
    }
    static void แยก(Path เก็บถาวร_ค่า, Path ปลายทาง_ค่า_a0fbc067) throws Exception {
        for (String ชื่อ : คําสั่ง_ผลผลิต(Arrays.asList("tar","-tzf",เก็บถาวร_ค่า.toString())).split("\n")) ภายใน_พาธ(ปลายทาง_ค่า_a0fbc067, ชื่อ);
        for (String บรรทัด : คําสั่ง_ผลผลิต(Arrays.asList("tar","-tvzf",เก็บถาวร_ค่า.toString())).split("\n"))
            if (!บรรทัด.isEmpty() && บรรทัด.charAt(0) != '-' && บรรทัด.charAt(0) != 'd') throw new IOException("ภายนอก_ค่า 링크 또는 특수 파일을 포함한 의존성");
        Files.createDirectories(ปลายทาง_ค่า_a0fbc067);
        int สถานะ_ค่า = new ProcessBuilder("tar","--no-same-owner","--no-same-permissions","-xzf",เก็บถาวร_ค่า.toString(),"-C",ปลายทาง_ค่า_a0fbc067.toString()).inheritIO().start().waitFor();
        if (สถานะ_ค่า != 0) throw new IOException("의존성 เก็บถาวร_ค่า ปล่อย_ที่เก็บ ความล้มเหลว_ค่า");
    }
    static void 호출(Path 작업경로, Path เครื่องมือ, List<String> อาร์กิวเมนต์, Map<String,String> สภาพแวดล้อม) throws Exception {
        List<String> คําสั่ง = new ArrayList<>(Arrays.asList("python3", เครื่องมือ.toString())); คําสั่ง.addAll(อาร์กิวเมนต์);
        ProcessBuilder ดําเนินการ_คําสั่ง = new ProcessBuilder(คําสั่ง).directory(작업경로.toFile()).inheritIO(); ดําเนินการ_คําสั่ง.environment().putAll(สภาพแวดล้อม);
        int สถานะ_ค่า = ดําเนินการ_คําสั่ง.start().waitFor(); if (สถานะ_ค่า != 0) throw new IOException("เครื่องมือ ความล้มเหลว_ค่า: " + เครื่องมือ + " (" + สถานะ_ค่า + ")");
    }
    @SuppressWarnings("unchecked")
    public static void main(String[] อาร์กิวเมนต์) throws Exception {
        if (อาร์กิวเมนต์.length < 1) throw new IllegalArgumentException("build, run, desktop, image, check, test-system 중 동작을 지정하세요");
        String การกระทํา = อาร์กิวเมนต์[0];
        if (!Arrays.asList("build","run","desktop","image","check","test-system").contains(การกระทํา)) throw new IllegalArgumentException("알 หมายเลข 없는 การกระทํา");
        Path แสดง_ราก = Paths.get(System.getProperty("worldos.edition.root")).toAbsolutePath().normalize();
        Map<String,Object> ตั้งค่า = (Map<String,Object>)new ข้อมูล_ตัวแยกวิเคราะห์(Files.readString(แสดง_ราก.resolve("native.json"),StandardCharsets.UTF_8)).อ่าน();
        Path แหล่ง_ทรี = ภายใน_พาธ(แสดง_ราก,(String)ตั้งค่า.get("source")), เคอร์เนล_ค่า = ภายใน_พาธ(แหล่ง_ทรี,(String)ตั้งค่า.get("native"));
        List<String> 소유파일들 = (List<String>)(List<?>)ตั้งค่า.get("owned_files");
        for (String ชื่อ : 소유파일들) if (!Files.isRegularFile(ภายใน_พาธ(แหล่ง_ทรี,ชื่อ))) throw new IOException("แหล่ง_ทรี 없음: " + ชื่อ);
        if (การกระทํา.equals("check")) { System.out.println(ตั้งค่า.get("country") + " " + ตั้งค่า.get("language") + " 독립 แหล่ง_ทรี ยืนยัน 완료"); return; }
        String ทรัพยากร_เส้นทางสัมพัทธ์ = (String)ตั้งค่า.getOrDefault("resource_root", ".");
        if (!ทรัพยากร_เส้นทางสัมพัทธ์.equals(".") && !ทรัพยากร_เส้นทางสัมพัทธ์.equals("..")) throw new IllegalArgumentException("의존성 แสดง_ราก เส้นทาง ข้อผิดพลาด");
        Path ทรัพยากร_ค่า = แสดง_ราก.resolve(ทรัพยากร_เส้นทางสัมพัทธ์).normalize(); Path เก็บถาวร_ค่า = ทรัพยากร_ค่า.resolve("native-vendor.tar.gz");
        String 기대해시 = (String)ตั้งค่า.get("vendor_sha256");
        if (!แฮช_แฟ้ม(เก็บถาวร_ค่า).equals(기대해시)) throw new IOException("의존성 SHA-256 불일치");
        Path มาร์กเกอร์_ค่า = แหล่ง_ทรี.resolve(".vendor-sha256");
        if (!Files.isRegularFile(มาร์กเกอร์_ค่า) || !Files.readString(มาร์กเกอร์_ค่า).trim().equals(기대해시)) { แยก(เก็บถาวร_ค่า, แหล่ง_ทรี); Files.writeString(มาร์กเกอร์_ค่า,기대해시 + "\n"); }
        Map<String,String> สภาพแวดล้อม = new HashMap<>(System.getenv());
        Path ipConfig = null;
        if (สภาพแวดล้อม.containsKey("IP_CONFIG")) ipConfig = Paths.get(สภาพแวดล้อม.get("IP_CONFIG")).toAbsolutePath().normalize();
        else for (Path parent = แสดง_ราก; parent != null; parent = parent.getParent()) {
            if (Files.isRegularFile(parent.resolve("ip.conf"))) { ipConfig = parent.resolve("ip.conf"); break; }
        }
        if (ipConfig == null) ipConfig = แหล่ง_ทรี.resolve("ip.conf");
        if (!Files.isRegularFile(ipConfig)) throw new IOException("Missing ip.conf: " + ipConfig);
        สภาพแวดล้อม.put("IP_CONFIG", ipConfig.toString());
        if (Arrays.asList("run","desktop","test-system").contains(การกระทํา) && !สภาพแวดล้อม.containsKey("QEMU_AARCH64")) {
            Path แอป_ลิ้นชักแอป = ทรัพยากร_ค่า.resolve("host/qemu"), ลิ้นชักแอป_มาร์กเกอร์ = ทรัพยากร_ค่า.resolve("host/.qemu-sha256");
            String ลิ้นชักแอป_แฮช = (String)ตั้งค่า.get("qemu_sha256");
            if (!Files.isRegularFile(แอป_ลิ้นชักแอป) || !Files.isRegularFile(ลิ้นชักแอป_มาร์กเกอร์) || !Files.readString(ลิ้นชักแอป_มาร์กเกอร์).trim().equals(ลิ้นชักแอป_แฮช)) {
                Path ลิ้นชักแอป_เก็บถาวร = ทรัพยากร_ค่า.resolve("qemu-host.tar.gz"); if (!แฮช_แฟ้ม(ลิ้นชักแอป_เก็บถาวร).equals(ลิ้นชักแอป_แฮช)) throw new IOException("QEMU SHA-256 불일치");
                แยก(ลิ้นชักแอป_เก็บถาวร,ทรัพยากร_ค่า.resolve("host")); Files.writeString(ลิ้นชักแอป_มาร์กเกอร์,ลิ้นชักแอป_แฮช + "\n");
            }
            สภาพแวดล้อม.put("QEMU_AARCH64",แอป_ลิ้นชักแอป.toString());
        }
        MessageDigest 계산 = MessageDigest.getInstance("SHA-256"); Collections.sort(소유파일들);
        for (String ชื่อ : 소유파일들) { 계산.update(ชื่อ.getBytes(StandardCharsets.UTF_8)); 계산.update(Files.readAllBytes(ภายใน_พาธ(แหล่ง_ทรี,ชื่อ))); }
        계산.update("ip.conf\0".getBytes(StandardCharsets.UTF_8)); 계산.update(Files.readAllBytes(ipConfig));
        String แหล่ง_แฮช = แฮช_ข้อความ(계산.digest()); Path รุ่น_มาร์กเกอร์ = เคอร์เนล_ค่า.resolve("build/worldos-source.sha256");
        if (การกระทํา.equals("build") || !Files.isRegularFile(รุ่น_มาร์กเกอร์) || !Files.readString(รุ่น_มาร์กเกอร์).trim().equals(แหล่ง_แฮช)) {
            호출(เคอร์เนล_ค่า,ภายใน_พาธ(เคอร์เนล_ค่า,(String)ตั้งค่า.get("builder")),Collections.emptyList(),สภาพแวดล้อม);
            Files.writeString(รุ่น_มาร์กเกอร์,แหล่ง_แฮช + "\n");
        }
        List<String> 추가인수 = new ArrayList<>(Arrays.asList(อาร์กิวเมนต์).subList(1,อาร์กิวเมนต์.length));
        if (การกระทํา.equals("run") || การกระทํา.equals("desktop")) {
            if (การกระทํา.equals("desktop")) 추가인수.add(0,"--desktop");
            호출(เคอร์เนล_ค่า,ภายใน_พาธ(เคอร์เนล_ค่า,(String)ตั้งค่า.get("runner")),추가인수,สภาพแวดล้อม);
        } else if (การกระทํา.equals("image")) 호출(เคอร์เนล_ค่า,ภายใน_พาธ(เคอร์เนล_ค่า,(String)ตั้งค่า.get("image_builder")),추가인수,สภาพแวดล้อม);
        else if (การกระทํา.equals("test-system")) {
            추가인수.add(0,แสดง_ราก.toString()); 추가인수.add(0,"--edition");
            호출(เคอร์เนล_ค่า,ภายใน_พาธ(เคอร์เนล_ค่า,(String)ตั้งค่า.get("system_tester")),추가인수,สภาพแวดล้อม);
        }
    }
}
