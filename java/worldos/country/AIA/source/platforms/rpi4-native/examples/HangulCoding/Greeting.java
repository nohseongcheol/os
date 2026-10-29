// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public class Greeting {
    static int addValues(int firstOrdinal, int secondOrdinal) { return firstOrdinal + secondOrdinal; }
    public static void main(String[] arguments) {
        int totalValue = addValues(20, 22);
        System.out.println("안녕하세요 · totalValue=" + totalValue);
    }
}
