// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package British_Virgin_Islands.JVgbOS.interrupt;

@FunctionalInterface
public interface InterruptHandler {
    int processValueEntry(int savedStackAddress);
}

