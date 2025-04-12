import json
import os
import random
from datetime import datetime
from dotenv import load_dotenv

# 載入環境變數
load_dotenv()

HISTORY_PATH = os.getenv('HISTORY_PATH', 'quiz_history.json')

def select_random_questions(words, count=None):
    if count is None:
        count = int(os.getenv('MAX_QUESTIONS', 5))
    if len(words) <= count:
        return words
    selected_words = {}
    word_list = list(words.items())
    random.shuffle(word_list)
    for word, meaning in word_list[:count]:
        selected_words[word] = meaning
    return selected_words

def load_history():
    if not os.path.exists(HISTORY_PATH):
        return {}
    try:
        with open(HISTORY_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return {}

def save_history(history):
    with open(HISTORY_PATH, 'w', encoding='utf-8') as f:
        json.dump(history, f, ensure_ascii=False, indent=2)

def update_history(quiz_name, correct_words, skipped_words, failed_words):
    history = load_history()
    
    if quiz_name not in history:
        history[quiz_name] = {
            "total_attempts": 0,
            "words": {}
        }
    
    quiz_data = history[quiz_name]
    quiz_data["total_attempts"] += 1
    
    # 更新單字記錄
    for word in correct_words:
        if word not in quiz_data["words"]:
            quiz_data["words"][word] = {"correct": 0, "wrong": 0, "skipped": 0}
        quiz_data["words"][word]["correct"] += 1
    
    for word in skipped_words:
        if word not in quiz_data["words"]:
            quiz_data["words"][word] = {"correct": 0, "wrong": 0, "skipped": 0}
        quiz_data["words"][word]["skipped"] += 1
    
    for word in failed_words:
        if word not in quiz_data["words"]:
            quiz_data["words"][word] = {"correct": 0, "wrong": 0, "skipped": 0}
        quiz_data["words"][word]["wrong"] += 1
    
    save_history(history)

def get_word_difficulty(word_data):
    total = word_data["correct"] + word_data["wrong"] + word_data["skipped"]
    if total == 0:
        return 0
    return (word_data["wrong"] + word_data["skipped"]) / total

def select_words_based_on_history(words, quiz_name, count=None):
    if count is None:
        count = int(os.getenv('MAX_QUESTIONS', 5))
    history = load_history()
    
    if quiz_name not in history:
        return select_random_questions(words, count)
    
    quiz_data = history[quiz_name]
    word_difficulties = {}
    
    for word, meaning in words.items():
        if word in quiz_data["words"]:
            word_difficulties[word] = get_word_difficulty(quiz_data["words"][word])
        else:
            word_difficulties[word] = 0.5  # 新單字預設難度
    
    # 根據難度排序並選擇最難的單字
    sorted_words = sorted(word_difficulties.items(), key=lambda x: x[1], reverse=True)
    selected_words = {}
    
    for word, _ in sorted_words[:count]:
        selected_words[word] = words[word]
    
    return selected_words

def check_all_words_mastered(quiz_name, all_words):
    history = load_history()
    if quiz_name not in history:
        return False
    
    quiz_data = history[quiz_name]
    for word in all_words:
        if word not in quiz_data["words"] or quiz_data["words"][word]["correct"] == 0:
            return False
    return True 