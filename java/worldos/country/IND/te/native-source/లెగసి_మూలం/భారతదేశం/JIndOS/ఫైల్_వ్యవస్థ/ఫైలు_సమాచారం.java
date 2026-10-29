// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package భారతదేశం.JIndOS.ఫైల్_వ్యవస్థ;

public final class ఫైలు_సమాచారం {
    private final int పరిమాణం;
    private final int 형태;

    public ఫైలు_సమాచారం(int పరిమాణం, int 형태) {
        this.పరిమాణం = పరిమాణం;
        this.형태 = 형태;
    }

    public int పరిమాణం() {
        return పరిమాణం;
    }

    public int 형태() {
        return 형태;
    }
}

