// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package हिंदी.निज;
/** 작업 थ्रेड_मान: 하나의 निष्पादित_करें_आदेश स्ट्रीम_मान. निज JVM 안에서 आदेश 수를 기준으로 번갈아 실행한다. */
public final class 작업 {
    private 작업() {}
    public static कार्यसूत्र चलाएँ(실행할일 कार्य_एक्शन) { कार्यसूत्र थ्रेड_मान = new कार्यसूत्र(कार्य_एक्शन); थ्रेड_मान.प्रारंभ_कार्य(); return थ्रेड_मान; }
    public static void 기다리기(कार्यसूत्र थ्रेड_मान) throws 대기중단예외 { थ्रेड_मान.기다리기(); }
    public static boolean 살아있는가(कार्यसूत्र थ्रेड_मान) { return थ्रेड_मान.살아있는가(); }
    public static void स्थगित_करें_कार्य() { कार्यसूत्र.स्थगित_करें_कार्य(); }
}
