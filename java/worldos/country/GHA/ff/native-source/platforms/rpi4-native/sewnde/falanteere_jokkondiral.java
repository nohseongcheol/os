// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 네 터미널의 laalagal ngonka_njaru. fiilde 저장소는 공유하고 laawol/변수/suurnal_winndande/입력은 분리한다. */
public final class falanteere_jokkondiral {
    static int[] 보관 = new int[4 * 30000], Heblu = new int[4];
    static int 현재, 위치;
    static boolean 이어읽기;
    static void 배열(int[] keɓe, boolean resde_njaru) {
        for (int kowal_joopirdu = 0; kowal_joopirdu < keɓe.length; kowal_joopirdu++) { if (resde_njaru) 보관[위치++] = keɓe[kowal_joopirdu]; else keɓe[kowal_joopirdu] = 보관[위치++]; }
    }
    static int njaru(int keɓe_njaru, boolean 저장여부) { if (저장여부) { 보관[위치++] = keɓe_njaru; return keɓe_njaru; } return 보관[위치++]; }
    static void 옮기기(int 보관칸, boolean 저장여부) {
        위치 = 보관칸 * 30000;
        배열(기억파일.현재, 저장여부); 기억파일.현재길이 = njaru(기억파일.현재길이, 저장여부);
        배열(셸문법.변수이름, 저장여부); 배열(셸문법.변수값, 저장여부); 배열(셸문법.이름길이, 저장여부); 배열(셸문법.njaru_njuuteendi, 저장여부);
        셸문법.ngonka_njaru = njaru(셸문법.ngonka_njaru, 저장여부);
        배열(diidol_feewnditirde.suurnal_winndande, 저장여부); 배열(diidol_feewnditirde.suurnal_njuuteendi, 저장여부); 배열(diidol_feewnditirde.resde_njaru, 저장여부); 배열(명령해석기.diidol, 저장여부);
        diidol_feewnditirde.기록수 = njaru(diidol_feewnditirde.기록수, 저장여부); diidol_feewnditirde.suurnal_winndande_taƴde = njaru(diidol_feewnditirde.suurnal_winndande_taƴde, 저장여부);
        diidol_feewnditirde.njiilawu_njaru = njaru(diidol_feewnditirde.njiilawu_njaru, 저장여부); diidol_feewnditirde.저장길이 = njaru(diidol_feewnditirde.저장길이, 저장여부);
        diidol_feewnditirde.waylude_etannde = njaru(diidol_feewnditirde.waylude_etannde, 저장여부); diidol_feewnditirde.kirseer_njaru = njaru(diidol_feewnditirde.kirseer_njaru, 저장여부); diidol_feewnditirde.huɓɓude_falanteere = njaru(diidol_feewnditirde.huɓɓude_falanteere, 저장여부);
        Heblu[보관칸] = 1;
    }
    static void Yuɓɓo_golle_njaru_naatnugol() {
        int 사건번호 = 보드.터미널(12); if (사건번호 == 0) return;
        옮기기(현재, true);
        for (int kowal_joopirdu = 0; kowal_joopirdu < 4; kowal_joopirdu++) {
            if ((사건번호 & (1 << (8 + kowal_joopirdu))) != 0) { 보드.yuurnitorde_kuutoro_tafirde(32 + kowal_joopirdu); Heblu[kowal_joopirdu] = 0; }
            if ((사건번호 & (1 << (4 + kowal_joopirdu))) != 0 && kowal_joopirdu != 현재) Heblu[kowal_joopirdu] = 0;
        }
        int 다음자리 = (사건번호 & 15) - 1; if (다음자리 < 0) 다음자리 = 0;
        if (Heblu[다음자리] == 0) for (int kowal_joopirdu = 0; kowal_joopirdu < 30000; kowal_joopirdu++) 보관[다음자리 * 30000 + kowal_joopirdu] = 0;
        현재 = 다음자리; 옮기기(현재, false); 보드.터미널(100 + 현재); 이어읽기 = true;
        단말.winndude("\nTERMINAL FOCUS "); 단말.수(현재 + 1); 단말.문자(10);
    }
    static boolean 재개() {
        if (보드.yuurnitorde_kuutoro_tafirde(16 + 현재) == 0) return false;
        셸입출력.Wellit_jokkondirtoo = true; 셸입출력.huutoraade(false, false); 보드.입출력전환(1);
        int 처리값 = 보드.yuurnitorde_kuutoro_tafirde(현재); 셸입출력.끝();
        if (처리값 != -1005) { 이어읽기 = false; 셸문법.ngonka_njaru = 처리값 < 0 ? 126 : 처리값; 단말.winndude("exit "); 단말.수(처리값); 단말.문자(10); 보드.터미널(3); }
        return true;
    }
}
