// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.util.Arrays;

/** real_ma_lumotlar Java murojaat_VALUE 처리기를 JVM에서 호출해 경계와 손상된 입력을 빠르게 검사한다. */
public final class 패킷시험 {
    static int 횟수 = 0;
    static void tasdiqlamoq(boolean VALUE) { if (!VALUE) throw new AssertionError("case " + 횟수); 횟수++; }
    static int 검사합(int[] VALUE, int Bajarish, int uzunlik_VALUE, int 초기) {
        int SUM_VALUE = 초기;
        for (int INDEX = 0; INDEX < uzunlik_VALUE; INDEX++) SUM_VALUE += VALUE[Bajarish + INDEX] << ((INDEX & 1) == 0 ? 8 : 0);
        SUM_VALUE = (SUM_VALUE & 65535) + (SUM_VALUE >>> 16);
        SUM_VALUE = (SUM_VALUE & 65535) + (SUM_VALUE >>> 16);
        return ~SUM_VALUE & 65535;
    }
    static void Tayyorlamoq(int uzunlik_VALUE) {
        Tarmoq_Stack.Toza_Jarayon();
        tasdiqlamoq(Tarmoq_Stack.Ochish(5000) == 3);
        int[] kadr_INDEX = Tarmoq_Stack.입력틀;
        Arrays.fill(kadr_INDEX, 0);
        for (int INDEX = 0; INDEX < 6; INDEX++) kadr_INDEX[INDEX] = Tarmoq_drayver.qurilma_manzil[INDEX];
        Tarmoq_Stack.넣기16(kadr_INDEX, 12, 0x0800);
        kadr_INDEX[14] = 0x45; kadr_INDEX[22] = 64; kadr_INDEX[23] = 17;
        Tarmoq_Stack.넣기16(kadr_INDEX, 16, 28 + uzunlik_VALUE);
        Tarmoq_Stack.넣기32(kadr_INDEX, 26, 0x0a000202); Tarmoq_Stack.넣기32(kadr_INDEX, 30, Tarmoq_Stack.내주소);
        Tarmoq_Stack.넣기16(kadr_INDEX, 34, 4321); Tarmoq_Stack.넣기16(kadr_INDEX, 36, 5000); Tarmoq_Stack.넣기16(kadr_INDEX, 38, uzunlik_VALUE + 8);
        for (int INDEX = 0; INDEX < uzunlik_VALUE; INDEX++) kadr_INDEX[42 + INDEX] = INDEX & 255;
        검사합넣기(uzunlik_VALUE);
    }
    static void 검사합넣기(int uzunlik_VALUE) {
        int[] kadr_INDEX = Tarmoq_Stack.입력틀;
        Tarmoq_Stack.넣기16(kadr_INDEX, 24, 0); Tarmoq_Stack.넣기16(kadr_INDEX, 40, 0);
        Tarmoq_Stack.넣기16(kadr_INDEX, 24, 검사합(kadr_INDEX, 14, 20, 0));
        int 초기 = Tarmoq_Stack.가상머리합(Tarmoq_Stack.butun_son_32(kadr_INDEX, 26), Tarmoq_Stack.내주소, uzunlik_VALUE + 8);
        int SUM_VALUE = 검사합(kadr_INDEX, 34, uzunlik_VALUE + 8, 초기);
        Tarmoq_Stack.넣기16(kadr_INDEX, 40, SUM_VALUE == 0 ? 65535 : SUM_VALUE);
    }
    static void 거부(int uzunlik_VALUE) { Tarmoq_Stack.Jarayon_kadr(uzunlik_VALUE); tasdiqlamoq(Tarmoq_Stack.RECEIVED_uzunlik[0] == -1); }
    public static void main(String[] 인수) {
        for (int uzunlik_VALUE : new int[]{0, 1, 2, 7, 1023, 1024}) {
            Tayyorlamoq(uzunlik_VALUE); Tarmoq_Stack.Jarayon_kadr(uzunlik_VALUE + 42);
            tasdiqlamoq(Tarmoq_Stack.RECEIVED_uzunlik[0] == uzunlik_VALUE);
            tasdiqlamoq(Tarmoq_Stack.RECEIVED_manzil[0] == 0x0a000202 && Tarmoq_Stack.받은접속번호[0] == 4321);
            for (int INDEX = 0; INDEX < uzunlik_VALUE; INDEX++) tasdiqlamoq(Tarmoq_Stack.RECEIVED_ma_lumotlar[INDEX] == (INDEX & 255));
        }
        for (int uzunlik_VALUE = 0; uzunlik_VALUE < 42; uzunlik_VALUE++) { Tayyorlamoq(0); 거부(uzunlik_VALUE); }
        Tayyorlamoq(1025); 거부(1067);
        Tayyorlamoq(2); Tarmoq_Stack.입력틀[24] ^= 1; 거부(44);
        Tayyorlamoq(2); Tarmoq_Stack.입력틀[42] ^= 1; 거부(44);
        Tayyorlamoq(2); Tarmoq_Stack.넣기16(Tarmoq_Stack.입력틀, 38, 7); 거부(44);
        Tayyorlamoq(2); Tarmoq_Stack.넣기16(Tarmoq_Stack.입력틀, 38, 65535); 거부(44);
        Tayyorlamoq(2); Tarmoq_Stack.입력틀[14] = 0x4f; 거부(44);
        Tayyorlamoq(2); Tarmoq_Stack.입력틀[14] = 0x44; 거부(44);
        Tayyorlamoq(2); Tarmoq_Stack.입력틀[20] = 0x20; 검사합넣기(2); 거부(44);
        Tayyorlamoq(2); Tarmoq_Stack.입력틀[21] = 1; 검사합넣기(2); 거부(44);
        Tayyorlamoq(2); Tarmoq_Stack.입력틀[33] = 99; 검사합넣기(2); 거부(44);
        Tayyorlamoq(2); Tarmoq_Stack.입력틀[0] ^= 1; 거부(44);
        Tayyorlamoq(2); Tarmoq_Stack.입력틀[23] = 6; 검사합넣기(2); 거부(44);
        Tayyorlamoq(2); Tarmoq_Stack.넣기16(Tarmoq_Stack.입력틀, 40, 0); Tarmoq_Stack.Jarayon_kadr(44); tasdiqlamoq(Tarmoq_Stack.RECEIVED_uzunlik[0] == 2);
        int[] o_lchov = new int[4];
        tasdiqlamoq(Tarmoq_Stack.받기(3, o_lchov, 1, 0) == -90);
        tasdiqlamoq(Tarmoq_Stack.받기(3, o_lchov, 4, 0) == -11);
        Tayyorlamoq(2); Tarmoq_Stack.Jarayon_kadr(44); int rad_etmoq_VALUE = Tarmoq_Stack.폐기수;
        Tarmoq_Stack.Jarayon_kadr(44); tasdiqlamoq(Tarmoq_Stack.폐기수 == rad_etmoq_VALUE + 1);
        Tarmoq_Stack.Toza_Jarayon(); tasdiqlamoq(Tarmoq_Stack.Ochish(5000) == 3);
        tasdiqlamoq(Tarmoq_Stack.Ochish(5000) == -98); tasdiqlamoq(Tarmoq_Stack.Ochish(0) == 4);
        tasdiqlamoq(Tarmoq_Stack.Ochish(0) == 5); tasdiqlamoq(Tarmoq_Stack.Ochish(0) == 6); tasdiqlamoq(Tarmoq_Stack.Ochish(0) == -24);
        tasdiqlamoq(Tarmoq_Stack.Yopish(4) == 0); tasdiqlamoq(Tarmoq_Stack.Yopish(4) == -9);
        Tarmoq_Stack.찾은주소 = Tarmoq_Stack.shluz_VALUE;
        tasdiqlamoq(Tarmoq_Stack.yuborish(3, Tarmoq_Stack.shluz_VALUE, 4321, new int[]{1, 2, 3}, 3) == 3);
        int[] 보냄 = Tarmoq_drayver.so_nggi_VALUE;
        tasdiqlamoq(검사합(보냄, 14, 20, 0) == 0);
        tasdiqlamoq(검사합(보냄, 34, 11, Tarmoq_Stack.가상머리합(Tarmoq_Stack.내주소, Tarmoq_Stack.shluz_VALUE, 11)) == 0);
        tasdiqlamoq(보냄[42] == 1 && 보냄[44] == 3);
        System.out.println("PACKET TEST PASS: " + 횟수 + " assertions");
    }
}
