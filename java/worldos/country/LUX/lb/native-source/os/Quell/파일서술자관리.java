// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 단일 Benotzer 과정의 파일서술자와 열린 Fichier 기술을 분리한다. 호출 번호는 POSIX ABI 문서에 기록한다. */
public final class 파일서술자관리 {
    static final int 서술자한도 = 32;
    static final int lies_schreiffäeg_kennzeechnen = 2, Create_Agab = 64, 독점생성 = 128, läschen_Inhalt = 512;
    static final int 이어쓰기 = 1024, 기다리지않기 = 2048, 실행시닫기 = 524288;
    static int[] ariichten_Handle = new int[서술자한도], 서술자설정 = new int[서술자한도];
    static int[] 종류 = new int[서술자한도], Zil = new int[서술자한도];
    static int[] Fichier_positionéieren = new int[서술자한도], ariichten_Astellungen = new int[서술자한도], Referenzen_COUNT = new int[서술자한도];
    static int[] Reseau_Handle = new int[서술자한도], 수신대기밀리초 = new int[서술자한도];
    static int[] Wee_Numm = new int[64], Transfer_Daten = new int[1024];

    static int 기술찾기(int 파일서술자) {
        if (파일서술자 < 0 || 파일서술자 >= 서술자한도) return -9;
        return ariichten_Handle[파일서술자] - 1;
    }
    static int 빈서술자(int Laf) {
        for (int INDEX = Laf; INDEX < 서술자한도; INDEX++) if (ariichten_Handle[INDEX] == 0) return INDEX;
        return -24;
    }
    static int eidel_Handle() {
        for (int INDEX = 0; INDEX < 서술자한도; INDEX++) if (Referenzen_COUNT[INDEX] == 0) return INDEX;
        return -24;
    }
    static int Verbannen(int 서술자, int 기술, int 파일종류, int Fichier_Zil, int Astellungen) {
        ariichten_Handle[서술자] = 기술 + 1; 서술자설정[서술자] = (Astellungen & 실행시닫기) != 0 ? 1 : 0;
        종류[기술] = 파일종류; Zil[기술] = Fichier_Zil; Referenzen_COUNT[기술] = 1;
        ariichten_Astellungen[기술] = Astellungen & (3 | 이어쓰기 | 기다리지않기); Fichier_positionéieren[기술] = 0;
        Reseau_Handle[기술] = 0; 수신대기밀리초[기술] = 0;
        return 서술자;
    }
    static void Start_Prozess() {
        CLEAN_Prozess();
        for (int INDEX = 0; INDEX < 3; INDEX++) Verbannen(INDEX, INDEX, 1, INDEX, INDEX == 0 ? 0 : 1);
    }
    static void CLEAN_Prozess() {
        for (int INDEX = 0; INDEX < 서술자한도; INDEX++) if (ariichten_Handle[INDEX] != 0) Clôture_Fichier(INDEX);
    }
    static int Clôture_Fichier(int 서술자) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        ariichten_Handle[서술자] = 0; 서술자설정[서술자] = 0;
        Referenzen_COUNT[기술]--;
        if (Referenzen_COUNT[기술] == 0) {
            if (종류[기술] == 2) Späicher_Fichierssystem.ariichten_COUNT[Zil[기술]]--;
            if (종류[기술] == 3 && Reseau_Handle[기술] != 0) Reseau_Stapel.Clôture(Reseau_Handle[기술]);
            종류[기술] = 0;
        }
        return 0;
    }
    // C 경로는 NUL 끝 Byte_VALUE 문자열이다. 루트의 한 이름만 지원한다.
    static int 경로읽기(int Adress) {
        if (!실행관리.Clip(Adress, 1)) return -14;
        int positionéieren = Mobil_VALUE.기억읽기(Adress) == '/' ? 1 : 0;
        for (int Längt_VALUE = 0; Längt_VALUE < 64; Längt_VALUE++) {
            if (!실행관리.Clip(Adress + positionéieren + Längt_VALUE, 1)) return -14;
            int VALUE = Mobil_VALUE.기억읽기(Adress + positionéieren + Längt_VALUE);
            Wee_Numm[Längt_VALUE] = VALUE;
            if (VALUE == 0) return Längt_VALUE == 0 ? -2 : (Späicher_Fichierssystem.Scheck_Numm(Wee_Numm, Längt_VALUE) ? Längt_VALUE : -22);
            if (VALUE == '/') return -20;
        }
        return -36;
    }
    static int ariichten_Fichier(int Numm_Adress, int Astellungen, int 허가) {
        int Längt_VALUE = 경로읽기(Numm_Adress);
        if (Längt_VALUE < 0) return Längt_VALUE;
        if ((Astellungen & ~(3 | Create_Agab | 독점생성 | läschen_Inhalt | 이어쓰기 | 기다리지않기 | 실행시닫기)) != 0) return -95;
        if ((Astellungen & 3) == 3 || ((Astellungen & läschen_Inhalt) != 0 && (Astellungen & 3) == 0)) return -22;
        int Fichier = Späicher_Fichierssystem.FIND_Agab(Wee_Numm, Längt_VALUE);
        if (Fichier >= 0 && (Astellungen & (Create_Agab | 독점생성)) == (Create_Agab | 독점생성)) return -17;
        if (Fichier == -2 && (Astellungen & Create_Agab) == 0) return -2;
        int 서술자 = 빈서술자(0), 기술 = eidel_Handle();
        if (서술자 < 0 || 기술 < 0) return -24;
        if (Fichier == -2) {
            int Mooss = Späicher_Fichierssystem.Store_VALUE(Wee_Numm, Längt_VALUE, Wee_Numm, 0);
            if (Mooss < 0) return Mooss;
            Fichier = Späicher_Fichierssystem.FIND_Agab(Wee_Numm, Längt_VALUE);
            Späicher_Fichierssystem.허가들[Fichier] = 허가 & 511;
        }
        if (Fichier < 0) return Fichier;
        if ((Astellungen & läschen_Inhalt) != 0) Späicher_Fichierssystem.d_Gréisst_veränneren_Lëscht[Fichier] = 0;
        Späicher_Fichierssystem.ariichten_COUNT[Fichier]++;
        return Verbannen(서술자, 기술, 2, Fichier, Astellungen);
    }
    static int 파일읽기(int 서술자, int Daten_Adress, int Längt_VALUE) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0 || (ariichten_Astellungen[기술] & 3) == 1) return -9;
        if (Längt_VALUE < 0) return -22;
        if (Längt_VALUE == 0) return 0;
        if (!실행관리.Clip(Daten_Adress, Längt_VALUE)) return -14;
        if (종류[기술] == 3) return 자료전문받기(서술자, Daten_Adress, Längt_VALUE, 0, 0);
        if (종류[기술] == 1) {
            int RECEIVED_COUNT = 0;
            while (RECEIVED_COUNT < Längt_VALUE) {
                int VALUE = SMS_Terminal.직렬읽기();
                if (VALUE < 0) VALUE = Tastatur.읽기();
                if (VALUE < 0) {
                    if (RECEIVED_COUNT > 0) return RECEIVED_COUNT;
                    if ((ariichten_Astellungen[기술] & 기다리지않기) != 0) return -11;
                    if (Mobil_VALUE.사용자남은밀리초() <= 10) return -11;
                    Reseau_Stapel.verifizéieren(); Mobil_VALUE.잠시양보();
                } else {
                    Mobil_VALUE.schreiwen_Späicher(Daten_Adress + RECEIVED_COUNT, VALUE); RECEIVED_COUNT++;
                }
            }
            return RECEIVED_COUNT;
        }
        int Fichier = Zil[기술], positionéieren = Fichier_positionéieren[기술];
        if (positionéieren >= Späicher_Fichierssystem.d_Gréisst_veränneren_Lëscht[Fichier]) return 0;
        if (Längt_VALUE > Späicher_Fichierssystem.d_Gréisst_veränneren_Lëscht[Fichier] - positionéieren) Längt_VALUE = Späicher_Fichierssystem.d_Gréisst_veränneren_Lëscht[Fichier] - positionéieren;
        int 원본주소 = Mobil_VALUE.Fichier_Späicher() + Fichier * Späicher_Fichierssystem.최대크기 + positionéieren;
        for (int INDEX = 0; INDEX < Längt_VALUE; INDEX++) Mobil_VALUE.schreiwen_Späicher(Daten_Adress + INDEX, Mobil_VALUE.기억읽기(원본주소 + INDEX));
        Fichier_positionéieren[기술] += Längt_VALUE;
        return Längt_VALUE;
    }
    static int schreiwen_Fichier(int 서술자, int Daten_Adress, int Längt_VALUE) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0 || (ariichten_Astellungen[기술] & 3) == 0) return -9;
        if (Längt_VALUE < 0) return -22;
        if (Längt_VALUE == 0) return 0;
        if (!실행관리.Clip(Daten_Adress, Längt_VALUE)) return -14;
        if (종류[기술] == 3) return -89; // 연결하지 않은 자료전문 종단점에는 Zil_VALUE 주소가 필요하다.
        if (종류[기술] == 1) {
            if (Längt_VALUE > 16384) Längt_VALUE = 16384;
            for (int INDEX = 0; INDEX < Längt_VALUE; INDEX++) {
                int VALUE = Mobil_VALUE.기억읽기(Daten_Adress + INDEX);
                SMS_Terminal.직렬바이트(VALUE); SMS_Terminal.화면문자(VALUE);
            }
            return Längt_VALUE;
        }
        int Fichier = Zil[기술], d_Gréisst_veränneren = Späicher_Fichierssystem.d_Gréisst_veränneren_Lëscht[Fichier];
        int positionéieren = (ariichten_Astellungen[기술] & 이어쓰기) != 0 ? d_Gréisst_veränneren : Fichier_positionéieren[기술];
        if (positionéieren >= Späicher_Fichierssystem.최대크기) return -27;
        if (Längt_VALUE > Späicher_Fichierssystem.최대크기 - positionéieren) Längt_VALUE = Späicher_Fichierssystem.최대크기 - positionéieren;
        int Zil_Adress_08bbd577 = Mobil_VALUE.Fichier_Späicher() + Fichier * Späicher_Fichierssystem.최대크기;
        for (int INDEX = d_Gréisst_veränneren; INDEX < positionéieren; INDEX++) Mobil_VALUE.schreiwen_Späicher(Zil_Adress_08bbd577 + INDEX, 0);
        for (int INDEX = 0; INDEX < Längt_VALUE; INDEX++) Mobil_VALUE.schreiwen_Späicher(Zil_Adress_08bbd577 + positionéieren + INDEX, Mobil_VALUE.기억읽기(Daten_Adress + INDEX));
        Fichier_positionéieren[기술] = positionéieren + Längt_VALUE;
        if (positionéieren + Längt_VALUE > d_Gréisst_veränneren) Späicher_Fichierssystem.d_Gréisst_veränneren_Lëscht[Fichier] = positionéieren + Längt_VALUE;
        return Längt_VALUE;
    }
    static int sichen_Fichier(int 서술자, int OFFSET_VALUE, int projezéieren_Racinn) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (종류[기술] != 2) return -29;
        if (projezéieren_Racinn < 0 || projezéieren_Racinn > 2) return -22;
        int Hannergrond_VALUE = projezéieren_Racinn == 0 ? 0 : (projezéieren_Racinn == 1 ? Fichier_positionéieren[기술] : Späicher_Fichierssystem.d_Gréisst_veränneren_Lëscht[Zil[기술]]);
        if (OFFSET_VALUE > 0 && Hannergrond_VALUE > 2147483647 - OFFSET_VALUE) return -75;
        if (OFFSET_VALUE < 0 && OFFSET_VALUE < -Hannergrond_VALUE) return -22;
        Fichier_positionéieren[기술] = Hannergrond_VALUE + OFFSET_VALUE;
        return Fichier_positionéieren[기술];
    }
    static int 서술자복제(int 서술자, int 새서술자, boolean 지정, int Astellungen) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (새서술자 < 0 || 새서술자 >= 서술자한도) return 지정 ? -9 : -22;
        if (지정 && 서술자 == 새서술자) return 새서술자;
        if (지정) { if (ariichten_Handle[새서술자] != 0) Clôture_Fichier(새서술자); }
        else { 새서술자 = 빈서술자(새서술자); if (새서술자 < 0) return 새서술자; }
        ariichten_Handle[새서술자] = 기술 + 1; 서술자설정[새서술자] = Astellungen; Referenzen_COUNT[기술]++;
        return 새서술자;
    }
    static int ewechhuelen_Fichier_Agab_Numm(int Numm_Adress) {
        int Längt_VALUE = 경로읽기(Numm_Adress);
        if (Längt_VALUE < 0) return Längt_VALUE;
        int Fichier = Späicher_Fichierssystem.FIND_Agab(Wee_Numm, Längt_VALUE);
        if (Fichier < 0) return Fichier;
        Späicher_Fichierssystem.이름들[Fichier * 64] = 0;
        return 0;
    }
    static int Saz_Fichier_Längt(int 서술자, int Längt_VALUE) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (종류[기술] != 2 || (ariichten_Astellungen[기술] & 3) == 0 || Längt_VALUE < 0) return -22;
        if (Längt_VALUE > Späicher_Fichierssystem.최대크기) return -27;
        int Fichier = Zil[기술], Adress = Mobil_VALUE.Fichier_Späicher() + Fichier * Späicher_Fichierssystem.최대크기;
        for (int INDEX = Späicher_Fichierssystem.d_Gréisst_veränneren_Lëscht[Fichier]; INDEX < Längt_VALUE; INDEX++) Mobil_VALUE.schreiwen_Späicher(Adress + INDEX, 0);
        Späicher_Fichierssystem.d_Gréisst_veränneren_Lëscht[Fichier] = Längt_VALUE;
        return 0;
    }
    static int 파일상태읽기(int 서술자, int Adress) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (!실행관리.Clip(Adress, 48)) return -14;
        for (int INDEX = 0; INDEX < 12; INDEX++) 실행관리.수쓰기(Adress + INDEX * 4, 0);
        int Fichier = Zil[기술], d_Gréisst_veränneren = 종류[기술] == 2 ? Späicher_Fichierssystem.d_Gréisst_veränneren_Lëscht[Fichier] : 0;
        int 허가 = 종류[기술] == 2 ? Späicher_Fichierssystem.허가들[Fichier] : 438;
        실행관리.수쓰기(Adress, 1);
        실행관리.수쓰기(Adress + 4, 종류[기술] == 2 ? Fichier + 1 : 100 + 기술);
        실행관리.수쓰기(Adress + 8, (종류[기술] == 2 ? 32768 : (종류[기술] == 1 ? 8192 : 49152)) | 허가);
        실행관리.수쓰기(Adress + 12, 종류[기술] == 2 && Späicher_Fichierssystem.이름들[Fichier * 64] == 0 ? 0 : 1);
        실행관리.수쓰기(Adress + 28, d_Gréisst_veränneren); 실행관리.수쓰기(Adress + 32, 512);
        실행관리.수쓰기(Adress + 36, (d_Gréisst_veränneren + 511) / 512);
        return 0;
    }
    static int 서술자제어(int 서술자, int Befeel, int VALUE) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (Befeel == 0 || Befeel == 1030) return 서술자복제(서술자, VALUE, false, Befeel == 1030 ? 1 : 0);
        if (Befeel == 1) return 서술자설정[서술자];
        if (Befeel == 2) { if ((VALUE & ~1) != 0) return -22; 서술자설정[서술자] = VALUE; return 0; }
        if (Befeel == 3) return ariichten_Astellungen[기술];
        if (Befeel == 4) {
            if ((VALUE & ~(3 | 이어쓰기 | 기다리지않기)) != 0) return -95;
            ariichten_Astellungen[기술] = (ariichten_Astellungen[기술] & 3) | (VALUE & (이어쓰기 | 기다리지않기)); return 0;
        }
        return -95;
    }
    static int 통신종단점만들기(int 주소체계, int 통신종류, int 규약번호) {
        if (주소체계 != 2) return -97;
        if (통신종류 != 2) return -93;
        if (규약번호 != 0 && 규약번호 != 17) return -93;
        int 서술자 = 빈서술자(0), 기술 = eidel_Handle();
        if (서술자 < 0 || 기술 < 0) return -24;
        return Verbannen(서술자, 기술, 3, 0, lies_schreiffäeg_kennzeechnen);
    }
    static int 종단점기술(int 서술자) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        return 종류[기술] == 3 ? 기술 : -88;
    }
    static int Adress_32(int Adress) {
        return Mobil_VALUE.기억읽기(Adress) << 24 | Mobil_VALUE.기억읽기(Adress + 1) << 16
            | Mobil_VALUE.기억읽기(Adress + 2) << 8 | Mobil_VALUE.기억읽기(Adress + 3);
    }
    static int Scheck_Adress(int Adress, int Längt_VALUE) {
        if (Längt_VALUE < 16) return -22;
        if (!실행관리.Clip(Adress, 16)) return -14;
        return 실행관리.짧은수(Adress) == 2 ? 0 : -97;
    }
    static int BANNEN_Adress(int 서술자, int Adress, int Längt_VALUE) {
        int 기술 = 종단점기술(서술자);
        if (기술 < 0) return 기술;
        int Mooss = Scheck_Adress(Adress, Längt_VALUE);
        if (Mooss < 0) return Mooss;
        if (Reseau_Handle[기술] != 0) return -22;
        int Reseau_Adress = Adress_32(Adress + 4);
        if (Reseau_Adress != 0 && Reseau_Adress != Reseau_Stapel.내주소) return -99;
        int 접속번호 = Mobil_VALUE.기억읽기(Adress + 2) << 8 | Mobil_VALUE.기억읽기(Adress + 3);
        Mooss = Reseau_Stapel.ariichten(접속번호);
        if (Mooss < 0) return Mooss;
        Reseau_Handle[기술] = Mooss; Zil[기술] = Reseau_Adress;
        return 0;
    }
    static int 자동묶기(int 기술) {
        if (Reseau_Handle[기술] != 0) return 0;
        int Mooss = Reseau_Stapel.ariichten(0);
        if (Mooss < 0) return Mooss;
        Reseau_Handle[기술] = Mooss;
        return 0;
    }
    // sendto/recvfrom의 마지막 두 인자는 8바이트 요청 구조체로 전달한다.
    static int 자료전문보내기(int 서술자, int Daten_Adress, int Längt_VALUE, int Astellungen, int 요청주소) {
        int 기술 = 종단점기술(서술자);
        if (기술 < 0) return 기술;
        if (Astellungen != 0) return -95;
        if (Längt_VALUE < 0 || Längt_VALUE > 1024) return -90;
        if (Längt_VALUE != 0 && !실행관리.Clip(Daten_Adress, Längt_VALUE)) return -14;
        if (!실행관리.Clip(요청주소, 8)) return -14;
        int Adress = 실행관리.수(요청주소);
        int Mooss = Scheck_Adress(Adress, 실행관리.수(요청주소 + 4));
        if (Mooss < 0) return Mooss;
        int 접속번호 = Mobil_VALUE.기억읽기(Adress + 2) << 8 | Mobil_VALUE.기억읽기(Adress + 3);
        if (접속번호 == 0) return -22;
        Mooss = 자동묶기(기술);
        if (Mooss < 0) return Mooss;
        for (int INDEX = 0; INDEX < Längt_VALUE; INDEX++) Transfer_Daten[INDEX] = Mobil_VALUE.기억읽기(Daten_Adress + INDEX);
        return Reseau_Stapel.mailen(Reseau_Handle[기술], Adress_32(Adress + 4), 접속번호, Transfer_Daten, Längt_VALUE);
    }
    static void schreiwen_Adress(int Adress, int Längt_VALUE, int Reseau_Adress, int 접속번호) {
        for (int INDEX = 0; INDEX < Längt_VALUE && INDEX < 16; INDEX++) {
            int VALUE = 0;
            if (INDEX == 0) VALUE = 2;
            if (INDEX == 2) VALUE = 접속번호 >>> 8;
            if (INDEX == 3) VALUE = 접속번호;
            if (INDEX >= 4 && INDEX < 8) VALUE = Reseau_Adress >>> (56 - INDEX * 8);
            Mobil_VALUE.schreiwen_Späicher(Adress + INDEX, VALUE & 255);
        }
    }
    static int 자료전문받기(int 서술자, int Daten_Adress, int Längt_VALUE, int Astellungen, int 요청주소) {
        int 기술 = 종단점기술(서술자);
        if (기술 < 0) return 기술;
        if ((Astellungen & ~64) != 0) return -95;
        if (Längt_VALUE < 0) return -22;
        if (Längt_VALUE != 0 && !실행관리.Clip(Daten_Adress, Längt_VALUE)) return -14;
        int Adress = 0, Adress_Längt_Adress = 0, Adress_Längt = 0;
        if (요청주소 != 0) {
            if (!실행관리.Clip(요청주소, 8)) return -14;
            Adress = 실행관리.수(요청주소); Adress_Längt_Adress = 실행관리.수(요청주소 + 4);
            if (Adress != 0) {
                if (!실행관리.Clip(Adress_Längt_Adress, 4)) return -14;
                Adress_Längt = 실행관리.수(Adress_Längt_Adress);
                if (Adress_Längt < 0) return -22;
                if (!실행관리.Clip(Adress, Adress_Längt < 16 ? Adress_Längt : 16)) return -14;
            }
        }
        int Mooss = 자동묶기(기술);
        if (Mooss < 0) return Mooss;
        int Laf = Mobil_VALUE.밀리초();
        while (true) {
            Mooss = Reseau_Stapel.받기(Reseau_Handle[기술], Transfer_Daten, 1024, 0);
            if (Mooss != -11) break;
            if ((Astellungen & 64) != 0 || (ariichten_Astellungen[기술] & 기다리지않기) != 0) return -11;
            if (수신대기밀리초[기술] > 0 && Mobil_VALUE.밀리초() - Laf >= 수신대기밀리초[기술]) return -11;
            if (Mobil_VALUE.사용자남은밀리초() <= 10) return -11;
            Mobil_VALUE.잠시양보();
        }
        if (Mooss < 0) return Mooss;
        if (Mooss > Längt_VALUE) Mooss = Längt_VALUE;
        for (int INDEX = 0; INDEX < Mooss; INDEX++) Mobil_VALUE.schreiwen_Späicher(Daten_Adress + INDEX, Transfer_Daten[INDEX]);
        if (Adress != 0) {
            schreiwen_Adress(Adress, Adress_Längt, Reseau_Stapel.Peer_Adress(Reseau_Handle[기술]), Reseau_Stapel.상대접속번호(Reseau_Handle[기술]));
            실행관리.수쓰기(Adress_Längt_Adress, 16);
        }
        return Mooss;
    }
    static int 통신주소읽기(int 서술자, int Adress, int Längt_Adress) {
        int 기술 = 종단점기술(서술자);
        if (기술 < 0) return 기술;
        if (!실행관리.Clip(Längt_Adress, 4)) return -14;
        int Längt_VALUE = 실행관리.수(Längt_Adress);
        if (Längt_VALUE < 0) return -22;
        if (!실행관리.Clip(Adress, Längt_VALUE < 16 ? Längt_VALUE : 16)) return -14;
        int Slot_Agab = Reseau_Stapel.INDEX(Reseau_Handle[기술]);
        schreiwen_Adress(Adress, Längt_VALUE, Zil[기술], Slot_Agab < 0 ? 0 : Reseau_Stapel.접속번호들[Slot_Agab]);
        실행관리.수쓰기(Längt_Adress, 16);
        return 0;
    }
    static int 수신대기정하기(int 서술자, int 밀리초) {
        int 기술 = 종단점기술(서술자);
        if (기술 < 0) return 기술;
        if (밀리초 < 0 || 밀리초 > 2000) return -22;
        수신대기밀리초[기술] = 밀리초;
        return 0;
    }
}
