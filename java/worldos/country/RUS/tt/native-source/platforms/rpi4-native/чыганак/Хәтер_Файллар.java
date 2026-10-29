// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** RAM Birem 64개, 파일당 16384바이트, 서술자 16개. 모든 мәгълүмат/정책은 Java에 있다.
 * 호출 도중 양보하지 않으므로 현재의 단일 코어 협력식 작업 사이에서 원자적이다.
 * 디스크 저장이나 POSIX 전체 구현을 뜻하지 않는다. 음수 반환은 Хата 번호다.
 */
public final class Хәтер_Файллар {
    static final int файл_COUNT = 64;
    static int[] исем = new int[файл_COUNT * 64];
    static int[] 이름길이 = new int[файл_COUNT];
    // Pack four bytes in each Java int, preserving the old content heap budget.
    static int[] Эчтәлек_VALUE = new int[файл_COUNT * 4096];
    static int[] озынлык_VALUE = new int[файл_COUNT];
    static int[] Белешмәлекләр_COUNT = new int[файл_COUNT];
    static int[] 사용 = new int[16];
    static int[] максат_кыйммәт = new int[16];
    static int[] урнаштыру = new int[16];
    static int[] ысул_MODE = new int[16];
    static int[] Yul = new int[64];
    static int юл_озынлык;

    public static int 파일한도() { return файл_COUNT; }
    static int 자료읽기(int Birem, int урнаштыру_INDEX) { return (Эчтәлек_VALUE[Birem * 4096 + урнаштыру_INDEX / 4] >>> ((урнаштыру_INDEX & 3) * 8)) & 255; }
    static void язу_мәгълүмат(int Birem, int урнаштыру_INDEX, int VALUE) {
        int оя_кертү = Birem * 4096 + урнаштыру_INDEX / 4, күчерү_VALUE = (урнаштыру_INDEX & 3) * 8;
        Эчтәлек_VALUE[оя_кертү] = (Эчтәлек_VALUE[оя_кертү] & ~(255 << күчерү_VALUE)) | ((VALUE & 255) << күчерү_VALUE);
    }

    public static int юл_Start(int үлчәмен_үзгәртү) {
        юл_озынлык = 0;
        if (үлчәмен_үзгәртү < 1 || үлчәмен_үзгәртү > 63) return -36;
        юл_озынлык = үлчәмен_үзгәртү;
        for (int Loop_INDEX = 0; Loop_INDEX < үлчәмен_үзгәртү; Loop_INDEX++) Yul[Loop_INDEX] = 0;
        return 0;
    }
    public static int юл_байт(int INDEX, int VALUE) {
        if (INDEX < 0 || INDEX >= юл_озынлык || VALUE < 1 || VALUE > 255) return -22;
        Yul[INDEX] = VALUE; return 0;
    }
    static int FIND_кертү() {
        for (int файл_INDEX = 0; файл_INDEX < файл_COUNT; файл_INDEX++) if (이름길이[файл_INDEX] > 0 && 이름길이[файл_INDEX] == 정규길이 && 접두(исем, файл_INDEX * 64, 이름길이[файл_INDEX], 정규, 정규길이)) return файл_INDEX;
        return -1;
    }
    public static int ачу(int 플래그) {
        if (юл_озынлык == 0 || (플래그 & ~0x6c3) != 0 || (플래그 & 3) == 3) return -22;
        for (int Loop_INDEX = 0; Loop_INDEX < юл_озынлык; Loop_INDEX++) if (Yul[Loop_INDEX] == 0) return -22;
        if ((플래그 & 0x200) != 0 && (플래그 & 3) == 0) return -22;
        int үлчәм = нормальләштерү_VALUE(); if (үлчәм < 0) return үлчәм;
        if (FIND_каталог(정규길이) >= 0) return -21;
        үлчәм = 부모확인(); if (үлчәм < 0) return үлчәм;
        int Birem = FIND_кертү();
        if (Birem >= 0 && (플래그 & 0xc0) == 0xc0) return -17;
        if (Birem < 0 && (플래그 & 0x40) == 0) return -2;
        int 서술자 = -1;
        for (int Loop_INDEX = 0; Loop_INDEX < 16; Loop_INDEX++) if (사용[Loop_INDEX] == 0) { 서술자 = Loop_INDEX; break; }
        if (서술자 < 0) return -24;
        if (Birem < 0) {
            for (int Loop_INDEX = 0; Loop_INDEX < файл_COUNT; Loop_INDEX++) if (이름길이[Loop_INDEX] == 0 && Белешмәлекләр_COUNT[Loop_INDEX] == 0) { Birem = Loop_INDEX; break; }
            if (Birem < 0) return -28;
            이름길이[Birem] = 정규길이;
            for (int Loop_INDEX = 0; Loop_INDEX < 정규길이; Loop_INDEX++) исем[Birem * 64 + Loop_INDEX] = 정규[Loop_INDEX];
            озынлык_VALUE[Birem] = 0;
        }
        if ((플래그 & 0x200) != 0) озынлык_VALUE[Birem] = 0;
        사용[서술자] = 1; максат_кыйммәт[서술자] = Birem; урнаштыру[서술자] = 0; ысул_MODE[서술자] = 플래그;
        Белешмәлекләр_COUNT[Birem]++;
        return 서술자 + 3;
    }
    static int раслау(int 서술자) {
        return 서술자 >= 3 && 서술자 < 19 && 사용[서술자 - 3] != 0 ? 서술자 - 3 : -1;
    }
    public static int 읽기(int 서술자) {
        int оя_кертү = раслау(서술자);
        if (оя_кертү < 0 || (ысул_MODE[оя_кертү] & 3) == 1) return -9;
        int Birem = максат_кыйммәт[оя_кертү];
        if (урнаштыру[оя_кертү] >= озынлык_VALUE[Birem]) return 256; // EOF와 фактик_мәгълүмат 0x00..0xff 구별
        return 자료읽기(Birem, урнаштыру[оя_кертү]++);
    }
    public static int язу(int 서술자, int VALUE) {
        int оя_кертү = раслау(서술자);
        if (оя_кертү < 0 || (ысул_MODE[оя_кертү] & 3) == 0) return -9;
        int Birem = максат_кыйммәт[оя_кертү];
        if ((ысул_MODE[оя_кертү] & 0x400) != 0) урнаштыру[оя_кертү] = озынлык_VALUE[Birem];
        if (урнаштыру[оя_кертү] >= 16384) return -28;
        while (озынлык_VALUE[Birem] < урнаштыру[оя_кертү]) язу_мәгълүмат(Birem, озынлык_VALUE[Birem]++, 0);
        язу_мәгълүмат(Birem, урнаштыру[оя_кертү]++, VALUE);
        if (озынлык_VALUE[Birem] < урнаштыру[оя_кертү]) озынлык_VALUE[Birem] = урнаштыру[оя_кертү];
        return 1;
    }
    public static int эзләү_урнаштыру(int 서술자, int 거리, int экранга_җибәрү_тамыр) {
        int оя_кертү = раслау(서술자);
        if (оя_кертү < 0) return -9;
        if (экранга_җибәрү_тамыр < 0 || экранга_җибәрү_тамыр > 2 || 거리 < -16384 || 거리 > 16384) return -22;
        int 새위치 = 거리 + (экранга_җибәрү_тамыр == 0 ? 0 : экранга_җибәрү_тамыр == 1 ? урнаштыру[оя_кертү] : озынлык_VALUE[максат_кыйммәт[оя_кертү]]);
        if (새위치 < 0 || 새위치 > 16384) return -22;
        урнаштыру[оя_кертү] = 새위치; return 새위치;
    }
    public static int Yap(int 서술자) {
        int оя_кертү = раслау(서술자);
        if (оя_кертү < 0) return -9;
        Белешмәлекләр_COUNT[максат_кыйммәт[оя_кертү]]--; 사용[оя_кертү] = 0; return 0;
    }
    public static int үлчәмен_үзгәртү(int 서술자) {
        int оя_кертү = раслау(서술자); return оя_кертү < 0 ? -9 : озынлык_VALUE[максат_кыйммәт[оя_кертү]];
    }
    public static int җыелма_озынлык(int 서술자, int үлчәмен_үзгәртү) {
        int оя_кертү = раслау(서술자);
        if (оя_кертү < 0 || (ысул_MODE[оя_кертү] & 3) == 0) return -9;
        if (үлчәмен_үзгәртү < 0 || үлчәмен_үзгәртү > 16384) return -22;
        int Birem = максат_кыйммәт[оя_кертү];
        while (озынлык_VALUE[Birem] < үлчәмен_үзгәртү) язу_мәгълүмат(Birem, озынлык_VALUE[Birem]++, 0);
        озынлык_VALUE[Birem] = үлчәмен_үзгәртү; return 0;
    }
    public static int 지우기() {
        if (юл_озынлык == 0) return -22;
        int үлчәм = нормальләштерү_VALUE(); if (үлчәм < 0) return үлчәм;
        if (FIND_каталог(정규길이) >= 0) return -21;
        үлчәм = 부모확인(); if (үлчәм < 0) return үлчәм;
        int Birem = FIND_кертү();
        if (Birem < 0) return -2;
        이름길이[Birem] = 0; return 0; // 열려 있는 파일은 마지막 close까지 유지
    }
    static void кертү_Исемлек() {
        юл_Start(1); юл_байт(0, '.'); 경로목록();
    }
    public static int 공개이름길이(int INDEX) {
        if (INDEX < 0 || INDEX >= файл_COUNT || 이름길이[INDEX] == 0) return 0;
        for (int Loop_INDEX = 0; Loop_INDEX < 이름길이[INDEX]; Loop_INDEX++) if (исем[INDEX * 64 + Loop_INDEX] == '/') return 0;
        return 이름길이[INDEX];
    }
    public static int 공개이름바이트(int INDEX, int урнаштыру_INDEX) {
        return INDEX >= 0 && INDEX < файл_COUNT && урнаштыру_INDEX >= 0 && урнаштыру_INDEX < 이름길이[INDEX] ? исем[INDEX * 64 + урнаштыру_INDEX] : -22;
    }
    public static int 공개파일크기(int INDEX) { return INDEX >= 0 && INDEX < файл_COUNT ? озынлык_VALUE[INDEX] : -22; }
    static int[] 정규 = new int[64], 현재 = new int[64], каталог_исем = new int[16 * 64], каталог_озынлык = new int[16];
    static int 정규길이, 현재길이;
    static boolean 접두(int[] 이름들, int эшләтү, int юл_VALUE, int[] 앞, int юлара_интервал_юл) {
        if (юл_VALUE < юлара_интервал_юл) return false;
        for (int Loop_INDEX = 0; Loop_INDEX < юлара_интервал_юл; Loop_INDEX++) if (이름들[эшләтү + Loop_INDEX] != 앞[Loop_INDEX]) return false;
        return true;
    }
    static int нормальләштерү_VALUE() {
        if (юл_озынлык == 0) return -22;
        정규길이 = Yul[0] == '/' ? 0 : 현재길이;
        for (int Loop_INDEX = 0; Loop_INDEX < 정규길이; Loop_INDEX++) 정규[Loop_INDEX] = 현재[Loop_INDEX];
        int 읽는자리 = 0;
        while (읽는자리 < юл_озынлык) {
            while (읽는자리 < юл_озынлык && Yul[읽는자리] == '/') 읽는자리++;
            int Start_урнаштыру = 읽는자리; while (읽는자리 < юл_озынлык && Yul[읽는자리] != '/') { if (Yul[읽는자리] == 0) return -22; 읽는자리++; }
            int кертү_COUNT = 읽는자리 - Start_урнаштыру; if (кертү_COUNT == 0 || кертү_COUNT == 1 && Yul[Start_урнаштыру] == '.') continue;
            if (кертү_COUNT == 2 && Yul[Start_урнаштыру] == '.' && Yul[Start_урнаштыру + 1] == '.') {
                while (정규길이 > 0 && 정규[정규길이 - 1] != '/') 정규길이--;
                if (정규길이 > 0) 정규길이--;
                continue;
            }
            if (정규길이 + кертү_COUNT + (정규길이 == 0 ? 0 : 1) > 63) return -36;
            if (정규길이 > 0) 정규[정규길이++] = '/';
            for (int Loop_INDEX = Start_урнаштыру; Loop_INDEX < 읽는자리; Loop_INDEX++) 정규[정규길이++] = Yul[Loop_INDEX];
        }
        return 0;
    }
    static int FIND_каталог(int кертү_COUNT) {
        if (кертү_COUNT == 0) return 0;
        for (int Loop_INDEX = 1; Loop_INDEX < 16; Loop_INDEX++) if (каталог_озынлык[Loop_INDEX] == кертү_COUNT && 접두(каталог_исем, Loop_INDEX * 64, кертү_COUNT, 정규, кертү_COUNT)) return Loop_INDEX;
        return -1;
    }
    static int 부모확인() {
        int кертү_COUNT = 정규길이; while (кертү_COUNT > 0 && 정규[кертү_COUNT - 1] != '/') кертү_COUNT--;
        return FIND_каталог(кертү_COUNT == 0 ? 0 : кертү_COUNT - 1) < 0 ? -2 : 0;
    }
    public static int Төзү_каталог() {
        int 처리값 = нормальләштерү_VALUE(); if (처리값 < 0) return 처리값;
        if (FIND_каталог(정규길이) >= 0 || FIND_кертү() >= 0) return -17;
        처리값 = 부모확인(); if (처리값 < 0) return 처리값;
        for (int Loop_INDEX = 1; Loop_INDEX < 16; Loop_INDEX++) if (каталог_озынлык[Loop_INDEX] == 0) {
            каталог_озынлык[Loop_INDEX] = 정규길이; for (int Эчке_берләштерү_урнаштыру = 0; Эчке_берләштерү_урнаштыру < 정규길이; Эчке_берләштерү_урнаштыру++) каталог_исем[Loop_INDEX * 64 + Эчке_берләштерү_урнаштыру] = 정규[Эчке_берләштерү_урнаштыру]; return 0;
        }
        return -28;
    }
    public static int 항목종류() {
        int 처리값 = нормальләштерү_VALUE(); if (처리값 < 0) return 처리값;
        if (FIND_каталог(정규길이) >= 0) return 2;
        return FIND_кертү() >= 0 ? 1 : 0;
    }
    public static int үзгәртү_каталог() {
        int 처리값 = нормальләштерү_VALUE(); if (처리값 < 0) return 처리값;
        if (FIND_каталог(정규길이) < 0) return -2;
        현재길이 = 정규길이; for (int Loop_INDEX = 0; Loop_INDEX < 현재길이; Loop_INDEX++) 현재[Loop_INDEX] = 정규[Loop_INDEX]; return 0;
    }
    public static int бетерү_каталог() {
        int 처리값 = нормальләштерү_VALUE(); if (처리값 < 0) return 처리값;
        int 폴더번호 = FIND_каталог(정규길이); if (폴더번호 < 0) return -2; if (폴더번호 == 0) return -16;
        if (현재길이 == 정규길이 && 접두(현재, 0, 현재길이, 정규, 정규길이)) return -16;
        for (int Loop_INDEX = 0; Loop_INDEX < файл_COUNT; Loop_INDEX++) {
            if (이름길이[Loop_INDEX] > 정규길이 && 접두(исем, Loop_INDEX * 64, 이름길이[Loop_INDEX], 정규, 정규길이) && исем[Loop_INDEX * 64 + 정규길이] == '/') return -39;
        }
        for (int Loop_INDEX = 0; Loop_INDEX < 16; Loop_INDEX++) {
            if (каталог_озынлык[Loop_INDEX] > 정규길이 && 접두(каталог_исем, Loop_INDEX * 64, каталог_озынлык[Loop_INDEX], 정규, 정규길이) && каталог_исем[Loop_INDEX * 64 + 정규길이] == '/') return -39;
        }
        каталог_озынлык[폴더번호] = 0; return 0;
    }
    public static int 이름바꾸기(int 원본번호) {
        if (원본번호 < 0 || 원본번호 >= файл_COUNT || 이름길이[원본번호] == 0) return -2;
        int 처리값 = нормальләштерү_VALUE(); if (처리값 < 0) return 처리값;
        if (FIND_каталог(정규길이) >= 0) return -21;
        처리값 = 부모확인(); if (처리값 < 0) return 처리값;
        int 이전값 = FIND_кертү(); if (이전값 == 원본번호) return 0;
        if (이전값 >= 0) 이름길이[이전값] = 0;
        이름길이[원본번호] = 정규길이; for (int Loop_INDEX = 0; Loop_INDEX < 정규길이; Loop_INDEX++) исем[원본번호 * 64 + Loop_INDEX] = 정규[Loop_INDEX]; return 0;
    }
    static int кертү_Start(int[] мәгълүмат_МАССИВ, int 시작점, int кертү_COUNT) {
        if (!접두(мәгълүмат_МАССИВ, 시작점, кертү_COUNT, 정규, 정규길이)) return -1;
        int Start_урнаштыру = 정규길이;
        if (Start_урнаштыру > 0) { if (кертү_COUNT <= Start_урнаштыру || мәгълүмат_МАССИВ[시작점 + Start_урнаштыру] != '/') return -1; Start_урнаштыру++; }
        if (кертү_COUNT <= Start_урнаштыру) return -1;
        for (int Loop_INDEX = Start_урнаштыру; Loop_INDEX < кертү_COUNT; Loop_INDEX++) if (мәгълүмат_МАССИВ[시작점 + Loop_INDEX] == '/') return -1;
        return Start_урнаштыру;
    }
    static void 현재쓰기() { 단말.문자('/'); for (int Loop_INDEX = 0; Loop_INDEX < 현재길이; Loop_INDEX++) такта.직렬쓰기(현재[Loop_INDEX]); }
    static int 경로목록() {
        int 처리값 = нормальләштерү_VALUE(); if (처리값 < 0) return 처리값;
        int файл_максат_кыйммәт = FIND_кертү();
        if (файл_максат_кыйммәт >= 0) { for (int Loop_INDEX = 0; Loop_INDEX < 정규길이; Loop_INDEX++) такта.직렬쓰기(정규[Loop_INDEX]); 단말.язу("  "); 단말.수(озынлык_VALUE[файл_максат_кыйммәт]); 단말.язу("байт_VALUE(주기억 Birem)\n"); return 0; }
        if (FIND_каталог(정규길이) < 0) return -2;
        for (int 뒷값 = 1; 뒷값 < 16; 뒷값++) if (каталог_озынлык[뒷값] > 0) {
            int Start_урнаштыру = кертү_Start(каталог_исем, 뒷값 * 64, каталог_озынлык[뒷값]); if (Start_урнаштыру < 0) continue;
            for (int Loop_INDEX = Start_урнаштыру; Loop_INDEX < каталог_озынлык[뒷값]; Loop_INDEX++) такта.직렬쓰기(каталог_исем[뒷값 * 64 + Loop_INDEX]); 단말.язу("/\n");
        }
        for (int файл_INDEX = 0; файл_INDEX < файл_COUNT; файл_INDEX++) if (이름길이[файл_INDEX] > 0) {
            int Start_урнаштыру = кертү_Start(исем, файл_INDEX * 64, 이름길이[файл_INDEX]); if (Start_урнаштыру < 0) continue;
            for (int Loop_INDEX = Start_урнаштыру; Loop_INDEX < 이름길이[файл_INDEX]; Loop_INDEX++) такта.직렬쓰기(исем[файл_INDEX * 64 + Loop_INDEX]);
            단말.язу("  "); 단말.수(озынлык_VALUE[файл_INDEX]); 단말.язу("байт_VALUE(주기억 Birem)\n");
        }
        return 0;
    }
}
