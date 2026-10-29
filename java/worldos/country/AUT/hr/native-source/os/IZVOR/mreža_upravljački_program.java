// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** PCI RTL8139 (10ec:8139), 단일 slati_VALUE 버퍼와 8KiB primiti_VALUE Loop_VALUE. 인터럽트 대신 폴링한다. */
public final class mreža_upravljački_program {
    static int 입출력기준주소 = 0;
    static int primiti_položaj = 0, 송신칸 = 0;
    static int[] uređaj_adresa = new int[6];
    static int 송신수 = 0, primiti_COUNT = 0, pogreška_COUNT = 0;

    static int 설정읽기(int 장치번호, int Položaj) {
        uređaj_VALUE.입출력정수쓰기(0xcf8, 0x80000000 | (장치번호 << 11) | Položaj);
        return uređaj_VALUE.입출력정수읽기(0xcfc);
    }

    static boolean Pripremi() {
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
        uređaj_VALUE.입출력짧은수쓰기(0xcfc, Naredba | 5); // I/O 및 bus master Dopusti_VALUE, PCI Stanje_VALUE 비트는 건드리지 않음
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
        primiti_položaj = 0; 송신칸 = 0;
        uređaj_VALUE.입출력정수쓰기(입출력기준주소 + 0x30, uređaj_VALUE.mreža_Memorija());
        for (int INDEX = 0; INDEX < 4; INDEX++) uređaj_VALUE.입출력정수쓰기(입출력기준주소 + 0x20 + INDEX * 4, uređaj_VALUE.mreža_Memorija() + 12288);
        uređaj_VALUE.입출력짧은수쓰기(입출력기준주소 + 0x3c, 0);
        uređaj_VALUE.입출력짧은수쓰기(입출력기준주소 + 0x3e, 0xffff);
        uređaj_VALUE.입출력바이트쓰기(입출력기준주소 + 0x37, 0x0c);
        uređaj_VALUE.입출력정수쓰기(입출력기준주소 + 0x44, 0x0000e78a); // 자기주소/emitirati_VALUE, wrap 연속 Store_VALUE, 8KiB
        uređaj_VALUE.입출력정수쓰기(입출력기준주소 + 0x40, 0x03000600);
        return true;
    }

    static int slati(int[] podaci, int 길이) {
        if (입출력기준주소 == 0) return -19;
        if (길이 < 14 || 길이 > 1514) return -90;
        int stanje_prebaciti = 입출력기준주소 + 0x10 + 송신칸 * 4;
        int Pokreni = uređaj_VALUE.밀리초();
        while ((uređaj_VALUE.입출력정수읽기(stanje_prebaciti) & 0x2000) == 0)
            if (uređaj_VALUE.밀리초() - Pokreni > 100) return -110;
        int Veličina = 길이 < 60 ? 60 : 길이;
        for (int INDEX = 0; INDEX < Veličina; INDEX++)
            uređaj_VALUE.zapisivanje_Memorija(uređaj_VALUE.mreža_Memorija() + 12288 + INDEX, INDEX < 길이 ? podaci[INDEX] : 0);
        uređaj_VALUE.입출력정수쓰기(stanje_prebaciti, Veličina | 0x00080000);
        Pokreni = uređaj_VALUE.밀리초();
        while ((uređaj_VALUE.입출력정수읽기(stanje_prebaciti) & 0xe0008000) == 0)
            if (uređaj_VALUE.밀리초() - Pokreni > 100) return -110;
        if ((uređaj_VALUE.입출력정수읽기(stanje_prebaciti) & 0x8000) == 0) { pogreška_COUNT++; return -5; }
        송신칸 = (송신칸 + 1) & 3;
        송신수++;
        return 길이;
    }

    static int primiti(int[] podaci) {
        if (입출력기준주소 == 0) return 0;
        if ((uređaj_VALUE.입출력바이트읽기(입출력기준주소 + 0x3e) & 0x50) != 0) {
            pogreška_COUNT++;
            if (!vrati_VALUE()) 입출력기준주소 = 0;
            return 0;
        }
        if ((uređaj_VALUE.입출력바이트읽기(입출력기준주소 + 0x37) & 1) != 0) return 0;
        int 머리 = uređaj_VALUE.mreža_Memorija() + primiti_položaj;
        int Stanje_VALUE = 실행관리.짧은수(머리), Veličina = 실행관리.짧은수(머리 + 2);
        if (Veličina == 0xfff0) return 0; // DMA 진행 중
        if (Veličina < 4 || Veličina > 1518) {
            pogreška_COUNT++;
            if (!vrati_VALUE()) 입출력기준주소 = 0;
            return 0;
        }
        int 길이 = Veličina - 4;
        if ((Stanje_VALUE & 1) != 0) {
            for (int INDEX = 0; INDEX < 길이; INDEX++) podaci[INDEX] = uređaj_VALUE.기억읽기(머리 + 4 + INDEX);
            primiti_COUNT++;
        } else { 길이 = 0; pogreška_COUNT++; }
        primiti_položaj = (primiti_položaj + Veličina + 4 + 3) & ~3;
        primiti_položaj &= 8191;
        uređaj_VALUE.입출력짧은수쓰기(입출력기준주소 + 0x38, (primiti_položaj - 16) & 65535);
        uređaj_VALUE.입출력짧은수쓰기(입출력기준주소 + 0x3e, 0x000f);
        return 길이;
    }
}
