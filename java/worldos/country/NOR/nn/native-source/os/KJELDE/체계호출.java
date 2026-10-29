// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** int 0x80 게이트가 호출한다. 모든 brukar peikar/길이는 tilgang_oppføring 전에 검사한다. */
public final class 체계호출 {
    static int[] 임시자료 = new int[1024];

    static int ARRAY_lengd(int ADDRESS) {
        if (!실행관리.klipp(ADDRESS, 4)) return -14;
        int lengd_VALUE = 실행관리.수(ADDRESS);
        if (lengd_VALUE < 0 || lengd_VALUE > (실행관리.brukar_avslutte - ADDRESS - 4) / 4) return -14;
        return lengd_VALUE;
    }

    public static int Prosess_VALUE_oppføring(int INDEX, int 가, int 나, int 다, int 라, int 마) {
        if (INDEX == 30) return 파일서술자관리.opne_fil(가, 나, 다);
        if (INDEX == 31) return 파일서술자관리.파일읽기(가, 나, 다);
        if (INDEX == 32) return 파일서술자관리.skrive_fil(가, 나, 다);
        if (INDEX == 33) return 파일서술자관리.Lukk_fil(가);
        if (INDEX == 34) return 파일서술자관리.søk_fil(가, 나, 다);
        if (INDEX == 35) return 파일서술자관리.서술자복제(가, 0, false, 0);
        if (INDEX == 36) return 파일서술자관리.서술자복제(가, 나, true, 0);
        if (INDEX == 37) return 파일서술자관리.파일상태읽기(가, 나);
        if (INDEX == 38) return 파일서술자관리.fjerne_fil_oppføring_namn(가);
        if (INDEX == 39) return 파일서술자관리.sett_fil_lengd(가, 나);
        if (INDEX == 40) return 파일서술자관리.서술자제어(가, 나, 다);
        if (INDEX == 41) return 파일서술자관리.Opprett_endepunkt(가, 나, 다);
        if (INDEX == 42) return 파일서술자관리.BIND_ADDRESS(가, 나, 다);
        if (INDEX == 43) return 파일서술자관리.자료전문보내기(가, 나, 다, 라, 마);
        if (INDEX == 44) return 파일서술자관리.자료전문받기(가, 나, 다, 라, 마);
        if (INDEX == 45) return 파일서술자관리.통신주소읽기(가, 나, 다);
        if (INDEX == 46) return 파일서술자관리.수신대기정하기(가, 나);
        if (INDEX == 47) {
            int 기술 = 파일서술자관리.기술찾기(가);
            if (기술 < 0) return -9;
            if (파일서술자관리.종류[기술] != 2) return -22;
            return 파일보존.synkronisere();
        }
        if (INDEX == 1) {
            int lengd_VALUE = ARRAY_lengd(가);
            if (lengd_VALUE < 0) return lengd_VALUE;
            if (lengd_VALUE > 4096) return -90;
            for (int teikn_VALUE = 0; teikn_VALUE < lengd_VALUE; teikn_VALUE++) SMS_Terminal.문자(실행관리.수(가 + 4 + teikn_VALUE * 4) & 65535);
            return lengd_VALUE;
        }
        if (INDEX == 2) return 실행관리.argument_COUNT;
        if (INDEX == 3) return 가 >= 0 && 가 < 실행관리.argument_COUNT ? 실행관리.argument_ADDRESS[가] : 0;
        if (INDEX == 10) return Nettverk_Stabel.Opna(가);
        if (INDEX == 11) {
            int lengd_VALUE = ARRAY_lengd(라);
            if (lengd_VALUE < 0) return lengd_VALUE;
            if (마 < 0 || 마 > lengd_VALUE || 마 > 1024) return -90;
            for (int Posisjon = 0; Posisjon < 마; Posisjon++) 임시자료[Posisjon] = 실행관리.수(라 + 4 + Posisjon * 4) & 255;
            return Nettverk_Stabel.sende(가, 나, 다, 임시자료, 마);
        }
        if (INDEX == 12) {
            int lengd_VALUE = ARRAY_lengd(나);
            if (lengd_VALUE < 0) return lengd_VALUE;
            if (다 < 0 || 다 > 2000) return -22;
            int forretningsmål = Nettverk_Stabel.받기(가, 임시자료, lengd_VALUE < 1024 ? lengd_VALUE : 1024, 다);
            if (forretningsmål >= 0) for (int Posisjon = 0; Posisjon < forretningsmål; Posisjon++) 실행관리.수쓰기(나 + 4 + Posisjon * 4, 임시자료[Posisjon]);
            return forretningsmål;
        }
        if (INDEX == 13) return Nettverk_Stabel.Lukk(가);
        if (INDEX == 14) return Nettverk_Stabel.내주소;
        if (INDEX == 15) return Nettverk_Stabel.node_ADDRESS(가);
        if (INDEX == 16) return Nettverk_Stabel.node_portnummer(가);
        if (INDEX == 22) {
            if (가 < 0 || 가 > 65535) return -22;
            SMS_Terminal.문자(가); return 1;
        }
        if (INDEX == 20 || INDEX == 21) {
            int namn_endre_storleik = ARRAY_lengd(가), data_endre_storleik = ARRAY_lengd(나);
            if (namn_endre_storleik < 0 || data_endre_storleik < 0) return -14;
            if (namn_endre_storleik < 1 || namn_endre_storleik > 64) return -22;
            int lengd_VALUE = 0;
            while (lengd_VALUE < namn_endre_storleik && 실행관리.수(가 + 4 + lengd_VALUE * 4) != 0) {
                Minne_filsystem.Namn[lengd_VALUE] = 실행관리.수(가 + 4 + lengd_VALUE * 4);
                lengd_VALUE++;
            }
            if (!Minne_filsystem.sjekk_namn(Minne_filsystem.Namn, lengd_VALUE)) return -22;
            if (INDEX == 20) {
                int Fil = Minne_filsystem.Søk_oppføring(Minne_filsystem.Namn, lengd_VALUE);
                if (Fil < 0) return Fil;
                int Storleik = Minne_filsystem.endre_storleik_Liste[Fil];
                if (Storleik > data_endre_storleik) return -90;
                int ADDRESS = mobil_VALUE.fil_Minne() + Fil * Minne_filsystem.최대크기;
                for (int 수 = 0; 수 < Storleik; 수++) 실행관리.수쓰기(나 + 4 + 수 * 4, mobil_VALUE.기억읽기(ADDRESS + 수));
                return Storleik;
            }
            if (다 < 0 || 다 > data_endre_storleik) return -22;
            if (다 > Minne_filsystem.최대크기) return -90;
            for (int 수 = 0; 수 < 다; 수++) Minne_filsystem.redigere_VALUE[수] = 실행관리.수(나 + 4 + 수 * 4) & 255;
            return Minne_filsystem.Store_VALUE(Minne_filsystem.Namn, lengd_VALUE, Minne_filsystem.redigere_VALUE, 다);
        }
        return -38;
    }
}
