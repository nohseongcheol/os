// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package युगांडा.JUgaOS.फ़ाइल_सिस्टम;

public final class फ़ाइल_जानकारी {
    private final int आकार;
    private final int 형태;

    public फ़ाइल_जानकारी(int आकार, int 형태) {
        this.आकार = आकार;
        this.형태 = 형태;
    }

    public int आकार() {
        return आकार;
    }

    public int 형태() {
        return 형태;
    }
}

