// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** PCI RTL8139 (10ec:8139), 단일 tuma_thamani 버퍼와 8KiB 수신 kitanzi_thamani. 인터럽트 대신 폴링한다. */
public final class Mtandao_kiendeshaji {
    static int 입출력기준주소 = 0;
    static int 수신위치 = 0, 송신칸 = 0;
    static int[] kifaa_anwani = new int[6];
    static int 송신수 = 0, 수신수 = 0, 오류수 = 0;

    static int 설정읽기(int 장치번호, int 위치) {
        kifaa_thamani.입출력정수쓰기(0xcf8, 0x80000000 | (장치번호 << 11) | 위치);
        return kifaa_thamani.입출력정수읽기(0xcfc);
    }

    static boolean Andaa() {
        int 장치번호 = -1;
        for (int kielezo = 0; kielezo < 32; kielezo++) {
            if (설정읽기(kielezo, 0) == 0x813910ec) { 장치번호 = kielezo; break; }
        }
        if (장치번호 < 0) return false;
        int hali_ya_chaguo_msingi = 설정읽기(장치번호, 0x10);
        if ((hali_ya_chaguo_msingi & 1) == 0 || (hali_ya_chaguo_msingi & 0xfffffffc) < 0x100 || (hali_ya_chaguo_msingi & 0xfffffffc) > 65535) return false;
        입출력기준주소 = hali_ya_chaguo_msingi & 0xfffc;
        int amri = 설정읽기(장치번호, 4);
        kifaa_thamani.입출력정수쓰기(0xcf8, 0x80000004 | (장치번호 << 11));
        kifaa_thamani.입출력짧은수쓰기(0xcfc, amri | 5); // I/O 및 bus master Ruhusu_thamani, PCI hali_thamani 비트는 건드리지 않음
        kifaa_thamani.입출력바이트쓰기(입출력기준주소 + 0x52, 0);
        if (!Weka_upya_thamani()) { 입출력기준주소 = 0; return false; }
        for (int kielezo = 0; kielezo < 6; kielezo++) kifaa_anwani[kielezo] = kifaa_thamani.입출력바이트읽기(입출력기준주소 + kielezo);
        return true;
    }

    static boolean Weka_upya_thamani() {
        kifaa_thamani.입출력바이트쓰기(입출력기준주소 + 0x37, 0x10);
        int endesha = kifaa_thamani.밀리초();
        while ((kifaa_thamani.입출력바이트읽기(입출력기준주소 + 0x37) & 0x10) != 0)
            if (kifaa_thamani.밀리초() - endesha > 100) return false;
        수신위치 = 0; 송신칸 = 0;
        kifaa_thamani.입출력정수쓰기(입출력기준주소 + 0x30, kifaa_thamani.Mtandao_kumbukumbu());
        for (int kielezo = 0; kielezo < 4; kielezo++) kifaa_thamani.입출력정수쓰기(입출력기준주소 + 0x20 + kielezo * 4, kifaa_thamani.Mtandao_kumbukumbu() + 12288);
        kifaa_thamani.입출력짧은수쓰기(입출력기준주소 + 0x3c, 0);
        kifaa_thamani.입출력짧은수쓰기(입출력기준주소 + 0x3e, 0xffff);
        kifaa_thamani.입출력바이트쓰기(입출력기준주소 + 0x37, 0x0c);
        kifaa_thamani.입출력정수쓰기(입출력기준주소 + 0x44, 0x0000e78a); // 자기주소/kutangaza_thamani, wrap 연속 Store_thamani, 8KiB
        kifaa_thamani.입출력정수쓰기(입출력기준주소 + 0x40, 0x03000600);
        return true;
    }

    static int tuma(int[] data, int urefu_thamani) {
        if (입출력기준주소 == 0) return -19;
        if (urefu_thamani < 14 || urefu_thamani > 1514) return -90;
        int hali_kituo = 입출력기준주소 + 0x10 + 송신칸 * 4;
        int endesha = kifaa_thamani.밀리초();
        while ((kifaa_thamani.입출력정수읽기(hali_kituo) & 0x2000) == 0)
            if (kifaa_thamani.밀리초() - endesha > 100) return -110;
        int panga_ukubwa = urefu_thamani < 60 ? 60 : urefu_thamani;
        for (int kielezo = 0; kielezo < panga_ukubwa; kielezo++)
            kifaa_thamani.andika_kumbukumbu(kifaa_thamani.Mtandao_kumbukumbu() + 12288 + kielezo, kielezo < urefu_thamani ? data[kielezo] : 0);
        kifaa_thamani.입출력정수쓰기(hali_kituo, panga_ukubwa | 0x00080000);
        endesha = kifaa_thamani.밀리초();
        while ((kifaa_thamani.입출력정수읽기(hali_kituo) & 0xe0008000) == 0)
            if (kifaa_thamani.밀리초() - endesha > 100) return -110;
        if ((kifaa_thamani.입출력정수읽기(hali_kituo) & 0x8000) == 0) { 오류수++; return -5; }
        송신칸 = (송신칸 + 1) & 3;
        송신수++;
        return urefu_thamani;
    }

    static int 받기(int[] data) {
        if (입출력기준주소 == 0) return 0;
        if ((kifaa_thamani.입출력바이트읽기(입출력기준주소 + 0x3e) & 0x50) != 0) {
            오류수++;
            if (!Weka_upya_thamani()) 입출력기준주소 = 0;
            return 0;
        }
        if ((kifaa_thamani.입출력바이트읽기(입출력기준주소 + 0x37) & 1) != 0) return 0;
        int 머리 = kifaa_thamani.Mtandao_kumbukumbu() + 수신위치;
        int hali_thamani = 실행관리.짧은수(머리), panga_ukubwa = 실행관리.짧은수(머리 + 2);
        if (panga_ukubwa == 0xfff0) return 0; // DMA 진행 중
        if (panga_ukubwa < 4 || panga_ukubwa > 1518) {
            오류수++;
            if (!Weka_upya_thamani()) 입출력기준주소 = 0;
            return 0;
        }
        int urefu_thamani = panga_ukubwa - 4;
        if ((hali_thamani & 1) != 0) {
            for (int kielezo = 0; kielezo < urefu_thamani; kielezo++) data[kielezo] = kifaa_thamani.기억읽기(머리 + 4 + kielezo);
            수신수++;
        } else { urefu_thamani = 0; 오류수++; }
        수신위치 = (수신위치 + panga_ukubwa + 4 + 3) & ~3;
        수신위치 &= 8191;
        kifaa_thamani.입출력짧은수쓰기(입출력기준주소 + 0x38, (수신위치 - 16) & 65535);
        kifaa_thamani.입출력짧은수쓰기(입출력기준주소 + 0x3e, 0x000f);
        return urefu_thamani;
    }
}
