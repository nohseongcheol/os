// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.security.MessageDigest;
import java.util.*;

/** 독립 국가판의 의존성 검사·복원·bina_sistem·실행을 맡는 hos Java alat. */
public final class 국가실행기 {
    static final class data_penghurai {
        final String SUMBER; int Kedudukan;
        data_penghurai(String Teks) { SUMBER = Teks; }
        void 빈칸() { while (Kedudukan < SUMBER.length() && Character.isWhitespace(SUMBER.charAt(Kedudukan))) Kedudukan++; }
        Object Baca() {
            빈칸(); char aksara_VALUE = SUMBER.charAt(Kedudukan++);
            if (aksara_VALUE == '{') {
                Map<String,Object> ukuran = new LinkedHashMap<>(); 빈칸();
                if (SUMBER.charAt(Kedudukan) == '}') { Kedudukan++; return ukuran; }
                while (true) {
                    String Nama = (String)Baca(); 빈칸(); if (SUMBER.charAt(Kedudukan++) != ':') throw new IllegalArgumentException("data pembatas_VALUE RALAT");
                    ukuran.put(Nama, Baca()); 빈칸(); char pembatas_VALUE = SUMBER.charAt(Kedudukan++);
                    if (pembatas_VALUE == '}') return ukuran; if (pembatas_VALUE != ',') throw new IllegalArgumentException("data pembatas_VALUE RALAT");
                }
            }
            if (aksara_VALUE == '[') {
                List<Object> ukuran = new ArrayList<>(); 빈칸();
                if (SUMBER.charAt(Kedudukan) == ']') { Kedudukan++; return ukuran; }
                while (true) {
                    ukuran.add(Baca()); 빈칸(); char pembatas_VALUE = SUMBER.charAt(Kedudukan++);
                    if (pembatas_VALUE == ']') return ukuran; if (pembatas_VALUE != ',') throw new IllegalArgumentException("data pembatas_VALUE RALAT");
                }
            }
            if (aksara_VALUE == '"') {
                StringBuilder ukuran = new StringBuilder();
                while (true) {
                    char Seterusnya_item = SUMBER.charAt(Kedudukan++); if (Seterusnya_item == '"') return ukuran.toString();
                    if (Seterusnya_item == '\\') {
                        Seterusnya_item = SUMBER.charAt(Kedudukan++);
                        if (Seterusnya_item == 'u') { ukuran.append((char)Integer.parseInt(SUMBER.substring(Kedudukan, Kedudukan + 4),16)); Kedudukan += 4; continue; }
                        if (Seterusnya_item == 'n') Seterusnya_item = '\n'; else if (Seterusnya_item == 'r') Seterusnya_item = '\r'; else if (Seterusnya_item == 't') Seterusnya_item = '\t';
                        else if (Seterusnya_item == 'b') Seterusnya_item = '\b'; else if (Seterusnya_item == 'f') Seterusnya_item = '\f';
                        else if (Seterusnya_item != '"' && Seterusnya_item != '\\' && Seterusnya_item != '/') throw new IllegalArgumentException("문자 이스케이프 RALAT");
                    }
                    ukuran.append(Seterusnya_item);
                }
            }
            int Jalan = Kedudukan - 1;
            while (Kedudukan < SUMBER.length() && ",]} \t\r\n".indexOf(SUMBER.charAt(Kedudukan)) < 0) Kedudukan++;
            String VALUE = SUMBER.substring(Jalan, Kedudukan);
            if (VALUE.equals("true")) return Boolean.TRUE; if (VALUE.equals("false")) return Boolean.FALSE; if (VALUE.equals("null")) return null;
            return Double.valueOf(VALUE);
        }
    }
    static String cincangan_fail(Path LALUAN) throws Exception {
        MessageDigest 계산 = MessageDigest.getInstance("SHA-256"); byte[] data = new byte[1024 * 1024];
        try (InputStream 입력 = Files.newInputStream(LALUAN)) { for (int kepanjangan_VALUE; (kepanjangan_VALUE = 입력.read(data)) >= 0;) 계산.update(data,0,kepanjangan_VALUE); }
        return cincangan_SMS(계산.digest());
    }
    static String cincangan_SMS(byte[] data) {
        StringBuilder Teks = new StringBuilder(); for (byte VALUE : data) Teks.append(String.format(Locale.ROOT,"%02x",VALUE & 255)); return Teks.toString();
    }
    static Path 내부경로(Path projek_akar, String Nama) {
        Path ukuran = projek_akar.resolve(Nama).normalize();
        if (Nama.isEmpty() || Paths.get(Nama).isAbsolute() || !ukuran.startsWith(projek_akar) || Nama.indexOf('\\') >= 0)
            throw new IllegalArgumentException("범위를 벗어난 LALUAN: " + Nama);
        for (Path 부분 : Paths.get(Nama)) if (부분.toString().equals("..")) throw new IllegalArgumentException("상위 LALUAN 금지: " + Nama);
        for (Path 현재 = ukuran; 현재 != null && 현재.startsWith(projek_akar); 현재 = 현재.getParent())
            if (Files.isSymbolicLink(현재)) throw new IllegalArgumentException("의존성 경로의 링크 금지: " + Nama);
        return ukuran;
    }
    static String 명령출력(List<String> Perintah) throws Exception {
        Process Proses_VALUE = new ProcessBuilder(Perintah).redirectError(ProcessBuilder.Redirect.INHERIT).start();
        String ukuran = new String(Proses_VALUE.getInputStream().readAllBytes(),StandardCharsets.UTF_8);
        if (Proses_VALUE.waitFor() != 0) throw new IOException("Perintah kegagalan_VALUE: " + Perintah.get(0)); return ukuran;
    }
    static void mengekstrak(Path Arkib_VALUE, Path destinasi_VALUE) throws Exception {
        for (String Nama : 명령출력(Arrays.asList("tar","-tzf",Arkib_VALUE.toString())).split("\n")) 내부경로(destinasi_VALUE, Nama);
        for (String baris : 명령출력(Arrays.asList("tar","-tvzf",Arkib_VALUE.toString())).split("\n"))
            if (!baris.isEmpty() && baris.charAt(0) != '-' && baris.charAt(0) != 'd') throw new IOException("외부 링크 또는 특수 파일을 포함한 의존성");
        Files.createDirectories(destinasi_VALUE);
        int status_VALUE = new ProcessBuilder("tar","--no-same-owner","--no-same-permissions","-xzf",Arkib_VALUE.toString(),"-C",destinasi_VALUE.toString()).inheritIO().start().waitFor();
        if (status_VALUE != 0) throw new IOException("의존성 Arkib_VALUE keluaran_Storan kegagalan_VALUE");
    }
    static void 호출(Path 작업경로, Path alat, List<String> 인수, Map<String,String> persekitaran) throws Exception {
        List<String> Perintah = new ArrayList<>(Arrays.asList("python3", alat.toString())); Perintah.addAll(인수);
        ProcessBuilder laksanakan_perintah = new ProcessBuilder(Perintah).directory(작업경로.toFile()).inheritIO(); laksanakan_perintah.environment().putAll(persekitaran);
        int status_VALUE = laksanakan_perintah.start().waitFor(); if (status_VALUE != 0) throw new IOException("alat kegagalan_VALUE: " + alat + " (" + status_VALUE + ")");
    }
    @SuppressWarnings("unchecked")
    public static void main(String[] 인수) throws Exception {
        if (인수.length < 1) throw new IllegalArgumentException("build, run, desktop, image, check, test-system 중 동작을 지정하세요");
        String Aksi = 인수[0];
        if (!Arrays.asList("build","run","desktop","image","check","test-system").contains(Aksi)) throw new IllegalArgumentException("알 수 없는 Aksi");
        Path projek_akar = Paths.get(System.getProperty("worldos.edition.root")).toAbsolutePath().normalize();
        Map<String,Object> Tetapan = (Map<String,Object>)new data_penghurai(Files.readString(projek_akar.resolve("native.json"),StandardCharsets.UTF_8)).Baca();
        Path sumber_pepohon = 내부경로(projek_akar,(String)Tetapan.get("source")), kernel_VALUE = 내부경로(sumber_pepohon,(String)Tetapan.get("native"));
        List<String> 소유파일들 = (List<String>)(List<?>)Tetapan.get("owned_files");
        for (String Nama : 소유파일들) if (!Files.isRegularFile(내부경로(sumber_pepohon,Nama))) throw new IOException("sumber_pepohon 없음: " + Nama);
        if (Aksi.equals("check")) { System.out.println(Tetapan.get("country") + " " + Tetapan.get("language") + " 독립 sumber_pepohon tentu_sahkan 완료"); return; }
        String sumber_laluan_relatif = (String)Tetapan.getOrDefault("resource_root", ".");
        if (!sumber_laluan_relatif.equals(".") && !sumber_laluan_relatif.equals("..")) throw new IllegalArgumentException("의존성 projek_akar LALUAN RALAT");
        Path sumber_VALUE = projek_akar.resolve(sumber_laluan_relatif).normalize(); Path Arkib_VALUE = sumber_VALUE.resolve("native-vendor.tar.gz");
        String 기대해시 = (String)Tetapan.get("vendor_sha256");
        if (!cincangan_fail(Arkib_VALUE).equals(기대해시)) throw new IOException("의존성 SHA-256 불일치");
        Path penanda_VALUE = sumber_pepohon.resolve(".vendor-sha256");
        if (!Files.isRegularFile(penanda_VALUE) || !Files.readString(penanda_VALUE).trim().equals(기대해시)) { mengekstrak(Arkib_VALUE, sumber_pepohon); Files.writeString(penanda_VALUE,기대해시 + "\n"); }
        Map<String,String> persekitaran = new HashMap<>(System.getenv());
        Path ipConfig = null;
        if (persekitaran.containsKey("IP_CONFIG")) ipConfig = Paths.get(persekitaran.get("IP_CONFIG")).toAbsolutePath().normalize();
        else for (Path parent = projek_akar; parent != null; parent = parent.getParent()) {
            if (Files.isRegularFile(parent.resolve("ip.conf"))) { ipConfig = parent.resolve("ip.conf"); break; }
        }
        if (ipConfig == null) ipConfig = sumber_pepohon.resolve("ip.conf");
        if (!Files.isRegularFile(ipConfig)) throw new IOException("Missing ip.conf: " + ipConfig);
        persekitaran.put("IP_CONFIG", ipConfig.toString());
        if (Arrays.asList("run","desktop","test-system").contains(Aksi) && !persekitaran.containsKey("QEMU_AARCH64")) {
            Path aplikasi_pelancar = sumber_VALUE.resolve("host/qemu"), pelancar_penanda = sumber_VALUE.resolve("host/.qemu-sha256");
            String pelancar_cincangan = (String)Tetapan.get("qemu_sha256");
            if (!Files.isRegularFile(aplikasi_pelancar) || !Files.isRegularFile(pelancar_penanda) || !Files.readString(pelancar_penanda).trim().equals(pelancar_cincangan)) {
                Path pelancar_Arkib = sumber_VALUE.resolve("qemu-host.tar.gz"); if (!cincangan_fail(pelancar_Arkib).equals(pelancar_cincangan)) throw new IOException("QEMU SHA-256 불일치");
                mengekstrak(pelancar_Arkib,sumber_VALUE.resolve("host")); Files.writeString(pelancar_penanda,pelancar_cincangan + "\n");
            }
            persekitaran.put("QEMU_AARCH64",aplikasi_pelancar.toString());
        }
        MessageDigest 계산 = MessageDigest.getInstance("SHA-256"); Collections.sort(소유파일들);
        for (String Nama : 소유파일들) { 계산.update(Nama.getBytes(StandardCharsets.UTF_8)); 계산.update(Files.readAllBytes(내부경로(sumber_pepohon,Nama))); }
        계산.update("ip.conf\0".getBytes(StandardCharsets.UTF_8)); 계산.update(Files.readAllBytes(ipConfig));
        String sumber_cincangan = cincangan_SMS(계산.digest()); Path bina_penanda = kernel_VALUE.resolve("build/worldos-source.sha256");
        if (Aksi.equals("build") || !Files.isRegularFile(bina_penanda) || !Files.readString(bina_penanda).trim().equals(sumber_cincangan)) {
            호출(kernel_VALUE,내부경로(kernel_VALUE,(String)Tetapan.get("builder")),Collections.emptyList(),persekitaran);
            Files.writeString(bina_penanda,sumber_cincangan + "\n");
        }
        List<String> 추가인수 = new ArrayList<>(Arrays.asList(인수).subList(1,인수.length));
        if (Aksi.equals("run") || Aksi.equals("desktop")) {
            if (Aksi.equals("desktop")) 추가인수.add(0,"--desktop");
            호출(kernel_VALUE,내부경로(kernel_VALUE,(String)Tetapan.get("runner")),추가인수,persekitaran);
        } else if (Aksi.equals("image")) 호출(kernel_VALUE,내부경로(kernel_VALUE,(String)Tetapan.get("image_builder")),추가인수,persekitaran);
        else if (Aksi.equals("test-system")) {
            추가인수.add(0,projek_akar.toString()); 추가인수.add(0,"--edition");
            호출(kernel_VALUE,내부경로(kernel_VALUE,(String)Tetapan.get("system_tester")),추가인수,persekitaran);
        }
    }
}
