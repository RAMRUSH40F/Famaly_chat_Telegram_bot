import config
from SQLighter import SQLighter

class Poll:

    def get_name(self):
        return self._name

    def add_points_to_database(id, points, last_task):
        # Можно сделать рабочую with open|менеджер классов
        db = SQLighter('scores.db')
        db.up_score(id, points, last_task)
        db.close()

    def process_new_poll_answer(self, poll):
        # Waiting for an update, using dictionaries except of if/else brunch
        answer = poll.option_ids[0]

        if answer == 0:
            self.num_votes_yes += 1
        elif answer == 1:
            self.num_votes_no += 1
        elif answer == 2:
            self.num_votes_middle += 1

        self.check_end()

    def check_end(self):

        votes_num = self.num_votes_yes + self.num_votes_no + self.num_votes_middle
        texts = {0:'Последнее голосование завершено, большинство согласно 😁', 1:'Последнее голосование завершено, большинство не согласно 🤓',2:'Последнее голосование завершено, Не все согласны. Половоина баллов за уборку зачислено 🥴 '}

        if self.num_votes_yes >= config.poll_min_number:
            self.bot.send_message(self.room_id, texts[0])
            self.add_points_to_database(self._sender_id, self.POINTS, self.message.text)

        elif self.num_votes_yes <= config.poll_min_number -1 :

            self.bot.send_message(self.room_id, texts[1])

        elif self.num_votes_yes >= config.poll_min_number - 2 and votes_num >= self.min_number:

            self.bot.send_message(self.room_id, texts[2])

            self.add_points_to_database(self.POINTS, self._sender_id, self.message.text)
        else:
            pass

    def __init__(self, message, bot_object):

        self.min_number = config.poll_min_number
        self.room_id = int(config.family_chat_id)
        self._name = message.json[ 'from' ][ 'first_name' ]
        self._sender_id = str(message.from_user.id)
        self.bot = bot_object

        self.num_votes_yes = 0
        self.num_votes_no = 0
        self.num_votes_middle = 0

        self.message = message

        self.POINTS, self.HALF_POINTS = 100, 50


    def send_poll(self):
            self.poll = self.bot.send_poll(self.room_id, f'Убрал ли {self.get_name()} комнату {self.message.text}?',
                                      [ f'Да (+{self.POINTS}б)', 'Нет(0б.)', f'50/50 (+{self.HALF_POINTS}б.)' ], is_anonymous=False, type='regular',
                                      disable_notification=True)




