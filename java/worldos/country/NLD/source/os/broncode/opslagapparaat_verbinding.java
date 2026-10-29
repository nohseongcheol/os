// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 첫 IDE 장치의 512바이트 논리 sectie_WAARDE. 이 계층은 포맷을 만들거나 임의 장치를 지우지 않는다. */
public final class opslagapparaat_verbinding {
    static boolean informatie_Actief_9e72441a = false;
    static int[] sectie_gegevens = new int[512];
    static void 잠깐기다리기() {
        for (int INDEX = 0; INDEX < 4; INDEX++) mobiel_WAARDE.입출력바이트읽기(0x3f6);
    }
    static int 준비기다리기(boolean 자료필요) {
        int starten = mobiel_WAARDE.밀리초();
        while (mobiel_WAARDE.밀리초() - starten < 500) {
            int Status_WAARDE = mobiel_WAARDE.입출력바이트읽기(0x1f7);
            if (Status_WAARDE == 0 || Status_WAARDE == 255) return -19;
            if ((Status_WAARDE & 128) == 0) {
                if ((Status_WAARDE & 33) != 0) return -5;
                if (!자료필요 || (Status_WAARDE & 8) != 0) return 0;
            }
            mobiel_WAARDE.잠시양보();
        }
        return -110;
    }
    static int aanvraag(int sectie_WAARDE, int opdracht) {
        if (sectie_WAARDE < 0 || sectie_WAARDE >= 2048) return -22;
        mobiel_WAARDE.입출력바이트쓰기(0x3f6, 2); // polling; IDE IRQ gebruik_WAARDE 안 함
        mobiel_WAARDE.입출력바이트쓰기(0x1f6, 0xe0); 잠깐기다리기();
        int resultaat = 준비기다리기(false);
        if (resultaat < 0) return resultaat;
        mobiel_WAARDE.입출력바이트쓰기(0x1f2, 1);
        mobiel_WAARDE.입출력바이트쓰기(0x1f3, sectie_WAARDE & 255);
        mobiel_WAARDE.입출력바이트쓰기(0x1f4, (sectie_WAARDE >>> 8) & 255);
        mobiel_WAARDE.입출력바이트쓰기(0x1f5, 0);
        mobiel_WAARDE.입출력바이트쓰기(0x1f7, opdracht); 잠깐기다리기();
        return 준비기다리기(true);
    }
    static int Lezen(int sectie_WAARDE) {
        int resultaat = aanvraag(sectie_WAARDE, 0x20);
        if (resultaat < 0) return resultaat;
        for (int INDEX = 0; INDEX < 256; INDEX++) {
            int WAARDE = mobiel_WAARDE.입출력짧은수읽기(0x1f0);
            sectie_gegevens[INDEX * 2] = WAARDE & 255; sectie_gegevens[INDEX * 2 + 1] = WAARDE >>> 8;
        }
        잠깐기다리기(); return 준비기다리기(false);
    }
    static int Schrijven(int sectie_WAARDE) {
        if (!informatie_Actief_9e72441a || sectie_WAARDE < 1 || sectie_WAARDE > 518) return -19;
        int resultaat = aanvraag(sectie_WAARDE, 0x30);
        if (resultaat < 0) return resultaat;
        for (int INDEX = 0; INDEX < 256; INDEX++)
            mobiel_WAARDE.입출력짧은수쓰기(0x1f0, sectie_gegevens[INDEX * 2] | sectie_gegevens[INDEX * 2 + 1] << 8);
        잠깐기다리기(); return 준비기다리기(false);
    }
    static int leegmaken_uitvoer() {
        if (!informatie_Actief_9e72441a) return -19;
        mobiel_WAARDE.입출력바이트쓰기(0x1f7, 0xe7); 잠깐기다리기();
        return 준비기다리기(false);
    }
    static int parseren_geheel_getal(int positie) {
        return sectie_gegevens[positie] | sectie_gegevens[positie + 1] << 8 | sectie_gegevens[positie + 2] << 16 | sectie_gegevens[positie + 3] << 24;
    }
    static void schrijven_geheel_getal_WAARDE(int positie, int WAARDE) {
        for (int INDEX = 0; INDEX < 4; INDEX++) sectie_gegevens[positie + INDEX] = (WAARDE >>> (INDEX * 8)) & 255;
    }
}
