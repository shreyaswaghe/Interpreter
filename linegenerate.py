def line_generate(filename='file.txt'):
        for line in open(f'./{filename}'):
            yield line
