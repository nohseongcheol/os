// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class ToolEntry {
    public static int run() {
        return User.toolNumber() == 0 ? JavaCompiler.run() : JavaMachine.run();
    }
}
