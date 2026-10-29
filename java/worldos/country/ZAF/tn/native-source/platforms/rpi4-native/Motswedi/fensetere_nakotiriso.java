// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 네 터미널의 setlhalosataelo kemo_Boleng. faele 저장소는 공유하고 tsela/변수/rekota_mola/입력은 분리한다. */
public final class fensetere_nakotiriso {
    static int[] 보관 = new int[4 * 30000], Baakanya = new int[4];
    static int ga_jaana_selwana, 위치;
    static boolean 이어읽기;
    static void setlhopha_Boleng_ed437109(int[] tshedimosetso, boolean Store_Boleng) {
        for (int lupu_tshupane = 0; lupu_tshupane < tshedimosetso.length; lupu_tshupane++) { if (Store_Boleng) 보관[위치++] = tshedimosetso[lupu_tshupane]; else tshedimosetso[lupu_tshupane] = 보관[위치++]; }
    }
    static int Boleng(int tshedimosetso_Boleng, boolean 저장여부) { if (저장여부) { 보관[위치++] = tshedimosetso_Boleng; return tshedimosetso_Boleng; } return 보관[위치++]; }
    static void 옮기기(int 보관칸, boolean 저장여부) {
        위치 = 보관칸 * 30000;
        setlhopha_Boleng_ed437109(memori_Difaele.ga_jaana_selwana, 저장여부); memori_Difaele.ga_jaana_boleele = Boleng(memori_Difaele.ga_jaana_boleele, 저장여부);
        setlhopha_Boleng_ed437109(setlhalosataelo_popapolelo.변수이름, 저장여부); setlhopha_Boleng_ed437109(setlhalosataelo_popapolelo.변수값, 저장여부); setlhopha_Boleng_ed437109(setlhalosataelo_popapolelo.이름길이, 저장여부); setlhopha_Boleng_ed437109(setlhalosataelo_popapolelo.Boleng_boleele, 저장여부);
        setlhalosataelo_popapolelo.kemo_Boleng = Boleng(setlhalosataelo_popapolelo.kemo_Boleng, 저장여부);
        setlhopha_Boleng_ed437109(Mola_Setseleganyi.rekota_mola, 저장여부); setlhopha_Boleng_ed437109(Mola_Setseleganyi.rekota_boleele, 저장여부); setlhopha_Boleng_ed437109(Mola_Setseleganyi.Store_Boleng, 저장여부); setlhopha_Boleng_ed437109(명령해석기.Mola, 저장여부);
        Mola_Setseleganyi.기록수 = Boleng(Mola_Setseleganyi.기록수, 저장여부); Mola_Setseleganyi.rekota_mola_kgaola = Boleng(Mola_Setseleganyi.rekota_mola_kgaola, 저장여부);
        Mola_Setseleganyi.batla_Boleng = Boleng(Mola_Setseleganyi.batla_Boleng, 저장여부); Mola_Setseleganyi.저장길이 = Boleng(Mola_Setseleganyi.저장길이, 저장여부);
        Mola_Setseleganyi.lekanya = Boleng(Mola_Setseleganyi.lekanya, 저장여부); Mola_Setseleganyi.khesara_Boleng = Boleng(Mola_Setseleganyi.khesara_Boleng, 저장여부); Mola_Setseleganyi.simolola_fensetere = Boleng(Mola_Setseleganyi.simolola_fensetere, 저장여부);
        Baakanya[보관칸] = 1;
    }
    static void Thulaganyo_Boleng_tsenyo() {
        int 사건번호 = 보드.터미널(12); if (사건번호 == 0) return;
        옮기기(ga_jaana_selwana, true);
        for (int lupu_tshupane = 0; lupu_tshupane < 4; lupu_tshupane++) {
            if ((사건번호 & (1 << (8 + lupu_tshupane))) != 0) { 보드.taolo_modirisi_Tiriso(32 + lupu_tshupane); Baakanya[lupu_tshupane] = 0; }
            if ((사건번호 & (1 << (4 + lupu_tshupane))) != 0 && lupu_tshupane != ga_jaana_selwana) Baakanya[lupu_tshupane] = 0;
        }
        int 다음자리 = (사건번호 & 15) - 1; if (다음자리 < 0) 다음자리 = 0;
        if (Baakanya[다음자리] == 0) for (int lupu_tshupane = 0; lupu_tshupane < 30000; lupu_tshupane++) 보관[다음자리 * 30000 + lupu_tshupane] = 0;
        ga_jaana_selwana = 다음자리; 옮기기(ga_jaana_selwana, false); 보드.터미널(100 + ga_jaana_selwana); 이어읽기 = true;
        단말.kwala("\nTERMINAL FOCUS "); 단말.수(ga_jaana_selwana + 1); 단말.문자(10);
    }
    static boolean 재개() {
        if (보드.taolo_modirisi_Tiriso(16 + ga_jaana_selwana) == 0) return false;
        셸입출력.letla_Tirisano = true; 셸입출력.dirisa(false, false); 보드.입출력전환(1);
        int 처리값 = 보드.taolo_modirisi_Tiriso(ga_jaana_selwana); 셸입출력.끝();
        if (처리값 != -1005) { 이어읽기 = false; setlhalosataelo_popapolelo.kemo_Boleng = 처리값 < 0 ? 126 : 처리값; 단말.kwala("exit "); 단말.수(처리값); 단말.문자(10); 보드.터미널(3); }
        return true;
    }
}
