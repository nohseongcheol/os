// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import Català.propi.*;
public class 한국어가닥시험 implements 실행할일 {
    private int total_VALOR;
    public void Executa() {
        for (int SEQÜÈNCIA_VALOR = 0; SEQÜÈNCIA_VALOR < 100; SEQÜÈNCIA_VALOR++) { total_VALOR++; 작업가닥.RENDTO_tasca(); }
    }
    public static void Executa_2() throws 대기중단예외 {
        한국어가닥시험 tasca_acció = new 한국어가닥시험();
        작업가닥 fil_VALOR = new 작업가닥(tasca_acció);
        검사.참인지(!fil_VALOR.살아있는가(), "Executa_2 전 Estat_VALOR");
        검사.참인지(!((Object)fil_VALOR instanceof Thread), "표준 가닥과 독립된 format_VALOR");
        fil_VALOR.Inici_tasca(); fil_VALOR.기다리기();
        검사.참인지(tasca_acció.total_VALOR == 100 && !fil_VALOR.살아있는가(), "한글 fil_VALOR 실행과 Espera_Estat");
        try { fil_VALOR.Inici_tasca(); 검사.참인지(false, "중복 Executa_2 rebutjar_VALOR"); }
        catch (fil_Estat_excepció s_ha_produït_un_error) { Sortida.escriure_línia("Català fil_VALOR 중복 Executa_2 rebutjar_VALOR"); }
        작업가닥 Següent_fil = 작업.Executa_2(tasca_acció); 작업.기다리기(Següent_fil);
        검사.참인지(tasca_acció.total_VALOR == 200 && !작업.살아있는가(Següent_fil), "Català 작업 편의 FUNCIÓ_VALOR");
        검사.참인지(실행인수.element_COMPT() == 0, "빈 Executa_ordre 인수");
        try { 실행인수.SMS(0); 검사.참인지(false, "인수 clip 검사"); }
        catch (범위예외 s_ha_produït_un_error) { Sortida.escriure_línia("Català 인수 clip rebutjar_VALOR"); }
        Sortida.escriure_línia("Català 직접 fil_VALOR transmetre_VALOR");
    }
}
