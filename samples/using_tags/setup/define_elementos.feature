@setup
Funcionalidade: Definir o mapeamento dos elementos da interface

  Cenário: Definir os elementos da tela de busca
    Dado que quero definir os elementos da tela de busca
    Então a URL é https://www.google.com/
    E os elementos são
      | elemento                  | método | identificação                                |
      | barra de busca por xpath  | xpath  | //*[@id="lst-ib"]                            |
      | barra de busca por nome   | nome   | q                                            |
      | barra de busca por id     | id     | lsb-ib                                       |
      | barra de busca por classe | classe | gsfi                                         |
      | botão de pesquisa         | xpath  | //*[@id="tsf"]/div[2]/div[3]/center/input[1] |
