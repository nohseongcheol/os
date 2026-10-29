// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** PCI RTL8139 (10ec:8139), 단일 trimite_VALUE 버퍼와 8KiB primi_VALUE Loop_VALUE. 인터럽트 대신 폴링한다. */
public final class rețea_driver {
    static int 입출력기준주소 = 0;
    static int primi_poziție = 0, 송신칸 = 0;
    static int[] mobil_adresa = new int[6];
    static int 송신수 = 0, primi_COUNT = 0, eroare_COUNT = 0;

    static int 설정읽기(int 장치번호, int Poziție) {
        mobil_VALUE.입출력정수쓰기(0xcf8, 0x80000000 | (장치번호 << 11) | Poziție);
        return mobil_VALUE.입출력정수읽기(0xcfc);
    }

    static boolean Pregătiți() {
        int 장치번호 = -1;
        for (int INDEX = 0; INDEX < 32; INDEX++) {
            if (설정읽기(INDEX, 0) == 0x813910ec) { 장치번호 = INDEX; break; }
        }
        if (장치번호 < 0) return false;
        int valoare_implicită = 설정읽기(장치번호, 0x10);
        if ((valoare_implicită & 1) == 0 || (valoare_implicită & 0xfffffffc) < 0x100 || (valoare_implicită & 0xfffffffc) > 65535) return false;
        입출력기준주소 = valoare_implicită & 0xfffc;
        int Comandă = 설정읽기(장치번호, 4);
        mobil_VALUE.입출력정수쓰기(0xcf8, 0x80000004 | (장치번호 << 11));
        mobil_VALUE.입출력짧은수쓰기(0xcfc, Comandă | 5); // I/O 및 bus master permite_VALUE, PCI Stare_VALUE 비트는 건드리지 않음
        mobil_VALUE.입출력바이트쓰기(입출력기준주소 + 0x52, 0);
        if (!reseta_VALUE()) { 입출력기준주소 = 0; return false; }
        for (int INDEX = 0; INDEX < 6; INDEX++) mobil_adresa[INDEX] = mobil_VALUE.입출력바이트읽기(입출력기준주소 + INDEX);
        return true;
    }

    static boolean reseta_VALUE() {
        mobil_VALUE.입출력바이트쓰기(입출력기준주소 + 0x37, 0x10);
        int Pornește = mobil_VALUE.밀리초();
        while ((mobil_VALUE.입출력바이트읽기(입출력기준주소 + 0x37) & 0x10) != 0)
            if (mobil_VALUE.밀리초() - Pornește > 100) return false;
        primi_poziție = 0; 송신칸 = 0;
        mobil_VALUE.입출력정수쓰기(입출력기준주소 + 0x30, mobil_VALUE.rețea_Memorie());
        for (int INDEX = 0; INDEX < 4; INDEX++) mobil_VALUE.입출력정수쓰기(입출력기준주소 + 0x20 + INDEX * 4, mobil_VALUE.rețea_Memorie() + 12288);
        mobil_VALUE.입출력짧은수쓰기(입출력기준주소 + 0x3c, 0);
        mobil_VALUE.입출력짧은수쓰기(입출력기준주소 + 0x3e, 0xffff);
        mobil_VALUE.입출력바이트쓰기(입출력기준주소 + 0x37, 0x0c);
        mobil_VALUE.입출력정수쓰기(입출력기준주소 + 0x44, 0x0000e78a); // 자기주소/difuza_VALUE, wrap 연속 Store_VALUE, 8KiB
        mobil_VALUE.입출력정수쓰기(입출력기준주소 + 0x40, 0x03000600);
        return true;
    }

    static int trimite(int[] date, int lungime_VALUE) {
        if (입출력기준주소 == 0) return -19;
        if (lungime_VALUE < 14 || lungime_VALUE > 1514) return -90;
        int stare_muta = 입출력기준주소 + 0x10 + 송신칸 * 4;
        int Pornește = mobil_VALUE.밀리초();
        while ((mobil_VALUE.입출력정수읽기(stare_muta) & 0x2000) == 0)
            if (mobil_VALUE.밀리초() - Pornește > 100) return -110;
        int Mărime = lungime_VALUE < 60 ? 60 : lungime_VALUE;
        for (int INDEX = 0; INDEX < Mărime; INDEX++)
            mobil_VALUE.scriere_Memorie(mobil_VALUE.rețea_Memorie() + 12288 + INDEX, INDEX < lungime_VALUE ? date[INDEX] : 0);
        mobil_VALUE.입출력정수쓰기(stare_muta, Mărime | 0x00080000);
        Pornește = mobil_VALUE.밀리초();
        while ((mobil_VALUE.입출력정수읽기(stare_muta) & 0xe0008000) == 0)
            if (mobil_VALUE.밀리초() - Pornește > 100) return -110;
        if ((mobil_VALUE.입출력정수읽기(stare_muta) & 0x8000) == 0) { eroare_COUNT++; return -5; }
        송신칸 = (송신칸 + 1) & 3;
        송신수++;
        return lungime_VALUE;
    }

    static int primi(int[] date) {
        if (입출력기준주소 == 0) return 0;
        if ((mobil_VALUE.입출력바이트읽기(입출력기준주소 + 0x3e) & 0x50) != 0) {
            eroare_COUNT++;
            if (!reseta_VALUE()) 입출력기준주소 = 0;
            return 0;
        }
        if ((mobil_VALUE.입출력바이트읽기(입출력기준주소 + 0x37) & 1) != 0) return 0;
        int 머리 = mobil_VALUE.rețea_Memorie() + primi_poziție;
        int Stare_VALUE = 실행관리.짧은수(머리), Mărime = 실행관리.짧은수(머리 + 2);
        if (Mărime == 0xfff0) return 0; // DMA 진행 중
        if (Mărime < 4 || Mărime > 1518) {
            eroare_COUNT++;
            if (!reseta_VALUE()) 입출력기준주소 = 0;
            return 0;
        }
        int lungime_VALUE = Mărime - 4;
        if ((Stare_VALUE & 1) != 0) {
            for (int INDEX = 0; INDEX < lungime_VALUE; INDEX++) date[INDEX] = mobil_VALUE.기억읽기(머리 + 4 + INDEX);
            primi_COUNT++;
        } else { lungime_VALUE = 0; eroare_COUNT++; }
        primi_poziție = (primi_poziție + Mărime + 4 + 3) & ~3;
        primi_poziție &= 8191;
        mobil_VALUE.입출력짧은수쓰기(입출력기준주소 + 0x38, (primi_poziție - 16) & 65535);
        mobil_VALUE.입출력짧은수쓰기(입출력기준주소 + 0x3e, 0x000f);
        return lungime_VALUE;
    }
}
