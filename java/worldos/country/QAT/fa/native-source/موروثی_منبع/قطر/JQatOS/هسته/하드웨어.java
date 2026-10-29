// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package قطر.JQatOS.هسته;

/** Java 관리 커널과 CPU 고유 کد_مقدار 사이의 유일한 경계다. */
public interface 하드웨어 {
    void 직렬출력(String محتوا_مقدار);

    int 포트바이트읽기(int 포트번호);

    void نوشتن_تبدیل_بایت(int 포트번호, int مقدار);

    void 중앙처리장치멈춤();
}

