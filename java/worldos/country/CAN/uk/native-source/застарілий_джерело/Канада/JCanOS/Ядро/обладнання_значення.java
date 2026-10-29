// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Канада.JCanOS.Ядро;

/** Java 관리 커널과 CPU 고유 код_значення 사이의 유일한 경계다. */
public interface обладнання_значення {
    void 직렬출력(String Вміст_значення);

    int 포트바이트읽기(int обладнання_номер_порту);

    void записування_порт_байт(int обладнання_номер_порту, int значення);

    void 중앙처리장치멈춤();
}

