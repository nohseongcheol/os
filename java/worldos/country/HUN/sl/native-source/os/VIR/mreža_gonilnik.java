// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** PCI RTL8139 (10ec:8139), 단일 poslati_VALUE 버퍼와 8KiB sprejeti_sprejemati_prejeti_prejemati_VALUE Loop_VALUE. 인터럽트 대신 폴링한다. */
public final class mreža_gonilnik {
    static int 입출력기준주소 = 0;
    static int sprejeti_sprejemati_prejeti_prejemati_položaj = 0, 송신칸 = 0;
    static int[] naprava_naslov = new int[6];
    static int 송신수 = 0, sprejeti_sprejemati_prejeti_prejemati_COUNT = 0, 오류수 = 0;

    static int 설정읽기(int 장치번호, int Položaj) {
        naprava_VALUE.입출력정수쓰기(0xcf8, 0x80000000 | (장치번호 << 11) | Položaj);
        return naprava_VALUE.입출력정수읽기(0xcfc);
    }

    static boolean Pripravi() {
        int 장치번호 = -1;
        for (int INDEX = 0; INDEX < 32; INDEX++) {
            if (설정읽기(INDEX, 0) == 0x813910ec) { 장치번호 = INDEX; break; }
        }
        if (장치번호 < 0) return false;
        int privzeta_vrednost = 설정읽기(장치번호, 0x10);
        if ((privzeta_vrednost & 1) == 0 || (privzeta_vrednost & 0xfffffffc) < 0x100 || (privzeta_vrednost & 0xfffffffc) > 65535) return false;
        입출력기준주소 = privzeta_vrednost & 0xfffc;
        int Ukaz = 설정읽기(장치번호, 4);
        naprava_VALUE.입출력정수쓰기(0xcf8, 0x80000004 | (장치번호 << 11));
        naprava_VALUE.입출력짧은수쓰기(0xcfc, Ukaz | 5); // I/O 및 bus master Dovoli_VALUE, PCI stanje_VALUE 비트는 건드리지 않음
        naprava_VALUE.입출력바이트쓰기(입출력기준주소 + 0x52, 0);
        if (!ponastavi_VALUE()) { 입출력기준주소 = 0; return false; }
        for (int INDEX = 0; INDEX < 6; INDEX++) naprava_naslov[INDEX] = naprava_VALUE.입출력바이트읽기(입출력기준주소 + INDEX);
        return true;
    }

    static boolean ponastavi_VALUE() {
        naprava_VALUE.입출력바이트쓰기(입출력기준주소 + 0x37, 0x10);
        int Zaženi = naprava_VALUE.밀리초();
        while ((naprava_VALUE.입출력바이트읽기(입출력기준주소 + 0x37) & 0x10) != 0)
            if (naprava_VALUE.밀리초() - Zaženi > 100) return false;
        sprejeti_sprejemati_prejeti_prejemati_položaj = 0; 송신칸 = 0;
        naprava_VALUE.입출력정수쓰기(입출력기준주소 + 0x30, naprava_VALUE.mreža_pomnilnik());
        for (int INDEX = 0; INDEX < 4; INDEX++) naprava_VALUE.입출력정수쓰기(입출력기준주소 + 0x20 + INDEX * 4, naprava_VALUE.mreža_pomnilnik() + 12288);
        naprava_VALUE.입출력짧은수쓰기(입출력기준주소 + 0x3c, 0);
        naprava_VALUE.입출력짧은수쓰기(입출력기준주소 + 0x3e, 0xffff);
        naprava_VALUE.입출력바이트쓰기(입출력기준주소 + 0x37, 0x0c);
        naprava_VALUE.입출력정수쓰기(입출력기준주소 + 0x44, 0x0000e78a); // 자기주소/oddaja_VALUE, wrap 연속 Store_VALUE, 8KiB
        naprava_VALUE.입출력정수쓰기(입출력기준주소 + 0x40, 0x03000600);
        return true;
    }

    static int poslati(int[] podatki, int 길이) {
        if (입출력기준주소 == 0) return -19;
        if (길이 < 14 || 길이 > 1514) return -90;
        int stanje_vrata = 입출력기준주소 + 0x10 + 송신칸 * 4;
        int Zaženi = naprava_VALUE.밀리초();
        while ((naprava_VALUE.입출력정수읽기(stanje_vrata) & 0x2000) == 0)
            if (naprava_VALUE.밀리초() - Zaženi > 100) return -110;
        int Velikost = 길이 < 60 ? 60 : 길이;
        for (int INDEX = 0; INDEX < Velikost; INDEX++)
            naprava_VALUE.pisati_pomnilnik(naprava_VALUE.mreža_pomnilnik() + 12288 + INDEX, INDEX < 길이 ? podatki[INDEX] : 0);
        naprava_VALUE.입출력정수쓰기(stanje_vrata, Velikost | 0x00080000);
        Zaženi = naprava_VALUE.밀리초();
        while ((naprava_VALUE.입출력정수읽기(stanje_vrata) & 0xe0008000) == 0)
            if (naprava_VALUE.밀리초() - Zaženi > 100) return -110;
        if ((naprava_VALUE.입출력정수읽기(stanje_vrata) & 0x8000) == 0) { 오류수++; return -5; }
        송신칸 = (송신칸 + 1) & 3;
        송신수++;
        return 길이;
    }

    static int sprejeti_sprejemati_prejeti_prejemati(int[] podatki) {
        if (입출력기준주소 == 0) return 0;
        if ((naprava_VALUE.입출력바이트읽기(입출력기준주소 + 0x3e) & 0x50) != 0) {
            오류수++;
            if (!ponastavi_VALUE()) 입출력기준주소 = 0;
            return 0;
        }
        if ((naprava_VALUE.입출력바이트읽기(입출력기준주소 + 0x37) & 1) != 0) return 0;
        int 머리 = naprava_VALUE.mreža_pomnilnik() + sprejeti_sprejemati_prejeti_prejemati_položaj;
        int stanje_VALUE = 실행관리.짧은수(머리), Velikost = 실행관리.짧은수(머리 + 2);
        if (Velikost == 0xfff0) return 0; // DMA 진행 중
        if (Velikost < 4 || Velikost > 1518) {
            오류수++;
            if (!ponastavi_VALUE()) 입출력기준주소 = 0;
            return 0;
        }
        int 길이 = Velikost - 4;
        if ((stanje_VALUE & 1) != 0) {
            for (int INDEX = 0; INDEX < 길이; INDEX++) podatki[INDEX] = naprava_VALUE.기억읽기(머리 + 4 + INDEX);
            sprejeti_sprejemati_prejeti_prejemati_COUNT++;
        } else { 길이 = 0; 오류수++; }
        sprejeti_sprejemati_prejeti_prejemati_položaj = (sprejeti_sprejemati_prejeti_prejemati_položaj + Velikost + 4 + 3) & ~3;
        sprejeti_sprejemati_prejeti_prejemati_položaj &= 8191;
        naprava_VALUE.입출력짧은수쓰기(입출력기준주소 + 0x38, (sprejeti_sprejemati_prejeti_prejemati_položaj - 16) & 65535);
        naprava_VALUE.입출력짧은수쓰기(입출력기준주소 + 0x3e, 0x000f);
        return 길이;
    }
}
