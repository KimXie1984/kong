import string
import uuid
import random
from datetime import datetime, timedelta
import time


class RandomUtil:

    @staticmethod
    def true_or_false():
        return random.choice([True, False])

    @staticmethod
    def _uuid():
        return uuid.uuid1()

    @staticmethod
    def str_uuid():
        return str(RandomUtil._uuid())

    @staticmethod
    def string(length=10):
        return ''.join(random.choice(string.ascii_letters) for _ in range(length))

    @staticmethod
    def str_double(x=5, y=5):
        return f"{RandomUtil.str_number(x)}.{RandomUtil.str_number(y)}"

    @staticmethod
    def str_number(length=3):
        return str(random.randint(1, 9)) + ''.join(str(random.randint(0, 9)) for _ in range(length - 1))

    @staticmethod
    def integer(start, end=None):
        end = end or start * 10 - 1
        return random.randint(start, end)

    @staticmethod
    def timestamp():
        end_time = datetime.now() + timedelta(days=365)
        start_time = datetime.now() + timedelta(days=-3650)
        timestamp = random.randint(int(time.mktime(start_time.timetuple())), int(time.mktime(end_time.timetuple())))
        return timestamp

    @staticmethod
    def str_datetime():
        """
        literal_value: "2021-07-01T11:07:00+08:00"
        """
        # todo(zxu): fixed timezone
        return datetime.fromtimestamp(RandomUtil.timestamp()).strftime("%Y-%m-%dT%H:%M:%S+08:00")

    @staticmethod
    def str_date():
        """
        literal_value: "2021-07-01"
        """
        # todo(zxu): fixed timezone
        return datetime.fromtimestamp(RandomUtil.timestamp()).strftime("%Y-%m-%d")

    @staticmethod
    def partial_date():
        """
        literal_value: "0000-07-01"
        """
        date_string = RandomUtil.str_date()
        if RandomUtil.true_or_false():
            date_string = '0000' + date_string[4:]
        if RandomUtil.true_or_false():
            date_string = date_string[:5] + '00' + date_string[7:]
        if RandomUtil.true_or_false():
            date_string = date_string[:8] + '00'
        return date_string

    @staticmethod
    def partial_time():
        """
        literal_value: "00:07:00"
        """
        # index of replacement
        start_position = [0, 3, 6]
        selected_start_position = random.choice(start_position)
        full_time = datetime.fromtimestamp(RandomUtil.timestamp()).strftime("%H:%M:%S")
        # replace 2 chars started from index
        return full_time[:selected_start_position] + '00' + full_time[selected_start_position + 2:]

    @staticmethod
    def str_time():
        """
        literal_value: "11:07:00"
        """
        # todo(zxu): fixed timezone
        return datetime.fromtimestamp(RandomUtil.timestamp()).strftime("%H:%M:%S")

    @staticmethod
    def str_printable(length: int = 10):
        return ''.join(random.choice(string.printable) for _ in range(length))

    @staticmethod
    def str_punctuation(length: int = 10):
        return ''.join(random.choice(string.punctuation) for _ in range(length))

    @staticmethod
    def i18ntext_dict(length: int = 10):
        _string = RandomUtil.string(length=length)
        return dict(en_us=_string, zh_cn=f"{_string}中")

    @staticmethod
    def test_tag(prefix='AutoTest', conjunction='_'):
        return conjunction.join(
            [prefix,
             datetime.now().strftime("%Y%m%d%H%M%S"),
             "".join(random.choices(string.ascii_letters, k=5))])


if __name__ == "__main__":
    print(RandomUtil.partial_date())
