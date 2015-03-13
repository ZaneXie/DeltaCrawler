__author__ = 'xiezj'
from DeltaCrawler import DeltaCrawler
import lib.threadpool
import copy
from User import User
from lib.progressbar import ProgressBar, Percentage, Bar


progress_bar = None
user_left = 0
user_failed = 0


class UserLeft(Percentage):
    def update(self, pbar):
        return "%s users left, %s users failed." % (user_left, user_failed)


def parse_user(user):
    d = DeltaCrawler(user)
    d.run()
    progress_bar.next()
    global user_left
    user_left -= 1
    if user.parsed is not True:
        global user_failed
        user_failed += 1


def parse(users):
    pool_size = 20
    progress_bar.start()
    if users.__len__() < pool_size:
        pool_size = users.__len__()
    pool = lib.threadpool.ThreadPool(pool_size)
    requests = lib.threadpool.makeRequests(parse_user, users)
    [pool.putRequest(req) for req in requests]
    pool.wait()
    progress_bar.finish()


if __name__ == "__main__":
    MAX_RETRY_TIME = 10
    users = User.read_user_from_file("acctlist.txt")
    parsing_users = copy.copy(users)
    retry_time = MAX_RETRY_TIME
    while parsing_users.__len__() > 0 and retry_time > 0:
        user_left = parsing_users.__len__()
        user_failed = 0
        retry_time -= 1
        if retry_time == MAX_RETRY_TIME - 1:
            left = "Parsing..."
        else:
            left = "Retrying " + str(MAX_RETRY_TIME - retry_time - 1) + " time..."
        widget = [left, Percentage(), Bar(">"), UserLeft()]
        progress_bar = ProgressBar(maxval=users.__len__(), widgets=widget)
        parse(parsing_users)
        parsing_users = [user for user in parsing_users if user.parsed is False]
    with open("result.txt", "w") as out:
        for user in users:
            out.write(user.__str__() + "\n")
