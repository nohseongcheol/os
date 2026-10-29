// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ኢትዮጵያ.JEthOS.ዓንኳር;

/** Java 관리 커널과 CPU 고유 코드 사이의 유일한 경계다. */
public interface 하드웨어 {
    void 직렬출력(String ይዘት_እሴት);

    int 포트바이트읽기(int 포트번호);

    void ጻፍ_ወደብ_ባይት(int 포트번호, int እሴት);

    void 중앙처리장치멈춤();
}

