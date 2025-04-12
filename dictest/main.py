# -*- coding: utf-8 -*-

import random
import json
import config
import os
from dotenv import load_dotenv
from quiz_history import (
    update_history,
    select_words_based_on_history,
    check_all_words_mastered,
)

# 載入環境變數
load_dotenv()

DATA_PATH = os.getenv("DATA_PATH", "../data")
MAX_QUESTIONS = int(os.getenv("MAX_QUESTIONS", 5))


def get_words_by_info(file_name):
    try:
        with open(f"{DATA_PATH}/{file_name}", "r", encoding="UTF8") as f:
            words = json.load(f)
        return words
    except Exception as e:
        print("輸入錯誤，請重新確認。")
        print(e)
        exit(1)


def get_data_list():
    # 只取json檔案
    data_list = [f for f in os.listdir(DATA_PATH) if f.endswith(".json")]
    return data_list


def show_data_list(data_list):
    print("選擇要測驗的題庫")
    for i, filename in enumerate(data_list):
        print(f"{i}: {filename}")


if __name__ == "__main__":
    data_list = get_data_list()
    show_data_list(data_list)
    index = int(input("請輸入要測驗的題庫編號 >> ", "0"))
    quiz_name = data_list[index]

    check = True
    count = 0
    all_words = get_words_by_info(quiz_name)
    words = select_words_based_on_history(all_words, quiz_name)
    total_questions = len(words)
    skipped_questions = []
    correct_words = []
    failed_words = []

    def finish_quiz():
        print(config.EXIT_MESSAGE)
        exit(1)

    while True:
        if len(words) == 0:
            break

        if check:
            answer, meaning = random.choice(list(words.items()))
            check = False
            print(meaning)
            # 顯示頭尾
            print(answer[0], "_" * (len(answer) - 2), answer[-1])

        question = input("Ans >> ")

        if question == answer:
            check = True
            count = 0
            words.pop(answer)
            correct_words.append(answer)
            print(config.CORRECT_MESSAGE.format(count=len(words)))
        elif question == "next":
            print(f"放棄此題，答案是：{answer}")
            skipped_questions.append((answer, meaning))
            words.pop(answer)
            check = True
            count = 0
        elif question != answer:
            print(config.TRY_AGAIN_MESSAGE)
            count += 1

        if count == 5:
            print(config.FIRST_CHARACTER_HINT.format(answer=answer))
        if count == 7:
            print(config.LENGTH_HINT.format(answer=answer))
        if count == 10:
            print(config.FAILED_MESSAGE.format(answer=answer))
            words.pop(answer)
            failed_words.append(answer)
            check = True

        if question == "exit":
            finish_quiz()

    print(config.END_MESSAGE)
    print(f"本次測驗共 {total_questions} 題，答對 {len(correct_words)} 題。")
    if skipped_questions:
        print("\n放棄的題目：")
        for word, meaning in skipped_questions:
            print(f"{word}: {meaning}")

    # 更新測驗歷史
    update_history(
        quiz_name, correct_words, [w[0] for w in skipped_questions], failed_words
    )

    # 檢查是否所有題目都曾經答對過
    if check_all_words_mastered(quiz_name, all_words):
        print("\n恭喜！你已經完全掌握這個題庫的所有單字了！🎉")
