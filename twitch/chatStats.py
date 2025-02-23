from vars.direction import Direction


class ChatStats:
    def __init__(self):
        self.leaderboard = {}
        self.leader_list = []
        self.curr_votes = {
            Direction.UP: [],
            Direction.RIGHT: [],
            Direction.DOWN: [],
            Direction.LEFT: []
        }

    def reset(self):
        self.leaderboard = {}
        self.leader_list = []
        self.reset_votes()

    def reset_votes(self):
        self.curr_votes = {
            Direction.UP: [],
            Direction.RIGHT: [],
            Direction.DOWN: [],
            Direction.LEFT: []
        }

    def add_vote(self, direction, user):
        if user not in self.curr_votes[direction]:
            self.curr_votes[direction].append(user)

    def get_vote_count(self, direction):
        return len(self.curr_votes[direction])

    def can_vote(self, user):
        for dir in self.curr_votes.values():
            if user in dir:
                return False
        return True

    def vote_won(self, direction):
        for user in self.curr_votes[direction]:
            if self.leaderboard.get(user) is not None:
                self.leaderboard[user] += 1
            else:
                self.leaderboard[user] = 1
        self.leader_list = sorted(self.leaderboard.items(), key=lambda item: item[1], reverse=True)
        self.reset_votes()
