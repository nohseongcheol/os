// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** PCI RTL8139 (10ec:8139), 단일 tuku_uara 버퍼와 8KiB 수신 Loop_uara. 인터럽트 대신 폴링한다. */
public final class whatunga_atekōkiri {
    static int 입출력기준주소 = 0;
    static int 수신위치 = 0, 송신칸 = 0;
    static int[] pūkoro_ADDRESS = new int[6];
    static int 송신수 = 0, 수신수 = 0, hapa_COUNT = 0;

    static int 설정읽기(int 장치번호, int tūranga) {
        pūkoro_uara.입출력정수쓰기(0xcf8, 0x80000000 | (장치번호 << 11) | tūranga);
        return pūkoro_uara.입출력정수읽기(0xcfc);
    }

    static boolean Whakarite() {
        int 장치번호 = -1;
        for (int INDEX = 0; INDEX < 32; INDEX++) {
            if (설정읽기(INDEX, 0) == 0x813910ec) { 장치번호 = INDEX; break; }
        }
        if (장치번호 < 0) return false;
        int uara_taunoa = 설정읽기(장치번호, 0x10);
        if ((uara_taunoa & 1) == 0 || (uara_taunoa & 0xfffffffc) < 0x100 || (uara_taunoa & 0xfffffffc) > 65535) return false;
        입출력기준주소 = uara_taunoa & 0xfffc;
        int tono = 설정읽기(장치번호, 4);
        pūkoro_uara.입출력정수쓰기(0xcf8, 0x80000004 | (장치번호 << 11));
        pūkoro_uara.입출력짧은수쓰기(0xcfc, tono | 5); // I/O 및 bus master Tuku_uara, PCI tūnga_uara 비트는 건드리지 않음
        pūkoro_uara.입출력바이트쓰기(입출력기준주소 + 0x52, 0);
        if (!Tautuhi_anō_uara()) { 입출력기준주소 = 0; return false; }
        for (int INDEX = 0; INDEX < 6; INDEX++) pūkoro_ADDRESS[INDEX] = pūkoro_uara.입출력바이트읽기(입출력기준주소 + INDEX);
        return true;
    }

    static boolean Tautuhi_anō_uara() {
        pūkoro_uara.입출력바이트쓰기(입출력기준주소 + 0x37, 0x10);
        int whakahaere = pūkoro_uara.밀리초();
        while ((pūkoro_uara.입출력바이트읽기(입출력기준주소 + 0x37) & 0x10) != 0)
            if (pūkoro_uara.밀리초() - whakahaere > 100) return false;
        수신위치 = 0; 송신칸 = 0;
        pūkoro_uara.입출력정수쓰기(입출력기준주소 + 0x30, pūkoro_uara.whatunga_Pūmahara());
        for (int INDEX = 0; INDEX < 4; INDEX++) pūkoro_uara.입출력정수쓰기(입출력기준주소 + 0x20 + INDEX * 4, pūkoro_uara.whatunga_Pūmahara() + 12288);
        pūkoro_uara.입출력짧은수쓰기(입출력기준주소 + 0x3c, 0);
        pūkoro_uara.입출력짧은수쓰기(입출력기준주소 + 0x3e, 0xffff);
        pūkoro_uara.입출력바이트쓰기(입출력기준주소 + 0x37, 0x0c);
        pūkoro_uara.입출력정수쓰기(입출력기준주소 + 0x44, 0x0000e78a); // 자기주소/pāohotanga_uara, wrap 연속 Store_uara, 8KiB
        pūkoro_uara.입출력정수쓰기(입출력기준주소 + 0x40, 0x03000600);
        return true;
    }

    static int tuku(int[] raraunga, int roa_uara) {
        if (입출력기준주소 == 0) return -19;
        if (roa_uara < 14 || roa_uara > 1514) return -90;
        int tūnga_kawe = 입출력기준주소 + 0x10 + 송신칸 * 4;
        int whakahaere = pūkoro_uara.밀리초();
        while ((pūkoro_uara.입출력정수읽기(tūnga_kawe) & 0x2000) == 0)
            if (pūkoro_uara.밀리초() - whakahaere > 100) return -110;
        int rahi = roa_uara < 60 ? 60 : roa_uara;
        for (int INDEX = 0; INDEX < rahi; INDEX++)
            pūkoro_uara.tuhi_Pūmahara(pūkoro_uara.whatunga_Pūmahara() + 12288 + INDEX, INDEX < roa_uara ? raraunga[INDEX] : 0);
        pūkoro_uara.입출력정수쓰기(tūnga_kawe, rahi | 0x00080000);
        whakahaere = pūkoro_uara.밀리초();
        while ((pūkoro_uara.입출력정수읽기(tūnga_kawe) & 0xe0008000) == 0)
            if (pūkoro_uara.밀리초() - whakahaere > 100) return -110;
        if ((pūkoro_uara.입출력정수읽기(tūnga_kawe) & 0x8000) == 0) { hapa_COUNT++; return -5; }
        송신칸 = (송신칸 + 1) & 3;
        송신수++;
        return roa_uara;
    }

    static int 받기(int[] raraunga) {
        if (입출력기준주소 == 0) return 0;
        if ((pūkoro_uara.입출력바이트읽기(입출력기준주소 + 0x3e) & 0x50) != 0) {
            hapa_COUNT++;
            if (!Tautuhi_anō_uara()) 입출력기준주소 = 0;
            return 0;
        }
        if ((pūkoro_uara.입출력바이트읽기(입출력기준주소 + 0x37) & 1) != 0) return 0;
        int 머리 = pūkoro_uara.whatunga_Pūmahara() + 수신위치;
        int tūnga_uara = 실행관리.짧은수(머리), rahi = 실행관리.짧은수(머리 + 2);
        if (rahi == 0xfff0) return 0; // DMA 진행 중
        if (rahi < 4 || rahi > 1518) {
            hapa_COUNT++;
            if (!Tautuhi_anō_uara()) 입출력기준주소 = 0;
            return 0;
        }
        int roa_uara = rahi - 4;
        if ((tūnga_uara & 1) != 0) {
            for (int INDEX = 0; INDEX < roa_uara; INDEX++) raraunga[INDEX] = pūkoro_uara.기억읽기(머리 + 4 + INDEX);
            수신수++;
        } else { roa_uara = 0; hapa_COUNT++; }
        수신위치 = (수신위치 + rahi + 4 + 3) & ~3;
        수신위치 &= 8191;
        pūkoro_uara.입출력짧은수쓰기(입출력기준주소 + 0x38, (수신위치 - 16) & 65535);
        pūkoro_uara.입출력짧은수쓰기(입출력기준주소 + 0x3e, 0x000f);
        return roa_uara;
    }
}
