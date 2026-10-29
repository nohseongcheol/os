// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.util.Arrays;

/** laatii_keɓe Java haaju_njaru 처리기를 JVM에서 호출해 경계와 손상된 입력을 빠르게 검사한다. */
public final class 패킷시험 {
    static int 횟수 = 0;
    static void ƴeewtaade(boolean njaru) { if (!njaru) throw new AssertionError("case " + 횟수); 횟수++; }
    static int 검사합(int[] njaru, int huutoraade, int njuuteendi_njaru, int 초기) {
        int 합 = 초기;
        for (int joopirdu = 0; joopirdu < njuuteendi_njaru; joopirdu++) 합 += njaru[huutoraade + joopirdu] << ((joopirdu & 1) == 0 ? 8 : 0);
        합 = (합 & 65535) + (합 >>> 16);
        합 = (합 & 65535) + (합 >>> 16);
        return ~합 & 65535;
    }
    static void Heblu(int njuuteendi_njaru) {
        통신망.과정정리();
        ƴeewtaade(통신망.udditde(5000) == 3);
        int[] taƴtinnde_joopirdu = 통신망.입력틀;
        Arrays.fill(taƴtinnde_joopirdu, 0);
        for (int joopirdu = 0; joopirdu < 6; joopirdu++) taƴtinnde_joopirdu[joopirdu] = laylaytol_pilot.kaɓirgal_ñiiɓirde[joopirdu];
        통신망.넣기16(taƴtinnde_joopirdu, 12, 0x0800);
        taƴtinnde_joopirdu[14] = 0x45; taƴtinnde_joopirdu[22] = 64; taƴtinnde_joopirdu[23] = 17;
        통신망.넣기16(taƴtinnde_joopirdu, 16, 28 + njuuteendi_njaru);
        통신망.넣기32(taƴtinnde_joopirdu, 26, 0x0a000202); 통신망.넣기32(taƴtinnde_joopirdu, 30, 통신망.내주소);
        통신망.넣기16(taƴtinnde_joopirdu, 34, 4321); 통신망.넣기16(taƴtinnde_joopirdu, 36, 5000); 통신망.넣기16(taƴtinnde_joopirdu, 38, njuuteendi_njaru + 8);
        for (int joopirdu = 0; joopirdu < njuuteendi_njaru; joopirdu++) taƴtinnde_joopirdu[42 + joopirdu] = joopirdu & 255;
        검사합넣기(njuuteendi_njaru);
    }
    static void 검사합넣기(int njuuteendi_njaru) {
        int[] taƴtinnde_joopirdu = 통신망.입력틀;
        통신망.넣기16(taƴtinnde_joopirdu, 24, 0); 통신망.넣기16(taƴtinnde_joopirdu, 40, 0);
        통신망.넣기16(taƴtinnde_joopirdu, 24, 검사합(taƴtinnde_joopirdu, 14, 20, 0));
        int 초기 = 통신망.가상머리합(통신망.수32(taƴtinnde_joopirdu, 26), 통신망.내주소, njuuteendi_njaru + 8);
        int 합 = 검사합(taƴtinnde_joopirdu, 34, njuuteendi_njaru + 8, 초기);
        통신망.넣기16(taƴtinnde_joopirdu, 40, 합 == 0 ? 65535 : 합);
    }
    static void 거부(int njuuteendi_njaru) { 통신망.Yuɓɓo_golle_taƴtinnde(njuuteendi_njaru); ƴeewtaade(통신망.받은길이[0] == -1); }
    public static void main(String[] 인수) {
        for (int njuuteendi_njaru : new int[]{0, 1, 2, 7, 1023, 1024}) {
            Heblu(njuuteendi_njaru); 통신망.Yuɓɓo_golle_taƴtinnde(njuuteendi_njaru + 42);
            ƴeewtaade(통신망.받은길이[0] == njuuteendi_njaru);
            ƴeewtaade(통신망.받은주소[0] == 0x0a000202 && 통신망.받은접속번호[0] == 4321);
            for (int joopirdu = 0; joopirdu < njuuteendi_njaru; joopirdu++) ƴeewtaade(통신망.받은자료[joopirdu] == (joopirdu & 255));
        }
        for (int njuuteendi_njaru = 0; njuuteendi_njaru < 42; njuuteendi_njaru++) { Heblu(0); 거부(njuuteendi_njaru); }
        Heblu(1025); 거부(1067);
        Heblu(2); 통신망.입력틀[24] ^= 1; 거부(44);
        Heblu(2); 통신망.입력틀[42] ^= 1; 거부(44);
        Heblu(2); 통신망.넣기16(통신망.입력틀, 38, 7); 거부(44);
        Heblu(2); 통신망.넣기16(통신망.입력틀, 38, 65535); 거부(44);
        Heblu(2); 통신망.입력틀[14] = 0x4f; 거부(44);
        Heblu(2); 통신망.입력틀[14] = 0x44; 거부(44);
        Heblu(2); 통신망.입력틀[20] = 0x20; 검사합넣기(2); 거부(44);
        Heblu(2); 통신망.입력틀[21] = 1; 검사합넣기(2); 거부(44);
        Heblu(2); 통신망.입력틀[33] = 99; 검사합넣기(2); 거부(44);
        Heblu(2); 통신망.입력틀[0] ^= 1; 거부(44);
        Heblu(2); 통신망.입력틀[23] = 6; 검사합넣기(2); 거부(44);
        Heblu(2); 통신망.넣기16(통신망.입력틀, 40, 0); 통신망.Yuɓɓo_golle_taƴtinnde(44); ƴeewtaade(통신망.받은길이[0] == 2);
        int[] 결과 = new int[4];
        ƴeewtaade(통신망.받기(3, 결과, 1, 0) == -90);
        ƴeewtaade(통신망.받기(3, 결과, 4, 0) == -11);
        Heblu(2); 통신망.Yuɓɓo_golle_taƴtinnde(44); int 폐기 = 통신망.폐기수;
        통신망.Yuɓɓo_golle_taƴtinnde(44); ƴeewtaade(통신망.폐기수 == 폐기 + 1);
        통신망.과정정리(); ƴeewtaade(통신망.udditde(5000) == 3);
        ƴeewtaade(통신망.udditde(5000) == -98); ƴeewtaade(통신망.udditde(0) == 4);
        ƴeewtaade(통신망.udditde(0) == 5); ƴeewtaade(통신망.udditde(0) == 6); ƴeewtaade(통신망.udditde(0) == -24);
        ƴeewtaade(통신망.uddude(4) == 0); ƴeewtaade(통신망.uddude(4) == -9);
        통신망.찾은주소 = 통신망.관문;
        ƴeewtaade(통신망.neldude(3, 통신망.관문, 4321, new int[]{1, 2, 3}, 3) == 3);
        int[] 보냄 = laylaytol_pilot.최근;
        ƴeewtaade(검사합(보냄, 14, 20, 0) == 0);
        ƴeewtaade(검사합(보냄, 34, 11, 통신망.가상머리합(통신망.내주소, 통신망.관문, 11)) == 0);
        ƴeewtaade(보냄[42] == 1 && 보냄[44] == 3);
        System.out.println("PACKET TEST PASS: " + 횟수 + " assertions");
    }
}
