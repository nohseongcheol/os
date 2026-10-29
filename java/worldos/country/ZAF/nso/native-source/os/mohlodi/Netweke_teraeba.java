// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** PCI RTL8139 (10ec:8139), 단일 Romela_boleng 버퍼와 8KiB 수신 ditaelopoeletšwa_boleng. 인터럽트 대신 폴링한다. */
public final class Netweke_teraeba {
    static int 입출력기준주소 = 0;
    static int 수신위치 = 0, 송신칸 = 0;
    static int[] sedirišwa_atrese = new int[6];
    static int 송신수 = 0, 수신수 = 0, 오류수 = 0;

    static int 설정읽기(int 장치번호, int 위치) {
        sedirišwa_boleng.입출력정수쓰기(0xcf8, 0x80000000 | (장치번호 << 11) | 위치);
        return sedirišwa_boleng.입출력정수읽기(0xcfc);
    }

    static boolean Lokišetša() {
        int 장치번호 = -1;
        for (int lokela = 0; lokela < 32; lokela++) {
            if (설정읽기(lokela, 0) == 0x813910ec) { 장치번호 = lokela; break; }
        }
        if (장치번호 < 0) return false;
        int setsenywa_sa_tirelwa = 설정읽기(장치번호, 0x10);
        if ((setsenywa_sa_tirelwa & 1) == 0 || (setsenywa_sa_tirelwa & 0xfffffffc) < 0x100 || (setsenywa_sa_tirelwa & 0xfffffffc) > 65535) return false;
        입출력기준주소 = setsenywa_sa_tirelwa & 0xfffc;
        int Taelo = 설정읽기(장치번호, 4);
        sedirišwa_boleng.입출력정수쓰기(0xcf8, 0x80000004 | (장치번호 << 11));
        sedirišwa_boleng.입출력짧은수쓰기(0xcfc, Taelo | 5); // I/O 및 bus master Dumelela_boleng, PCI boemo_boleng 비트는 건드리지 않음
        sedirišwa_boleng.입출력바이트쓰기(입출력기준주소 + 0x52, 0);
        if (!setalefsa_boleng()) { 입출력기준주소 = 0; return false; }
        for (int lokela = 0; lokela < 6; lokela++) sedirišwa_atrese[lokela] = sedirišwa_boleng.입출력바이트읽기(입출력기준주소 + lokela);
        return true;
    }

    static boolean setalefsa_boleng() {
        sedirišwa_boleng.입출력바이트쓰기(입출력기준주소 + 0x37, 0x10);
        int Diriša = sedirišwa_boleng.밀리초();
        while ((sedirišwa_boleng.입출력바이트읽기(입출력기준주소 + 0x37) & 0x10) != 0)
            if (sedirišwa_boleng.밀리초() - Diriša > 100) return false;
        수신위치 = 0; 송신칸 = 0;
        sedirišwa_boleng.입출력정수쓰기(입출력기준주소 + 0x30, sedirišwa_boleng.Netweke_memori());
        for (int lokela = 0; lokela < 4; lokela++) sedirišwa_boleng.입출력정수쓰기(입출력기준주소 + 0x20 + lokela * 4, sedirišwa_boleng.Netweke_memori() + 12288);
        sedirišwa_boleng.입출력짧은수쓰기(입출력기준주소 + 0x3c, 0);
        sedirišwa_boleng.입출력짧은수쓰기(입출력기준주소 + 0x3e, 0xffff);
        sedirišwa_boleng.입출력바이트쓰기(입출력기준주소 + 0x37, 0x0c);
        sedirišwa_boleng.입출력정수쓰기(입출력기준주소 + 0x44, 0x0000e78a); // 자기주소/kgašo_boleng, wrap 연속 lota_boleng, 8KiB
        sedirišwa_boleng.입출력정수쓰기(입출력기준주소 + 0x40, 0x03000600);
        return true;
    }

    static int Romela(int[] data, int botelele_boleng) {
        if (입출력기준주소 == 0) return -19;
        if (botelele_boleng < 14 || botelele_boleng > 1514) return -90;
        int boemo_phote = 입출력기준주소 + 0x10 + 송신칸 * 4;
        int Diriša = sedirišwa_boleng.밀리초();
        while ((sedirišwa_boleng.입출력정수읽기(boemo_phote) & 0x2000) == 0)
            if (sedirišwa_boleng.밀리초() - Diriša > 100) return -110;
        int Bogolo = botelele_boleng < 60 ? 60 : botelele_boleng;
        for (int lokela = 0; lokela < Bogolo; lokela++)
            sedirišwa_boleng.ngwala_memori(sedirišwa_boleng.Netweke_memori() + 12288 + lokela, lokela < botelele_boleng ? data[lokela] : 0);
        sedirišwa_boleng.입출력정수쓰기(boemo_phote, Bogolo | 0x00080000);
        Diriša = sedirišwa_boleng.밀리초();
        while ((sedirišwa_boleng.입출력정수읽기(boemo_phote) & 0xe0008000) == 0)
            if (sedirišwa_boleng.밀리초() - Diriša > 100) return -110;
        if ((sedirišwa_boleng.입출력정수읽기(boemo_phote) & 0x8000) == 0) { 오류수++; return -5; }
        송신칸 = (송신칸 + 1) & 3;
        송신수++;
        return botelele_boleng;
    }

    static int 받기(int[] data) {
        if (입출력기준주소 == 0) return 0;
        if ((sedirišwa_boleng.입출력바이트읽기(입출력기준주소 + 0x3e) & 0x50) != 0) {
            오류수++;
            if (!setalefsa_boleng()) 입출력기준주소 = 0;
            return 0;
        }
        if ((sedirišwa_boleng.입출력바이트읽기(입출력기준주소 + 0x37) & 1) != 0) return 0;
        int 머리 = sedirišwa_boleng.Netweke_memori() + 수신위치;
        int boemo_boleng = 실행관리.짧은수(머리), Bogolo = 실행관리.짧은수(머리 + 2);
        if (Bogolo == 0xfff0) return 0; // DMA 진행 중
        if (Bogolo < 4 || Bogolo > 1518) {
            오류수++;
            if (!setalefsa_boleng()) 입출력기준주소 = 0;
            return 0;
        }
        int botelele_boleng = Bogolo - 4;
        if ((boemo_boleng & 1) != 0) {
            for (int lokela = 0; lokela < botelele_boleng; lokela++) data[lokela] = sedirišwa_boleng.기억읽기(머리 + 4 + lokela);
            수신수++;
        } else { botelele_boleng = 0; 오류수++; }
        수신위치 = (수신위치 + Bogolo + 4 + 3) & ~3;
        수신위치 &= 8191;
        sedirišwa_boleng.입출력짧은수쓰기(입출력기준주소 + 0x38, (수신위치 - 16) & 65535);
        sedirišwa_boleng.입출력짧은수쓰기(입출력기준주소 + 0x3e, 0x000f);
        return botelele_boleng;
    }
}
