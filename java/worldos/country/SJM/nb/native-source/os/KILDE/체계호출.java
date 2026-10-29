// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** int 0x80 게이트가 호출한다. 모든 bruker peker/길이는 tilgang_oppføring 전에 검사한다. */
public final class 체계호출 {
    static int[] 임시자료 = new int[1024];

    static int MATRISE_lengde(int e_post) {
        if (!kjøring_overordnet.klippe(e_post, 4)) return -14;
        int lengde_VERDI = kjøring_overordnet.nummer(e_post);
        if (lengde_VERDI < 0 || lengde_VERDI > (kjøring_overordnet.bruker_avslutte_en_samtale - e_post - 4) / 4) return -14;
        return lengde_VERDI;
    }

    public static int Prosess_VERDI_oppføring(int INDEKS, int 가, int SEKUND_operand, int 다, int 라, int 마) {
        if (INDEKS == 30) return 파일서술자관리.åpen_Fil(가, SEKUND_operand, 다);
        if (INDEKS == 31) return 파일서술자관리.파일읽기(가, SEKUND_operand, 다);
        if (INDEKS == 32) return 파일서술자관리.skrive_Fil(가, SEKUND_operand, 다);
        if (INDEKS == 33) return 파일서술자관리.Lukk_Fil(가);
        if (INDEKS == 34) return 파일서술자관리.søk_Fil(가, SEKUND_operand, 다);
        if (INDEKS == 35) return 파일서술자관리.서술자복제(가, 0, false, 0);
        if (INDEKS == 36) return 파일서술자관리.서술자복제(가, SEKUND_operand, true, 0);
        if (INDEKS == 37) return 파일서술자관리.파일상태읽기(가, SEKUND_operand);
        if (INDEKS == 38) return 파일서술자관리.fjerne_Fil_oppføring_navn(가);
        if (INDEKS == 39) return 파일서술자관리.sett_Fil_lengde(가, SEKUND_operand);
        if (INDEKS == 40) return 파일서술자관리.서술자제어(가, SEKUND_operand, 다);
        if (INDEKS == 41) return 파일서술자관리.åpne_deltaker(가, SEKUND_operand, 다);
        if (INDEKS == 42) return 파일서술자관리.BIND_e_post(가, SEKUND_operand, 다);
        if (INDEKS == 43) return 파일서술자관리.sende_datagram_data(가, SEKUND_operand, 다, 라, 마);
        if (INDEKS == 44) return 파일서술자관리.motta_datagram_data(가, SEKUND_operand, 다, 라, 마);
        if (INDEKS == 45) return 파일서술자관리.통신주소읽기(가, SEKUND_operand, 다);
        if (INDEKS == 46) return 파일서술자관리.sett_motta_TIMEOUT(가, SEKUND_operand);
        if (INDEKS == 47) {
            int 기술 = 파일서술자관리.기술찾기(가);
            if (기술 < 0) return -9;
            if (파일서술자관리.종류[기술] != 2) return -22;
            return 파일보존.synkronisere();
        }
        if (INDEKS == 1) {
            int lengde_VERDI = MATRISE_lengde(가);
            if (lengde_VERDI < 0) return lengde_VERDI;
            if (lengde_VERDI > 4096) return -90;
            for (int tegn_VERDI = 0; tegn_VERDI < lengde_VERDI; tegn_VERDI++) SMS_Terminal.문자(kjøring_overordnet.nummer(가 + 4 + tegn_VERDI * 4) & 65535);
            return lengde_VERDI;
        }
        if (INDEKS == 2) return kjøring_overordnet.argument_ANTALL;
        if (INDEKS == 3) return 가 >= 0 && 가 < kjøring_overordnet.argument_ANTALL ? kjøring_overordnet.argument_e_post[가] : 0;
        if (INDEKS == 10) return nettverk_stakk.Åpne(가);
        if (INDEKS == 11) {
            int lengde_VERDI = MATRISE_lengde(라);
            if (lengde_VERDI < 0) return lengde_VERDI;
            if (마 < 0 || 마 > lengde_VERDI || 마 > 1024) return -90;
            for (int Posisjon = 0; Posisjon < 마; Posisjon++) 임시자료[Posisjon] = kjøring_overordnet.nummer(라 + 4 + Posisjon * 4) & 255;
            return nettverk_stakk.sende(가, SEKUND_operand, 다, 임시자료, 마);
        }
        if (INDEKS == 12) {
            int lengde_VERDI = MATRISE_lengde(SEKUND_operand);
            if (lengde_VERDI < 0) return lengde_VERDI;
            if (다 < 0 || 다 > 2000) return -22;
            int KR = nettverk_stakk.motta(가, 임시자료, lengde_VERDI < 1024 ? lengde_VERDI : 1024, 다);
            if (KR >= 0) for (int Posisjon = 0; Posisjon < KR; Posisjon++) kjøring_overordnet.skrive_nummer(SEKUND_operand + 4 + Posisjon * 4, 임시자료[Posisjon]);
            return KR;
        }
        if (INDEKS == 13) return nettverk_stakk.Lukk(가);
        if (INDEKS == 14) return nettverk_stakk.내주소;
        if (INDEKS == 15) return nettverk_stakk.node_e_post(가);
        if (INDEKS == 16) return nettverk_stakk.node_portnummer(가);
        if (INDEKS == 22) {
            if (가 < 0 || 가 > 65535) return -22;
            SMS_Terminal.문자(가); return 1;
        }
        if (INDEKS == 20 || INDEKS == 21) {
            int navn_skalere = MATRISE_lengde(가), data_skalere = MATRISE_lengde(SEKUND_operand);
            if (navn_skalere < 0 || data_skalere < 0) return -14;
            if (navn_skalere < 1 || navn_skalere > 64) return -22;
            int lengde_VERDI = 0;
            while (lengde_VERDI < navn_skalere && kjøring_overordnet.nummer(가 + 4 + lengde_VERDI * 4) != 0) {
                Minne_filsystem.Navn[lengde_VERDI] = kjøring_overordnet.nummer(가 + 4 + lengde_VERDI * 4);
                lengde_VERDI++;
            }
            if (!Minne_filsystem.sjekk_navn(Minne_filsystem.Navn, lengde_VERDI)) return -22;
            if (INDEKS == 20) {
                int Fil = Minne_filsystem.Søk_oppføring(Minne_filsystem.Navn, lengde_VERDI);
                if (Fil < 0) return Fil;
                int Størrelse = Minne_filsystem.skalere_Liste[Fil];
                if (Størrelse > data_skalere) return -90;
                int e_post = enhet_VERDI.Fil_Minne() + Fil * Minne_filsystem.최대크기;
                for (int nummer = 0; nummer < Størrelse; nummer++) kjøring_overordnet.skrive_nummer(SEKUND_operand + 4 + nummer * 4, enhet_VERDI.기억읽기(e_post + nummer));
                return Størrelse;
            }
            if (다 < 0 || 다 > data_skalere) return -22;
            if (다 > Minne_filsystem.최대크기) return -90;
            for (int nummer = 0; nummer < 다; nummer++) Minne_filsystem.Rediger_VERDI[nummer] = kjøring_overordnet.nummer(SEKUND_operand + 4 + nummer * 4) & 255;
            return Minne_filsystem.Store_VERDI(Minne_filsystem.Navn, lengde_VERDI, Minne_filsystem.Rediger_VERDI, 다);
        }
        return -38;
    }
}
