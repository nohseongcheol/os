// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.security.MessageDigest;
import java.util.*;
import java.util.regex.*;

/** Java Kelas_VALUE 파일에서 독립 ARM64 커널용 C 원문을 만든다. hos JDK에서 실행한다. */
public final class 기계어미리번역 {
    static final class Terjemahan_ralat extends RuntimeException {
        Terjemahan_ralat(String 설명) { super(설명); }
    }
    static final class data_Pembaca {
        final byte[] data;
        int Kedudukan;
        data_Pembaca(byte[] 입력자료) { data = 입력자료; }
        byte[] Baca(int kepanjangan_VALUE) {
            if (kepanjangan_VALUE < 0 || kepanjangan_VALUE > data.length - Kedudukan) throw new Terjemahan_ralat("잘린 Kelas_VALUE 또는 Perintah data");
            byte[] ukuran = Arrays.copyOfRange(data, Kedudukan, Kedudukan + kepanjangan_VALUE); Kedudukan += kepanjangan_VALUE; return ukuran;
        }
        int 한바이트() { if (Kedudukan >= data.length) throw new Terjemahan_ralat("잘린 Perintah data"); return data[Kedudukan++] & 255; }
        int 두바이트() { return (한바이트() << 8) | 한바이트(); }
        int 네바이트() { return (두바이트() << 16) | 두바이트(); }
        int 부호한바이트() { return (byte) 한바이트(); }
        int 부호두바이트() { return (short) 두바이트(); }
    }
    static final class ahli_data {
        final int capai_pemasukan;
        final String Nama, 서술;
        final Map<String, byte[]> atribut_VALUE;
        ahli_data(int capai_VALUE, String nama_VALUE, String 서술값, Map<String, byte[]> atribut_data) {
            capai_pemasukan = capai_VALUE; Nama = nama_VALUE; 서술 = 서술값; atribut_VALUE = atribut_data;
        }
    }
    static final class kaedah_Rujukan implements Comparable<kaedah_Rujukan> {
        final String pemilik_VALUE, Nama, 서술;
        kaedah_Rujukan(String 소유값, String nama_VALUE, String 서술값) { pemilik_VALUE = 소유값; Nama = nama_VALUE; 서술 = 서술값; }
        String[] 부분들() { return new String[]{pemilik_VALUE, Nama, 서술}; }
        public int compareTo(kaedah_Rujukan rakan_VALUE) {
            int Perbandingan_VALUE = pemilik_VALUE.compareTo(rakan_VALUE.pemilik_VALUE);
            if (Perbandingan_VALUE == 0) Perbandingan_VALUE = Nama.compareTo(rakan_VALUE.Nama);
            return Perbandingan_VALUE == 0 ? 서술.compareTo(rakan_VALUE.서술) : Perbandingan_VALUE;
        }
        public boolean equals(Object rakan_VALUE) { return rakan_VALUE instanceof kaedah_Rujukan && compareTo((kaedah_Rujukan) rakan_VALUE) == 0; }
        public int hashCode() { return Objects.hash(pemilik_VALUE, Nama, 서술); }
    }
    static final class Kelas_data {
        final int[] 상수종류;
        final Object[] pemalar_data;
        final String Nama;
        final List<ahli_data> medan_VALUE, fungsi_VALUE;
        Kelas_data(Path LALUAN) throws IOException {
            data_Pembaca Pembaca_VALUE = new data_Pembaca(Files.readAllBytes(LALUAN));
            if (Pembaca_VALUE.네바이트() != 0xcafebabe) throw new Terjemahan_ralat("Java Kelas_VALUE 표식이 아님");
            Pembaca_VALUE.Baca(4);
            int item_COUNT = Pembaca_VALUE.두바이트(); 상수종류 = new int[item_COUNT]; pemalar_data = new Object[item_COUNT];
            for (int 순번 = 1; 순번 < item_COUNT; 순번++) {
                int 종류 = Pembaca_VALUE.한바이트(); 상수종류[순번] = 종류;
                switch (종류) {
                    case 1:
                        int kepanjangan_VALUE = Pembaca_VALUE.두바이트();
                        byte[] aksara_penimbal = Pembaca_VALUE.Baca(kepanjangan_VALUE), 길이붙인자료 = new byte[kepanjangan_VALUE + 2];
                        길이붙인자료[0] = (byte)(kepanjangan_VALUE >> 8); 길이붙인자료[1] = (byte)kepanjangan_VALUE;
                        System.arraycopy(aksara_penimbal, 0, 길이붙인자료, 2, kepanjangan_VALUE);
                        pemalar_data[순번] = new DataInputStream(new ByteArrayInputStream(길이붙인자료)).readUTF(); break;
                    case 3: pemalar_data[순번] = Pembaca_VALUE.네바이트(); break;
                    case 4: Pembaca_VALUE.Baca(4); break;
                    case 5: case 6: Pembaca_VALUE.Baca(8); 순번++; break;
                    case 7: case 8: case 16: pemalar_data[순번] = Pembaca_VALUE.두바이트(); break;
                    case 9: case 10: case 11: case 12: case 18:
                        pemalar_data[순번] = new int[]{Pembaca_VALUE.두바이트(), Pembaca_VALUE.두바이트()}; break;
                    case 15: pemalar_data[순번] = new int[]{Pembaca_VALUE.한바이트(), Pembaca_VALUE.두바이트()}; break;
                    default: throw new Terjemahan_ralat("지원하지 않는 pemalar_VALUE 종류: " + 종류);
                }
            }
            Pembaca_VALUE.두바이트(); Nama = nama_kelas(Pembaca_VALUE.두바이트());
            if (!nama_kelas(Pembaca_VALUE.두바이트()).equals("java/lang/Object") || Pembaca_VALUE.두바이트() != 0)
                throw new Terjemahan_ralat(Nama + ": 상속 및 인터페이스 미지원");
            medan_VALUE = 멤버읽기(Pembaca_VALUE); fungsi_VALUE = 멤버읽기(Pembaca_VALUE); 속성읽기(Pembaca_VALUE);
            if (Pembaca_VALUE.Kedudukan != Pembaca_VALUE.data.length) throw new Terjemahan_ralat("Kelas_VALUE 뒤에 남은 data");
        }
        String 문자(int INDEX) {
            if (INDEX < 1 || INDEX >= 상수종류.length || 상수종류[INDEX] != 1) throw new Terjemahan_ralat("문자 pemalar_VALUE INDEX RALAT");
            return (String) pemalar_data[INDEX];
        }
        String nama_kelas(int INDEX) {
            if (INDEX < 1 || INDEX >= 상수종류.length || 상수종류[INDEX] != 7) throw new Terjemahan_ralat("Kelas_VALUE Rujukan RALAT");
            return 문자((Integer)pemalar_data[INDEX]);
        }
        kaedah_Rujukan Rujukan(int INDEX) {
            if (INDEX < 1 || INDEX >= 상수종류.length || 상수종류[INDEX] < 9 || 상수종류[INDEX] > 11) throw new Terjemahan_ralat("멤버 Rujukan RALAT");
            int[] berpasangan_VALUE = (int[])pemalar_data[INDEX], nama_berpasangan = (int[])pemalar_data[berpasangan_VALUE[1]];
            return new kaedah_Rujukan(nama_kelas(berpasangan_VALUE[0]), 문자(nama_berpasangan[0]), 문자(nama_berpasangan[1]));
        }
        Map<String, byte[]> 속성읽기(data_Pembaca Pembaca_VALUE) {
            Map<String, byte[]> ukuran = new LinkedHashMap<>();
            int item_COUNT = Pembaca_VALUE.두바이트();
            for (int 순번 = 0; 순번 < item_COUNT; 순번++) {
                String atribut_nama = 문자(Pembaca_VALUE.두바이트()); byte[] VALUE = Pembaca_VALUE.Baca(Pembaca_VALUE.네바이트());
                if (ukuran.put(atribut_nama, VALUE) != null) throw new Terjemahan_ralat("겹친 atribut_VALUE: " + atribut_nama);
            }
            return ukuran;
        }
        List<ahli_data> 멤버읽기(data_Pembaca Pembaca_VALUE) {
            List<ahli_data> ukuran = new ArrayList<>(); int item_COUNT = Pembaca_VALUE.두바이트();
            for (int 순번 = 0; 순번 < item_COUNT; 순번++) {
                int capai_pemasukan = Pembaca_VALUE.두바이트(); String kaedah_pemasukan_nama = 문자(Pembaca_VALUE.두바이트()), 서술 = 문자(Pembaca_VALUE.두바이트());
                ukuran.add(new ahli_data(capai_pemasukan, kaedah_pemasukan_nama, 서술, 속성읽기(Pembaca_VALUE)));
            }
            return ukuran;
        }
    }
    static final class 함수형식 {
        final List<String> 인수 = new ArrayList<>();
        final String kembalikan_ukuran;
        함수형식(String 서술) {
            if (!서술.startsWith("(")) throw new Terjemahan_ralat("fungsi_VALUE 서술 RALAT: " + 서술);
            int 끝 = 서술.indexOf(')'); if (끝 < 0) throw new Terjemahan_ralat("fungsi_VALUE 서술 RALAT: " + 서술);
            인수.addAll(형식읽기(서술.substring(1, 끝)));
            List<String> 반환들 = 형식읽기(서술.substring(끝 + 1));
            if (인수.contains("V") || 반환들.size() != 1) throw new Terjemahan_ralat("fungsi_VALUE 서술 RALAT: " + 서술);
            kembalikan_ukuran = 반환들.get(0);
        }
    }
    static List<String> 형식읽기(String 서술) {
        List<String> ukuran = new ArrayList<>();
        String[] 허용형식 = {"Ljava/lang/String;", "[I", "I", "Z", "B", "C", "S", "V"};
        for (int Kedudukan = 0; Kedudukan < 서술.length();) {
            String pilihan_VALUE = null;
            for (String format_VALUE : 허용형식) if (서술.startsWith(format_VALUE, Kedudukan)) { pilihan_VALUE = format_VALUE; break; }
            if (pilihan_VALUE == null) throw new Terjemahan_ralat("지원하지 않는 jenis_data: " + 서술);
            ukuran.add(pilihan_VALUE); Kedudukan += pilihan_VALUE.length();
        }
        return ukuran;
    }
    static String simbol(String 종류, String... 부분들) {
        try {
            byte[] cincangan_fail = MessageDigest.getInstance("SHA-256").digest(String.join("\0", 부분들).getBytes(StandardCharsets.UTF_8));
            StringBuilder Teks = new StringBuilder("j_" + 종류 + "_");
            for (int 순번 = 0; 순번 < 12; 순번++) Teks.append(String.format(Locale.ROOT, "%02x", cincangan_fail[순번] & 255));
            return Teks.toString();
        } catch (Exception RALAT) { throw new Terjemahan_ralat(RALAT.toString()); }
    }
    final Map<String, Kelas_data> 클래스들 = new TreeMap<>();
    final Map<kaedah_Rujukan, ahli_data> 함수들 = new TreeMap<>(), 필드들 = new TreeMap<>();
    final Map<String, String> 문자열들 = new LinkedHashMap<>(), mesin_Fungsi_Azure_c3a8e64a = new LinkedHashMap<>();
    final String 실행대상, mesin_Kelas;
    final int timbunan_Kiraan_Kata;
    final Path sumber_laluan;
    기계어미리번역(List<Path> laluan_Senarai, String sasaran, int 낱말수, Path sumber_VALUE) throws IOException {
        if ((!sasaran.equals("kernel") && !sasaran.equals("user")) || 낱말수 < 1024 || 낱말수 > 1048576) throw new Terjemahan_ralat("laksanakan_perintah sasaran 또는 Memori_VALUE e_mel_rantau Saiz RALAT");
        실행대상 = sasaran; timbunan_Kiraan_Kata = 낱말수; sumber_laluan = sumber_VALUE;
        // 이 이름도 국가별 sumber_pepohon jana 시 해당 언어로 옮긴다.
        mesin_Kelas = sasaran.equals("kernel") ? "Papan" : "ruang_pengguna";
        for (String baris : Files.readAllLines(sumber_VALUE.resolve("mesin_Fungsi_Azure.tsv"), StandardCharsets.UTF_8)) {
            String[] 부분들 = baris.split("\t", -1);
            if (부분들.length != 4) throw new Terjemahan_ralat("mesin fungsi_VALUE data RALAT");
            if (부분들[0].equals(sasaran)) mesin_Fungsi_Azure_c3a8e64a.put(부분들[1] + 부분들[2], 부분들[3]);
        }
        for (Path LALUAN : laluan_Senarai) {
            Kelas_data data = new Kelas_data(LALUAN);
            if (클래스들.put(data.Nama, data) != null) throw new Terjemahan_ralat("중복 Kelas_VALUE: " + data.Nama);
            for (ahli_data medan_VALUE : data.medan_VALUE) {
                if ((medan_VALUE.capai_pemasukan & 8) == 0 || 형식읽기(medan_VALUE.서술).equals(Collections.singletonList("V"))) throw new Terjemahan_ralat("statik_VALUE 필드만 Sokongan_VALUE");
                if (필드들.put(new kaedah_Rujukan(data.Nama, medan_VALUE.Nama, medan_VALUE.서술), medan_VALUE) != null) throw new Terjemahan_ralat("중복 medan_VALUE");
            }
            for (ahli_data fungsi_VALUE : data.fungsi_VALUE) {
                if (fungsi_VALUE.Nama.equals("<init>")) continue;
                if ((fungsi_VALUE.capai_pemasukan & 8) == 0 || (fungsi_VALUE.capai_pemasukan & (0x20 | 0x400)) != 0) throw new Terjemahan_ralat("statik_VALUE 비동기화 함수만 Sokongan_VALUE");
                new 함수형식(fungsi_VALUE.서술);
                if (함수들.put(new kaedah_Rujukan(data.Nama, fungsi_VALUE.Nama, fungsi_VALUE.서술), fungsi_VALUE) != null) throw new Terjemahan_ralat("중복 fungsi_VALUE");
            }
        }
    }
    String rentetan_simbol(String Teks) { return 문자열들.computeIfAbsent(Teks, VALUE -> "j_text_" + 문자열들.size()); }
    String pemalar_ungkapan(Kelas_data data, int INDEX) {
        if (INDEX < 1 || INDEX >= data.상수종류.length) throw new Terjemahan_ralat("pemalar_VALUE INDEX klip RALAT");
        if (data.상수종류[INDEX] == 3) return "(word)(uint32_t)(" + data.pemalar_data[INDEX] + ")";
        if (data.상수종류[INDEX] == 8) return "(word)" + rentetan_simbol(data.문자((Integer)data.pemalar_data[INDEX]));
        throw new Terjemahan_ralat("정수와 rentetan_VALUE 상수만 Sokongan_VALUE");
    }
    String kaedah_prototaip(kaedah_Rujukan Rujukan) {
        List<String> 인수들 = new ArrayList<>(); int item_COUNT = new 함수형식(Rujukan.서술).인수.size();
        for (int 순번 = 0; 순번 < item_COUNT; 순번++) 인수들.add("word a" + 순번);
        return "static word " + simbol("method", Rujukan.부분들()) + "(" + (item_COUNT == 0 ? "void" : String.join(", ", 인수들)) + ")";
    }
    void cek_setempat(int INDEX, int setempat_pemboleh_ubah_COUNT) { if (INDEX < 0 || INDEX >= setempat_pemboleh_ubah_COUNT) throw new Terjemahan_ralat("setempat_Skop pemboleh_ubah_VALUE INDEX klip RALAT"); }
    void 분기넣기(List<String> 출력, Set<Integer> cabang_Senarai, int Kedudukan, int 이동량, String syarat) {
        int destinasi_VALUE = Kedudukan + 이동량; cabang_Senarai.add(destinasi_VALUE);
        출력.add((syarat == null ? "" : "if (" + syarat + ") ") + "goto b" + destinasi_VALUE + ";");
    }
    String kaedah_isi(kaedah_Rujukan fungsi_VALUE, ahli_data data) {
        byte[] isi_data = data.atribut_VALUE.get("Code"); if (isi_data == null) throw new Terjemahan_ralat("fungsi_VALUE 몸체가 없음: " + fungsi_VALUE.Nama);
        data_Pembaca Pembaca_VALUE = new data_Pembaca(isi_data); int 쌓임깊이 = Pembaca_VALUE.두바이트(), setempat_pemboleh_ubah_COUNT = Pembaca_VALUE.두바이트();
        data_Pembaca perintah_data = new data_Pembaca(Pembaca_VALUE.Baca(Pembaca_VALUE.네바이트()));
        if (Pembaca_VALUE.두바이트() != 0) throw new Terjemahan_ralat("try/catch/finally 미지원");
        함수형식 format_VALUE = new 함수형식(fungsi_VALUE.서술); if (setempat_pemboleh_ubah_COUNT < format_VALUE.인수.size()) throw new Terjemahan_ralat("매개변수보다 적은 setempat_Skop pemboleh_ubah_VALUE");
        Kelas_data Kelas_VALUE = 클래스들.get(fungsi_VALUE.pemilik_VALUE);
        List<String> 출력 = new ArrayList<>(); 출력.add(kaedah_prototaip(fungsi_VALUE) + " {");
        출력.add("word s[" + Math.max(쌓임깊이, 1) + "], l[" + Math.max(setempat_pemboleh_ubah_COUNT, 1) + "] = {0}, a,b,c,d; size_t sp = 0;");
        for (int 순번 = 0; 순번 < format_VALUE.인수.size(); 순번++) 출력.add("l[" + 순번 + "] = a" + 순번 + ";");
        Set<Integer> 경계들 = new HashSet<>(), cabang_Senarai = new HashSet<>();
        String[] 비교들 = {"==", "!=", "<", ">=", ">", "<=", "==", "!="};
        while (perintah_data.Kedudukan < perintah_data.data.length) {
            int Kedudukan = perintah_data.Kedudukan, Perintah = perintah_data.한바이트(); 경계들.add(Kedudukan); 출력.add("b" + Kedudukan + ":;");
            if (Perintah == 0) continue;
            if (Perintah == 1) 출력.add("PUSH(0);");
            else if (Perintah >= 2 && Perintah <= 8) 출력.add("PUSH((uint32_t)(" + (Perintah - 3) + "));");
            else if (Perintah == 16 || Perintah == 17) 출력.add("PUSH((uint32_t)(" + (Perintah == 16 ? perintah_data.부호한바이트() : perintah_data.부호두바이트()) + "));");
            else if (Perintah == 18 || Perintah == 19) 출력.add("PUSH(" + pemalar_ungkapan(Kelas_VALUE, Perintah == 18 ? perintah_data.한바이트() : perintah_data.두바이트()) + ");");
            else if (Perintah == 21 || Perintah == 25 || (Perintah >= 26 && Perintah <= 29) || (Perintah >= 42 && Perintah <= 45)) {
                int INDEX = Perintah == 21 || Perintah == 25 ? perintah_data.한바이트() : Perintah - (Perintah <= 29 ? 26 : 42);
                cek_setempat(INDEX, setempat_pemboleh_ubah_COUNT); 출력.add("PUSH(l[" + INDEX + "]);");
            } else if (Perintah == 54 || Perintah == 58 || (Perintah >= 59 && Perintah <= 62) || (Perintah >= 75 && Perintah <= 78)) {
                int INDEX = Perintah == 54 || Perintah == 58 ? perintah_data.한바이트() : Perintah - (Perintah <= 62 ? 59 : 75);
                cek_setempat(INDEX, setempat_pemboleh_ubah_COUNT); 출력.add("l[" + INDEX + "] = POP();");
            } else if (Perintah == 46) 출력.add("b = POP(); a = POP(); PUSH(*checked(a,(int32_t)b));");
            else if (Perintah == 79) 출력.add("c = POP(); b = POP(); a = POP(); *checked(a,(int32_t)b) = (uint32_t)c;");
            else if (Perintah == 87 || Perintah == 88) 출력.add(Perintah == 87 ? "(void)POP();" : "(void)POP(); (void)POP();");
            else if (Perintah >= 89 && Perintah <= 95) {
                int[] 개수들 = {1,2,3,2,3,4,2}; String[] tertib_Senarai = {"aa","aba","acba","baba","bacba","badcba","ab"};
                for (int 순번 = 0; 순번 < 개수들[Perintah - 89]; 순번++) 출력.add("abcd".charAt(순번) + " = POP();");
                for (char VALUE : tertib_Senarai[Perintah - 89].toCharArray()) 출력.add("PUSH(" + VALUE + ");");
            } else if (Perintah == 96 || Perintah == 100 || Perintah == 104 || Perintah == 126 || Perintah == 128 || Perintah == 130) {
                String operasi_VALUE = Perintah == 96 ? "+" : Perintah == 100 ? "-" : Perintah == 104 ? "*" : Perintah == 126 ? "&" : Perintah == 128 ? "|" : "^";
                출력.add("b = POP(); a = POP(); PUSH((uint32_t)a " + operasi_VALUE + " (uint32_t)b);");
            } else if (Perintah == 108 || Perintah == 112) 출력.add("b = POP(); a = POP(); PUSH(divide(a,b," + (Perintah == 112 ? 1 : 0) + "));");
            else if (Perintah == 116) 출력.add("a = POP(); PUSH(0u-(uint32_t)a);");
            else if (Perintah == 120 || Perintah == 122 || Perintah == 124) {
                출력.add("b = POP(); a = POP();"); 출력.add("PUSH(" + (Perintah == 122 ? "arithmetic_shift(a,b)" : "(uint32_t)a " + (Perintah == 120 ? "<<" : ">>") + " ((uint32_t)b & 31)") + ");");
            } else if (Perintah == 132) {
                int INDEX = perintah_data.한바이트(), tokokan_amaun = perintah_data.부호한바이트(); cek_setempat(INDEX, setempat_pemboleh_ubah_COUNT);
                출력.add("l[" + INDEX + "] = (uint32_t)l[" + INDEX + "] + (uint32_t)(" + tokokan_amaun + ");");
            } else if (Perintah >= 145 && Perintah <= 147) 출력.add("a = POP(); PUSH((uint32_t)(" + (Perintah == 145 ? "int8_t" : Perintah == 146 ? "uint16_t" : "int16_t") + ")a);");
            else if (Perintah >= 153 && Perintah <= 158) {
                출력.add("a = POP();"); 분기넣기(출력, cabang_Senarai, Kedudukan, perintah_data.부호두바이트(), "(int32_t)a " + 비교들[Perintah - 153] + " 0");
            } else if (Perintah >= 159 && Perintah <= 166) {
                출력.add("b = POP(); a = POP();"); 분기넣기(출력, cabang_Senarai, Kedudukan, perintah_data.부호두바이트(), Perintah >= 165 ? "a " + 비교들[Perintah - 159] + " b" : "(int32_t)a " + 비교들[Perintah - 159] + " (int32_t)b");
            } else if (Perintah == 167 || Perintah == 200) 분기넣기(출력, cabang_Senarai, Kedudukan, Perintah == 167 ? perintah_data.부호두바이트() : perintah_data.네바이트(), null);
            else if (Perintah == 170 || Perintah == 171) {
                while (perintah_data.Kedudukan % 4 != 0) perintah_data.한바이트();
                int nilai_lalai = perintah_data.네바이트(); 출력.add("a = POP();");
                if (Perintah == 170) {
                    int 아래 = perintah_data.네바이트(), 위 = perintah_data.네바이트(); long item_COUNT = (long)위 - 아래 + 1;
                    if (item_COUNT < 1 || item_COUNT > (perintah_data.data.length - perintah_data.Kedudukan) / 4) throw new Terjemahan_ralat("switch klip RALAT");
                    for (long VALUE = 아래; VALUE <= 위; VALUE++) 분기넣기(출력, cabang_Senarai, Kedudukan, perintah_data.네바이트(), "(int32_t)a == (" + VALUE + ")");
                } else {
                    int item_COUNT = perintah_data.네바이트(), hadapan_data = 0;
                    if (item_COUNT < 0 || item_COUNT > (perintah_data.data.length - perintah_data.Kedudukan) / 8) throw new Terjemahan_ralat("switch Saiz RALAT");
                    for (int 순번 = 0; 순번 < item_COUNT; 순번++) {
                        int VALUE = perintah_data.네바이트(); if (순번 > 0 && VALUE <= hadapan_data) throw new Terjemahan_ralat("switch tertib_VALUE RALAT"); hadapan_data = VALUE;
                        분기넣기(출력, cabang_Senarai, Kedudukan, perintah_data.네바이트(), "(int32_t)a == (" + VALUE + ")");
                    }
                }
                분기넣기(출력, cabang_Senarai, Kedudukan, nilai_lalai, null);
            } else if (Perintah == 172 || Perintah == 176 || Perintah == 177) 출력.add("return " + (Perintah == 177 ? "0" : "POP()") + ";");
            else if (Perintah == 178 || Perintah == 179) {
                kaedah_Rujukan Rujukan = Kelas_VALUE.Rujukan(perintah_data.두바이트()); if (!필드들.containsKey(Rujukan)) throw new Terjemahan_ralat("알 수 없는 medan_VALUE");
                출력.add(simbol("init", Rujukan.pemilik_VALUE) + "();"); String medan_VALUE = simbol("field", Rujukan.부분들());
                출력.add(Perintah == 178 ? "PUSH(" + medan_VALUE + ");" : medan_VALUE + " = POP();");
            } else if (Perintah == 184) {
                kaedah_Rujukan Rujukan = Kelas_VALUE.Rujukan(perintah_data.두바이트()); if (!함수들.containsKey(Rujukan)) throw new Terjemahan_ralat("알 수 없는 fungsi_VALUE");
                함수형식 호출형식 = new 함수형식(Rujukan.서술); int item_COUNT = 호출형식.인수.size();
                출력.add(simbol("init", Rujukan.pemilik_VALUE) + "();"); 출력.add("if(sp < " + item_COUNT + ") kernel_panic(\"call stack underflow\"); sp -= " + item_COUNT + ";");
                List<String> 호출인수 = new ArrayList<>(); for (int 순번 = 0; 순번 < item_COUNT; 순번++) 호출인수.add("s[sp + " + 순번 + "]");
                출력.add("a = " + simbol("method", Rujukan.부분들()) + "(" + String.join(",", 호출인수) + ");");
                if (!호출형식.kembalikan_ukuran.equals("V")) 출력.add("PUSH(a);");
            } else if (Perintah == 182) {
                kaedah_Rujukan Rujukan = Kelas_VALUE.Rujukan(perintah_data.두바이트());
                if (Rujukan.equals(new kaedah_Rujukan("java/lang/String", "length", "()I"))) 출력.add("a = POP(); PUSH(length(a));");
                else if (Rujukan.equals(new kaedah_Rujukan("java/lang/String", "charAt", "(I)C"))) 출력.add("b = POP(); a = POP(); PUSH(*checked(a,(int32_t)b));");
                else throw new Terjemahan_ralat("가상 fungsi_VALUE 호출 미지원");
            } else if (Perintah == 188) {
                if (perintah_data.한바이트() != 10) throw new Terjemahan_ralat("new int[]만 Sokongan_VALUE"); 출력.add("a = POP(); PUSH(new_array((int32_t)a));");
            } else if (Perintah == 190) 출력.add("a = POP(); PUSH(length(a));");
            else if (Perintah == 196) {
                int sambungan_VALUE = perintah_data.한바이트(), INDEX = perintah_data.두바이트(); cek_setempat(INDEX, setempat_pemboleh_ubah_COUNT);
                if (sambungan_VALUE == 21 || sambungan_VALUE == 25) 출력.add("PUSH(l[" + INDEX + "]);");
                else if (sambungan_VALUE == 54 || sambungan_VALUE == 58) 출력.add("l[" + INDEX + "] = POP();");
                else if (sambungan_VALUE == 132) 출력.add("l[" + INDEX + "] = (uint32_t)l[" + INDEX + "] + (uint32_t)(" + perintah_data.부호두바이트() + ");");
                else throw new Terjemahan_ralat("미지원 wide Perintah");
            } else if (Perintah == 198 || Perintah == 199) {
                출력.add("a = POP();"); 분기넣기(출력, cabang_Senarai, Kedudukan, perintah_data.부호두바이트(), "a " + (Perintah == 198 ? "==" : "!=") + " 0");
            } else throw new Terjemahan_ralat(fungsi_VALUE.pemilik_VALUE + "." + fungsi_VALUE.Nama + ", bait_VALUE " + Kedudukan + ": 미지원 Perintah " + Perintah);
        }
        if (!경계들.containsAll(cabang_Senarai)) throw new Terjemahan_ralat("Perintah 경계가 아닌 곳으로 cabang");
        출력.add("kernel_panic(\"method fell through\"); }"); return String.join("\n", 출력);
    }
    String Eksport_kaedah(String paut_simbol, String sasaran, boolean 진입점여부) {
        int jawatan_INDEX = sasaran.lastIndexOf('.'); if (jawatan_INDEX < 0 || !paut_simbol.matches("[A-Za-z_][A-Za-z0-9_]*")) throw new Terjemahan_ralat("내보내기 Tugaskan_VALUE RALAT");
        String pemilik_VALUE = sasaran.substring(0, jawatan_INDEX).replace('.', '/'), Nama = sasaran.substring(jawatan_INDEX + 1); kaedah_Rujukan pilihan_VALUE = null;
        for (kaedah_Rujukan Rujukan : 함수들.keySet()) if (Rujukan.pemilik_VALUE.equals(pemilik_VALUE) && Rujukan.Nama.equals(Nama)) {
            if (pilihan_VALUE != null) throw new Terjemahan_ralat("겹친 내보내기 sasaran"); pilihan_VALUE = Rujukan;
        }
        if (pilihan_VALUE == null || (함수들.get(pilihan_VALUE).capai_pemasukan & 0x100) != 0) throw new Terjemahan_ralat("내보낼 함수가 없음 또는 native fungsi_VALUE");
        함수형식 format_VALUE = new 함수형식(pilihan_VALUE.서술);
        if ((진입점여부 && !format_VALUE.인수.isEmpty()) || !Arrays.asList("V", "I").contains(format_VALUE.kembalikan_ukuran)) throw new Terjemahan_ralat("titik_permulaan_VALUE 또는 C 경계 format_VALUE RALAT");
        List<String> 인수들 = new ArrayList<>(), 호출인수 = new ArrayList<>();
        for (int 순번 = 0; 순번 < format_VALUE.인수.size(); 순번++) {
            if (!format_VALUE.인수.get(순번).equals("I")) throw new Terjemahan_ralat("C 경계는 int 인수만 Sokongan_VALUE");
            인수들.add("int32_t a" + 순번); 호출인수.add("(uint32_t)a" + 순번);
        }
        return (format_VALUE.kembalikan_ukuran.equals("V") ? "void " : "int32_t ") + paut_simbol + "(" + (인수들.isEmpty() ? "void" : String.join(",", 인수들)) + ") { " + simbol("init", pilihan_VALUE.pemilik_VALUE) + "(); " + (format_VALUE.kembalikan_ukuran.equals("V") ? "" : "return (int32_t)") + simbol("method", pilihan_VALUE.부분들()) + "(" + String.join(",", 호출인수) + "); }";
    }
    String jana(String titik_permulaan, List<String> 내보내기목록, boolean 범용표기) throws IOException {
        List<String> 선언들 = new ArrayList<>(), 몸체들 = new ArrayList<>(), 필드선언들 = new ArrayList<>();
        for (Map.Entry<kaedah_Rujukan, ahli_data> pemasukan_VALUE : 함수들.entrySet()) {
            kaedah_Rujukan Rujukan = pemasukan_VALUE.getKey(); ahli_data data = pemasukan_VALUE.getValue(); 선언들.add(kaedah_prototaip(Rujukan) + ";");
            if ((data.capai_pemasukan & 0x100) != 0) {
                String Sambung = mesin_Fungsi_Azure_c3a8e64a.get(Rujukan.Nama + Rujukan.서술);
                if (!Rujukan.pemilik_VALUE.equals(mesin_Kelas) || Sambung == null) throw new Terjemahan_ralat("허용되지 않은 native fungsi_VALUE: " + Rujukan.Nama);
                int item_COUNT = new 함수형식(Rujukan.서술).인수.size(); List<String> 인수들 = new ArrayList<>();
                for (int 순번 = 0; 순번 < item_COUNT; 순번++) 인수들.add("a" + 순번);
                선언들.add("extern word " + Sambung + "(" + (item_COUNT == 0 ? "void" : String.join(",", Collections.nCopies(item_COUNT, "word"))) + ");");
                몸체들.add(kaedah_prototaip(Rujukan) + " { return " + Sambung + "(" + String.join(",", 인수들) + "); }");
            } else 몸체들.add(kaedah_isi(Rujukan, data));
        }
        for (Map.Entry<kaedah_Rujukan, ahli_data> pemasukan_VALUE : 필드들.entrySet()) {
            kaedah_Rujukan Rujukan = pemasukan_VALUE.getKey(); byte[] pemalar_VALUE = pemasukan_VALUE.getValue().atribut_VALUE.get("ConstantValue");
            String VALUE = pemalar_VALUE == null ? "0" : pemalar_ungkapan(클래스들.get(Rujukan.pemilik_VALUE), new data_Pembaca(pemalar_VALUE).두바이트());
            필드선언들.add("static word " + simbol("field", Rujukan.부분들()) + " = " + VALUE + ";");
        }
        for (String Nama : 클래스들.keySet()) {
            String mengasal = simbol("init", Nama), status_VALUE = simbol("state", Nama);
            선언들.add("static void " + mengasal + "(void);"); 필드선언들.add("static unsigned " + status_VALUE + ";");
            kaedah_Rujukan Rujukan = new kaedah_Rujukan(Nama, "<clinit>", "()V");
            몸체들.add("static void " + mengasal + "(void) { if(" + status_VALUE + ") return; " + status_VALUE + " = 1; " + (함수들.containsKey(Rujukan) ? simbol("method", Rujukan.부분들()) + "(); " : "") + status_VALUE + " = 2; }");
        }
        몸체들.add(Eksport_kaedah("java_entry", titik_permulaan, true)); Set<String> 공개이름 = new HashSet<>();
        for (String Tugaskan_VALUE : 내보내기목록) {
            int jawatan_INDEX = Tugaskan_VALUE.indexOf('='); if (jawatan_INDEX < 1) throw new Terjemahan_ralat("내보내기 Tugaskan_VALUE RALAT");
            String Nama = Tugaskan_VALUE.substring(0, jawatan_INDEX); 공개이름.add(Nama); 몸체들.add(Eksport_kaedah(Nama, Tugaskan_VALUE.substring(jawatan_INDEX + 1), false));
        }
        List<String> 문자열선언들 = new ArrayList<>();
        for (Map.Entry<String, String> pemasukan_VALUE : 문자열들.entrySet()) {
            String Teks = pemasukan_VALUE.getKey(); StringBuilder ARRAY_VALUE = new StringBuilder("static const word " + pemasukan_VALUE.getValue() + "[] = {" + Teks.length());
            for (int 순번 = 0; 순번 < Teks.length(); 순번++) ARRAY_VALUE.append(", ").append((int)Teks.charAt(순번));
            문자열선언들.add(ARRAY_VALUE.append("};").toString());
        }
        String Sokongan_VALUE = Files.readString(sumber_laluan.resolve("masa_jalan_bahasa_biasa_Sokongan.c.txt"), StandardCharsets.UTF_8).replace("262144", Integer.toString(timbunan_Kiraan_Kata));
        return 기계원문한국어화(Sokongan_VALUE + String.join("\n", 문자열선언들) + "\n" + String.join("\n", 선언들) + "\n" + String.join("\n", 필드선언들) + "\n" + String.join("\n", 몸체들) + "\n", 공개이름, 범용표기);
    }
    String 기계원문한국어화(String SUMBER, Set<String> 공개이름, boolean 범용표기) throws IOException {
        Map<String, String> nama_jadual = new HashMap<>();
        for (String baris : Files.readAllLines(sumber_laluan.resolve("생성이름.tsv"), StandardCharsets.UTF_8)) {
            String[] berpasangan_VALUE = baris.split("\t"); nama_jadual.put(berpasangan_VALUE[0], berpasangan_VALUE[1]);
        }
        Pattern cebis_ungkapan = Pattern.compile("//[^\\n]*|/\\*[\\s\\S]*?\\*/|\"(?:\\\\.|[^\"\\\\])*\"|'(?:\\\\.|[^'\\\\])*'|\\b[A-Za-z_]\\w*\\b");
        Matcher 찾개 = cebis_ungkapan.matcher(SUMBER); StringBuffer ukuran = new StringBuffer();
        while (찾개.find()) {
            String Nama = 찾개.group(), 새이름 = Nama;
            if (!Nama.startsWith("//") && !Nama.startsWith("/*") && !Nama.startsWith("\"") && !Nama.startsWith("'") && !공개이름.contains(Nama)) {
                새이름 = nama_jadual.getOrDefault(Nama, Nama);
                if (Nama.matches("a[0-9]+")) 새이름 = "인수" + Nama.substring(1);
                if (Nama.matches("b[0-9]+")) 새이름 = "cabang" + Nama.substring(1);
                if (범용표기) {
                    StringBuilder notasi_VALUE = new StringBuilder();
                    for (char aksara_VALUE : 새이름.toCharArray()) notasi_VALUE.append(aksara_VALUE < 128 ? Character.toString(aksara_VALUE) : String.format(Locale.ROOT, "\\u%04x", (int)aksara_VALUE));
                    새이름 = notasi_VALUE.toString();
                }
            }
            찾개.appendReplacement(ukuran, Matcher.quoteReplacement(새이름));
        }
        찾개.appendTail(ukuran); return ukuran.toString();
    }
    String X_86_kaedah_isi(kaedah_Rujukan fungsi_VALUE, ahli_data data, Map<String,String> mesin_jadual, String sasaran) {
        String penanda_VALUE = simbol("method", fungsi_VALUE.부분들());
        List<String> baris = new ArrayList<>();
        if ((data.capai_pemasukan & 0x100) != 0) {
            String Sambung = mesin_jadual.get(fungsi_VALUE.Nama + fungsi_VALUE.서술);
            if (!fungsi_VALUE.pemilik_VALUE.equals(sasaran.equals("kernel") ? "peranti_VALUE" : "ruang_pengguna") || Sambung == null) throw new Terjemahan_ralat("허용되지 않은 native fungsi_VALUE");
            return ".text\n" + penanda_VALUE + ":\njmp " + Sambung;
        }
        byte[] teks_jasad = data.atribut_VALUE.get("Code"); if (teks_jasad == null) throw new Terjemahan_ralat("fungsi_VALUE 몸체가 없음");
        data_Pembaca Pembaca_VALUE = new data_Pembaca(teks_jasad); Pembaca_VALUE.두바이트(); int setempat_COUNT = Pembaca_VALUE.두바이트();
        data_Pembaca perintah_data = new data_Pembaca(Pembaca_VALUE.Baca(Pembaca_VALUE.네바이트()));
        if (Pembaca_VALUE.두바이트() != 0) throw new Terjemahan_ralat("try/catch/finally 미지원");
        함수형식 format_VALUE = new 함수형식(fungsi_VALUE.서술); if (setempat_COUNT < format_VALUE.인수.size()) throw new Terjemahan_ralat("매개변수보다 적은 setempat_Skop pemboleh_ubah_VALUE");
        Collections.addAll(baris,".text",".globl " + penanda_VALUE,".type " + penanda_VALUE + ", @function",penanda_VALUE + ":","pushl %ebp","movl %esp, %ebp","subl $" + setempat_COUNT * 4 + ", %esp");
        for (int 순번 = 0; 순번 < format_VALUE.인수.size(); 순번++) Collections.addAll(baris,"movl " + (8 + 4 * (format_VALUE.인수.size() - 순번 - 1)) + "(%ebp), %eax","movl %eax, -" + (4 * (순번 + 1)) + "(%ebp)");
        Kelas_data Kelas_VALUE = 클래스들.get(fungsi_VALUE.pemilik_VALUE); Set<Integer> 경계들 = new HashSet<>(), cabang_Senarai = new HashSet<>();
        String[] 비교들 = {"je","jne","jl","jge","jg","jle","je","jne"};
        while (perintah_data.Kedudukan < perintah_data.data.length) {
            int Kedudukan = perintah_data.Kedudukan, Perintah = perintah_data.한바이트(); String jawatan_INDEX = penanda_VALUE + "_b" + Kedudukan;
            baris.add(jawatan_INDEX + ":"); 경계들.add(Kedudukan);
            if (Perintah == 0) baris.add("nop");
            else if (Perintah == 1) baris.add("pushl $0");
            else if (Perintah >= 2 && Perintah <= 8) baris.add("pushl $" + (Perintah - 3));
            else if (Perintah == 16 || Perintah == 17) baris.add("pushl $" + (Perintah == 16 ? perintah_data.부호한바이트() : perintah_data.부호두바이트()));
            else if (Perintah == 18 || Perintah == 19) {
                int INDEX = Perintah == 18 ? perintah_data.한바이트() : perintah_data.두바이트();
                baris.add("pushl $" + X_86_pemalar(Kelas_VALUE,INDEX));
            } else if (Perintah == 21 || Perintah == 25 || (Perintah >= 26 && Perintah <= 29) || (Perintah >= 42 && Perintah <= 45) || Perintah == 54 || Perintah == 58 || (Perintah >= 59 && Perintah <= 62) || (Perintah >= 75 && Perintah <= 78)) {
                boolean 읽음 = Perintah < 54; int INDEX = Perintah == 21 || Perintah == 25 || Perintah == 54 || Perintah == 58 ? perintah_data.한바이트() : Perintah - (Perintah <= 29 ? 26 : Perintah <= 45 ? 42 : Perintah <= 62 ? 59 : 75);
                cek_setempat(INDEX,setempat_COUNT); baris.add((읽음 ? "pushl " : "popl ") + "-" + (4 * (INDEX + 1)) + "(%ebp)");
            } else if (Perintah == 46) Collections.addAll(baris,"popl %ecx","popl %eax","call rt_array_check","pushl 4(%eax,%ecx,4)");
            else if (Perintah == 79) Collections.addAll(baris,"popl %edx","popl %ecx","popl %eax","call rt_array_check","movl %edx, 4(%eax,%ecx,4)");
            else if (Perintah == 87 || Perintah == 88) baris.add("addl $" + (Perintah == 87 ? 4 : 8) + ", %esp");
            else if (Perintah >= 89 && Perintah <= 95) {
                int[] 개수들 = {1,2,3,2,3,4,2}; int[][] tertib_Senarai = {{0,0},{0,1,0},{0,2,1,0},{1,0,1,0},{1,0,2,1,0},{1,0,3,2,1,0},{0,1}}; String[] 저장기들 = {"%eax","%ecx","%edx","%ebx"};
                for (int 순번 = 0; 순번 < 개수들[Perintah - 89]; 순번++) baris.add("popl " + 저장기들[순번]);
                for (int 순번 : tertib_Senarai[Perintah - 89]) baris.add("pushl " + 저장기들[순번]);
            } else if (Perintah == 96 || Perintah == 100 || Perintah == 104 || Perintah == 126 || Perintah == 128 || Perintah == 130) {
                String operasi_VALUE = Perintah == 96 ? "addl" : Perintah == 100 ? "subl" : Perintah == 104 ? "imull" : Perintah == 126 ? "andl" : Perintah == 128 ? "orl" : "xorl";
                Collections.addAll(baris,"popl %ecx","popl %eax",operasi_VALUE + " %ecx, %eax","pushl %eax");
            } else if (Perintah == 108 || Perintah == 112) Collections.addAll(baris,"popl %ecx","popl %eax","testl %ecx, %ecx","jz rt_div_zero","cmpl $-1, %ecx","jne " + jawatan_INDEX + "_divide","cmpl $0x80000000, %eax","jne " + jawatan_INDEX + "_divide","xorl %edx, %edx","jmp " + jawatan_INDEX + "_done",jawatan_INDEX + "_divide:","cltd","idivl %ecx",jawatan_INDEX + "_done:","pushl " + (Perintah == 108 ? "%eax" : "%edx"));
            else if (Perintah == 116) baris.add("negl (%esp)");
            else if (Perintah == 120 || Perintah == 122 || Perintah == 124) Collections.addAll(baris,"popl %ecx","popl %eax",(Perintah == 120 ? "sall" : Perintah == 122 ? "sarl" : "shrl") + " %cl, %eax","pushl %eax");
            else if (Perintah == 132) {
                int INDEX = perintah_data.한바이트(), tokokan_VALUE = perintah_data.부호한바이트(); cek_setempat(INDEX,setempat_COUNT); baris.add("addl $" + tokokan_VALUE + ", -" + (4 * (INDEX + 1)) + "(%ebp)");
            } else if (Perintah >= 145 && Perintah <= 147) Collections.addAll(baris,"popl %eax",Perintah == 145 ? "movsbl %al, %eax" : Perintah == 146 ? "movzwl %ax, %eax" : "movswl %ax, %eax","pushl %eax");
            else if (Perintah >= 153 && Perintah <= 166) {
                if (Perintah <= 158) Collections.addAll(baris,"popl %eax","testl %eax, %eax");
                else Collections.addAll(baris,"popl %ecx","popl %eax","cmpl %ecx, %eax");
                int destinasi_VALUE = Kedudukan + perintah_data.부호두바이트(); cabang_Senarai.add(destinasi_VALUE); baris.add(비교들[Perintah - (Perintah <= 158 ? 153 : 159)] + " " + penanda_VALUE + "_b" + destinasi_VALUE);
            } else if (Perintah == 167 || Perintah == 200) {
                int destinasi_VALUE = Kedudukan + (Perintah == 167 ? perintah_data.부호두바이트() : perintah_data.네바이트()); cabang_Senarai.add(destinasi_VALUE); baris.add("jmp " + penanda_VALUE + "_b" + destinasi_VALUE);
            } else if (Perintah == 170 || Perintah == 171) {
                while (perintah_data.Kedudukan % 4 != 0) perintah_data.한바이트();
                int nilai_lalai = Kedudukan + perintah_data.네바이트(); cabang_Senarai.add(nilai_lalai); baris.add("popl %eax");
                int item_COUNT, 아래 = 0;
                if (Perintah == 170) { 아래 = perintah_data.네바이트(); int 위 = perintah_data.네바이트(); long kepanjangan_VALUE = (long)위 - 아래 + 1; if (kepanjangan_VALUE < 1 || kepanjangan_VALUE > (perintah_data.data.length - perintah_data.Kedudukan) / 4) throw new Terjemahan_ralat("switch klip RALAT"); item_COUNT = (int)kepanjangan_VALUE; }
                else { item_COUNT = perintah_data.네바이트(); if (item_COUNT < 0 || item_COUNT > (perintah_data.data.length - perintah_data.Kedudukan) / 8) throw new Terjemahan_ralat("switch Saiz RALAT"); }
                for (int 순번 = 0; 순번 < item_COUNT; 순번++) {
                    int VALUE = Perintah == 170 ? 아래 + 순번 : perintah_data.네바이트(), destinasi_VALUE = Kedudukan + perintah_data.네바이트(); cabang_Senarai.add(destinasi_VALUE);
                    Collections.addAll(baris,"cmpl $" + VALUE + ", %eax","je " + penanda_VALUE + "_b" + destinasi_VALUE);
                }
                baris.add("jmp " + penanda_VALUE + "_b" + nilai_lalai);
            } else if (Perintah == 172 || Perintah == 176 || Perintah == 177) {
                if (Perintah != 177) baris.add("popl %eax"); Collections.addAll(baris,"leave","ret");
            } else if (Perintah == 178 || Perintah == 179) {
                kaedah_Rujukan Rujukan = Kelas_VALUE.Rujukan(perintah_data.두바이트()); if (!필드들.containsKey(Rujukan)) throw new Terjemahan_ralat("알 수 없는 medan_VALUE");
                Collections.addAll(baris,"call " + simbol("init",Rujukan.pemilik_VALUE),(Perintah == 178 ? "pushl " : "popl ") + simbol("field",Rujukan.부분들()));
            } else if (Perintah == 184) {
                kaedah_Rujukan Rujukan = Kelas_VALUE.Rujukan(perintah_data.두바이트()); if (!함수들.containsKey(Rujukan)) throw new Terjemahan_ralat("알 수 없는 fungsi_VALUE");
                함수형식 호출형식 = new 함수형식(Rujukan.서술); Collections.addAll(baris,"call " + simbol("init",Rujukan.pemilik_VALUE),"call " + simbol("method",Rujukan.부분들()));
                if (!호출형식.인수.isEmpty()) baris.add("addl $" + 호출형식.인수.size() * 4 + ", %esp");
                if (!호출형식.kembalikan_ukuran.equals("V")) baris.add("pushl %eax");
            } else if (Perintah == 182) {
                kaedah_Rujukan Rujukan = Kelas_VALUE.Rujukan(perintah_data.두바이트());
                if (Rujukan.equals(new kaedah_Rujukan("java/lang/String","length","()I"))) Collections.addAll(baris,"popl %eax","testl %eax, %eax","jz rt_null","pushl (%eax)");
                else if (Rujukan.equals(new kaedah_Rujukan("java/lang/String","charAt","(I)C"))) Collections.addAll(baris,"popl %ecx","popl %eax","call rt_array_check","pushl 4(%eax,%ecx,4)");
                else throw new Terjemahan_ralat("가상 fungsi_VALUE 호출 미지원");
            } else if (Perintah == 188) {
                if (perintah_data.한바이트() != 10) throw new Terjemahan_ralat("new int[]만 Sokongan_VALUE"); Collections.addAll(baris,"popl %eax","call rt_new_array","pushl %eax");
            } else if (Perintah == 190) Collections.addAll(baris,"popl %eax","testl %eax, %eax","jz rt_null","pushl (%eax)");
            else if (Perintah == 196) {
                int sambungan_VALUE = perintah_data.한바이트(), INDEX = perintah_data.두바이트(); cek_setempat(INDEX,setempat_COUNT);
                if (sambungan_VALUE == 21 || sambungan_VALUE == 25 || sambungan_VALUE == 54 || sambungan_VALUE == 58) baris.add((sambungan_VALUE <= 25 ? "pushl " : "popl ") + "-" + 4 * (INDEX + 1) + "(%ebp)");
                else if (sambungan_VALUE == 132) baris.add("addl $" + perintah_data.부호두바이트() + ", -" + 4 * (INDEX + 1) + "(%ebp)");
                else throw new Terjemahan_ralat("wide Perintah 미지원");
            } else if (Perintah == 198 || Perintah == 199) {
                int destinasi_VALUE = Kedudukan + perintah_data.부호두바이트(); cabang_Senarai.add(destinasi_VALUE); Collections.addAll(baris,"popl %eax","testl %eax, %eax",(Perintah == 198 ? "je " : "jne ") + penanda_VALUE + "_b" + destinasi_VALUE);
            } else throw new Terjemahan_ralat("미지원 Perintah: " + Perintah);
        }
        if (!경계들.containsAll(cabang_Senarai)) throw new Terjemahan_ralat("Perintah 경계가 아닌 곳으로 cabang");
        baris.add(".size " + penanda_VALUE + ", .-" + penanda_VALUE); return String.join("\n",baris);
    }
    String X_86_pemalar(Kelas_data data, int INDEX) {
        if (data.상수종류[INDEX] == 3) return data.pemalar_data[INDEX].toString();
        if (data.상수종류[INDEX] == 8) return rentetan_simbol(data.문자((Integer)data.pemalar_data[INDEX]));
        throw new Terjemahan_ralat("정수와 rentetan_VALUE 상수만 Sokongan_VALUE");
    }
    String X_86_himpunan(String titik_permulaan, List<String> 내보냄, String sasaran) throws IOException {
        Map<String,String> mesin_jadual = new HashMap<>();
        for (String baris : Files.readAllLines(sumber_laluan.resolve("_86_mesin_Fungsi_Azure.tsv"))) { String[] berpasangan_VALUE = baris.split("\t"); if (berpasangan_VALUE[0].equals(sasaran)) mesin_jadual.put(berpasangan_VALUE[1] + berpasangan_VALUE[2],berpasangan_VALUE[3]); }
        int jawatan_INDEX = titik_permulaan.lastIndexOf('.'); if (jawatan_INDEX < 0) throw new Terjemahan_ralat("titik_permulaan Tugaskan_VALUE RALAT");
        String pemilik_VALUE = titik_permulaan.substring(0,jawatan_INDEX).replace('.','/'), kaedah_pemasukan_nama = titik_permulaan.substring(jawatan_INDEX + 1); kaedah_Rujukan titik_permulaan_VALUE = null;
        for (String 서술 : Arrays.asList("()I","()V")) { kaedah_Rujukan Rujukan = new kaedah_Rujukan(pemilik_VALUE,kaedah_pemasukan_nama,서술); if (함수들.containsKey(Rujukan)) { if (titik_permulaan_VALUE != null) throw new Terjemahan_ralat("겹친 titik_permulaan"); titik_permulaan_VALUE = Rujukan; } }
        if (titik_permulaan_VALUE == null || (함수들.get(titik_permulaan_VALUE).capai_pemasukan & 0x100) != 0) throw new Terjemahan_ralat("titik_permulaan_VALUE fungsi_VALUE format_VALUE RALAT");
        List<String> baris = new ArrayList<>(); baris.add(".code32");
        for (Kelas_data data : 클래스들.values()) {
            String status_VALUE = simbol("state",data.Nama), mengasal = simbol("init",data.Nama);
            Collections.addAll(baris,".bss",".balign 4",status_VALUE + ": .long 0",".text",mengasal + ":","cmpl $0, " + status_VALUE,"jne " + mengasal + "_done","movl $1, " + status_VALUE);
            kaedah_Rujukan 초기화참조 = new kaedah_Rujukan(data.Nama,"<clinit>","()V"); if (함수들.containsKey(초기화참조)) baris.add("call " + simbol("method",초기화참조.부분들()));
            Collections.addAll(baris,"movl $2, " + status_VALUE,mengasal + "_done:","ret");
            for (ahli_data medan_VALUE : data.medan_VALUE) {
                byte[] pemalar_VALUE = medan_VALUE.atribut_VALUE.get("ConstantValue"); String VALUE = pemalar_VALUE == null ? "0" : X_86_pemalar(data,new data_Pembaca(pemalar_VALUE).두바이트());
                Collections.addAll(baris,".data",".balign 4",simbol("field",data.Nama,medan_VALUE.Nama,medan_VALUE.서술) + ": .long " + VALUE);
            }
            for (ahli_data fungsi_VALUE : data.fungsi_VALUE) if (!fungsi_VALUE.Nama.equals("<init>")) baris.add(X_86_kaedah_isi(new kaedah_Rujukan(data.Nama,fungsi_VALUE.Nama,fungsi_VALUE.서술),fungsi_VALUE,mesin_jadual,sasaran));
        }
        Collections.addAll(baris,".text",".globl java_entry","java_entry:","call " + simbol("init",titik_permulaan_VALUE.pemilik_VALUE),"call " + simbol("method",titik_permulaan_VALUE.부분들()));
        if (titik_permulaan_VALUE.서술.equals("()V")) baris.add("xorl %eax, %eax"); baris.add("ret");
        for (String Tugaskan_VALUE : 내보냄) {
            int pembatas_VALUE = Tugaskan_VALUE.indexOf('='); if (pembatas_VALUE < 1) throw new Terjemahan_ralat("내보내기 Tugaskan_VALUE RALAT");
            String 외부 = Tugaskan_VALUE.substring(0,pembatas_VALUE), fungsi_VALUE = Tugaskan_VALUE.substring(pembatas_VALUE + 1); int divisyen_ukuran = fungsi_VALUE.lastIndexOf('.');
            if (divisyen_ukuran < 0 || !외부.matches("[A-Za-z_][A-Za-z0-9_]*")) throw new Terjemahan_ralat("내보내기 simbol RALAT");
            String Kelas_VALUE = fungsi_VALUE.substring(0,divisyen_ukuran).replace('.','/'), Nama = fungsi_VALUE.substring(divisyen_ukuran + 1); kaedah_Rujukan pilihan_VALUE = null;
            for (kaedah_Rujukan Rujukan : 함수들.keySet()) if (Rujukan.pemilik_VALUE.equals(Kelas_VALUE) && Rujukan.Nama.equals(Nama)) { if (pilihan_VALUE != null) throw new Terjemahan_ralat("겹친 내보내기 sasaran"); pilihan_VALUE = Rujukan; }
            if (pilihan_VALUE == null) throw new Terjemahan_ralat("내보낼 함수가 없음");
            Collections.addAll(baris,".text",".globl " + 외부,외부 + ":","call " + simbol("init",pilihan_VALUE.pemilik_VALUE),"jmp " + simbol("method",pilihan_VALUE.부분들()));
        }
        baris.add(".section .rodata");
        for (Map.Entry<String,String> pemasukan_VALUE : 문자열들.entrySet()) {
            Collections.addAll(baris,".balign 4",pemasukan_VALUE.getValue() + ":",".long " + pemasukan_VALUE.getKey().length());
            List<String> 단위들 = new ArrayList<>(); for (char unit_VALUE : pemasukan_VALUE.getKey().toCharArray()) 단위들.add(Integer.toString(unit_VALUE)); if (!단위들.isEmpty()) baris.add(".long " + String.join(",",단위들));
        }
        baris.add(".section .note.GNU-stack,\"\",@progbits"); return String.join("\n",baris) + "\n";
    }
    static void laksanakan_alat(List<String> Perintah) throws Exception {
        if (new ProcessBuilder(Perintah).inheritIO().start().waitFor() != 0) throw new Terjemahan_ralat("bina_sumber RALAT: " + Perintah.get(0));
    }
    static String data_rentetan(String Teks) { return "\"" + Teks.replace("\\","\\\\").replace("\"","\\\"").replace("\n","\\n").replace("\r","\\r").replace("\t","\\t") + "\""; }
    static void X_86_Terjemahan(List<Path> 입력들, String sasaran, String titik_permulaan, List<String> 내보냄, Path 출력, Path sumber_VALUE) throws Exception {
        Path 임시 = Files.createTempDirectory("jkoros-java-x86-"), Kelas_laluan = 임시.resolve("classes"); Files.createDirectory(Kelas_laluan);
        try {
            List<String> 자바명령 = new ArrayList<>(Arrays.asList("javac","-J-XX:-UsePerfData","--release","8","-encoding","UTF-8","-g:none","-proc:none","-implicit:none","-classpath",Kelas_laluan.toString(),"-sourcepath",Kelas_laluan.toString(),"-d",Kelas_laluan.toString()));
            List<Path> 바이트코드 = new ArrayList<>(); int sumber_COUNT = 0;
            for (Path 입력 : 입력들) {
                if (출력.toAbsolutePath().normalize().equals(입력.toAbsolutePath().normalize())) throw new Terjemahan_ralat("출력 파일과 입력이 같음");
                if (입력.toString().endsWith(".java")) { 자바명령.add(입력.toString()); sumber_COUNT++; }
                else if (입력.toString().endsWith(".class")) 바이트코드.add(입력);
                else throw new Terjemahan_ralat(".java 또는 .class만 Sokongan_VALUE");
            }
            if (sumber_COUNT > 0) laksanakan_alat(자바명령);
            try (java.util.stream.Stream<Path> laluan_Senarai = Files.walk(Kelas_laluan)) { laluan_Senarai.filter(LALUAN -> LALUAN.toString().endsWith(".class")).sorted().forEach(바이트코드::add); }
            기계어미리번역 tukar_VALUE = new 기계어미리번역(바이트코드,sasaran.equals("user") ? "user" : "kernel",262144,sumber_VALUE);
            String 조립 = tukar_VALUE.X_86_himpunan(titik_permulaan,내보냄,sasaran); Files.writeString(임시.resolve("program.s"),조립,StandardCharsets.UTF_8);
            Path alat_jawatan = sumber_VALUE.getParent();
            laksanakan_alat(Arrays.asList("as","--32","-o",임시.resolve("program.o").toString(),임시.resolve("program.s").toString()));
            laksanakan_alat(Arrays.asList("as","--32","-o",임시.resolve("runtime.o").toString(),alat_jawatan.resolve("masa_jalan_bahasa_biasa_Sokongan.s").toString()));
            List<String> Sambung = new ArrayList<>(Arrays.asList("ld","-m","elf_i386"));
            if (sasaran.equals("kernel")) Sambung.add("-r");
            else {
                laksanakan_alat(Arrays.asList("as","--32","-o",임시.resolve("start.o").toString(),alat_jawatan.resolve(sasaran.equals("user") ? "Mula_pengguna_aplikasi.s" : "리눅스시작.s").toString()));
                Collections.addAll(Sambung,"-e","_start",임시.resolve("start.o").toString());
                if (sasaran.equals("user")) Collections.addAll(Sambung,"-T",alat_jawatan.resolve("pengguna_paut_Navigasi.ld").toString());
            }
            Collections.addAll(Sambung,"-o",임시.resolve("result").toString(),임시.resolve("program.o").toString(),임시.resolve("runtime.o").toString()); laksanakan_alat(Sambung);
            출력 = 출력.toAbsolutePath(); Files.createDirectories(출력.getParent()); Path terbit_VALUE = Files.createTempFile(출력.getParent(),".elf-",".tmp");
            try { Files.copy(임시.resolve("result"),terbit_VALUE,StandardCopyOption.REPLACE_EXISTING); Files.move(terbit_VALUE,출력,StandardCopyOption.REPLACE_EXISTING); } finally { Files.deleteIfExists(terbit_VALUE); }
            Files.setPosixFilePermissions(출력,java.nio.file.attribute.PosixFilePermissions.fromString(sasaran.equals("linux") ? "rwxr-xr-x" : "rw-r--r--"));
            Files.writeString(Paths.get(출력 + ".s"),조립,StandardCharsets.UTF_8);
            List<String> simbol_data = new ArrayList<>(), data_sumber = new ArrayList<>();
            for (kaedah_Rujukan Rujukan : tukar_VALUE.함수들.keySet()) simbol_data.add(data_rentetan(simbol("method",Rujukan.부분들())) + ":" + data_rentetan(Rujukan.pemilik_VALUE + "." + Rujukan.Nama + Rujukan.서술));
            for (Path 입력 : 입력들) {
                byte[] cincangan_fail = MessageDigest.getInstance("SHA-256").digest(Files.readAllBytes(입력)); StringBuilder Teks = new StringBuilder(); for (byte VALUE : cincangan_fail) Teks.append(String.format(Locale.ROOT,"%02x",VALUE & 255));
                data_sumber.add(data_rentetan(입력.toAbsolutePath().toString()) + ":" + data_rentetan(Teks.toString()));
            }
            Files.writeString(Paths.get(출력 + ".json"),"{\"target\":" + data_rentetan(sasaran) + ",\"entry\":" + data_rentetan(titik_permulaan) + ",\"format\":\"ELF32 i386\",\"runtime_jvm\":false,\"symbols\":{" + String.join(",",simbol_data) + "},\"sources\":{" + String.join(",",data_sumber) + "}}\n",StandardCharsets.UTF_8);
        } finally {
            try (java.util.stream.Stream<Path> laluan_Senarai = Files.walk(임시)) { for (Path LALUAN : (Iterable<Path>)laluan_Senarai.sorted(Comparator.reverseOrder())::iterator) Files.deleteIfExists(LALUAN); }
        }
    }
    public static void main(String[] 인수) {
        try {
            String titik_permulaan = null, sasaran = "kernel", X_86_sasaran = null; Path 출력경로 = null; int 낱말수 = 262144; boolean 범용표기 = false;
            List<String> 내보냄 = new ArrayList<>(); List<Path> laluan_Senarai = new ArrayList<>();
            for (int 순번 = 0; 순번 < 인수.length; 순번++) {
                String VALUE = 인수[순번];
                switch (VALUE) {
                    case "--target": X_86_sasaran = 인수[++순번]; break;
                    case "--help": case "-h": System.out.println("사용법: --entry Kelas_VALUE.fungsi_VALUE -o 출력 [--target linux|kernel|user] [--profile kernel|user] [--export simbol=Kelas_VALUE.fungsi_VALUE] 클래스파일 또는 Java원문"); return;
                    case "--entry": titik_permulaan = 인수[++순번]; break;
                    case "--profile": sasaran = 인수[++순번]; break;
                    case "--heap-words": 낱말수 = Integer.parseInt(인수[++순번]); break;
                    case "--export": 내보냄.add(인수[++순번]); break;
                    case "-o": 출력경로 = Paths.get(인수[++순번]); break;
                    case "--ucn": 범용표기 = true; break;
                    default: if (VALUE.startsWith("-")) throw new Terjemahan_ralat("알 수 없는 옵션: " + VALUE); laluan_Senarai.add(Paths.get(VALUE));
                }
            }
            if (titik_permulaan == null || 출력경로 == null || laluan_Senarai.isEmpty()) throw new Terjemahan_ralat("--entry, -o, Kelas_VALUE 파일이 필요합니다");
            Path sumber_VALUE = Paths.get(System.getProperty("jkoros.compiler.resources"));
            if (X_86_sasaran != null) {
                if (!Arrays.asList("linux","kernel","user").contains(X_86_sasaran)) throw new Terjemahan_ralat("알 수 없는 laksanakan_perintah sasaran");
                X_86_Terjemahan(laluan_Senarai,X_86_sasaran,titik_permulaan,내보냄,출력경로,sumber_VALUE); return;
            }
            String SUMBER = new 기계어미리번역(laluan_Senarai, sasaran, 낱말수, sumber_VALUE).jana(titik_permulaan, 내보냄, 범용표기);
            출력경로 = 출력경로.toAbsolutePath(); Files.createDirectories(출력경로.getParent());
            Path 임시 = Files.createTempFile(출력경로.getParent(), ".aot-", ".tmp");
            try { Files.writeString(임시, SUMBER, StandardCharsets.UTF_8); Files.move(임시, 출력경로, StandardCopyOption.REPLACE_EXISTING); }
            finally { Files.deleteIfExists(임시); }
        } catch (Exception RALAT) { System.err.println("bina_sumber RALAT: " + RALAT.getMessage()); System.exit(1); }
    }
}
