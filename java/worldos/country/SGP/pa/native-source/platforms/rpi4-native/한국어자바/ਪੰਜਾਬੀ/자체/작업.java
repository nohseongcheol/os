// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ਪੰਜਾਬੀ.자체;
/** 작업 ਥ੍ਰੈਡ_ਕੀਮਤ: 하나의 ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼ ਸਟ੍ਰੀਮ_ਕੀਮਤ. 자체 JVM 안에서 ਕਮਾਂਡ 수를 기준으로 번갈아 실행한다. */
public final class 작업 {
    private 작업() {}
    public static 작업가닥 ਚਲਾਓ_2(실행할일 ਕਾਰਜ_ਕਿਰਿਆ) { 작업가닥 ਥ੍ਰੈਡ_ਕੀਮਤ = new 작업가닥(ਕਾਰਜ_ਕਿਰਿਆ); ਥ੍ਰੈਡ_ਕੀਮਤ.ਸੁਰੂ_ਕਾਰਜ(); return ਥ੍ਰੈਡ_ਕੀਮਤ; }
    public static void 기다리기(작업가닥 ਥ੍ਰੈਡ_ਕੀਮਤ) throws 대기중단예외 { ਥ੍ਰੈਡ_ਕੀਮਤ.기다리기(); }
    public static boolean 살아있는가(작업가닥 ਥ੍ਰੈਡ_ਕੀਮਤ) { return ਥ੍ਰੈਡ_ਕੀਮਤ.살아있는가(); }
    public static void ਮੁਅੱਤਲ_ਕਾਰਜ() { 작업가닥.ਮੁਅੱਤਲ_ਕਾਰਜ(); }
}
