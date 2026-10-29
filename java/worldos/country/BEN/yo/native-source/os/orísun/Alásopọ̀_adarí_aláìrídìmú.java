// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** PCI RTL8139 (10ec:8139), 단일 í_meèlì_iye 버퍼와 8KiB 수신 ṣetúnṣe_iye. 인터럽트 대신 폴링한다. */
public final class Alásopọ̀_adarí_aláìrídìmú {
    static int 입출력기준주소 = 0;
    static int 수신위치 = 0, 송신칸 = 0;
    static int[] ohun_èlò_àdírẹ́ẹ̀sì = new int[6];
    static int 송신수 = 0, 수신수 = 0, 오류수 = 0;

    static int 설정읽기(int 장치번호, int 위치) {
        ohun_èlò_iye.입출력정수쓰기(0xcf8, 0x80000000 | (장치번호 << 11) | 위치);
        return ohun_èlò_iye.입출력정수읽기(0xcfc);
    }

    static boolean gbaradì() {
        int 장치번호 = -1;
        for (int wá_atọ̀ka_àkóónú = 0; wá_atọ̀ka_àkóónú < 32; wá_atọ̀ka_àkóónú++) {
            if (설정읽기(wá_atọ̀ka_àkóónú, 0) == 0x813910ec) { 장치번호 = wá_atọ̀ka_àkóónú; break; }
        }
        if (장치번호 < 0) return false;
        int àdáwọ̀ = 설정읽기(장치번호, 0x10);
        if ((àdáwọ̀ & 1) == 0 || (àdáwọ̀ & 0xfffffffc) < 0x100 || (àdáwọ̀ & 0xfffffffc) > 65535) return false;
        입출력기준주소 = àdáwọ̀ & 0xfffc;
        int Àṣẹ = 설정읽기(장치번호, 4);
        ohun_èlò_iye.입출력정수쓰기(0xcf8, 0x80000004 | (장치번호 << 11));
        ohun_èlò_iye.입출력짧은수쓰기(0xcfc, Àṣẹ | 5); // I/O 및 bus master Fún_Lááyè_iye, PCI ipò_iye 비트는 건드리지 않음
        ohun_èlò_iye.입출력바이트쓰기(입출력기준주소 + 0x52, 0);
        if (!ṣàtúntò_iye()) { 입출력기준주소 = 0; return false; }
        for (int wá_atọ̀ka_àkóónú = 0; wá_atọ̀ka_àkóónú < 6; wá_atọ̀ka_àkóónú++) ohun_èlò_àdírẹ́ẹ̀sì[wá_atọ̀ka_àkóónú] = ohun_èlò_iye.입출력바이트읽기(입출력기준주소 + wá_atọ̀ka_àkóónú);
        return true;
    }

    static boolean ṣàtúntò_iye() {
        ohun_èlò_iye.입출력바이트쓰기(입출력기준주소 + 0x37, 0x10);
        int Rọ́ọ̀nù = ohun_èlò_iye.밀리초();
        while ((ohun_èlò_iye.입출력바이트읽기(입출력기준주소 + 0x37) & 0x10) != 0)
            if (ohun_èlò_iye.밀리초() - Rọ́ọ̀nù > 100) return false;
        수신위치 = 0; 송신칸 = 0;
        ohun_èlò_iye.입출력정수쓰기(입출력기준주소 + 0x30, ohun_èlò_iye.Alásopọ̀_ibi_ìpamọ́());
        for (int wá_atọ̀ka_àkóónú = 0; wá_atọ̀ka_àkóónú < 4; wá_atọ̀ka_àkóónú++) ohun_èlò_iye.입출력정수쓰기(입출력기준주소 + 0x20 + wá_atọ̀ka_àkóónú * 4, ohun_èlò_iye.Alásopọ̀_ibi_ìpamọ́() + 12288);
        ohun_èlò_iye.입출력짧은수쓰기(입출력기준주소 + 0x3c, 0);
        ohun_èlò_iye.입출력짧은수쓰기(입출력기준주소 + 0x3e, 0xffff);
        ohun_èlò_iye.입출력바이트쓰기(입출력기준주소 + 0x37, 0x0c);
        ohun_èlò_iye.입출력정수쓰기(입출력기준주소 + 0x44, 0x0000e78a); // 자기주소/àtagbà_iye, wrap 연속 Store_iye, 8KiB
        ohun_èlò_iye.입출력정수쓰기(입출력기준주소 + 0x40, 0x03000600);
        return true;
    }

    static int í_meèlì(int[] détà, int gígùn_iye) {
        if (입출력기준주소 == 0) return -19;
        if (gígùn_iye < 14 || gígùn_iye > 1514) return -90;
        int ipò_ojú = 입출력기준주소 + 0x10 + 송신칸 * 4;
        int Rọ́ọ̀nù = ohun_èlò_iye.밀리초();
        while ((ohun_èlò_iye.입출력정수읽기(ipò_ojú) & 0x2000) == 0)
            if (ohun_èlò_iye.밀리초() - Rọ́ọ̀nù > 100) return -110;
        int Ìwọ̀n = gígùn_iye < 60 ? 60 : gígùn_iye;
        for (int wá_atọ̀ka_àkóónú = 0; wá_atọ̀ka_àkóónú < Ìwọ̀n; wá_atọ̀ka_àkóónú++)
            ohun_èlò_iye.kọ_ibi_ìpamọ́(ohun_èlò_iye.Alásopọ̀_ibi_ìpamọ́() + 12288 + wá_atọ̀ka_àkóónú, wá_atọ̀ka_àkóónú < gígùn_iye ? détà[wá_atọ̀ka_àkóónú] : 0);
        ohun_èlò_iye.입출력정수쓰기(ipò_ojú, Ìwọ̀n | 0x00080000);
        Rọ́ọ̀nù = ohun_èlò_iye.밀리초();
        while ((ohun_èlò_iye.입출력정수읽기(ipò_ojú) & 0xe0008000) == 0)
            if (ohun_èlò_iye.밀리초() - Rọ́ọ̀nù > 100) return -110;
        if ((ohun_èlò_iye.입출력정수읽기(ipò_ojú) & 0x8000) == 0) { 오류수++; return -5; }
        송신칸 = (송신칸 + 1) & 3;
        송신수++;
        return gígùn_iye;
    }

    static int 받기(int[] détà) {
        if (입출력기준주소 == 0) return 0;
        if ((ohun_èlò_iye.입출력바이트읽기(입출력기준주소 + 0x3e) & 0x50) != 0) {
            오류수++;
            if (!ṣàtúntò_iye()) 입출력기준주소 = 0;
            return 0;
        }
        if ((ohun_èlò_iye.입출력바이트읽기(입출력기준주소 + 0x37) & 1) != 0) return 0;
        int 머리 = ohun_èlò_iye.Alásopọ̀_ibi_ìpamọ́() + 수신위치;
        int ipò_iye = 실행관리.짧은수(머리), Ìwọ̀n = 실행관리.짧은수(머리 + 2);
        if (Ìwọ̀n == 0xfff0) return 0; // DMA 진행 중
        if (Ìwọ̀n < 4 || Ìwọ̀n > 1518) {
            오류수++;
            if (!ṣàtúntò_iye()) 입출력기준주소 = 0;
            return 0;
        }
        int gígùn_iye = Ìwọ̀n - 4;
        if ((ipò_iye & 1) != 0) {
            for (int wá_atọ̀ka_àkóónú = 0; wá_atọ̀ka_àkóónú < gígùn_iye; wá_atọ̀ka_àkóónú++) détà[wá_atọ̀ka_àkóónú] = ohun_èlò_iye.기억읽기(머리 + 4 + wá_atọ̀ka_àkóónú);
            수신수++;
        } else { gígùn_iye = 0; 오류수++; }
        수신위치 = (수신위치 + Ìwọ̀n + 4 + 3) & ~3;
        수신위치 &= 8191;
        ohun_èlò_iye.입출력짧은수쓰기(입출력기준주소 + 0x38, (수신위치 - 16) & 65535);
        ohun_èlò_iye.입출력짧은수쓰기(입출력기준주소 + 0x3e, 0x000f);
        return gígùn_iye;
    }
}
