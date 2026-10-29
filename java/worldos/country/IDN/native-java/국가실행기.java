// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.security.MessageDigest;
import java.util.*;

/** 독립 국가판의 의존성 검사·복원·bangun·실행을 맡는 host Java alat. */
public final class 국가실행기 {
    static final class data_parser {
        final String kodeSumber; int posisi;
        data_parser(String teks) { kodeSumber = teks; }
        void 빈칸() { while (posisi < kodeSumber.length() && Character.isWhitespace(kodeSumber.charAt(posisi))) posisi++; }
        Object Baca() {
            빈칸(); char karakter_VALUE = kodeSumber.charAt(posisi++);
            if (karakter_VALUE == '{') {
                Map<String,Object> hasil = new LinkedHashMap<>(); 빈칸();
                if (kodeSumber.charAt(posisi) == '}') { posisi++; return hasil; }
                while (true) {
                    String Nama_2 = (String)Baca(); 빈칸(); if (kodeSumber.charAt(posisi++) != ':') throw new IllegalArgumentException("data pemisah_VALUE_d8ba4873 galat");
                    hasil.put(Nama_2, Baca()); 빈칸(); char pemisah_VALUE_d8ba4873 = kodeSumber.charAt(posisi++);
                    if (pemisah_VALUE_d8ba4873 == '}') return hasil; if (pemisah_VALUE_d8ba4873 != ',') throw new IllegalArgumentException("data pemisah_VALUE_d8ba4873 galat");
                }
            }
            if (karakter_VALUE == '[') {
                List<Object> hasil = new ArrayList<>(); 빈칸();
                if (kodeSumber.charAt(posisi) == ']') { posisi++; return hasil; }
                while (true) {
                    hasil.add(Baca()); 빈칸(); char pemisah_VALUE_d8ba4873 = kodeSumber.charAt(posisi++);
                    if (pemisah_VALUE_d8ba4873 == ']') return hasil; if (pemisah_VALUE_d8ba4873 != ',') throw new IllegalArgumentException("data pemisah_VALUE_d8ba4873 galat");
                }
            }
            if (karakter_VALUE == '"') {
                StringBuilder hasil = new StringBuilder();
                while (true) {
                    char Berikutnya_item = kodeSumber.charAt(posisi++); if (Berikutnya_item == '"') return hasil.toString();
                    if (Berikutnya_item == '\\') {
                        Berikutnya_item = kodeSumber.charAt(posisi++);
                        if (Berikutnya_item == 'u') { hasil.append((char)Integer.parseInt(kodeSumber.substring(posisi, posisi + 4),16)); posisi += 4; continue; }
                        if (Berikutnya_item == 'n') Berikutnya_item = '\n'; else if (Berikutnya_item == 'r') Berikutnya_item = '\r'; else if (Berikutnya_item == 't') Berikutnya_item = '\t';
                        else if (Berikutnya_item == 'b') Berikutnya_item = '\b'; else if (Berikutnya_item == 'f') Berikutnya_item = '\f';
                        else if (Berikutnya_item != '"' && Berikutnya_item != '\\' && Berikutnya_item != '/') throw new IllegalArgumentException("문자 이스케이프 galat");
                    }
                    hasil.append(Berikutnya_item);
                }
            }
            int jalankan = posisi - 1;
            while (posisi < kodeSumber.length() && ",]} \t\r\n".indexOf(kodeSumber.charAt(posisi)) < 0) posisi++;
            String VALUE = kodeSumber.substring(jalankan, posisi);
            if (VALUE.equals("true")) return Boolean.TRUE; if (VALUE.equals("false")) return Boolean.FALSE; if (VALUE.equals("null")) return null;
            return Double.valueOf(VALUE);
        }
    }
    static String hash_file(Path jalur) throws Exception {
        MessageDigest 계산 = MessageDigest.getInstance("SHA-256"); byte[] data = new byte[1024 * 1024];
        try (InputStream 입력 = Files.newInputStream(jalur)) { for (int panjang_VALUE; (panjang_VALUE = 입력.read(data)) >= 0;) 계산.update(data,0,panjang_VALUE); }
        return hash_SMS(계산.digest());
    }
    static String hash_SMS(byte[] data) {
        StringBuilder teks = new StringBuilder(); for (byte VALUE : data) teks.append(String.format(Locale.ROOT,"%02x",VALUE & 255)); return teks.toString();
    }
    static Path internal_jalur(Path Tugas_akar, String Nama_2) {
        Path hasil = Tugas_akar.resolve(Nama_2).normalize();
        if (Nama_2.isEmpty() || Paths.get(Nama_2).isAbsolute() || !hasil.startsWith(Tugas_akar) || Nama_2.indexOf('\\') >= 0)
            throw new IllegalArgumentException("범위를 벗어난 jalur: " + Nama_2);
        for (Path 부분 : Paths.get(Nama_2)) if (부분.toString().equals("..")) throw new IllegalArgumentException("상위 jalur 금지: " + Nama_2);
        for (Path saat_ini_item = hasil; saat_ini_item != null && saat_ini_item.startsWith(Tugas_akar); saat_ini_item = saat_ini_item.getParent())
            if (Files.isSymbolicLink(saat_ini_item)) throw new IllegalArgumentException("의존성 경로의 링크 금지: " + Nama_2);
        return hasil;
    }
    static String 명령출력(List<String> perintah) throws Exception {
        Process Proses_VALUE = new ProcessBuilder(perintah).redirectError(ProcessBuilder.Redirect.INHERIT).start();
        String hasil = new String(Proses_VALUE.getInputStream().readAllBytes(),StandardCharsets.UTF_8);
        if (Proses_VALUE.waitFor() != 0) throw new IOException("perintah kegagalan_VALUE: " + perintah.get(0)); return hasil;
    }
    static void ekstrak(Path Arsip_VALUE, Path tujuan_VALUE) throws Exception {
        for (String Nama_2 : 명령출력(Arrays.asList("tar","-tzf",Arsip_VALUE.toString())).split("\n")) internal_jalur(tujuan_VALUE, Nama_2);
        for (String baris_masukan : 명령출력(Arrays.asList("tar","-tvzf",Arsip_VALUE.toString())).split("\n"))
            if (!baris_masukan.isEmpty() && baris_masukan.charAt(0) != '-' && baris_masukan.charAt(0) != 'd') throw new IOException("eksternal_VALUE 링크 또는 특수 파일을 포함한 의존성");
        Files.createDirectories(tujuan_VALUE);
        int Status_VALUE = new ProcessBuilder("tar","--no-same-owner","--no-same-permissions","-xzf",Arsip_VALUE.toString(),"-C",tujuan_VALUE.toString()).inheritIO().start().waitFor();
        if (Status_VALUE != 0) throw new IOException("의존성 Arsip_VALUE lepas_Storage kegagalan_VALUE");
    }
    static void 호출(Path 작업경로, Path alat, List<String> argumen, Map<String,String> lingkungan) throws Exception {
        List<String> perintah = new ArrayList<>(Arrays.asList("python3", alat.toString())); perintah.addAll(argumen);
        ProcessBuilder Jalankan_perintah = new ProcessBuilder(perintah).directory(작업경로.toFile()).inheritIO(); Jalankan_perintah.environment().putAll(lingkungan);
        int Status_VALUE = Jalankan_perintah.start().waitFor(); if (Status_VALUE != 0) throw new IOException("alat kegagalan_VALUE: " + alat + " (" + Status_VALUE + ")");
    }
    @SuppressWarnings("unchecked")
    public static void main(String[] argumen) throws Exception {
        if (argumen.length < 1) throw new IllegalArgumentException("build, run, desktop, image, check, test-system 중 동작을 지정하세요");
        String Aksi = argumen[0];
        if (!Arrays.asList("build","run","desktop","image","check","test-system").contains(Aksi)) throw new IllegalArgumentException("알 수 없는 Aksi");
        Path Tugas_akar = Paths.get(System.getProperty("worldos.edition.root")).toAbsolutePath().normalize();
        Map<String,Object> Konfigurasi = (Map<String,Object>)new data_parser(Files.readString(Tugas_akar.resolve("native.json"),StandardCharsets.UTF_8)).Baca();
        Path sumber_pohon = internal_jalur(Tugas_akar,(String)Konfigurasi.get("source")), kernel_VALUE = internal_jalur(sumber_pohon,(String)Konfigurasi.get("native"));
        List<String> 소유파일들 = (List<String>)(List<?>)Konfigurasi.get("owned_files");
        for (String Nama_2 : 소유파일들) if (!Files.isRegularFile(internal_jalur(sumber_pohon,Nama_2))) throw new IOException("sumber_pohon 없음: " + Nama_2);
        if (Aksi.equals("check")) { System.out.println(Konfigurasi.get("country") + " " + Konfigurasi.get("language") + " 독립 sumber_pohon periksa 완료"); return; }
        String 자원상대 = (String)Konfigurasi.getOrDefault("resource_root", ".");
        if (!자원상대.equals(".") && !자원상대.equals("..")) throw new IllegalArgumentException("의존성 Tugas_akar jalur galat");
        Path sumber_daya_VALUE = Tugas_akar.resolve(자원상대).normalize(); Path Arsip_VALUE = sumber_daya_VALUE.resolve("native-vendor.tar.gz");
        String 기대해시 = (String)Konfigurasi.get("vendor_sha256");
        if (!hash_file(Arsip_VALUE).equals(기대해시)) throw new IOException("의존성 SHA-256 불일치");
        Path 표식 = sumber_pohon.resolve(".vendor-sha256");
        if (!Files.isRegularFile(표식) || !Files.readString(표식).trim().equals(기대해시)) { ekstrak(Arsip_VALUE, sumber_pohon); Files.writeString(표식,기대해시 + "\n"); }
        Map<String,String> lingkungan = new HashMap<>(System.getenv());
        Path ipConfig = null;
        if (lingkungan.containsKey("IP_CONFIG")) ipConfig = Paths.get(lingkungan.get("IP_CONFIG")).toAbsolutePath().normalize();
        else for (Path parent = Tugas_akar; parent != null; parent = parent.getParent()) {
            if (Files.isRegularFile(parent.resolve("ip.conf"))) { ipConfig = parent.resolve("ip.conf"); break; }
        }
        if (ipConfig == null) ipConfig = sumber_pohon.resolve("ip.conf");
        if (!Files.isRegularFile(ipConfig)) throw new IOException("Missing ip.conf: " + ipConfig);
        lingkungan.put("IP_CONFIG", ipConfig.toString());
        if (Arrays.asList("run","desktop","test-system").contains(Aksi) && !lingkungan.containsKey("QEMU_AARCH64")) {
            Path apl_peluncur = sumber_daya_VALUE.resolve("host/qemu"), 실행기표식 = sumber_daya_VALUE.resolve("host/.qemu-sha256");
            String peluncur_hash = (String)Konfigurasi.get("qemu_sha256");
            if (!Files.isRegularFile(apl_peluncur) || !Files.isRegularFile(실행기표식) || !Files.readString(실행기표식).trim().equals(peluncur_hash)) {
                Path peluncur_Arsip = sumber_daya_VALUE.resolve("qemu-host.tar.gz"); if (!hash_file(peluncur_Arsip).equals(peluncur_hash)) throw new IOException("QEMU SHA-256 불일치");
                ekstrak(peluncur_Arsip,sumber_daya_VALUE.resolve("host")); Files.writeString(실행기표식,peluncur_hash + "\n");
            }
            lingkungan.put("QEMU_AARCH64",apl_peluncur.toString());
        }
        MessageDigest 계산 = MessageDigest.getInstance("SHA-256"); Collections.sort(소유파일들);
        for (String Nama_2 : 소유파일들) { 계산.update(Nama_2.getBytes(StandardCharsets.UTF_8)); 계산.update(Files.readAllBytes(internal_jalur(sumber_pohon,Nama_2))); }
        계산.update("ip.conf\0".getBytes(StandardCharsets.UTF_8)); 계산.update(Files.readAllBytes(ipConfig));
        String sumber_hash = hash_SMS(계산.digest()); Path 빌드표식 = kernel_VALUE.resolve("build/worldos-source.sha256");
        if (Aksi.equals("build") || !Files.isRegularFile(빌드표식) || !Files.readString(빌드표식).trim().equals(sumber_hash)) {
            호출(kernel_VALUE,internal_jalur(kernel_VALUE,(String)Konfigurasi.get("builder")),Collections.emptyList(),lingkungan);
            Files.writeString(빌드표식,sumber_hash + "\n");
        }
        List<String> 추가인수 = new ArrayList<>(Arrays.asList(argumen).subList(1,argumen.length));
        if (Aksi.equals("run") || Aksi.equals("desktop")) {
            if (Aksi.equals("desktop")) 추가인수.add(0,"--desktop");
            호출(kernel_VALUE,internal_jalur(kernel_VALUE,(String)Konfigurasi.get("runner")),추가인수,lingkungan);
        } else if (Aksi.equals("image")) 호출(kernel_VALUE,internal_jalur(kernel_VALUE,(String)Konfigurasi.get("image_builder")),추가인수,lingkungan);
        else if (Aksi.equals("test-system")) {
            추가인수.add(0,Tugas_akar.toString()); 추가인수.add(0,"--edition");
            호출(kernel_VALUE,internal_jalur(kernel_VALUE,(String)Konfigurasi.get("system_tester")),추가인수,lingkungan);
        }
    }
}
