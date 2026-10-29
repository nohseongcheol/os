// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** PCI RTL8139 (10ec:8139), 단일 җибәрү_VALUE 버퍼와 8KiB 수신 Loop_VALUE. 인터럽트 대신 폴링한다. */
public final class Челтәр_драйвер {
    static int 입출력기준주소 = 0;
    static int 수신위치 = 0, 송신칸 = 0;
    static int[] мобиль_адрес = new int[6];
    static int 송신수 = 0, 수신수 = 0, хата_COUNT = 0;

    static int 설정읽기(int 장치번호, int урнаштыру) {
        мобиль_VALUE.입출력정수쓰기(0xcf8, 0x80000000 | (장치번호 << 11) | урнаштыру);
        return мобиль_VALUE.입출력정수읽기(0xcfc);
    }

    static boolean Әзерләү() {
        int 장치번호 = -1;
        for (int INDEX = 0; INDEX < 32; INDEX++) {
            if (설정읽기(INDEX, 0) == 0x813910ec) { 장치번호 = INDEX; break; }
        }
        if (장치번호 < 0) return false;
        int килешенгәнчә_кыйммәт = 설정읽기(장치번호, 0x10);
        if ((килешенгәнчә_кыйммәт & 1) == 0 || (килешенгәнчә_кыйммәт & 0xfffffffc) < 0x100 || (килешенгәнчә_кыйммәт & 0xfffffffc) > 65535) return false;
        입출력기준주소 = килешенгәнчә_кыйммәт & 0xfffc;
        int команда = 설정읽기(장치번호, 4);
        мобиль_VALUE.입출력정수쓰기(0xcf8, 0x80000004 | (장치번호 << 11));
        мобиль_VALUE.입출력짧은수쓰기(0xcfc, команда | 5); // I/O 및 bus master Рөхсәт_VALUE, PCI халәт_VALUE 비트는 건드리지 않음
        мобиль_VALUE.입출력바이트쓰기(입출력기준주소 + 0x52, 0);
        if (!ташлату_VALUE()) { 입출력기준주소 = 0; return false; }
        for (int INDEX = 0; INDEX < 6; INDEX++) мобиль_адрес[INDEX] = мобиль_VALUE.입출력바이트읽기(입출력기준주소 + INDEX);
        return true;
    }

    static boolean ташлату_VALUE() {
        мобиль_VALUE.입출력바이트쓰기(입출력기준주소 + 0x37, 0x10);
        int эшләтү = мобиль_VALUE.밀리초();
        while ((мобиль_VALUE.입출력바이트읽기(입출력기준주소 + 0x37) & 0x10) != 0)
            if (мобиль_VALUE.밀리초() - эшләтү > 100) return false;
        수신위치 = 0; 송신칸 = 0;
        мобиль_VALUE.입출력정수쓰기(입출력기준주소 + 0x30, мобиль_VALUE.Челтәр_Хәтер());
        for (int INDEX = 0; INDEX < 4; INDEX++) мобиль_VALUE.입출력정수쓰기(입출력기준주소 + 0x20 + INDEX * 4, мобиль_VALUE.Челтәр_Хәтер() + 12288);
        мобиль_VALUE.입출력짧은수쓰기(입출력기준주소 + 0x3c, 0);
        мобиль_VALUE.입출력짧은수쓰기(입출력기준주소 + 0x3e, 0xffff);
        мобиль_VALUE.입출력바이트쓰기(입출력기준주소 + 0x37, 0x0c);
        мобиль_VALUE.입출력정수쓰기(입출력기준주소 + 0x44, 0x0000e78a); // 자기주소/киңтапшыру_VALUE, wrap 연속 Store_VALUE, 8KiB
        мобиль_VALUE.입출력정수쓰기(입출력기준주소 + 0x40, 0x03000600);
        return true;
    }

    static int җибәрү(int[] мәгълүмат, int озынлык_VALUE) {
        if (입출력기준주소 == 0) return -19;
        if (озынлык_VALUE < 14 || озынлык_VALUE > 1514) return -90;
        int халәт_порт = 입출력기준주소 + 0x10 + 송신칸 * 4;
        int эшләтү = мобиль_VALUE.밀리초();
        while ((мобиль_VALUE.입출력정수읽기(халәт_порт) & 0x2000) == 0)
            if (мобиль_VALUE.밀리초() - эшләтү > 100) return -110;
        int үлчәмен_үзгәртү = озынлык_VALUE < 60 ? 60 : озынлык_VALUE;
        for (int INDEX = 0; INDEX < үлчәмен_үзгәртү; INDEX++)
            мобиль_VALUE.язу_Хәтер(мобиль_VALUE.Челтәр_Хәтер() + 12288 + INDEX, INDEX < озынлык_VALUE ? мәгълүмат[INDEX] : 0);
        мобиль_VALUE.입출력정수쓰기(халәт_порт, үлчәмен_үзгәртү | 0x00080000);
        эшләтү = мобиль_VALUE.밀리초();
        while ((мобиль_VALUE.입출력정수읽기(халәт_порт) & 0xe0008000) == 0)
            if (мобиль_VALUE.밀리초() - эшләтү > 100) return -110;
        if ((мобиль_VALUE.입출력정수읽기(халәт_порт) & 0x8000) == 0) { хата_COUNT++; return -5; }
        송신칸 = (송신칸 + 1) & 3;
        송신수++;
        return озынлык_VALUE;
    }

    static int 받기(int[] мәгълүмат) {
        if (입출력기준주소 == 0) return 0;
        if ((мобиль_VALUE.입출력바이트읽기(입출력기준주소 + 0x3e) & 0x50) != 0) {
            хата_COUNT++;
            if (!ташлату_VALUE()) 입출력기준주소 = 0;
            return 0;
        }
        if ((мобиль_VALUE.입출력바이트읽기(입출력기준주소 + 0x37) & 1) != 0) return 0;
        int 머리 = мобиль_VALUE.Челтәр_Хәтер() + 수신위치;
        int халәт_VALUE = 실행관리.짧은수(머리), үлчәмен_үзгәртү = 실행관리.짧은수(머리 + 2);
        if (үлчәмен_үзгәртү == 0xfff0) return 0; // DMA 진행 중
        if (үлчәмен_үзгәртү < 4 || үлчәмен_үзгәртү > 1518) {
            хата_COUNT++;
            if (!ташлату_VALUE()) 입출력기준주소 = 0;
            return 0;
        }
        int озынлык_VALUE = үлчәмен_үзгәртү - 4;
        if ((халәт_VALUE & 1) != 0) {
            for (int INDEX = 0; INDEX < озынлык_VALUE; INDEX++) мәгълүмат[INDEX] = мобиль_VALUE.기억읽기(머리 + 4 + INDEX);
            수신수++;
        } else { озынлык_VALUE = 0; хата_COUNT++; }
        수신위치 = (수신위치 + үлчәмен_үзгәртү + 4 + 3) & ~3;
        수신위치 &= 8191;
        мобиль_VALUE.입출력짧은수쓰기(입출력기준주소 + 0x38, (수신위치 - 16) & 65535);
        мобиль_VALUE.입출력짧은수쓰기(입출력기준주소 + 0x3e, 0x000f);
        return озынлык_VALUE;
    }
}
