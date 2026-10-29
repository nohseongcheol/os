// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ગુજરાતી.자체;
/** 작업 થ્રેડ_મૂલ્ય: 하나의 અમલ_કરો_આદેશ સ્ટ્રીમ_મૂલ્ય. 자체 JVM 안에서 આદેશ 수를 기준으로 번갈아 실행한다. */
public final class 작업 {
    private 작업() {}
    public static 작업가닥 ચલાવો_2(실행할일 કાર્ય_સંદેશ) { 작업가닥 થ્રેડ_મૂલ્ય = new 작업가닥(કાર્ય_સંદેશ); થ્રેડ_મૂલ્ય.પ્રારંભ_કાર્ય(); return થ્રેડ_મૂલ્ય; }
    public static void 기다리기(작업가닥 થ્રેડ_મૂલ્ય) throws 대기중단예외 { થ્રેડ_મૂલ્ય.기다리기(); }
    public static boolean 살아있는가(작업가닥 થ્રેડ_મૂલ્ય) { return થ્રેડ_મૂલ્ય.살아있는가(); }
    public static void સ્થગિત_કરો_કાર્ય() { 작업가닥.સ્થગિત_કરો_કાર્ય(); }
}
