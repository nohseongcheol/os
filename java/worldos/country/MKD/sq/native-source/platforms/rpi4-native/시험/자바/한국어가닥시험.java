// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import 한국어.자체.*;
public class 한국어가닥시험 implements 실행할일 {
    private int 합계;
    public void Kryej() {
        for (int SEQUENCE_VALUE = 0; SEQUENCE_VALUE < 100; SEQUENCE_VALUE++) { 합계++; 작업가닥.YIELD_detyrë(); }
    }
    public static void Ekzekuto() throws 대기중단예외 {
        한국어가닥시험 detyrë_veprim = new 한국어가닥시험();
        작업가닥 thread_VALUE = new 작업가닥(detyrë_veprim);
        검사.참인지(!thread_VALUE.살아있는가(), "Ekzekuto 전 status_VALUE");
        검사.참인지(!((Object)thread_VALUE instanceof Thread), "표준 가닥과 독립된 format_VALUE");
        thread_VALUE.nis_detyrë(); thread_VALUE.기다리기();
        검사.참인지(detyrë_veprim.합계 == 100 && !thread_VALUE.살아있는가(), "한글 thread_VALUE 실행과 Prit_status");
        try { thread_VALUE.nis_detyrë(); 검사.참인지(false, "중복 Ekzekuto refuzo_VALUE"); }
        catch (thread_status_përjashtim GABIM) { 출력.shkruaj_linjë("한국어 thread_VALUE 중복 Ekzekuto refuzo_VALUE"); }
        작업가닥 Tjetër_thread = 작업.Ekzekuto(detyrë_veprim); 작업.기다리기(Tjetër_thread);
        검사.참인지(detyrë_veprim.합계 == 200 && !작업.살아있는가(Tjetër_thread), "한국어 작업 편의 FUNCTION_VALUE");
        검사.참인지(실행인수.njësi_COUNT() == 0, "빈 zbatoj_komandë Argumente");
        try { 실행인수.Teksti(0); 검사.참인지(false, "Argumente fragment 검사"); }
        catch (범위예외 GABIM) { 출력.shkruaj_linjë("한국어 Argumente fragment refuzo_VALUE"); }
        출력.shkruaj_linjë("한국어 직접 thread_VALUE kaloj_VALUE");
    }
}
