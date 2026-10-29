// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** RAM Датотека 64개, 파일당 16384바이트, 서술자 16개. 모든 податоци/정책은 Java에 있다.
 * 호출 도중 양보하지 않으므로 현재의 단일 코어 협력식 작업 사이에서 원자적이다.
 * 디스크 저장이나 POSIX 전체 구현을 뜻하지 않는다. 음수 반환은 ГРЕШКА 번호다.
 */
public final class Меморија_Датотеки {
    static final int датотека_COUNT = 64;
    static int[] Име = new int[датотека_COUNT * 64];
    static int[] 이름길이 = new int[датотека_COUNT];
    // Pack four bytes in each Java int, preserving the old content heap budget.
    static int[] Содржина_VALUE = new int[датотека_COUNT * 4096];
    static int[] должина_VALUE = new int[датотека_COUNT];
    static int[] Референци_COUNT = new int[датотека_COUNT];
    static int[] 사용 = new int[16];
    static int[] цел = new int[16];
    static int[] Позиција = new int[16];
    static int[] метод_MODE = new int[16];
    static int[] ПАТЕКА = new int[64];
    static int патека_должина;

    public static int 파일한도() { return датотека_COUNT; }
    static int 자료읽기(int Датотека, int позиционирање_INDEX) { return (Содржина_VALUE[Датотека * 4096 + позиционирање_INDEX / 4] >>> ((позиционирање_INDEX & 3) * 8)) & 255; }
    static void запиши_податоци(int Датотека, int позиционирање_INDEX, int VALUE) {
        int отвор_внес = Датотека * 4096 + позиционирање_INDEX / 4, премести_VALUE = (позиционирање_INDEX & 3) * 8;
        Содржина_VALUE[отвор_внес] = (Содржина_VALUE[отвор_внес] & ~(255 << премести_VALUE)) | ((VALUE & 255) << премести_VALUE);
    }

    public static int патека_Start(int Големина) {
        патека_должина = 0;
        if (Големина < 1 || Големина > 63) return -36;
        патека_должина = Големина;
        for (int Loop_INDEX = 0; Loop_INDEX < Големина; Loop_INDEX++) ПАТЕКА[Loop_INDEX] = 0;
        return 0;
    }
    public static int патека_бајт(int INDEX, int VALUE) {
        if (INDEX < 0 || INDEX >= патека_должина || VALUE < 1 || VALUE > 255) return -22;
        ПАТЕКА[INDEX] = VALUE; return 0;
    }
    static int FIND_внес() {
        for (int датотека_INDEX = 0; датотека_INDEX < датотека_COUNT; датотека_INDEX++) if (이름길이[датотека_INDEX] > 0 && 이름길이[датотека_INDEX] == 정규길이 && 접두(Име, датотека_INDEX * 64, 이름길이[датотека_INDEX], 정규, 정규길이)) return датотека_INDEX;
        return -1;
    }
    public static int Отвори(int 플래그) {
        if (патека_должина == 0 || (플래그 & ~0x6c3) != 0 || (플래그 & 3) == 3) return -22;
        for (int Loop_INDEX = 0; Loop_INDEX < патека_должина; Loop_INDEX++) if (ПАТЕКА[Loop_INDEX] == 0) return -22;
        if ((플래그 & 0x200) != 0 && (플래그 & 3) == 0) return -22;
        int мерка = нормализирање_VALUE(); if (мерка < 0) return мерка;
        if (FIND_Именик(정규길이) >= 0) return -21;
        мерка = 부모확인(); if (мерка < 0) return мерка;
        int Датотека = FIND_внес();
        if (Датотека >= 0 && (플래그 & 0xc0) == 0xc0) return -17;
        if (Датотека < 0 && (플래그 & 0x40) == 0) return -2;
        int 서술자 = -1;
        for (int Loop_INDEX = 0; Loop_INDEX < 16; Loop_INDEX++) if (사용[Loop_INDEX] == 0) { 서술자 = Loop_INDEX; break; }
        if (서술자 < 0) return -24;
        if (Датотека < 0) {
            for (int Loop_INDEX = 0; Loop_INDEX < датотека_COUNT; Loop_INDEX++) if (이름길이[Loop_INDEX] == 0 && Референци_COUNT[Loop_INDEX] == 0) { Датотека = Loop_INDEX; break; }
            if (Датотека < 0) return -28;
            이름길이[Датотека] = 정규길이;
            for (int Loop_INDEX = 0; Loop_INDEX < 정규길이; Loop_INDEX++) Име[Датотека * 64 + Loop_INDEX] = 정규[Loop_INDEX];
            должина_VALUE[Датотека] = 0;
        }
        if ((플래그 & 0x200) != 0) должина_VALUE[Датотека] = 0;
        사용[서술자] = 1; цел[서술자] = Датотека; Позиција[서술자] = 0; метод_MODE[서술자] = 플래그;
        Референци_COUNT[Датотека]++;
        return 서술자 + 3;
    }
    static int провери(int 서술자) {
        return 서술자 >= 3 && 서술자 < 19 && 사용[서술자 - 3] != 0 ? 서술자 - 3 : -1;
    }
    public static int Читај(int 서술자) {
        int отвор_внес = провери(서술자);
        if (отвор_внес < 0 || (метод_MODE[отвор_внес] & 3) == 1) return -9;
        int Датотека = цел[отвор_внес];
        if (Позиција[отвор_внес] >= должина_VALUE[Датотека]) return 256; // EOF와 реален_податоци 0x00..0xff 구별
        return 자료읽기(Датотека, Позиција[отвор_внес]++);
    }
    public static int Запиши(int 서술자, int VALUE) {
        int отвор_внес = провери(서술자);
        if (отвор_внес < 0 || (метод_MODE[отвор_внес] & 3) == 0) return -9;
        int Датотека = цел[отвор_внес];
        if ((метод_MODE[отвор_внес] & 0x400) != 0) Позиција[отвор_внес] = должина_VALUE[Датотека];
        if (Позиција[отвор_внес] >= 16384) return -28;
        while (должина_VALUE[Датотека] < Позиција[отвор_внес]) запиши_податоци(Датотека, должина_VALUE[Датотека]++, 0);
        запиши_податоци(Датотека, Позиција[отвор_внес]++, VALUE);
        if (должина_VALUE[Датотека] < Позиција[отвор_внес]) должина_VALUE[Датотека] = Позиција[отвор_внес];
        return 1;
    }
    public static int пребарај_позиционирање(int 서술자, int 거리, int Project_корен) {
        int отвор_внес = провери(서술자);
        if (отвор_внес < 0) return -9;
        if (Project_корен < 0 || Project_корен > 2 || 거리 < -16384 || 거리 > 16384) return -22;
        int 새위치 = 거리 + (Project_корен == 0 ? 0 : Project_корен == 1 ? Позиција[отвор_внес] : должина_VALUE[цел[отвор_внес]]);
        if (새위치 < 0 || 새위치 > 16384) return -22;
        Позиција[отвор_внес] = 새위치; return 새위치;
    }
    public static int Затвори(int 서술자) {
        int отвор_внес = провери(서술자);
        if (отвор_внес < 0) return -9;
        Референци_COUNT[цел[отвор_внес]]--; 사용[отвор_внес] = 0; return 0;
    }
    public static int Големина(int 서술자) {
        int отвор_внес = провери(서술자); return отвор_внес < 0 ? -9 : должина_VALUE[цел[отвор_внес]];
    }
    public static int збир_должина(int 서술자, int Големина) {
        int отвор_внес = провери(서술자);
        if (отвор_внес < 0 || (метод_MODE[отвор_внес] & 3) == 0) return -9;
        if (Големина < 0 || Големина > 16384) return -22;
        int Датотека = цел[отвор_внес];
        while (должина_VALUE[Датотека] < Големина) запиши_податоци(Датотека, должина_VALUE[Датотека]++, 0);
        должина_VALUE[Датотека] = Големина; return 0;
    }
    public static int избриши_внес() {
        if (патека_должина == 0) return -22;
        int мерка = нормализирање_VALUE(); if (мерка < 0) return мерка;
        if (FIND_Именик(정규길이) >= 0) return -21;
        мерка = 부모확인(); if (мерка < 0) return мерка;
        int Датотека = FIND_внес();
        if (Датотека < 0) return -2;
        이름길이[Датотека] = 0; return 0; // 열려 있는 파일은 마지막 close까지 유지
    }
    static void внес_Список() {
        патека_Start(1); патека_бајт(0, '.'); 경로목록();
    }
    public static int 공개이름길이(int INDEX) {
        if (INDEX < 0 || INDEX >= датотека_COUNT || 이름길이[INDEX] == 0) return 0;
        for (int Loop_INDEX = 0; Loop_INDEX < 이름길이[INDEX]; Loop_INDEX++) if (Име[INDEX * 64 + Loop_INDEX] == '/') return 0;
        return 이름길이[INDEX];
    }
    public static int 공개이름바이트(int INDEX, int позиционирање_INDEX) {
        return INDEX >= 0 && INDEX < датотека_COUNT && позиционирање_INDEX >= 0 && позиционирање_INDEX < 이름길이[INDEX] ? Име[INDEX * 64 + позиционирање_INDEX] : -22;
    }
    public static int 공개파일크기(int INDEX) { return INDEX >= 0 && INDEX < датотека_COUNT ? должина_VALUE[INDEX] : -22; }
    static int[] 정규 = new int[64], 현재 = new int[64], Именик_име = new int[16 * 64], Именик_должина = new int[16];
    static int 정규길이, 현재길이;
    static boolean 접두(int[] 이름들, int Изврши_2, int патека_VALUE, int[] предна_VALUE, int проред_патека) {
        if (патека_VALUE < проред_патека) return false;
        for (int Loop_INDEX = 0; Loop_INDEX < проред_патека; Loop_INDEX++) if (이름들[Изврши_2 + Loop_INDEX] != предна_VALUE[Loop_INDEX]) return false;
        return true;
    }
    static int нормализирање_VALUE() {
        if (патека_должина == 0) return -22;
        정규길이 = ПАТЕКА[0] == '/' ? 0 : 현재길이;
        for (int Loop_INDEX = 0; Loop_INDEX < 정규길이; Loop_INDEX++) 정규[Loop_INDEX] = 현재[Loop_INDEX];
        int 읽는자리 = 0;
        while (읽는자리 < патека_должина) {
            while (읽는자리 < патека_должина && ПАТЕКА[읽는자리] == '/') 읽는자리++;
            int Start_позиционирање = 읽는자리; while (읽는자리 < патека_должина && ПАТЕКА[읽는자리] != '/') { if (ПАТЕКА[읽는자리] == 0) return -22; 읽는자리++; }
            int внес_COUNT = 읽는자리 - Start_позиционирање; if (внес_COUNT == 0 || внес_COUNT == 1 && ПАТЕКА[Start_позиционирање] == '.') continue;
            if (внес_COUNT == 2 && ПАТЕКА[Start_позиционирање] == '.' && ПАТЕКА[Start_позиционирање + 1] == '.') {
                while (정규길이 > 0 && 정규[정규길이 - 1] != '/') 정규길이--;
                if (정규길이 > 0) 정규길이--;
                continue;
            }
            if (정규길이 + внес_COUNT + (정규길이 == 0 ? 0 : 1) > 63) return -36;
            if (정규길이 > 0) 정규[정규길이++] = '/';
            for (int Loop_INDEX = Start_позиционирање; Loop_INDEX < 읽는자리; Loop_INDEX++) 정규[정규길이++] = ПАТЕКА[Loop_INDEX];
        }
        return 0;
    }
    static int FIND_Именик(int внес_COUNT) {
        if (внес_COUNT == 0) return 0;
        for (int Loop_INDEX = 1; Loop_INDEX < 16; Loop_INDEX++) if (Именик_должина[Loop_INDEX] == внес_COUNT && 접두(Именик_име, Loop_INDEX * 64, внес_COUNT, 정규, внес_COUNT)) return Loop_INDEX;
        return -1;
    }
    static int 부모확인() {
        int внес_COUNT = 정규길이; while (внес_COUNT > 0 && 정규[внес_COUNT - 1] != '/') внес_COUNT--;
        return FIND_Именик(внес_COUNT == 0 ? 0 : внес_COUNT - 1) < 0 ? -2 : 0;
    }
    public static int Create_Именик() {
        int 처리값 = нормализирање_VALUE(); if (처리값 < 0) return 처리값;
        if (FIND_Именик(정규길이) >= 0 || FIND_внес() >= 0) return -17;
        처리값 = 부모확인(); if (처리값 < 0) return 처리값;
        for (int Loop_INDEX = 1; Loop_INDEX < 16; Loop_INDEX++) if (Именик_должина[Loop_INDEX] == 0) {
            Именик_должина[Loop_INDEX] = 정규길이; for (int внатрешно_поврзување_позиционирање = 0; внатрешно_поврзување_позиционирање < 정규길이; внатрешно_поврзување_позиционирање++) Именик_име[Loop_INDEX * 64 + внатрешно_поврзување_позиционирање] = 정규[внатрешно_поврзување_позиционирање]; return 0;
        }
        return -28;
    }
    public static int 항목종류() {
        int 처리값 = нормализирање_VALUE(); if (처리값 < 0) return 처리값;
        if (FIND_Именик(정규길이) >= 0) return 2;
        return FIND_внес() >= 0 ? 1 : 0;
    }
    public static int измени_Именик() {
        int 처리값 = нормализирање_VALUE(); if (처리값 < 0) return 처리값;
        if (FIND_Именик(정규길이) < 0) return -2;
        현재길이 = 정규길이; for (int Loop_INDEX = 0; Loop_INDEX < 현재길이; Loop_INDEX++) 현재[Loop_INDEX] = 정규[Loop_INDEX]; return 0;
    }
    public static int отстрани_Именик() {
        int 처리값 = нормализирање_VALUE(); if (처리값 < 0) return 처리값;
        int 폴더번호 = FIND_Именик(정규길이); if (폴더번호 < 0) return -2; if (폴더번호 == 0) return -16;
        if (현재길이 == 정규길이 && 접두(현재, 0, 현재길이, 정규, 정규길이)) return -16;
        for (int Loop_INDEX = 0; Loop_INDEX < датотека_COUNT; Loop_INDEX++) {
            if (이름길이[Loop_INDEX] > 정규길이 && 접두(Име, Loop_INDEX * 64, 이름길이[Loop_INDEX], 정규, 정규길이) && Име[Loop_INDEX * 64 + 정규길이] == '/') return -39;
        }
        for (int Loop_INDEX = 0; Loop_INDEX < 16; Loop_INDEX++) {
            if (Именик_должина[Loop_INDEX] > 정규길이 && 접두(Именик_име, Loop_INDEX * 64, Именик_должина[Loop_INDEX], 정규, 정규길이) && Именик_име[Loop_INDEX * 64 + 정규길이] == '/') return -39;
        }
        Именик_должина[폴더번호] = 0; return 0;
    }
    public static int 이름바꾸기(int 원본번호) {
        if (원본번호 < 0 || 원본번호 >= датотека_COUNT || 이름길이[원본번호] == 0) return -2;
        int 처리값 = нормализирање_VALUE(); if (처리값 < 0) return 처리값;
        if (FIND_Именик(정규길이) >= 0) return -21;
        처리값 = 부모확인(); if (처리값 < 0) return 처리값;
        int 이전값 = FIND_внес(); if (이전값 == 원본번호) return 0;
        if (이전값 >= 0) 이름길이[이전값] = 0;
        이름길이[원본번호] = 정규길이; for (int Loop_INDEX = 0; Loop_INDEX < 정규길이; Loop_INDEX++) Име[원본번호 * 64 + Loop_INDEX] = 정규[Loop_INDEX]; return 0;
    }
    static int внес_Start(int[] податоци_низа, int 시작점, int внес_COUNT) {
        if (!접두(податоци_низа, 시작점, внес_COUNT, 정규, 정규길이)) return -1;
        int Start_позиционирање = 정규길이;
        if (Start_позиционирање > 0) { if (внес_COUNT <= Start_позиционирање || податоци_низа[시작점 + Start_позиционирање] != '/') return -1; Start_позиционирање++; }
        if (внес_COUNT <= Start_позиционирање) return -1;
        for (int Loop_INDEX = Start_позиционирање; Loop_INDEX < внес_COUNT; Loop_INDEX++) if (податоци_низа[시작점 + Loop_INDEX] == '/') return -1;
        return Start_позиционирање;
    }
    static void 현재쓰기() { 단말.문자('/'); for (int Loop_INDEX = 0; Loop_INDEX < 현재길이; Loop_INDEX++) табла.직렬쓰기(현재[Loop_INDEX]); }
    static int 경로목록() {
        int 처리값 = нормализирање_VALUE(); if (처리값 < 0) return 처리값;
        int датотека_цел = FIND_внес();
        if (датотека_цел >= 0) { for (int Loop_INDEX = 0; Loop_INDEX < 정규길이; Loop_INDEX++) табла.직렬쓰기(정규[Loop_INDEX]); 단말.Запиши("  "); 단말.수(должина_VALUE[датотека_цел]); 단말.Запиши("бајт_VALUE(주기억 Датотека)\n"); return 0; }
        if (FIND_Именик(정규길이) < 0) return -2;
        for (int 뒷값 = 1; 뒷값 < 16; 뒷값++) if (Именик_должина[뒷값] > 0) {
            int Start_позиционирање = внес_Start(Именик_име, 뒷값 * 64, Именик_должина[뒷값]); if (Start_позиционирање < 0) continue;
            for (int Loop_INDEX = Start_позиционирање; Loop_INDEX < Именик_должина[뒷값]; Loop_INDEX++) табла.직렬쓰기(Именик_име[뒷값 * 64 + Loop_INDEX]); 단말.Запиши("/\n");
        }
        for (int датотека_INDEX = 0; датотека_INDEX < датотека_COUNT; датотека_INDEX++) if (이름길이[датотека_INDEX] > 0) {
            int Start_позиционирање = внес_Start(Име, датотека_INDEX * 64, 이름길이[датотека_INDEX]); if (Start_позиционирање < 0) continue;
            for (int Loop_INDEX = Start_позиционирање; Loop_INDEX < 이름길이[датотека_INDEX]; Loop_INDEX++) табла.직렬쓰기(Име[датотека_INDEX * 64 + Loop_INDEX]);
            단말.Запиши("  "); 단말.수(должина_VALUE[датотека_INDEX]); 단말.Запиши("бајт_VALUE(주기억 Датотека)\n");
        }
        return 0;
    }
}
