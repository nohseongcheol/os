// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Հայաստան.JArmOS.խզում;

import java.util.Arrays;

/** IDT의 Java 관리 측 처리기 등록과 분배를 담당한다. */
public final class խզում_կառավարիչ {
    private final 개입중단처리기[] 처리기들 = new 개입중단처리기[256];
    private boolean գործուն;

    public void գրանցվել_մուտքագրում(int դասիչ, 개입중단처리기 처리기) {
        번호확인(դասիչ);
        처리기들[դասիչ] = 처리기;
    }

    public void արձակել_Պահեստ(int դասիչ) {
        번호확인(դասիչ);
        처리기들[դասիչ] = null;
    }

    public int տարածել_արժեք(int դասիչ, int 저장된쌓임주소) {
        번호확인(դասիչ);
        if (!գործուն) {
            return 저장된쌓임주소;
        }
        개입중단처리기 처리기 = 처리기들[դասիչ];
        return 처리기 == null ? 저장된쌓임주소 : 처리기.Ընթացք_արժեք_մուտքագրում(저장된쌓임주소);
    }

    public void միացնել() {
        գործուն = true;
    }

    public void ապագործունացնել() {
        գործուն = false;
    }

    public boolean 활성인가() {
        return գործուն;
    }

    public void 모두해제() {
        Arrays.fill(처리기들, null);
    }

    private void 번호확인(int դասիչ) {
        if (դասիչ < 0 || դասիչ >= 처리기들.length) {
            throw new IllegalArgumentException("խզում 번호가 올바르지 않습니다.");
        }
    }
}

