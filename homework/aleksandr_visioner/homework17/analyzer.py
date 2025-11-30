import argparse
import os
import re
from colorama import init, Fore, Style

init(autoreset=True)


def parse_arguments():
    parser = argparse.ArgumentParser(description='Анализатор логов')
    parser.add_argument('log_path', help='Полный путь к папке с логами')
    parser.add_argument('--text', required=True,
                        help='Текст для поиска в логах')
    return parser.parse_args()


def get_log_files(path):
    if os.path.isfile(path) and path.endswith('.log'):
        return [path]
    elif os.path.isdir(path):
        log_files = []
        for f in os.listdir(path):
            if f.endswith('.log') and os.path.isfile(os.path.join(path, f)):
                log_files.append(os.path.join(path, f))
        return log_files
    else:
        print(
            f"{Fore.RED}Ошибка: Проверь путь!: {path}")
        return []


def parse_log_blocks(content):
    blocks = {}
    # Паттерн: 2022-02-03 00:01:13.623
    log_start_pattern = re.compile(
        r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{3})')

    lines = content.split('\n')
    current_time = None
    current_block = []

    for line in lines:
        time_match = log_start_pattern.match(line)
        if time_match:
            if current_time and current_block:
                blocks[current_time] = '\n'.join(current_block)
            current_time = time_match.group(1)
            current_block = [line]
        elif current_time:
            current_block.append(line)

    if current_time and current_block:
        blocks[current_time] = '\n'.join(current_block)

    return blocks


def get_context(text, pos, search_len):
    words_count = 0

    i = pos - 1
    while i >= 0 and words_count < 5:
        if text[i].isspace() and (i == 0 or not text[i - 1].isspace()):
            words_count += 1
        i -= 1

    start_boundary = max(0, i + 1)

    words_count = 0
    i = pos + search_len
    text_length = len(text)

    while i < text_length and words_count < 5:
        if text[i].isspace() and (
                i == text_length - 1 or not text[i + 1].isspace()):
            words_count += 1
        i += 1

    end_boundary = min(text_length, i)

    context = text[start_boundary:end_boundary].strip()

    marked_pos = pos - start_boundary
    marked_context = (context[:marked_pos] +
                      f"{Fore.RED}{Style.BRIGHT}"
                      f"{text[pos:pos + search_len]}{Style.RESET_ALL}" +
                      context[marked_pos + search_len:])

    return marked_context


def find_text_in_logs(log_path, search_text):
    log_files = get_log_files(log_path)

    if not log_files:
        return

    found_any = False

    for file_path in log_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
        except Exception as e:
            print(f"{Fore.RED}Ошибка чтения файла {file_path}: {e}")
            continue

        blocks = parse_log_blocks(content)

        for time, block in blocks.items():
            if search_text in block:
                start_index = 0
                while True:
                    pos = block.find(search_text, start_index)
                    if pos == -1:
                        break

                    context = get_context(block, pos, len(search_text))

                    filename = os.path.basename(file_path)
                    print(f"{Fore.CYAN}{'=' * 80}")
                    print(f"{Fore.GREEN}Файл: {filename}")
                    print(f"{Fore.YELLOW}Время ошибки: {time}")
                    print(f"{Fore.WHITE}Текст: {context}")
                    print(f"{Fore.CYAN}{'=' * 80}")

                    start_index = pos + 1
                    found_any = True

        if not found_any:
            print(
                f"{Fore.YELLOW}Текст '{search_text}' не найдено совпадений. "
                f"{file_path}")


def main():
    args = parse_arguments()

    find_text_in_logs(args.log_path, args.text)


if __name__ == "__main__":
    main()
