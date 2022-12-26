from transitions.extensions import GraphMachine

from utils import send_text_message, send_rock_paper_scissors, send_menu, send_guess_number, send_random_generator, send_edit_list, send_fsm_image
import random
import time


class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)
        self.success = 0
        self.fail = 0
        self.total_count = 0
        self.best_count = 0
        self.total_time = 0
        self.best_time = 0
        self.option = 0
        self.guess = []
        self.list = []

    def is_going_rock_paper_scissors(self, event):
        text = event.message.text
        if text == "猜拳":
            self.rock_paper_scissors_enter = True
            return True
        else:
            return False
    
    def is_playing_rock_paper_scissors(self, event):
        self.rock_paper_scissors_enter = False
        text = event.message.text
        if text == "林北不玩了": return False
        if text == "剪刀": self.player = 0
        elif text == "石頭": self.player = 1
        elif text == "布": self.player = 2
        else: self.player = -1
        return True

    # def is_leaving_rock_paper_scissors(self, event):
    #     text = event.message.text
    #     return text == "林北不玩了"

    def is_leaving(self, event):
        text = event.message.text
        reply_token = event.reply_token
        if text == "林北不玩了":
            send_menu(event.reply_token, "要不要再試試其他功能?")
            return True
        return False

    def is_going_guess_number(self, event):
        text = event.message.text
        if text == "猜數字":
            self.result = -1
            self.number_enter = True
            return True
        else:
            return False

    def is_playing_guess_number(self, event):
        text = event.message.text
        self.invalid = 0
        self.count = 0
        if text == "讓我來猜你的數字":
            self.number_enter = True
            self.start = time.time()
            return True
        return False

    def is_in_guess_number_menu(self, event):
        text = event.message.text
        if text == "林北不玩了": return False
        elif text == "讓我來猜你的數字": return False
        elif text == "我表現得如何":
            self.result = 2
            return True
        self.result = -2
        return True

    def is_guessing_number(self, event):
        self.number_enter = False
        text = event.message.text
        if text != '放棄':
            if text.isdigit():
                guess = int(text)
                if float(text) != guess:
                    self.invalid = 1
                    return True
                elif len(text) != 4:
                    self.invalid = 2
                    return True
                else:
                    self.guess.clear()
                    self.guess.append((int)(guess / 1000))
                    self.guess.append((int)((guess - self.guess[0] * 1000) / 100))
                    self.guess.append((int)((guess - self.guess[0] * 1000 - self.guess[1] * 100) / 10))
                    self.guess.append((int)(guess - self.guess[0] * 1000 - self.guess[1] * 100 - self.guess[2] * 10))
                    print(self.guess)
                    self.count += 1
                    if self.guess != self.number:
                        return True 
                    return False
            else:
                self.invalid = 1
                return True
        return False

    def leave_guessing_number(self, event):
        text = event.message.text
        if text == "放棄": 
            self.end = time.time()
            self.result = 0
            self.fail += 1
            return True
        if self.guess == self.number:
            self.end = time.time()
            self.result = 1
            self.success += 1
            self.time = self.end - self.start
            self.total_count += self.count
            self.total_time += self.time
            if self.best_count == 0 or self.count < self.best_count:
                self.best_count = self.count
            if self.best_time == 0 or self.time < self.best_time:
                self.best_time = self.time
            return True
        return False

    def is_going_random_generator(self, event):
        text = event.message.text
        if text == "隨機產生器":
            self.random_enter = True
            return True
        else:
            return False

    def enter_editing_list(self, event):
        text = event.message.text
        self.watch = False
        if text == "編輯選項":
            self.edit_enter = True
            return True
        return False

    def is_editing_list(self, event):
        text = event.message.text
        self.edit_enter = False
        if text == "新增選項" or text == "刪除選項" or text == "結束":
            return False
        if text == "檢視選項":
            self.watch = True
        return True

    def enter_adding_list(self, event):
        text = event.message.text
        if text == "新增選項":
            self.add_enter = True
            return True
        return False

    def is_adding_list(self, event):
        text = event.message.text
        if text != "結束":
            self.add_enter = False
            self.list.append(text)
            return True
        return False

    def enter_removing_list(self, event):
        text = event.message.text
        if text == "刪除選項":
            self.remove_enter = True
            return True
        return False

    def is_removing_list(self, event):
        text = event.message.text
        if text == "清空":
            self.remove_enter = False
            self.remove_mode = 0
            self.list.clear()
            return True
        elif text != "結束":
            self.remove_enter = False
            if text in self.list:
                self.remove_mode = 1
                self.list.remove(text)
            else:
                self.remove_mode = 2
            return True
        return False
    
    def finish_edit(self, event):
        text = event.message.text
        if text == "結束":
            self.edit_enter = True
            return True
        return False

    def enter_generate(self, event):
        text = event.message.text
        if text == "開始產生":
            self.generate_enter = True
            return True
        return False

    def is_generating(self, event):
        text = event.message.text
        if (text != "結束"):
            self.generate_enter = False
            if text.isdigit():
                num = int(text)
                if num > 0 and num <= len(self.list):
                    self.error = 0
                    self.generate = random.sample(self.list, num)
                else:
                    self.error = 1
            else:
                self.error = -1
            return True
        return False

    def back_to_random_menu(self, event):
        text = event.message.text
        if text == "結束":
            self.option = 1
            return True
        return False

    def is_in_random_menu(self, event):
        text = event.message.text
        if text == "新增選項" or text == "刪除選項" or text == "林北不玩了" or text == "開始產生":
            return False
        self.option = 0
        if text == "檢視選項":
            self.option = 2
        return True

    def is_show_fsm(self, event):
        text = event.message.text
        if text == "聽話，讓我看看!":
            return True
        return False

    def on_enter_rock_paper_scissors(self, event):
        reply_token = event.reply_token
        array = ['剪刀', '石頭', '布']
        opponent = random.randint(0, 2)
        message = "來猜拳吧"
        if self.rock_paper_scissors_enter == False:
            if self.player == -1: 
                message = '認真玩好不好'             
            else:          
                if self.player == opponent: result = '我們平手'
                elif (self.player+1) % 3 == opponent: result = '你輸了'
                else: result = '你贏了'
                message = "我出"+array[opponent]+"，"+result
        send_rock_paper_scissors(reply_token, message)

    def on_enter_guess_number_menu(self, event):
        reply_token = event.reply_token
        if self.result == -2: message = "你在公三小"
        elif self.result == -1: message = "來猜數字吧"
        elif self.result == 0: message = "我剛剛的數字是"+str(self.number[0])+str(self.number[1])+str(self.number[2])+str(self.number[3])+",要不要再試一次?"
        elif self.result == 1: message = "恭喜你猜到我的數字，你總共猜了"+str(self.count)+"次，花了"+str(round(self.time, 2))+"秒"
        else: 
            success = str(self.success)+" 次"
            fail = str(self.fail)+" 次"
            if self.success == 0: average_count = "無"
            else: average_count = str(round(self.total_count/self.success, 2))+" 次"
            if self.success == 0: average_time = "無"
            else: average_time = str(round(self.total_time/self.success, 2))+" 秒"
            if self.best_count == 0: best_count = "無"
            else: best_count = str(self.best_count)+" 次"
            if self.best_time == 0: best_time = "無"
            else: best_time = str(round(self.best_time, 2))+" 秒"
            message = "成功猜出次數: "+success+"\n放棄次數: "+fail+"\n平均猜測次數: "+average_count+"\n平均猜測時間: "+average_time+"\n最佳猜測次數: "+best_count+"\n最佳猜測時間: "+best_time
        send_guess_number(reply_token, message)
                
    def on_enter_play_guess_number(self, event):
        reply_token = event.reply_token
        if self.number_enter == True:
            array = [i for i in range(10)]
            self.number = random.sample(array, 4)
            print(self.number)
            message = '我剛剛隨機產生了一個四位數，每個數字不重複。\n如果猜對一個數字且位置相同，則得1A。\n如果猜對一個數字，但是位置不同，則得1B。\n你可以接著輸入你要猜的數字，如果你放棄了也可以隨時輸入"放棄"。'            
        else:
            if self.invalid == 1:
                self.invalid = 0
                message = '輸入無效，請再試一次'
            elif self.invalid == 2:
                self.invalid = 0
                message = '你猜的數字不在有效範圍內'
            else:
                A = 0
                B = 0
                for i in range(4):
                    if self.number[i] in self.guess:
                        if self.guess.index(self.number[i]) == i:
                            A += 1
                        else:
                            B += 1
                message = str(A)+"A"+str(B)+"B" 
        send_text_message(reply_token, message)

    def on_enter_random_generator(self, event):
        reply_token = event.reply_token
        if self.random_enter == True: 
            self.random_enter = False
            message = "歡迎來到隨機產生器"
        elif self.option == 0:
            message = "你在公三小"
        elif self.option == 1:
            message = "接下來要做什麼呢?"
        else:
            self.option = 0
            if len(self.list) == 0:
                message = "選項是空的"
            else:
                message = ""
                for i in self.list:
                    message += i
                    if i != self.list[len(self.list) - 1]: message += "、"
        send_random_generator(reply_token, message)

    def on_enter_edit_list(self, event):
        reply_token = event.reply_token
        if self.edit_enter == True: message = '接下來要做什麼呢?'
        elif self.watch == False: 
            message = '你在公三小'
        else: 
            self.watch = False
            if len(self.list) == 0:
                message = "選項是空的"
            else:
                message = ""
                for i in self.list:
                    message += i
                    if i != self.list[len(self.list) - 1]: message += "、"
        send_edit_list(reply_token, message)

    def on_enter_add_list(self, event):
        reply_token = event.reply_token
        if self.add_enter == True: message = '你可以接著輸入你要新增的選項，或輸入"結束"回到上一頁'
        else: message = '新增成功'
        send_text_message(reply_token, message)

    def on_enter_remove_list(self, event):
        reply_token = event.reply_token
        if self.remove_enter == True: message = '你可以接著輸入你要刪除的選項，或輸入"清空"來清空選項，或輸入"結束"回到上一頁'
        elif self.remove_mode == 0: message = '清空成功'
        elif self.remove_mode == 1: message = '刪除成功'
        else: message = '選項不存在'
        send_text_message(reply_token, message)

    def on_enter_generate(self, event):
        reply_token = event.reply_token
        if self.generate_enter == True: message = '你可以接著輸入你要從選項中隨機產生的數量，或輸入"結束"回到上一頁'
        elif self.error == 1: message = '你輸入的數字不在合理範圍'
        elif self.error == -1: message = '你輸入的格式錯誤'
        else: 
            message = ""
            for i in self.generate:
                message += i
                if i != self.generate[len(self.generate) - 1]: message += "、"
        send_text_message(reply_token, message)
        
    def on_enter_fsm_image(self, event):
        reply_token = event.reply_token
        send_fsm_image(reply_token)
        self.go_back()
