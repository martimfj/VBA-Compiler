Sub main()
    Dim teste_bool as boolean
    Dim teste_int as integer
    teste_bool = True
    teste_int = 10

    if teste_bool then
        print teste_int + 10
    end if

    while (teste_int > 0) and teste_bool = True
        print teste_int
        teste_int = teste_int - 1
    wend

    teste_int = 10
    print teste_int

End Sub