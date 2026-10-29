// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** PCI RTL8139 (10ec:8139), 단일 siųsti_VALUE 버퍼와 8KiB gauti_VALUE_cef4d8ab Loop_VALUE. 인터럽트 대신 폴링한다. */
public final class tinklas_tvarkyklė {
    static int 입출력기준주소 = 0;
    static int gauti_padėtis = 0, 송신칸 = 0;
    static int[] įrenginys_ADDRESS = new int[6];
    static int 송신수 = 0, gauti_COUNT = 0, 오류수 = 0;

    static int 설정읽기(int įrenginys_numeris, int Pozicija) {
        įrenginys_VALUE.입출력정수쓰기(0xcf8, 0x80000000 | (įrenginys_numeris << 11) | Pozicija);
        return įrenginys_VALUE.입출력정수읽기(0xcfc);
    }

    static boolean Parengti() {
        int įrenginys_numeris = -1;
        for (int INDEX = 0; INDEX < 32; INDEX++) {
            if (설정읽기(INDEX, 0) == 0x813910ec) { įrenginys_numeris = INDEX; break; }
        }
        if (įrenginys_numeris < 0) return false;
        int numatytoji_reikšmė = 설정읽기(įrenginys_numeris, 0x10);
        if ((numatytoji_reikšmė & 1) == 0 || (numatytoji_reikšmė & 0xfffffffc) < 0x100 || (numatytoji_reikšmė & 0xfffffffc) > 65535) return false;
        입출력기준주소 = numatytoji_reikšmė & 0xfffc;
        int Komanda = 설정읽기(įrenginys_numeris, 4);
        įrenginys_VALUE.입출력정수쓰기(0xcf8, 0x80000004 | (įrenginys_numeris << 11));
        įrenginys_VALUE.입출력짧은수쓰기(0xcfc, Komanda | 5); // I/O 및 bus master Leisti_VALUE, PCI Būsena_VALUE 비트는 건드리지 않음
        įrenginys_VALUE.입출력바이트쓰기(입출력기준주소 + 0x52, 0);
        if (!atkurti_VALUE()) { 입출력기준주소 = 0; return false; }
        for (int INDEX = 0; INDEX < 6; INDEX++) įrenginys_ADDRESS[INDEX] = įrenginys_VALUE.입출력바이트읽기(입출력기준주소 + INDEX);
        return true;
    }

    static boolean atkurti_VALUE() {
        įrenginys_VALUE.입출력바이트쓰기(입출력기준주소 + 0x37, 0x10);
        int Paleisti = įrenginys_VALUE.밀리초();
        while ((įrenginys_VALUE.입출력바이트읽기(입출력기준주소 + 0x37) & 0x10) != 0)
            if (įrenginys_VALUE.밀리초() - Paleisti > 100) return false;
        gauti_padėtis = 0; 송신칸 = 0;
        įrenginys_VALUE.입출력정수쓰기(입출력기준주소 + 0x30, įrenginys_VALUE.tinklas_atmintis());
        for (int INDEX = 0; INDEX < 4; INDEX++) įrenginys_VALUE.입출력정수쓰기(입출력기준주소 + 0x20 + INDEX * 4, įrenginys_VALUE.tinklas_atmintis() + 12288);
        įrenginys_VALUE.입출력짧은수쓰기(입출력기준주소 + 0x3c, 0);
        įrenginys_VALUE.입출력짧은수쓰기(입출력기준주소 + 0x3e, 0xffff);
        įrenginys_VALUE.입출력바이트쓰기(입출력기준주소 + 0x37, 0x0c);
        įrenginys_VALUE.입출력정수쓰기(입출력기준주소 + 0x44, 0x0000e78a); // 자기주소/transliuoti_VALUE, wrap 연속 Store_VALUE, 8KiB
        įrenginys_VALUE.입출력정수쓰기(입출력기준주소 + 0x40, 0x03000600);
        return true;
    }

    static int siųsti(int[] duomenys, int 길이) {
        if (입출력기준주소 == 0) return -19;
        if (길이 < 14 || 길이 > 1514) return -90;
        int būsena_jungtis = 입출력기준주소 + 0x10 + 송신칸 * 4;
        int Paleisti = įrenginys_VALUE.밀리초();
        while ((įrenginys_VALUE.입출력정수읽기(būsena_jungtis) & 0x2000) == 0)
            if (įrenginys_VALUE.밀리초() - Paleisti > 100) return -110;
        int Dydis = 길이 < 60 ? 60 : 길이;
        for (int INDEX = 0; INDEX < Dydis; INDEX++)
            įrenginys_VALUE.rašymas_atmintis(įrenginys_VALUE.tinklas_atmintis() + 12288 + INDEX, INDEX < 길이 ? duomenys[INDEX] : 0);
        įrenginys_VALUE.입출력정수쓰기(būsena_jungtis, Dydis | 0x00080000);
        Paleisti = įrenginys_VALUE.밀리초();
        while ((įrenginys_VALUE.입출력정수읽기(būsena_jungtis) & 0xe0008000) == 0)
            if (įrenginys_VALUE.밀리초() - Paleisti > 100) return -110;
        if ((įrenginys_VALUE.입출력정수읽기(būsena_jungtis) & 0x8000) == 0) { 오류수++; return -5; }
        송신칸 = (송신칸 + 1) & 3;
        송신수++;
        return 길이;
    }

    static int gauti(int[] duomenys) {
        if (입출력기준주소 == 0) return 0;
        if ((įrenginys_VALUE.입출력바이트읽기(입출력기준주소 + 0x3e) & 0x50) != 0) {
            오류수++;
            if (!atkurti_VALUE()) 입출력기준주소 = 0;
            return 0;
        }
        if ((įrenginys_VALUE.입출력바이트읽기(입출력기준주소 + 0x37) & 1) != 0) return 0;
        int 머리 = įrenginys_VALUE.tinklas_atmintis() + gauti_padėtis;
        int Būsena_VALUE = 실행관리.짧은수(머리), Dydis = 실행관리.짧은수(머리 + 2);
        if (Dydis == 0xfff0) return 0; // DMA 진행 중
        if (Dydis < 4 || Dydis > 1518) {
            오류수++;
            if (!atkurti_VALUE()) 입출력기준주소 = 0;
            return 0;
        }
        int 길이 = Dydis - 4;
        if ((Būsena_VALUE & 1) != 0) {
            for (int INDEX = 0; INDEX < 길이; INDEX++) duomenys[INDEX] = įrenginys_VALUE.기억읽기(머리 + 4 + INDEX);
            gauti_COUNT++;
        } else { 길이 = 0; 오류수++; }
        gauti_padėtis = (gauti_padėtis + Dydis + 4 + 3) & ~3;
        gauti_padėtis &= 8191;
        įrenginys_VALUE.입출력짧은수쓰기(입출력기준주소 + 0x38, (gauti_padėtis - 16) & 65535);
        įrenginys_VALUE.입출력짧은수쓰기(입출력기준주소 + 0x3e, 0x000f);
        return 길이;
    }
}
