// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** PCI RTL8139 (10ec:8139), 단일 odoslať_VALUE 버퍼와 8KiB dostať_VALUE Loop_VALUE. 인터럽트 대신 폴링한다. */
public final class sieť_ovládač {
    static int 입출력기준주소 = 0;
    static int dostať_pozícia = 0, 송신칸 = 0;
    static int[] telefón_adresa = new int[6];
    static int 송신수 = 0, dostať_COUNT = 0, Chyba_COUNT = 0;

    static int 설정읽기(int 장치번호, int Pozícia) {
        telefón_VALUE.입출력정수쓰기(0xcf8, 0x80000000 | (장치번호 << 11) | Pozícia);
        return telefón_VALUE.입출력정수읽기(0xcfc);
    }

    static boolean Pripraviť() {
        int 장치번호 = -1;
        for (int INDEX = 0; INDEX < 32; INDEX++) {
            if (설정읽기(INDEX, 0) == 0x813910ec) { 장치번호 = INDEX; break; }
        }
        if (장치번호 < 0) return false;
        int predvolená_hodnota = 설정읽기(장치번호, 0x10);
        if ((predvolená_hodnota & 1) == 0 || (predvolená_hodnota & 0xfffffffc) < 0x100 || (predvolená_hodnota & 0xfffffffc) > 65535) return false;
        입출력기준주소 = predvolená_hodnota & 0xfffc;
        int Príkaz = 설정읽기(장치번호, 4);
        telefón_VALUE.입출력정수쓰기(0xcf8, 0x80000004 | (장치번호 << 11));
        telefón_VALUE.입출력짧은수쓰기(0xcfc, Príkaz | 5); // I/O 및 bus master Povoliť_VALUE, PCI Stav_VALUE 비트는 건드리지 않음
        telefón_VALUE.입출력바이트쓰기(입출력기준주소 + 0x52, 0);
        if (!reset_VALUE()) { 입출력기준주소 = 0; return false; }
        for (int INDEX = 0; INDEX < 6; INDEX++) telefón_adresa[INDEX] = telefón_VALUE.입출력바이트읽기(입출력기준주소 + INDEX);
        return true;
    }

    static boolean reset_VALUE() {
        telefón_VALUE.입출력바이트쓰기(입출력기준주소 + 0x37, 0x10);
        int Spustiť_2 = telefón_VALUE.밀리초();
        while ((telefón_VALUE.입출력바이트읽기(입출력기준주소 + 0x37) & 0x10) != 0)
            if (telefón_VALUE.밀리초() - Spustiť_2 > 100) return false;
        dostať_pozícia = 0; 송신칸 = 0;
        telefón_VALUE.입출력정수쓰기(입출력기준주소 + 0x30, telefón_VALUE.sieť_Pamäť());
        for (int INDEX = 0; INDEX < 4; INDEX++) telefón_VALUE.입출력정수쓰기(입출력기준주소 + 0x20 + INDEX * 4, telefón_VALUE.sieť_Pamäť() + 12288);
        telefón_VALUE.입출력짧은수쓰기(입출력기준주소 + 0x3c, 0);
        telefón_VALUE.입출력짧은수쓰기(입출력기준주소 + 0x3e, 0xffff);
        telefón_VALUE.입출력바이트쓰기(입출력기준주소 + 0x37, 0x0c);
        telefón_VALUE.입출력정수쓰기(입출력기준주소 + 0x44, 0x0000e78a); // 자기주소/vysielať_VALUE, wrap 연속 Store_VALUE, 8KiB
        telefón_VALUE.입출력정수쓰기(입출력기준주소 + 0x40, 0x03000600);
        return true;
    }

    static int odoslať(int[] údaje, int dĺžka_VALUE) {
        if (입출력기준주소 == 0) return -19;
        if (dĺžka_VALUE < 14 || dĺžka_VALUE > 1514) return -90;
        int stav_port = 입출력기준주소 + 0x10 + 송신칸 * 4;
        int Spustiť_2 = telefón_VALUE.밀리초();
        while ((telefón_VALUE.입출력정수읽기(stav_port) & 0x2000) == 0)
            if (telefón_VALUE.밀리초() - Spustiť_2 > 100) return -110;
        int Veľkosť = dĺžka_VALUE < 60 ? 60 : dĺžka_VALUE;
        for (int INDEX = 0; INDEX < Veľkosť; INDEX++)
            telefón_VALUE.zapísať_Pamäť(telefón_VALUE.sieť_Pamäť() + 12288 + INDEX, INDEX < dĺžka_VALUE ? údaje[INDEX] : 0);
        telefón_VALUE.입출력정수쓰기(stav_port, Veľkosť | 0x00080000);
        Spustiť_2 = telefón_VALUE.밀리초();
        while ((telefón_VALUE.입출력정수읽기(stav_port) & 0xe0008000) == 0)
            if (telefón_VALUE.밀리초() - Spustiť_2 > 100) return -110;
        if ((telefón_VALUE.입출력정수읽기(stav_port) & 0x8000) == 0) { Chyba_COUNT++; return -5; }
        송신칸 = (송신칸 + 1) & 3;
        송신수++;
        return dĺžka_VALUE;
    }

    static int dostať(int[] údaje) {
        if (입출력기준주소 == 0) return 0;
        if ((telefón_VALUE.입출력바이트읽기(입출력기준주소 + 0x3e) & 0x50) != 0) {
            Chyba_COUNT++;
            if (!reset_VALUE()) 입출력기준주소 = 0;
            return 0;
        }
        if ((telefón_VALUE.입출력바이트읽기(입출력기준주소 + 0x37) & 1) != 0) return 0;
        int 머리 = telefón_VALUE.sieť_Pamäť() + dostať_pozícia;
        int Stav_VALUE = 실행관리.짧은수(머리), Veľkosť = 실행관리.짧은수(머리 + 2);
        if (Veľkosť == 0xfff0) return 0; // DMA 진행 중
        if (Veľkosť < 4 || Veľkosť > 1518) {
            Chyba_COUNT++;
            if (!reset_VALUE()) 입출력기준주소 = 0;
            return 0;
        }
        int dĺžka_VALUE = Veľkosť - 4;
        if ((Stav_VALUE & 1) != 0) {
            for (int INDEX = 0; INDEX < dĺžka_VALUE; INDEX++) údaje[INDEX] = telefón_VALUE.기억읽기(머리 + 4 + INDEX);
            dostať_COUNT++;
        } else { dĺžka_VALUE = 0; Chyba_COUNT++; }
        dostať_pozícia = (dostať_pozícia + Veľkosť + 4 + 3) & ~3;
        dostať_pozícia &= 8191;
        telefón_VALUE.입출력짧은수쓰기(입출력기준주소 + 0x38, (dostať_pozícia - 16) & 65535);
        telefón_VALUE.입출력짧은수쓰기(입출력기준주소 + 0x3e, 0x000f);
        return dĺžka_VALUE;
    }
}
