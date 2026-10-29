// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class testNetworking {
    public static int run() {
        int firstOrdinal = User.openNetwork(45000);
        if (firstOrdinal < 0) { User.write("NETWORK UNAVAILABLE\n"); return 3; }
        int[] data = new int[8];
        boolean passValue = User.openNetwork(45000) == -98
            && User.receiveData(firstOrdinal, data, 0) == -11
            && User.receiveData(firstOrdinal, data, 50) == -110
            && User.receiveData(firstOrdinal, data, 3000) == -22
            && User.sendData(firstOrdinal, 0x0a000202, 9, data, 9) == -90
            && User.receiveData(firstOrdinal, null, 0) == -14
            && User.closeNetwork(firstOrdinal) == 0 && User.closeNetwork(firstOrdinal) == -9;
        User.write(passValue ? "UDP API CHECK PASS\n" : "UDP API CHECK FAIL\n");
        return passValue ? 0 : 1;
    }
}
