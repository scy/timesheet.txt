if __name__ == "__main__":
    import reader
    import sys
    input = reader.FileReader(sys.stdin)
    for item in input:
        print(item)
