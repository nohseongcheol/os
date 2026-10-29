// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 네 터미널의 Mai_fayyace_umani Matsayi_Daraja. Fayil 저장소는 공유하고 Hanyar_shiga/변수/logu_naɗa/입력은 분리한다. */
public final class taga_Mahadin_canjin_bayanai {
    static int[] 보관 = new int[4 * 30000], Shirya = new int[4];
    static int 현재, 위치;
    static boolean 이어읽기;
    static void TSARI_Daraja(int[] Tarin_bayani, boolean Ajiye_Daraja) {
        for (int Warware_Indes = 0; Warware_Indes < Tarin_bayani.length; Warware_Indes++) { if (Ajiye_Daraja) 보관[위치++] = Tarin_bayani[Warware_Indes]; else Tarin_bayani[Warware_Indes] = 보관[위치++]; }
    }
    static int Daraja(int Tarin_bayani_Daraja, boolean 저장여부) { if (저장여부) { 보관[위치++] = Tarin_bayani_Daraja; return Tarin_bayani_Daraja; } return 보관[위치++]; }
    static void 옮기기(int 보관칸, boolean 저장여부) {
        위치 = 보관칸 * 30000;
        TSARI_Daraja(Mahardatar_kwamfuta_Fayiloli.현재, 저장여부); Mahardatar_kwamfuta_Fayiloli.현재길이 = Daraja(Mahardatar_kwamfuta_Fayiloli.현재길이, 저장여부);
        TSARI_Daraja(Mai_fayyace_umani_Ka_idojin_zancen_kwamfuta.변수이름, 저장여부); TSARI_Daraja(Mai_fayyace_umani_Ka_idojin_zancen_kwamfuta.변수값, 저장여부); TSARI_Daraja(Mai_fayyace_umani_Ka_idojin_zancen_kwamfuta.이름길이, 저장여부); TSARI_Daraja(Mai_fayyace_umani_Ka_idojin_zancen_kwamfuta.Daraja_Tsawo, 저장여부);
        Mai_fayyace_umani_Ka_idojin_zancen_kwamfuta.Matsayi_Daraja = Daraja(Mai_fayyace_umani_Ka_idojin_zancen_kwamfuta.Matsayi_Daraja, 저장여부);
        TSARI_Daraja(Layi_Edita.logu_naɗa, 저장여부); TSARI_Daraja(Layi_Edita.logu_Tsawo, 저장여부); TSARI_Daraja(Layi_Edita.Ajiye_Daraja, 저장여부); TSARI_Daraja(명령해석기.Layi, 저장여부);
        Layi_Edita.기록수 = Daraja(Layi_Edita.기록수, 저장여부); Layi_Edita.logu_naɗa_Ƙarshe = Daraja(Layi_Edita.logu_naɗa_Ƙarshe, 저장여부);
        Layi_Edita.Leko_Daraja = Daraja(Layi_Edita.Leko_Daraja, 저장여부); Layi_Edita.저장길이 = Daraja(Layi_Edita.저장길이, 저장여부);
        Layi_Edita.Girma = Daraja(Layi_Edita.Girma, 저장여부); Layi_Edita.Ɗan_jagora_Daraja = Daraja(Layi_Edita.Ɗan_jagora_Daraja, 저장여부); Layi_Edita.Fara_taga = Daraja(Layi_Edita.Fara_taga, 저장여부);
        Shirya[보관칸] = 1;
    }
    static void haryar_aikin_na_ura_Daraja_Mashigar_bayanai() {
        int 사건번호 = 보드.터미널(12); if (사건번호 == 0) return;
        옮기기(현재, true);
        for (int Warware_Indes = 0; Warware_Indes < 4; Warware_Indes++) {
            if ((사건번호 & (1 << (8 + Warware_Indes))) != 0) { 보드.masarrafa_Mai_anfani_da_kwamfuta_Shiri(32 + Warware_Indes); Shirya[Warware_Indes] = 0; }
            if ((사건번호 & (1 << (4 + Warware_Indes))) != 0 && Warware_Indes != 현재) Shirya[Warware_Indes] = 0;
        }
        int 다음자리 = (사건번호 & 15) - 1; if (다음자리 < 0) 다음자리 = 0;
        if (Shirya[다음자리] == 0) for (int Warware_Indes = 0; Warware_Indes < 30000; Warware_Indes++) 보관[다음자리 * 30000 + Warware_Indes] = 0;
        현재 = 다음자리; 옮기기(현재, false); 보드.터미널(100 + 현재); 이어읽기 = true;
        단말.Yi_Rubutu("\nTERMINAL FOCUS "); 단말.수(현재 + 1); 단말.문자(10);
    }
    static boolean 재개() {
        if (보드.masarrafa_Mai_anfani_da_kwamfuta_Shiri(16 + 현재) == 0) return false;
        셸입출력.Bada_izini_Shigar_da_umarni_na_kwamfuta = true; 셸입출력.Tafiyar_da(false, false); 보드.입출력전환(1);
        int 처리값 = 보드.masarrafa_Mai_anfani_da_kwamfuta_Shiri(현재); 셸입출력.끝();
        if (처리값 != -1005) { 이어읽기 = false; Mai_fayyace_umani_Ka_idojin_zancen_kwamfuta.Matsayi_Daraja = 처리값 < 0 ? 126 : 처리값; 단말.Yi_Rubutu("exit "); 단말.수(처리값); 단말.문자(10); 보드.터미널(3); }
        return true;
    }
}
