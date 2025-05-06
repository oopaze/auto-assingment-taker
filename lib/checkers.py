import re
from lib.assignment import Assignment


class BaseAssignmentChecker:
    def check(assignment: Assignment) -> bool:
        raise NotImplementedError("Subclasses should implement this method.")


class BossPowerAssigmentChecker(BaseAssignmentChecker):
    MIN_PRICE = 5

    def check(self, assignment: Assignment) -> bool:
        title_has_boss_power = "boss power" in assignment.title.lower()
        description_has_seasonal = "seasonal softcore" in assignment.description.lower()
        price_is_cheap = assignment.price >= self.MIN_PRICE
        return title_has_boss_power and description_has_seasonal and price_is_cheap
    

class LairBossKillAssignmentChecker(BaseAssignmentChecker):
    MIN_PRICE = 5
    MAX_BOSS_KILLS = 15

    def extract_boss_kills(self, description: str) -> int | None:
        match = re.search(r"boss kills:\s*(\d+)", description.lower())
        return int(match.group(1)) if match else None

    def check(self, assignment: Assignment) -> bool:
        title_is_correct = assignment.title.strip().lower() == "lair boss kill"
        description_lower = assignment.description.lower()

        description_has_seasonal = "seasonal softcore" in description_lower
        description_has_belial = "select the boss: belial" in description_lower
        boss_kills = self.extract_boss_kills(description_lower)
        boss_kills_ok = boss_kills is not None and boss_kills <= self.MAX_BOSS_KILLS
        price_is_ok = assignment.price > self.MIN_PRICE

        return (
            title_is_correct and
            description_has_seasonal and
            description_has_belial and
            boss_kills_ok and
            price_is_ok
        )