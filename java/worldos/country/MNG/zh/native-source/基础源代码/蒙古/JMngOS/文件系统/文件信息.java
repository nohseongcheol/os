// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 蒙古.JMngOS.文件系统;

public final class 文件信息 {
    private final int 大小;
    private final int 形状种类;

    public 文件信息(int 大小, int 形状种类) {
        this.大小 = 大小;
        this.形状种类 = 形状种类;
    }

    public int 大小() {
        return 大小;
    }

    public int 形状种类() {
        return 形状种类;
    }
}

