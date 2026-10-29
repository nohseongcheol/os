// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** PCI RTL8139 (10ec:8139), 단일 poslati_VALUE 버퍼와 8KiB 수신 Loop_VALUE. 인터럽트 대신 폴링한다. */
public final class Mreža_drajver_uređaja {
    static int 입출력기준주소 = 0;
    static int 수신위치 = 0, prenositi_prostor_za_unos = 0;
    static int[] uređaj_adresa = new int[6];
    static int prenositi_COUNT = 0, 수신수 = 0, greška_COUNT = 0;

    static int 설정읽기(int 장치번호, int Pozicija) {
        uređaj_VALUE.입출력정수쓰기(0xcf8, 0x80000000 | (장치번호 << 11) | Pozicija);
        return uređaj_VALUE.입출력정수읽기(0xcfc);
    }

    static boolean Pripremiti() {
        int 장치번호 = -1;
        for (int INDEX = 0; INDEX < 32; INDEX++) {
            if (설정읽기(INDEX, 0) == 0x813910ec) { 장치번호 = INDEX; break; }
        }
        if (장치번호 < 0) return false;
        int zadana_vrijednost = 설정읽기(장치번호, 0x10);
        if ((zadana_vrijednost & 1) == 0 || (zadana_vrijednost & 0xfffffffc) < 0x100 || (zadana_vrijednost & 0xfffffffc) > 65535) return false;
        입출력기준주소 = zadana_vrijednost & 0xfffc;
        int Naredba = 설정읽기(장치번호, 4);
        uređaj_VALUE.입출력정수쓰기(0xcf8, 0x80000004 | (장치번호 << 11));
        uređaj_VALUE.입출력짧은수쓰기(0xcfc, Naredba | 5); // I/O 및 bus master Dozvoliti_VALUE, PCI stanje_VALUE 비트는 건드리지 않음
        uređaj_VALUE.입출력바이트쓰기(입출력기준주소 + 0x52, 0);
        if (!vrati_VALUE()) { 입출력기준주소 = 0; return false; }
        for (int INDEX = 0; INDEX < 6; INDEX++) uređaj_adresa[INDEX] = uređaj_VALUE.입출력바이트읽기(입출력기준주소 + INDEX);
        return true;
    }

    static boolean vrati_VALUE() {
        uređaj_VALUE.입출력바이트쓰기(입출력기준주소 + 0x37, 0x10);
        int Pokreni = uređaj_VALUE.밀리초();
        while ((uređaj_VALUE.입출력바이트읽기(입출력기준주소 + 0x37) & 0x10) != 0)
            if (uređaj_VALUE.밀리초() - Pokreni > 100) return false;
        수신위치 = 0; prenositi_prostor_za_unos = 0;
        uređaj_VALUE.입출력정수쓰기(입출력기준주소 + 0x30, uređaj_VALUE.Mreža_Memorija());
        for (int INDEX = 0; INDEX < 4; INDEX++) uređaj_VALUE.입출력정수쓰기(입출력기준주소 + 0x20 + INDEX * 4, uređaj_VALUE.Mreža_Memorija() + 12288);
        uređaj_VALUE.입출력짧은수쓰기(입출력기준주소 + 0x3c, 0);
        uređaj_VALUE.입출력짧은수쓰기(입출력기준주소 + 0x3e, 0xffff);
        uređaj_VALUE.입출력바이트쓰기(입출력기준주소 + 0x37, 0x0c);
        uređaj_VALUE.입출력정수쓰기(입출력기준주소 + 0x44, 0x0000e78a); // 자기주소/emitirati_VALUE, wrap 연속 Store_VALUE, 8KiB
        uređaj_VALUE.입출력정수쓰기(입출력기준주소 + 0x40, 0x03000600);
        return true;
    }

    static int poslati(int[] podaci, int dužina_VALUE) {
        if (입출력기준주소 == 0) return -19;
        if (dužina_VALUE < 14 || dužina_VALUE > 1514) return -90;
        int stanje_port = 입출력기준주소 + 0x10 + prenositi_prostor_za_unos * 4;
        int Pokreni = uređaj_VALUE.밀리초();
        while ((uređaj_VALUE.입출력정수읽기(stanje_port) & 0x2000) == 0)
            if (uređaj_VALUE.밀리초() - Pokreni > 100) return -110;
        int Veličina = dužina_VALUE < 60 ? 60 : dužina_VALUE;
        for (int INDEX = 0; INDEX < Veličina; INDEX++)
            uređaj_VALUE.pisati_Memorija(uređaj_VALUE.Mreža_Memorija() + 12288 + INDEX, INDEX < dužina_VALUE ? podaci[INDEX] : 0);
        uređaj_VALUE.입출력정수쓰기(stanje_port, Veličina | 0x00080000);
        Pokreni = uređaj_VALUE.밀리초();
        while ((uređaj_VALUE.입출력정수읽기(stanje_port) & 0xe0008000) == 0)
            if (uređaj_VALUE.밀리초() - Pokreni > 100) return -110;
        if ((uređaj_VALUE.입출력정수읽기(stanje_port) & 0x8000) == 0) { greška_COUNT++; return -5; }
        prenositi_prostor_za_unos = (prenositi_prostor_za_unos + 1) & 3;
        prenositi_COUNT++;
        return dužina_VALUE;
    }

    static int 받기(int[] podaci) {
        if (입출력기준주소 == 0) return 0;
        if ((uređaj_VALUE.입출력바이트읽기(입출력기준주소 + 0x3e) & 0x50) != 0) {
            greška_COUNT++;
            if (!vrati_VALUE()) 입출력기준주소 = 0;
            return 0;
        }
        if ((uređaj_VALUE.입출력바이트읽기(입출력기준주소 + 0x37) & 1) != 0) return 0;
        int 머리 = uređaj_VALUE.Mreža_Memorija() + 수신위치;
        int stanje_VALUE = 실행관리.짧은수(머리), Veličina = 실행관리.짧은수(머리 + 2);
        if (Veličina == 0xfff0) return 0; // DMA 진행 중
        if (Veličina < 4 || Veličina > 1518) {
            greška_COUNT++;
            if (!vrati_VALUE()) 입출력기준주소 = 0;
            return 0;
        }
        int dužina_VALUE = Veličina - 4;
        if ((stanje_VALUE & 1) != 0) {
            for (int INDEX = 0; INDEX < dužina_VALUE; INDEX++) podaci[INDEX] = uređaj_VALUE.기억읽기(머리 + 4 + INDEX);
            수신수++;
        } else { dužina_VALUE = 0; greška_COUNT++; }
        수신위치 = (수신위치 + Veličina + 4 + 3) & ~3;
        수신위치 &= 8191;
        uređaj_VALUE.입출력짧은수쓰기(입출력기준주소 + 0x38, (수신위치 - 16) & 65535);
        uređaj_VALUE.입출력짧은수쓰기(입출력기준주소 + 0x3e, 0x000f);
        return dužina_VALUE;
    }
}
