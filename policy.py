from enum import Enum
class PolicyType(Enum):
    RANDOM = 0
    GREEDY = 1
    EXPLOIT = 2
class Policy:
    def __init__(self,type):
        self.policyType = type
    def switchPolicy(self, type):
        self.policyType = type
    def getName(self):
        return str(self.policyType.name)