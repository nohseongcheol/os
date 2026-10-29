// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** PCI RTL8139 (10ec:8139), 단일 iber_baha 버퍼와 8KiB 수신 sikl_baha. 인터럽트 대신 폴링한다. */
public final class Tor_draýwer {
    static int 입출력기준주소 = 0;
    static int 수신위치 = 0, 송신칸 = 0;
    static int[] enjam_salgy = new int[6];
    static int 송신수 = 0, 수신수 = 0, 오류수 = 0;

    static int 설정읽기(int 장치번호, int 위치) {
        enjam_baha.입출력정수쓰기(0xcf8, 0x80000000 | (장치번호 << 11) | 위치);
        return enjam_baha.입출력정수읽기(0xcfc);
    }

    static boolean Taýýarla() {
        int 장치번호 = -1;
        for (int indeks = 0; indeks < 32; indeks++) {
            if (설정읽기(indeks, 0) == 0x813910ec) { 장치번호 = indeks; break; }
        }
        if (장치번호 < 0) return false;
        int öňünden_kabul_edilen_baha = 설정읽기(장치번호, 0x10);
        if ((öňünden_kabul_edilen_baha & 1) == 0 || (öňünden_kabul_edilen_baha & 0xfffffffc) < 0x100 || (öňünden_kabul_edilen_baha & 0xfffffffc) > 65535) return false;
        입출력기준주소 = öňünden_kabul_edilen_baha & 0xfffc;
        int buýruk = 설정읽기(장치번호, 4);
        enjam_baha.입출력정수쓰기(0xcf8, 0x80000004 | (장치번호 << 11));
        enjam_baha.입출력짧은수쓰기(0xcfc, buýruk | 5); // I/O 및 bus master Rugsat_ber_baha, PCI ýagdaý_baha 비트는 건드리지 않음
        enjam_baha.입출력바이트쓰기(입출력기준주소 + 0x52, 0);
        if (!Nol_et_baha()) { 입출력기준주소 = 0; return false; }
        for (int indeks = 0; indeks < 6; indeks++) enjam_salgy[indeks] = enjam_baha.입출력바이트읽기(입출력기준주소 + indeks);
        return true;
    }

    static boolean Nol_et_baha() {
        enjam_baha.입출력바이트쓰기(입출력기준주소 + 0x37, 0x10);
        int Bitir = enjam_baha.밀리초();
        while ((enjam_baha.입출력바이트읽기(입출력기준주소 + 0x37) & 0x10) != 0)
            if (enjam_baha.밀리초() - Bitir > 100) return false;
        수신위치 = 0; 송신칸 = 0;
        enjam_baha.입출력정수쓰기(입출력기준주소 + 0x30, enjam_baha.Tor_ýat());
        for (int indeks = 0; indeks < 4; indeks++) enjam_baha.입출력정수쓰기(입출력기준주소 + 0x20 + indeks * 4, enjam_baha.Tor_ýat() + 12288);
        enjam_baha.입출력짧은수쓰기(입출력기준주소 + 0x3c, 0);
        enjam_baha.입출력짧은수쓰기(입출력기준주소 + 0x3e, 0xffff);
        enjam_baha.입출력바이트쓰기(입출력기준주소 + 0x37, 0x0c);
        enjam_baha.입출력정수쓰기(입출력기준주소 + 0x44, 0x0000e78a); // 자기주소/방송, wrap 연속 Store_baha, 8KiB
        enjam_baha.입출력정수쓰기(입출력기준주소 + 0x40, 0x03000600);
        return true;
    }

    static int iber(int[] maglumat, int dowamlylyk_baha) {
        if (입출력기준주소 == 0) return -19;
        if (dowamlylyk_baha < 14 || dowamlylyk_baha > 1514) return -90;
        int ýagdaý_port = 입출력기준주소 + 0x10 + 송신칸 * 4;
        int Bitir = enjam_baha.밀리초();
        while ((enjam_baha.입출력정수읽기(ýagdaý_port) & 0x2000) == 0)
            if (enjam_baha.밀리초() - Bitir > 100) return -110;
        int Ululyk = dowamlylyk_baha < 60 ? 60 : dowamlylyk_baha;
        for (int indeks = 0; indeks < Ululyk; indeks++)
            enjam_baha.ýaz_ýat(enjam_baha.Tor_ýat() + 12288 + indeks, indeks < dowamlylyk_baha ? maglumat[indeks] : 0);
        enjam_baha.입출력정수쓰기(ýagdaý_port, Ululyk | 0x00080000);
        Bitir = enjam_baha.밀리초();
        while ((enjam_baha.입출력정수읽기(ýagdaý_port) & 0xe0008000) == 0)
            if (enjam_baha.밀리초() - Bitir > 100) return -110;
        if ((enjam_baha.입출력정수읽기(ýagdaý_port) & 0x8000) == 0) { 오류수++; return -5; }
        송신칸 = (송신칸 + 1) & 3;
        송신수++;
        return dowamlylyk_baha;
    }

    static int 받기(int[] maglumat) {
        if (입출력기준주소 == 0) return 0;
        if ((enjam_baha.입출력바이트읽기(입출력기준주소 + 0x3e) & 0x50) != 0) {
            오류수++;
            if (!Nol_et_baha()) 입출력기준주소 = 0;
            return 0;
        }
        if ((enjam_baha.입출력바이트읽기(입출력기준주소 + 0x37) & 1) != 0) return 0;
        int 머리 = enjam_baha.Tor_ýat() + 수신위치;
        int ýagdaý_baha = 실행관리.짧은수(머리), Ululyk = 실행관리.짧은수(머리 + 2);
        if (Ululyk == 0xfff0) return 0; // DMA 진행 중
        if (Ululyk < 4 || Ululyk > 1518) {
            오류수++;
            if (!Nol_et_baha()) 입출력기준주소 = 0;
            return 0;
        }
        int dowamlylyk_baha = Ululyk - 4;
        if ((ýagdaý_baha & 1) != 0) {
            for (int indeks = 0; indeks < dowamlylyk_baha; indeks++) maglumat[indeks] = enjam_baha.기억읽기(머리 + 4 + indeks);
            수신수++;
        } else { dowamlylyk_baha = 0; 오류수++; }
        수신위치 = (수신위치 + Ululyk + 4 + 3) & ~3;
        수신위치 &= 8191;
        enjam_baha.입출력짧은수쓰기(입출력기준주소 + 0x38, (수신위치 - 16) & 65535);
        enjam_baha.입출력짧은수쓰기(입출력기준주소 + 0x3e, 0x000f);
        return dowamlylyk_baha;
    }
}
