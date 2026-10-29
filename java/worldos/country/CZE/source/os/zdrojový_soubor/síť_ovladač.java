// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** PCI RTL8139 (10ec:8139), 단일 poslat_HODNOTA 버퍼와 8KiB dostat_HODNOTA Loop_HODNOTA. 인터럽트 대신 폴링한다. */
public final class síť_ovladač {
    static int 입출력기준주소 = 0;
    static int dostat_pozice = 0, 송신칸 = 0;
    static int[] mobilní_ODKAZ = new int[6];
    static int 송신수 = 0, dostat_POČET = 0, chyba_POČET = 0;

    static int 설정읽기(int mobilní_číslo, int pozice) {
        mobilní_HODNOTA.입출력정수쓰기(0xcf8, 0x80000000 | (mobilní_číslo << 11) | pozice);
        return mobilní_HODNOTA.입출력정수읽기(0xcfc);
    }

    static boolean Připravit() {
        int mobilní_číslo = -1;
        for (int INDEX = 0; INDEX < 32; INDEX++) {
            if (설정읽기(INDEX, 0) == 0x813910ec) { mobilní_číslo = INDEX; break; }
        }
        if (mobilní_číslo < 0) return false;
        int výchozí_hodnota = 설정읽기(mobilní_číslo, 0x10);
        if ((výchozí_hodnota & 1) == 0 || (výchozí_hodnota & 0xfffffffc) < 0x100 || (výchozí_hodnota & 0xfffffffc) > 65535) return false;
        입출력기준주소 = výchozí_hodnota & 0xfffc;
        int příkaz = 설정읽기(mobilní_číslo, 4);
        mobilní_HODNOTA.입출력정수쓰기(0xcf8, 0x80000004 | (mobilní_číslo << 11));
        mobilní_HODNOTA.입출력짧은수쓰기(0xcfc, příkaz | 5); // I/O 및 bus master Povolit_HODNOTA, PCI Stav_HODNOTA 비트는 건드리지 않음
        mobilní_HODNOTA.입출력바이트쓰기(입출력기준주소 + 0x52, 0);
        if (!obnovit_HODNOTA()) { 입출력기준주소 = 0; return false; }
        for (int INDEX = 0; INDEX < 6; INDEX++) mobilní_ODKAZ[INDEX] = mobilní_HODNOTA.입출력바이트읽기(입출력기준주소 + INDEX);
        return true;
    }

    static boolean obnovit_HODNOTA() {
        mobilní_HODNOTA.입출력바이트쓰기(입출력기준주소 + 0x37, 0x10);
        int Spustit_2 = mobilní_HODNOTA.밀리초();
        while ((mobilní_HODNOTA.입출력바이트읽기(입출력기준주소 + 0x37) & 0x10) != 0)
            if (mobilní_HODNOTA.밀리초() - Spustit_2 > 100) return false;
        dostat_pozice = 0; 송신칸 = 0;
        mobilní_HODNOTA.입출력정수쓰기(입출력기준주소 + 0x30, mobilní_HODNOTA.síť_Paměť());
        for (int INDEX = 0; INDEX < 4; INDEX++) mobilní_HODNOTA.입출력정수쓰기(입출력기준주소 + 0x20 + INDEX * 4, mobilní_HODNOTA.síť_Paměť() + 12288);
        mobilní_HODNOTA.입출력짧은수쓰기(입출력기준주소 + 0x3c, 0);
        mobilní_HODNOTA.입출력짧은수쓰기(입출력기준주소 + 0x3e, 0xffff);
        mobilní_HODNOTA.입출력바이트쓰기(입출력기준주소 + 0x37, 0x0c);
        mobilní_HODNOTA.입출력정수쓰기(입출력기준주소 + 0x44, 0x0000e78a); // 자기주소/vysílat_HODNOTA, wrap 연속 Store_HODNOTA, 8KiB
        mobilní_HODNOTA.입출력정수쓰기(입출력기준주소 + 0x40, 0x03000600);
        return true;
    }

    static int poslat(int[] data, int délka_HODNOTA) {
        if (입출력기준주소 == 0) return -19;
        if (délka_HODNOTA < 14 || délka_HODNOTA > 1514) return -90;
        int stav_port = 입출력기준주소 + 0x10 + 송신칸 * 4;
        int Spustit_2 = mobilní_HODNOTA.밀리초();
        while ((mobilní_HODNOTA.입출력정수읽기(stav_port) & 0x2000) == 0)
            if (mobilní_HODNOTA.밀리초() - Spustit_2 > 100) return -110;
        int Velikost = délka_HODNOTA < 60 ? 60 : délka_HODNOTA;
        for (int INDEX = 0; INDEX < Velikost; INDEX++)
            mobilní_HODNOTA.zápis_Paměť(mobilní_HODNOTA.síť_Paměť() + 12288 + INDEX, INDEX < délka_HODNOTA ? data[INDEX] : 0);
        mobilní_HODNOTA.입출력정수쓰기(stav_port, Velikost | 0x00080000);
        Spustit_2 = mobilní_HODNOTA.밀리초();
        while ((mobilní_HODNOTA.입출력정수읽기(stav_port) & 0xe0008000) == 0)
            if (mobilní_HODNOTA.밀리초() - Spustit_2 > 100) return -110;
        if ((mobilní_HODNOTA.입출력정수읽기(stav_port) & 0x8000) == 0) { chyba_POČET++; return -5; }
        송신칸 = (송신칸 + 1) & 3;
        송신수++;
        return délka_HODNOTA;
    }

    static int dostat(int[] data) {
        if (입출력기준주소 == 0) return 0;
        if ((mobilní_HODNOTA.입출력바이트읽기(입출력기준주소 + 0x3e) & 0x50) != 0) {
            chyba_POČET++;
            if (!obnovit_HODNOTA()) 입출력기준주소 = 0;
            return 0;
        }
        if ((mobilní_HODNOTA.입출력바이트읽기(입출력기준주소 + 0x37) & 1) != 0) return 0;
        int 머리 = mobilní_HODNOTA.síť_Paměť() + dostat_pozice;
        int Stav_HODNOTA = spuštění_Správce.짧은수(머리), Velikost = spuštění_Správce.짧은수(머리 + 2);
        if (Velikost == 0xfff0) return 0; // DMA 진행 중
        if (Velikost < 4 || Velikost > 1518) {
            chyba_POČET++;
            if (!obnovit_HODNOTA()) 입출력기준주소 = 0;
            return 0;
        }
        int délka_HODNOTA = Velikost - 4;
        if ((Stav_HODNOTA & 1) != 0) {
            for (int INDEX = 0; INDEX < délka_HODNOTA; INDEX++) data[INDEX] = mobilní_HODNOTA.기억읽기(머리 + 4 + INDEX);
            dostat_POČET++;
        } else { délka_HODNOTA = 0; chyba_POČET++; }
        dostat_pozice = (dostat_pozice + Velikost + 4 + 3) & ~3;
        dostat_pozice &= 8191;
        mobilní_HODNOTA.입출력짧은수쓰기(입출력기준주소 + 0x38, (dostat_pozice - 16) & 65535);
        mobilní_HODNOTA.입출력짧은수쓰기(입출력기준주소 + 0x3e, 0x000f);
        return délka_HODNOTA;
    }
}
