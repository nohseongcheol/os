// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package नेपाली.निज;
/** 작업 धागो_मान: 하나의 कार्यान्वयन_गर्नुहोस्_आदेश प्रवाह_मान. निज JVM 안에서 आदेश 수를 기준으로 번갈아 실행한다. */
public final class 작업 {
    private 작업() {}
    public static 작업가닥 चलाउनुहोस्(실행할일 कार्य_कार्य) { 작업가닥 धागो_मान = new 작업가닥(कार्य_कार्य); धागो_मान.सुरु_कार्य(); return धागो_मान; }
    public static void 기다리기(작업가닥 धागो_मान) throws 대기중단예외 { धागो_मान.기다리기(); }
    public static boolean 살아있는가(작업가닥 धागो_मान) { return धागो_मान.살아있는가(); }
    public static void स्थगन_गर्नुहोस्_कार्य() { 작업가닥.स्थगन_गर्नुहोस्_कार्य(); }
}
