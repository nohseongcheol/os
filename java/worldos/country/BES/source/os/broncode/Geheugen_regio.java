// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** machineopstart msinfo32_exe 조회와 4KiB 고정 Grootte 작업 sectie_WAARDE toewijzen_Opslag/Retour_HR. 일반 물리 page_WAARDE 관리자는 아니다. */
public final class Geheugen_regio {
    static int[] sectie_WAARDE = new int[8192];
    static int[] gebruik_WAARDE = new int[8];

    static int parseren_geheel_getal(int ADRES) {
        return mobiel_WAARDE.기억읽기(ADRES) | (mobiel_WAARDE.기억읽기(ADRES + 1) << 8)
            | (mobiel_WAARDE.기억읽기(ADRES + 2) << 16) | (mobiel_WAARDE.기억읽기(ADRES + 3) << 24);
    }

    static int HOOFDLETTERS_Geheugen_formaat_wijzigen() {
        int msinfo32_exe = mobiel_WAARDE.부팅정보();
        if (mobiel_WAARDE.부팅표식() != 0x2badb002 || msinfo32_exe == 0 || (parseren_geheel_getal(msinfo32_exe) & 1) == 0) return -1;
        return parseren_geheel_getal(msinfo32_exe + 8);
    }

    static int toewijzen_Opslag() {
        for (int INDEX = 0; INDEX < gebruik_WAARDE.length; INDEX++) {
            if (gebruik_WAARDE[INDEX] == 0) {
                gebruik_WAARDE[INDEX] = 1;
                for (int sleuf_invoer = 0; sleuf_invoer < 1024; sleuf_invoer++) sectie_WAARDE[INDEX * 1024 + sleuf_invoer] = 0;
                return INDEX;
            }
        }
        return -1;
    }

    static boolean Retour_HR(int INDEX) {
        if (INDEX < 0 || INDEX >= gebruik_WAARDE.length || gebruik_WAARDE[INDEX] == 0) return false;
        gebruik_WAARDE[INDEX] = 0;
        return true;
    }

    static int 사용개수() {
        int item_AANTAL = 0;
        for (int INDEX = 0; INDEX < gebruik_WAARDE.length; INDEX++) item_AANTAL += gebruik_WAARDE[INDEX];
        return item_AANTAL;
    }
}
