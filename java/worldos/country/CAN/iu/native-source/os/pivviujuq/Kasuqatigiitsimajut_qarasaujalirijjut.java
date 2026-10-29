// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** PCI RTL8139 (10ec:8139), 단일 nassiutili_atuutilik 버퍼와 8KiB 수신 piliqqittaajuq_atuutilik. 인터럽트 대신 폴링한다. */
public final class Kasuqatigiitsimajut_qarasaujalirijjut {
    static int 입출력기준주소 = 0;
    static int 수신위치 = 0, 송신칸 = 0;
    static int[] sunakkutaaq_turaarut = new int[6];
    static int 송신수 = 0, 수신수 = 0, 오류수 = 0;

    static int 설정읽기(int 장치번호, int 위치) {
        sunakkutaaq_atuutilik.입출력정수쓰기(0xcf8, 0x80000000 | (장치번호 << 11) | 위치);
        return sunakkutaaq_atuutilik.입출력정수읽기(0xcfc);
    }

    static boolean Parnalli() {
        int 장치번호 = -1;
        for (int nalunaiqsimavik = 0; nalunaiqsimavik < 32; nalunaiqsimavik++) {
            if (설정읽기(nalunaiqsimavik, 0) == 0x813910ec) { 장치번호 = nalunaiqsimavik; break; }
        }
        if (장치번호 < 0) return false;
        int Aturniliuvagiiqtut = 설정읽기(장치번호, 0x10);
        if ((Aturniliuvagiiqtut & 1) == 0 || (Aturniliuvagiiqtut & 0xfffffffc) < 0x100 || (Aturniliuvagiiqtut & 0xfffffffc) > 65535) return false;
        입출력기준주소 = Aturniliuvagiiqtut & 0xfffc;
        int piqujijjut = 설정읽기(장치번호, 4);
        sunakkutaaq_atuutilik.입출력정수쓰기(0xcf8, 0x80000004 | (장치번호 << 11));
        sunakkutaaq_atuutilik.입출력짧은수쓰기(0xcfc, piqujijjut | 5); // I/O 및 bus master Pijunnaqtilli_atuutilik, PCI qanuilinganiq_atuutilik 비트는 건드리지 않음
        sunakkutaaq_atuutilik.입출력바이트쓰기(입출력기준주소 + 0x52, 0);
        if (!pigiattiarli_atuutilik()) { 입출력기준주소 = 0; return false; }
        for (int nalunaiqsimavik = 0; nalunaiqsimavik < 6; nalunaiqsimavik++) sunakkutaaq_turaarut[nalunaiqsimavik] = sunakkutaaq_atuutilik.입출력바이트읽기(입출력기준주소 + nalunaiqsimavik);
        return true;
    }

    static boolean pigiattiarli_atuutilik() {
        sunakkutaaq_atuutilik.입출력바이트쓰기(입출력기준주소 + 0x37, 0x10);
        int 시작 = sunakkutaaq_atuutilik.밀리초();
        while ((sunakkutaaq_atuutilik.입출력바이트읽기(입출력기준주소 + 0x37) & 0x10) != 0)
            if (sunakkutaaq_atuutilik.밀리초() - 시작 > 100) return false;
        수신위치 = 0; 송신칸 = 0;
        sunakkutaaq_atuutilik.입출력정수쓰기(입출력기준주소 + 0x30, sunakkutaaq_atuutilik.Kasuqatigiitsimajut_puigujjaikkut());
        for (int nalunaiqsimavik = 0; nalunaiqsimavik < 4; nalunaiqsimavik++) sunakkutaaq_atuutilik.입출력정수쓰기(입출력기준주소 + 0x20 + nalunaiqsimavik * 4, sunakkutaaq_atuutilik.Kasuqatigiitsimajut_puigujjaikkut() + 12288);
        sunakkutaaq_atuutilik.입출력짧은수쓰기(입출력기준주소 + 0x3c, 0);
        sunakkutaaq_atuutilik.입출력짧은수쓰기(입출력기준주소 + 0x3e, 0xffff);
        sunakkutaaq_atuutilik.입출력바이트쓰기(입출력기준주소 + 0x37, 0x0c);
        sunakkutaaq_atuutilik.입출력정수쓰기(입출력기준주소 + 0x44, 0x0000e78a); // 자기주소/방송, wrap 연속 tuqqurli_atuutilik, 8KiB
        sunakkutaaq_atuutilik.입출력정수쓰기(입출력기준주소 + 0x40, 0x03000600);
        return true;
    }

    static int nassiutili(int[] titiqqat, int takininga_atuutilik) {
        if (입출력기준주소 == 0) return -19;
        if (takininga_atuutilik < 14 || takininga_atuutilik > 1514) return -90;
        int qanuilinganiq_kapputigaq = 입출력기준주소 + 0x10 + 송신칸 * 4;
        int 시작 = sunakkutaaq_atuutilik.밀리초();
        while ((sunakkutaaq_atuutilik.입출력정수읽기(qanuilinganiq_kapputigaq) & 0x2000) == 0)
            if (sunakkutaaq_atuutilik.밀리초() - 시작 > 100) return -110;
        int anininga = takininga_atuutilik < 60 ? 60 : takininga_atuutilik;
        for (int nalunaiqsimavik = 0; nalunaiqsimavik < anininga; nalunaiqsimavik++)
            sunakkutaaq_atuutilik.titiraq_puigujjaikkut(sunakkutaaq_atuutilik.Kasuqatigiitsimajut_puigujjaikkut() + 12288 + nalunaiqsimavik, nalunaiqsimavik < takininga_atuutilik ? titiqqat[nalunaiqsimavik] : 0);
        sunakkutaaq_atuutilik.입출력정수쓰기(qanuilinganiq_kapputigaq, anininga | 0x00080000);
        시작 = sunakkutaaq_atuutilik.밀리초();
        while ((sunakkutaaq_atuutilik.입출력정수읽기(qanuilinganiq_kapputigaq) & 0xe0008000) == 0)
            if (sunakkutaaq_atuutilik.밀리초() - 시작 > 100) return -110;
        if ((sunakkutaaq_atuutilik.입출력정수읽기(qanuilinganiq_kapputigaq) & 0x8000) == 0) { 오류수++; return -5; }
        송신칸 = (송신칸 + 1) & 3;
        송신수++;
        return takininga_atuutilik;
    }

    static int 받기(int[] titiqqat) {
        if (입출력기준주소 == 0) return 0;
        if ((sunakkutaaq_atuutilik.입출력바이트읽기(입출력기준주소 + 0x3e) & 0x50) != 0) {
            오류수++;
            if (!pigiattiarli_atuutilik()) 입출력기준주소 = 0;
            return 0;
        }
        if ((sunakkutaaq_atuutilik.입출력바이트읽기(입출력기준주소 + 0x37) & 1) != 0) return 0;
        int 머리 = sunakkutaaq_atuutilik.Kasuqatigiitsimajut_puigujjaikkut() + 수신위치;
        int qanuilinganiq_atuutilik = 실행관리.짧은수(머리), anininga = 실행관리.짧은수(머리 + 2);
        if (anininga == 0xfff0) return 0; // DMA 진행 중
        if (anininga < 4 || anininga > 1518) {
            오류수++;
            if (!pigiattiarli_atuutilik()) 입출력기준주소 = 0;
            return 0;
        }
        int takininga_atuutilik = anininga - 4;
        if ((qanuilinganiq_atuutilik & 1) != 0) {
            for (int nalunaiqsimavik = 0; nalunaiqsimavik < takininga_atuutilik; nalunaiqsimavik++) titiqqat[nalunaiqsimavik] = sunakkutaaq_atuutilik.기억읽기(머리 + 4 + nalunaiqsimavik);
            수신수++;
        } else { takininga_atuutilik = 0; 오류수++; }
        수신위치 = (수신위치 + anininga + 4 + 3) & ~3;
        수신위치 &= 8191;
        sunakkutaaq_atuutilik.입출력짧은수쓰기(입출력기준주소 + 0x38, (수신위치 - 16) & 65535);
        sunakkutaaq_atuutilik.입출력짧은수쓰기(입출력기준주소 + 0x3e, 0x000f);
        return takininga_atuutilik;
    }
}
