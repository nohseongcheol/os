// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.security.MessageDigest;
import java.util.*;
import java.util.regex.*;

/** Java Kelas_VALUE 파일에서 독립 ARM64 커널용 C 원문을 만든다. host JDK에서 실행한다. */
public final class 기계어미리번역 {
    static final class Terjemahan_kesalahan extends RuntimeException {
        Terjemahan_kesalahan(String 설명) { super(설명); }
    }
    static final class data_Pembaca {
        final byte[] data;
        int posisi;
        data_Pembaca(byte[] 입력자료) { data = 입력자료; }
        byte[] Baca(int panjang_VALUE) {
            if (panjang_VALUE < 0 || panjang_VALUE > data.length - posisi) throw new Terjemahan_kesalahan("잘린 Kelas_VALUE 또는 perintah data");
            byte[] hasil = Arrays.copyOfRange(data, posisi, posisi + panjang_VALUE); posisi += panjang_VALUE; return hasil;
        }
        int 한바이트() { if (posisi >= data.length) throw new Terjemahan_kesalahan("잘린 perintah data"); return data[posisi++] & 255; }
        int 두바이트() { return (한바이트() << 8) | 한바이트(); }
        int 네바이트() { return (두바이트() << 16) | 두바이트(); }
        int 부호한바이트() { return (byte) 한바이트(); }
        int 부호두바이트() { return (short) 두바이트(); }
    }
    static final class anggota_data {
        final int akses_entri;
        final String Nama_2, 서술;
        final Map<String, byte[]> nilai_atribut;
        anggota_data(int akses_VALUE, String nama_VALUE, String 서술값, Map<String, byte[]> atribut_data) {
            akses_entri = akses_VALUE; Nama_2 = nama_VALUE; 서술 = 서술값; nilai_atribut = atribut_data;
        }
    }
    static final class metode_Referensi implements Comparable<metode_Referensi> {
        final String pemilik_VALUE, Nama_2, 서술;
        metode_Referensi(String 소유값, String nama_VALUE, String 서술값) { pemilik_VALUE = 소유값; Nama_2 = nama_VALUE; 서술 = 서술값; }
        String[] 부분들() { return new String[]{pemilik_VALUE, Nama_2, 서술}; }
        public int compareTo(metode_Referensi serekan_VALUE) {
            int Perbandingan_VALUE = pemilik_VALUE.compareTo(serekan_VALUE.pemilik_VALUE);
            if (Perbandingan_VALUE == 0) Perbandingan_VALUE = Nama_2.compareTo(serekan_VALUE.Nama_2);
            return Perbandingan_VALUE == 0 ? 서술.compareTo(serekan_VALUE.서술) : Perbandingan_VALUE;
        }
        public boolean equals(Object serekan_VALUE) { return serekan_VALUE instanceof metode_Referensi && compareTo((metode_Referensi) serekan_VALUE) == 0; }
        public int hashCode() { return Objects.hash(pemilik_VALUE, Nama_2, 서술); }
    }
    static final class Kelas_data {
        final int[] 상수종류;
        final Object[] konstanta_data;
        final String Nama_2;
        final List<anggota_data> nilai_bidang, fungsi_VALUE;
        Kelas_data(Path jalur) throws IOException {
            data_Pembaca Pembaca_VALUE = new data_Pembaca(Files.readAllBytes(jalur));
            if (Pembaca_VALUE.네바이트() != 0xcafebabe) throw new Terjemahan_kesalahan("Java Kelas_VALUE 표식이 아님");
            Pembaca_VALUE.Baca(4);
            int item_COUNT = Pembaca_VALUE.두바이트(); 상수종류 = new int[item_COUNT]; konstanta_data = new Object[item_COUNT];
            for (int 순번 = 1; 순번 < item_COUNT; 순번++) {
                int 종류 = Pembaca_VALUE.한바이트(); 상수종류[순번] = 종류;
                switch (종류) {
                    case 1:
                        int panjang_VALUE = Pembaca_VALUE.두바이트();
                        byte[] karakter_buffer = Pembaca_VALUE.Baca(panjang_VALUE), 길이붙인자료 = new byte[panjang_VALUE + 2];
                        길이붙인자료[0] = (byte)(panjang_VALUE >> 8); 길이붙인자료[1] = (byte)panjang_VALUE;
                        System.arraycopy(karakter_buffer, 0, 길이붙인자료, 2, panjang_VALUE);
                        konstanta_data[순번] = new DataInputStream(new ByteArrayInputStream(길이붙인자료)).readUTF(); break;
                    case 3: konstanta_data[순번] = Pembaca_VALUE.네바이트(); break;
                    case 4: Pembaca_VALUE.Baca(4); break;
                    case 5: case 6: Pembaca_VALUE.Baca(8); 순번++; break;
                    case 7: case 8: case 16: konstanta_data[순번] = Pembaca_VALUE.두바이트(); break;
                    case 9: case 10: case 11: case 12: case 18:
                        konstanta_data[순번] = new int[]{Pembaca_VALUE.두바이트(), Pembaca_VALUE.두바이트()}; break;
                    case 15: konstanta_data[순번] = new int[]{Pembaca_VALUE.한바이트(), Pembaca_VALUE.두바이트()}; break;
                    default: throw new Terjemahan_kesalahan("지원하지 않는 konstanta_VALUE 종류: " + 종류);
                }
            }
            Pembaca_VALUE.두바이트(); Nama_2 = nama_kelas(Pembaca_VALUE.두바이트());
            if (!nama_kelas(Pembaca_VALUE.두바이트()).equals("java/lang/Object") || Pembaca_VALUE.두바이트() != 0)
                throw new Terjemahan_kesalahan(Nama_2 + ": 상속 및 인터페이스 미지원");
            nilai_bidang = 멤버읽기(Pembaca_VALUE); fungsi_VALUE = 멤버읽기(Pembaca_VALUE); 속성읽기(Pembaca_VALUE);
            if (Pembaca_VALUE.posisi != Pembaca_VALUE.data.length) throw new Terjemahan_kesalahan("Kelas_VALUE 뒤에 남은 data");
        }
        String 문자(int INDEX) {
            if (INDEX < 1 || INDEX >= 상수종류.length || 상수종류[INDEX] != 1) throw new Terjemahan_kesalahan("문자 konstanta_VALUE INDEX galat");
            return (String) konstanta_data[INDEX];
        }
        String nama_kelas(int INDEX) {
            if (INDEX < 1 || INDEX >= 상수종류.length || 상수종류[INDEX] != 7) throw new Terjemahan_kesalahan("Kelas_VALUE Referensi galat");
            return 문자((Integer)konstanta_data[INDEX]);
        }
        metode_Referensi Referensi(int INDEX) {
            if (INDEX < 1 || INDEX >= 상수종류.length || 상수종류[INDEX] < 9 || 상수종류[INDEX] > 11) throw new Terjemahan_kesalahan("멤버 Referensi galat");
            int[] pasang_VALUE = (int[])konstanta_data[INDEX], nama_pasang = (int[])konstanta_data[pasang_VALUE[1]];
            return new metode_Referensi(nama_kelas(pasang_VALUE[0]), 문자(nama_pasang[0]), 문자(nama_pasang[1]));
        }
        Map<String, byte[]> 속성읽기(data_Pembaca Pembaca_VALUE) {
            Map<String, byte[]> hasil = new LinkedHashMap<>();
            int item_COUNT = Pembaca_VALUE.두바이트();
            for (int 순번 = 0; 순번 < item_COUNT; 순번++) {
                String atribut_nama = 문자(Pembaca_VALUE.두바이트()); byte[] VALUE = Pembaca_VALUE.Baca(Pembaca_VALUE.네바이트());
                if (hasil.put(atribut_nama, VALUE) != null) throw new Terjemahan_kesalahan("겹친 nilai_atribut: " + atribut_nama);
            }
            return hasil;
        }
        List<anggota_data> 멤버읽기(data_Pembaca Pembaca_VALUE) {
            List<anggota_data> hasil = new ArrayList<>(); int item_COUNT = Pembaca_VALUE.두바이트();
            for (int 순번 = 0; 순번 < item_COUNT; 순번++) {
                int akses_entri = Pembaca_VALUE.두바이트(); String metode_entri_nama = 문자(Pembaca_VALUE.두바이트()), 서술 = 문자(Pembaca_VALUE.두바이트());
                hasil.add(new anggota_data(akses_entri, metode_entri_nama, 서술, 속성읽기(Pembaca_VALUE)));
            }
            return hasil;
        }
    }
    static final class 함수형식 {
        final List<String> argumen = new ArrayList<>();
        final String kembalikan_KR;
        함수형식(String 서술) {
            if (!서술.startsWith("(")) throw new Terjemahan_kesalahan("fungsi_VALUE 서술 galat: " + 서술);
            int 끝 = 서술.indexOf(')'); if (끝 < 0) throw new Terjemahan_kesalahan("fungsi_VALUE 서술 galat: " + 서술);
            argumen.addAll(형식읽기(서술.substring(1, 끝)));
            List<String> 반환들 = 형식읽기(서술.substring(끝 + 1));
            if (argumen.contains("V") || 반환들.size() != 1) throw new Terjemahan_kesalahan("fungsi_VALUE 서술 galat: " + 서술);
            kembalikan_KR = 반환들.get(0);
        }
    }
    static List<String> 형식읽기(String 서술) {
        List<String> hasil = new ArrayList<>();
        String[] 허용형식 = {"Ljava/lang/String;", "[I", "I", "Z", "B", "C", "S", "V"};
        for (int posisi = 0; posisi < 서술.length();) {
            String pilihan_VALUE = null;
            for (String format_VALUE : 허용형식) if (서술.startsWith(format_VALUE, posisi)) { pilihan_VALUE = format_VALUE; break; }
            if (pilihan_VALUE == null) throw new Terjemahan_kesalahan("지원하지 않는 tipe_data: " + 서술);
            hasil.add(pilihan_VALUE); posisi += pilihan_VALUE.length();
        }
        return hasil;
    }
    static String simbol(String 종류, String... 부분들) {
        try {
            byte[] hash_file = MessageDigest.getInstance("SHA-256").digest(String.join("\0", 부분들).getBytes(StandardCharsets.UTF_8));
            StringBuilder teks = new StringBuilder("j_" + 종류 + "_");
            for (int 순번 = 0; 순번 < 12; 순번++) teks.append(String.format(Locale.ROOT, "%02x", hash_file[순번] & 255));
            return teks.toString();
        } catch (Exception galat) { throw new Terjemahan_kesalahan(galat.toString()); }
    }
    final Map<String, Kelas_data> 클래스들 = new TreeMap<>();
    final Map<metode_Referensi, anggota_data> 함수들 = new TreeMap<>(), 필드들 = new TreeMap<>();
    final Map<String, String> 문자열들 = new LinkedHashMap<>(), mesin_Functions_c3a8e64a = new LinkedHashMap<>();
    final String 실행대상, mesin_Kelas;
    final int 동적기억낱말수;
    final Path sumber_daya_jalur;
    기계어미리번역(List<Path> jalur_Daftar, String target, int 낱말수, Path sumber_daya_VALUE) throws IOException {
        if ((!target.equals("kernel") && !target.equals("user")) || 낱말수 < 1024 || 낱말수 > 1048576) throw new Terjemahan_kesalahan("Jalankan_perintah target 또는 Memori_VALUE surel_wilayah Ukuran galat");
        실행대상 = target; 동적기억낱말수 = 낱말수; sumber_daya_jalur = sumber_daya_VALUE;
        // 이 이름도 국가별 sumber_pohon buat 시 해당 언어로 옮긴다.
        mesin_Kelas = target.equals("kernel") ? "Papan" : "ruang_pengguna";
        for (String baris_masukan : Files.readAllLines(sumber_daya_VALUE.resolve("mesin_Functions.tsv"), StandardCharsets.UTF_8)) {
            String[] 부분들 = baris_masukan.split("\t", -1);
            if (부분들.length != 4) throw new Terjemahan_kesalahan("mesin fungsi_VALUE data galat");
            if (부분들[0].equals(target)) mesin_Functions_c3a8e64a.put(부분들[1] + 부분들[2], 부분들[3]);
        }
        for (Path jalur : jalur_Daftar) {
            Kelas_data data = new Kelas_data(jalur);
            if (클래스들.put(data.Nama_2, data) != null) throw new Terjemahan_kesalahan("중복 Kelas_VALUE: " + data.Nama_2);
            for (anggota_data nilai_bidang : data.nilai_bidang) {
                if ((nilai_bidang.akses_entri & 8) == 0 || 형식읽기(nilai_bidang.서술).equals(Collections.singletonList("V"))) throw new Terjemahan_kesalahan("statik_VALUE 필드만 dukung_VALUE");
                if (필드들.put(new metode_Referensi(data.Nama_2, nilai_bidang.Nama_2, nilai_bidang.서술), nilai_bidang) != null) throw new Terjemahan_kesalahan("중복 nilai_bidang");
            }
            for (anggota_data fungsi_VALUE : data.fungsi_VALUE) {
                if (fungsi_VALUE.Nama_2.equals("<init>")) continue;
                if ((fungsi_VALUE.akses_entri & 8) == 0 || (fungsi_VALUE.akses_entri & (0x20 | 0x400)) != 0) throw new Terjemahan_kesalahan("statik_VALUE 비동기화 함수만 dukung_VALUE");
                new 함수형식(fungsi_VALUE.서술);
                if (함수들.put(new metode_Referensi(data.Nama_2, fungsi_VALUE.Nama_2, fungsi_VALUE.서술), fungsi_VALUE) != null) throw new Terjemahan_kesalahan("중복 fungsi_VALUE");
            }
        }
    }
    String string_simbol(String teks) { return 문자열들.computeIfAbsent(teks, VALUE -> "j_text_" + 문자열들.size()); }
    String konstanta_ekspresi(Kelas_data data, int INDEX) {
        if (INDEX < 1 || INDEX >= data.상수종류.length) throw new Terjemahan_kesalahan("konstanta_VALUE INDEX klip galat");
        if (data.상수종류[INDEX] == 3) return "(word)(uint32_t)(" + data.konstanta_data[INDEX] + ")";
        if (data.상수종류[INDEX] == 8) return "(word)" + string_simbol(data.문자((Integer)data.konstanta_data[INDEX]));
        throw new Terjemahan_kesalahan("정수와 string_VALUE 상수만 dukung_VALUE");
    }
    String 함수원형(metode_Referensi Referensi) {
        List<String> 인수들 = new ArrayList<>(); int item_COUNT = new 함수형식(Referensi.서술).argumen.size();
        for (int 순번 = 0; 순번 < item_COUNT; 순번++) 인수들.add("word a" + 순번);
        return "static word " + simbol("method", Referensi.부분들()) + "(" + (item_COUNT == 0 ? "void" : String.join(", ", 인수들)) + ")";
    }
    void cek_lokal(int INDEX, int lokal_variabel_COUNT) { if (INDEX < 0 || INDEX >= lokal_variabel_COUNT) throw new Terjemahan_kesalahan("lokal_Cakupan variabel_VALUE INDEX klip galat"); }
    void 분기넣기(List<String> keluaranTeks, Set<Integer> cabang_Daftar, int posisi, int 이동량, String kondisi) {
        int tujuan_VALUE = posisi + 이동량; cabang_Daftar.add(tujuan_VALUE);
        keluaranTeks.add((kondisi == null ? "" : "if (" + kondisi + ") ") + "goto b" + tujuan_VALUE + ";");
    }
    String metode_isi(metode_Referensi fungsi_VALUE, anggota_data data) {
        byte[] isi_data = data.nilai_atribut.get("Code"); if (isi_data == null) throw new Terjemahan_kesalahan("fungsi_VALUE 몸체가 없음: " + fungsi_VALUE.Nama_2);
        data_Pembaca Pembaca_VALUE = new data_Pembaca(isi_data); int 쌓임깊이 = Pembaca_VALUE.두바이트(), lokal_variabel_COUNT = Pembaca_VALUE.두바이트();
        data_Pembaca perintah_data = new data_Pembaca(Pembaca_VALUE.Baca(Pembaca_VALUE.네바이트()));
        if (Pembaca_VALUE.두바이트() != 0) throw new Terjemahan_kesalahan("try/catch/finally 미지원");
        함수형식 format_VALUE = new 함수형식(fungsi_VALUE.서술); if (lokal_variabel_COUNT < format_VALUE.argumen.size()) throw new Terjemahan_kesalahan("매개변수보다 적은 lokal_Cakupan variabel_VALUE");
        Kelas_data Kelas_VALUE = 클래스들.get(fungsi_VALUE.pemilik_VALUE);
        List<String> keluaranTeks = new ArrayList<>(); keluaranTeks.add(함수원형(fungsi_VALUE) + " {");
        keluaranTeks.add("word s[" + Math.max(쌓임깊이, 1) + "], l[" + Math.max(lokal_variabel_COUNT, 1) + "] = {0}, a,b,c,d; size_t sp = 0;");
        for (int 순번 = 0; 순번 < format_VALUE.argumen.size(); 순번++) keluaranTeks.add("l[" + 순번 + "] = a" + 순번 + ";");
        Set<Integer> 경계들 = new HashSet<>(), cabang_Daftar = new HashSet<>();
        String[] 비교들 = {"==", "!=", "<", ">=", ">", "<=", "==", "!="};
        while (perintah_data.posisi < perintah_data.data.length) {
            int posisi = perintah_data.posisi, perintah = perintah_data.한바이트(); 경계들.add(posisi); keluaranTeks.add("b" + posisi + ":;");
            if (perintah == 0) continue;
            if (perintah == 1) keluaranTeks.add("PUSH(0);");
            else if (perintah >= 2 && perintah <= 8) keluaranTeks.add("PUSH((uint32_t)(" + (perintah - 3) + "));");
            else if (perintah == 16 || perintah == 17) keluaranTeks.add("PUSH((uint32_t)(" + (perintah == 16 ? perintah_data.부호한바이트() : perintah_data.부호두바이트()) + "));");
            else if (perintah == 18 || perintah == 19) keluaranTeks.add("PUSH(" + konstanta_ekspresi(Kelas_VALUE, perintah == 18 ? perintah_data.한바이트() : perintah_data.두바이트()) + ");");
            else if (perintah == 21 || perintah == 25 || (perintah >= 26 && perintah <= 29) || (perintah >= 42 && perintah <= 45)) {
                int INDEX = perintah == 21 || perintah == 25 ? perintah_data.한바이트() : perintah - (perintah <= 29 ? 26 : 42);
                cek_lokal(INDEX, lokal_variabel_COUNT); keluaranTeks.add("PUSH(l[" + INDEX + "]);");
            } else if (perintah == 54 || perintah == 58 || (perintah >= 59 && perintah <= 62) || (perintah >= 75 && perintah <= 78)) {
                int INDEX = perintah == 54 || perintah == 58 ? perintah_data.한바이트() : perintah - (perintah <= 62 ? 59 : 75);
                cek_lokal(INDEX, lokal_variabel_COUNT); keluaranTeks.add("l[" + INDEX + "] = POP();");
            } else if (perintah == 46) keluaranTeks.add("b = POP(); a = POP(); PUSH(*checked(a,(int32_t)b));");
            else if (perintah == 79) keluaranTeks.add("c = POP(); b = POP(); a = POP(); *checked(a,(int32_t)b) = (uint32_t)c;");
            else if (perintah == 87 || perintah == 88) keluaranTeks.add(perintah == 87 ? "(void)POP();" : "(void)POP(); (void)POP();");
            else if (perintah >= 89 && perintah <= 95) {
                int[] 개수들 = {1,2,3,2,3,4,2}; String[] urutan_Daftar = {"aa","aba","acba","baba","bacba","badcba","ab"};
                for (int 순번 = 0; 순번 < 개수들[perintah - 89]; 순번++) keluaranTeks.add("abcd".charAt(순번) + " = POP();");
                for (char VALUE : urutan_Daftar[perintah - 89].toCharArray()) keluaranTeks.add("PUSH(" + VALUE + ");");
            } else if (perintah == 96 || perintah == 100 || perintah == 104 || perintah == 126 || perintah == 128 || perintah == 130) {
                String bedah_VALUE = perintah == 96 ? "+" : perintah == 100 ? "-" : perintah == 104 ? "*" : perintah == 126 ? "&" : perintah == 128 ? "|" : "^";
                keluaranTeks.add("b = POP(); a = POP(); PUSH((uint32_t)a " + bedah_VALUE + " (uint32_t)b);");
            } else if (perintah == 108 || perintah == 112) keluaranTeks.add("b = POP(); a = POP(); PUSH(divide(a,b," + (perintah == 112 ? 1 : 0) + "));");
            else if (perintah == 116) keluaranTeks.add("a = POP(); PUSH(0u-(uint32_t)a);");
            else if (perintah == 120 || perintah == 122 || perintah == 124) {
                keluaranTeks.add("b = POP(); a = POP();"); keluaranTeks.add("PUSH(" + (perintah == 122 ? "arithmetic_shift(a,b)" : "(uint32_t)a " + (perintah == 120 ? "<<" : ">>") + " ((uint32_t)b & 31)") + ");");
            } else if (perintah == 132) {
                int INDEX = perintah_data.한바이트(), tahapan_jumlah = perintah_data.부호한바이트(); cek_lokal(INDEX, lokal_variabel_COUNT);
                keluaranTeks.add("l[" + INDEX + "] = (uint32_t)l[" + INDEX + "] + (uint32_t)(" + tahapan_jumlah + ");");
            } else if (perintah >= 145 && perintah <= 147) keluaranTeks.add("a = POP(); PUSH((uint32_t)(" + (perintah == 145 ? "int8_t" : perintah == 146 ? "uint16_t" : "int16_t") + ")a);");
            else if (perintah >= 153 && perintah <= 158) {
                keluaranTeks.add("a = POP();"); 분기넣기(keluaranTeks, cabang_Daftar, posisi, perintah_data.부호두바이트(), "(int32_t)a " + 비교들[perintah - 153] + " 0");
            } else if (perintah >= 159 && perintah <= 166) {
                keluaranTeks.add("b = POP(); a = POP();"); 분기넣기(keluaranTeks, cabang_Daftar, posisi, perintah_data.부호두바이트(), perintah >= 165 ? "a " + 비교들[perintah - 159] + " b" : "(int32_t)a " + 비교들[perintah - 159] + " (int32_t)b");
            } else if (perintah == 167 || perintah == 200) 분기넣기(keluaranTeks, cabang_Daftar, posisi, perintah == 167 ? perintah_data.부호두바이트() : perintah_data.네바이트(), null);
            else if (perintah == 170 || perintah == 171) {
                while (perintah_data.posisi % 4 != 0) perintah_data.한바이트();
                int nilai_default = perintah_data.네바이트(); keluaranTeks.add("a = POP();");
                if (perintah == 170) {
                    int 아래 = perintah_data.네바이트(), 위 = perintah_data.네바이트(); long item_COUNT = (long)위 - 아래 + 1;
                    if (item_COUNT < 1 || item_COUNT > (perintah_data.data.length - perintah_data.posisi) / 4) throw new Terjemahan_kesalahan("switch klip galat");
                    for (long VALUE = 아래; VALUE <= 위; VALUE++) 분기넣기(keluaranTeks, cabang_Daftar, posisi, perintah_data.네바이트(), "(int32_t)a == (" + VALUE + ")");
                } else {
                    int item_COUNT = perintah_data.네바이트(), depan_data = 0;
                    if (item_COUNT < 0 || item_COUNT > (perintah_data.data.length - perintah_data.posisi) / 8) throw new Terjemahan_kesalahan("switch Ukuran galat");
                    for (int 순번 = 0; 순번 < item_COUNT; 순번++) {
                        int VALUE = perintah_data.네바이트(); if (순번 > 0 && VALUE <= depan_data) throw new Terjemahan_kesalahan("switch urutan_VALUE galat"); depan_data = VALUE;
                        분기넣기(keluaranTeks, cabang_Daftar, posisi, perintah_data.네바이트(), "(int32_t)a == (" + VALUE + ")");
                    }
                }
                분기넣기(keluaranTeks, cabang_Daftar, posisi, nilai_default, null);
            } else if (perintah == 172 || perintah == 176 || perintah == 177) keluaranTeks.add("return " + (perintah == 177 ? "0" : "POP()") + ";");
            else if (perintah == 178 || perintah == 179) {
                metode_Referensi Referensi = Kelas_VALUE.Referensi(perintah_data.두바이트()); if (!필드들.containsKey(Referensi)) throw new Terjemahan_kesalahan("알 수 없는 nilai_bidang");
                keluaranTeks.add(simbol("init", Referensi.pemilik_VALUE) + "();"); String nilai_bidang = simbol("field", Referensi.부분들());
                keluaranTeks.add(perintah == 178 ? "PUSH(" + nilai_bidang + ");" : nilai_bidang + " = POP();");
            } else if (perintah == 184) {
                metode_Referensi Referensi = Kelas_VALUE.Referensi(perintah_data.두바이트()); if (!함수들.containsKey(Referensi)) throw new Terjemahan_kesalahan("알 수 없는 fungsi_VALUE");
                함수형식 호출형식 = new 함수형식(Referensi.서술); int item_COUNT = 호출형식.argumen.size();
                keluaranTeks.add(simbol("init", Referensi.pemilik_VALUE) + "();"); keluaranTeks.add("if(sp < " + item_COUNT + ") kernel_panic(\"call stack underflow\"); sp -= " + item_COUNT + ";");
                List<String> 호출인수 = new ArrayList<>(); for (int 순번 = 0; 순번 < item_COUNT; 순번++) 호출인수.add("s[sp + " + 순번 + "]");
                keluaranTeks.add("a = " + simbol("method", Referensi.부분들()) + "(" + String.join(",", 호출인수) + ");");
                if (!호출형식.kembalikan_KR.equals("V")) keluaranTeks.add("PUSH(a);");
            } else if (perintah == 182) {
                metode_Referensi Referensi = Kelas_VALUE.Referensi(perintah_data.두바이트());
                if (Referensi.equals(new metode_Referensi("java/lang/String", "length", "()I"))) keluaranTeks.add("a = POP(); PUSH(length(a));");
                else if (Referensi.equals(new metode_Referensi("java/lang/String", "charAt", "(I)C"))) keluaranTeks.add("b = POP(); a = POP(); PUSH(*checked(a,(int32_t)b));");
                else throw new Terjemahan_kesalahan("가상 fungsi_VALUE 호출 미지원");
            } else if (perintah == 188) {
                if (perintah_data.한바이트() != 10) throw new Terjemahan_kesalahan("new int[]만 dukung_VALUE"); keluaranTeks.add("a = POP(); PUSH(new_array((int32_t)a));");
            } else if (perintah == 190) keluaranTeks.add("a = POP(); PUSH(length(a));");
            else if (perintah == 196) {
                int ekstensi_VALUE = perintah_data.한바이트(), INDEX = perintah_data.두바이트(); cek_lokal(INDEX, lokal_variabel_COUNT);
                if (ekstensi_VALUE == 21 || ekstensi_VALUE == 25) keluaranTeks.add("PUSH(l[" + INDEX + "]);");
                else if (ekstensi_VALUE == 54 || ekstensi_VALUE == 58) keluaranTeks.add("l[" + INDEX + "] = POP();");
                else if (ekstensi_VALUE == 132) keluaranTeks.add("l[" + INDEX + "] = (uint32_t)l[" + INDEX + "] + (uint32_t)(" + perintah_data.부호두바이트() + ");");
                else throw new Terjemahan_kesalahan("미지원 wide perintah");
            } else if (perintah == 198 || perintah == 199) {
                keluaranTeks.add("a = POP();"); 분기넣기(keluaranTeks, cabang_Daftar, posisi, perintah_data.부호두바이트(), "a " + (perintah == 198 ? "==" : "!=") + " 0");
            } else throw new Terjemahan_kesalahan(fungsi_VALUE.pemilik_VALUE + "." + fungsi_VALUE.Nama_2 + ", byte_VALUE " + posisi + ": 미지원 perintah " + perintah);
        }
        if (!경계들.containsAll(cabang_Daftar)) throw new Terjemahan_kesalahan("perintah 경계가 아닌 곳으로 cabang");
        keluaranTeks.add("kernel_panic(\"method fell through\"); }"); return String.join("\n", keluaranTeks);
    }
    String Ekspor_metode(String link_simbol, String target, boolean 진입점여부) {
        int posisi_INDEX = target.lastIndexOf('.'); if (posisi_INDEX < 0 || !link_simbol.matches("[A-Za-z_][A-Za-z0-9_]*")) throw new Terjemahan_kesalahan("내보내기 Tugaskan_VALUE galat");
        String pemilik_VALUE = target.substring(0, posisi_INDEX).replace('.', '/'), Nama_2 = target.substring(posisi_INDEX + 1); metode_Referensi pilihan_VALUE = null;
        for (metode_Referensi Referensi : 함수들.keySet()) if (Referensi.pemilik_VALUE.equals(pemilik_VALUE) && Referensi.Nama_2.equals(Nama_2)) {
            if (pilihan_VALUE != null) throw new Terjemahan_kesalahan("겹친 내보내기 target"); pilihan_VALUE = Referensi;
        }
        if (pilihan_VALUE == null || (함수들.get(pilihan_VALUE).akses_entri & 0x100) != 0) throw new Terjemahan_kesalahan("내보낼 함수가 없음 또는 native fungsi_VALUE");
        함수형식 format_VALUE = new 함수형식(pilihan_VALUE.서술);
        if ((진입점여부 && !format_VALUE.argumen.isEmpty()) || !Arrays.asList("V", "I").contains(format_VALUE.kembalikan_KR)) throw new Terjemahan_kesalahan("entri_p_VALUE 또는 C 경계 format_VALUE galat");
        List<String> 인수들 = new ArrayList<>(), 호출인수 = new ArrayList<>();
        for (int 순번 = 0; 순번 < format_VALUE.argumen.size(); 순번++) {
            if (!format_VALUE.argumen.get(순번).equals("I")) throw new Terjemahan_kesalahan("C 경계는 int 인수만 dukung_VALUE");
            인수들.add("int32_t a" + 순번); 호출인수.add("(uint32_t)a" + 순번);
        }
        return (format_VALUE.kembalikan_KR.equals("V") ? "void " : "int32_t ") + link_simbol + "(" + (인수들.isEmpty() ? "void" : String.join(",", 인수들)) + ") { " + simbol("init", pilihan_VALUE.pemilik_VALUE) + "(); " + (format_VALUE.kembalikan_KR.equals("V") ? "" : "return (int32_t)") + simbol("method", pilihan_VALUE.부분들()) + "(" + String.join(",", 호출인수) + "); }";
    }
    String buat(String entri_p, List<String> 내보내기목록, boolean 범용표기) throws IOException {
        List<String> 선언들 = new ArrayList<>(), 몸체들 = new ArrayList<>(), 필드선언들 = new ArrayList<>();
        for (Map.Entry<metode_Referensi, anggota_data> entri_VALUE : 함수들.entrySet()) {
            metode_Referensi Referensi = entri_VALUE.getKey(); anggota_data data = entri_VALUE.getValue(); 선언들.add(함수원형(Referensi) + ";");
            if ((data.akses_entri & 0x100) != 0) {
                String Sambung = mesin_Functions_c3a8e64a.get(Referensi.Nama_2 + Referensi.서술);
                if (!Referensi.pemilik_VALUE.equals(mesin_Kelas) || Sambung == null) throw new Terjemahan_kesalahan("허용되지 않은 native fungsi_VALUE: " + Referensi.Nama_2);
                int item_COUNT = new 함수형식(Referensi.서술).argumen.size(); List<String> 인수들 = new ArrayList<>();
                for (int 순번 = 0; 순번 < item_COUNT; 순번++) 인수들.add("a" + 순번);
                선언들.add("extern word " + Sambung + "(" + (item_COUNT == 0 ? "void" : String.join(",", Collections.nCopies(item_COUNT, "word"))) + ");");
                몸체들.add(함수원형(Referensi) + " { return " + Sambung + "(" + String.join(",", 인수들) + "); }");
            } else 몸체들.add(metode_isi(Referensi, data));
        }
        for (Map.Entry<metode_Referensi, anggota_data> entri_VALUE : 필드들.entrySet()) {
            metode_Referensi Referensi = entri_VALUE.getKey(); byte[] konstanta_VALUE = entri_VALUE.getValue().nilai_atribut.get("ConstantValue");
            String VALUE = konstanta_VALUE == null ? "0" : konstanta_ekspresi(클래스들.get(Referensi.pemilik_VALUE), new data_Pembaca(konstanta_VALUE).두바이트());
            필드선언들.add("static word " + simbol("field", Referensi.부분들()) + " = " + VALUE + ";");
        }
        for (String Nama_2 : 클래스들.keySet()) {
            String inisialisasi = simbol("init", Nama_2), Status_VALUE = simbol("state", Nama_2);
            선언들.add("static void " + inisialisasi + "(void);"); 필드선언들.add("static unsigned " + Status_VALUE + ";");
            metode_Referensi Referensi = new metode_Referensi(Nama_2, "<clinit>", "()V");
            몸체들.add("static void " + inisialisasi + "(void) { if(" + Status_VALUE + ") return; " + Status_VALUE + " = 1; " + (함수들.containsKey(Referensi) ? simbol("method", Referensi.부분들()) + "(); " : "") + Status_VALUE + " = 2; }");
        }
        몸체들.add(Ekspor_metode("java_entry", entri_p, true)); Set<String> 공개이름 = new HashSet<>();
        for (String Tugaskan_VALUE : 내보내기목록) {
            int posisi_INDEX = Tugaskan_VALUE.indexOf('='); if (posisi_INDEX < 1) throw new Terjemahan_kesalahan("내보내기 Tugaskan_VALUE galat");
            String Nama_2 = Tugaskan_VALUE.substring(0, posisi_INDEX); 공개이름.add(Nama_2); 몸체들.add(Ekspor_metode(Nama_2, Tugaskan_VALUE.substring(posisi_INDEX + 1), false));
        }
        List<String> 문자열선언들 = new ArrayList<>();
        for (Map.Entry<String, String> entri_VALUE : 문자열들.entrySet()) {
            String teks = entri_VALUE.getKey(); StringBuilder ARRAY_VALUE = new StringBuilder("static const word " + entri_VALUE.getValue() + "[] = {" + teks.length());
            for (int 순번 = 0; 순번 < teks.length(); 순번++) ARRAY_VALUE.append(", ").append((int)teks.charAt(순번));
            문자열선언들.add(ARRAY_VALUE.append("};").toString());
        }
        String dukung_VALUE = Files.readString(sumber_daya_jalur.resolve("runtime_bahasa_umum_dukung.c.txt"), StandardCharsets.UTF_8).replace("262144", Integer.toString(동적기억낱말수));
        return 기계원문한국어화(dukung_VALUE + String.join("\n", 문자열선언들) + "\n" + String.join("\n", 선언들) + "\n" + String.join("\n", 필드선언들) + "\n" + String.join("\n", 몸체들) + "\n", 공개이름, 범용표기);
    }
    String 기계원문한국어화(String kodeSumber, Set<String> 공개이름, boolean 범용표기) throws IOException {
        Map<String, String> nama_tabel = new HashMap<>();
        for (String baris_masukan : Files.readAllLines(sumber_daya_jalur.resolve("생성이름.tsv"), StandardCharsets.UTF_8)) {
            String[] pasang_VALUE = baris_masukan.split("\t"); nama_tabel.put(pasang_VALUE[0], pasang_VALUE[1]);
        }
        Pattern gugus_ekspresi = Pattern.compile("//[^\\n]*|/\\*[\\s\\S]*?\\*/|\"(?:\\\\.|[^\"\\\\])*\"|'(?:\\\\.|[^'\\\\])*'|\\b[A-Za-z_]\\w*\\b");
        Matcher 찾개 = gugus_ekspresi.matcher(kodeSumber); StringBuffer hasil = new StringBuffer();
        while (찾개.find()) {
            String Nama_2 = 찾개.group(), 새이름 = Nama_2;
            if (!Nama_2.startsWith("//") && !Nama_2.startsWith("/*") && !Nama_2.startsWith("\"") && !Nama_2.startsWith("'") && !공개이름.contains(Nama_2)) {
                새이름 = nama_tabel.getOrDefault(Nama_2, Nama_2);
                if (Nama_2.matches("a[0-9]+")) 새이름 = "argumen" + Nama_2.substring(1);
                if (Nama_2.matches("b[0-9]+")) 새이름 = "cabang" + Nama_2.substring(1);
                if (범용표기) {
                    StringBuilder notasi_VALUE = new StringBuilder();
                    for (char karakter_VALUE : 새이름.toCharArray()) notasi_VALUE.append(karakter_VALUE < 128 ? Character.toString(karakter_VALUE) : String.format(Locale.ROOT, "\\u%04x", (int)karakter_VALUE));
                    새이름 = notasi_VALUE.toString();
                }
            }
            찾개.appendReplacement(hasil, Matcher.quoteReplacement(새이름));
        }
        찾개.appendTail(hasil); return hasil.toString();
    }
    String X_86_metode_isi(metode_Referensi fungsi_VALUE, anggota_data data, Map<String,String> mesin_tabel, String target) {
        String 표식 = simbol("method", fungsi_VALUE.부분들());
        List<String> baris_masukan = new ArrayList<>();
        if ((data.akses_entri & 0x100) != 0) {
            String Sambung = mesin_tabel.get(fungsi_VALUE.Nama_2 + fungsi_VALUE.서술);
            if (!fungsi_VALUE.pemilik_VALUE.equals(target.equals("kernel") ? "Ponsel_VALUE" : "ruang_pengguna") || Sambung == null) throw new Terjemahan_kesalahan("허용되지 않은 native fungsi_VALUE");
            return ".text\n" + 표식 + ":\njmp " + Sambung;
        }
        byte[] teks_isi = data.nilai_atribut.get("Code"); if (teks_isi == null) throw new Terjemahan_kesalahan("fungsi_VALUE 몸체가 없음");
        data_Pembaca Pembaca_VALUE = new data_Pembaca(teks_isi); Pembaca_VALUE.두바이트(); int lokal_COUNT = Pembaca_VALUE.두바이트();
        data_Pembaca perintah_data = new data_Pembaca(Pembaca_VALUE.Baca(Pembaca_VALUE.네바이트()));
        if (Pembaca_VALUE.두바이트() != 0) throw new Terjemahan_kesalahan("try/catch/finally 미지원");
        함수형식 format_VALUE = new 함수형식(fungsi_VALUE.서술); if (lokal_COUNT < format_VALUE.argumen.size()) throw new Terjemahan_kesalahan("매개변수보다 적은 lokal_Cakupan variabel_VALUE");
        Collections.addAll(baris_masukan,".text",".globl " + 표식,".type " + 표식 + ", @function",표식 + ":","pushl %ebp","movl %esp, %ebp","subl $" + lokal_COUNT * 4 + ", %esp");
        for (int 순번 = 0; 순번 < format_VALUE.argumen.size(); 순번++) Collections.addAll(baris_masukan,"movl " + (8 + 4 * (format_VALUE.argumen.size() - 순번 - 1)) + "(%ebp), %eax","movl %eax, -" + (4 * (순번 + 1)) + "(%ebp)");
        Kelas_data Kelas_VALUE = 클래스들.get(fungsi_VALUE.pemilik_VALUE); Set<Integer> 경계들 = new HashSet<>(), cabang_Daftar = new HashSet<>();
        String[] 비교들 = {"je","jne","jl","jge","jg","jle","je","jne"};
        while (perintah_data.posisi < perintah_data.data.length) {
            int posisi = perintah_data.posisi, perintah = perintah_data.한바이트(); String posisi_INDEX = 표식 + "_b" + posisi;
            baris_masukan.add(posisi_INDEX + ":"); 경계들.add(posisi);
            if (perintah == 0) baris_masukan.add("nop");
            else if (perintah == 1) baris_masukan.add("pushl $0");
            else if (perintah >= 2 && perintah <= 8) baris_masukan.add("pushl $" + (perintah - 3));
            else if (perintah == 16 || perintah == 17) baris_masukan.add("pushl $" + (perintah == 16 ? perintah_data.부호한바이트() : perintah_data.부호두바이트()));
            else if (perintah == 18 || perintah == 19) {
                int INDEX = perintah == 18 ? perintah_data.한바이트() : perintah_data.두바이트();
                baris_masukan.add("pushl $" + X_86_konstanta(Kelas_VALUE,INDEX));
            } else if (perintah == 21 || perintah == 25 || (perintah >= 26 && perintah <= 29) || (perintah >= 42 && perintah <= 45) || perintah == 54 || perintah == 58 || (perintah >= 59 && perintah <= 62) || (perintah >= 75 && perintah <= 78)) {
                boolean 읽음 = perintah < 54; int INDEX = perintah == 21 || perintah == 25 || perintah == 54 || perintah == 58 ? perintah_data.한바이트() : perintah - (perintah <= 29 ? 26 : perintah <= 45 ? 42 : perintah <= 62 ? 59 : 75);
                cek_lokal(INDEX,lokal_COUNT); baris_masukan.add((읽음 ? "pushl " : "popl ") + "-" + (4 * (INDEX + 1)) + "(%ebp)");
            } else if (perintah == 46) Collections.addAll(baris_masukan,"popl %ecx","popl %eax","call rt_array_check","pushl 4(%eax,%ecx,4)");
            else if (perintah == 79) Collections.addAll(baris_masukan,"popl %edx","popl %ecx","popl %eax","call rt_array_check","movl %edx, 4(%eax,%ecx,4)");
            else if (perintah == 87 || perintah == 88) baris_masukan.add("addl $" + (perintah == 87 ? 4 : 8) + ", %esp");
            else if (perintah >= 89 && perintah <= 95) {
                int[] 개수들 = {1,2,3,2,3,4,2}; int[][] urutan_Daftar = {{0,0},{0,1,0},{0,2,1,0},{1,0,1,0},{1,0,2,1,0},{1,0,3,2,1,0},{0,1}}; String[] 저장기들 = {"%eax","%ecx","%edx","%ebx"};
                for (int 순번 = 0; 순번 < 개수들[perintah - 89]; 순번++) baris_masukan.add("popl " + 저장기들[순번]);
                for (int 순번 : urutan_Daftar[perintah - 89]) baris_masukan.add("pushl " + 저장기들[순번]);
            } else if (perintah == 96 || perintah == 100 || perintah == 104 || perintah == 126 || perintah == 128 || perintah == 130) {
                String bedah_VALUE = perintah == 96 ? "addl" : perintah == 100 ? "subl" : perintah == 104 ? "imull" : perintah == 126 ? "andl" : perintah == 128 ? "orl" : "xorl";
                Collections.addAll(baris_masukan,"popl %ecx","popl %eax",bedah_VALUE + " %ecx, %eax","pushl %eax");
            } else if (perintah == 108 || perintah == 112) Collections.addAll(baris_masukan,"popl %ecx","popl %eax","testl %ecx, %ecx","jz rt_div_zero","cmpl $-1, %ecx","jne " + posisi_INDEX + "_divide","cmpl $0x80000000, %eax","jne " + posisi_INDEX + "_divide","xorl %edx, %edx","jmp " + posisi_INDEX + "_done",posisi_INDEX + "_divide:","cltd","idivl %ecx",posisi_INDEX + "_done:","pushl " + (perintah == 108 ? "%eax" : "%edx"));
            else if (perintah == 116) baris_masukan.add("negl (%esp)");
            else if (perintah == 120 || perintah == 122 || perintah == 124) Collections.addAll(baris_masukan,"popl %ecx","popl %eax",(perintah == 120 ? "sall" : perintah == 122 ? "sarl" : "shrl") + " %cl, %eax","pushl %eax");
            else if (perintah == 132) {
                int INDEX = perintah_data.한바이트(), tahapan_VALUE = perintah_data.부호한바이트(); cek_lokal(INDEX,lokal_COUNT); baris_masukan.add("addl $" + tahapan_VALUE + ", -" + (4 * (INDEX + 1)) + "(%ebp)");
            } else if (perintah >= 145 && perintah <= 147) Collections.addAll(baris_masukan,"popl %eax",perintah == 145 ? "movsbl %al, %eax" : perintah == 146 ? "movzwl %ax, %eax" : "movswl %ax, %eax","pushl %eax");
            else if (perintah >= 153 && perintah <= 166) {
                if (perintah <= 158) Collections.addAll(baris_masukan,"popl %eax","testl %eax, %eax");
                else Collections.addAll(baris_masukan,"popl %ecx","popl %eax","cmpl %ecx, %eax");
                int tujuan_VALUE = posisi + perintah_data.부호두바이트(); cabang_Daftar.add(tujuan_VALUE); baris_masukan.add(비교들[perintah - (perintah <= 158 ? 153 : 159)] + " " + 표식 + "_b" + tujuan_VALUE);
            } else if (perintah == 167 || perintah == 200) {
                int tujuan_VALUE = posisi + (perintah == 167 ? perintah_data.부호두바이트() : perintah_data.네바이트()); cabang_Daftar.add(tujuan_VALUE); baris_masukan.add("jmp " + 표식 + "_b" + tujuan_VALUE);
            } else if (perintah == 170 || perintah == 171) {
                while (perintah_data.posisi % 4 != 0) perintah_data.한바이트();
                int nilai_default = posisi + perintah_data.네바이트(); cabang_Daftar.add(nilai_default); baris_masukan.add("popl %eax");
                int item_COUNT, 아래 = 0;
                if (perintah == 170) { 아래 = perintah_data.네바이트(); int 위 = perintah_data.네바이트(); long panjang_VALUE = (long)위 - 아래 + 1; if (panjang_VALUE < 1 || panjang_VALUE > (perintah_data.data.length - perintah_data.posisi) / 4) throw new Terjemahan_kesalahan("switch klip galat"); item_COUNT = (int)panjang_VALUE; }
                else { item_COUNT = perintah_data.네바이트(); if (item_COUNT < 0 || item_COUNT > (perintah_data.data.length - perintah_data.posisi) / 8) throw new Terjemahan_kesalahan("switch Ukuran galat"); }
                for (int 순번 = 0; 순번 < item_COUNT; 순번++) {
                    int VALUE = perintah == 170 ? 아래 + 순번 : perintah_data.네바이트(), tujuan_VALUE = posisi + perintah_data.네바이트(); cabang_Daftar.add(tujuan_VALUE);
                    Collections.addAll(baris_masukan,"cmpl $" + VALUE + ", %eax","je " + 표식 + "_b" + tujuan_VALUE);
                }
                baris_masukan.add("jmp " + 표식 + "_b" + nilai_default);
            } else if (perintah == 172 || perintah == 176 || perintah == 177) {
                if (perintah != 177) baris_masukan.add("popl %eax"); Collections.addAll(baris_masukan,"leave","ret");
            } else if (perintah == 178 || perintah == 179) {
                metode_Referensi Referensi = Kelas_VALUE.Referensi(perintah_data.두바이트()); if (!필드들.containsKey(Referensi)) throw new Terjemahan_kesalahan("알 수 없는 nilai_bidang");
                Collections.addAll(baris_masukan,"call " + simbol("init",Referensi.pemilik_VALUE),(perintah == 178 ? "pushl " : "popl ") + simbol("field",Referensi.부분들()));
            } else if (perintah == 184) {
                metode_Referensi Referensi = Kelas_VALUE.Referensi(perintah_data.두바이트()); if (!함수들.containsKey(Referensi)) throw new Terjemahan_kesalahan("알 수 없는 fungsi_VALUE");
                함수형식 호출형식 = new 함수형식(Referensi.서술); Collections.addAll(baris_masukan,"call " + simbol("init",Referensi.pemilik_VALUE),"call " + simbol("method",Referensi.부분들()));
                if (!호출형식.argumen.isEmpty()) baris_masukan.add("addl $" + 호출형식.argumen.size() * 4 + ", %esp");
                if (!호출형식.kembalikan_KR.equals("V")) baris_masukan.add("pushl %eax");
            } else if (perintah == 182) {
                metode_Referensi Referensi = Kelas_VALUE.Referensi(perintah_data.두바이트());
                if (Referensi.equals(new metode_Referensi("java/lang/String","length","()I"))) Collections.addAll(baris_masukan,"popl %eax","testl %eax, %eax","jz rt_null","pushl (%eax)");
                else if (Referensi.equals(new metode_Referensi("java/lang/String","charAt","(I)C"))) Collections.addAll(baris_masukan,"popl %ecx","popl %eax","call rt_array_check","pushl 4(%eax,%ecx,4)");
                else throw new Terjemahan_kesalahan("가상 fungsi_VALUE 호출 미지원");
            } else if (perintah == 188) {
                if (perintah_data.한바이트() != 10) throw new Terjemahan_kesalahan("new int[]만 dukung_VALUE"); Collections.addAll(baris_masukan,"popl %eax","call rt_new_array","pushl %eax");
            } else if (perintah == 190) Collections.addAll(baris_masukan,"popl %eax","testl %eax, %eax","jz rt_null","pushl (%eax)");
            else if (perintah == 196) {
                int ekstensi_VALUE = perintah_data.한바이트(), INDEX = perintah_data.두바이트(); cek_lokal(INDEX,lokal_COUNT);
                if (ekstensi_VALUE == 21 || ekstensi_VALUE == 25 || ekstensi_VALUE == 54 || ekstensi_VALUE == 58) baris_masukan.add((ekstensi_VALUE <= 25 ? "pushl " : "popl ") + "-" + 4 * (INDEX + 1) + "(%ebp)");
                else if (ekstensi_VALUE == 132) baris_masukan.add("addl $" + perintah_data.부호두바이트() + ", -" + 4 * (INDEX + 1) + "(%ebp)");
                else throw new Terjemahan_kesalahan("wide perintah 미지원");
            } else if (perintah == 198 || perintah == 199) {
                int tujuan_VALUE = posisi + perintah_data.부호두바이트(); cabang_Daftar.add(tujuan_VALUE); Collections.addAll(baris_masukan,"popl %eax","testl %eax, %eax",(perintah == 198 ? "je " : "jne ") + 표식 + "_b" + tujuan_VALUE);
            } else throw new Terjemahan_kesalahan("미지원 perintah: " + perintah);
        }
        if (!경계들.containsAll(cabang_Daftar)) throw new Terjemahan_kesalahan("perintah 경계가 아닌 곳으로 cabang");
        baris_masukan.add(".size " + 표식 + ", .-" + 표식); return String.join("\n",baris_masukan);
    }
    String X_86_konstanta(Kelas_data data, int INDEX) {
        if (data.상수종류[INDEX] == 3) return data.konstanta_data[INDEX].toString();
        if (data.상수종류[INDEX] == 8) return string_simbol(data.문자((Integer)data.konstanta_data[INDEX]));
        throw new Terjemahan_kesalahan("정수와 string_VALUE 상수만 dukung_VALUE");
    }
    String X_86_rakitan(String entri_p, List<String> 내보냄, String target) throws IOException {
        Map<String,String> mesin_tabel = new HashMap<>();
        for (String baris_masukan : Files.readAllLines(sumber_daya_jalur.resolve("_86_mesin_Functions.tsv"))) { String[] pasang_VALUE = baris_masukan.split("\t"); if (pasang_VALUE[0].equals(target)) mesin_tabel.put(pasang_VALUE[1] + pasang_VALUE[2],pasang_VALUE[3]); }
        int posisi_INDEX = entri_p.lastIndexOf('.'); if (posisi_INDEX < 0) throw new Terjemahan_kesalahan("entri_p Tugaskan_VALUE galat");
        String pemilik_VALUE = entri_p.substring(0,posisi_INDEX).replace('.','/'), metode_entri_nama = entri_p.substring(posisi_INDEX + 1); metode_Referensi entri_p_VALUE = null;
        for (String 서술 : Arrays.asList("()I","()V")) { metode_Referensi Referensi = new metode_Referensi(pemilik_VALUE,metode_entri_nama,서술); if (함수들.containsKey(Referensi)) { if (entri_p_VALUE != null) throw new Terjemahan_kesalahan("겹친 entri_p"); entri_p_VALUE = Referensi; } }
        if (entri_p_VALUE == null || (함수들.get(entri_p_VALUE).akses_entri & 0x100) != 0) throw new Terjemahan_kesalahan("entri_p_VALUE fungsi_VALUE format_VALUE galat");
        List<String> baris_masukan = new ArrayList<>(); baris_masukan.add(".code32");
        for (Kelas_data data : 클래스들.values()) {
            String Status_VALUE = simbol("state",data.Nama_2), inisialisasi = simbol("init",data.Nama_2);
            Collections.addAll(baris_masukan,".bss",".balign 4",Status_VALUE + ": .long 0",".text",inisialisasi + ":","cmpl $0, " + Status_VALUE,"jne " + inisialisasi + "_done","movl $1, " + Status_VALUE);
            metode_Referensi 초기화참조 = new metode_Referensi(data.Nama_2,"<clinit>","()V"); if (함수들.containsKey(초기화참조)) baris_masukan.add("call " + simbol("method",초기화참조.부분들()));
            Collections.addAll(baris_masukan,"movl $2, " + Status_VALUE,inisialisasi + "_done:","ret");
            for (anggota_data nilai_bidang : data.nilai_bidang) {
                byte[] konstanta_VALUE = nilai_bidang.nilai_atribut.get("ConstantValue"); String VALUE = konstanta_VALUE == null ? "0" : X_86_konstanta(data,new data_Pembaca(konstanta_VALUE).두바이트());
                Collections.addAll(baris_masukan,".data",".balign 4",simbol("field",data.Nama_2,nilai_bidang.Nama_2,nilai_bidang.서술) + ": .long " + VALUE);
            }
            for (anggota_data fungsi_VALUE : data.fungsi_VALUE) if (!fungsi_VALUE.Nama_2.equals("<init>")) baris_masukan.add(X_86_metode_isi(new metode_Referensi(data.Nama_2,fungsi_VALUE.Nama_2,fungsi_VALUE.서술),fungsi_VALUE,mesin_tabel,target));
        }
        Collections.addAll(baris_masukan,".text",".globl java_entry","java_entry:","call " + simbol("init",entri_p_VALUE.pemilik_VALUE),"call " + simbol("method",entri_p_VALUE.부분들()));
        if (entri_p_VALUE.서술.equals("()V")) baris_masukan.add("xorl %eax, %eax"); baris_masukan.add("ret");
        for (String Tugaskan_VALUE : 내보냄) {
            int pemisah_VALUE_d8ba4873 = Tugaskan_VALUE.indexOf('='); if (pemisah_VALUE_d8ba4873 < 1) throw new Terjemahan_kesalahan("내보내기 Tugaskan_VALUE galat");
            String eksternal_VALUE = Tugaskan_VALUE.substring(0,pemisah_VALUE_d8ba4873), fungsi_VALUE = Tugaskan_VALUE.substring(pemisah_VALUE_d8ba4873 + 1); int Divisi_KR = fungsi_VALUE.lastIndexOf('.');
            if (Divisi_KR < 0 || !eksternal_VALUE.matches("[A-Za-z_][A-Za-z0-9_]*")) throw new Terjemahan_kesalahan("내보내기 simbol galat");
            String Kelas_VALUE = fungsi_VALUE.substring(0,Divisi_KR).replace('.','/'), Nama_2 = fungsi_VALUE.substring(Divisi_KR + 1); metode_Referensi pilihan_VALUE = null;
            for (metode_Referensi Referensi : 함수들.keySet()) if (Referensi.pemilik_VALUE.equals(Kelas_VALUE) && Referensi.Nama_2.equals(Nama_2)) { if (pilihan_VALUE != null) throw new Terjemahan_kesalahan("겹친 내보내기 target"); pilihan_VALUE = Referensi; }
            if (pilihan_VALUE == null) throw new Terjemahan_kesalahan("내보낼 함수가 없음");
            Collections.addAll(baris_masukan,".text",".globl " + eksternal_VALUE,eksternal_VALUE + ":","call " + simbol("init",pilihan_VALUE.pemilik_VALUE),"jmp " + simbol("method",pilihan_VALUE.부분들()));
        }
        baris_masukan.add(".section .rodata");
        for (Map.Entry<String,String> entri_VALUE : 문자열들.entrySet()) {
            Collections.addAll(baris_masukan,".balign 4",entri_VALUE.getValue() + ":",".long " + entri_VALUE.getKey().length());
            List<String> 단위들 = new ArrayList<>(); for (char unit_VALUE : entri_VALUE.getKey().toCharArray()) 단위들.add(Integer.toString(unit_VALUE)); if (!단위들.isEmpty()) baris_masukan.add(".long " + String.join(",",단위들));
        }
        baris_masukan.add(".section .note.GNU-stack,\"\",@progbits"); return String.join("\n",baris_masukan) + "\n";
    }
    static void Jalankan_alat(List<String> perintah) throws Exception {
        if (new ProcessBuilder(perintah).inheritIO().start().waitFor() != 0) throw new Terjemahan_kesalahan("bangun_sumber galat: " + perintah.get(0));
    }
    static String data_string(String teks) { return "\"" + teks.replace("\\","\\\\").replace("\"","\\\"").replace("\n","\\n").replace("\r","\\r").replace("\t","\\t") + "\""; }
    static void X_86_Terjemahan(List<Path> 입력들, String target, String entri_p, List<String> 내보냄, Path keluaranTeks, Path sumber_daya_VALUE) throws Exception {
        Path 임시 = Files.createTempDirectory("jkoros-java-x86-"), Kelas_jalur = 임시.resolve("classes"); Files.createDirectory(Kelas_jalur);
        try {
            List<String> 자바명령 = new ArrayList<>(Arrays.asList("javac","-J-XX:-UsePerfData","--release","8","-encoding","UTF-8","-g:none","-proc:none","-implicit:none","-classpath",Kelas_jalur.toString(),"-sourcepath",Kelas_jalur.toString(),"-d",Kelas_jalur.toString()));
            List<Path> 바이트코드 = new ArrayList<>(); int sumber_COUNT = 0;
            for (Path 입력 : 입력들) {
                if (keluaranTeks.toAbsolutePath().normalize().equals(입력.toAbsolutePath().normalize())) throw new Terjemahan_kesalahan("keluaranTeks 파일과 입력이 같음");
                if (입력.toString().endsWith(".java")) { 자바명령.add(입력.toString()); sumber_COUNT++; }
                else if (입력.toString().endsWith(".class")) 바이트코드.add(입력);
                else throw new Terjemahan_kesalahan(".java 또는 .class만 dukung_VALUE");
            }
            if (sumber_COUNT > 0) Jalankan_alat(자바명령);
            try (java.util.stream.Stream<Path> jalur_Daftar = Files.walk(Kelas_jalur)) { jalur_Daftar.filter(jalur -> jalur.toString().endsWith(".class")).sorted().forEach(바이트코드::add); }
            기계어미리번역 CONVERT_VALUE = new 기계어미리번역(바이트코드,target.equals("user") ? "user" : "kernel",262144,sumber_daya_VALUE);
            String 조립 = CONVERT_VALUE.X_86_rakitan(entri_p,내보냄,target); Files.writeString(임시.resolve("program.s"),조립,StandardCharsets.UTF_8);
            Path alat_posisi = sumber_daya_VALUE.getParent();
            Jalankan_alat(Arrays.asList("as","--32","-o",임시.resolve("program.o").toString(),임시.resolve("program.s").toString()));
            Jalankan_alat(Arrays.asList("as","--32","-o",임시.resolve("runtime.o").toString(),alat_posisi.resolve("runtime_bahasa_umum_dukung.s").toString()));
            List<String> Sambung = new ArrayList<>(Arrays.asList("ld","-m","elf_i386"));
            if (target.equals("kernel")) Sambung.add("-r");
            else {
                Jalankan_alat(Arrays.asList("as","--32","-o",임시.resolve("start.o").toString(),alat_posisi.resolve(target.equals("user") ? "Mulai_pengguna_apl.s" : "리눅스시작.s").toString()));
                Collections.addAll(Sambung,"-e","_start",임시.resolve("start.o").toString());
                if (target.equals("user")) Collections.addAll(Sambung,"-T",alat_posisi.resolve("pengguna_link_Navigasi.ld").toString());
            }
            Collections.addAll(Sambung,"-o",임시.resolve("result").toString(),임시.resolve("program.o").toString(),임시.resolve("runtime.o").toString()); Jalankan_alat(Sambung);
            keluaranTeks = keluaranTeks.toAbsolutePath(); Files.createDirectories(keluaranTeks.getParent()); Path terbitkan_VALUE = Files.createTempFile(keluaranTeks.getParent(),".elf-",".tmp");
            try { Files.copy(임시.resolve("result"),terbitkan_VALUE,StandardCopyOption.REPLACE_EXISTING); Files.move(terbitkan_VALUE,keluaranTeks,StandardCopyOption.REPLACE_EXISTING); } finally { Files.deleteIfExists(terbitkan_VALUE); }
            Files.setPosixFilePermissions(keluaranTeks,java.nio.file.attribute.PosixFilePermissions.fromString(target.equals("linux") ? "rwxr-xr-x" : "rw-r--r--"));
            Files.writeString(Paths.get(keluaranTeks + ".s"),조립,StandardCharsets.UTF_8);
            List<String> simbol_data = new ArrayList<>(), data_sumber = new ArrayList<>();
            for (metode_Referensi Referensi : CONVERT_VALUE.함수들.keySet()) simbol_data.add(data_string(simbol("method",Referensi.부분들())) + ":" + data_string(Referensi.pemilik_VALUE + "." + Referensi.Nama_2 + Referensi.서술));
            for (Path 입력 : 입력들) {
                byte[] hash_file = MessageDigest.getInstance("SHA-256").digest(Files.readAllBytes(입력)); StringBuilder teks = new StringBuilder(); for (byte VALUE : hash_file) teks.append(String.format(Locale.ROOT,"%02x",VALUE & 255));
                data_sumber.add(data_string(입력.toAbsolutePath().toString()) + ":" + data_string(teks.toString()));
            }
            Files.writeString(Paths.get(keluaranTeks + ".json"),"{\"target\":" + data_string(target) + ",\"entry\":" + data_string(entri_p) + ",\"format\":\"ELF32 i386\",\"runtime_jvm\":false,\"symbols\":{" + String.join(",",simbol_data) + "},\"sources\":{" + String.join(",",data_sumber) + "}}\n",StandardCharsets.UTF_8);
        } finally {
            try (java.util.stream.Stream<Path> jalur_Daftar = Files.walk(임시)) { for (Path jalur : (Iterable<Path>)jalur_Daftar.sorted(Comparator.reverseOrder())::iterator) Files.deleteIfExists(jalur); }
        }
    }
    public static void main(String[] argumen) {
        try {
            String entri_p = null, target = "kernel", X_86_target = null; Path 출력경로 = null; int 낱말수 = 262144; boolean 범용표기 = false;
            List<String> 내보냄 = new ArrayList<>(); List<Path> jalur_Daftar = new ArrayList<>();
            for (int 순번 = 0; 순번 < argumen.length; 순번++) {
                String VALUE = argumen[순번];
                switch (VALUE) {
                    case "--target": X_86_target = argumen[++순번]; break;
                    case "--help": case "-h": System.out.println("사용법: --entry Kelas_VALUE.fungsi_VALUE -o keluaranTeks [--target linux|kernel|user] [--profile kernel|user] [--export simbol=Kelas_VALUE.fungsi_VALUE] 클래스파일 또는 Java원문"); return;
                    case "--entry": entri_p = argumen[++순번]; break;
                    case "--profile": target = argumen[++순번]; break;
                    case "--heap-words": 낱말수 = Integer.parseInt(argumen[++순번]); break;
                    case "--export": 내보냄.add(argumen[++순번]); break;
                    case "-o": 출력경로 = Paths.get(argumen[++순번]); break;
                    case "--ucn": 범용표기 = true; break;
                    default: if (VALUE.startsWith("-")) throw new Terjemahan_kesalahan("알 수 없는 옵션: " + VALUE); jalur_Daftar.add(Paths.get(VALUE));
                }
            }
            if (entri_p == null || 출력경로 == null || jalur_Daftar.isEmpty()) throw new Terjemahan_kesalahan("--entry, -o, Kelas_VALUE 파일이 필요합니다");
            Path sumber_daya_VALUE = Paths.get(System.getProperty("jkoros.compiler.resources"));
            if (X_86_target != null) {
                if (!Arrays.asList("linux","kernel","user").contains(X_86_target)) throw new Terjemahan_kesalahan("알 수 없는 Jalankan_perintah target");
                X_86_Terjemahan(jalur_Daftar,X_86_target,entri_p,내보냄,출력경로,sumber_daya_VALUE); return;
            }
            String kodeSumber = new 기계어미리번역(jalur_Daftar, target, 낱말수, sumber_daya_VALUE).buat(entri_p, 내보냄, 범용표기);
            출력경로 = 출력경로.toAbsolutePath(); Files.createDirectories(출력경로.getParent());
            Path 임시 = Files.createTempFile(출력경로.getParent(), ".aot-", ".tmp");
            try { Files.writeString(임시, kodeSumber, StandardCharsets.UTF_8); Files.move(임시, 출력경로, StandardCopyOption.REPLACE_EXISTING); }
            finally { Files.deleteIfExists(임시); }
        } catch (Exception galat) { System.err.println("bangun_sumber galat: " + galat.getMessage()); System.exit(1); }
    }
}
