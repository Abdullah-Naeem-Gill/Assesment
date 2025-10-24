def most_frequent_char(s: str):
    char_count = {}
    for char in s:
        char_count[char] = char_count.get(char, 0) + 1

    max_count = max(char_count.values())

    for char in s:
        if char_count[char] == max_count:
            return char

if __name__ == "__main__":
    print(most_frequent_char("abdullah naeem gill"))
    print(most_frequent_char("aabbdd"))