// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 蒙古.JMngOS.宿主;

import 蒙古.JMngOS.内核.内核;

public final class 宿主启动 {
    private 宿主启动() {
    }

    public static void main(String[] 形参参数) {
        内核 内核值 = new 内核(new 宿主硬件());
        内核值.运行();
        内核值.执行步骤();
    }
}

