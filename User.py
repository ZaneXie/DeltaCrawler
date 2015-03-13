__author__ = 'xiezj'


class User(object):
    def __init__(self, line=None):
        self.type = "DL"
        self.login_name = ""
        self.password = ""
        self.miles = 0
        self.current_miles = 0
        self.MQM = 0
        self.current_MQM = 0
        self.status = ""
        self.expriration = "null"
        self.name = ""
        self.gender = ""
        self.day_of_birth = ""
        self.address = ""
        self.phone = ""
        self.email = ""
        self.parsed = False
        if line is not None:
            self.read(line)

    def read(self, line):
        params = line.split("\t")
        self.type = params[0]
        self.login_name = params[1]
        self.password = params[2]
        if params.__len__() > 3:
            self.current_miles = int(params[3])
        if params.__len__() > 4:
            self.current_miles = int(params[4])

    def __str__(self):
        attr = [
            self.type,
            self.login_name,
            self.password,
            str(self.miles),
            str(self.current_miles),
            str(self.current_miles - self.miles),
            str(self.MQM),
            str(self.current_MQM),
            str(self.current_MQM - self.MQM),
            self.status,
            self.expriration,
            self.name,
            self.gender,
            self.day_of_birth,
            self.address,
            self.phone,
            self.email
        ]
        return "\t".join(attr)

    @staticmethod
    def read_user_from_file(filename):
        users = []
        with open(filename) as file:
            for line in file:
                if line.__len__() > 0:
                    user = User(line)
                    users.append(user)
        return users
