// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package New_Zealand.JNzlOS.interrupt;

@FunctionalInterface
public interface InterruptHandler {
    int processValueEntry(int savedStackAddress);
}

