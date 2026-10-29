// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** PCI RTL8139 (10ec:8139), 단일 wysłać_WARTOŚĆ 버퍼와 8KiB odbierać_WARTOŚĆ Loop_WARTOŚĆ. 인터럽트 대신 폴링한다. */
public final class sieć_sterownik {
    static int 입출력기준주소 = 0;
    static int odbierać_stanowisko = 0, 송신칸 = 0;
    static int[] urządzenie_ADRES = new int[6];
    static int 송신수 = 0, odbierać_ILE_LICZB = 0, błąd_ILE_LICZB = 0;

    static int 설정읽기(int urządzenie_identyfikator_c1e5bfa4, int pozycja) {
        urządzenie_WARTOŚĆ.입출력정수쓰기(0xcf8, 0x80000000 | (urządzenie_identyfikator_c1e5bfa4 << 11) | pozycja);
        return urządzenie_WARTOŚĆ.입출력정수읽기(0xcfc);
    }

    static boolean Przygotuj() {
        int urządzenie_identyfikator_c1e5bfa4 = -1;
        for (int INDEKS = 0; INDEKS < 32; INDEKS++) {
            if (설정읽기(INDEKS, 0) == 0x813910ec) { urządzenie_identyfikator_c1e5bfa4 = INDEKS; break; }
        }
        if (urządzenie_identyfikator_c1e5bfa4 < 0) return false;
        int wartość_domyślna = 설정읽기(urządzenie_identyfikator_c1e5bfa4, 0x10);
        if ((wartość_domyślna & 1) == 0 || (wartość_domyślna & 0xfffffffc) < 0x100 || (wartość_domyślna & 0xfffffffc) > 65535) return false;
        입출력기준주소 = wartość_domyślna & 0xfffc;
        int polecenie = 설정읽기(urządzenie_identyfikator_c1e5bfa4, 4);
        urządzenie_WARTOŚĆ.입출력정수쓰기(0xcf8, 0x80000004 | (urządzenie_identyfikator_c1e5bfa4 << 11));
        urządzenie_WARTOŚĆ.입출력짧은수쓰기(0xcfc, polecenie | 5); // I/O 및 bus master Zezwalaj_WARTOŚĆ, PCI Stan_WARTOŚĆ 비트는 건드리지 않음
        urządzenie_WARTOŚĆ.입출력바이트쓰기(입출력기준주소 + 0x52, 0);
        if (!resetować_WARTOŚĆ()) { 입출력기준주소 = 0; return false; }
        for (int INDEKS = 0; INDEKS < 6; INDEKS++) urządzenie_ADRES[INDEKS] = urządzenie_WARTOŚĆ.입출력바이트읽기(입출력기준주소 + INDEKS);
        return true;
    }

    static boolean resetować_WARTOŚĆ() {
        urządzenie_WARTOŚĆ.입출력바이트쓰기(입출력기준주소 + 0x37, 0x10);
        int Uruchom_2 = urządzenie_WARTOŚĆ.밀리초();
        while ((urządzenie_WARTOŚĆ.입출력바이트읽기(입출력기준주소 + 0x37) & 0x10) != 0)
            if (urządzenie_WARTOŚĆ.밀리초() - Uruchom_2 > 100) return false;
        odbierać_stanowisko = 0; 송신칸 = 0;
        urządzenie_WARTOŚĆ.입출력정수쓰기(입출력기준주소 + 0x30, urządzenie_WARTOŚĆ.sieć_Pamięć());
        for (int INDEKS = 0; INDEKS < 4; INDEKS++) urządzenie_WARTOŚĆ.입출력정수쓰기(입출력기준주소 + 0x20 + INDEKS * 4, urządzenie_WARTOŚĆ.sieć_Pamięć() + 12288);
        urządzenie_WARTOŚĆ.입출력짧은수쓰기(입출력기준주소 + 0x3c, 0);
        urządzenie_WARTOŚĆ.입출력짧은수쓰기(입출력기준주소 + 0x3e, 0xffff);
        urządzenie_WARTOŚĆ.입출력바이트쓰기(입출력기준주소 + 0x37, 0x0c);
        urządzenie_WARTOŚĆ.입출력정수쓰기(입출력기준주소 + 0x44, 0x0000e78a); // 자기주소/emisja_WARTOŚĆ, wrap 연속 Store_WARTOŚĆ, 8KiB
        urządzenie_WARTOŚĆ.입출력정수쓰기(입출력기준주소 + 0x40, 0x03000600);
        return true;
    }

    static int wysłać(int[] dane, int długość_WARTOŚĆ) {
        if (입출력기준주소 == 0) return -19;
        if (długość_WARTOŚĆ < 14 || długość_WARTOŚĆ > 1514) return -90;
        int stan_port = 입출력기준주소 + 0x10 + 송신칸 * 4;
        int Uruchom_2 = urządzenie_WARTOŚĆ.밀리초();
        while ((urządzenie_WARTOŚĆ.입출력정수읽기(stan_port) & 0x2000) == 0)
            if (urządzenie_WARTOŚĆ.밀리초() - Uruchom_2 > 100) return -110;
        int Rozmiar = długość_WARTOŚĆ < 60 ? 60 : długość_WARTOŚĆ;
        for (int INDEKS = 0; INDEKS < Rozmiar; INDEKS++)
            urządzenie_WARTOŚĆ.zapis_Pamięć(urządzenie_WARTOŚĆ.sieć_Pamięć() + 12288 + INDEKS, INDEKS < długość_WARTOŚĆ ? dane[INDEKS] : 0);
        urządzenie_WARTOŚĆ.입출력정수쓰기(stan_port, Rozmiar | 0x00080000);
        Uruchom_2 = urządzenie_WARTOŚĆ.밀리초();
        while ((urządzenie_WARTOŚĆ.입출력정수읽기(stan_port) & 0xe0008000) == 0)
            if (urządzenie_WARTOŚĆ.밀리초() - Uruchom_2 > 100) return -110;
        if ((urządzenie_WARTOŚĆ.입출력정수읽기(stan_port) & 0x8000) == 0) { błąd_ILE_LICZB++; return -5; }
        송신칸 = (송신칸 + 1) & 3;
        송신수++;
        return długość_WARTOŚĆ;
    }

    static int odbierać(int[] dane) {
        if (입출력기준주소 == 0) return 0;
        if ((urządzenie_WARTOŚĆ.입출력바이트읽기(입출력기준주소 + 0x3e) & 0x50) != 0) {
            błąd_ILE_LICZB++;
            if (!resetować_WARTOŚĆ()) 입출력기준주소 = 0;
            return 0;
        }
        if ((urządzenie_WARTOŚĆ.입출력바이트읽기(입출력기준주소 + 0x37) & 1) != 0) return 0;
        int 머리 = urządzenie_WARTOŚĆ.sieć_Pamięć() + odbierać_stanowisko;
        int Stan_WARTOŚĆ = wykonanie_Menedżer.짧은수(머리), Rozmiar = wykonanie_Menedżer.짧은수(머리 + 2);
        if (Rozmiar == 0xfff0) return 0; // DMA 진행 중
        if (Rozmiar < 4 || Rozmiar > 1518) {
            błąd_ILE_LICZB++;
            if (!resetować_WARTOŚĆ()) 입출력기준주소 = 0;
            return 0;
        }
        int długość_WARTOŚĆ = Rozmiar - 4;
        if ((Stan_WARTOŚĆ & 1) != 0) {
            for (int INDEKS = 0; INDEKS < długość_WARTOŚĆ; INDEKS++) dane[INDEKS] = urządzenie_WARTOŚĆ.기억읽기(머리 + 4 + INDEKS);
            odbierać_ILE_LICZB++;
        } else { długość_WARTOŚĆ = 0; błąd_ILE_LICZB++; }
        odbierać_stanowisko = (odbierać_stanowisko + Rozmiar + 4 + 3) & ~3;
        odbierać_stanowisko &= 8191;
        urządzenie_WARTOŚĆ.입출력짧은수쓰기(입출력기준주소 + 0x38, (odbierać_stanowisko - 16) & 65535);
        urządzenie_WARTOŚĆ.입출력짧은수쓰기(입출력기준주소 + 0x3e, 0x000f);
        return długość_WARTOŚĆ;
    }
}
