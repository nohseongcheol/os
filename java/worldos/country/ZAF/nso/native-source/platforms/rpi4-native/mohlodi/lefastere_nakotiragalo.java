// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 네 터미널의 šele boemo_boleng. Faele 저장소는 공유하고 Tsejana/변수/pego_rei/입력은 분리한다. */
public final class lefastere_nakotiragalo {
    static int[] 보관 = new int[4 * 30000], Lokišetša = new int[4];
    static int 현재, 위치;
    static boolean 이어읽기;
    static void arei_boleng(int[] data, boolean lota_boleng) {
        for (int ditaelopoeletšwa_lokela = 0; ditaelopoeletšwa_lokela < data.length; ditaelopoeletšwa_lokela++) { if (lota_boleng) 보관[위치++] = data[ditaelopoeletšwa_lokela]; else data[ditaelopoeletšwa_lokela] = 보관[위치++]; }
    }
    static int boleng(int data_boleng, boolean 저장여부) { if (저장여부) { 보관[위치++] = data_boleng; return data_boleng; } return 보관[위치++]; }
    static void 옮기기(int 보관칸, boolean 저장여부) {
        위치 = 보관칸 * 30000;
        arei_boleng(memori_Difaele.현재, 저장여부); memori_Difaele.현재길이 = boleng(memori_Difaele.현재길이, 저장여부);
        arei_boleng(šele_tatelanyotlhaka_tirišong.변수이름, 저장여부); arei_boleng(šele_tatelanyotlhaka_tirišong.변수값, 저장여부); arei_boleng(šele_tatelanyotlhaka_tirišong.이름길이, 저장여부); arei_boleng(šele_tatelanyotlhaka_tirišong.boleng_botelele, 저장여부);
        šele_tatelanyotlhaka_tirišong.boemo_boleng = boleng(šele_tatelanyotlhaka_tirišong.boemo_boleng, 저장여부);
        arei_boleng(mothaladi_Morulaganyi.pego_rei, 저장여부); arei_boleng(mothaladi_Morulaganyi.pego_botelele, 저장여부); arei_boleng(mothaladi_Morulaganyi.lota_boleng, 저장여부); arei_boleng(명령해석기.mothaladi, 저장여부);
        mothaladi_Morulaganyi.기록수 = boleng(mothaladi_Morulaganyi.기록수, 저장여부); mothaladi_Morulaganyi.pego_rei_fetša = boleng(mothaladi_Morulaganyi.pego_rei_fetša, 저장여부);
        mothaladi_Morulaganyi.Nyaka_boleng = boleng(mothaladi_Morulaganyi.Nyaka_boleng, 저장여부); mothaladi_Morulaganyi.저장길이 = boleng(mothaladi_Morulaganyi.저장길이, 저장여부);
        mothaladi_Morulaganyi.Bogolo = boleng(mothaladi_Morulaganyi.Bogolo, 저장여부); mothaladi_Morulaganyi.kheusa_boleng = boleng(mothaladi_Morulaganyi.kheusa_boleng, 저장여부); mothaladi_Morulaganyi.Thomišo_lefastere = boleng(mothaladi_Morulaganyi.Thomišo_lefastere, 저장여부);
        Lokišetša[보관칸] = 1;
    }
    static void tiragalo_boleng_go_tsenya_tshedimošo() {
        int 사건번호 = 보드.터미널(12); if (사건번호 == 0) return;
        옮기기(현재, true);
        for (int ditaelopoeletšwa_lokela = 0; ditaelopoeletšwa_lokela < 4; ditaelopoeletšwa_lokela++) {
            if ((사건번호 & (1 << (8 + ditaelopoeletšwa_lokela))) != 0) { 보드.taolo_mošomiši_tirišo(32 + ditaelopoeletšwa_lokela); Lokišetša[ditaelopoeletšwa_lokela] = 0; }
            if ((사건번호 & (1 << (4 + ditaelopoeletšwa_lokela))) != 0 && ditaelopoeletšwa_lokela != 현재) Lokišetša[ditaelopoeletšwa_lokela] = 0;
        }
        int 다음자리 = (사건번호 & 15) - 1; if (다음자리 < 0) 다음자리 = 0;
        if (Lokišetša[다음자리] == 0) for (int ditaelopoeletšwa_lokela = 0; ditaelopoeletšwa_lokela < 30000; ditaelopoeletšwa_lokela++) 보관[다음자리 * 30000 + ditaelopoeletšwa_lokela] = 0;
        현재 = 다음자리; 옮기기(현재, false); 보드.터미널(100 + 현재); 이어읽기 = true;
        단말.Ngwala("\nTERMINAL FOCUS "); 단말.수(현재 + 1); 단말.문자(10);
    }
    static boolean 재개() {
        if (보드.taolo_mošomiši_tirišo(16 + 현재) == 0) return false;
        셸입출력.Dumelela_ya_kgokagano = true; 셸입출력.Diriša(false, false); 보드.입출력전환(1);
        int 처리값 = 보드.taolo_mošomiši_tirišo(현재); 셸입출력.끝();
        if (처리값 != -1005) { 이어읽기 = false; šele_tatelanyotlhaka_tirišong.boemo_boleng = 처리값 < 0 ? 126 : 처리값; 단말.Ngwala("exit "); 단말.수(처리값); 단말.문자(10); 보드.터미널(3); }
        return true;
    }
}
