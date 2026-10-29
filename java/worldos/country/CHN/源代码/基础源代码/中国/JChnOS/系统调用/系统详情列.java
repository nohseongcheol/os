// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 中国.JChnOS.系统调用;

public final class 系统详情列 {
    private final String 系统名称;
    private final String 节点名称;
    private final String 版本版次值;
    private final String 版本值;
    private final String 计算机;

    public 系统详情列(String 系统名称, String 节点名称, String 版本版次值, String 版本值, String 计算机) {
        this.系统名称 = 系统名称;
        this.节点名称 = 节点名称;
        this.版本版次值 = 版本版次值;
        this.版本值 = 版本值;
        this.计算机 = 计算机;
    }

    public String 系统名称() { return 系统名称; }
    public String 节点名称() { return 节点名称; }
    public String 版本版次值() { return 版本版次值; }
    public String 版本值() { return 版本值; }
    public String 计算机() { return 计算机; }
}
