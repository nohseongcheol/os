// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** UTF-8 bayiti_agaciro 경계를 지키는 삽입/삭제, 방향키, Icyo_wifuza kubika_umurongo, Tab 완성. */
public final class umurongo_Muhindura {
    static boolean interuro_y_ibwiriza;
    static int[] kubika_umurongo = new int[16 * 1024], kubika_uburebure = new int[16], Store_agaciro = new int[4096], 후보 = new int[64];
    static int 기록수, kubika_umurongo_kurangiza, Gushaka_agaciro, 저장길이, Ingano, inyoboranyandika_agaciro, 후보수, 후보길이, Itangira_idirishya;
    static boolean 가로보기;
    static String 명령들 = "help info pwd cd ls mkdir rmdir touch cp mv rm cat edit load hex echo clear wc grep head tail tee env export unset history sh source true false exit terminal gui vi javac java python pip jaot cc tcc ftpd sshd vncd gitekanye_insomamabwiriza kure_kwerekana run samples example tasks selftest ipconfig ip ifconfig ping route netstat ss ps top free df uptime poweroff";
    static int[] 명령후보 = new int[128];
    static void 명령후보넣기(String icyinjizwa_Urutonde, int 시작자리, int 끝자리, int 입력길이) {
        int 바이트수=0;
        for(int 자리=시작자리;자리<끝자리;자리++) {
            int 문자값=icyinjizwa_Urutonde.charAt(자리);
            if(문자값>=0xd800 && 문자값<=0xdbff && 자리+1<끝자리)문자값=0x10000+((문자값-0xd800)<<10)+icyinjizwa_Urutonde.charAt(++자리)-0xdc00;
            int 수=문자값<128?1:문자값<2048?2:문자값<65536?3:4;
            if(바이트수+수>62)return;
            for(int URUKURIKIRANE_agaciro=수-1;URUKURIKIRANE_agaciro>=0;URUKURIKIRANE_agaciro--)명령후보[바이트수++]=수==1?문자값:URUKURIKIRANE_agaciro==수-1?(수==2?0xc0:수==3?0xe0:0xf0)|(문자값>>(6*URUKURIKIRANE_agaciro)):0x80|((문자값>>(6*URUKURIKIRANE_agaciro))&63);
        }
        if(바이트수<입력길이)return;
        for(int 자리=0;자리<입력길이;자리++)if(명령후보[자리]!=명령해석기.umurongo[자리])return;
        후보수++;후보길이=바이트수+1;
        for(int 자리=0;자리<바이트수;자리++)후보[자리]=명령후보[자리];후보[바이트수]=' ';
    }
    static int 앞(int 읽는자리) { if (읽는자리 > 0) { 읽는자리--; while (읽는자리 > 0 && (명령해석기.umurongo[읽는자리] & 192) == 128) 읽는자리--; } return 읽는자리; }
    static int Ikibanza_agaciro(int 읽는자리) { if (읽는자리 < Ingano) { 읽는자리++; while (읽는자리 < Ingano && (명령해석기.umurongo[읽는자리] & 192) == 128) 읽는자리++; } return 읽는자리; }
    static int 폭(int 시작자리, int aho_ijya_agaciro_umugerekashakiro) {
        int 글칸수 = 0;
        for (int gukora_mu_matsinda_umugerekashakiro = 시작자리; gukora_mu_matsinda_umugerekashakiro < aho_ijya_agaciro_umugerekashakiro; gukora_mu_matsinda_umugerekashakiro++) { int bayiti_amakurushingiro = 명령해석기.umurongo[gukora_mu_matsinda_umugerekashakiro]; if ((bayiti_amakurushingiro & 192) == 128) continue; 글칸수 += bayiti_amakurushingiro >= 196 ? 2 : 1; }
        return 글칸수;
    }
    static void 다시() {
        단말.kwandika("\r\u001b[2K");
        단말.kwandika(interuro_y_ibwiriza ? "jkoros-native> " : "edit> ");
        보이는줄();
    }
    // 한 물리 umurongo 안에서 좌우로 이동한다. 긴 명령의 재표시가 위쪽 출력을 지우지 않는다.
    static int 보이는폭() { int 열수 = 보드.터미널(13) & 65535; return 열수 - (interuro_y_ibwiriza ? 18 : 9); }
    static void 보이는줄() {
        if (inyoboranyandika_agaciro < Itangira_idirishya) Itangira_idirishya = inyoboranyandika_agaciro;
        while (폭(Itangira_idirishya, inyoboranyandika_agaciro) > 보이는폭()) Itangira_idirishya = Ikibanza_agaciro(Itangira_idirishya);
        int 끝자리 = Itangira_idirishya;
        while (끝자리 < Ingano && 폭(Itangira_idirishya, Ikibanza_agaciro(끝자리)) <= 보이는폭()) 끝자리 = Ikibanza_agaciro(끝자리);
        단말.kwandika("\r\u001b["); 단말.수(interuro_y_ibwiriza ? 16 : 7); 단말.kwandika("G\u001b[K");
        if (Itangira_idirishya > 0) 단말.문자('<');
        for (int gukora_mu_matsinda_umugerekashakiro = Itangira_idirishya; gukora_mu_matsinda_umugerekashakiro < 끝자리; gukora_mu_matsinda_umugerekashakiro++) 보드.직렬쓰기(명령해석기.umurongo[gukora_mu_matsinda_umugerekashakiro]);
        단말.문자(끝자리 < Ingano ? '>' : ' ');
        단말.kwandika("\u001b["); 단말.수(폭(inyoboranyandika_agaciro, 끝자리) + 1); 단말.문자('D');
        가로보기 = Itangira_idirishya > 0 || 끝자리 < Ingano || 폭(0, Ingano) > 보이는폭();
    }
    static void 기록넣기() {
        if (!interuro_y_ibwiriza || Ingano == 0 || Ingano > 1024) return;
        if (기록수 > 0) {
            int 마지막자리 = (kubika_umurongo_kurangiza + 15) % 16; boolean 같은여부 = kubika_uburebure[마지막자리] == Ingano;
            for (int gukora_mu_matsinda_umugerekashakiro = 0; 같은여부 && gukora_mu_matsinda_umugerekashakiro < Ingano; gukora_mu_matsinda_umugerekashakiro++) if (kubika_umurongo[마지막자리 * 1024 + gukora_mu_matsinda_umugerekashakiro] != 명령해석기.umurongo[gukora_mu_matsinda_umugerekashakiro]) 같은여부 = false;
            if (같은여부) return;
        }
        kubika_uburebure[kubika_umurongo_kurangiza] = Ingano; for (int gukora_mu_matsinda_umugerekashakiro = 0; gukora_mu_matsinda_umugerekashakiro < Ingano; gukora_mu_matsinda_umugerekashakiro++) kubika_umurongo[kubika_umurongo_kurangiza * 1024 + gukora_mu_matsinda_umugerekashakiro] = 명령해석기.umurongo[gukora_mu_matsinda_umugerekashakiro];
        kubika_umurongo_kurangiza = (kubika_umurongo_kurangiza + 1) % 16; if (기록수 < 16) 기록수++;
    }
    static void 기록이동(int 변화량) {
        if (!interuro_y_ibwiriza) return;
        if (Gushaka_agaciro == 0 && 변화량 > 0) { 저장길이 = Ingano; for (int gukora_mu_matsinda_umugerekashakiro = 0; gukora_mu_matsinda_umugerekashakiro < Ingano; gukora_mu_matsinda_umugerekashakiro++) Store_agaciro[gukora_mu_matsinda_umugerekashakiro] = 명령해석기.umurongo[gukora_mu_matsinda_umugerekashakiro]; }
        int 다음자리 = Gushaka_agaciro + 변화량; if (다음자리 < 0 || 다음자리 > 기록수) return; Gushaka_agaciro = 다음자리;
        if (Gushaka_agaciro == 0) { Ingano = 저장길이; for (int gukora_mu_matsinda_umugerekashakiro = 0; gukora_mu_matsinda_umugerekashakiro < Ingano; gukora_mu_matsinda_umugerekashakiro++) 명령해석기.umurongo[gukora_mu_matsinda_umugerekashakiro] = Store_agaciro[gukora_mu_matsinda_umugerekashakiro]; }
        else { int 보관칸 = (kubika_umurongo_kurangiza + 16 - Gushaka_agaciro) % 16; Ingano = kubika_uburebure[보관칸]; for (int gukora_mu_matsinda_umugerekashakiro = 0; gukora_mu_matsinda_umugerekashakiro < Ingano; gukora_mu_matsinda_umugerekashakiro++) 명령해석기.umurongo[gukora_mu_matsinda_umugerekashakiro] = kubika_umurongo[보관칸 * 1024 + gukora_mu_matsinda_umugerekashakiro]; }
        inyoboranyandika_agaciro = Ingano; 다시();
    }
    static void kugaragaza_kubika() {
        for (int 항목수 = 0; 항목수 < 기록수; 항목수++) {
            int 보관칸 = (kubika_umurongo_kurangiza + 16 - 기록수 + 항목수) % 16; 단말.수(항목수 + 1); 단말.kwandika("  ");
            for (int gukora_mu_matsinda_umugerekashakiro = 0; gukora_mu_matsinda_umugerekashakiro < kubika_uburebure[보관칸]; gukora_mu_matsinda_umugerekashakiro++) 보드.직렬쓰기(kubika_umurongo[보관칸 * 1024 + gukora_mu_matsinda_umugerekashakiro]); 단말.문자(10);
        }
    }
    static void 후보넣기(int[] amakurushingiro_ARRAY, int 시작자리, int 항목수, int 접두말, int 총수, boolean 폴더번호) {
        if (항목수 < 총수 || 항목수 > 62) return;
        for (int gukora_mu_matsinda_umugerekashakiro = 0; gukora_mu_matsinda_umugerekashakiro < 총수; gukora_mu_matsinda_umugerekashakiro++) if (amakurushingiro_ARRAY[시작자리 + gukora_mu_matsinda_umugerekashakiro] != 명령해석기.umurongo[접두말 + gukora_mu_matsinda_umugerekashakiro]) return;
        후보수++; 후보길이 = 항목수 + 1;
        for (int gukora_mu_matsinda_umugerekashakiro = 0; gukora_mu_matsinda_umugerekashakiro < 항목수; gukora_mu_matsinda_umugerekashakiro++) 후보[gukora_mu_matsinda_umugerekashakiro] = amakurushingiro_ARRAY[시작자리 + gukora_mu_matsinda_umugerekashakiro]; 후보[항목수] = 폴더번호 ? '/' : ' ';
    }
    static void 완성() {
        if (!interuro_y_ibwiriza || inyoboranyandika_agaciro != Ingano) return;
        int 시작점 = Ingano; while (시작점 > 0 && 명령해석기.umurongo[시작점 - 1] != ' ') 시작점--;
        for (int gukora_mu_matsinda_umugerekashakiro = 시작점; gukora_mu_matsinda_umugerekashakiro < Ingano; gukora_mu_matsinda_umugerekashakiro++) if (명령해석기.umurongo[gukora_mu_matsinda_umugerekashakiro] == '/' || 명령해석기.umurongo[gukora_mu_matsinda_umugerekashakiro] == '"' || 명령해석기.umurongo[gukora_mu_matsinda_umugerekashakiro] == 39 || 명령해석기.umurongo[gukora_mu_matsinda_umugerekashakiro] == '\\') return;
        후보수 = 0; int 항목수 = Ingano - 시작점;
        if (시작점 == 0) {
            for(int Urutonde_umugerekashakiro=0;Urutonde_umugerekashakiro<2;Urutonde_umugerekashakiro++) {
                String icyinjizwa_Urutonde=Urutonde_umugerekashakiro==0?명령들:관리명령.완성어();
                int 읽는자리=0;
                while(읽는자리<icyinjizwa_Urutonde.length()) {
                    int 끝자리=읽는자리;while(끝자리<icyinjizwa_Urutonde.length() && icyinjizwa_Urutonde.charAt(끝자리)!=' ')끝자리++;
                    명령후보넣기(icyinjizwa_Urutonde,읽는자리,끝자리,항목수);읽는자리=끝자리+1;
                }
            }
        } else {
            ububiko_Dosiye.inzira_Itangira(1); ububiko_Dosiye.inzira_bayiti(0, '.'); ububiko_Dosiye.kuboneza_agaciro();
            for (int gukora_mu_matsinda_umugerekashakiro = 0; gukora_mu_matsinda_umugerekashakiro < ububiko_Dosiye.파일수; gukora_mu_matsinda_umugerekashakiro++) {
                int 시작자리 = ububiko_Dosiye.icyinjizwa_Itangira(ububiko_Dosiye.Izina, gukora_mu_matsinda_umugerekashakiro * 64, ububiko_Dosiye.이름길이[gukora_mu_matsinda_umugerekashakiro]);
                if (시작자리 >= 0) 후보넣기(ububiko_Dosiye.Izina, gukora_mu_matsinda_umugerekashakiro * 64 + 시작자리, ububiko_Dosiye.이름길이[gukora_mu_matsinda_umugerekashakiro] - 시작자리, 시작점, 항목수, false);
            }
            for (int gukora_mu_matsinda_umugerekashakiro = 0; gukora_mu_matsinda_umugerekashakiro < 16; gukora_mu_matsinda_umugerekashakiro++) {
                int 시작자리 = ububiko_Dosiye.icyinjizwa_Itangira(ububiko_Dosiye.ububiko_izina, gukora_mu_matsinda_umugerekashakiro * 64, ububiko_Dosiye.ububiko_uburebure[gukora_mu_matsinda_umugerekashakiro]);
                if (시작자리 >= 0) 후보넣기(ububiko_Dosiye.ububiko_izina, gukora_mu_matsinda_umugerekashakiro * 64 + 시작자리, ububiko_Dosiye.ububiko_uburebure[gukora_mu_matsinda_umugerekashakiro] - 시작자리, 시작점, 항목수, true);
            }
        }
        if (후보수 != 1) { 보드.직렬쓰기(7); return; }
        for (int gukora_mu_matsinda_umugerekashakiro = 항목수; gukora_mu_matsinda_umugerekashakiro < 후보길이 && Ingano < 명령해석기.umurongo.length - 1; gukora_mu_matsinda_umugerekashakiro++) {
            if (후보[gukora_mu_matsinda_umugerekashakiro] == ' ' && gukora_mu_matsinda_umugerekashakiro != 후보길이 - 1) 명령해석기.umurongo[Ingano++] = '\\';
            명령해석기.umurongo[Ingano++] = 후보[gukora_mu_matsinda_umugerekashakiro];
        }
        inyoboranyandika_agaciro = Ingano; 다시();
    }
    static int 탈출읽기() {
        int 시작점 = 보드.밀리초();
        while (보드.밀리초() - 시작점 < 80) { int bayiti_amakurushingiro = 보드.직렬읽기(); if (bayiti_amakurushingiro >= 0) return bayiti_amakurushingiro; 보드.gusubika_CPU(); }
        return -1;
    }
    static void 탈출() {
        int 첫자리 = 탈출읽기(); if (첫자리 != '[' && 첫자리 != 'O') return;
        int 항목수 = 0, 끝자리 = -1;
        for (int gukora_mu_matsinda_umugerekashakiro = 0; gukora_mu_matsinda_umugerekashakiro < 12; gukora_mu_matsinda_umugerekashakiro++) { int bayiti_amakurushingiro = 탈출읽기(); if (bayiti_amakurushingiro < 0) return; if (bayiti_amakurushingiro >= '0' && bayiti_amakurushingiro <= '9') 항목수 = 항목수 * 10 + bayiti_amakurushingiro - '0'; else { 끝자리 = bayiti_amakurushingiro; break; } }
        if (끝자리 == 'A') 기록이동(1);
        else if (끝자리 == 'B') 기록이동(-1);
        else if (끝자리 == 'C') { inyoboranyandika_agaciro = Ikibanza_agaciro(inyoboranyandika_agaciro); 다시(); }
        else if (끝자리 == 'D') { inyoboranyandika_agaciro = 앞(inyoboranyandika_agaciro); 다시(); }
        else if (끝자리 == 'H' || 끝자리 == '~' && (항목수 == 1 || 항목수 == 7)) { inyoboranyandika_agaciro = 0; 다시(); }
        else if (끝자리 == 'F' || 끝자리 == '~' && (항목수 == 4 || 항목수 == 8)) { inyoboranyandika_agaciro = Ingano; 다시(); }
        else if (끝자리 == '~' && 항목수 == 3 && inyoboranyandika_agaciro < Ingano) {
            int 다음자리 = Ikibanza_agaciro(inyoboranyandika_agaciro); for (int gukora_mu_matsinda_umugerekashakiro = 다음자리; gukora_mu_matsinda_umugerekashakiro < Ingano; gukora_mu_matsinda_umugerekashakiro++) 명령해석기.umurongo[gukora_mu_matsinda_umugerekashakiro - 다음자리 + inyoboranyandika_agaciro] = 명령해석기.umurongo[gukora_mu_matsinda_umugerekashakiro]; Ingano -= 다음자리 - inyoboranyandika_agaciro; 다시();
        }
        else if (끝자리 == '~' && (항목수 == 5 || 항목수 == 6)) 보드.터미널(항목수 == 5 ? 5 : 6);
        else if (끝자리 == '~' && 항목수 == 24 && interuro_y_ibwiriza) { 명령해석기.터미널(true); }
    }
    static int 읽기() {
        if (!idirishya_kwihuza.이어읽기) { Ingano = inyoboranyandika_agaciro = Gushaka_agaciro = Itangira_idirishya = 0; 가로보기 = false; }
        else { idirishya_kwihuza.이어읽기 = false; 다시(); } boolean umusago = false;
        while (true) {
            int bayiti_amakurushingiro = 보드.직렬읽기(); if (bayiti_amakurushingiro == -4096) return -3;
            if (보드.터미널(14) != 0) 다시(); if (bayiti_amakurushingiro < 0) { 보드.gusubika_CPU(); continue; }
            if (bayiti_amakurushingiro == 10 && 명령해석기.앞줄) { 명령해석기.앞줄 = false; continue; } 명령해석기.앞줄 = bayiti_amakurushingiro == 13;
            if (bayiti_amakurushingiro == 27) { 탈출(); continue; }
            if (bayiti_amakurushingiro == 3) { 단말.kwandika("^C\n"); return -1; }
            if (bayiti_amakurushingiro == 4 && Ingano == 0 && interuro_y_ibwiriza) { if (보드.터미널(2) != 0) 명령해석기.터미널(true); return -1; }
            if (bayiti_amakurushingiro == 13 || bayiti_amakurushingiro == 10) { 단말.문자(10); if (!umusago) 기록넣기(); return umusago ? -2 : Ingano; }
            if (bayiti_amakurushingiro == 9 && interuro_y_ibwiriza) { 완성(); continue; }
            if (bayiti_amakurushingiro == 1 || bayiti_amakurushingiro == 5) { inyoboranyandika_agaciro = bayiti_amakurushingiro == 1 ? 0 : Ingano; 다시(); continue; }
            if (bayiti_amakurushingiro == 8 || bayiti_amakurushingiro == 127 || bayiti_amakurushingiro == 21) {
                if (bayiti_amakurushingiro == 21) { for (int gukora_mu_matsinda_umugerekashakiro = inyoboranyandika_agaciro; gukora_mu_matsinda_umugerekashakiro < Ingano; gukora_mu_matsinda_umugerekashakiro++) 명령해석기.umurongo[gukora_mu_matsinda_umugerekashakiro - inyoboranyandika_agaciro] = 명령해석기.umurongo[gukora_mu_matsinda_umugerekashakiro]; Ingano -= inyoboranyandika_agaciro; inyoboranyandika_agaciro = 0; }
                else if (inyoboranyandika_agaciro > 0) { int 변경전 = 앞(inyoboranyandika_agaciro); for (int gukora_mu_matsinda_umugerekashakiro = inyoboranyandika_agaciro; gukora_mu_matsinda_umugerekashakiro < Ingano; gukora_mu_matsinda_umugerekashakiro++) 명령해석기.umurongo[gukora_mu_matsinda_umugerekashakiro - inyoboranyandika_agaciro + 변경전] = 명령해석기.umurongo[gukora_mu_matsinda_umugerekashakiro]; Ingano -= inyoboranyandika_agaciro - 변경전; inyoboranyandika_agaciro = 변경전; }
                다시(); continue;
            }
            if (bayiti_amakurushingiro == 11) { Ingano = inyoboranyandika_agaciro; 다시(); continue; }
            if (bayiti_amakurushingiro < 32 && bayiti_amakurushingiro != 9) continue;
            if (Ingano == 명령해석기.umurongo.length) { umusago = true; continue; }
            for (int gukora_mu_matsinda_umugerekashakiro = Ingano; gukora_mu_matsinda_umugerekashakiro > inyoboranyandika_agaciro; gukora_mu_matsinda_umugerekashakiro--) 명령해석기.umurongo[gukora_mu_matsinda_umugerekashakiro] = 명령해석기.umurongo[gukora_mu_matsinda_umugerekashakiro - 1];
            명령해석기.umurongo[inyoboranyandika_agaciro++] = bayiti_amakurushingiro; Ingano++;
            if (inyoboranyandika_agaciro == Ingano && !가로보기 && 폭(0, Ingano) <= 보이는폭()) 보드.직렬쓰기(bayiti_amakurushingiro);
            else if (inyoboranyandika_agaciro == Ingano) 보이는줄(); else 다시();
        }
    }
}
