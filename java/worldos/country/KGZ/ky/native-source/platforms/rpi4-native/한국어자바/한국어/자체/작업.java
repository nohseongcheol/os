// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
/** 작업 трэд_маани: 하나의 аткаруу_буйрук агым_маани. 자체 JVM 안에서 Команда 수를 기준으로 번갈아 실행한다. */
public final class 작업 {
    private 작업() {}
    public static 작업가닥 Жүргүзүү(실행할일 маселе_иш_аракет) { 작업가닥 трэд_маани = new 작업가닥(маселе_иш_аракет); трэд_маани.Баштоо_маселе(); return трэд_маани; }
    public static void 기다리기(작업가닥 трэд_маани) throws 대기중단예외 { трэд_маани.기다리기(); }
    public static boolean 살아있는가(작업가닥 трэд_маани) { return трэд_маани.살아있는가(); }
    public static void токтотуу_маселе() { 작업가닥.токтотуу_маселе(); }
}
