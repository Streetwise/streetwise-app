"""
API Models
"""

from datetime import datetime

class VoteClass(object):
    def __init__(self):
        self.counter = 0
        self.user_id = 0
        self.votes = []

    def get(self, id):
        for vote in self.votes:
            if vote['id'] == id:
                return vote
        api.abort(404, "Vote {} doesn't exist".format(id))

    def create(self, data):
        vote = data
        vote['timestamp'] = datetime.utcnow().isoformat()
        vote['id'] = self.counter = self.counter + 1
        self.votes.append(vote)
        return vote

    def update(self, id, data):
        vote = self.get(id)
        vote.update(data)
        return vote

    def delete(self, id):
        vote = self.get(id)
        self.votes.remove(todo)
