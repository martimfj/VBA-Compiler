Sub main()
    ' bool ops
    Dim bt as boolean
    Dim bf as boolean
    bt = True
    bf = False

    print bf and bt
    print bf or bt
    print not(not(bf))
    print not((bt and bf) or bf)
end sub