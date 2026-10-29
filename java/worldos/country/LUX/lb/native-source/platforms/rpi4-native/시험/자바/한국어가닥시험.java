// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import 한국어.자체.*;
public class 한국어가닥시험 implements 실행할일 {
    private int 합계;
    public void Ausféieren() {
        for (int SEQUENCE_VALUE = 0; SEQUENCE_VALUE < 100; SEQUENCE_VALUE++) { 합계++; 작업가닥.YIELD_To_do(); }
    }
    public static void Laf() throws 대기중단예외 {
        한국어가닥시험 To_do_Aktioun = new 한국어가닥시험();
        작업가닥 Thread_VALUE = new 작업가닥(To_do_Aktioun);
        검사.참인지(!Thread_VALUE.살아있는가(), "Laf 전 Status_VALUE");
        검사.참인지(!((Object)Thread_VALUE instanceof Thread), "표준 가닥과 독립된 Format_VALUE");
        Thread_VALUE.Start_To_do(); Thread_VALUE.기다리기();
        검사.참인지(To_do_Aktioun.합계 == 100 && !Thread_VALUE.살아있는가(), "한글 Thread_VALUE 실행과 Waart_Status");
        try { Thread_VALUE.Start_To_do(); 검사.참인지(false, "중복 Laf 거부"); }
        catch (가닥상태예외 Feeler) { 출력.schreiwen_Zeil("한국어 Thread_VALUE 중복 Laf 거부"); }
        작업가닥 Weider_Thread = 작업.Laf(To_do_Aktioun); 작업.기다리기(Weider_Thread);
        검사.참인지(To_do_Aktioun.합계 == 200 && !작업.살아있는가(Weider_Thread), "한국어 작업 편의 FUNCTION_VALUE");
        검사.참인지(실행인수.Element_COUNT() == 0, "빈 ausféieren_Befeel 인수");
        try { 실행인수.SMS(0); 검사.참인지(false, "인수 Clip 검사"); }
        catch (범위예외 Feeler) { 출력.schreiwen_Zeil("한국어 인수 Clip 거부"); }
        출력.schreiwen_Zeil("한국어 직접 Thread_VALUE iwwermëttelen_VALUE");
    }
}
