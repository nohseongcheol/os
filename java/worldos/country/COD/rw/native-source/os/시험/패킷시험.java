// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.util.Arrays;

/** nyakuri_amakurushingiro Java ikibazo_agaciro 처리기를 JVM에서 호출해 경계와 손상된 입력을 빠르게 검사한다. */
public final class 패킷시험 {
    static int 횟수 = 0;
    static void gusuzuma(boolean agaciro) { if (!agaciro) throw new AssertionError("case " + 횟수); 횟수++; }
    static int 검사합(int[] agaciro, int ihuriro, int uburebure_agaciro, int 초기) {
        int 합 = 초기;
        for (int umugerekashakiro = 0; umugerekashakiro < uburebure_agaciro; umugerekashakiro++) 합 += agaciro[ihuriro + umugerekashakiro] << ((umugerekashakiro & 1) == 0 ? 8 : 0);
        합 = (합 & 65535) + (합 >>> 16);
        합 = (합 & 65535) + (합 >>> 16);
        return ~합 & 65535;
    }
    static void Gutegura(int uburebure_agaciro) {
        Urusobemiyoboro_Ikirundo.과정정리();
        gusuzuma(Urusobemiyoboro_Ikirundo.Gufungura(5000) == 3);
        int[] ikadiri_umugerekashakiro = Urusobemiyoboro_Ikirundo.입력틀;
        Arrays.fill(ikadiri_umugerekashakiro, 0);
        for (int umugerekashakiro = 0; umugerekashakiro < 6; umugerekashakiro++) ikadiri_umugerekashakiro[umugerekashakiro] = Urusobemiyoboro_mukoresha.igendanwa_aderesi[umugerekashakiro];
        Urusobemiyoboro_Ikirundo.넣기16(ikadiri_umugerekashakiro, 12, 0x0800);
        ikadiri_umugerekashakiro[14] = 0x45; ikadiri_umugerekashakiro[22] = 64; ikadiri_umugerekashakiro[23] = 17;
        Urusobemiyoboro_Ikirundo.넣기16(ikadiri_umugerekashakiro, 16, 28 + uburebure_agaciro);
        Urusobemiyoboro_Ikirundo.넣기32(ikadiri_umugerekashakiro, 26, 0x0a000202); Urusobemiyoboro_Ikirundo.넣기32(ikadiri_umugerekashakiro, 30, Urusobemiyoboro_Ikirundo.내주소);
        Urusobemiyoboro_Ikirundo.넣기16(ikadiri_umugerekashakiro, 34, 4321); Urusobemiyoboro_Ikirundo.넣기16(ikadiri_umugerekashakiro, 36, 5000); Urusobemiyoboro_Ikirundo.넣기16(ikadiri_umugerekashakiro, 38, uburebure_agaciro + 8);
        for (int umugerekashakiro = 0; umugerekashakiro < uburebure_agaciro; umugerekashakiro++) ikadiri_umugerekashakiro[42 + umugerekashakiro] = umugerekashakiro & 255;
        검사합넣기(uburebure_agaciro);
    }
    static void 검사합넣기(int uburebure_agaciro) {
        int[] ikadiri_umugerekashakiro = Urusobemiyoboro_Ikirundo.입력틀;
        Urusobemiyoboro_Ikirundo.넣기16(ikadiri_umugerekashakiro, 24, 0); Urusobemiyoboro_Ikirundo.넣기16(ikadiri_umugerekashakiro, 40, 0);
        Urusobemiyoboro_Ikirundo.넣기16(ikadiri_umugerekashakiro, 24, 검사합(ikadiri_umugerekashakiro, 14, 20, 0));
        int 초기 = Urusobemiyoboro_Ikirundo.가상머리합(Urusobemiyoboro_Ikirundo.umubare_wuzuye_32(ikadiri_umugerekashakiro, 26), Urusobemiyoboro_Ikirundo.내주소, uburebure_agaciro + 8);
        int 합 = 검사합(ikadiri_umugerekashakiro, 34, uburebure_agaciro + 8, 초기);
        Urusobemiyoboro_Ikirundo.넣기16(ikadiri_umugerekashakiro, 40, 합 == 0 ? 65535 : 합);
    }
    static void 거부(int uburebure_agaciro) { Urusobemiyoboro_Ikirundo.Inzira_ikadiri(uburebure_agaciro); gusuzuma(Urusobemiyoboro_Ikirundo.받은길이[0] == -1); }
    public static void main(String[] 인수) {
        for (int uburebure_agaciro : new int[]{0, 1, 2, 7, 1023, 1024}) {
            Gutegura(uburebure_agaciro); Urusobemiyoboro_Ikirundo.Inzira_ikadiri(uburebure_agaciro + 42);
            gusuzuma(Urusobemiyoboro_Ikirundo.받은길이[0] == uburebure_agaciro);
            gusuzuma(Urusobemiyoboro_Ikirundo.받은주소[0] == 0x0a000202 && Urusobemiyoboro_Ikirundo.받은접속번호[0] == 4321);
            for (int umugerekashakiro = 0; umugerekashakiro < uburebure_agaciro; umugerekashakiro++) gusuzuma(Urusobemiyoboro_Ikirundo.받은자료[umugerekashakiro] == (umugerekashakiro & 255));
        }
        for (int uburebure_agaciro = 0; uburebure_agaciro < 42; uburebure_agaciro++) { Gutegura(0); 거부(uburebure_agaciro); }
        Gutegura(1025); 거부(1067);
        Gutegura(2); Urusobemiyoboro_Ikirundo.입력틀[24] ^= 1; 거부(44);
        Gutegura(2); Urusobemiyoboro_Ikirundo.입력틀[42] ^= 1; 거부(44);
        Gutegura(2); Urusobemiyoboro_Ikirundo.넣기16(Urusobemiyoboro_Ikirundo.입력틀, 38, 7); 거부(44);
        Gutegura(2); Urusobemiyoboro_Ikirundo.넣기16(Urusobemiyoboro_Ikirundo.입력틀, 38, 65535); 거부(44);
        Gutegura(2); Urusobemiyoboro_Ikirundo.입력틀[14] = 0x4f; 거부(44);
        Gutegura(2); Urusobemiyoboro_Ikirundo.입력틀[14] = 0x44; 거부(44);
        Gutegura(2); Urusobemiyoboro_Ikirundo.입력틀[20] = 0x20; 검사합넣기(2); 거부(44);
        Gutegura(2); Urusobemiyoboro_Ikirundo.입력틀[21] = 1; 검사합넣기(2); 거부(44);
        Gutegura(2); Urusobemiyoboro_Ikirundo.입력틀[33] = 99; 검사합넣기(2); 거부(44);
        Gutegura(2); Urusobemiyoboro_Ikirundo.입력틀[0] ^= 1; 거부(44);
        Gutegura(2); Urusobemiyoboro_Ikirundo.입력틀[23] = 6; 검사합넣기(2); 거부(44);
        Gutegura(2); Urusobemiyoboro_Ikirundo.넣기16(Urusobemiyoboro_Ikirundo.입력틀, 40, 0); Urusobemiyoboro_Ikirundo.Inzira_ikadiri(44); gusuzuma(Urusobemiyoboro_Ikirundo.받은길이[0] == 2);
        int[] 결과 = new int[4];
        gusuzuma(Urusobemiyoboro_Ikirundo.받기(3, 결과, 1, 0) == -90);
        gusuzuma(Urusobemiyoboro_Ikirundo.받기(3, 결과, 4, 0) == -11);
        Gutegura(2); Urusobemiyoboro_Ikirundo.Inzira_ikadiri(44); int kureka_agaciro = Urusobemiyoboro_Ikirundo.폐기수;
        Urusobemiyoboro_Ikirundo.Inzira_ikadiri(44); gusuzuma(Urusobemiyoboro_Ikirundo.폐기수 == kureka_agaciro + 1);
        Urusobemiyoboro_Ikirundo.과정정리(); gusuzuma(Urusobemiyoboro_Ikirundo.Gufungura(5000) == 3);
        gusuzuma(Urusobemiyoboro_Ikirundo.Gufungura(5000) == -98); gusuzuma(Urusobemiyoboro_Ikirundo.Gufungura(0) == 4);
        gusuzuma(Urusobemiyoboro_Ikirundo.Gufungura(0) == 5); gusuzuma(Urusobemiyoboro_Ikirundo.Gufungura(0) == 6); gusuzuma(Urusobemiyoboro_Ikirundo.Gufungura(0) == -24);
        gusuzuma(Urusobemiyoboro_Ikirundo.Gufunga(4) == 0); gusuzuma(Urusobemiyoboro_Ikirundo.Gufunga(4) == -9);
        Urusobemiyoboro_Ikirundo.찾은주소 = Urusobemiyoboro_Ikirundo.muhuzaporotokore_agaciro;
        gusuzuma(Urusobemiyoboro_Ikirundo.kohereza(3, Urusobemiyoboro_Ikirundo.muhuzaporotokore_agaciro, 4321, new int[]{1, 2, 3}, 3) == 3);
        int[] 보냄 = Urusobemiyoboro_mukoresha.biheruka_agaciro;
        gusuzuma(검사합(보냄, 14, 20, 0) == 0);
        gusuzuma(검사합(보냄, 34, 11, Urusobemiyoboro_Ikirundo.가상머리합(Urusobemiyoboro_Ikirundo.내주소, Urusobemiyoboro_Ikirundo.muhuzaporotokore_agaciro, 11)) == 0);
        gusuzuma(보냄[42] == 1 && 보냄[44] == 3);
        System.out.println("PACKET TEST PASS: " + 횟수 + " assertions");
    }
}
