// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.util.Arrays;

/** aktual_data Java kasus_VALUE 처리기를 JVM에서 호출해 경계와 손상된 입력을 빠르게 검사한다. */
public final class 패킷시험 {
    static int pengulangan_COUNT = 0;
    static void periksa(boolean VALUE) { if (!VALUE) throw new AssertionError("case " + pengulangan_COUNT); pengulangan_COUNT++; }
    static int checksum(int[] VALUE, int jalankan, int panjang_VALUE, int keadaan_awal) {
        int SUM_VALUE = keadaan_awal;
        for (int INDEX = 0; INDEX < panjang_VALUE; INDEX++) SUM_VALUE += VALUE[jalankan + INDEX] << ((INDEX & 1) == 0 ? 8 : 0);
        SUM_VALUE = (SUM_VALUE & 65535) + (SUM_VALUE >>> 16);
        SUM_VALUE = (SUM_VALUE & 65535) + (SUM_VALUE >>> 16);
        return ~SUM_VALUE & 65535;
    }
    static void Siapkan(int panjang_VALUE) {
        jaringan_tumpuk.CLEAN_Proses();
        periksa(jaringan_tumpuk.Buka(5000) == 3);
        int[] bingkai_INDEX = jaringan_tumpuk.입력틀;
        Arrays.fill(bingkai_INDEX, 0);
        for (int INDEX = 0; INDEX < 6; INDEX++) bingkai_INDEX[INDEX] = jaringan_driver.Ponsel_surel[INDEX];
        jaringan_tumpuk.넣기16(bingkai_INDEX, 12, 0x0800);
        bingkai_INDEX[14] = 0x45; bingkai_INDEX[22] = 64; bingkai_INDEX[23] = 17;
        jaringan_tumpuk.넣기16(bingkai_INDEX, 16, 28 + panjang_VALUE);
        jaringan_tumpuk.넣기32(bingkai_INDEX, 26, 0x0a000202); jaringan_tumpuk.넣기32(bingkai_INDEX, 30, jaringan_tumpuk.내주소);
        jaringan_tumpuk.넣기16(bingkai_INDEX, 34, 4321); jaringan_tumpuk.넣기16(bingkai_INDEX, 36, 5000); jaringan_tumpuk.넣기16(bingkai_INDEX, 38, panjang_VALUE + 8);
        for (int INDEX = 0; INDEX < panjang_VALUE; INDEX++) bingkai_INDEX[42 + INDEX] = INDEX & 255;
        set_checksum(panjang_VALUE);
    }
    static void set_checksum(int panjang_VALUE) {
        int[] bingkai_INDEX = jaringan_tumpuk.입력틀;
        jaringan_tumpuk.넣기16(bingkai_INDEX, 24, 0); jaringan_tumpuk.넣기16(bingkai_INDEX, 40, 0);
        jaringan_tumpuk.넣기16(bingkai_INDEX, 24, checksum(bingkai_INDEX, 14, 20, 0));
        int keadaan_awal = jaringan_tumpuk.가상머리합(jaringan_tumpuk.bilangan_bulat_32(bingkai_INDEX, 26), jaringan_tumpuk.내주소, panjang_VALUE + 8);
        int SUM_VALUE = checksum(bingkai_INDEX, 34, panjang_VALUE + 8, keadaan_awal);
        jaringan_tumpuk.넣기16(bingkai_INDEX, 40, SUM_VALUE == 0 ? 65535 : SUM_VALUE);
    }
    static void tolak_VALUE(int panjang_VALUE) { jaringan_tumpuk.Proses_bingkai(panjang_VALUE); periksa(jaringan_tumpuk.RECEIVED_panjang[0] == -1); }
    public static void main(String[] argumen) {
        for (int panjang_VALUE : new int[]{0, 1, 2, 7, 1023, 1024}) {
            Siapkan(panjang_VALUE); jaringan_tumpuk.Proses_bingkai(panjang_VALUE + 42);
            periksa(jaringan_tumpuk.RECEIVED_panjang[0] == panjang_VALUE);
            periksa(jaringan_tumpuk.RECEIVED_surel[0] == 0x0a000202 && jaringan_tumpuk.RECEIVED_nomor_port[0] == 4321);
            for (int INDEX = 0; INDEX < panjang_VALUE; INDEX++) periksa(jaringan_tumpuk.RECEIVED_data[INDEX] == (INDEX & 255));
        }
        for (int panjang_VALUE = 0; panjang_VALUE < 42; panjang_VALUE++) { Siapkan(0); tolak_VALUE(panjang_VALUE); }
        Siapkan(1025); tolak_VALUE(1067);
        Siapkan(2); jaringan_tumpuk.입력틀[24] ^= 1; tolak_VALUE(44);
        Siapkan(2); jaringan_tumpuk.입력틀[42] ^= 1; tolak_VALUE(44);
        Siapkan(2); jaringan_tumpuk.넣기16(jaringan_tumpuk.입력틀, 38, 7); tolak_VALUE(44);
        Siapkan(2); jaringan_tumpuk.넣기16(jaringan_tumpuk.입력틀, 38, 65535); tolak_VALUE(44);
        Siapkan(2); jaringan_tumpuk.입력틀[14] = 0x4f; tolak_VALUE(44);
        Siapkan(2); jaringan_tumpuk.입력틀[14] = 0x44; tolak_VALUE(44);
        Siapkan(2); jaringan_tumpuk.입력틀[20] = 0x20; set_checksum(2); tolak_VALUE(44);
        Siapkan(2); jaringan_tumpuk.입력틀[21] = 1; set_checksum(2); tolak_VALUE(44);
        Siapkan(2); jaringan_tumpuk.입력틀[33] = 99; set_checksum(2); tolak_VALUE(44);
        Siapkan(2); jaringan_tumpuk.입력틀[0] ^= 1; tolak_VALUE(44);
        Siapkan(2); jaringan_tumpuk.입력틀[23] = 6; set_checksum(2); tolak_VALUE(44);
        Siapkan(2); jaringan_tumpuk.넣기16(jaringan_tumpuk.입력틀, 40, 0); jaringan_tumpuk.Proses_bingkai(44); periksa(jaringan_tumpuk.RECEIVED_panjang[0] == 2);
        int[] hasil = new int[4];
        periksa(jaringan_tumpuk.terima(3, hasil, 1, 0) == -90);
        periksa(jaringan_tumpuk.terima(3, hasil, 4, 0) == -11);
        Siapkan(2); jaringan_tumpuk.Proses_bingkai(44); int buang_VALUE = jaringan_tumpuk.폐기수;
        jaringan_tumpuk.Proses_bingkai(44); periksa(jaringan_tumpuk.폐기수 == buang_VALUE + 1);
        jaringan_tumpuk.CLEAN_Proses(); periksa(jaringan_tumpuk.Buka(5000) == 3);
        periksa(jaringan_tumpuk.Buka(5000) == -98); periksa(jaringan_tumpuk.Buka(0) == 4);
        periksa(jaringan_tumpuk.Buka(0) == 5); periksa(jaringan_tumpuk.Buka(0) == 6); periksa(jaringan_tumpuk.Buka(0) == -24);
        periksa(jaringan_tumpuk.Tutup(4) == 0); periksa(jaringan_tumpuk.Tutup(4) == -9);
        jaringan_tumpuk.찾은주소 = jaringan_tumpuk.gateway_VALUE;
        periksa(jaringan_tumpuk.kirim(3, jaringan_tumpuk.gateway_VALUE, 4321, new int[]{1, 2, 3}, 3) == 3);
        int[] 보냄 = jaringan_driver.terakhir_VALUE;
        periksa(checksum(보냄, 14, 20, 0) == 0);
        periksa(checksum(보냄, 34, 11, jaringan_tumpuk.가상머리합(jaringan_tumpuk.내주소, jaringan_tumpuk.gateway_VALUE, 11)) == 0);
        periksa(보냄[42] == 1 && 보냄[44] == 3);
        System.out.println("PACKET TEST PASS: " + pengulangan_COUNT + " assertions");
    }
}
