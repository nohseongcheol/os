// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 부팅 Systémové_informácie 조회와 4KiB 고정 Veľkosť 작업 sekcia_VALUE vyhradiť_Úložisko/vrátiť_KR. 일반 물리 strana_VALUE 관리자는 아니다. */
public final class Pamäť_oblasť {
    static int[] sekcia_VALUE = new int[8192];
    static int[] používať_VALUE = new int[8];

    static int analyzovať_celé_číslo(int adresa) {
        return telefón_VALUE.기억읽기(adresa) | (telefón_VALUE.기억읽기(adresa + 1) << 8)
            | (telefón_VALUE.기억읽기(adresa + 2) << 16) | (telefón_VALUE.기억읽기(adresa + 3) << 24);
    }

    static int UPPER_Pamäť_zmeniť_veľkosť() {
        int Systémové_informácie = telefón_VALUE.부팅정보();
        if (telefón_VALUE.부팅표식() != 0x2badb002 || Systémové_informácie == 0 || (analyzovať_celé_číslo(Systémové_informácie) & 1) == 0) return -1;
        return analyzovať_celé_číslo(Systémové_informácie + 8);
    }

    static int vyhradiť_Úložisko() {
        for (int INDEX = 0; INDEX < používať_VALUE.length; INDEX++) {
            if (používať_VALUE[INDEX] == 0) {
                používať_VALUE[INDEX] = 1;
                for (int 칸 = 0; 칸 < 1024; 칸++) sekcia_VALUE[INDEX * 1024 + 칸] = 0;
                return INDEX;
            }
        }
        return -1;
    }

    static boolean vrátiť_KR(int INDEX) {
        if (INDEX < 0 || INDEX >= používať_VALUE.length || používať_VALUE[INDEX] == 0) return false;
        používať_VALUE[INDEX] = 0;
        return true;
    }

    static int 사용개수() {
        int položka_COUNT = 0;
        for (int INDEX = 0; INDEX < používať_VALUE.length; INDEX++) položka_COUNT += používať_VALUE[INDEX];
        return položka_COUNT;
    }
}
