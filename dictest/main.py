# -*- coding: utf-8 -*-

import random
import json
import config
import os

__author__ = "dsm_helper"
data_path = "../data"

def get_quiz_data_from_input():
    return input("請輸入要測驗的題庫(0) >> ")


def get_words_by_info(file_name):
    try:
        with open(f'{data_path}/{file_name}', 'r', encoding="UTF8") as f:
            words = json.load(f)
        return words
    except Exception as e:
        print("輸入錯誤，請重新確認。")
        print(e)
        exit(1)

def get_data_list():
    # 只取json檔案
    data_list = [f for f in os.listdir(data_path) if f.endswith('.json')]
    return data_list

def show_data_list(data_list):
    print("選擇要測驗的題庫")
    for i, filename in enumerate(data_list):
        print(f"{i}: {filename}")

if __name__ == "__main__":
    data_list = get_data_list()
    show_data_list(data_list)
    index = int(input("請輸入要測驗的題庫編號 >> "))

    check = True
    count = 0
    words = get_words_by_info(data_list[index])

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
            print(answer[0],'_'*len(answer), answer[-1])

        question = input("Ans >> ")

        if question == answer:
            check = True
            count = 0
            words.pop(answer)
            print(config.CORRECT_MESSAGE.format(count=len(words)))
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
            check = True

        if question == "exit":
            finish_quiz()

    print(config.END_MESSAGE)
