// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** maskinstart msinfo32_exe 조회와 4KiB 고정 Storlek 작업 avsnitt_värde allokera_minne/Retur_KR. 일반 물리 page_värde 관리자는 아니다. */
public final class Minne_område {
    static int[] avsnitt_värde = new int[8192];
    static int[] använda_värde = new int[8];

    static int parsa_heltal(int Adress) {
        return enhet_värde.läsa_Minne(Adress) | (enhet_värde.läsa_Minne(Adress + 1) << 8)
            | (enhet_värde.läsa_Minne(Adress + 2) << 16) | (enhet_värde.läsa_Minne(Adress + 3) << 24);
    }

    static int VERSALER_Minne_storlek() {
        int msinfo32_exe = enhet_värde.부팅정보();
        if (enhet_värde.부팅표식() != 0x2badb002 || msinfo32_exe == 0 || (parsa_heltal(msinfo32_exe) & 1) == 0) return -1;
        return parsa_heltal(msinfo32_exe + 8);
    }

    static int allokera_minne() {
        for (int INDEX = 0; INDEX < använda_värde.length; INDEX++) {
            if (använda_värde[INDEX] == 0) {
                använda_värde[INDEX] = 1;
                for (int fack_post = 0; fack_post < 1024; fack_post++) avsnitt_värde[INDEX * 1024 + fack_post] = 0;
                return INDEX;
            }
        }
        return -1;
    }

    static boolean Retur_KR(int INDEX) {
        if (INDEX < 0 || INDEX >= använda_värde.length || använda_värde[INDEX] == 0) return false;
        använda_värde[INDEX] = 0;
        return true;
    }

    static int 사용개수() {
        int objekt_ANTAL = 0;
        for (int INDEX = 0; INDEX < använda_värde.length; INDEX++) objekt_ANTAL += använda_värde[INDEX];
        return objekt_ANTAL;
    }
}
