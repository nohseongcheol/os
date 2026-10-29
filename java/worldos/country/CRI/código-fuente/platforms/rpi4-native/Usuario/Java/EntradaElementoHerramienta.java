// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class EntradaElementoHerramienta {
    public static int ponerEnMarcha() {
        return Usuario.númeroHerramienta() == 0 ? CompiladorJava.ponerEnMarcha() : MáquinaVirtualJava.ponerEnMarcha();
    }
}
