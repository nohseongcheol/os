// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 첫 IDE 장치의 512바이트 논리 secció_VALOR. 이 계층은 포맷을 만들거나 임의 장치를 지우지 않는다. */
public final class Emmagatzematge_dispositiu_connexió {
    static boolean tecnologies_de_la_informació_Actiu_9e72441a = false;
    static int[] secció_dades = new int[512];
    static void 잠깐기다리기() {
        for (int INDEX = 0; INDEX < 4; INDEX++) dispositiu_VALOR.입출력바이트읽기(0x3f6);
    }
    static int 준비기다리기(boolean 자료필요) {
        int Executa_2 = dispositiu_VALOR.밀리초();
        while (dispositiu_VALOR.밀리초() - Executa_2 < 500) {
            int Estat_VALOR = dispositiu_VALOR.입출력바이트읽기(0x1f7);
            if (Estat_VALOR == 0 || Estat_VALOR == 255) return -19;
            if ((Estat_VALOR & 128) == 0) {
                if ((Estat_VALOR & 33) != 0) return -5;
                if (!자료필요 || (Estat_VALOR & 8) != 0) return 0;
            }
            dispositiu_VALOR.잠시양보();
        }
        return -110;
    }
    static int sol_licitud(int secció_VALOR, int Ordre) {
        if (secció_VALOR < 0 || secció_VALOR >= 2048) return -22;
        dispositiu_VALOR.입출력바이트쓰기(0x3f6, 2); // polling; IDE IRQ ús_VALOR 안 함
        dispositiu_VALOR.입출력바이트쓰기(0x1f6, 0xe0); 잠깐기다리기();
        int RESULTAT = 준비기다리기(false);
        if (RESULTAT < 0) return RESULTAT;
        dispositiu_VALOR.입출력바이트쓰기(0x1f2, 1);
        dispositiu_VALOR.입출력바이트쓰기(0x1f3, secció_VALOR & 255);
        dispositiu_VALOR.입출력바이트쓰기(0x1f4, (secció_VALOR >>> 8) & 255);
        dispositiu_VALOR.입출력바이트쓰기(0x1f5, 0);
        dispositiu_VALOR.입출력바이트쓰기(0x1f7, Ordre); 잠깐기다리기();
        return 준비기다리기(true);
    }
    static int Lectura(int secció_VALOR) {
        int RESULTAT = sol_licitud(secció_VALOR, 0x20);
        if (RESULTAT < 0) return RESULTAT;
        for (int INDEX = 0; INDEX < 256; INDEX++) {
            int VALOR = dispositiu_VALOR.입출력짧은수읽기(0x1f0);
            secció_dades[INDEX * 2] = VALOR & 255; secció_dades[INDEX * 2 + 1] = VALOR >>> 8;
        }
        잠깐기다리기(); return 준비기다리기(false);
    }
    static int Escriptura(int secció_VALOR) {
        if (!tecnologies_de_la_informació_Actiu_9e72441a || secció_VALOR < 1 || secció_VALOR > 518) return -19;
        int RESULTAT = sol_licitud(secció_VALOR, 0x30);
        if (RESULTAT < 0) return RESULTAT;
        for (int INDEX = 0; INDEX < 256; INDEX++)
            dispositiu_VALOR.입출력짧은수쓰기(0x1f0, secció_dades[INDEX * 2] | secció_dades[INDEX * 2 + 1] << 8);
        잠깐기다리기(); return 준비기다리기(false);
    }
    static int 밀어쓰기() {
        if (!tecnologies_de_la_informació_Actiu_9e72441a) return -19;
        dispositiu_VALOR.입출력바이트쓰기(0x1f7, 0xe7); 잠깐기다리기();
        return 준비기다리기(false);
    }
    static int 정수읽기(int Posició) {
        return secció_dades[Posició] | secció_dades[Posició + 1] << 8 | secció_dades[Posició + 2] << 16 | secció_dades[Posició + 3] << 24;
    }
    static void 정수쓰기(int Posició, int VALOR) {
        for (int INDEX = 0; INDEX < 4; INDEX++) secció_dades[Posició + INDEX] = (VALOR >>> (INDEX * 8)) & 255;
    }
}
