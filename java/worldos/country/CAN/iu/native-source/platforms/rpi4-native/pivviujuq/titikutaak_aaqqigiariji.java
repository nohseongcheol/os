// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** UTF-8 byte_atuutilik 경계를 지키는 삽입/삭제, 방향키, piqujijjut papattivik_sanimukutaak, Tab 완성. */
public final class titikutaak_aaqqigiariji {
    static boolean piqujivik;
    static int[] papattivik_sanimukutaak = new int[16 * 1024], papattivik_takininga = new int[16], tuqqurli_atuutilik = new int[4096], 후보 = new int[64];
    static int 기록수, papattivik_sanimukutaak_isulittuq, Qinirli_atuutilik, 저장길이, anininga, pigiarut_atuutilik, 후보수, 후보길이, pigiarli_igalaangujaq;
    static boolean 가로보기;
    static String 명령들 = "help info pwd cd ls mkdir rmdir touch cp mv rm cat edit load hex echo clear wc grep head tail tee env export unset history sh source true false exit terminal gui vi javac java python pip jaot cc tcc ftpd sshd vncd 보안셸 ungasittuq_saqqijaarli run samples example tasks selftest ipconfig ip ifconfig ping route netstat ss ps top free df uptime poweroff";
    static int[] 명령후보 = new int[128];
    static void 명령후보넣기(String Iliniku_Titiqpalliagaq, int 시작자리, int 끝자리, int 입력길이) {
        int 바이트수=0;
        for(int 자리=시작자리;자리<끝자리;자리++) {
            int immikkuuqtumut_nalunaikkut=Iliniku_Titiqpalliagaq.charAt(자리);
            if(immikkuuqtumut_nalunaikkut>=0xd800 && immikkuuqtumut_nalunaikkut<=0xdbff && 자리+1<끝자리)immikkuuqtumut_nalunaikkut=0x10000+((immikkuuqtumut_nalunaikkut-0xd800)<<10)+Iliniku_Titiqpalliagaq.charAt(++자리)-0xdc00;
            int 수=immikkuuqtumut_nalunaikkut<128?1:immikkuuqtumut_nalunaikkut<2048?2:immikkuuqtumut_nalunaikkut<65536?3:4;
            if(바이트수+수>62)return;
            for(int 차례=수-1;차례>=0;차례--)명령후보[바이트수++]=수==1?immikkuuqtumut_nalunaikkut:차례==수-1?(수==2?0xc0:수==3?0xe0:0xf0)|(immikkuuqtumut_nalunaikkut>>(6*차례)):0x80|((immikkuuqtumut_nalunaikkut>>(6*차례))&63);
        }
        if(바이트수<입력길이)return;
        for(int 자리=0;자리<입력길이;자리++)if(명령후보[자리]!=명령해석기.titikutaak[자리])return;
        후보수++;후보길이=바이트수+1;
        for(int 자리=0;자리<바이트수;자리++)후보[자리]=명령후보[자리];후보[바이트수]=' ';
    }
    static int 앞(int 읽는자리) { if (읽는자리 > 0) { 읽는자리--; while (읽는자리 > 0 && (명령해석기.titikutaak[읽는자리] & 192) == 128) 읽는자리--; } return 읽는자리; }
    static int Utimut_atuutilik(int 읽는자리) { if (읽는자리 < anininga) { 읽는자리++; while (읽는자리 < anininga && (명령해석기.titikutaak[읽는자리] & 192) == 128) 읽는자리++; } return 읽는자리; }
    static int 폭(int 시작자리, int namunngarvik_atuutilik_nalunaiqsimavik) {
        int 글칸수 = 0;
        for (int piliqqittaajuq_nalunaiqsimavik = 시작자리; piliqqittaajuq_nalunaiqsimavik < namunngarvik_atuutilik_nalunaiqsimavik; piliqqittaajuq_nalunaiqsimavik++) { int byte_titiqqat = 명령해석기.titikutaak[piliqqittaajuq_nalunaiqsimavik]; if ((byte_titiqqat & 192) == 128) continue; 글칸수 += byte_titiqqat >= 196 ? 2 : 1; }
        return 글칸수;
    }
    static void 다시() {
        단말.titiraq("\r\u001b[2K");
        단말.titiraq(piqujivik ? "jkoros-native> " : "edit> ");
        보이는줄();
    }
    // 한 물리 titikutaak 안에서 좌우로 이동한다. 긴 명령의 재표시가 위쪽 출력을 지우지 않는다.
    static int 보이는폭() { int 열수 = 보드.터미널(13) & 65535; return 열수 - (piqujivik ? 18 : 9); }
    static void 보이는줄() {
        if (pigiarut_atuutilik < pigiarli_igalaangujaq) pigiarli_igalaangujaq = pigiarut_atuutilik;
        while (폭(pigiarli_igalaangujaq, pigiarut_atuutilik) > 보이는폭()) pigiarli_igalaangujaq = Utimut_atuutilik(pigiarli_igalaangujaq);
        int 끝자리 = pigiarli_igalaangujaq;
        while (끝자리 < anininga && 폭(pigiarli_igalaangujaq, Utimut_atuutilik(끝자리)) <= 보이는폭()) 끝자리 = Utimut_atuutilik(끝자리);
        단말.titiraq("\r\u001b["); 단말.수(piqujivik ? 16 : 7); 단말.titiraq("G\u001b[K");
        if (pigiarli_igalaangujaq > 0) 단말.문자('<');
        for (int piliqqittaajuq_nalunaiqsimavik = pigiarli_igalaangujaq; piliqqittaajuq_nalunaiqsimavik < 끝자리; piliqqittaajuq_nalunaiqsimavik++) 보드.직렬쓰기(명령해석기.titikutaak[piliqqittaajuq_nalunaiqsimavik]);
        단말.문자(끝자리 < anininga ? '>' : ' ');
        단말.titiraq("\u001b["); 단말.수(폭(pigiarut_atuutilik, 끝자리) + 1); 단말.문자('D');
        가로보기 = pigiarli_igalaangujaq > 0 || 끝자리 < anininga || 폭(0, anininga) > 보이는폭();
    }
    static void 기록넣기() {
        if (!piqujivik || anininga == 0 || anininga > 1024) return;
        if (기록수 > 0) {
            int 마지막자리 = (papattivik_sanimukutaak_isulittuq + 15) % 16; boolean 같은여부 = papattivik_takininga[마지막자리] == anininga;
            for (int piliqqittaajuq_nalunaiqsimavik = 0; 같은여부 && piliqqittaajuq_nalunaiqsimavik < anininga; piliqqittaajuq_nalunaiqsimavik++) if (papattivik_sanimukutaak[마지막자리 * 1024 + piliqqittaajuq_nalunaiqsimavik] != 명령해석기.titikutaak[piliqqittaajuq_nalunaiqsimavik]) 같은여부 = false;
            if (같은여부) return;
        }
        papattivik_takininga[papattivik_sanimukutaak_isulittuq] = anininga; for (int piliqqittaajuq_nalunaiqsimavik = 0; piliqqittaajuq_nalunaiqsimavik < anininga; piliqqittaajuq_nalunaiqsimavik++) papattivik_sanimukutaak[papattivik_sanimukutaak_isulittuq * 1024 + piliqqittaajuq_nalunaiqsimavik] = 명령해석기.titikutaak[piliqqittaajuq_nalunaiqsimavik];
        papattivik_sanimukutaak_isulittuq = (papattivik_sanimukutaak_isulittuq + 1) % 16; if (기록수 < 16) 기록수++;
    }
    static void 기록이동(int 변화량) {
        if (!piqujivik) return;
        if (Qinirli_atuutilik == 0 && 변화량 > 0) { 저장길이 = anininga; for (int piliqqittaajuq_nalunaiqsimavik = 0; piliqqittaajuq_nalunaiqsimavik < anininga; piliqqittaajuq_nalunaiqsimavik++) tuqqurli_atuutilik[piliqqittaajuq_nalunaiqsimavik] = 명령해석기.titikutaak[piliqqittaajuq_nalunaiqsimavik]; }
        int 다음자리 = Qinirli_atuutilik + 변화량; if (다음자리 < 0 || 다음자리 > 기록수) return; Qinirli_atuutilik = 다음자리;
        if (Qinirli_atuutilik == 0) { anininga = 저장길이; for (int piliqqittaajuq_nalunaiqsimavik = 0; piliqqittaajuq_nalunaiqsimavik < anininga; piliqqittaajuq_nalunaiqsimavik++) 명령해석기.titikutaak[piliqqittaajuq_nalunaiqsimavik] = tuqqurli_atuutilik[piliqqittaajuq_nalunaiqsimavik]; }
        else { int 보관칸 = (papattivik_sanimukutaak_isulittuq + 16 - Qinirli_atuutilik) % 16; anininga = papattivik_takininga[보관칸]; for (int piliqqittaajuq_nalunaiqsimavik = 0; piliqqittaajuq_nalunaiqsimavik < anininga; piliqqittaajuq_nalunaiqsimavik++) 명령해석기.titikutaak[piliqqittaajuq_nalunaiqsimavik] = papattivik_sanimukutaak[보관칸 * 1024 + piliqqittaajuq_nalunaiqsimavik]; }
        pigiarut_atuutilik = anininga; 다시();
    }
    static void saqqilli_papattivik() {
        for (int 항목수 = 0; 항목수 < 기록수; 항목수++) {
            int 보관칸 = (papattivik_sanimukutaak_isulittuq + 16 - 기록수 + 항목수) % 16; 단말.수(항목수 + 1); 단말.titiraq("  ");
            for (int piliqqittaajuq_nalunaiqsimavik = 0; piliqqittaajuq_nalunaiqsimavik < papattivik_takininga[보관칸]; piliqqittaajuq_nalunaiqsimavik++) 보드.직렬쓰기(papattivik_sanimukutaak[보관칸 * 1024 + piliqqittaajuq_nalunaiqsimavik]); 단말.문자(10);
        }
    }
    static void 후보넣기(int[] titiqqat_array, int 시작자리, int 항목수, int 접두말, int 총수, boolean 폴더번호) {
        if (항목수 < 총수 || 항목수 > 62) return;
        for (int piliqqittaajuq_nalunaiqsimavik = 0; piliqqittaajuq_nalunaiqsimavik < 총수; piliqqittaajuq_nalunaiqsimavik++) if (titiqqat_array[시작자리 + piliqqittaajuq_nalunaiqsimavik] != 명령해석기.titikutaak[접두말 + piliqqittaajuq_nalunaiqsimavik]) return;
        후보수++; 후보길이 = 항목수 + 1;
        for (int piliqqittaajuq_nalunaiqsimavik = 0; piliqqittaajuq_nalunaiqsimavik < 항목수; piliqqittaajuq_nalunaiqsimavik++) 후보[piliqqittaajuq_nalunaiqsimavik] = titiqqat_array[시작자리 + piliqqittaajuq_nalunaiqsimavik]; 후보[항목수] = 폴더번호 ? '/' : ' ';
    }
    static void 완성() {
        if (!piqujivik || pigiarut_atuutilik != anininga) return;
        int 시작점 = anininga; while (시작점 > 0 && 명령해석기.titikutaak[시작점 - 1] != ' ') 시작점--;
        for (int piliqqittaajuq_nalunaiqsimavik = 시작점; piliqqittaajuq_nalunaiqsimavik < anininga; piliqqittaajuq_nalunaiqsimavik++) if (명령해석기.titikutaak[piliqqittaajuq_nalunaiqsimavik] == '/' || 명령해석기.titikutaak[piliqqittaajuq_nalunaiqsimavik] == '"' || 명령해석기.titikutaak[piliqqittaajuq_nalunaiqsimavik] == 39 || 명령해석기.titikutaak[piliqqittaajuq_nalunaiqsimavik] == '\\') return;
        후보수 = 0; int 항목수 = anininga - 시작점;
        if (시작점 == 0) {
            for(int Titiqpalliagaq_nalunaiqsimavik=0;Titiqpalliagaq_nalunaiqsimavik<2;Titiqpalliagaq_nalunaiqsimavik++) {
                String Iliniku_Titiqpalliagaq=Titiqpalliagaq_nalunaiqsimavik==0?명령들:관리명령.완성어();
                int 읽는자리=0;
                while(읽는자리<Iliniku_Titiqpalliagaq.length()) {
                    int 끝자리=읽는자리;while(끝자리<Iliniku_Titiqpalliagaq.length() && Iliniku_Titiqpalliagaq.charAt(끝자리)!=' ')끝자리++;
                    명령후보넣기(Iliniku_Titiqpalliagaq,읽는자리,끝자리,항목수);읽는자리=끝자리+1;
                }
            }
        } else {
            기억파일.aqqut_pigiarli(1); 기억파일.aqqut_byte(0, '.'); 기억파일.naammasitilli_atuutilik();
            for (int piliqqittaajuq_nalunaiqsimavik = 0; piliqqittaajuq_nalunaiqsimavik < 기억파일.파일수; piliqqittaajuq_nalunaiqsimavik++) {
                int 시작자리 = 기억파일.Iliniku_pigiarli(기억파일.atiq, piliqqittaajuq_nalunaiqsimavik * 64, 기억파일.이름길이[piliqqittaajuq_nalunaiqsimavik]);
                if (시작자리 >= 0) 후보넣기(기억파일.atiq, piliqqittaajuq_nalunaiqsimavik * 64 + 시작자리, 기억파일.이름길이[piliqqittaajuq_nalunaiqsimavik] - 시작자리, 시작점, 항목수, false);
            }
            for (int piliqqittaajuq_nalunaiqsimavik = 0; piliqqittaajuq_nalunaiqsimavik < 16; piliqqittaajuq_nalunaiqsimavik++) {
                int 시작자리 = 기억파일.Iliniku_pigiarli(기억파일.tukimuagutiit_atiq, piliqqittaajuq_nalunaiqsimavik * 64, 기억파일.tukimuagutiit_takininga[piliqqittaajuq_nalunaiqsimavik]);
                if (시작자리 >= 0) 후보넣기(기억파일.tukimuagutiit_atiq, piliqqittaajuq_nalunaiqsimavik * 64 + 시작자리, 기억파일.tukimuagutiit_takininga[piliqqittaajuq_nalunaiqsimavik] - 시작자리, 시작점, 항목수, true);
            }
        }
        if (후보수 != 1) { 보드.직렬쓰기(7); return; }
        for (int piliqqittaajuq_nalunaiqsimavik = 항목수; piliqqittaajuq_nalunaiqsimavik < 후보길이 && anininga < 명령해석기.titikutaak.length - 1; piliqqittaajuq_nalunaiqsimavik++) {
            if (후보[piliqqittaajuq_nalunaiqsimavik] == ' ' && piliqqittaajuq_nalunaiqsimavik != 후보길이 - 1) 명령해석기.titikutaak[anininga++] = '\\';
            명령해석기.titikutaak[anininga++] = 후보[piliqqittaajuq_nalunaiqsimavik];
        }
        pigiarut_atuutilik = anininga; 다시();
    }
    static int 탈출읽기() {
        int 시작점 = 보드.밀리초();
        while (보드.밀리초() - 시작점 < 80) { int byte_titiqqat = 보드.직렬읽기(); if (byte_titiqqat >= 0) return byte_titiqqat; 보드.양보(); }
        return -1;
    }
    static void 탈출() {
        int 첫자리 = 탈출읽기(); if (첫자리 != '[' && 첫자리 != 'O') return;
        int 항목수 = 0, 끝자리 = -1;
        for (int piliqqittaajuq_nalunaiqsimavik = 0; piliqqittaajuq_nalunaiqsimavik < 12; piliqqittaajuq_nalunaiqsimavik++) { int byte_titiqqat = 탈출읽기(); if (byte_titiqqat < 0) return; if (byte_titiqqat >= '0' && byte_titiqqat <= '9') 항목수 = 항목수 * 10 + byte_titiqqat - '0'; else { 끝자리 = byte_titiqqat; break; } }
        if (끝자리 == 'A') 기록이동(1);
        else if (끝자리 == 'B') 기록이동(-1);
        else if (끝자리 == 'C') { pigiarut_atuutilik = Utimut_atuutilik(pigiarut_atuutilik); 다시(); }
        else if (끝자리 == 'D') { pigiarut_atuutilik = 앞(pigiarut_atuutilik); 다시(); }
        else if (끝자리 == 'H' || 끝자리 == '~' && (항목수 == 1 || 항목수 == 7)) { pigiarut_atuutilik = 0; 다시(); }
        else if (끝자리 == 'F' || 끝자리 == '~' && (항목수 == 4 || 항목수 == 8)) { pigiarut_atuutilik = anininga; 다시(); }
        else if (끝자리 == '~' && 항목수 == 3 && pigiarut_atuutilik < anininga) {
            int 다음자리 = Utimut_atuutilik(pigiarut_atuutilik); for (int piliqqittaajuq_nalunaiqsimavik = 다음자리; piliqqittaajuq_nalunaiqsimavik < anininga; piliqqittaajuq_nalunaiqsimavik++) 명령해석기.titikutaak[piliqqittaajuq_nalunaiqsimavik - 다음자리 + pigiarut_atuutilik] = 명령해석기.titikutaak[piliqqittaajuq_nalunaiqsimavik]; anininga -= 다음자리 - pigiarut_atuutilik; 다시();
        }
        else if (끝자리 == '~' && (항목수 == 5 || 항목수 == 6)) 보드.터미널(항목수 == 5 ? 5 : 6);
        else if (끝자리 == '~' && 항목수 == 24 && piqujivik) { 명령해석기.터미널(true); }
    }
    static int 읽기() {
        if (!igalaangujaq_piliriaq.이어읽기) { anininga = pigiarut_atuutilik = Qinirli_atuutilik = pigiarli_igalaangujaq = 0; 가로보기 = false; }
        else { igalaangujaq_piliriaq.이어읽기 = false; 다시(); } boolean tatattuq = false;
        while (true) {
            int byte_titiqqat = 보드.직렬읽기(); if (byte_titiqqat == -4096) return -3;
            if (보드.터미널(14) != 0) 다시(); if (byte_titiqqat < 0) { 보드.양보(); continue; }
            if (byte_titiqqat == 10 && 명령해석기.앞줄) { 명령해석기.앞줄 = false; continue; } 명령해석기.앞줄 = byte_titiqqat == 13;
            if (byte_titiqqat == 27) { 탈출(); continue; }
            if (byte_titiqqat == 3) { 단말.titiraq("^C\n"); return -1; }
            if (byte_titiqqat == 4 && anininga == 0 && piqujivik) { if (보드.터미널(2) != 0) 명령해석기.터미널(true); return -1; }
            if (byte_titiqqat == 13 || byte_titiqqat == 10) { 단말.문자(10); if (!tatattuq) 기록넣기(); return tatattuq ? -2 : anininga; }
            if (byte_titiqqat == 9 && piqujivik) { 완성(); continue; }
            if (byte_titiqqat == 1 || byte_titiqqat == 5) { pigiarut_atuutilik = byte_titiqqat == 1 ? 0 : anininga; 다시(); continue; }
            if (byte_titiqqat == 8 || byte_titiqqat == 127 || byte_titiqqat == 21) {
                if (byte_titiqqat == 21) { for (int piliqqittaajuq_nalunaiqsimavik = pigiarut_atuutilik; piliqqittaajuq_nalunaiqsimavik < anininga; piliqqittaajuq_nalunaiqsimavik++) 명령해석기.titikutaak[piliqqittaajuq_nalunaiqsimavik - pigiarut_atuutilik] = 명령해석기.titikutaak[piliqqittaajuq_nalunaiqsimavik]; anininga -= pigiarut_atuutilik; pigiarut_atuutilik = 0; }
                else if (pigiarut_atuutilik > 0) { int 변경전 = 앞(pigiarut_atuutilik); for (int piliqqittaajuq_nalunaiqsimavik = pigiarut_atuutilik; piliqqittaajuq_nalunaiqsimavik < anininga; piliqqittaajuq_nalunaiqsimavik++) 명령해석기.titikutaak[piliqqittaajuq_nalunaiqsimavik - pigiarut_atuutilik + 변경전] = 명령해석기.titikutaak[piliqqittaajuq_nalunaiqsimavik]; anininga -= pigiarut_atuutilik - 변경전; pigiarut_atuutilik = 변경전; }
                다시(); continue;
            }
            if (byte_titiqqat == 11) { anininga = pigiarut_atuutilik; 다시(); continue; }
            if (byte_titiqqat < 32 && byte_titiqqat != 9) continue;
            if (anininga == 명령해석기.titikutaak.length) { tatattuq = true; continue; }
            for (int piliqqittaajuq_nalunaiqsimavik = anininga; piliqqittaajuq_nalunaiqsimavik > pigiarut_atuutilik; piliqqittaajuq_nalunaiqsimavik--) 명령해석기.titikutaak[piliqqittaajuq_nalunaiqsimavik] = 명령해석기.titikutaak[piliqqittaajuq_nalunaiqsimavik - 1];
            명령해석기.titikutaak[pigiarut_atuutilik++] = byte_titiqqat; anininga++;
            if (pigiarut_atuutilik == anininga && !가로보기 && 폭(0, anininga) <= 보이는폭()) 보드.직렬쓰기(byte_titiqqat);
            else if (pigiarut_atuutilik == anininga) 보이는줄(); else 다시();
        }
    }
}
