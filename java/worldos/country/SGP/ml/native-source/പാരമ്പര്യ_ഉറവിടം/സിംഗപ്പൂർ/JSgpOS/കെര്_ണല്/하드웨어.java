// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package സിംഗപ്പൂർ.JSgpOS.കെര്_ണല്;

/** Java 관리 커널과 CPU 고유 കോഡ്_മൂല്യം 사이의 유일한 경계다. */
public interface 하드웨어 {
    void 직렬출력(String ഉള്ളടക്കം_മൂല്യം);

    int 포트바이트읽기(int 포트번호);

    void റൈറ്റ്_ചെയ്യുക_പോര്_ട്ട്_బైట్(int 포트번호, int മൂല്യം);

    void 중앙처리장치멈춤();
}

