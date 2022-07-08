import config
from SQLighter import SQLighter
import json
import collections

class Poll:

    def get_name(self):
        return self._name

    def add_points_to_database(id, points, last_task):
        # Можно сделать рабочую with open|менеджер классов
        db = SQLighter('scores.db')
        db.up_score(id, points, last_task)
        db.close()

    @staticmethod
    def process_new_poll_answer(poll_answer_info):

        new_answer = poll_answer_info.option_ids
        user_id = poll_answer_info.user.id

        try:
            polls_stats = Poll.get_stats_from_json()
        except FileNotFoundError :
            polls_stats = {}

        polls_stats[user_id] = new_answer

        if Poll.check_end(polls_stats):
            polls_stats = {}

        Poll.save_stats_to_json(polls_stats)


    @staticmethod
    def save_stats_to_json(new_info):
        with open('Poll_info.json', 'w') as json_file:
            json.dump(new_info, json_file)

    @staticmethod
    def get_stats_from_json():
        with open('Poll_info.json','r') as json_file:
            info = json.load(json_file)
            return info

    @staticmethod
    def check_end(self, polls_stats):

        options = []
        for i in polls_stats.values():
            options.extend(i)

        votes_num = len(options)
        votes_for = collections.Counter(options)[0]
        votes_againts = collections.Counter(options)[1]

        texts = {0:'Последнее голосование завершено, большинство согласно 😁', 1:'Последнее голосование завершено, большинство не согласно 🤓', 2:'Последнее голосование завершено, Не все согласны. Половоина баллов за уборку зачислено 🥴 '}


        if votes_for >= config.poll_min_number:
            self.bot.send_message(self.room_id, texts[0])
            self.add_points_to_database(self._sender_id, self.POINTS, self.message.text)
            return True

        elif votes_againts >= config.poll_min_number//2 :
            self.bot.send_message(self.room_id, texts[1])
            return True

        elif votes_num >= config.poll_min_number:
            self.bot.send_message(self.room_id, texts[2])
            self.add_points_to_database(self.POINTS, self._sender_id, self.message.text)
            return True
        else:
            return False

    def __init__(self, message, bot_object):


        self.room_id = int(config.family_chat_id)
        self._name = message.json['from']['first_name']
        self._sender_id = str(message.from_user.id)
        self.bot = bot_object

        self.message = message

        self.POINTS, self.HALF_POINTS = 100, 50

    def send_poll(self):

        try:
            polls_stats = Poll.get_stats_from_json()
        except FileNotFoundError :
            polls_stats = {}

        if not self.check_end(polls_stats):
            self.bot.send_poll(self.room_id, f'Убрал ли {self.get_name()} комнату {self.message.text}?',
                                      [ f'Да (+{self.POINTS}б)', 'Нет(0б.)', f'50/50 (+{self.HALF_POINTS}б.)' ], is_anonymous=False, type='regular',
                                      disable_notification=True)





