// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** PCI RTL8139 (10ec:8139), 단일 senda_VALUE_f993dacd 버퍼와 8KiB 수신 Loop_VALUE. 인터럽트 대신 폴링한다. */
public final class Net_rekill {
    static int 입출력기준주소 = 0;
    static int 수신위치 = 0, 송신칸 = 0;
    static int[] tæki_slóð = new int[6];
    static int 송신수 = 0, 수신수 = 0, villa_COUNT = 0;

    static int 설정읽기(int tæki_númer, int Staðsetning) {
        tæki_VALUE.입출력정수쓰기(0xcf8, 0x80000000 | (tæki_númer << 11) | Staðsetning);
        return tæki_VALUE.입출력정수읽기(0xcfc);
    }

    static boolean Undirbúa() {
        int tæki_númer = -1;
        for (int INDEX = 0; INDEX < 32; INDEX++) {
            if (설정읽기(INDEX, 0) == 0x813910ec) { tæki_númer = INDEX; break; }
        }
        if (tæki_númer < 0) return false;
        int sjálfgildi = 설정읽기(tæki_númer, 0x10);
        if ((sjálfgildi & 1) == 0 || (sjálfgildi & 0xfffffffc) < 0x100 || (sjálfgildi & 0xfffffffc) > 65535) return false;
        입출력기준주소 = sjálfgildi & 0xfffc;
        int Skipun = 설정읽기(tæki_númer, 4);
        tæki_VALUE.입출력정수쓰기(0xcf8, 0x80000004 | (tæki_númer << 11));
        tæki_VALUE.입출력짧은수쓰기(0xcfc, Skipun | 5); // I/O 및 bus master leyfa_VALUE, PCI staða_VALUE_e10195a1 비트는 건드리지 않음
        tæki_VALUE.입출력바이트쓰기(입출력기준주소 + 0x52, 0);
        if (!Endurstilla_VALUE()) { 입출력기준주소 = 0; return false; }
        for (int INDEX = 0; INDEX < 6; INDEX++) tæki_slóð[INDEX] = tæki_VALUE.입출력바이트읽기(입출력기준주소 + INDEX);
        return true;
    }

    static boolean Endurstilla_VALUE() {
        tæki_VALUE.입출력바이트쓰기(입출력기준주소 + 0x37, 0x10);
        int Keyra_2 = tæki_VALUE.밀리초();
        while ((tæki_VALUE.입출력바이트읽기(입출력기준주소 + 0x37) & 0x10) != 0)
            if (tæki_VALUE.밀리초() - Keyra_2 > 100) return false;
        수신위치 = 0; 송신칸 = 0;
        tæki_VALUE.입출력정수쓰기(입출력기준주소 + 0x30, tæki_VALUE.Net_Minni());
        for (int INDEX = 0; INDEX < 4; INDEX++) tæki_VALUE.입출력정수쓰기(입출력기준주소 + 0x20 + INDEX * 4, tæki_VALUE.Net_Minni() + 12288);
        tæki_VALUE.입출력짧은수쓰기(입출력기준주소 + 0x3c, 0);
        tæki_VALUE.입출력짧은수쓰기(입출력기준주소 + 0x3e, 0xffff);
        tæki_VALUE.입출력바이트쓰기(입출력기준주소 + 0x37, 0x0c);
        tæki_VALUE.입출력정수쓰기(입출력기준주소 + 0x44, 0x0000e78a); // 자기주소/senda_út_VALUE, wrap 연속 Store_VALUE, 8KiB
        tæki_VALUE.입출력정수쓰기(입출력기준주소 + 0x40, 0x03000600);
        return true;
    }

    static int senda(int[] gögn, int lengd_VALUE) {
        if (입출력기준주소 == 0) return -19;
        if (lengd_VALUE < 14 || lengd_VALUE > 1514) return -90;
        int staða_gátt = 입출력기준주소 + 0x10 + 송신칸 * 4;
        int Keyra_2 = tæki_VALUE.밀리초();
        while ((tæki_VALUE.입출력정수읽기(staða_gátt) & 0x2000) == 0)
            if (tæki_VALUE.밀리초() - Keyra_2 > 100) return -110;
        int Stærð = lengd_VALUE < 60 ? 60 : lengd_VALUE;
        for (int INDEX = 0; INDEX < Stærð; INDEX++)
            tæki_VALUE.skrifa_Minni(tæki_VALUE.Net_Minni() + 12288 + INDEX, INDEX < lengd_VALUE ? gögn[INDEX] : 0);
        tæki_VALUE.입출력정수쓰기(staða_gátt, Stærð | 0x00080000);
        Keyra_2 = tæki_VALUE.밀리초();
        while ((tæki_VALUE.입출력정수읽기(staða_gátt) & 0xe0008000) == 0)
            if (tæki_VALUE.밀리초() - Keyra_2 > 100) return -110;
        if ((tæki_VALUE.입출력정수읽기(staða_gátt) & 0x8000) == 0) { villa_COUNT++; return -5; }
        송신칸 = (송신칸 + 1) & 3;
        송신수++;
        return lengd_VALUE;
    }

    static int 받기(int[] gögn) {
        if (입출력기준주소 == 0) return 0;
        if ((tæki_VALUE.입출력바이트읽기(입출력기준주소 + 0x3e) & 0x50) != 0) {
            villa_COUNT++;
            if (!Endurstilla_VALUE()) 입출력기준주소 = 0;
            return 0;
        }
        if ((tæki_VALUE.입출력바이트읽기(입출력기준주소 + 0x37) & 1) != 0) return 0;
        int 머리 = tæki_VALUE.Net_Minni() + 수신위치;
        int staða_VALUE_e10195a1 = 실행관리.짧은수(머리), Stærð = 실행관리.짧은수(머리 + 2);
        if (Stærð == 0xfff0) return 0; // DMA 진행 중
        if (Stærð < 4 || Stærð > 1518) {
            villa_COUNT++;
            if (!Endurstilla_VALUE()) 입출력기준주소 = 0;
            return 0;
        }
        int lengd_VALUE = Stærð - 4;
        if ((staða_VALUE_e10195a1 & 1) != 0) {
            for (int INDEX = 0; INDEX < lengd_VALUE; INDEX++) gögn[INDEX] = tæki_VALUE.기억읽기(머리 + 4 + INDEX);
            수신수++;
        } else { lengd_VALUE = 0; villa_COUNT++; }
        수신위치 = (수신위치 + Stærð + 4 + 3) & ~3;
        수신위치 &= 8191;
        tæki_VALUE.입출력짧은수쓰기(입출력기준주소 + 0x38, (수신위치 - 16) & 65535);
        tæki_VALUE.입출력짧은수쓰기(입출력기준주소 + 0x3e, 0x000f);
        return lengd_VALUE;
    }
}
