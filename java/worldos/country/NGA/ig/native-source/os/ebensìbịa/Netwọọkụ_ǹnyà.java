// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** PCI RTL8139 (10ec:8139), 단일 zìga_valuu 버퍼와 8KiB 수신 memmenwè_valuu. 인터럽트 대신 폴링한다. */
public final class Netwọọkụ_ǹnyà {
    static int 입출력기준주소 = 0;
    static int 수신위치 = 0, 송신칸 = 0;
    static int[] njìarụ_àdreèsì = new int[6];
    static int 송신수 = 0, 수신수 = 0, 오류수 = 0;

    static int 설정읽기(int 장치번호, int 위치) {
        njìarụ_valuu.입출력정수쓰기(0xcf8, 0x80000000 | (장치번호 << 11) | 위치);
        return njìarụ_valuu.입출력정수읽기(0xcfc);
    }

    static boolean Kwado() {
        int 장치번호 = -1;
        for (int indèks = 0; indèks < 32; indèks++) {
            if (설정읽기(indèks, 0) == 0x813910ec) { 장치번호 = indèks; break; }
        }
        if (장치번호 < 0) return false;
        int Ngwa_ihe_dịadị = 설정읽기(장치번호, 0x10);
        if ((Ngwa_ihe_dịadị & 1) == 0 || (Ngwa_ihe_dịadị & 0xfffffffc) < 0x100 || (Ngwa_ihe_dịadị & 0xfffffffc) > 65535) return false;
        입출력기준주소 = Ngwa_ihe_dịadị & 0xfffc;
        int Ntiiwu = 설정읽기(장치번호, 4);
        njìarụ_valuu.입출력정수쓰기(0xcf8, 0x80000004 | (장치번호 << 11));
        njìarụ_valuu.입출력짧은수쓰기(0xcfc, Ntiiwu | 5); // I/O 및 bus master Kwère_valuu, PCI ọnọdụ_valuu 비트는 건드리지 않음
        njìarụ_valuu.입출력바이트쓰기(입출력기준주소 + 0x52, 0);
        if (!bidokwa_valuu()) { 입출력기준주소 = 0; return false; }
        for (int indèks = 0; indèks < 6; indèks++) njìarụ_àdreèsì[indèks] = njìarụ_valuu.입출력바이트읽기(입출력기준주소 + indèks);
        return true;
    }

    static boolean bidokwa_valuu() {
        njìarụ_valuu.입출력바이트쓰기(입출력기준주소 + 0x37, 0x10);
        int Bido = njìarụ_valuu.밀리초();
        while ((njìarụ_valuu.입출력바이트읽기(입출력기준주소 + 0x37) & 0x10) != 0)
            if (njìarụ_valuu.밀리초() - Bido > 100) return false;
        수신위치 = 0; 송신칸 = 0;
        njìarụ_valuu.입출력정수쓰기(입출력기준주소 + 0x30, njìarụ_valuu.Netwọọkụ_memọrị());
        for (int indèks = 0; indèks < 4; indèks++) njìarụ_valuu.입출력정수쓰기(입출력기준주소 + 0x20 + indèks * 4, njìarụ_valuu.Netwọọkụ_memọrị() + 12288);
        njìarụ_valuu.입출력짧은수쓰기(입출력기준주소 + 0x3c, 0);
        njìarụ_valuu.입출력짧은수쓰기(입출력기준주소 + 0x3e, 0xffff);
        njìarụ_valuu.입출력바이트쓰기(입출력기준주소 + 0x37, 0x0c);
        njìarụ_valuu.입출력정수쓰기(입출력기준주소 + 0x44, 0x0000e78a); // 자기주소/방송, wrap 연속 Store_valuu, 8KiB
        njìarụ_valuu.입출력정수쓰기(입출력기준주소 + 0x40, 0x03000600);
        return true;
    }

    static int zìga(int[] datà, int ogologo_valuu) {
        if (입출력기준주소 == 0) return -19;
        if (ogologo_valuu < 14 || ogologo_valuu > 1514) return -90;
        int ọnọdụ_pọọt = 입출력기준주소 + 0x10 + 송신칸 * 4;
        int Bido = njìarụ_valuu.밀리초();
        while ((njìarụ_valuu.입출력정수읽기(ọnọdụ_pọọt) & 0x2000) == 0)
            if (njìarụ_valuu.밀리초() - Bido > 100) return -110;
        int Ụhara = ogologo_valuu < 60 ? 60 : ogologo_valuu;
        for (int indèks = 0; indèks < Ụhara; indèks++)
            njìarụ_valuu.dee_memọrị(njìarụ_valuu.Netwọọkụ_memọrị() + 12288 + indèks, indèks < ogologo_valuu ? datà[indèks] : 0);
        njìarụ_valuu.입출력정수쓰기(ọnọdụ_pọọt, Ụhara | 0x00080000);
        Bido = njìarụ_valuu.밀리초();
        while ((njìarụ_valuu.입출력정수읽기(ọnọdụ_pọọt) & 0xe0008000) == 0)
            if (njìarụ_valuu.밀리초() - Bido > 100) return -110;
        if ((njìarụ_valuu.입출력정수읽기(ọnọdụ_pọọt) & 0x8000) == 0) { 오류수++; return -5; }
        송신칸 = (송신칸 + 1) & 3;
        송신수++;
        return ogologo_valuu;
    }

    static int 받기(int[] datà) {
        if (입출력기준주소 == 0) return 0;
        if ((njìarụ_valuu.입출력바이트읽기(입출력기준주소 + 0x3e) & 0x50) != 0) {
            오류수++;
            if (!bidokwa_valuu()) 입출력기준주소 = 0;
            return 0;
        }
        if ((njìarụ_valuu.입출력바이트읽기(입출력기준주소 + 0x37) & 1) != 0) return 0;
        int 머리 = njìarụ_valuu.Netwọọkụ_memọrị() + 수신위치;
        int ọnọdụ_valuu = 실행관리.짧은수(머리), Ụhara = 실행관리.짧은수(머리 + 2);
        if (Ụhara == 0xfff0) return 0; // DMA 진행 중
        if (Ụhara < 4 || Ụhara > 1518) {
            오류수++;
            if (!bidokwa_valuu()) 입출력기준주소 = 0;
            return 0;
        }
        int ogologo_valuu = Ụhara - 4;
        if ((ọnọdụ_valuu & 1) != 0) {
            for (int indèks = 0; indèks < ogologo_valuu; indèks++) datà[indèks] = njìarụ_valuu.기억읽기(머리 + 4 + indèks);
            수신수++;
        } else { ogologo_valuu = 0; 오류수++; }
        수신위치 = (수신위치 + Ụhara + 4 + 3) & ~3;
        수신위치 &= 8191;
        njìarụ_valuu.입출력짧은수쓰기(입출력기준주소 + 0x38, (수신위치 - 16) & 65535);
        njìarụ_valuu.입출력짧은수쓰기(입출력기준주소 + 0x3e, 0x000f);
        return ogologo_valuu;
    }
}
