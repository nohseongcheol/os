// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 단일 bruger 과정의 파일서술자와 열린 Fil 기술을 분리한다. 호출 번호는 POSIX ABI 문서에 기록한다. */
public final class 파일서술자관리 {
    static final int 서술자한도 = 32;
    static final int læse_skrive_flag = 2, åbne_post_81b8d99b = 64, 독점생성 = 128, rydde_Indhold = 512;
    static final int 이어쓰기 = 1024, 기다리지않기 = 2048, 실행시닫기 = 524288;
    static int[] åben_handle = new int[서술자한도], 서술자설정 = new int[서술자한도];
    static int[] 종류 = new int[서술자한도], mål = new int[서술자한도];
    static int[] fil_placere = new int[서술자한도], åben_Indstillinger = new int[서술자한도], referere_TÆL = new int[서술자한도];
    static int[] netværk_handle = new int[서술자한도], 수신대기밀리초 = new int[서술자한도];
    static int[] sti_navn = new int[64], overføre_data = new int[1024];

    static int 기술찾기(int 파일서술자) {
        if (파일서술자 < 0 || 파일서술자 >= 서술자한도) return -9;
        return åben_handle[파일서술자] - 1;
    }
    static int 빈서술자(int Kør_2) {
        for (int INDEKS = Kør_2; INDEKS < 서술자한도; INDEKS++) if (åben_handle[INDEKS] == 0) return INDEKS;
        return -24;
    }
    static int 빈기술() {
        for (int INDEKS = 0; INDEKS < 서술자한도; INDEKS++) if (referere_TÆL[INDEKS] == 0) return INDEKS;
        return -24;
    }
    static int Tilslut(int 서술자, int 기술, int 파일종류, int fil_mål, int Indstillinger) {
        åben_handle[서술자] = 기술 + 1; 서술자설정[서술자] = (Indstillinger & 실행시닫기) != 0 ? 1 : 0;
        종류[기술] = 파일종류; mål[기술] = fil_mål; referere_TÆL[기술] = 1;
        åben_Indstillinger[기술] = Indstillinger & (3 | 이어쓰기 | 기다리지않기); fil_placere[기술] = 0;
        netværk_handle[기술] = 0; 수신대기밀리초[기술] = 0;
        return 서술자;
    }
    static void START_Proces() {
        Ren_Proces();
        for (int INDEKS = 0; INDEKS < 3; INDEKS++) Tilslut(INDEKS, INDEKS, 1, INDEKS, INDEKS == 0 ? 0 : 1);
    }
    static void Ren_Proces() {
        for (int INDEKS = 0; INDEKS < 서술자한도; INDEKS++) if (åben_handle[INDEKS] != 0) Luk_fil(INDEKS);
    }
    static int Luk_fil(int 서술자) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        åben_handle[서술자] = 0; 서술자설정[서술자] = 0;
        referere_TÆL[기술]--;
        if (referere_TÆL[기술] == 0) {
            if (종류[기술] == 2) Hukommelse_filsystem.åben_TÆL[mål[기술]]--;
            if (종류[기술] == 3 && netværk_handle[기술] != 0) netværk_Stak.Luk(netværk_handle[기술]);
            종류[기술] = 0;
        }
        return 0;
    }
    // C 경로는 NUL 끝 byte_VÆRDI 문자열이다. 루트의 한 이름만 지원한다.
    static int 경로읽기(int mail) {
        if (!udførelse_Leder.klippe(mail, 1)) return -14;
        int Placering = enhed_VÆRDI.기억읽기(mail) == '/' ? 1 : 0;
        for (int varighed_VÆRDI = 0; varighed_VÆRDI < 64; varighed_VÆRDI++) {
            if (!udførelse_Leder.klippe(mail + Placering + varighed_VÆRDI, 1)) return -14;
            int VÆRDI = enhed_VÆRDI.기억읽기(mail + Placering + varighed_VÆRDI);
            sti_navn[varighed_VÆRDI] = VÆRDI;
            if (VÆRDI == 0) return varighed_VÆRDI == 0 ? -2 : (Hukommelse_filsystem.check_navn(sti_navn, varighed_VÆRDI) ? varighed_VÆRDI : -22);
            if (VÆRDI == '/') return -20;
        }
        return -36;
    }
    static int åben_fil(int navn_mail, int Indstillinger, int 허가) {
        int varighed_VÆRDI = 경로읽기(navn_mail);
        if (varighed_VÆRDI < 0) return varighed_VÆRDI;
        if ((Indstillinger & ~(3 | åbne_post_81b8d99b | 독점생성 | rydde_Indhold | 이어쓰기 | 기다리지않기 | 실행시닫기)) != 0) return -95;
        if ((Indstillinger & 3) == 3 || ((Indstillinger & rydde_Indhold) != 0 && (Indstillinger & 3) == 0)) return -22;
        int Fil = Hukommelse_filsystem.Søg_post(sti_navn, varighed_VÆRDI);
        if (Fil >= 0 && (Indstillinger & (åbne_post_81b8d99b | 독점생성)) == (åbne_post_81b8d99b | 독점생성)) return -17;
        if (Fil == -2 && (Indstillinger & åbne_post_81b8d99b) == 0) return -2;
        int 서술자 = 빈서술자(0), 기술 = 빈기술();
        if (서술자 < 0 || 기술 < 0) return -24;
        if (Fil == -2) {
            int KR = Hukommelse_filsystem.Store_VÆRDI(sti_navn, varighed_VÆRDI, sti_navn, 0);
            if (KR < 0) return KR;
            Fil = Hukommelse_filsystem.Søg_post(sti_navn, varighed_VÆRDI);
            Hukommelse_filsystem.허가들[Fil] = 허가 & 511;
        }
        if (Fil < 0) return Fil;
        if ((Indstillinger & rydde_Indhold) != 0) Hukommelse_filsystem.tilpasse_størrelse_Liste[Fil] = 0;
        Hukommelse_filsystem.åben_TÆL[Fil]++;
        return Tilslut(서술자, 기술, 2, Fil, Indstillinger);
    }
    static int 파일읽기(int 서술자, int data_mail, int varighed_VÆRDI) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0 || (åben_Indstillinger[기술] & 3) == 1) return -9;
        if (varighed_VÆRDI < 0) return -22;
        if (varighed_VÆRDI == 0) return 0;
        if (!udførelse_Leder.klippe(data_mail, varighed_VÆRDI)) return -14;
        if (종류[기술] == 3) return modtage_datagram_data(서술자, data_mail, varighed_VÆRDI, 0, 0);
        if (종류[기술] == 1) {
            int MODTAGET_VED_UDLØB_TÆL = 0;
            while (MODTAGET_VED_UDLØB_TÆL < varighed_VÆRDI) {
                int VÆRDI = sms_Terminal.직렬읽기();
                if (VÆRDI < 0) VÆRDI = tastatur.Læse();
                if (VÆRDI < 0) {
                    if (MODTAGET_VED_UDLØB_TÆL > 0) return MODTAGET_VED_UDLØB_TÆL;
                    if ((åben_Indstillinger[기술] & 기다리지않기) != 0) return -11;
                    if (enhed_VÆRDI.사용자남은밀리초() <= 10) return -11;
                    netværk_Stak.bekræfte(); enhed_VÆRDI.잠시양보();
                } else {
                    enhed_VÆRDI.skrive_Hukommelse(data_mail + MODTAGET_VED_UDLØB_TÆL, VÆRDI); MODTAGET_VED_UDLØB_TÆL++;
                }
            }
            return MODTAGET_VED_UDLØB_TÆL;
        }
        int Fil = mål[기술], Placering = fil_placere[기술];
        if (Placering >= Hukommelse_filsystem.tilpasse_størrelse_Liste[Fil]) return 0;
        if (varighed_VÆRDI > Hukommelse_filsystem.tilpasse_størrelse_Liste[Fil] - Placering) varighed_VÆRDI = Hukommelse_filsystem.tilpasse_størrelse_Liste[Fil] - Placering;
        int 원본주소 = enhed_VÆRDI.fil_Hukommelse() + Fil * Hukommelse_filsystem.최대크기 + Placering;
        for (int INDEKS = 0; INDEKS < varighed_VÆRDI; INDEKS++) enhed_VÆRDI.skrive_Hukommelse(data_mail + INDEKS, enhed_VÆRDI.기억읽기(원본주소 + INDEKS));
        fil_placere[기술] += varighed_VÆRDI;
        return varighed_VÆRDI;
    }
    static int skrive_fil(int 서술자, int data_mail, int varighed_VÆRDI) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0 || (åben_Indstillinger[기술] & 3) == 0) return -9;
        if (varighed_VÆRDI < 0) return -22;
        if (varighed_VÆRDI == 0) return 0;
        if (!udførelse_Leder.klippe(data_mail, varighed_VÆRDI)) return -14;
        if (종류[기술] == 3) return -89; // 연결하지 않은 자료전문 종단점에는 destination_VÆRDI 주소가 필요하다.
        if (종류[기술] == 1) {
            if (varighed_VÆRDI > 16384) varighed_VÆRDI = 16384;
            for (int INDEKS = 0; INDEKS < varighed_VÆRDI; INDEKS++) {
                int VÆRDI = enhed_VÆRDI.기억읽기(data_mail + INDEKS);
                sms_Terminal.직렬바이트(VÆRDI); sms_Terminal.skærmbillede_tegn(VÆRDI);
            }
            return varighed_VÆRDI;
        }
        int Fil = mål[기술], Størrelse = Hukommelse_filsystem.tilpasse_størrelse_Liste[Fil];
        int Placering = (åben_Indstillinger[기술] & 이어쓰기) != 0 ? Størrelse : fil_placere[기술];
        if (Placering >= Hukommelse_filsystem.최대크기) return -27;
        if (varighed_VÆRDI > Hukommelse_filsystem.최대크기 - Placering) varighed_VÆRDI = Hukommelse_filsystem.최대크기 - Placering;
        int destination_mail = enhed_VÆRDI.fil_Hukommelse() + Fil * Hukommelse_filsystem.최대크기;
        for (int INDEKS = Størrelse; INDEKS < Placering; INDEKS++) enhed_VÆRDI.skrive_Hukommelse(destination_mail + INDEKS, 0);
        for (int INDEKS = 0; INDEKS < varighed_VÆRDI; INDEKS++) enhed_VÆRDI.skrive_Hukommelse(destination_mail + Placering + INDEKS, enhed_VÆRDI.기억읽기(data_mail + INDEKS));
        fil_placere[기술] = Placering + varighed_VÆRDI;
        if (Placering + varighed_VÆRDI > Størrelse) Hukommelse_filsystem.tilpasse_størrelse_Liste[Fil] = Placering + varighed_VÆRDI;
        return varighed_VÆRDI;
    }
    static int søge_fil(int 서술자, int FORSKYDNING_VÆRDI, int To_do_rod) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (종류[기술] != 2) return -29;
        if (To_do_rod < 0 || To_do_rod > 2) return -22;
        int Baggrund_VÆRDI = To_do_rod == 0 ? 0 : (To_do_rod == 1 ? fil_placere[기술] : Hukommelse_filsystem.tilpasse_størrelse_Liste[mål[기술]]);
        if (FORSKYDNING_VÆRDI > 0 && Baggrund_VÆRDI > 2147483647 - FORSKYDNING_VÆRDI) return -75;
        if (FORSKYDNING_VÆRDI < 0 && FORSKYDNING_VÆRDI < -Baggrund_VÆRDI) return -22;
        fil_placere[기술] = Baggrund_VÆRDI + FORSKYDNING_VÆRDI;
        return fil_placere[기술];
    }
    static int 서술자복제(int 서술자, int 새서술자, boolean Tildel_VÆRDI, int Indstillinger) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (새서술자 < 0 || 새서술자 >= 서술자한도) return Tildel_VÆRDI ? -9 : -22;
        if (Tildel_VÆRDI && 서술자 == 새서술자) return 새서술자;
        if (Tildel_VÆRDI) { if (åben_handle[새서술자] != 0) Luk_fil(새서술자); }
        else { 새서술자 = 빈서술자(새서술자); if (새서술자 < 0) return 새서술자; }
        åben_handle[새서술자] = 기술 + 1; 서술자설정[새서술자] = Indstillinger; referere_TÆL[기술]++;
        return 새서술자;
    }
    static int fjerne_fil_post_navn(int navn_mail) {
        int varighed_VÆRDI = 경로읽기(navn_mail);
        if (varighed_VÆRDI < 0) return varighed_VÆRDI;
        int Fil = Hukommelse_filsystem.Søg_post(sti_navn, varighed_VÆRDI);
        if (Fil < 0) return Fil;
        Hukommelse_filsystem.이름들[Fil * 64] = 0;
        return 0;
    }
    static int sæt_fil_varighed(int 서술자, int varighed_VÆRDI) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (종류[기술] != 2 || (åben_Indstillinger[기술] & 3) == 0 || varighed_VÆRDI < 0) return -22;
        if (varighed_VÆRDI > Hukommelse_filsystem.최대크기) return -27;
        int Fil = mål[기술], mail = enhed_VÆRDI.fil_Hukommelse() + Fil * Hukommelse_filsystem.최대크기;
        for (int INDEKS = Hukommelse_filsystem.tilpasse_størrelse_Liste[Fil]; INDEKS < varighed_VÆRDI; INDEKS++) enhed_VÆRDI.skrive_Hukommelse(mail + INDEKS, 0);
        Hukommelse_filsystem.tilpasse_størrelse_Liste[Fil] = varighed_VÆRDI;
        return 0;
    }
    static int 파일상태읽기(int 서술자, int mail) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (!udførelse_Leder.klippe(mail, 48)) return -14;
        for (int INDEKS = 0; INDEKS < 12; INDEKS++) udførelse_Leder.skrive_tal(mail + INDEKS * 4, 0);
        int Fil = mål[기술], Størrelse = 종류[기술] == 2 ? Hukommelse_filsystem.tilpasse_størrelse_Liste[Fil] : 0;
        int 허가 = 종류[기술] == 2 ? Hukommelse_filsystem.허가들[Fil] : 438;
        udførelse_Leder.skrive_tal(mail, 1);
        udførelse_Leder.skrive_tal(mail + 4, 종류[기술] == 2 ? Fil + 1 : 100 + 기술);
        udførelse_Leder.skrive_tal(mail + 8, (종류[기술] == 2 ? 32768 : (종류[기술] == 1 ? 8192 : 49152)) | 허가);
        udførelse_Leder.skrive_tal(mail + 12, 종류[기술] == 2 && Hukommelse_filsystem.이름들[Fil * 64] == 0 ? 0 : 1);
        udførelse_Leder.skrive_tal(mail + 28, Størrelse); udførelse_Leder.skrive_tal(mail + 32, 512);
        udførelse_Leder.skrive_tal(mail + 36, (Størrelse + 511) / 512);
        return 0;
    }
    static int 서술자제어(int 서술자, int Kommando, int VÆRDI) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (Kommando == 0 || Kommando == 1030) return 서술자복제(서술자, VÆRDI, false, Kommando == 1030 ? 1 : 0);
        if (Kommando == 1) return 서술자설정[서술자];
        if (Kommando == 2) { if ((VÆRDI & ~1) != 0) return -22; 서술자설정[서술자] = VÆRDI; return 0; }
        if (Kommando == 3) return åben_Indstillinger[기술];
        if (Kommando == 4) {
            if ((VÆRDI & ~(3 | 이어쓰기 | 기다리지않기)) != 0) return -95;
            åben_Indstillinger[기술] = (åben_Indstillinger[기술] & 3) | (VÆRDI & (이어쓰기 | 기다리지않기)); return 0;
        }
        return -95;
    }
    static int åbne_slutpunkt(int 주소체계, int 통신종류, int job_tal) {
        if (주소체계 != 2) return -97;
        if (통신종류 != 2) return -93;
        if (job_tal != 0 && job_tal != 17) return -93;
        int 서술자 = 빈서술자(0), 기술 = 빈기술();
        if (서술자 < 0 || 기술 < 0) return -24;
        return Tilslut(서술자, 기술, 3, 0, læse_skrive_flag);
    }
    static int 종단점기술(int 서술자) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        return 종류[기술] == 3 ? 기술 : -88;
    }
    static int mail_32(int mail) {
        return enhed_VÆRDI.기억읽기(mail) << 24 | enhed_VÆRDI.기억읽기(mail + 1) << 16
            | enhed_VÆRDI.기억읽기(mail + 2) << 8 | enhed_VÆRDI.기억읽기(mail + 3);
    }
    static int check_mail(int mail, int varighed_VÆRDI) {
        if (varighed_VÆRDI < 16) return -22;
        if (!udførelse_Leder.klippe(mail, 16)) return -14;
        return udførelse_Leder.짧은수(mail) == 2 ? 0 : -97;
    }
    static int BIND_mail(int 서술자, int mail, int varighed_VÆRDI) {
        int 기술 = 종단점기술(서술자);
        if (기술 < 0) return 기술;
        int KR = check_mail(mail, varighed_VÆRDI);
        if (KR < 0) return KR;
        if (netværk_handle[기술] != 0) return -22;
        int netværks_id = mail_32(mail + 4);
        if (netværks_id != 0 && netværks_id != netværk_Stak.내주소) return -99;
        int portnummer = enhed_VÆRDI.기억읽기(mail + 2) << 8 | enhed_VÆRDI.기억읽기(mail + 3);
        KR = netværk_Stak.Åbn(portnummer);
        if (KR < 0) return KR;
        netværk_handle[기술] = KR; mål[기술] = netværks_id;
        return 0;
    }
    static int Autofunktion_BIND(int 기술) {
        if (netværk_handle[기술] != 0) return 0;
        int KR = netværk_Stak.Åbn(0);
        if (KR < 0) return KR;
        netværk_handle[기술] = KR;
        return 0;
    }
    // sendto/recvfrom의 마지막 두 인자는 8바이트 anmodning 구조체로 전달한다.
    static int maile_datagram_data(int 서술자, int data_mail, int varighed_VÆRDI, int Indstillinger, int anmodet_mail) {
        int 기술 = 종단점기술(서술자);
        if (기술 < 0) return 기술;
        if (Indstillinger != 0) return -95;
        if (varighed_VÆRDI < 0 || varighed_VÆRDI > 1024) return -90;
        if (varighed_VÆRDI != 0 && !udførelse_Leder.klippe(data_mail, varighed_VÆRDI)) return -14;
        if (!udførelse_Leder.klippe(anmodet_mail, 8)) return -14;
        int mail = udførelse_Leder.tal(anmodet_mail);
        int KR = check_mail(mail, udførelse_Leder.tal(anmodet_mail + 4));
        if (KR < 0) return KR;
        int portnummer = enhed_VÆRDI.기억읽기(mail + 2) << 8 | enhed_VÆRDI.기억읽기(mail + 3);
        if (portnummer == 0) return -22;
        KR = Autofunktion_BIND(기술);
        if (KR < 0) return KR;
        for (int INDEKS = 0; INDEKS < varighed_VÆRDI; INDEKS++) overføre_data[INDEKS] = enhed_VÆRDI.기억읽기(data_mail + INDEKS);
        return netværk_Stak.maile(netværk_handle[기술], mail_32(mail + 4), portnummer, overføre_data, varighed_VÆRDI);
    }
    static void skrive_mail(int mail, int varighed_VÆRDI, int netværks_id, int portnummer) {
        for (int INDEKS = 0; INDEKS < varighed_VÆRDI && INDEKS < 16; INDEKS++) {
            int VÆRDI = 0;
            if (INDEKS == 0) VÆRDI = 2;
            if (INDEKS == 2) VÆRDI = portnummer >>> 8;
            if (INDEKS == 3) VÆRDI = portnummer;
            if (INDEKS >= 4 && INDEKS < 8) VÆRDI = netværks_id >>> (56 - INDEKS * 8);
            enhed_VÆRDI.skrive_Hukommelse(mail + INDEKS, VÆRDI & 255);
        }
    }
    static int modtage_datagram_data(int 서술자, int data_mail, int varighed_VÆRDI, int Indstillinger, int anmodet_mail) {
        int 기술 = 종단점기술(서술자);
        if (기술 < 0) return 기술;
        if ((Indstillinger & ~64) != 0) return -95;
        if (varighed_VÆRDI < 0) return -22;
        if (varighed_VÆRDI != 0 && !udførelse_Leder.klippe(data_mail, varighed_VÆRDI)) return -14;
        int mail = 0, mail_varighed_mail = 0, mail_varighed = 0;
        if (anmodet_mail != 0) {
            if (!udførelse_Leder.klippe(anmodet_mail, 8)) return -14;
            mail = udførelse_Leder.tal(anmodet_mail); mail_varighed_mail = udførelse_Leder.tal(anmodet_mail + 4);
            if (mail != 0) {
                if (!udførelse_Leder.klippe(mail_varighed_mail, 4)) return -14;
                mail_varighed = udførelse_Leder.tal(mail_varighed_mail);
                if (mail_varighed < 0) return -22;
                if (!udførelse_Leder.klippe(mail, mail_varighed < 16 ? mail_varighed : 16)) return -14;
            }
        }
        int KR = Autofunktion_BIND(기술);
        if (KR < 0) return KR;
        int Kør_2 = enhed_VÆRDI.밀리초();
        while (true) {
            KR = netværk_Stak.modtage(netværk_handle[기술], overføre_data, 1024, 0);
            if (KR != -11) break;
            if ((Indstillinger & 64) != 0 || (åben_Indstillinger[기술] & 기다리지않기) != 0) return -11;
            if (수신대기밀리초[기술] > 0 && enhed_VÆRDI.밀리초() - Kør_2 >= 수신대기밀리초[기술]) return -11;
            if (enhed_VÆRDI.사용자남은밀리초() <= 10) return -11;
            enhed_VÆRDI.잠시양보();
        }
        if (KR < 0) return KR;
        if (KR > varighed_VÆRDI) KR = varighed_VÆRDI;
        for (int INDEKS = 0; INDEKS < KR; INDEKS++) enhed_VÆRDI.skrive_Hukommelse(data_mail + INDEKS, overføre_data[INDEKS]);
        if (mail != 0) {
            skrive_mail(mail, mail_varighed, netværk_Stak.peer_mail(netværk_handle[기술]), netværk_Stak.peer_portnummer(netværk_handle[기술]));
            udførelse_Leder.skrive_tal(mail_varighed_mail, 16);
        }
        return KR;
    }
    static int 통신주소읽기(int 서술자, int mail, int varighed_mail) {
        int 기술 = 종단점기술(서술자);
        if (기술 < 0) return 기술;
        if (!udførelse_Leder.klippe(varighed_mail, 4)) return -14;
        int varighed_VÆRDI = udførelse_Leder.tal(varighed_mail);
        if (varighed_VÆRDI < 0) return -22;
        if (!udførelse_Leder.klippe(mail, varighed_VÆRDI < 16 ? varighed_VÆRDI : 16)) return -14;
        int udvidelsesstik_post = netværk_Stak.INDEKS(netværk_handle[기술]);
        skrive_mail(mail, varighed_VÆRDI, mål[기술], udvidelsesstik_post < 0 ? 0 : netværk_Stak.접속번호들[udvidelsesstik_post]);
        udførelse_Leder.skrive_tal(varighed_mail, 16);
        return 0;
    }
    static int sæt_modtage_TIMEOUT(int 서술자, int 밀리초) {
        int 기술 = 종단점기술(서술자);
        if (기술 < 0) return 기술;
        if (밀리초 < 0 || 밀리초 > 2000) return -22;
        수신대기밀리초[기술] = 밀리초;
        return 0;
    }
}
