// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** PCI RTL8139 (10ec:8139), 단일 испрати_VALUE 버퍼와 8KiB 수신 Loop_VALUE. 인터럽트 대신 폴링한다. */
public final class Мрежа_двигател {
    static int 입출력기준주소 = 0;
    static int 수신위치 = 0, пренесува_отвор = 0;
    static int[] уред_адреса = new int[6];
    static int пренесува_COUNT = 0, 수신수 = 0, грешка_COUNT = 0;

    static int 설정읽기(int 장치번호, int Позиција) {
        уред_VALUE.입출력정수쓰기(0xcf8, 0x80000000 | (장치번호 << 11) | Позиција);
        return уред_VALUE.입출력정수읽기(0xcfc);
    }

    static boolean Подготви() {
        int 장치번호 = -1;
        for (int INDEX = 0; INDEX < 32; INDEX++) {
            if (설정읽기(INDEX, 0) == 0x813910ec) { 장치번호 = INDEX; break; }
        }
        if (장치번호 < 0) return false;
        int стандардна_вредност = 설정읽기(장치번호, 0x10);
        if ((стандардна_вредност & 1) == 0 || (стандардна_вредност & 0xfffffffc) < 0x100 || (стандардна_вредност & 0xfffffffc) > 65535) return false;
        입출력기준주소 = стандардна_вредност & 0xfffc;
        int Команда = 설정읽기(장치번호, 4);
        уред_VALUE.입출력정수쓰기(0xcf8, 0x80000004 | (장치번호 << 11));
        уред_VALUE.입출력짧은수쓰기(0xcfc, Команда | 5); // I/O 및 bus master Дозволи_VALUE, PCI статус_VALUE 비트는 건드리지 않음
        уред_VALUE.입출력바이트쓰기(입출력기준주소 + 0x52, 0);
        if (!Ресетирај_VALUE()) { 입출력기준주소 = 0; return false; }
        for (int INDEX = 0; INDEX < 6; INDEX++) уред_адреса[INDEX] = уред_VALUE.입출력바이트읽기(입출력기준주소 + INDEX);
        return true;
    }

    static boolean Ресетирај_VALUE() {
        уред_VALUE.입출력바이트쓰기(입출력기준주소 + 0x37, 0x10);
        int Изврши_2 = уред_VALUE.밀리초();
        while ((уред_VALUE.입출력바이트읽기(입출력기준주소 + 0x37) & 0x10) != 0)
            if (уред_VALUE.밀리초() - Изврши_2 > 100) return false;
        수신위치 = 0; пренесува_отвор = 0;
        уред_VALUE.입출력정수쓰기(입출력기준주소 + 0x30, уред_VALUE.Мрежа_Меморија());
        for (int INDEX = 0; INDEX < 4; INDEX++) уред_VALUE.입출력정수쓰기(입출력기준주소 + 0x20 + INDEX * 4, уред_VALUE.Мрежа_Меморија() + 12288);
        уред_VALUE.입출력짧은수쓰기(입출력기준주소 + 0x3c, 0);
        уред_VALUE.입출력짧은수쓰기(입출력기준주소 + 0x3e, 0xffff);
        уред_VALUE.입출력바이트쓰기(입출력기준주소 + 0x37, 0x0c);
        уред_VALUE.입출력정수쓰기(입출력기준주소 + 0x44, 0x0000e78a); // 자기주소/емитување_VALUE, wrap 연속 Store_VALUE, 8KiB
        уред_VALUE.입출력정수쓰기(입출력기준주소 + 0x40, 0x03000600);
        return true;
    }

    static int испрати(int[] податоци, int должина_VALUE) {
        if (입출력기준주소 == 0) return -19;
        if (должина_VALUE < 14 || должина_VALUE > 1514) return -90;
        int статус_порта = 입출력기준주소 + 0x10 + пренесува_отвор * 4;
        int Изврши_2 = уред_VALUE.밀리초();
        while ((уред_VALUE.입출력정수읽기(статус_порта) & 0x2000) == 0)
            if (уред_VALUE.밀리초() - Изврши_2 > 100) return -110;
        int Големина = должина_VALUE < 60 ? 60 : должина_VALUE;
        for (int INDEX = 0; INDEX < Големина; INDEX++)
            уред_VALUE.запиши_Меморија(уред_VALUE.Мрежа_Меморија() + 12288 + INDEX, INDEX < должина_VALUE ? податоци[INDEX] : 0);
        уред_VALUE.입출력정수쓰기(статус_порта, Големина | 0x00080000);
        Изврши_2 = уред_VALUE.밀리초();
        while ((уред_VALUE.입출력정수읽기(статус_порта) & 0xe0008000) == 0)
            if (уред_VALUE.밀리초() - Изврши_2 > 100) return -110;
        if ((уред_VALUE.입출력정수읽기(статус_порта) & 0x8000) == 0) { грешка_COUNT++; return -5; }
        пренесува_отвор = (пренесува_отвор + 1) & 3;
        пренесува_COUNT++;
        return должина_VALUE;
    }

    static int 받기(int[] податоци) {
        if (입출력기준주소 == 0) return 0;
        if ((уред_VALUE.입출력바이트읽기(입출력기준주소 + 0x3e) & 0x50) != 0) {
            грешка_COUNT++;
            if (!Ресетирај_VALUE()) 입출력기준주소 = 0;
            return 0;
        }
        if ((уред_VALUE.입출력바이트읽기(입출력기준주소 + 0x37) & 1) != 0) return 0;
        int 머리 = уред_VALUE.Мрежа_Меморија() + 수신위치;
        int статус_VALUE = 실행관리.짧은수(머리), Големина = 실행관리.짧은수(머리 + 2);
        if (Големина == 0xfff0) return 0; // DMA 진행 중
        if (Големина < 4 || Големина > 1518) {
            грешка_COUNT++;
            if (!Ресетирај_VALUE()) 입출력기준주소 = 0;
            return 0;
        }
        int должина_VALUE = Големина - 4;
        if ((статус_VALUE & 1) != 0) {
            for (int INDEX = 0; INDEX < должина_VALUE; INDEX++) податоци[INDEX] = уред_VALUE.기억읽기(머리 + 4 + INDEX);
            수신수++;
        } else { должина_VALUE = 0; грешка_COUNT++; }
        수신위치 = (수신위치 + Големина + 4 + 3) & ~3;
        수신위치 &= 8191;
        уред_VALUE.입출력짧은수쓰기(입출력기준주소 + 0x38, (수신위치 - 16) & 65535);
        уред_VALUE.입출력짧은수쓰기(입출력기준주소 + 0x3e, 0x000f);
        return должина_VALUE;
    }
}
