// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** PCI RTL8139 (10ec:8139), 단일 Thumela_inani 버퍼와 8KiB 수신 iluphu_inani. 인터럽트 대신 폴링한다. */
public final class iNethiwekhi_idrayiva {
    static int 입출력기준주소 = 0;
    static int 수신위치 = 0, 송신칸 = 0;
    static int[] idivayisi_ikheli = new int[6];
    static int 송신수 = 0, 수신수 = 0, 오류수 = 0;

    static int 설정읽기(int 장치번호, int 위치) {
        idivayisi_inani.입출력정수쓰기(0xcf8, 0x80000000 | (장치번호 << 11) | 위치);
        return idivayisi_inani.입출력정수읽기(0xcfc);
    }

    static boolean Hlela() {
        int 장치번호 = -1;
        for (int thola_inkomba = 0; thola_inkomba < 32; thola_inkomba++) {
            if (설정읽기(thola_inkomba, 0) == 0x813910ec) { 장치번호 = thola_inkomba; break; }
        }
        if (장치번호 < 0) return false;
        int inani_elimisiwe = 설정읽기(장치번호, 0x10);
        if ((inani_elimisiwe & 1) == 0 || (inani_elimisiwe & 0xfffffffc) < 0x100 || (inani_elimisiwe & 0xfffffffc) > 65535) return false;
        입출력기준주소 = inani_elimisiwe & 0xfffc;
        int Umlayelo = 설정읽기(장치번호, 4);
        idivayisi_inani.입출력정수쓰기(0xcf8, 0x80000004 | (장치번호 << 11));
        idivayisi_inani.입출력짧은수쓰기(0xcfc, Umlayelo | 5); // I/O 및 bus master vumela_inani, PCI isimo_inani 비트는 건드리지 않음
        idivayisi_inani.입출력바이트쓰기(입출력기준주소 + 0x52, 0);
        if (!Misa_kabusha_inani()) { 입출력기준주소 = 0; return false; }
        for (int thola_inkomba = 0; thola_inkomba < 6; thola_inkomba++) idivayisi_ikheli[thola_inkomba] = idivayisi_inani.입출력바이트읽기(입출력기준주소 + thola_inkomba);
        return true;
    }

    static boolean Misa_kabusha_inani() {
        idivayisi_inani.입출력바이트쓰기(입출력기준주소 + 0x37, 0x10);
        int Sebenzisa = idivayisi_inani.밀리초();
        while ((idivayisi_inani.입출력바이트읽기(입출력기준주소 + 0x37) & 0x10) != 0)
            if (idivayisi_inani.밀리초() - Sebenzisa > 100) return false;
        수신위치 = 0; 송신칸 = 0;
        idivayisi_inani.입출력정수쓰기(입출력기준주소 + 0x30, idivayisi_inani.iNethiwekhi_inkumbulo());
        for (int thola_inkomba = 0; thola_inkomba < 4; thola_inkomba++) idivayisi_inani.입출력정수쓰기(입출력기준주소 + 0x20 + thola_inkomba * 4, idivayisi_inani.iNethiwekhi_inkumbulo() + 12288);
        idivayisi_inani.입출력짧은수쓰기(입출력기준주소 + 0x3c, 0);
        idivayisi_inani.입출력짧은수쓰기(입출력기준주소 + 0x3e, 0xffff);
        idivayisi_inani.입출력바이트쓰기(입출력기준주소 + 0x37, 0x0c);
        idivayisi_inani.입출력정수쓰기(입출력기준주소 + 0x44, 0x0000e78a); // 자기주소/ukusakaza_inani, wrap 연속 Store_inani, 8KiB
        idivayisi_inani.입출력정수쓰기(입출력기준주소 + 0x40, 0x03000600);
        return true;
    }

    static int Thumela(int[] imininingwane, int ubude_inani) {
        if (입출력기준주소 == 0) return -19;
        if (ubude_inani < 14 || ubude_inani > 1514) return -90;
        int isimo_intuba = 입출력기준주소 + 0x10 + 송신칸 * 4;
        int Sebenzisa = idivayisi_inani.밀리초();
        while ((idivayisi_inani.입출력정수읽기(isimo_intuba) & 0x2000) == 0)
            if (idivayisi_inani.밀리초() - Sebenzisa > 100) return -110;
        int Ubungako = ubude_inani < 60 ? 60 : ubude_inani;
        for (int thola_inkomba = 0; thola_inkomba < Ubungako; thola_inkomba++)
            idivayisi_inani.bhala_inkumbulo(idivayisi_inani.iNethiwekhi_inkumbulo() + 12288 + thola_inkomba, thola_inkomba < ubude_inani ? imininingwane[thola_inkomba] : 0);
        idivayisi_inani.입출력정수쓰기(isimo_intuba, Ubungako | 0x00080000);
        Sebenzisa = idivayisi_inani.밀리초();
        while ((idivayisi_inani.입출력정수읽기(isimo_intuba) & 0xe0008000) == 0)
            if (idivayisi_inani.밀리초() - Sebenzisa > 100) return -110;
        if ((idivayisi_inani.입출력정수읽기(isimo_intuba) & 0x8000) == 0) { 오류수++; return -5; }
        송신칸 = (송신칸 + 1) & 3;
        송신수++;
        return ubude_inani;
    }

    static int 받기(int[] imininingwane) {
        if (입출력기준주소 == 0) return 0;
        if ((idivayisi_inani.입출력바이트읽기(입출력기준주소 + 0x3e) & 0x50) != 0) {
            오류수++;
            if (!Misa_kabusha_inani()) 입출력기준주소 = 0;
            return 0;
        }
        if ((idivayisi_inani.입출력바이트읽기(입출력기준주소 + 0x37) & 1) != 0) return 0;
        int 머리 = idivayisi_inani.iNethiwekhi_inkumbulo() + 수신위치;
        int isimo_inani = 실행관리.짧은수(머리), Ubungako = 실행관리.짧은수(머리 + 2);
        if (Ubungako == 0xfff0) return 0; // DMA 진행 중
        if (Ubungako < 4 || Ubungako > 1518) {
            오류수++;
            if (!Misa_kabusha_inani()) 입출력기준주소 = 0;
            return 0;
        }
        int ubude_inani = Ubungako - 4;
        if ((isimo_inani & 1) != 0) {
            for (int thola_inkomba = 0; thola_inkomba < ubude_inani; thola_inkomba++) imininingwane[thola_inkomba] = idivayisi_inani.기억읽기(머리 + 4 + thola_inkomba);
            수신수++;
        } else { ubude_inani = 0; 오류수++; }
        수신위치 = (수신위치 + Ubungako + 4 + 3) & ~3;
        수신위치 &= 8191;
        idivayisi_inani.입출력짧은수쓰기(입출력기준주소 + 0x38, (수신위치 - 16) & 65535);
        idivayisi_inani.입출력짧은수쓰기(입출력기준주소 + 0x3e, 0x000f);
        return ubude_inani;
    }
}
