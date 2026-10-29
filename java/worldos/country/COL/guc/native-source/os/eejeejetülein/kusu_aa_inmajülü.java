// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** PCI RTL8139 (10ec:8139), 단일 ajütaa_ajutuu 버퍼와 8KiB 수신 eitawaakualü_ajutuu. 인터럽트 대신 폴링한다. */
public final class kusu_aa_inmajülü {
    static int 입출력기준주소 = 0;
    static int 수신위치 = 0, 송신칸 = 0;
    static int[] serulaalü_ejepüsee = new int[6];
    static int 송신수 = 0, 수신수 = 0, 오류수 = 0;

    static int 설정읽기(int 장치번호, int 위치) {
        serulaalü_ajutuu.입출력정수쓰기(0xcf8, 0x80000000 | (장치번호 << 11) | 위치);
        return serulaalü_ajutuu.입출력정수읽기(0xcfc);
    }

    static boolean 준비() {
        int 장치번호 = -1;
        for (int ee_iyatialujuna = 0; ee_iyatialujuna < 32; ee_iyatialujuna++) {
            if (설정읽기(ee_iyatialujuna, 0) == 0x813910ec) { 장치번호 = ee_iyatialujuna; break; }
        }
        if (장치번호 < 0) return false;
        int ajutuu_aneekuushitüjülia = 설정읽기(장치번호, 0x10);
        if ((ajutuu_aneekuushitüjülia & 1) == 0 || (ajutuu_aneekuushitüjülia & 0xfffffffc) < 0x100 || (ajutuu_aneekuushitüjülia & 0xfffffffc) > 65535) return false;
        입출력기준주소 = ajutuu_aneekuushitüjülia & 0xfffc;
        int aluwataaya = 설정읽기(장치번호, 4);
        serulaalü_ajutuu.입출력정수쓰기(0xcf8, 0x80000004 | (장치번호 << 11));
        serulaalü_ajutuu.입출력짧은수쓰기(0xcfc, aluwataaya | 5); // I/O 및 bus master A_tte_eraa_ajutuu, PCI jamakua_iparülein_ajutuu 비트는 건드리지 않음
        serulaalü_ajutuu.입출력바이트쓰기(입출력기준주소 + 0x52, 0);
        if (!재설정()) { 입출력기준주소 = 0; return false; }
        for (int ee_iyatialujuna = 0; ee_iyatialujuna < 6; ee_iyatialujuna++) serulaalü_ejepüsee[ee_iyatialujuna] = serulaalü_ajutuu.입출력바이트읽기(입출력기준주소 + ee_iyatialujuna);
        return true;
    }

    static boolean 재설정() {
        serulaalü_ajutuu.입출력바이트쓰기(입출력기준주소 + 0x37, 0x10);
        int 시작 = serulaalü_ajutuu.밀리초();
        while ((serulaalü_ajutuu.입출력바이트읽기(입출력기준주소 + 0x37) & 0x10) != 0)
            if (serulaalü_ajutuu.밀리초() - 시작 > 100) return false;
        수신위치 = 0; 송신칸 = 0;
        serulaalü_ajutuu.입출력정수쓰기(입출력기준주소 + 0x30, serulaalü_ajutuu.통신기억());
        for (int ee_iyatialujuna = 0; ee_iyatialujuna < 4; ee_iyatialujuna++) serulaalü_ajutuu.입출력정수쓰기(입출력기준주소 + 0x20 + ee_iyatialujuna * 4, serulaalü_ajutuu.통신기억() + 12288);
        serulaalü_ajutuu.입출력짧은수쓰기(입출력기준주소 + 0x3c, 0);
        serulaalü_ajutuu.입출력짧은수쓰기(입출력기준주소 + 0x3e, 0xffff);
        serulaalü_ajutuu.입출력바이트쓰기(입출력기준주소 + 0x37, 0x0c);
        serulaalü_ajutuu.입출력정수쓰기(입출력기준주소 + 0x44, 0x0000e78a); // 자기주소/방송, wrap 연속 저장, 8KiB
        serulaalü_ajutuu.입출력정수쓰기(입출력기준주소 + 0x40, 0x03000600);
        return true;
    }

    static int ajütaa(int[] atijaaya, int akaliaa_ajutuu) {
        if (입출력기준주소 == 0) return -19;
        if (akaliaa_ajutuu < 14 || akaliaa_ajutuu > 1514) return -90;
        int jamakua_iparülein_outtülee = 입출력기준주소 + 0x10 + 송신칸 * 4;
        int 시작 = serulaalü_ajutuu.밀리초();
        while ((serulaalü_ajutuu.입출력정수읽기(jamakua_iparülein_outtülee) & 0x2000) == 0)
            if (serulaalü_ajutuu.밀리초() - 시작 > 100) return -110;
        int 크기 = akaliaa_ajutuu < 60 ? 60 : akaliaa_ajutuu;
        for (int ee_iyatialujuna = 0; ee_iyatialujuna < 크기; ee_iyatialujuna++)
            serulaalü_ajutuu.기억쓰기(serulaalü_ajutuu.통신기억() + 12288 + ee_iyatialujuna, ee_iyatialujuna < akaliaa_ajutuu ? atijaaya[ee_iyatialujuna] : 0);
        serulaalü_ajutuu.입출력정수쓰기(jamakua_iparülein_outtülee, 크기 | 0x00080000);
        시작 = serulaalü_ajutuu.밀리초();
        while ((serulaalü_ajutuu.입출력정수읽기(jamakua_iparülein_outtülee) & 0xe0008000) == 0)
            if (serulaalü_ajutuu.밀리초() - 시작 > 100) return -110;
        if ((serulaalü_ajutuu.입출력정수읽기(jamakua_iparülein_outtülee) & 0x8000) == 0) { 오류수++; return -5; }
        송신칸 = (송신칸 + 1) & 3;
        송신수++;
        return akaliaa_ajutuu;
    }

    static int 받기(int[] atijaaya) {
        if (입출력기준주소 == 0) return 0;
        if ((serulaalü_ajutuu.입출력바이트읽기(입출력기준주소 + 0x3e) & 0x50) != 0) {
            오류수++;
            if (!재설정()) 입출력기준주소 = 0;
            return 0;
        }
        if ((serulaalü_ajutuu.입출력바이트읽기(입출력기준주소 + 0x37) & 1) != 0) return 0;
        int 머리 = serulaalü_ajutuu.통신기억() + 수신위치;
        int jamakua_iparülein_ajutuu = 실행관리.짧은수(머리), 크기 = 실행관리.짧은수(머리 + 2);
        if (크기 == 0xfff0) return 0; // DMA 진행 중
        if (크기 < 4 || 크기 > 1518) {
            오류수++;
            if (!재설정()) 입출력기준주소 = 0;
            return 0;
        }
        int akaliaa_ajutuu = 크기 - 4;
        if ((jamakua_iparülein_ajutuu & 1) != 0) {
            for (int ee_iyatialujuna = 0; ee_iyatialujuna < akaliaa_ajutuu; ee_iyatialujuna++) atijaaya[ee_iyatialujuna] = serulaalü_ajutuu.기억읽기(머리 + 4 + ee_iyatialujuna);
            수신수++;
        } else { akaliaa_ajutuu = 0; 오류수++; }
        수신위치 = (수신위치 + 크기 + 4 + 3) & ~3;
        수신위치 &= 8191;
        serulaalü_ajutuu.입출력짧은수쓰기(입출력기준주소 + 0x38, (수신위치 - 16) & 65535);
        serulaalü_ajutuu.입출력짧은수쓰기(입출력기준주소 + 0x3e, 0x000f);
        return akaliaa_ajutuu;
    }
}
