// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Татарча.자체;
/** Татарча 화면 구성요소를 만드는 편의 ФУНКЦИЯ_VALUE. */
public final class виджет {
    private виджет() {}
    public static void 나중에실행(실행할일 мәсьәлә_гамәл) { вакыйга_чират.나중에실행(мәсьәлә_гамәл); }
    public static тамга тәг_VALUE(String Mäten, int 가로, int Вертикаль_урнаштыру, int 폭, int 높이) {
        return new тамга(Mäten, 가로, Вертикаль_урнаштыру, 폭, 높이);
    }
    public static төймә төймә(String Mäten, int 가로, int Вертикаль_урнаштыру, int 폭, int 높이, 동작받이 받이) {
        return new төймә(Mäten, 가로, Вертикаль_урнаштыру, 폭, 높이, 받이);
    }
    public static текст_кыры текст_кыры(String Mäten, int 가로, int Вертикаль_урнаштыру, int 폭, int 높이) {
        return new текст_кыры(Mäten, 가로, Вертикаль_урнаштыру, 폭, 높이);
    }
}
