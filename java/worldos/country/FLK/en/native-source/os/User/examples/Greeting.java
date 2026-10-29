// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class Greeting {
    public static int run() {
        User.write("Hello from a separate Java ELF!\n");
        User.write(User.executionPermission() == 3 ? "USER MODE ring 3\n" : "WRONG PRIVILEGE\n");
        for (int index = 0; index < User.argumentsCount(); index++) {
            User.write("arg: "); User.write(User.arguments(index)); User.write("\n");
        }
        return User.executionPermission() == 3 ? 0 : 1;
    }
}
