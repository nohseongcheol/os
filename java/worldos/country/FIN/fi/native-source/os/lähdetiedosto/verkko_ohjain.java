// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** PCI RTL8139 (10ec:8139), 단일 lähettää_ARVO 버퍼와 8KiB saada_ARVO Loop_ARVO. 인터럽트 대신 폴링한다. */
public final class verkko_ohjain {
    static int 입출력기준주소 = 0;
    static int saada_toimi_0ac41e06 = 0, lähettää_paikka = 0;
    static int[] laite_OSOITE = new int[6];
    static int lähettää_LASKE = 0, saada_LASKE = 0, virhe_LASKE = 0;

    static int lukea_Asetukset(int laite_numero, int paikka) {
        laite_ARVO.입출력정수쓰기(0xcf8, 0x80000000 | (laite_numero << 11) | paikka);
        return laite_ARVO.입출력정수읽기(0xcfc);
    }

    static boolean Valmistele() {
        int laite_numero = -1;
        for (int INDEKSI = 0; INDEKSI < 32; INDEKSI++) {
            if (lukea_Asetukset(INDEKSI, 0) == 0x813910ec) { laite_numero = INDEKSI; break; }
        }
        if (laite_numero < 0) return false;
        int oletusarvo = lukea_Asetukset(laite_numero, 0x10);
        if ((oletusarvo & 1) == 0 || (oletusarvo & 0xfffffffc) < 0x100 || (oletusarvo & 0xfffffffc) > 65535) return false;
        입출력기준주소 = oletusarvo & 0xfffc;
        int komento = lukea_Asetukset(laite_numero, 4);
        laite_ARVO.입출력정수쓰기(0xcf8, 0x80000004 | (laite_numero << 11));
        laite_ARVO.입출력짧은수쓰기(0xcfc, komento | 5); // I/O 및 bus master Salli_ARVO, PCI Tila_ARVO 비트는 건드리지 않음
        laite_ARVO.입출력바이트쓰기(입출력기준주소 + 0x52, 0);
        if (!nollata_ARVO()) { 입출력기준주소 = 0; return false; }
        for (int INDEKSI = 0; INDEKSI < 6; INDEKSI++) laite_OSOITE[INDEKSI] = laite_ARVO.입출력바이트읽기(입출력기준주소 + INDEKSI);
        return true;
    }

    static boolean nollata_ARVO() {
        laite_ARVO.입출력바이트쓰기(입출력기준주소 + 0x37, 0x10);
        int Suorita_2 = laite_ARVO.밀리초();
        while ((laite_ARVO.입출력바이트읽기(입출력기준주소 + 0x37) & 0x10) != 0)
            if (laite_ARVO.밀리초() - Suorita_2 > 100) return false;
        saada_toimi_0ac41e06 = 0; lähettää_paikka = 0;
        laite_ARVO.입출력정수쓰기(입출력기준주소 + 0x30, laite_ARVO.verkko_Muisti());
        for (int INDEKSI = 0; INDEKSI < 4; INDEKSI++) laite_ARVO.입출력정수쓰기(입출력기준주소 + 0x20 + INDEKSI * 4, laite_ARVO.verkko_Muisti() + 12288);
        laite_ARVO.입출력짧은수쓰기(입출력기준주소 + 0x3c, 0);
        laite_ARVO.입출력짧은수쓰기(입출력기준주소 + 0x3e, 0xffff);
        laite_ARVO.입출력바이트쓰기(입출력기준주소 + 0x37, 0x0c);
        laite_ARVO.입출력정수쓰기(입출력기준주소 + 0x44, 0x0000e78a); // 자기주소/lähetä_ARVO, wrap 연속 Store_ARVO, 8KiB
        laite_ARVO.입출력정수쓰기(입출력기준주소 + 0x40, 0x03000600);
        return true;
    }

    static int lähettää(int[] data, int kesto_ARVO) {
        if (입출력기준주소 == 0) return -19;
        if (kesto_ARVO < 14 || kesto_ARVO > 1514) return -90;
        int tila_portti = 입출력기준주소 + 0x10 + lähettää_paikka * 4;
        int Suorita_2 = laite_ARVO.밀리초();
        while ((laite_ARVO.입출력정수읽기(tila_portti) & 0x2000) == 0)
            if (laite_ARVO.밀리초() - Suorita_2 > 100) return -110;
        int Koko = kesto_ARVO < 60 ? 60 : kesto_ARVO;
        for (int INDEKSI = 0; INDEKSI < Koko; INDEKSI++)
            laite_ARVO.kirjoitus_Muisti(laite_ARVO.verkko_Muisti() + 12288 + INDEKSI, INDEKSI < kesto_ARVO ? data[INDEKSI] : 0);
        laite_ARVO.입출력정수쓰기(tila_portti, Koko | 0x00080000);
        Suorita_2 = laite_ARVO.밀리초();
        while ((laite_ARVO.입출력정수읽기(tila_portti) & 0xe0008000) == 0)
            if (laite_ARVO.밀리초() - Suorita_2 > 100) return -110;
        if ((laite_ARVO.입출력정수읽기(tila_portti) & 0x8000) == 0) { virhe_LASKE++; return -5; }
        lähettää_paikka = (lähettää_paikka + 1) & 3;
        lähettää_LASKE++;
        return kesto_ARVO;
    }

    static int saada(int[] data) {
        if (입출력기준주소 == 0) return 0;
        if ((laite_ARVO.입출력바이트읽기(입출력기준주소 + 0x3e) & 0x50) != 0) {
            virhe_LASKE++;
            if (!nollata_ARVO()) 입출력기준주소 = 0;
            return 0;
        }
        if ((laite_ARVO.입출력바이트읽기(입출력기준주소 + 0x37) & 1) != 0) return 0;
        int 머리 = laite_ARVO.verkko_Muisti() + saada_toimi_0ac41e06;
        int Tila_ARVO = suoritus_Valvoja.짧은수(머리), Koko = suoritus_Valvoja.짧은수(머리 + 2);
        if (Koko == 0xfff0) return 0; // DMA 진행 중
        if (Koko < 4 || Koko > 1518) {
            virhe_LASKE++;
            if (!nollata_ARVO()) 입출력기준주소 = 0;
            return 0;
        }
        int kesto_ARVO = Koko - 4;
        if ((Tila_ARVO & 1) != 0) {
            for (int INDEKSI = 0; INDEKSI < kesto_ARVO; INDEKSI++) data[INDEKSI] = laite_ARVO.lukea_Muisti(머리 + 4 + INDEKSI);
            saada_LASKE++;
        } else { kesto_ARVO = 0; virhe_LASKE++; }
        saada_toimi_0ac41e06 = (saada_toimi_0ac41e06 + Koko + 4 + 3) & ~3;
        saada_toimi_0ac41e06 &= 8191;
        laite_ARVO.입출력짧은수쓰기(입출력기준주소 + 0x38, (saada_toimi_0ac41e06 - 16) & 65535);
        laite_ARVO.입출력짧은수쓰기(입출력기준주소 + 0x3e, 0x000f);
        return kesto_ARVO;
    }
}
