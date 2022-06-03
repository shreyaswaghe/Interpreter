if __name__=='__main__':
    import tokenise, linegenerate
    for __ in tokenise.tokeniser(linegenerate.line_generate()):
        print(__)