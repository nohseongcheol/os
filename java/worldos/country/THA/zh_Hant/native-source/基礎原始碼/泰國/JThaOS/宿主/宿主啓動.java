// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 泰國.JThaOS.宿主;

import 泰國.JThaOS.內核.內核;

public final class 宿主啓動 {
    private 宿主啓動() {
    }

    public static void main(String[] 形式參數實際參數) {
        內核 內核值 = new 內核(new 宿主硬件());
        內核值.運行();
        內核值.執行步驟();
    }
}

