// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.util.Arrays;

/** faktiki_verilənlər Java müqavilə_VALUE 처리기를 JVM에서 호출해 경계와 손상된 입력을 빠르게 검사한다. */
public final class 패킷시험 {
    static int 횟수 = 0;
    static void yoxlamaq(boolean VALUE) { if (!VALUE) throw new AssertionError("case " + 횟수); 횟수++; }
    static int 검사합(int[] VALUE, int İcra_Et, int uzunluq_VALUE, int 초기) {
        int SUM_VALUE = 초기;
        for (int INDEX = 0; INDEX < uzunluq_VALUE; INDEX++) SUM_VALUE += VALUE[İcra_Et + INDEX] << ((INDEX & 1) == 0 ? 8 : 0);
        SUM_VALUE = (SUM_VALUE & 65535) + (SUM_VALUE >>> 16);
        SUM_VALUE = (SUM_VALUE & 65535) + (SUM_VALUE >>> 16);
        return ~SUM_VALUE & 65535;
    }
    static void Hazırla(int uzunluq_VALUE) {
        Şəbəkə_Yığın.CLEAN_Proses();
        yoxlamaq(Şəbəkə_Yığın.Aç(5000) == 3);
        int[] kadr_INDEX = Şəbəkə_Yığın.입력틀;
        Arrays.fill(kadr_INDEX, 0);
        for (int INDEX = 0; INDEX < 6; INDEX++) kadr_INDEX[INDEX] = Şəbəkə_drayver.cihaz_ünvan[INDEX];
        Şəbəkə_Yığın.넣기16(kadr_INDEX, 12, 0x0800);
        kadr_INDEX[14] = 0x45; kadr_INDEX[22] = 64; kadr_INDEX[23] = 17;
        Şəbəkə_Yığın.넣기16(kadr_INDEX, 16, 28 + uzunluq_VALUE);
        Şəbəkə_Yığın.넣기32(kadr_INDEX, 26, 0x0a000202); Şəbəkə_Yığın.넣기32(kadr_INDEX, 30, Şəbəkə_Yığın.내주소);
        Şəbəkə_Yığın.넣기16(kadr_INDEX, 34, 4321); Şəbəkə_Yığın.넣기16(kadr_INDEX, 36, 5000); Şəbəkə_Yığın.넣기16(kadr_INDEX, 38, uzunluq_VALUE + 8);
        for (int INDEX = 0; INDEX < uzunluq_VALUE; INDEX++) kadr_INDEX[42 + INDEX] = INDEX & 255;
        검사합넣기(uzunluq_VALUE);
    }
    static void 검사합넣기(int uzunluq_VALUE) {
        int[] kadr_INDEX = Şəbəkə_Yığın.입력틀;
        Şəbəkə_Yığın.넣기16(kadr_INDEX, 24, 0); Şəbəkə_Yığın.넣기16(kadr_INDEX, 40, 0);
        Şəbəkə_Yığın.넣기16(kadr_INDEX, 24, 검사합(kadr_INDEX, 14, 20, 0));
        int 초기 = Şəbəkə_Yığın.가상머리합(Şəbəkə_Yığın.tam_ədəd_32(kadr_INDEX, 26), Şəbəkə_Yığın.내주소, uzunluq_VALUE + 8);
        int SUM_VALUE = 검사합(kadr_INDEX, 34, uzunluq_VALUE + 8, 초기);
        Şəbəkə_Yığın.넣기16(kadr_INDEX, 40, SUM_VALUE == 0 ? 65535 : SUM_VALUE);
    }
    static void 거부(int uzunluq_VALUE) { Şəbəkə_Yığın.Proses_kadr(uzunluq_VALUE); yoxlamaq(Şəbəkə_Yığın.RECEIVED_uzunluq[0] == -1); }
    public static void main(String[] 인수) {
        for (int uzunluq_VALUE : new int[]{0, 1, 2, 7, 1023, 1024}) {
            Hazırla(uzunluq_VALUE); Şəbəkə_Yığın.Proses_kadr(uzunluq_VALUE + 42);
            yoxlamaq(Şəbəkə_Yığın.RECEIVED_uzunluq[0] == uzunluq_VALUE);
            yoxlamaq(Şəbəkə_Yığın.RECEIVED_ünvan[0] == 0x0a000202 && Şəbəkə_Yığın.받은접속번호[0] == 4321);
            for (int INDEX = 0; INDEX < uzunluq_VALUE; INDEX++) yoxlamaq(Şəbəkə_Yığın.RECEIVED_verilənlər[INDEX] == (INDEX & 255));
        }
        for (int uzunluq_VALUE = 0; uzunluq_VALUE < 42; uzunluq_VALUE++) { Hazırla(0); 거부(uzunluq_VALUE); }
        Hazırla(1025); 거부(1067);
        Hazırla(2); Şəbəkə_Yığın.입력틀[24] ^= 1; 거부(44);
        Hazırla(2); Şəbəkə_Yığın.입력틀[42] ^= 1; 거부(44);
        Hazırla(2); Şəbəkə_Yığın.넣기16(Şəbəkə_Yığın.입력틀, 38, 7); 거부(44);
        Hazırla(2); Şəbəkə_Yığın.넣기16(Şəbəkə_Yığın.입력틀, 38, 65535); 거부(44);
        Hazırla(2); Şəbəkə_Yığın.입력틀[14] = 0x4f; 거부(44);
        Hazırla(2); Şəbəkə_Yığın.입력틀[14] = 0x44; 거부(44);
        Hazırla(2); Şəbəkə_Yığın.입력틀[20] = 0x20; 검사합넣기(2); 거부(44);
        Hazırla(2); Şəbəkə_Yığın.입력틀[21] = 1; 검사합넣기(2); 거부(44);
        Hazırla(2); Şəbəkə_Yığın.입력틀[33] = 99; 검사합넣기(2); 거부(44);
        Hazırla(2); Şəbəkə_Yığın.입력틀[0] ^= 1; 거부(44);
        Hazırla(2); Şəbəkə_Yığın.입력틀[23] = 6; 검사합넣기(2); 거부(44);
        Hazırla(2); Şəbəkə_Yığın.넣기16(Şəbəkə_Yığın.입력틀, 40, 0); Şəbəkə_Yığın.Proses_kadr(44); yoxlamaq(Şəbəkə_Yığın.RECEIVED_uzunluq[0] == 2);
        int[] ölçü = new int[4];
        yoxlamaq(Şəbəkə_Yığın.받기(3, ölçü, 1, 0) == -90);
        yoxlamaq(Şəbəkə_Yığın.받기(3, ölçü, 4, 0) == -11);
        Hazırla(2); Şəbəkə_Yığın.Proses_kadr(44); int ləğv_etmək_VALUE = Şəbəkə_Yığın.폐기수;
        Şəbəkə_Yığın.Proses_kadr(44); yoxlamaq(Şəbəkə_Yığın.폐기수 == ləğv_etmək_VALUE + 1);
        Şəbəkə_Yığın.CLEAN_Proses(); yoxlamaq(Şəbəkə_Yığın.Aç(5000) == 3);
        yoxlamaq(Şəbəkə_Yığın.Aç(5000) == -98); yoxlamaq(Şəbəkə_Yığın.Aç(0) == 4);
        yoxlamaq(Şəbəkə_Yığın.Aç(0) == 5); yoxlamaq(Şəbəkə_Yığın.Aç(0) == 6); yoxlamaq(Şəbəkə_Yığın.Aç(0) == -24);
        yoxlamaq(Şəbəkə_Yığın.Bağla(4) == 0); yoxlamaq(Şəbəkə_Yığın.Bağla(4) == -9);
        Şəbəkə_Yığın.찾은주소 = Şəbəkə_Yığın.şlüz_VALUE;
        yoxlamaq(Şəbəkə_Yığın.göndərmək(3, Şəbəkə_Yığın.şlüz_VALUE, 4321, new int[]{1, 2, 3}, 3) == 3);
        int[] 보냄 = Şəbəkə_drayver.son_VALUE;
        yoxlamaq(검사합(보냄, 14, 20, 0) == 0);
        yoxlamaq(검사합(보냄, 34, 11, Şəbəkə_Yığın.가상머리합(Şəbəkə_Yığın.내주소, Şəbəkə_Yığın.şlüz_VALUE, 11)) == 0);
        yoxlamaq(보냄[42] == 1 && 보냄[44] == 3);
        System.out.println("PACKET TEST PASS: " + 횟수 + " assertions");
    }
}
