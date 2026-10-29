// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 단일 användarutrymme 과정의 파일서술자와 열린 filnamn 기술을 분리한다. 호출 번호는 POSIX ABI 문서에 기록한다. */
public final class 파일서술자관리 {
    static final int 서술자한도 = 32;
    static final int läsa_skriva_flagga = 2, Skapa_post = 64, 독점생성 = 128, rensa_Innehåll = 512;
    static final int 이어쓰기 = 1024, 기다리지않기 = 2048, 실행시닫기 = 524288;
    static int[] skapa_handtag = new int[서술자한도], 서술자설정 = new int[서술자한도];
    static int[] variant_värde = new int[서술자한도], mål = new int[서술자한도];
    static int[] fil_placera = new int[서술자한도], skapa_Inställningar = new int[서술자한도], referens_ANTAL = new int[서술자한도];
    static int[] nätverk_handtag = new int[서술자한도], 수신대기밀리초 = new int[서술자한도];
    static int[] väg_namn = new int[64], Överför_data = new int[1024];

    static int 기술찾기(int 파일서술자) {
        if (파일서술자 < 0 || 파일서술자 >= 서술자한도) return -9;
        return skapa_handtag[파일서술자] - 1;
    }
    static int 빈서술자(int Kör) {
        for (int INDEX = Kör; INDEX < 서술자한도; INDEX++) if (skapa_handtag[INDEX] == 0) return INDEX;
        return -24;
    }
    static int 빈기술() {
        for (int INDEX = 0; INDEX < 서술자한도; INDEX++) if (referens_ANTAL[INDEX] == 0) return INDEX;
        return -24;
    }
    static int Anslut(int 서술자, int 기술, int fil_variant, int fil_mål, int Inställningar) {
        skapa_handtag[서술자] = 기술 + 1; 서술자설정[서술자] = (Inställningar & 실행시닫기) != 0 ? 1 : 0;
        variant_värde[기술] = fil_variant; mål[기술] = fil_mål; referens_ANTAL[기술] = 1;
        skapa_Inställningar[기술] = Inställningar & (3 | 이어쓰기 | 기다리지않기); fil_placera[기술] = 0;
        nätverk_handtag[기술] = 0; 수신대기밀리초[기술] = 0;
        return 서술자;
    }
    static void START_Process() {
        Rent_Process();
        for (int INDEX = 0; INDEX < 3; INDEX++) Anslut(INDEX, INDEX, 1, INDEX, INDEX == 0 ? 0 : 1);
    }
    static void Rent_Process() {
        for (int INDEX = 0; INDEX < 서술자한도; INDEX++) if (skapa_handtag[INDEX] != 0) Stäng_fil(INDEX);
    }
    static int Stäng_fil(int 서술자) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        skapa_handtag[서술자] = 0; 서술자설정[서술자] = 0;
        referens_ANTAL[기술]--;
        if (referens_ANTAL[기술] == 0) {
            if (variant_värde[기술] == 2) Minne_filsystem.skapa_ANTAL[mål[기술]]--;
            if (variant_värde[기술] == 3 && nätverk_handtag[기술] != 0) nätverk_Stack.Stäng(nätverk_handtag[기술]);
            variant_värde[기술] = 0;
        }
        return 0;
    }
    // C 경로는 NUL 끝 byte_värde 문자열이다. 루트의 한 이름만 지원한다.
    static int läsa_väg(int Adress) {
        if (!körning_Ansvarig.klipp(Adress, 1)) return -14;
        int position = enhet_värde.läsa_Minne(Adress) == '/' ? 1 : 0;
        for (int längd_värde = 0; längd_värde < 64; längd_värde++) {
            if (!körning_Ansvarig.klipp(Adress + position + längd_värde, 1)) return -14;
            int värde = enhet_värde.läsa_Minne(Adress + position + längd_värde);
            väg_namn[längd_värde] = värde;
            if (värde == 0) return längd_värde == 0 ? -2 : (Minne_filsystem.check_namn(väg_namn, längd_värde) ? längd_värde : -22);
            if (värde == '/') return -20;
        }
        return -36;
    }
    static int skapa_fil(int namn_ADRESS, int Inställningar, int beviljande_behörighet) {
        int längd_värde = läsa_väg(namn_ADRESS);
        if (längd_värde < 0) return längd_värde;
        if ((Inställningar & ~(3 | Skapa_post | 독점생성 | rensa_Innehåll | 이어쓰기 | 기다리지않기 | 실행시닫기)) != 0) return -95;
        if ((Inställningar & 3) == 3 || ((Inställningar & rensa_Innehåll) != 0 && (Inställningar & 3) == 0)) return -22;
        int filnamn = Minne_filsystem.Sök_post(väg_namn, längd_värde);
        if (filnamn >= 0 && (Inställningar & (Skapa_post | 독점생성)) == (Skapa_post | 독점생성)) return -17;
        if (filnamn == -2 && (Inställningar & Skapa_post) == 0) return -2;
        int 서술자 = 빈서술자(0), 기술 = 빈기술();
        if (서술자 < 0 || 기술 < 0) return -24;
        if (filnamn == -2) {
            int RESULTAT = Minne_filsystem.Store_värde(väg_namn, längd_värde, väg_namn, 0);
            if (RESULTAT < 0) return RESULTAT;
            filnamn = Minne_filsystem.Sök_post(väg_namn, längd_värde);
            Minne_filsystem.허가들[filnamn] = beviljande_behörighet & 511;
        }
        if (filnamn < 0) return filnamn;
        if ((Inställningar & rensa_Innehåll) != 0) Minne_filsystem.storlek_ange[filnamn] = 0;
        Minne_filsystem.skapa_ANTAL[filnamn]++;
        return Anslut(서술자, 기술, 2, filnamn, Inställningar);
    }
    static int läsa_fil(int 서술자, int data_ADRESS, int längd_värde) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0 || (skapa_Inställningar[기술] & 3) == 1) return -9;
        if (längd_värde < 0) return -22;
        if (längd_värde == 0) return 0;
        if (!körning_Ansvarig.klipp(data_ADRESS, längd_värde)) return -14;
        if (variant_värde[기술] == 3) return få_datagram_data(서술자, data_ADRESS, längd_värde, 0, 0);
        if (variant_värde[기술] == 1) {
            int BELOPP_ANTAL = 0;
            while (BELOPP_ANTAL < längd_värde) {
                int värde = SMS_Terminal.직렬읽기();
                if (värde < 0) värde = tangentbord.Läs();
                if (värde < 0) {
                    if (BELOPP_ANTAL > 0) return BELOPP_ANTAL;
                    if ((skapa_Inställningar[기술] & 기다리지않기) != 0) return -11;
                    if (enhet_värde.사용자남은밀리초() <= 10) return -11;
                    nätverk_Stack.verifiera(); enhet_värde.잠시양보();
                } else {
                    enhet_värde.skriva_Minne(data_ADRESS + BELOPP_ANTAL, värde); BELOPP_ANTAL++;
                }
            }
            return BELOPP_ANTAL;
        }
        int filnamn = mål[기술], position = fil_placera[기술];
        if (position >= Minne_filsystem.storlek_ange[filnamn]) return 0;
        if (längd_värde > Minne_filsystem.storlek_ange[filnamn] - position) längd_värde = Minne_filsystem.storlek_ange[filnamn] - position;
        int 원본주소 = enhet_värde.fil_Minne() + filnamn * Minne_filsystem.최대크기 + position;
        for (int INDEX = 0; INDEX < längd_värde; INDEX++) enhet_värde.skriva_Minne(data_ADRESS + INDEX, enhet_värde.läsa_Minne(원본주소 + INDEX));
        fil_placera[기술] += längd_värde;
        return längd_värde;
    }
    static int skriva_fil(int 서술자, int data_ADRESS, int längd_värde) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0 || (skapa_Inställningar[기술] & 3) == 0) return -9;
        if (längd_värde < 0) return -22;
        if (längd_värde == 0) return 0;
        if (!körning_Ansvarig.klipp(data_ADRESS, längd_värde)) return -14;
        if (variant_värde[기술] == 3) return -89; // 연결하지 않은 자료전문 종단점에는 mål_värde 주소가 필요하다.
        if (variant_värde[기술] == 1) {
            if (längd_värde > 16384) längd_värde = 16384;
            for (int INDEX = 0; INDEX < längd_värde; INDEX++) {
                int värde = enhet_värde.läsa_Minne(data_ADRESS + INDEX);
                SMS_Terminal.직렬바이트(värde); SMS_Terminal.skärmbild_tecken(värde);
            }
            return längd_värde;
        }
        int filnamn = mål[기술], Storlek = Minne_filsystem.storlek_ange[filnamn];
        int position = (skapa_Inställningar[기술] & 이어쓰기) != 0 ? Storlek : fil_placera[기술];
        if (position >= Minne_filsystem.최대크기) return -27;
        if (längd_värde > Minne_filsystem.최대크기 - position) längd_värde = Minne_filsystem.최대크기 - position;
        int mål_ADRESS_08bbd577 = enhet_värde.fil_Minne() + filnamn * Minne_filsystem.최대크기;
        for (int INDEX = Storlek; INDEX < position; INDEX++) enhet_värde.skriva_Minne(mål_ADRESS_08bbd577 + INDEX, 0);
        for (int INDEX = 0; INDEX < längd_värde; INDEX++) enhet_värde.skriva_Minne(mål_ADRESS_08bbd577 + position + INDEX, enhet_värde.läsa_Minne(data_ADRESS + INDEX));
        fil_placera[기술] = position + längd_värde;
        if (position + längd_värde > Storlek) Minne_filsystem.storlek_ange[filnamn] = position + längd_värde;
        return längd_värde;
    }
    static int söka_fil(int 서술자, int FÖRSKJUTNING_värde, int åtgärd_rot) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (variant_värde[기술] != 2) return -29;
        if (åtgärd_rot < 0 || åtgärd_rot > 2) return -22;
        int Bakgrund_värde = åtgärd_rot == 0 ? 0 : (åtgärd_rot == 1 ? fil_placera[기술] : Minne_filsystem.storlek_ange[mål[기술]]);
        if (FÖRSKJUTNING_värde > 0 && Bakgrund_värde > 2147483647 - FÖRSKJUTNING_värde) return -75;
        if (FÖRSKJUTNING_värde < 0 && FÖRSKJUTNING_värde < -Bakgrund_värde) return -22;
        fil_placera[기술] = Bakgrund_värde + FÖRSKJUTNING_värde;
        return fil_placera[기술];
    }
    static int 서술자복제(int 서술자, int 새서술자, boolean Tilldela_värde, int Inställningar) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (새서술자 < 0 || 새서술자 >= 서술자한도) return Tilldela_värde ? -9 : -22;
        if (Tilldela_värde && 서술자 == 새서술자) return 새서술자;
        if (Tilldela_värde) { if (skapa_handtag[새서술자] != 0) Stäng_fil(새서술자); }
        else { 새서술자 = 빈서술자(새서술자); if (새서술자 < 0) return 새서술자; }
        skapa_handtag[새서술자] = 기술 + 1; 서술자설정[새서술자] = Inställningar; referens_ANTAL[기술]++;
        return 새서술자;
    }
    static int ta_bort_fil_post_namn(int namn_ADRESS) {
        int längd_värde = läsa_väg(namn_ADRESS);
        if (längd_värde < 0) return längd_värde;
        int filnamn = Minne_filsystem.Sök_post(väg_namn, längd_värde);
        if (filnamn < 0) return filnamn;
        Minne_filsystem.이름들[filnamn * 64] = 0;
        return 0;
    }
    static int uppsättning_fil_längd(int 서술자, int längd_värde) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (variant_värde[기술] != 2 || (skapa_Inställningar[기술] & 3) == 0 || längd_värde < 0) return -22;
        if (längd_värde > Minne_filsystem.최대크기) return -27;
        int filnamn = mål[기술], Adress = enhet_värde.fil_Minne() + filnamn * Minne_filsystem.최대크기;
        for (int INDEX = Minne_filsystem.storlek_ange[filnamn]; INDEX < längd_värde; INDEX++) enhet_värde.skriva_Minne(Adress + INDEX, 0);
        Minne_filsystem.storlek_ange[filnamn] = längd_värde;
        return 0;
    }
    static int läsa_fil_status(int 서술자, int Adress) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (!körning_Ansvarig.klipp(Adress, 48)) return -14;
        for (int INDEX = 0; INDEX < 12; INDEX++) körning_Ansvarig.skriva_nummer(Adress + INDEX * 4, 0);
        int filnamn = mål[기술], Storlek = variant_värde[기술] == 2 ? Minne_filsystem.storlek_ange[filnamn] : 0;
        int beviljande_behörighet = variant_värde[기술] == 2 ? Minne_filsystem.허가들[filnamn] : 438;
        körning_Ansvarig.skriva_nummer(Adress, 1);
        körning_Ansvarig.skriva_nummer(Adress + 4, variant_värde[기술] == 2 ? filnamn + 1 : 100 + 기술);
        körning_Ansvarig.skriva_nummer(Adress + 8, (variant_värde[기술] == 2 ? 32768 : (variant_värde[기술] == 1 ? 8192 : 49152)) | beviljande_behörighet);
        körning_Ansvarig.skriva_nummer(Adress + 12, variant_värde[기술] == 2 && Minne_filsystem.이름들[filnamn * 64] == 0 ? 0 : 1);
        körning_Ansvarig.skriva_nummer(Adress + 28, Storlek); körning_Ansvarig.skriva_nummer(Adress + 32, 512);
        körning_Ansvarig.skriva_nummer(Adress + 36, (Storlek + 511) / 512);
        return 0;
    }
    static int 서술자제어(int 서술자, int kommando, int värde) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (kommando == 0 || kommando == 1030) return 서술자복제(서술자, värde, false, kommando == 1030 ? 1 : 0);
        if (kommando == 1) return 서술자설정[서술자];
        if (kommando == 2) { if ((värde & ~1) != 0) return -22; 서술자설정[서술자] = värde; return 0; }
        if (kommando == 3) return skapa_Inställningar[기술];
        if (kommando == 4) {
            if ((värde & ~(3 | 이어쓰기 | 기다리지않기)) != 0) return -95;
            skapa_Inställningar[기술] = (skapa_Inställningar[기술] & 3) | (värde & (이어쓰기 | 기다리지않기)); return 0;
        }
        return -95;
    }
    static int Skapa_deltagare(int 주소체계, int nätverk_variant, int jobb_nummer) {
        if (주소체계 != 2) return -97;
        if (nätverk_variant != 2) return -93;
        if (jobb_nummer != 0 && jobb_nummer != 17) return -93;
        int 서술자 = 빈서술자(0), 기술 = 빈기술();
        if (서술자 < 0 || 기술 < 0) return -24;
        return Anslut(서술자, 기술, 3, 0, läsa_skriva_flagga);
    }
    static int 종단점기술(int 서술자) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        return variant_värde[기술] == 3 ? 기술 : -88;
    }
    static int ADRESS_32(int Adress) {
        return enhet_värde.läsa_Minne(Adress) << 24 | enhet_värde.läsa_Minne(Adress + 1) << 16
            | enhet_värde.läsa_Minne(Adress + 2) << 8 | enhet_värde.läsa_Minne(Adress + 3);
    }
    static int check_ADRESS(int Adress, int längd_värde) {
        if (längd_värde < 16) return -22;
        if (!körning_Ansvarig.klipp(Adress, 16)) return -14;
        return körning_Ansvarig.짧은수(Adress) == 2 ? 0 : -97;
    }
    static int BIND_ADRESS(int 서술자, int Adress, int längd_värde) {
        int 기술 = 종단점기술(서술자);
        if (기술 < 0) return 기술;
        int RESULTAT = check_ADRESS(Adress, längd_värde);
        if (RESULTAT < 0) return RESULTAT;
        if (nätverk_handtag[기술] != 0) return -22;
        int Nätverks_ID = ADRESS_32(Adress + 4);
        if (Nätverks_ID != 0 && Nätverks_ID != nätverk_Stack.내주소) return -99;
        int portnummer = enhet_värde.läsa_Minne(Adress + 2) << 8 | enhet_värde.läsa_Minne(Adress + 3);
        RESULTAT = nätverk_Stack.Öppna(portnummer);
        if (RESULTAT < 0) return RESULTAT;
        nätverk_handtag[기술] = RESULTAT; mål[기술] = Nätverks_ID;
        return 0;
    }
    static int Auto_BIND(int 기술) {
        if (nätverk_handtag[기술] != 0) return 0;
        int RESULTAT = nätverk_Stack.Öppna(0);
        if (RESULTAT < 0) return RESULTAT;
        nätverk_handtag[기술] = RESULTAT;
        return 0;
    }
    // sendto/recvfrom의 마지막 두 인자는 8바이트 begäran 구조체로 전달한다.
    static int skicka_datagram_data(int 서술자, int data_ADRESS, int längd_värde, int Inställningar, int begärd_ADRESS) {
        int 기술 = 종단점기술(서술자);
        if (기술 < 0) return 기술;
        if (Inställningar != 0) return -95;
        if (längd_värde < 0 || längd_värde > 1024) return -90;
        if (längd_värde != 0 && !körning_Ansvarig.klipp(data_ADRESS, längd_värde)) return -14;
        if (!körning_Ansvarig.klipp(begärd_ADRESS, 8)) return -14;
        int Adress = körning_Ansvarig.nummer(begärd_ADRESS);
        int RESULTAT = check_ADRESS(Adress, körning_Ansvarig.nummer(begärd_ADRESS + 4));
        if (RESULTAT < 0) return RESULTAT;
        int portnummer = enhet_värde.läsa_Minne(Adress + 2) << 8 | enhet_värde.läsa_Minne(Adress + 3);
        if (portnummer == 0) return -22;
        RESULTAT = Auto_BIND(기술);
        if (RESULTAT < 0) return RESULTAT;
        for (int INDEX = 0; INDEX < längd_värde; INDEX++) Överför_data[INDEX] = enhet_värde.läsa_Minne(data_ADRESS + INDEX);
        return nätverk_Stack.skicka(nätverk_handtag[기술], ADRESS_32(Adress + 4), portnummer, Överför_data, längd_värde);
    }
    static void skriva_ADRESS(int Adress, int längd_värde, int Nätverks_ID, int portnummer) {
        for (int INDEX = 0; INDEX < längd_värde && INDEX < 16; INDEX++) {
            int värde = 0;
            if (INDEX == 0) värde = 2;
            if (INDEX == 2) värde = portnummer >>> 8;
            if (INDEX == 3) värde = portnummer;
            if (INDEX >= 4 && INDEX < 8) värde = Nätverks_ID >>> (56 - INDEX * 8);
            enhet_värde.skriva_Minne(Adress + INDEX, värde & 255);
        }
    }
    static int få_datagram_data(int 서술자, int data_ADRESS, int längd_värde, int Inställningar, int begärd_ADRESS) {
        int 기술 = 종단점기술(서술자);
        if (기술 < 0) return 기술;
        if ((Inställningar & ~64) != 0) return -95;
        if (längd_värde < 0) return -22;
        if (längd_värde != 0 && !körning_Ansvarig.klipp(data_ADRESS, längd_värde)) return -14;
        int Adress = 0, ADRESS_längd_ADRESS = 0, ADRESS_längd = 0;
        if (begärd_ADRESS != 0) {
            if (!körning_Ansvarig.klipp(begärd_ADRESS, 8)) return -14;
            Adress = körning_Ansvarig.nummer(begärd_ADRESS); ADRESS_längd_ADRESS = körning_Ansvarig.nummer(begärd_ADRESS + 4);
            if (Adress != 0) {
                if (!körning_Ansvarig.klipp(ADRESS_längd_ADRESS, 4)) return -14;
                ADRESS_längd = körning_Ansvarig.nummer(ADRESS_längd_ADRESS);
                if (ADRESS_längd < 0) return -22;
                if (!körning_Ansvarig.klipp(Adress, ADRESS_längd < 16 ? ADRESS_längd : 16)) return -14;
            }
        }
        int RESULTAT = Auto_BIND(기술);
        if (RESULTAT < 0) return RESULTAT;
        int Kör = enhet_värde.밀리초();
        while (true) {
            RESULTAT = nätverk_Stack.få(nätverk_handtag[기술], Överför_data, 1024, 0);
            if (RESULTAT != -11) break;
            if ((Inställningar & 64) != 0 || (skapa_Inställningar[기술] & 기다리지않기) != 0) return -11;
            if (수신대기밀리초[기술] > 0 && enhet_värde.밀리초() - Kör >= 수신대기밀리초[기술]) return -11;
            if (enhet_värde.사용자남은밀리초() <= 10) return -11;
            enhet_värde.잠시양보();
        }
        if (RESULTAT < 0) return RESULTAT;
        if (RESULTAT > längd_värde) RESULTAT = längd_värde;
        for (int INDEX = 0; INDEX < RESULTAT; INDEX++) enhet_värde.skriva_Minne(data_ADRESS + INDEX, Överför_data[INDEX]);
        if (Adress != 0) {
            skriva_ADRESS(Adress, ADRESS_längd, nätverk_Stack.peer_ADRESS(nätverk_handtag[기술]), nätverk_Stack.peer_portnummer(nätverk_handtag[기술]));
            körning_Ansvarig.skriva_nummer(ADRESS_längd_ADRESS, 16);
        }
        return RESULTAT;
    }
    static int läsa_socket_ADRESS(int 서술자, int Adress, int längd_ADRESS) {
        int 기술 = 종단점기술(서술자);
        if (기술 < 0) return 기술;
        if (!körning_Ansvarig.klipp(längd_ADRESS, 4)) return -14;
        int längd_värde = körning_Ansvarig.nummer(längd_ADRESS);
        if (längd_värde < 0) return -22;
        if (!körning_Ansvarig.klipp(Adress, längd_värde < 16 ? längd_värde : 16)) return -14;
        int fack_post = nätverk_Stack.INDEX(nätverk_handtag[기술]);
        skriva_ADRESS(Adress, längd_värde, mål[기술], fack_post < 0 ? 0 : nätverk_Stack.접속번호들[fack_post]);
        körning_Ansvarig.skriva_nummer(längd_ADRESS, 16);
        return 0;
    }
    static int uppsättning_få_TIMEOUT(int 서술자, int 밀리초) {
        int 기술 = 종단점기술(서술자);
        if (기술 < 0) return 기술;
        if (밀리초 < 0 || 밀리초 > 2000) return -22;
        수신대기밀리초[기술] = 밀리초;
        return 0;
    }
}
