// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ATA.JAtaOS.개입중단;

@FunctionalInterface
public interface 개입중단처리기 {
    int 처리(int 저장된쌓임주소);
}

