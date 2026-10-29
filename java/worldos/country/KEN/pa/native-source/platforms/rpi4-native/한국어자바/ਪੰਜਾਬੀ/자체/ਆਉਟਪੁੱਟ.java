// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ਪੰਜਾਬੀ.자체;
/** 자체 커널의 표준 ਆਉਟਪੁੱਟ. UTF-16 서로게이트 쌍은 UART에서 UTF-8로 보낸다. */
public final class ਆਉਟਪੁੱਟ {
    private ਆਉਟਪੁੱਟ() {}
    public static void ਲਿਖਣ(String ਟੈਕਸਟ) { System.out.print(ਟੈਕਸਟ); }
    public static void ਲਿੱਖੋ_ਕਤਾਰ(String ਟੈਕਸਟ) { System.out.println(ਟੈਕਸਟ); }
    public static void 수쓰기(int 수) { System.out.println(수); }
}
