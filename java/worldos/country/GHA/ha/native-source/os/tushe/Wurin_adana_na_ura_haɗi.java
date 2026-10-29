// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 첫 IDE 장치의 512바이트 논리 Sashi_Daraja. 이 계층은 포맷을 만들거나 임의 장치를 지우지 않는다. */
public final class Wurin_adana_na_ura_haɗi {
    static boolean kimiyar_bayanai_Aiki_9e72441a = false;
    static int[] Sashi_Tarin_bayani = new int[512];
    static void 잠깐기다리기() {
        for (int Indes = 0; Indes < 4; Indes++) na_ura_Daraja.입출력바이트읽기(0x3f6);
    }
    static int 준비기다리기(boolean 자료필요) {
        int Tafiyar_da = na_ura_Daraja.밀리초();
        while (na_ura_Daraja.밀리초() - Tafiyar_da < 500) {
            int Matsayi_Daraja = na_ura_Daraja.입출력바이트읽기(0x1f7);
            if (Matsayi_Daraja == 0 || Matsayi_Daraja == 255) return -19;
            if ((Matsayi_Daraja & 128) == 0) {
                if ((Matsayi_Daraja & 33) != 0) return -5;
                if (!자료필요 || (Matsayi_Daraja & 8) != 0) return 0;
            }
            na_ura_Daraja.잠시양보();
        }
        return -110;
    }
    static int 요청(int Sashi_Daraja, int Umarni) {
        if (Sashi_Daraja < 0 || Sashi_Daraja >= 2048) return -22;
        na_ura_Daraja.입출력바이트쓰기(0x3f6, 2); // polling; IDE IRQ 사용 안 함
        na_ura_Daraja.입출력바이트쓰기(0x1f6, 0xe0); 잠깐기다리기();
        int 결과 = 준비기다리기(false);
        if (결과 < 0) return 결과;
        na_ura_Daraja.입출력바이트쓰기(0x1f2, 1);
        na_ura_Daraja.입출력바이트쓰기(0x1f3, Sashi_Daraja & 255);
        na_ura_Daraja.입출력바이트쓰기(0x1f4, (Sashi_Daraja >>> 8) & 255);
        na_ura_Daraja.입출력바이트쓰기(0x1f5, 0);
        na_ura_Daraja.입출력바이트쓰기(0x1f7, Umarni); 잠깐기다리기();
        return 준비기다리기(true);
    }
    static int Yi_Karatu(int Sashi_Daraja) {
        int 결과 = 요청(Sashi_Daraja, 0x20);
        if (결과 < 0) return 결과;
        for (int Indes = 0; Indes < 256; Indes++) {
            int Daraja = na_ura_Daraja.입출력짧은수읽기(0x1f0);
            Sashi_Tarin_bayani[Indes * 2] = Daraja & 255; Sashi_Tarin_bayani[Indes * 2 + 1] = Daraja >>> 8;
        }
        잠깐기다리기(); return 준비기다리기(false);
    }
    static int Yi_Rubutu(int Sashi_Daraja) {
        if (!kimiyar_bayanai_Aiki_9e72441a || Sashi_Daraja < 1 || Sashi_Daraja > 518) return -19;
        int 결과 = 요청(Sashi_Daraja, 0x30);
        if (결과 < 0) return 결과;
        for (int Indes = 0; Indes < 256; Indes++)
            na_ura_Daraja.입출력짧은수쓰기(0x1f0, Sashi_Tarin_bayani[Indes * 2] | Sashi_Tarin_bayani[Indes * 2 + 1] << 8);
        잠깐기다리기(); return 준비기다리기(false);
    }
    static int 밀어쓰기() {
        if (!kimiyar_bayanai_Aiki_9e72441a) return -19;
        na_ura_Daraja.입출력바이트쓰기(0x1f7, 0xe7); 잠깐기다리기();
        return 준비기다리기(false);
    }
    static int Daddatse_Lamba_mara(int 위치) {
        return Sashi_Tarin_bayani[위치] | Sashi_Tarin_bayani[위치 + 1] << 8 | Sashi_Tarin_bayani[위치 + 2] << 16 | Sashi_Tarin_bayani[위치 + 3] << 24;
    }
    static void Rubuta_Lamba_mara_Daraja(int 위치, int Daraja) {
        for (int Indes = 0; Indes < 4; Indes++) Sashi_Tarin_bayani[위치 + Indes] = (Daraja >>> (Indes * 8)) & 255;
    }
}
