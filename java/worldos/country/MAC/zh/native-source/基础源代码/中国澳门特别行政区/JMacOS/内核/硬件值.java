// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 中国澳门特别行政区.JMacOS.内核;

/** Java 管理内核与 CPU 专用代码之间的唯一边界。 */
public interface 硬件值 {
    void 串行输出(String 内容值);

    int 读取端口字节(int 硬件端口编号);

    void 写入端口字节(int 硬件端口编号, int 值);

    void 停机CPU();
}

