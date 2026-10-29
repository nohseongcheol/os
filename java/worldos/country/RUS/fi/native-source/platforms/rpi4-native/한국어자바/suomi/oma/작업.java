// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package suomi.oma;
/** 작업 säie_ARVO: 하나의 Suorita_komento virta_ARVO. oma JVM 안에서 komento 수를 기준으로 번갈아 실행한다. */
public final class 작업 {
    private 작업() {}
    public static työntekijä Suorita_2(실행할일 tehtävä_toimi) { työntekijä säie_ARVO = new työntekijä(tehtävä_toimi); säie_ARVO.alku_tehtävä(); return säie_ARVO; }
    public static void 기다리기(työntekijä säie_ARVO) throws 대기중단예외 { säie_ARVO.기다리기(); }
    public static boolean 살아있는가(työntekijä säie_ARVO) { return säie_ARVO.살아있는가(); }
    public static void TUOTTO_tehtävä() { työntekijä.TUOTTO_tehtävä(); }
}
