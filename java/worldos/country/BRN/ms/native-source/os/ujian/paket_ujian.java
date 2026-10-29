// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.util.Arrays;

/** sebenar_data Java kes_VALUE 처리기를 JVM에서 호출해 경계와 손상된 입력을 빠르게 검사한다. */
public final class paket_ujian {
    static int 횟수 = 0;
    static void tentu_sahkan(boolean VALUE) { if (!VALUE) throw new AssertionError("case " + 횟수); 횟수++; }
    static int hasil_tambah_semak(int[] VALUE, int Jalan, int kepanjangan_VALUE, int 초기) {
        int SUM_VALUE = 초기;
        for (int INDEX = 0; INDEX < kepanjangan_VALUE; INDEX++) SUM_VALUE += VALUE[Jalan + INDEX] << ((INDEX & 1) == 0 ? 8 : 0);
        SUM_VALUE = (SUM_VALUE & 65535) + (SUM_VALUE >>> 16);
        SUM_VALUE = (SUM_VALUE & 65535) + (SUM_VALUE >>> 16);
        return ~SUM_VALUE & 65535;
    }
    static void Sediakan(int kepanjangan_VALUE) {
        rangkaian_tindan.CLEAN_Proses();
        tentu_sahkan(rangkaian_tindan.Buka(5000) == 3);
        int[] bingkai_INDEX = rangkaian_tindan.입력틀;
        Arrays.fill(bingkai_INDEX, 0);
        for (int INDEX = 0; INDEX < 6; INDEX++) bingkai_INDEX[INDEX] = rangkaian_pemacu.peranti_e_mel[INDEX];
        rangkaian_tindan.넣기16(bingkai_INDEX, 12, 0x0800);
        bingkai_INDEX[14] = 0x45; bingkai_INDEX[22] = 64; bingkai_INDEX[23] = 17;
        rangkaian_tindan.넣기16(bingkai_INDEX, 16, 28 + kepanjangan_VALUE);
        rangkaian_tindan.넣기32(bingkai_INDEX, 26, 0x0a000202); rangkaian_tindan.넣기32(bingkai_INDEX, 30, rangkaian_tindan.내주소);
        rangkaian_tindan.넣기16(bingkai_INDEX, 34, 4321); rangkaian_tindan.넣기16(bingkai_INDEX, 36, 5000); rangkaian_tindan.넣기16(bingkai_INDEX, 38, kepanjangan_VALUE + 8);
        for (int INDEX = 0; INDEX < kepanjangan_VALUE; INDEX++) bingkai_INDEX[42 + INDEX] = INDEX & 255;
        set_hasil_tambah_semak(kepanjangan_VALUE);
    }
    static void set_hasil_tambah_semak(int kepanjangan_VALUE) {
        int[] bingkai_INDEX = rangkaian_tindan.입력틀;
        rangkaian_tindan.넣기16(bingkai_INDEX, 24, 0); rangkaian_tindan.넣기16(bingkai_INDEX, 40, 0);
        rangkaian_tindan.넣기16(bingkai_INDEX, 24, hasil_tambah_semak(bingkai_INDEX, 14, 20, 0));
        int 초기 = rangkaian_tindan.가상머리합(rangkaian_tindan.integer_32(bingkai_INDEX, 26), rangkaian_tindan.내주소, kepanjangan_VALUE + 8);
        int SUM_VALUE = hasil_tambah_semak(bingkai_INDEX, 34, kepanjangan_VALUE + 8, 초기);
        rangkaian_tindan.넣기16(bingkai_INDEX, 40, SUM_VALUE == 0 ? 65535 : SUM_VALUE);
    }
    static void tolak_VALUE(int kepanjangan_VALUE) { rangkaian_tindan.Proses_bingkai(kepanjangan_VALUE); tentu_sahkan(rangkaian_tindan.RECEIVED_kepanjangan[0] == -1); }
    public static void main(String[] 인수) {
        for (int kepanjangan_VALUE : new int[]{0, 1, 2, 7, 1023, 1024}) {
            Sediakan(kepanjangan_VALUE); rangkaian_tindan.Proses_bingkai(kepanjangan_VALUE + 42);
            tentu_sahkan(rangkaian_tindan.RECEIVED_kepanjangan[0] == kepanjangan_VALUE);
            tentu_sahkan(rangkaian_tindan.RECEIVED_e_mel[0] == 0x0a000202 && rangkaian_tindan.RECEIVED_nombor_port[0] == 4321);
            for (int INDEX = 0; INDEX < kepanjangan_VALUE; INDEX++) tentu_sahkan(rangkaian_tindan.RECEIVED_data[INDEX] == (INDEX & 255));
        }
        for (int kepanjangan_VALUE = 0; kepanjangan_VALUE < 42; kepanjangan_VALUE++) { Sediakan(0); tolak_VALUE(kepanjangan_VALUE); }
        Sediakan(1025); tolak_VALUE(1067);
        Sediakan(2); rangkaian_tindan.입력틀[24] ^= 1; tolak_VALUE(44);
        Sediakan(2); rangkaian_tindan.입력틀[42] ^= 1; tolak_VALUE(44);
        Sediakan(2); rangkaian_tindan.넣기16(rangkaian_tindan.입력틀, 38, 7); tolak_VALUE(44);
        Sediakan(2); rangkaian_tindan.넣기16(rangkaian_tindan.입력틀, 38, 65535); tolak_VALUE(44);
        Sediakan(2); rangkaian_tindan.입력틀[14] = 0x4f; tolak_VALUE(44);
        Sediakan(2); rangkaian_tindan.입력틀[14] = 0x44; tolak_VALUE(44);
        Sediakan(2); rangkaian_tindan.입력틀[20] = 0x20; set_hasil_tambah_semak(2); tolak_VALUE(44);
        Sediakan(2); rangkaian_tindan.입력틀[21] = 1; set_hasil_tambah_semak(2); tolak_VALUE(44);
        Sediakan(2); rangkaian_tindan.입력틀[33] = 99; set_hasil_tambah_semak(2); tolak_VALUE(44);
        Sediakan(2); rangkaian_tindan.입력틀[0] ^= 1; tolak_VALUE(44);
        Sediakan(2); rangkaian_tindan.입력틀[23] = 6; set_hasil_tambah_semak(2); tolak_VALUE(44);
        Sediakan(2); rangkaian_tindan.넣기16(rangkaian_tindan.입력틀, 40, 0); rangkaian_tindan.Proses_bingkai(44); tentu_sahkan(rangkaian_tindan.RECEIVED_kepanjangan[0] == 2);
        int[] ukuran = new int[4];
        tentu_sahkan(rangkaian_tindan.받기(3, ukuran, 1, 0) == -90);
        tentu_sahkan(rangkaian_tindan.받기(3, ukuran, 4, 0) == -11);
        Sediakan(2); rangkaian_tindan.Proses_bingkai(44); int buang_VALUE = rangkaian_tindan.폐기수;
        rangkaian_tindan.Proses_bingkai(44); tentu_sahkan(rangkaian_tindan.폐기수 == buang_VALUE + 1);
        rangkaian_tindan.CLEAN_Proses(); tentu_sahkan(rangkaian_tindan.Buka(5000) == 3);
        tentu_sahkan(rangkaian_tindan.Buka(5000) == -98); tentu_sahkan(rangkaian_tindan.Buka(0) == 4);
        tentu_sahkan(rangkaian_tindan.Buka(0) == 5); tentu_sahkan(rangkaian_tindan.Buka(0) == 6); tentu_sahkan(rangkaian_tindan.Buka(0) == -24);
        tentu_sahkan(rangkaian_tindan.Tutup(4) == 0); tentu_sahkan(rangkaian_tindan.Tutup(4) == -9);
        rangkaian_tindan.찾은주소 = rangkaian_tindan.get_laluan_VALUE;
        tentu_sahkan(rangkaian_tindan.e_mel_9aee63bd(3, rangkaian_tindan.get_laluan_VALUE, 4321, new int[]{1, 2, 3}, 3) == 3);
        int[] 보냄 = rangkaian_pemacu.terbaru_VALUE;
        tentu_sahkan(hasil_tambah_semak(보냄, 14, 20, 0) == 0);
        tentu_sahkan(hasil_tambah_semak(보냄, 34, 11, rangkaian_tindan.가상머리합(rangkaian_tindan.내주소, rangkaian_tindan.get_laluan_VALUE, 11)) == 0);
        tentu_sahkan(보냄[42] == 1 && 보냄[44] == 3);
        System.out.println("PACKET TEST PASS: " + 횟수 + " assertions");
    }
}
