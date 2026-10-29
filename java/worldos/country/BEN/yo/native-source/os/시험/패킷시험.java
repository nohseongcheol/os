// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.util.Arrays;

/** gangan_détà Java iṣẹ́_iye 처리기를 JVM에서 호출해 경계와 손상된 입력을 빠르게 검사한다. */
public final class 패킷시험 {
    static int 횟수 = 0;
    static void ridájú(boolean iye) { if (!iye) throw new AssertionError("case " + 횟수); 횟수++; }
    static int 검사합(int[] iye, int Rọ́ọ̀nù, int gígùn_iye, int 초기) {
        int 합 = 초기;
        for (int wá_atọ̀ka_àkóónú = 0; wá_atọ̀ka_àkóónú < gígùn_iye; wá_atọ̀ka_àkóónú++) 합 += iye[Rọ́ọ̀nù + wá_atọ̀ka_àkóónú] << ((wá_atọ̀ka_àkóónú & 1) == 0 ? 8 : 0);
        합 = (합 & 65535) + (합 >>> 16);
        합 = (합 & 65535) + (합 >>> 16);
        return ~합 & 65535;
    }
    static void gbaradì(int gígùn_iye) {
        Alásopọ̀_kójọ.과정정리();
        ridájú(Alásopọ̀_kójọ.Ṣi(5000) == 3);
        int[] férèmù_wá_atọ̀ka_àkóónú = Alásopọ̀_kójọ.입력틀;
        Arrays.fill(férèmù_wá_atọ̀ka_àkóónú, 0);
        for (int wá_atọ̀ka_àkóónú = 0; wá_atọ̀ka_àkóónú < 6; wá_atọ̀ka_àkóónú++) férèmù_wá_atọ̀ka_àkóónú[wá_atọ̀ka_àkóónú] = Alásopọ̀_adarí_aláìrídìmú.ohun_èlò_àdírẹ́ẹ̀sì[wá_atọ̀ka_àkóónú];
        Alásopọ̀_kójọ.넣기16(férèmù_wá_atọ̀ka_àkóónú, 12, 0x0800);
        férèmù_wá_atọ̀ka_àkóónú[14] = 0x45; férèmù_wá_atọ̀ka_àkóónú[22] = 64; férèmù_wá_atọ̀ka_àkóónú[23] = 17;
        Alásopọ̀_kójọ.넣기16(férèmù_wá_atọ̀ka_àkóónú, 16, 28 + gígùn_iye);
        Alásopọ̀_kójọ.넣기32(férèmù_wá_atọ̀ka_àkóónú, 26, 0x0a000202); Alásopọ̀_kójọ.넣기32(férèmù_wá_atọ̀ka_àkóónú, 30, Alásopọ̀_kójọ.내주소);
        Alásopọ̀_kójọ.넣기16(férèmù_wá_atọ̀ka_àkóónú, 34, 4321); Alásopọ̀_kójọ.넣기16(férèmù_wá_atọ̀ka_àkóónú, 36, 5000); Alásopọ̀_kójọ.넣기16(férèmù_wá_atọ̀ka_àkóónú, 38, gígùn_iye + 8);
        for (int wá_atọ̀ka_àkóónú = 0; wá_atọ̀ka_àkóónú < gígùn_iye; wá_atọ̀ka_àkóónú++) férèmù_wá_atọ̀ka_àkóónú[42 + wá_atọ̀ka_àkóónú] = wá_atọ̀ka_àkóónú & 255;
        검사합넣기(gígùn_iye);
    }
    static void 검사합넣기(int gígùn_iye) {
        int[] férèmù_wá_atọ̀ka_àkóónú = Alásopọ̀_kójọ.입력틀;
        Alásopọ̀_kójọ.넣기16(férèmù_wá_atọ̀ka_àkóónú, 24, 0); Alásopọ̀_kójọ.넣기16(férèmù_wá_atọ̀ka_àkóónú, 40, 0);
        Alásopọ̀_kójọ.넣기16(férèmù_wá_atọ̀ka_àkóónú, 24, 검사합(férèmù_wá_atọ̀ka_àkóónú, 14, 20, 0));
        int 초기 = Alásopọ̀_kójọ.가상머리합(Alásopọ̀_kójọ.nọ́ńbà_odindi_32(férèmù_wá_atọ̀ka_àkóónú, 26), Alásopọ̀_kójọ.내주소, gígùn_iye + 8);
        int 합 = 검사합(férèmù_wá_atọ̀ka_àkóónú, 34, gígùn_iye + 8, 초기);
        Alásopọ̀_kójọ.넣기16(férèmù_wá_atọ̀ka_àkóónú, 40, 합 == 0 ? 65535 : 합);
    }
    static void 거부(int gígùn_iye) { Alásopọ̀_kójọ.Ìlànà_férèmù(gígùn_iye); ridájú(Alásopọ̀_kójọ.받은길이[0] == -1); }
    public static void main(String[] 인수) {
        for (int gígùn_iye : new int[]{0, 1, 2, 7, 1023, 1024}) {
            gbaradì(gígùn_iye); Alásopọ̀_kójọ.Ìlànà_férèmù(gígùn_iye + 42);
            ridájú(Alásopọ̀_kójọ.받은길이[0] == gígùn_iye);
            ridájú(Alásopọ̀_kójọ.받은주소[0] == 0x0a000202 && Alásopọ̀_kójọ.받은접속번호[0] == 4321);
            for (int wá_atọ̀ka_àkóónú = 0; wá_atọ̀ka_àkóónú < gígùn_iye; wá_atọ̀ka_àkóónú++) ridájú(Alásopọ̀_kójọ.받은자료[wá_atọ̀ka_àkóónú] == (wá_atọ̀ka_àkóónú & 255));
        }
        for (int gígùn_iye = 0; gígùn_iye < 42; gígùn_iye++) { gbaradì(0); 거부(gígùn_iye); }
        gbaradì(1025); 거부(1067);
        gbaradì(2); Alásopọ̀_kójọ.입력틀[24] ^= 1; 거부(44);
        gbaradì(2); Alásopọ̀_kójọ.입력틀[42] ^= 1; 거부(44);
        gbaradì(2); Alásopọ̀_kójọ.넣기16(Alásopọ̀_kójọ.입력틀, 38, 7); 거부(44);
        gbaradì(2); Alásopọ̀_kójọ.넣기16(Alásopọ̀_kójọ.입력틀, 38, 65535); 거부(44);
        gbaradì(2); Alásopọ̀_kójọ.입력틀[14] = 0x4f; 거부(44);
        gbaradì(2); Alásopọ̀_kójọ.입력틀[14] = 0x44; 거부(44);
        gbaradì(2); Alásopọ̀_kójọ.입력틀[20] = 0x20; 검사합넣기(2); 거부(44);
        gbaradì(2); Alásopọ̀_kójọ.입력틀[21] = 1; 검사합넣기(2); 거부(44);
        gbaradì(2); Alásopọ̀_kójọ.입력틀[33] = 99; 검사합넣기(2); 거부(44);
        gbaradì(2); Alásopọ̀_kójọ.입력틀[0] ^= 1; 거부(44);
        gbaradì(2); Alásopọ̀_kójọ.입력틀[23] = 6; 검사합넣기(2); 거부(44);
        gbaradì(2); Alásopọ̀_kójọ.넣기16(Alásopọ̀_kójọ.입력틀, 40, 0); Alásopọ̀_kójọ.Ìlànà_férèmù(44); ridájú(Alásopọ̀_kójọ.받은길이[0] == 2);
        int[] 결과 = new int[4];
        ridájú(Alásopọ̀_kójọ.받기(3, 결과, 1, 0) == -90);
        ridájú(Alásopọ̀_kójọ.받기(3, 결과, 4, 0) == -11);
        gbaradì(2); Alásopọ̀_kójọ.Ìlànà_férèmù(44); int pátì_iye = Alásopọ̀_kójọ.폐기수;
        Alásopọ̀_kójọ.Ìlànà_férèmù(44); ridájú(Alásopọ̀_kójọ.폐기수 == pátì_iye + 1);
        Alásopọ̀_kójọ.과정정리(); ridájú(Alásopọ̀_kójọ.Ṣi(5000) == 3);
        ridájú(Alásopọ̀_kójọ.Ṣi(5000) == -98); ridájú(Alásopọ̀_kójọ.Ṣi(0) == 4);
        ridájú(Alásopọ̀_kójọ.Ṣi(0) == 5); ridájú(Alásopọ̀_kójọ.Ṣi(0) == 6); ridájú(Alásopọ̀_kójọ.Ṣi(0) == -24);
        ridájú(Alásopọ̀_kójọ.Ti(4) == 0); ridájú(Alásopọ̀_kójọ.Ti(4) == -9);
        Alásopọ̀_kójọ.찾은주소 = Alásopọ̀_kójọ.ẹnu_odi_iye;
        ridájú(Alásopọ̀_kójọ.í_meèlì(3, Alásopọ̀_kójọ.ẹnu_odi_iye, 4321, new int[]{1, 2, 3}, 3) == 3);
        int[] 보냄 = Alásopọ̀_adarí_aláìrídìmú.Àìpẹ́_iye;
        ridájú(검사합(보냄, 14, 20, 0) == 0);
        ridájú(검사합(보냄, 34, 11, Alásopọ̀_kójọ.가상머리합(Alásopọ̀_kójọ.내주소, Alásopọ̀_kójọ.ẹnu_odi_iye, 11)) == 0);
        ridájú(보냄[42] == 1 && 보냄[44] == 3);
        System.out.println("PACKET TEST PASS: " + 횟수 + " assertions");
    }
}
