// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 인사 {
    public static int Εκτέλεση_2() {
        χρήστης.Εγγραφή("Hello from a separate Java ELF!\n");
        χρήστης.Εγγραφή(χρήστης.εκτέλεση_άδεια() == 3 ? "USER MODE ring 3\n" : "WRONG PRIVILEGE\n");
        for (int Ευρετήριο = 0; Ευρετήριο < χρήστης.인수개수(); Ευρετήριο++) {
            χρήστης.Εγγραφή("arg: "); χρήστης.Εγγραφή(χρήστης.Παράμετροι(Ευρετήριο)); χρήστης.Εγγραφή("\n");
        }
        return χρήστης.εκτέλεση_άδεια() == 3 ? 0 : 1;
    }
}
