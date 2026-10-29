// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** PCI RTL8139 (10ec:8139), 단일 kohereza_agaciro 버퍼와 8KiB 수신 gukora_mu_matsinda_agaciro. 인터럽트 대신 폴링한다. */
public final class Urusobemiyoboro_mukoresha {
    static int 입출력기준주소 = 0;
    static int 수신위치 = 0, 송신칸 = 0;
    static int[] igendanwa_aderesi = new int[6];
    static int 송신수 = 0, 수신수 = 0, 오류수 = 0;

    static int 설정읽기(int 장치번호, int 위치) {
        igendanwa_agaciro.입출력정수쓰기(0xcf8, 0x80000000 | (장치번호 << 11) | 위치);
        return igendanwa_agaciro.입출력정수읽기(0xcfc);
    }

    static boolean Gutegura() {
        int 장치번호 = -1;
        for (int umugerekashakiro = 0; umugerekashakiro < 32; umugerekashakiro++) {
            if (설정읽기(umugerekashakiro, 0) == 0x813910ec) { 장치번호 = umugerekashakiro; break; }
        }
        if (장치번호 < 0) return false;
        int agaciro_gasanzweho = 설정읽기(장치번호, 0x10);
        if ((agaciro_gasanzweho & 1) == 0 || (agaciro_gasanzweho & 0xfffffffc) < 0x100 || (agaciro_gasanzweho & 0xfffffffc) > 65535) return false;
        입출력기준주소 = agaciro_gasanzweho & 0xfffc;
        int Icyo_wifuza = 설정읽기(장치번호, 4);
        igendanwa_agaciro.입출력정수쓰기(0xcf8, 0x80000004 | (장치번호 << 11));
        igendanwa_agaciro.입출력짧은수쓰기(0xcfc, Icyo_wifuza | 5); // I/O 및 bus master Kwemerera_agaciro, PCI imimerere_agaciro 비트는 건드리지 않음
        igendanwa_agaciro.입출력바이트쓰기(입출력기준주소 + 0x52, 0);
        if (!kugaruraho_agaciro()) { 입출력기준주소 = 0; return false; }
        for (int umugerekashakiro = 0; umugerekashakiro < 6; umugerekashakiro++) igendanwa_aderesi[umugerekashakiro] = igendanwa_agaciro.입출력바이트읽기(입출력기준주소 + umugerekashakiro);
        return true;
    }

    static boolean kugaruraho_agaciro() {
        igendanwa_agaciro.입출력바이트쓰기(입출력기준주소 + 0x37, 0x10);
        int ihuriro = igendanwa_agaciro.밀리초();
        while ((igendanwa_agaciro.입출력바이트읽기(입출력기준주소 + 0x37) & 0x10) != 0)
            if (igendanwa_agaciro.밀리초() - ihuriro > 100) return false;
        수신위치 = 0; 송신칸 = 0;
        igendanwa_agaciro.입출력정수쓰기(입출력기준주소 + 0x30, igendanwa_agaciro.Urusobemiyoboro_ububiko());
        for (int umugerekashakiro = 0; umugerekashakiro < 4; umugerekashakiro++) igendanwa_agaciro.입출력정수쓰기(입출력기준주소 + 0x20 + umugerekashakiro * 4, igendanwa_agaciro.Urusobemiyoboro_ububiko() + 12288);
        igendanwa_agaciro.입출력짧은수쓰기(입출력기준주소 + 0x3c, 0);
        igendanwa_agaciro.입출력짧은수쓰기(입출력기준주소 + 0x3e, 0xffff);
        igendanwa_agaciro.입출력바이트쓰기(입출력기준주소 + 0x37, 0x0c);
        igendanwa_agaciro.입출력정수쓰기(입출력기준주소 + 0x44, 0x0000e78a); // 자기주소/방송, wrap 연속 Store_agaciro, 8KiB
        igendanwa_agaciro.입출력정수쓰기(입출력기준주소 + 0x40, 0x03000600);
        return true;
    }

    static int kohereza(int[] amakurushingiro, int uburebure_agaciro) {
        if (입출력기준주소 == 0) return -19;
        if (uburebure_agaciro < 14 || uburebure_agaciro > 1514) return -90;
        int imimerere_poti = 입출력기준주소 + 0x10 + 송신칸 * 4;
        int ihuriro = igendanwa_agaciro.밀리초();
        while ((igendanwa_agaciro.입출력정수읽기(imimerere_poti) & 0x2000) == 0)
            if (igendanwa_agaciro.밀리초() - ihuriro > 100) return -110;
        int Ingano = uburebure_agaciro < 60 ? 60 : uburebure_agaciro;
        for (int umugerekashakiro = 0; umugerekashakiro < Ingano; umugerekashakiro++)
            igendanwa_agaciro.kwandika_ububiko(igendanwa_agaciro.Urusobemiyoboro_ububiko() + 12288 + umugerekashakiro, umugerekashakiro < uburebure_agaciro ? amakurushingiro[umugerekashakiro] : 0);
        igendanwa_agaciro.입출력정수쓰기(imimerere_poti, Ingano | 0x00080000);
        ihuriro = igendanwa_agaciro.밀리초();
        while ((igendanwa_agaciro.입출력정수읽기(imimerere_poti) & 0xe0008000) == 0)
            if (igendanwa_agaciro.밀리초() - ihuriro > 100) return -110;
        if ((igendanwa_agaciro.입출력정수읽기(imimerere_poti) & 0x8000) == 0) { 오류수++; return -5; }
        송신칸 = (송신칸 + 1) & 3;
        송신수++;
        return uburebure_agaciro;
    }

    static int 받기(int[] amakurushingiro) {
        if (입출력기준주소 == 0) return 0;
        if ((igendanwa_agaciro.입출력바이트읽기(입출력기준주소 + 0x3e) & 0x50) != 0) {
            오류수++;
            if (!kugaruraho_agaciro()) 입출력기준주소 = 0;
            return 0;
        }
        if ((igendanwa_agaciro.입출력바이트읽기(입출력기준주소 + 0x37) & 1) != 0) return 0;
        int 머리 = igendanwa_agaciro.Urusobemiyoboro_ububiko() + 수신위치;
        int imimerere_agaciro = 실행관리.짧은수(머리), Ingano = 실행관리.짧은수(머리 + 2);
        if (Ingano == 0xfff0) return 0; // DMA 진행 중
        if (Ingano < 4 || Ingano > 1518) {
            오류수++;
            if (!kugaruraho_agaciro()) 입출력기준주소 = 0;
            return 0;
        }
        int uburebure_agaciro = Ingano - 4;
        if ((imimerere_agaciro & 1) != 0) {
            for (int umugerekashakiro = 0; umugerekashakiro < uburebure_agaciro; umugerekashakiro++) amakurushingiro[umugerekashakiro] = igendanwa_agaciro.기억읽기(머리 + 4 + umugerekashakiro);
            수신수++;
        } else { uburebure_agaciro = 0; 오류수++; }
        수신위치 = (수신위치 + Ingano + 4 + 3) & ~3;
        수신위치 &= 8191;
        igendanwa_agaciro.입출력짧은수쓰기(입출력기준주소 + 0x38, (수신위치 - 16) & 65535);
        igendanwa_agaciro.입출력짧은수쓰기(입출력기준주소 + 0x3e, 0x000f);
        return uburebure_agaciro;
    }
}
