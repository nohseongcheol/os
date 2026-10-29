// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import isiXhosa.자체.*;
public class 한국어가닥시험 implements 실행할일 {
    private int 합계;
    public void ukwenza_umsebenzi() {
        for (int ULANDELELWANO_ixabiso = 0; ULANDELELWANO_ixabiso < 100; ULANDELELWANO_ixabiso++) { 합계++; 작업가닥.misa_okwexeshana_umsebenzi(); }
    }
    public static void Phumeza() throws 대기중단예외 {
        한국어가닥시험 umsebenzi_Isenzo = new 한국어가닥시험();
        작업가닥 ithredi_ixabiso = new 작업가닥(umsebenzi_Isenzo);
        검사.참인지(!ithredi_ixabiso.살아있는가(), "Phumeza 전 imo_ixabiso");
        검사.참인지(!((Object)ithredi_ixabiso instanceof Thread), "표준 가닥과 독립된 fomatha_ixabiso");
        ithredi_ixabiso.qala_umsebenzi(); ithredi_ixabiso.기다리기();
        검사.참인지(umsebenzi_Isenzo.합계 == 100 && !ithredi_ixabiso.살아있는가(), "한글 ithredi_ixabiso 실행과 기다림");
        try { ithredi_ixabiso.qala_umsebenzi(); 검사.참인지(false, "중복 Phumeza 거부"); }
        catch (가닥상태예외 Impazamo) { 출력.bhala_umgca("isiXhosa ithredi_ixabiso 중복 Phumeza 거부"); }
        작업가닥 다음가닥 = 작업.Phumeza(umsebenzi_Isenzo); 작업.기다리기(다음가닥);
        검사.참인지(umsebenzi_Isenzo.합계 == 200 && !작업.살아있는가(다음가닥), "isiXhosa 작업 편의 INKQUBO_ixabiso");
        검사.참인지(실행인수.개수() == 0, "빈 ukwenza_umyalelo 인수");
        try { 실행인수.Umbhalo(0); 검사.참인지(false, "인수 ikliphu 검사"); }
        catch (범위예외 Impazamo) { 출력.bhala_umgca("isiXhosa 인수 ikliphu 거부"); }
        출력.bhala_umgca("isiXhosa 직접 ithredi_ixabiso dlulisela_ixabiso");
    }
}
