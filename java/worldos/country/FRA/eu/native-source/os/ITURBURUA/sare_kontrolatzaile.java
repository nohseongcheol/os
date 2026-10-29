// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** PCI RTL8139 (10ec:8139), 단일 bidali_balio 버퍼와 8KiB 수신 Loop_balio. 인터럽트 대신 폴링한다. */
public final class sare_kontrolatzaile {
    static int 입출력기준주소 = 0;
    static int 수신위치 = 0, 송신칸 = 0;
    static int[] gailu_helbide_856320c2 = new int[6];
    static int 송신수 = 0, 수신수 = 0, errore_ZENBATU = 0;

    static int 설정읽기(int 장치번호, int Posizioa) {
        gailu_balio.입출력정수쓰기(0xcf8, 0x80000000 | (장치번호 << 11) | Posizioa);
        return gailu_balio.입출력정수읽기(0xcfc);
    }

    static boolean 준비() {
        int 장치번호 = -1;
        for (int INDIZE = 0; INDIZE < 32; INDIZE++) {
            if (설정읽기(INDIZE, 0) == 0x813910ec) { 장치번호 = INDIZE; break; }
        }
        if (장치번호 < 0) return false;
        int balio_lehenetsi = 설정읽기(장치번호, 0x10);
        if ((balio_lehenetsi & 1) == 0 || (balio_lehenetsi & 0xfffffffc) < 0x100 || (balio_lehenetsi & 0xfffffffc) > 65535) return false;
        입출력기준주소 = balio_lehenetsi & 0xfffc;
        int Komandoa = 설정읽기(장치번호, 4);
        gailu_balio.입출력정수쓰기(0xcf8, 0x80000004 | (장치번호 << 11));
        gailu_balio.입출력짧은수쓰기(0xcfc, Komandoa | 5); // I/O 및 bus master Onartu_balio, PCI Egoera_balio 비트는 건드리지 않음
        gailu_balio.입출력바이트쓰기(입출력기준주소 + 0x52, 0);
        if (!berrezarri_balio()) { 입출력기준주소 = 0; return false; }
        for (int INDIZE = 0; INDIZE < 6; INDIZE++) gailu_helbide_856320c2[INDIZE] = gailu_balio.입출력바이트읽기(입출력기준주소 + INDIZE);
        return true;
    }

    static boolean berrezarri_balio() {
        gailu_balio.입출력바이트쓰기(입출력기준주소 + 0x37, 0x10);
        int Exekutatu_2 = gailu_balio.밀리초();
        while ((gailu_balio.입출력바이트읽기(입출력기준주소 + 0x37) & 0x10) != 0)
            if (gailu_balio.밀리초() - Exekutatu_2 > 100) return false;
        수신위치 = 0; 송신칸 = 0;
        gailu_balio.입출력정수쓰기(입출력기준주소 + 0x30, gailu_balio.sare_Memoria());
        for (int INDIZE = 0; INDIZE < 4; INDIZE++) gailu_balio.입출력정수쓰기(입출력기준주소 + 0x20 + INDIZE * 4, gailu_balio.sare_Memoria() + 12288);
        gailu_balio.입출력짧은수쓰기(입출력기준주소 + 0x3c, 0);
        gailu_balio.입출력짧은수쓰기(입출력기준주소 + 0x3e, 0xffff);
        gailu_balio.입출력바이트쓰기(입출력기준주소 + 0x37, 0x0c);
        gailu_balio.입출력정수쓰기(입출력기준주소 + 0x44, 0x0000e78a); // 자기주소/igorri_balio, wrap 연속 Store_balio, 8KiB
        gailu_balio.입출력정수쓰기(입출력기준주소 + 0x40, 0x03000600);
        return true;
    }

    static int bidali(int[] datuak, int luzera_balio) {
        if (입출력기준주소 == 0) return -19;
        if (luzera_balio < 14 || luzera_balio > 1514) return -90;
        int egoera_ataka = 입출력기준주소 + 0x10 + 송신칸 * 4;
        int Exekutatu_2 = gailu_balio.밀리초();
        while ((gailu_balio.입출력정수읽기(egoera_ataka) & 0x2000) == 0)
            if (gailu_balio.밀리초() - Exekutatu_2 > 100) return -110;
        int Tamaina = luzera_balio < 60 ? 60 : luzera_balio;
        for (int INDIZE = 0; INDIZE < Tamaina; INDIZE++)
            gailu_balio.idatzi_Memoria(gailu_balio.sare_Memoria() + 12288 + INDIZE, INDIZE < luzera_balio ? datuak[INDIZE] : 0);
        gailu_balio.입출력정수쓰기(egoera_ataka, Tamaina | 0x00080000);
        Exekutatu_2 = gailu_balio.밀리초();
        while ((gailu_balio.입출력정수읽기(egoera_ataka) & 0xe0008000) == 0)
            if (gailu_balio.밀리초() - Exekutatu_2 > 100) return -110;
        if ((gailu_balio.입출력정수읽기(egoera_ataka) & 0x8000) == 0) { errore_ZENBATU++; return -5; }
        송신칸 = (송신칸 + 1) & 3;
        송신수++;
        return luzera_balio;
    }

    static int 받기(int[] datuak) {
        if (입출력기준주소 == 0) return 0;
        if ((gailu_balio.입출력바이트읽기(입출력기준주소 + 0x3e) & 0x50) != 0) {
            errore_ZENBATU++;
            if (!berrezarri_balio()) 입출력기준주소 = 0;
            return 0;
        }
        if ((gailu_balio.입출력바이트읽기(입출력기준주소 + 0x37) & 1) != 0) return 0;
        int 머리 = gailu_balio.sare_Memoria() + 수신위치;
        int Egoera_balio = 실행관리.짧은수(머리), Tamaina = 실행관리.짧은수(머리 + 2);
        if (Tamaina == 0xfff0) return 0; // DMA 진행 중
        if (Tamaina < 4 || Tamaina > 1518) {
            errore_ZENBATU++;
            if (!berrezarri_balio()) 입출력기준주소 = 0;
            return 0;
        }
        int luzera_balio = Tamaina - 4;
        if ((Egoera_balio & 1) != 0) {
            for (int INDIZE = 0; INDIZE < luzera_balio; INDIZE++) datuak[INDIZE] = gailu_balio.기억읽기(머리 + 4 + INDIZE);
            수신수++;
        } else { luzera_balio = 0; errore_ZENBATU++; }
        수신위치 = (수신위치 + Tamaina + 4 + 3) & ~3;
        수신위치 &= 8191;
        gailu_balio.입출력짧은수쓰기(입출력기준주소 + 0x38, (수신위치 - 16) & 65535);
        gailu_balio.입출력짧은수쓰기(입출력기준주소 + 0x3e, 0x000f);
        return luzera_balio;
    }
}
