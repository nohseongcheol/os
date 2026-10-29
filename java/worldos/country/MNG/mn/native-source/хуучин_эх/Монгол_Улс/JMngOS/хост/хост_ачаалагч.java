// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Монгол_Улс.JMngOS.хост;

import Монгол_Улс.JMngOS.кернел.кернел;

public final class хост_ачаалагч {
    private хост_ачаалагч() {
    }

    public static void main(String[] 인자) {
        кернел кернел_утга = new кернел(new 호스트하드웨어());
        кернел_утга.Ажиллуулах();
        кернел_утга.한단계실행();
    }
}

