// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.util.Arrays;

/** faktisks_dati Java līguma_vērtība 처리기를 JVM에서 호출해 경계와 손상된 입력을 빠르게 검사한다. */
public final class 패킷시험 {
    static int 횟수 = 0;
    static void verificēt(boolean VALUE) { if (!VALUE) throw new AssertionError("case " + 횟수); 횟수++; }
    static int kontrolsumma(int[] VALUE, int Palaist, int 길이, int sākumstāvoklis) {
        int SUM_VALUE = sākumstāvoklis;
        for (int INDEX = 0; INDEX < 길이; INDEX++) SUM_VALUE += VALUE[Palaist + INDEX] << ((INDEX & 1) == 0 ? 8 : 0);
        SUM_VALUE = (SUM_VALUE & 65535) + (SUM_VALUE >>> 16);
        SUM_VALUE = (SUM_VALUE & 65535) + (SUM_VALUE >>> 16);
        return ~SUM_VALUE & 65535;
    }
    static void Sagatavot(int 길이) {
        tīkls_kopa.CLEAN_Process();
        verificēt(tīkls_kopa.Atvērt(5000) == 3);
        int[] kadrs_INDEX = tīkls_kopa.입력틀;
        Arrays.fill(kadrs_INDEX, 0);
        for (int INDEX = 0; INDEX < 6; INDEX++) kadrs_INDEX[INDEX] = tīkls_draiveris.ierīce_adrese[INDEX];
        tīkls_kopa.넣기16(kadrs_INDEX, 12, 0x0800);
        kadrs_INDEX[14] = 0x45; kadrs_INDEX[22] = 64; kadrs_INDEX[23] = 17;
        tīkls_kopa.넣기16(kadrs_INDEX, 16, 28 + 길이);
        tīkls_kopa.넣기32(kadrs_INDEX, 26, 0x0a000202); tīkls_kopa.넣기32(kadrs_INDEX, 30, tīkls_kopa.내주소);
        tīkls_kopa.넣기16(kadrs_INDEX, 34, 4321); tīkls_kopa.넣기16(kadrs_INDEX, 36, 5000); tīkls_kopa.넣기16(kadrs_INDEX, 38, 길이 + 8);
        for (int INDEX = 0; INDEX < 길이; INDEX++) kadrs_INDEX[42 + INDEX] = INDEX & 255;
        kopa_kontrolsumma(길이);
    }
    static void kopa_kontrolsumma(int 길이) {
        int[] kadrs_INDEX = tīkls_kopa.입력틀;
        tīkls_kopa.넣기16(kadrs_INDEX, 24, 0); tīkls_kopa.넣기16(kadrs_INDEX, 40, 0);
        tīkls_kopa.넣기16(kadrs_INDEX, 24, kontrolsumma(kadrs_INDEX, 14, 20, 0));
        int sākumstāvoklis = tīkls_kopa.가상머리합(tīkls_kopa.vesels_skaitlis_32(kadrs_INDEX, 26), tīkls_kopa.내주소, 길이 + 8);
        int SUM_VALUE = kontrolsumma(kadrs_INDEX, 34, 길이 + 8, sākumstāvoklis);
        tīkls_kopa.넣기16(kadrs_INDEX, 40, SUM_VALUE == 0 ? 65535 : SUM_VALUE);
    }
    static void noraidīt_VALUE(int 길이) { tīkls_kopa.Process_kadrs(길이); verificēt(tīkls_kopa.받은길이[0] == -1); }
    public static void main(String[] Parametri) {
        for (int 길이 : new int[]{0, 1, 2, 7, 1023, 1024}) {
            Sagatavot(길이); tīkls_kopa.Process_kadrs(길이 + 42);
            verificēt(tīkls_kopa.받은길이[0] == 길이);
            verificēt(tīkls_kopa.RECEIVED_adrese[0] == 0x0a000202 && tīkls_kopa.RECEIVED_porta_numurs[0] == 4321);
            for (int INDEX = 0; INDEX < 길이; INDEX++) verificēt(tīkls_kopa.RECEIVED_dati[INDEX] == (INDEX & 255));
        }
        for (int 길이 = 0; 길이 < 42; 길이++) { Sagatavot(0); noraidīt_VALUE(길이); }
        Sagatavot(1025); noraidīt_VALUE(1067);
        Sagatavot(2); tīkls_kopa.입력틀[24] ^= 1; noraidīt_VALUE(44);
        Sagatavot(2); tīkls_kopa.입력틀[42] ^= 1; noraidīt_VALUE(44);
        Sagatavot(2); tīkls_kopa.넣기16(tīkls_kopa.입력틀, 38, 7); noraidīt_VALUE(44);
        Sagatavot(2); tīkls_kopa.넣기16(tīkls_kopa.입력틀, 38, 65535); noraidīt_VALUE(44);
        Sagatavot(2); tīkls_kopa.입력틀[14] = 0x4f; noraidīt_VALUE(44);
        Sagatavot(2); tīkls_kopa.입력틀[14] = 0x44; noraidīt_VALUE(44);
        Sagatavot(2); tīkls_kopa.입력틀[20] = 0x20; kopa_kontrolsumma(2); noraidīt_VALUE(44);
        Sagatavot(2); tīkls_kopa.입력틀[21] = 1; kopa_kontrolsumma(2); noraidīt_VALUE(44);
        Sagatavot(2); tīkls_kopa.입력틀[33] = 99; kopa_kontrolsumma(2); noraidīt_VALUE(44);
        Sagatavot(2); tīkls_kopa.입력틀[0] ^= 1; noraidīt_VALUE(44);
        Sagatavot(2); tīkls_kopa.입력틀[23] = 6; kopa_kontrolsumma(2); noraidīt_VALUE(44);
        Sagatavot(2); tīkls_kopa.넣기16(tīkls_kopa.입력틀, 40, 0); tīkls_kopa.Process_kadrs(44); verificēt(tīkls_kopa.받은길이[0] == 2);
        int[] mērs = new int[4];
        verificēt(tīkls_kopa.saņemt(3, mērs, 1, 0) == -90);
        verificēt(tīkls_kopa.saņemt(3, mērs, 4, 0) == -11);
        Sagatavot(2); tīkls_kopa.Process_kadrs(44); int atmest_VALUE = tīkls_kopa.폐기수;
        tīkls_kopa.Process_kadrs(44); verificēt(tīkls_kopa.폐기수 == atmest_VALUE + 1);
        tīkls_kopa.CLEAN_Process(); verificēt(tīkls_kopa.Atvērt(5000) == 3);
        verificēt(tīkls_kopa.Atvērt(5000) == -98); verificēt(tīkls_kopa.Atvērt(0) == 4);
        verificēt(tīkls_kopa.Atvērt(0) == 5); verificēt(tīkls_kopa.Atvērt(0) == 6); verificēt(tīkls_kopa.Atvērt(0) == -24);
        verificēt(tīkls_kopa.Aizvērt(4) == 0); verificēt(tīkls_kopa.Aizvērt(4) == -9);
        tīkls_kopa.찾은주소 = tīkls_kopa.vārteja_VALUE;
        verificēt(tīkls_kopa.sūtīt(3, tīkls_kopa.vārteja_VALUE, 4321, new int[]{1, 2, 3}, 3) == 3);
        int[] 보냄 = tīkls_draiveris.pēdējās_VALUE;
        verificēt(kontrolsumma(보냄, 14, 20, 0) == 0);
        verificēt(kontrolsumma(보냄, 34, 11, tīkls_kopa.가상머리합(tīkls_kopa.내주소, tīkls_kopa.vārteja_VALUE, 11)) == 0);
        verificēt(보냄[42] == 1 && 보냄[44] == 3);
        System.out.println("PACKET TEST PASS: " + 횟수 + " assertions");
    }
}
