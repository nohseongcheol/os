// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** spuštění_stroje Informace_o_systému 조회와 4KiB 고정 Velikost 작업 oddíl_HODNOTA_366e0bfa přidělit_Storage/Vratka_KV. 일반 물리 stránka_HODNOTA 관리자는 아니다. */
public final class Paměť_oblast {
    static int[] oddíl_HODNOTA_366e0bfa = new int[8192];
    static int[] použít_HODNOTA = new int[8];

    static int parsovat_integer(int Adresa) {
        return mobilní_HODNOTA.기억읽기(Adresa) | (mobilní_HODNOTA.기억읽기(Adresa + 1) << 8)
            | (mobilní_HODNOTA.기억읽기(Adresa + 2) << 16) | (mobilní_HODNOTA.기억읽기(Adresa + 3) << 24);
    }

    static int VELKÁ_Paměť_změnit_velikost() {
        int Informace_o_systému = mobilní_HODNOTA.부팅정보();
        if (mobilní_HODNOTA.부팅표식() != 0x2badb002 || Informace_o_systému == 0 || (parsovat_integer(Informace_o_systému) & 1) == 0) return -1;
        return parsovat_integer(Informace_o_systému + 8);
    }

    static int přidělit_Storage() {
        for (int INDEX = 0; INDEX < použít_HODNOTA.length; INDEX++) {
            if (použít_HODNOTA[INDEX] == 0) {
                použít_HODNOTA[INDEX] = 1;
                for (int přihrádka_položka = 0; přihrádka_položka < 1024; přihrádka_položka++) oddíl_HODNOTA_366e0bfa[INDEX * 1024 + přihrádka_položka] = 0;
                return INDEX;
            }
        }
        return -1;
    }

    static boolean Vratka_KV(int INDEX) {
        if (INDEX < 0 || INDEX >= použít_HODNOTA.length || použít_HODNOTA[INDEX] == 0) return false;
        použít_HODNOTA[INDEX] = 0;
        return true;
    }

    static int 사용개수() {
        int zboží_POČET = 0;
        for (int INDEX = 0; INDEX < použít_HODNOTA.length; INDEX++) zboží_POČET += použít_HODNOTA[INDEX];
        return zboží_POČET;
    }
}
