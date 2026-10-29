// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package বাংলা.নিজ;

/** 한국어로 ঘোষণা·던지기·잡기를 할 수 있는 অবৈধ_যুক্তি_ব্যতিক্রম. */
public class অবৈধ_যুক্তি_ব্যতিক্রম extends java.lang.IllegalArgumentException {
    public অবৈধ_যুক্তি_ব্যতিক্রম() { super(); }
    public অবৈধ_যুক্তি_ব্যতিক্রম(String 설명) { super(설명); }
    public String 설명() { return getMessage(); }
}
