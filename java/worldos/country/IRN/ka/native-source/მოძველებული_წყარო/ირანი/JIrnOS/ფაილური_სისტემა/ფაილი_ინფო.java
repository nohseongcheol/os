// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ირანი.JIrnOS.ფაილური_სისტემა;

public final class ფაილი_ინფო {
    private final int ზომა;
    private final int 형태;

    public ფაილი_ინფო(int ზომა, int 형태) {
        this.ზომა = ზომა;
        this.형태 = 형태;
    }

    public int ზომა() {
        return ზომა;
    }

    public int 형태() {
        return 형태;
    }
}

