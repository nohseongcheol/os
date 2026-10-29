// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 단일 bruker 과정의 파일서술자와 열린 Fil 기술을 분리한다. 호출 번호는 POSIX ABI 문서에 기록한다. */
public final class 파일서술자관리 {
    static final int 서술자한도 = 32;
    static final int lese_og_skrive_flagg = 2, åpne_oppføring = 64, 독점생성 = 128, tømme_Innhold = 512;
    static final int 이어쓰기 = 1024, 기다리지않기 = 2048, 실행시닫기 = 524288;
    static int[] åpen_håndtak = new int[서술자한도], 서술자설정 = new int[서술자한도];
    static int[] 종류 = new int[서술자한도], mål = new int[서술자한도];
    static int[] Fil_plassere = new int[서술자한도], åpen_Innstillinger = new int[서술자한도], referere_ANTALL = new int[서술자한도];
    static int[] nettverk_håndtak = new int[서술자한도], 수신대기밀리초 = new int[서술자한도];
    static int[] bane_navn = new int[64], overføre_data = new int[1024];

    static int 기술찾기(int 파일서술자) {
        if (파일서술자 < 0 || 파일서술자 >= 서술자한도) return -9;
        return åpen_håndtak[파일서술자] - 1;
    }
    static int 빈서술자(int Kjør_2) {
        for (int INDEKS = Kjør_2; INDEKS < 서술자한도; INDEKS++) if (åpen_håndtak[INDEKS] == 0) return INDEKS;
        return -24;
    }
    static int tom_håndtak() {
        for (int INDEKS = 0; INDEKS < 서술자한도; INDEKS++) if (referere_ANTALL[INDEKS] == 0) return INDEKS;
        return -24;
    }
    static int Koble_til(int 서술자, int 기술, int 파일종류, int Fil_mål, int Innstillinger) {
        åpen_håndtak[서술자] = 기술 + 1; 서술자설정[서술자] = (Innstillinger & 실행시닫기) != 0 ? 1 : 0;
        종류[기술] = 파일종류; mål[기술] = Fil_mål; referere_ANTALL[기술] = 1;
        åpen_Innstillinger[기술] = Innstillinger & (3 | 이어쓰기 | 기다리지않기); Fil_plassere[기술] = 0;
        nettverk_håndtak[기술] = 0; 수신대기밀리초[기술] = 0;
        return 서술자;
    }
    static void START_Prosess() {
        RENSK_Prosess();
        for (int INDEKS = 0; INDEKS < 3; INDEKS++) Koble_til(INDEKS, INDEKS, 1, INDEKS, INDEKS == 0 ? 0 : 1);
    }
    static void RENSK_Prosess() {
        for (int INDEKS = 0; INDEKS < 서술자한도; INDEKS++) if (åpen_håndtak[INDEKS] != 0) Lukk_Fil(INDEKS);
    }
    static int Lukk_Fil(int 서술자) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        åpen_håndtak[서술자] = 0; 서술자설정[서술자] = 0;
        referere_ANTALL[기술]--;
        if (referere_ANTALL[기술] == 0) {
            if (종류[기술] == 2) Minne_filsystem.åpen_ANTALL[mål[기술]]--;
            if (종류[기술] == 3 && nettverk_håndtak[기술] != 0) nettverk_stakk.Lukk(nettverk_håndtak[기술]);
            종류[기술] = 0;
        }
        return 0;
    }
    // C 경로는 NUL 끝 byte_VERDI 문자열이다. 루트의 한 이름만 지원한다.
    static int 경로읽기(int e_post) {
        if (!kjøring_overordnet.klippe(e_post, 1)) return -14;
        int Posisjon = enhet_VERDI.기억읽기(e_post) == '/' ? 1 : 0;
        for (int lengde_VERDI = 0; lengde_VERDI < 64; lengde_VERDI++) {
            if (!kjøring_overordnet.klippe(e_post + Posisjon + lengde_VERDI, 1)) return -14;
            int VERDI = enhet_VERDI.기억읽기(e_post + Posisjon + lengde_VERDI);
            bane_navn[lengde_VERDI] = VERDI;
            if (VERDI == 0) return lengde_VERDI == 0 ? -2 : (Minne_filsystem.sjekk_navn(bane_navn, lengde_VERDI) ? lengde_VERDI : -22);
            if (VERDI == '/') return -20;
        }
        return -36;
    }
    static int åpen_Fil(int navn_e_post, int Innstillinger, int 허가) {
        int lengde_VERDI = 경로읽기(navn_e_post);
        if (lengde_VERDI < 0) return lengde_VERDI;
        if ((Innstillinger & ~(3 | åpne_oppføring | 독점생성 | tømme_Innhold | 이어쓰기 | 기다리지않기 | 실행시닫기)) != 0) return -95;
        if ((Innstillinger & 3) == 3 || ((Innstillinger & tømme_Innhold) != 0 && (Innstillinger & 3) == 0)) return -22;
        int Fil = Minne_filsystem.Søk_oppføring(bane_navn, lengde_VERDI);
        if (Fil >= 0 && (Innstillinger & (åpne_oppføring | 독점생성)) == (åpne_oppføring | 독점생성)) return -17;
        if (Fil == -2 && (Innstillinger & åpne_oppføring) == 0) return -2;
        int 서술자 = 빈서술자(0), 기술 = tom_håndtak();
        if (서술자 < 0 || 기술 < 0) return -24;
        if (Fil == -2) {
            int KR = Minne_filsystem.Store_VERDI(bane_navn, lengde_VERDI, bane_navn, 0);
            if (KR < 0) return KR;
            Fil = Minne_filsystem.Søk_oppføring(bane_navn, lengde_VERDI);
            Minne_filsystem.허가들[Fil] = 허가 & 511;
        }
        if (Fil < 0) return Fil;
        if ((Innstillinger & tømme_Innhold) != 0) Minne_filsystem.skalere_Liste[Fil] = 0;
        Minne_filsystem.åpen_ANTALL[Fil]++;
        return Koble_til(서술자, 기술, 2, Fil, Innstillinger);
    }
    static int 파일읽기(int 서술자, int data_e_post, int lengde_VERDI) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0 || (åpen_Innstillinger[기술] & 3) == 1) return -9;
        if (lengde_VERDI < 0) return -22;
        if (lengde_VERDI == 0) return 0;
        if (!kjøring_overordnet.klippe(data_e_post, lengde_VERDI)) return -14;
        if (종류[기술] == 3) return motta_datagram_data(서술자, data_e_post, lengde_VERDI, 0, 0);
        if (종류[기술] == 1) {
            int MOTTATT_AVKAST_ANTALL = 0;
            while (MOTTATT_AVKAST_ANTALL < lengde_VERDI) {
                int VERDI = SMS_Terminal.직렬읽기();
                if (VERDI < 0) VERDI = tastatur.Les();
                if (VERDI < 0) {
                    if (MOTTATT_AVKAST_ANTALL > 0) return MOTTATT_AVKAST_ANTALL;
                    if ((åpen_Innstillinger[기술] & 기다리지않기) != 0) return -11;
                    if (enhet_VERDI.사용자남은밀리초() <= 10) return -11;
                    nettverk_stakk.bekrefte(); enhet_VERDI.잠시양보();
                } else {
                    enhet_VERDI.skrive_Minne(data_e_post + MOTTATT_AVKAST_ANTALL, VERDI); MOTTATT_AVKAST_ANTALL++;
                }
            }
            return MOTTATT_AVKAST_ANTALL;
        }
        int Fil = mål[기술], Posisjon = Fil_plassere[기술];
        if (Posisjon >= Minne_filsystem.skalere_Liste[Fil]) return 0;
        if (lengde_VERDI > Minne_filsystem.skalere_Liste[Fil] - Posisjon) lengde_VERDI = Minne_filsystem.skalere_Liste[Fil] - Posisjon;
        int 원본주소 = enhet_VERDI.Fil_Minne() + Fil * Minne_filsystem.최대크기 + Posisjon;
        for (int INDEKS = 0; INDEKS < lengde_VERDI; INDEKS++) enhet_VERDI.skrive_Minne(data_e_post + INDEKS, enhet_VERDI.기억읽기(원본주소 + INDEKS));
        Fil_plassere[기술] += lengde_VERDI;
        return lengde_VERDI;
    }
    static int skrive_Fil(int 서술자, int data_e_post, int lengde_VERDI) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0 || (åpen_Innstillinger[기술] & 3) == 0) return -9;
        if (lengde_VERDI < 0) return -22;
        if (lengde_VERDI == 0) return 0;
        if (!kjøring_overordnet.klippe(data_e_post, lengde_VERDI)) return -14;
        if (종류[기술] == 3) return -89; // 연결하지 않은 자료전문 종단점에는 mål_VERDI 주소가 필요하다.
        if (종류[기술] == 1) {
            if (lengde_VERDI > 16384) lengde_VERDI = 16384;
            for (int INDEKS = 0; INDEKS < lengde_VERDI; INDEKS++) {
                int VERDI = enhet_VERDI.기억읽기(data_e_post + INDEKS);
                SMS_Terminal.직렬바이트(VERDI); SMS_Terminal.skjermbilde_tegn(VERDI);
            }
            return lengde_VERDI;
        }
        int Fil = mål[기술], Størrelse = Minne_filsystem.skalere_Liste[Fil];
        int Posisjon = (åpen_Innstillinger[기술] & 이어쓰기) != 0 ? Størrelse : Fil_plassere[기술];
        if (Posisjon >= Minne_filsystem.최대크기) return -27;
        if (lengde_VERDI > Minne_filsystem.최대크기 - Posisjon) lengde_VERDI = Minne_filsystem.최대크기 - Posisjon;
        int mål_e_post_08bbd577 = enhet_VERDI.Fil_Minne() + Fil * Minne_filsystem.최대크기;
        for (int INDEKS = Størrelse; INDEKS < Posisjon; INDEKS++) enhet_VERDI.skrive_Minne(mål_e_post_08bbd577 + INDEKS, 0);
        for (int INDEKS = 0; INDEKS < lengde_VERDI; INDEKS++) enhet_VERDI.skrive_Minne(mål_e_post_08bbd577 + Posisjon + INDEKS, enhet_VERDI.기억읽기(data_e_post + INDEKS));
        Fil_plassere[기술] = Posisjon + lengde_VERDI;
        if (Posisjon + lengde_VERDI > Størrelse) Minne_filsystem.skalere_Liste[Fil] = Posisjon + lengde_VERDI;
        return lengde_VERDI;
    }
    static int søk_Fil(int 서술자, int FORSKYVNING_VERDI, int speile_rot) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (종류[기술] != 2) return -29;
        if (speile_rot < 0 || speile_rot > 2) return -22;
        int bakgrunn_VERDI = speile_rot == 0 ? 0 : (speile_rot == 1 ? Fil_plassere[기술] : Minne_filsystem.skalere_Liste[mål[기술]]);
        if (FORSKYVNING_VERDI > 0 && bakgrunn_VERDI > 2147483647 - FORSKYVNING_VERDI) return -75;
        if (FORSKYVNING_VERDI < 0 && FORSKYVNING_VERDI < -bakgrunn_VERDI) return -22;
        Fil_plassere[기술] = bakgrunn_VERDI + FORSKYVNING_VERDI;
        return Fil_plassere[기술];
    }
    static int 서술자복제(int 서술자, int 새서술자, boolean overdra_VERDI, int Innstillinger) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (새서술자 < 0 || 새서술자 >= 서술자한도) return overdra_VERDI ? -9 : -22;
        if (overdra_VERDI && 서술자 == 새서술자) return 새서술자;
        if (overdra_VERDI) { if (åpen_håndtak[새서술자] != 0) Lukk_Fil(새서술자); }
        else { 새서술자 = 빈서술자(새서술자); if (새서술자 < 0) return 새서술자; }
        åpen_håndtak[새서술자] = 기술 + 1; 서술자설정[새서술자] = Innstillinger; referere_ANTALL[기술]++;
        return 새서술자;
    }
    static int fjerne_Fil_oppføring_navn(int navn_e_post) {
        int lengde_VERDI = 경로읽기(navn_e_post);
        if (lengde_VERDI < 0) return lengde_VERDI;
        int Fil = Minne_filsystem.Søk_oppføring(bane_navn, lengde_VERDI);
        if (Fil < 0) return Fil;
        Minne_filsystem.이름들[Fil * 64] = 0;
        return 0;
    }
    static int sett_Fil_lengde(int 서술자, int lengde_VERDI) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (종류[기술] != 2 || (åpen_Innstillinger[기술] & 3) == 0 || lengde_VERDI < 0) return -22;
        if (lengde_VERDI > Minne_filsystem.최대크기) return -27;
        int Fil = mål[기술], e_post = enhet_VERDI.Fil_Minne() + Fil * Minne_filsystem.최대크기;
        for (int INDEKS = Minne_filsystem.skalere_Liste[Fil]; INDEKS < lengde_VERDI; INDEKS++) enhet_VERDI.skrive_Minne(e_post + INDEKS, 0);
        Minne_filsystem.skalere_Liste[Fil] = lengde_VERDI;
        return 0;
    }
    static int 파일상태읽기(int 서술자, int e_post) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (!kjøring_overordnet.klippe(e_post, 48)) return -14;
        for (int INDEKS = 0; INDEKS < 12; INDEKS++) kjøring_overordnet.skrive_nummer(e_post + INDEKS * 4, 0);
        int Fil = mål[기술], Størrelse = 종류[기술] == 2 ? Minne_filsystem.skalere_Liste[Fil] : 0;
        int 허가 = 종류[기술] == 2 ? Minne_filsystem.허가들[Fil] : 438;
        kjøring_overordnet.skrive_nummer(e_post, 1);
        kjøring_overordnet.skrive_nummer(e_post + 4, 종류[기술] == 2 ? Fil + 1 : 100 + 기술);
        kjøring_overordnet.skrive_nummer(e_post + 8, (종류[기술] == 2 ? 32768 : (종류[기술] == 1 ? 8192 : 49152)) | 허가);
        kjøring_overordnet.skrive_nummer(e_post + 12, 종류[기술] == 2 && Minne_filsystem.이름들[Fil * 64] == 0 ? 0 : 1);
        kjøring_overordnet.skrive_nummer(e_post + 28, Størrelse); kjøring_overordnet.skrive_nummer(e_post + 32, 512);
        kjøring_overordnet.skrive_nummer(e_post + 36, (Størrelse + 511) / 512);
        return 0;
    }
    static int 서술자제어(int 서술자, int Kommando, int VERDI) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (Kommando == 0 || Kommando == 1030) return 서술자복제(서술자, VERDI, false, Kommando == 1030 ? 1 : 0);
        if (Kommando == 1) return 서술자설정[서술자];
        if (Kommando == 2) { if ((VERDI & ~1) != 0) return -22; 서술자설정[서술자] = VERDI; return 0; }
        if (Kommando == 3) return åpen_Innstillinger[기술];
        if (Kommando == 4) {
            if ((VERDI & ~(3 | 이어쓰기 | 기다리지않기)) != 0) return -95;
            åpen_Innstillinger[기술] = (åpen_Innstillinger[기술] & 3) | (VERDI & (이어쓰기 | 기다리지않기)); return 0;
        }
        return -95;
    }
    static int åpne_deltaker(int 주소체계, int 통신종류, int sak_nummer) {
        if (주소체계 != 2) return -97;
        if (통신종류 != 2) return -93;
        if (sak_nummer != 0 && sak_nummer != 17) return -93;
        int 서술자 = 빈서술자(0), 기술 = tom_håndtak();
        if (서술자 < 0 || 기술 < 0) return -24;
        return Koble_til(서술자, 기술, 3, 0, lese_og_skrive_flagg);
    }
    static int 종단점기술(int 서술자) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        return 종류[기술] == 3 ? 기술 : -88;
    }
    static int e_post_32(int e_post) {
        return enhet_VERDI.기억읽기(e_post) << 24 | enhet_VERDI.기억읽기(e_post + 1) << 16
            | enhet_VERDI.기억읽기(e_post + 2) << 8 | enhet_VERDI.기억읽기(e_post + 3);
    }
    static int sjekk_e_post(int e_post, int lengde_VERDI) {
        if (lengde_VERDI < 16) return -22;
        if (!kjøring_overordnet.klippe(e_post, 16)) return -14;
        return kjøring_overordnet.짧은수(e_post) == 2 ? 0 : -97;
    }
    static int BIND_e_post(int 서술자, int e_post, int lengde_VERDI) {
        int 기술 = 종단점기술(서술자);
        if (기술 < 0) return 기술;
        int KR = sjekk_e_post(e_post, lengde_VERDI);
        if (KR < 0) return KR;
        if (nettverk_håndtak[기술] != 0) return -22;
        int nettverks_ID = e_post_32(e_post + 4);
        if (nettverks_ID != 0 && nettverks_ID != nettverk_stakk.내주소) return -99;
        int portnummer = enhet_VERDI.기억읽기(e_post + 2) << 8 | enhet_VERDI.기억읽기(e_post + 3);
        KR = nettverk_stakk.Åpne(portnummer);
        if (KR < 0) return KR;
        nettverk_håndtak[기술] = KR; mål[기술] = nettverks_ID;
        return 0;
    }
    static int Auto_BIND(int 기술) {
        if (nettverk_håndtak[기술] != 0) return 0;
        int KR = nettverk_stakk.Åpne(0);
        if (KR < 0) return KR;
        nettverk_håndtak[기술] = KR;
        return 0;
    }
    // sendto/recvfrom의 마지막 두 인자는 8바이트 forespørsel 구조체로 전달한다.
    static int sende_datagram_data(int 서술자, int data_e_post, int lengde_VERDI, int Innstillinger, int ønsket_e_post) {
        int 기술 = 종단점기술(서술자);
        if (기술 < 0) return 기술;
        if (Innstillinger != 0) return -95;
        if (lengde_VERDI < 0 || lengde_VERDI > 1024) return -90;
        if (lengde_VERDI != 0 && !kjøring_overordnet.klippe(data_e_post, lengde_VERDI)) return -14;
        if (!kjøring_overordnet.klippe(ønsket_e_post, 8)) return -14;
        int e_post = kjøring_overordnet.nummer(ønsket_e_post);
        int KR = sjekk_e_post(e_post, kjøring_overordnet.nummer(ønsket_e_post + 4));
        if (KR < 0) return KR;
        int portnummer = enhet_VERDI.기억읽기(e_post + 2) << 8 | enhet_VERDI.기억읽기(e_post + 3);
        if (portnummer == 0) return -22;
        KR = Auto_BIND(기술);
        if (KR < 0) return KR;
        for (int INDEKS = 0; INDEKS < lengde_VERDI; INDEKS++) overføre_data[INDEKS] = enhet_VERDI.기억읽기(data_e_post + INDEKS);
        return nettverk_stakk.sende(nettverk_håndtak[기술], e_post_32(e_post + 4), portnummer, overføre_data, lengde_VERDI);
    }
    static void skrive_e_post(int e_post, int lengde_VERDI, int nettverks_ID, int portnummer) {
        for (int INDEKS = 0; INDEKS < lengde_VERDI && INDEKS < 16; INDEKS++) {
            int VERDI = 0;
            if (INDEKS == 0) VERDI = 2;
            if (INDEKS == 2) VERDI = portnummer >>> 8;
            if (INDEKS == 3) VERDI = portnummer;
            if (INDEKS >= 4 && INDEKS < 8) VERDI = nettverks_ID >>> (56 - INDEKS * 8);
            enhet_VERDI.skrive_Minne(e_post + INDEKS, VERDI & 255);
        }
    }
    static int motta_datagram_data(int 서술자, int data_e_post, int lengde_VERDI, int Innstillinger, int ønsket_e_post) {
        int 기술 = 종단점기술(서술자);
        if (기술 < 0) return 기술;
        if ((Innstillinger & ~64) != 0) return -95;
        if (lengde_VERDI < 0) return -22;
        if (lengde_VERDI != 0 && !kjøring_overordnet.klippe(data_e_post, lengde_VERDI)) return -14;
        int e_post = 0, e_post_lengde_e_post = 0, e_post_lengde = 0;
        if (ønsket_e_post != 0) {
            if (!kjøring_overordnet.klippe(ønsket_e_post, 8)) return -14;
            e_post = kjøring_overordnet.nummer(ønsket_e_post); e_post_lengde_e_post = kjøring_overordnet.nummer(ønsket_e_post + 4);
            if (e_post != 0) {
                if (!kjøring_overordnet.klippe(e_post_lengde_e_post, 4)) return -14;
                e_post_lengde = kjøring_overordnet.nummer(e_post_lengde_e_post);
                if (e_post_lengde < 0) return -22;
                if (!kjøring_overordnet.klippe(e_post, e_post_lengde < 16 ? e_post_lengde : 16)) return -14;
            }
        }
        int KR = Auto_BIND(기술);
        if (KR < 0) return KR;
        int Kjør_2 = enhet_VERDI.밀리초();
        while (true) {
            KR = nettverk_stakk.motta(nettverk_håndtak[기술], overføre_data, 1024, 0);
            if (KR != -11) break;
            if ((Innstillinger & 64) != 0 || (åpen_Innstillinger[기술] & 기다리지않기) != 0) return -11;
            if (수신대기밀리초[기술] > 0 && enhet_VERDI.밀리초() - Kjør_2 >= 수신대기밀리초[기술]) return -11;
            if (enhet_VERDI.사용자남은밀리초() <= 10) return -11;
            enhet_VERDI.잠시양보();
        }
        if (KR < 0) return KR;
        if (KR > lengde_VERDI) KR = lengde_VERDI;
        for (int INDEKS = 0; INDEKS < KR; INDEKS++) enhet_VERDI.skrive_Minne(data_e_post + INDEKS, overføre_data[INDEKS]);
        if (e_post != 0) {
            skrive_e_post(e_post, e_post_lengde, nettverk_stakk.node_e_post(nettverk_håndtak[기술]), nettverk_stakk.node_portnummer(nettverk_håndtak[기술]));
            kjøring_overordnet.skrive_nummer(e_post_lengde_e_post, 16);
        }
        return KR;
    }
    static int 통신주소읽기(int 서술자, int e_post, int lengde_e_post) {
        int 기술 = 종단점기술(서술자);
        if (기술 < 0) return 기술;
        if (!kjøring_overordnet.klippe(lengde_e_post, 4)) return -14;
        int lengde_VERDI = kjøring_overordnet.nummer(lengde_e_post);
        if (lengde_VERDI < 0) return -22;
        if (!kjøring_overordnet.klippe(e_post, lengde_VERDI < 16 ? lengde_VERDI : 16)) return -14;
        int åpning_oppføring = nettverk_stakk.INDEKS(nettverk_håndtak[기술]);
        skrive_e_post(e_post, lengde_VERDI, mål[기술], åpning_oppføring < 0 ? 0 : nettverk_stakk.접속번호들[åpning_oppføring]);
        kjøring_overordnet.skrive_nummer(lengde_e_post, 16);
        return 0;
    }
    static int sett_motta_TIMEOUT(int 서술자, int 밀리초) {
        int 기술 = 종단점기술(서술자);
        if (기술 < 0) return 기술;
        if (밀리초 < 0 || 밀리초 > 2000) return -22;
        수신대기밀리초[기술] = 밀리초;
        return 0;
    }
}
