// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package বাংলা.নিজ;

/** 한국어로 ঘোষণা·던지기·잡기를 할 수 있는 থ্রেড_অবস্হা_ব্যতিক্রম. */
public class থ্রেড_অবস্হা_ব্যতিক্রম extends java.lang.IllegalThreadStateException {
    public থ্রেড_অবস্হা_ব্যতিক্রম() { super(); }
    public থ্রেড_অবস্হা_ব্যতিক্রম(String 설명) { super(설명); }
    public String 설명() { return getMessage(); }
}
